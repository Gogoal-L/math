#!/usr/bin/env python3
"""Fail-closed arithmetic checker for an S150 24-row Krawczyk center receipt.

This validates exact arithmetic for the supplied center residual intervals and
checks claimed noncenter margins and named guard intervals. It does not derive
the noncenter bound from a Jacobian, prove interval endpoints outward, or
certify a source root. Decimal values are strings interpreted exactly;
preconditioner entries are exact binary64 values encoded with float.hex().
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import zipfile
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from pathlib import Path
from typing import Any

SCHEMA = "s150.krawczyk24-center/v1"
NONCENTER_SCHEMA = "s150.krawczyk24-noncenter/v1"

EXPECTED_COLUMN_ORDER = (
    0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
    21, 22, 23, 24, 25, 40, 41,
)
X2_WIDE_RADIUS_INDICES = frozenset((22, 18, 23, 24))
X2_MID_RADIUS_INDICES = frozenset((16, 17, 21, 15, 14, 0, 13))
X1_RADIUS = Fraction(1, 1_000_000)

# These inputs are hash-verified in the local read-only master workspace but
# are not currently present in the remote Math tree. No source calculation is
# allowed to run until their exact bytes are made available to the cloud runner.
SOURCE_ARTIFACT_SHA256 = {
    "source_inputs/s150/original_submission.zip":
        "250aa4ea17514ffdeda3a51d95bedf8e034b181f97bdc254db29ddc36281b9c8",
    "source_inputs/s150/pro18c_prediction_extension.npz":
        "af7299434d7dcde687da3bf56b5ce31babbc4e0c1c0e12b1a849b5f5530ae8fd",
}
SOURCE_ARCHIVE_MEMBER_SHA256 = {
    "analysis/actual_law.py":
        "51b78f729393d29745f59ca150adfef69e1847bf26a8853c6cef3d6be9e2083d",
    "geometry.npz":
        "23e30e057e0f8eddcd83d48d2947c454bd2a2e6cf438814d590bd24b2c46851e",
    "information/source_crosscommand.npz":
        "2f13b10fcf24b81c09d5c625941abd12ff2c2d0aab5f017b7fdc7dfc38f7244e",
}

# Each entry is (required interval relation, unit). The caller must supply
# source-expression references and outward intervals; this checker does not
# derive the guard functions from actual_law.py.
REQUIRED_GUARDS = {
    "G11_Q1_LEFT": ("strict_positive", "A"),
    "G11_Q1_RIGHT": ("strict_negative", "A"),
    "G11_Q2_LEFT": ("strict_positive", "A"),
    "G11_Q2_RIGHT": ("strict_negative", "A"),
    "HEAT_Q1": ("strict_negative", "A"),
    "HEAT_Q2": ("strict_negative", "A"),
    "G2_MODE": ("inside_open", "V"),
    "ETH_MODE": ("inside_open", "V"),
    "DIODE_Q1": ("strict_positive", "A"),
    "DIODE_Q2": ("strict_positive", "A"),
    "THERMAL_Q1": ("inside_open", "C"),
    "THERMAL_Q2": ("inside_open", "C"),
}

CLAIM_CEILING = (
    "Arithmetic receipt validation only. This does not derive or validate the "
    "claimed noncenter image radius from interval Jacobians, prove that interval "
    "endpoints enclose the source law, establish root existence, cover other "
    "branches or time steps, validate a native solver, or certify any Goal27 "
    "source-wide signed-work diameter. SYNTHETIC_PASS_ONLY is never source evidence."
)


def _fraction(value: Any, label: str) -> Fraction:
    if not isinstance(value, str):
        raise ValueError(f"{label} must be an exact decimal string")
    try:
        decimal = Decimal(value)
    except InvalidOperation:
        raise ValueError(f"{label} is not a decimal string") from None
    if not decimal.is_finite():
        raise ValueError(f"{label} must be finite")
    return Fraction(decimal)


def _interval(value: Any, label: str) -> tuple[Fraction, Fraction]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{label} must be [lower, upper]")
    lower = _fraction(value[0], f"{label}.lower")
    upper = _fraction(value[1], f"{label}.upper")
    if lower > upper:
        raise ValueError(f"{label} has reversed endpoints")
    return lower, upper


def _vector(value: Any, label: str, parser) -> list:
    if not isinstance(value, list) or len(value) != 24:
        raise ValueError(f"{label} must contain exactly 24 ordered entries")
    return [parser(item, f"{label}[{i}]") for i, item in enumerate(value)]


def _scale_vector(value: Any, label: str, units: list[str]) -> list[Fraction]:
    if not isinstance(value, list) or len(value) != 24:
        raise ValueError(f"{label} must contain exactly 24 ordered scales")
    result = []
    for i, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"{label}[{i}] must contain value and unit")
        scale = _fraction(item.get("value"), f"{label}[{i}].value")
        if scale <= 0:
            raise ValueError(f"{label}[{i}] must be strictly positive")
        if item.get("unit") != units[i]:
            raise ValueError(
                f"{label} unit mismatch at row/coordinate {i}: "
                f"expected {units[i]}, got {item.get('unit')}"
            )
        result.append(scale)
    return result


def _expected_x2_radius(source_index: int) -> Fraction:
    if source_index in X2_WIDE_RADIUS_INDICES:
        return Fraction(14, 1_000_000)
    if source_index in X2_MID_RADIUS_INDICES:
        return Fraction(11, 1_000_000)
    return Fraction(8, 1_000_000)


def _parse_preconditioner(value: Any) -> list[list[Fraction]]:
    if not isinstance(value, list) or len(value) != 24:
        raise ValueError("R_binary64_hex must have 24 ordered rows")
    matrix = []
    for i, row in enumerate(value):
        if not isinstance(row, list) or len(row) != 24:
            raise ValueError(f"R_binary64_hex[{i}] must have 24 entries")
        parsed = []
        for j, item in enumerate(row):
            if not isinstance(item, str):
                raise ValueError(f"R_binary64_hex[{i}][{j}] must be float.hex() text")
            try:
                number = float.fromhex(item)
            except ValueError:
                raise ValueError(f"R_binary64_hex[{i}][{j}] is not float.hex() text") from None
            if not math.isfinite(number):
                raise ValueError(f"R_binary64_hex[{i}][{j}] must be finite")
            parsed.append(Fraction.from_float(number))
        matrix.append(parsed)
    return matrix


def _validate_rows(value: Any) -> tuple[list[dict], list[str]]:
    if not isinstance(value, list) or len(value) != 24:
        raise ValueError("row_order must contain exactly 24 explicit rows")
    rows = []
    ids = []
    counts = {"KCL": 0, "BODY": 0}
    for i, row in enumerate(value):
        if not isinstance(row, dict):
            raise ValueError(f"row_order[{i}] must be an object")
        row_id, kind, unit = row.get("id"), row.get("kind"), row.get("unit")
        if not isinstance(row_id, str) or not row_id.strip():
            raise ValueError(f"row_order[{i}] needs a nonempty id")
        if row_id in ids:
            raise ValueError(f"duplicate residual row id: {row_id}")
        if kind not in ("KCL", "BODY"):
            raise ValueError(f"unsupported residual kind at {row_id}: {kind}")
        expected_unit = "A" if kind == "KCL" else "V"
        if unit != expected_unit:
            raise ValueError(f"row unit mismatch at {row_id}: expected {expected_unit}")
        expression = row.get("source_expression")
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError(f"row {row_id} needs a source_expression reference")
        ids.append(row_id)
        counts[kind] += 1
        rows.append({
            "id": row_id, "kind": kind, "unit": unit,
            "source_expression": expression,
        })
    if counts != {"KCL": 22, "BODY": 2}:
        raise ValueError("row_order must contain exactly 22 KCL/A and 2 BODY/V rows")
    return rows, [row["unit"] for row in rows]


def _validate_guards(value: Any) -> list[dict]:
    if not isinstance(value, list):
        raise ValueError("guard_intervals must be a list")
    by_id = {}
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("each guard interval must be an object")
        guard_id = item.get("id")
        if not isinstance(guard_id, str) or guard_id in by_id:
            raise ValueError(f"guard id is missing or duplicated: {guard_id}")
        by_id[guard_id] = item
    if set(by_id) != set(REQUIRED_GUARDS):
        missing = sorted(set(REQUIRED_GUARDS) - set(by_id))
        extra = sorted(set(by_id) - set(REQUIRED_GUARDS))
        raise ValueError(f"guard coverage mismatch; missing={missing}, extra={extra}")

    validated = []
    for guard_id, (expected_relation, expected_unit) in REQUIRED_GUARDS.items():
        item = by_id[guard_id]
        relation = item.get("relation")
        unit = item.get("unit")
        if relation != expected_relation:
            raise ValueError(
                f"guard relation mismatch at {guard_id}: expected {expected_relation}"
            )
        if unit != expected_unit:
            raise ValueError(
                f"guard unit mismatch at {guard_id}: expected {expected_unit}"
            )
        expression = item.get("source_expression")
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError(f"guard {guard_id} needs a source_expression reference")
        lower, upper = _interval(item.get("interval"), f"guard {guard_id}.interval")
        if relation == "strict_positive" and lower <= 0:
            raise ValueError(f"guard {guard_id} is not strictly positive")
        if relation == "strict_negative" and upper >= 0:
            raise ValueError(f"guard {guard_id} is not strictly negative")
        if relation == "inside_open":
            open_lower, open_upper = _interval(
                item.get("open_bounds"), f"guard {guard_id}.open_bounds"
            )
            if not (open_lower < lower <= upper < open_upper):
                raise ValueError(f"guard {guard_id} is not strictly inside its open bounds")
        validated.append({
            "id": guard_id,
            "relation": relation,
            "unit": unit,
            "interval": [_fraction_text(lower), _fraction_text(upper)],
            "status": "STRICT_INTERVAL_CHECK_PASS",
        })
    return validated


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _safe_path(root: Path, relative: Any, label: str) -> Path:
    if not isinstance(relative, str) or not relative:
        raise ValueError(f"{label} must be a nonempty relative path")
    path = Path(relative)
    if path.is_absolute():
        raise ValueError(f"{label} must be relative to the repository root")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f"{label} escapes the repository root")
    return resolved


def verify_source_artifacts(root: str | Path | None = None) -> dict:
    """Verify pinned source-input identities only; never runs source physics."""
    root_path = Path(root or Path(__file__).resolve().parents[1]).resolve()
    missing = []
    mismatches = []
    for relative, expected in SOURCE_ARTIFACT_SHA256.items():
        path = _safe_path(root_path, relative, "source artifact path")
        if not path.is_file():
            missing.append(relative)
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            mismatches.append({"path": relative, "expected": expected, "actual": actual})

    archive_relative = "source_inputs/s150/original_submission.zip"
    archive_path = _safe_path(root_path, archive_relative, "source archive path")
    if archive_path.is_file() and not any(x["path"] == archive_relative for x in mismatches):
        try:
            with zipfile.ZipFile(archive_path) as archive:
                names = set(archive.namelist())
                for member, expected in SOURCE_ARCHIVE_MEMBER_SHA256.items():
                    if member not in names:
                        missing.append(f"{archive_relative}!/{member}")
                        continue
                    actual = hashlib.sha256(archive.read(member)).hexdigest()
                    if actual != expected:
                        mismatches.append({
                            "path": f"{archive_relative}!/{member}",
                            "expected": expected,
                            "actual": actual,
                        })
        except (OSError, zipfile.BadZipFile):
            mismatches.append({
                "path": archive_relative,
                "expected": SOURCE_ARTIFACT_SHA256[archive_relative],
                "actual": "UNREADABLE_OR_INVALID_ZIP",
            })

    if mismatches:
        status = "SOURCE_INPUT_HASH_MISMATCH"
    elif missing:
        status = "SOURCE_INPUTS_UNAVAILABLE"
    else:
        status = "SOURCE_INPUTS_HASHED_IDENTITY_ONLY"
    return {"status": status, "missing": sorted(set(missing)), "mismatches": mismatches}


def _verify_noncenter_receipt(receipt: dict, root: Path, expected_values: list[Fraction]) -> str:
    reference = receipt.get("noncenter_receipt")
    if not isinstance(reference, dict):
        return "NONCENTER_RECEIPT_UNAVAILABLE"
    relative = reference.get("path")
    expected_hash = reference.get("sha256")
    if not isinstance(expected_hash, str) or len(expected_hash) != 64:
        raise ValueError("noncenter_receipt.sha256 must be a 64-character SHA256")
    path = _safe_path(root, relative, "noncenter_receipt.path")
    if not path.is_file():
        return "NONCENTER_RECEIPT_UNAVAILABLE"
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual_hash != expected_hash.lower():
        return "NONCENTER_RECEIPT_HASH_MISMATCH"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "NONCENTER_RECEIPT_INVALID"
    if not isinstance(payload, dict) or payload.get("schema") != NONCENTER_SCHEMA:
        return "NONCENTER_RECEIPT_INVALID"
    try:
        values = _vector(
            payload.get("noncenter_image_radius_upper"),
            "noncenter_receipt.noncenter_image_radius_upper",
            _fraction,
        )
    except ValueError:
        return "NONCENTER_RECEIPT_INVALID"
    if values != expected_values:
        return "NONCENTER_RECEIPT_CONTENT_MISMATCH"
    return "NONCENTER_RECEIPT_HASHED"


def audit_receipt(receipt: dict, *, root: str | Path | None = None) -> dict:
    """Validate center-image arithmetic and the consistency of supplied margins."""
    if not isinstance(receipt, dict) or receipt.get("schema") != SCHEMA:
        raise ValueError(f"receipt schema must be {SCHEMA}")
    mode = receipt.get("mode")
    if mode not in ("synthetic", "source"):
        raise ValueError("mode must be synthetic or source")

    _, row_units = _validate_rows(receipt.get("row_order"))
    column_order = receipt.get("column_order")
    if not isinstance(column_order, list) or tuple(column_order) != EXPECTED_COLUMN_ORDER:
        raise ValueError("column_order does not match the pinned S-L26 retained-coordinate order")

    f_intervals = _vector(
        receipt.get("F_center_intervals"), "F_center_intervals", _interval
    )
    preconditioner = _parse_preconditioner(receipt.get("R_binary64_hex"))
    d_f = _scale_vector(receipt.get("D_F"), "D_F", row_units)
    d_x = _scale_vector(receipt.get("D_x"), "D_x", ["V"] * 24)
    for i, source_index in enumerate(column_order):
        if d_x[i] != _expected_x2_radius(source_index):
            raise ValueError(
                f"D_x[{i}] must equal the pinned X2 radius for source coordinate {source_index}"
            )

    x1 = _scale_vector(receipt.get("X1_radius"), "X1_radius", ["V"] * 24)
    if any(radius != X1_RADIUS for radius in x1):
        raise ValueError("X1_radius must be 1 microV for each retained predecessor coordinate")

    noncenter = _vector(
        receipt.get("noncenter_image_radius_upper"),
        "noncenter_image_radius_upper",
        _fraction,
    )
    if any(value < 0 for value in noncenter):
        raise ValueError("noncenter image radii must be nonnegative")
    claimed_margin = _vector(
        receipt.get("claimed_final_image_margin_lower"),
        "claimed_final_image_margin_lower",
        _fraction,
    )
    if any(value <= 0 for value in claimed_margin):
        raise ValueError("claimed final image margins must be strictly positive")
    guard_results = _validate_guards(receipt.get("guard_intervals"))

    # Compute D_x^-1 R D_F times D_F^-1 F(center) exactly. R entries are
    # exact binary64 values from their hex strings; interval endpoints/scales
    # are exact decimal rationals. D_x is pinned to the X2 box radii.
    center_intervals = []
    center_radius = []
    for i in range(24):
        lower_sum = Fraction(0)
        upper_sum = Fraction(0)
        for j in range(24):
            r_hat = preconditioner[i][j] * d_f[j] / d_x[i]
            f_lower, f_upper = f_intervals[j]
            f_hat_lower, f_hat_upper = f_lower / d_f[j], f_upper / d_f[j]
            if r_hat >= 0:
                lower_sum += r_hat * f_hat_lower
                upper_sum += r_hat * f_hat_upper
            else:
                lower_sum += r_hat * f_hat_upper
                upper_sum += r_hat * f_hat_lower
        center_intervals.append((lower_sum, upper_sum))
        center_radius.append(max(abs(lower_sum), abs(upper_sum)))

    computed_margin = []
    for i in range(24):
        margin = Fraction(1) - noncenter[i] - center_radius[i]
        if margin <= 0:
            raise ValueError(
                f"center plus claimed noncenter image reaches X2 boundary at coordinate {i}"
            )
        if claimed_margin[i] > margin:
            raise ValueError(
                f"claimed final image margin overstates exact arithmetic at coordinate {i}"
            )
        computed_margin.append(margin)

    result = {
        "schema": SCHEMA,
        "status": "SYNTHETIC_PASS_ONLY" if mode == "synthetic" else None,
        "row_counts": {"KCL_A": 22, "BODY_V": 2},
        "center_image_interval_normalized": [
            [_fraction_text(lo), _fraction_text(hi)] for lo, hi in center_intervals
        ],
        "center_image_radius_upper_normalized": [_fraction_text(x) for x in center_radius],
        "noncenter_image_radius_upper_normalized": [_fraction_text(x) for x in noncenter],
        "computed_image_margin_lower_normalized": [_fraction_text(x) for x in computed_margin],
        "claimed_final_image_margin_lower_normalized": [_fraction_text(x) for x in claimed_margin],
        "guard_results": guard_results,
        "claim_ceiling": CLAIM_CEILING,
    }

    if mode == "source":
        root_path = Path(root or Path(__file__).resolve().parents[1]).resolve()
        source_status = verify_source_artifacts(root_path)
        if source_status["status"] != "SOURCE_INPUTS_HASHED_IDENTITY_ONLY":
            result["status"] = source_status["status"]
            result["source_artifact_check"] = source_status
        else:
            noncenter_status = _verify_noncenter_receipt(receipt, root_path, noncenter)
            result["status"] = (
                "SOURCE_RECEIPTS_HASHED_CENTER_ARITHMETIC_PASS_ONLY"
                if noncenter_status == "NONCENTER_RECEIPT_HASHED"
                else noncenter_status
            )
            result["source_artifact_check"] = source_status
            result["noncenter_receipt_status"] = noncenter_status
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path, help="JSON receipt following s150.krawczyk24-center/v1")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.receipt.read_text(encoding="utf-8"))
        result = audit_receipt(payload, root=args.root)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if result["status"] in (
        "SYNTHETIC_PASS_ONLY",
        "SOURCE_RECEIPTS_HASHED_CENTER_ARITHMETIC_PASS_ONLY",
    ):
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
