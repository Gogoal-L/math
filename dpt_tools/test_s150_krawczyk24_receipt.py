"""Fail-closed tests for the S150 24-row center-receipt arithmetic interface."""
from __future__ import annotations

import hashlib
import json
import tempfile
import zipfile
from unittest.mock import patch
import unittest
from fractions import Fraction
from pathlib import Path

import s150_krawczyk24_receipt as receipt_module

from s150_krawczyk24_receipt import (
    EXPECTED_COLUMN_ORDER,
    NONCENTER_SCHEMA,
    REQUIRED_GUARDS,
    SCHEMA,
    audit_receipt,
    _verify_noncenter_receipt,
)


def synthetic_receipt() -> dict:
    rows = [
        {"id": f"KCL_{i:02d}", "kind": "KCL", "unit": "A",
         "source_expression": f"synthetic:KCL_{i:02d}"}
        for i in range(22)
    ] + [
        {"id": "BODY_Q1", "kind": "BODY", "unit": "V", "source_expression": "synthetic:BODY_Q1"},
        {"id": "BODY_Q2", "kind": "BODY", "unit": "V", "source_expression": "synthetic:BODY_Q2"},
    ]
    one, zero = float(1).hex(), float(0).hex()
    identity = [[one if i == j else zero for j in range(24)] for i in range(24)]
    df = [{"value": "1e-10", "unit": row["unit"]} for row in rows]
    dx = []
    for source_index in EXPECTED_COLUMN_ORDER:
        if source_index in (22, 18, 23, 24):
            value = "0.000014"
        elif source_index in (16, 17, 21, 15, 14, 0, 13):
            value = "0.000011"
        else:
            value = "0.000008"
        dx.append({"value": value, "unit": "V"})
    x1 = [{"value": "0.000001", "unit": "V"} for _ in range(24)]
    guards = []
    for guard_id, (relation, unit) in REQUIRED_GUARDS.items():
        expression = f"synthetic:{guard_id}"
        if relation == "strict_positive":
            guard = {"id": guard_id, "unit": unit, "relation": relation,
                     "interval": ["1", "2"], "source_expression": expression}
        elif relation == "strict_negative":
            guard = {"id": guard_id, "unit": unit, "relation": relation,
                     "interval": ["-2", "-1"], "source_expression": expression}
        else:
            guard = {"id": guard_id, "unit": unit, "relation": relation,
                     "interval": ["0.25", "0.75"], "open_bounds": ["0", "1"],
                     "source_expression": expression}
        guards.append(guard)
    return {
        "schema": SCHEMA,
        "mode": "synthetic",
        "image_normalization": "coordinatewise_D_x",
        "row_order": rows,
        "column_order": list(EXPECTED_COLUMN_ORDER),
        "F_center_intervals": [["-1e-12", "1e-12"] for _ in range(24)],
        "R_binary64_hex": identity,
        "D_F": df,
        "D_x": dx,
        "X1_radius": x1,
        "noncenter_image_radius_upper_normalized": ["0.1" for _ in range(24)],
        "claimed_final_image_margin_lower_normalized": ["0.8" for _ in range(24)],
        "guard_intervals": guards,
    }


class S150Krawczyk24ReceiptTests(unittest.TestCase):
    def test_synthetic_center_receipt_passes_but_is_not_source_certificate(self):
        result = audit_receipt(synthetic_receipt())
        self.assertEqual(result["status"], "SYNTHETIC_PASS_ONLY")
        self.assertEqual(result["row_counts"], {"KCL_A": 22, "BODY_V": 2})
        self.assertTrue(all(Fraction(x) > 0 for x in result["computed_image_margin_lower_normalized"]))
        self.assertIn("does not", result["claim_ceiling"])
        self.assertIn("SYNTHETIC_PASS_ONLY is never source evidence", result["claim_ceiling"])

    def test_missing_body_row_and_mixed_unit_scale_fail_closed(self):
        receipt = synthetic_receipt()
        receipt["row_order"][-1] = {
            "id": "KCL_EXTRA", "kind": "KCL", "unit": "A",
            "source_expression": "synthetic:KCL_EXTRA",
        }
        with self.assertRaisesRegex(ValueError, "22 KCL/A and 2 BODY/V"):
            audit_receipt(receipt)

        receipt = synthetic_receipt()
        receipt["D_F"][-1]["unit"] = "A"
        with self.assertRaisesRegex(ValueError, "D_F unit mismatch"):
            audit_receipt(receipt)

    def test_reordered_or_missing_coordinate_fails_closed(self):
        receipt = synthetic_receipt()
        receipt["column_order"][0], receipt["column_order"][1] = (
            receipt["column_order"][1], receipt["column_order"][0]
        )
        with self.assertRaisesRegex(ValueError, "column_order"):
            audit_receipt(receipt)

    def test_overstated_image_margin_fails_closed(self):
        receipt = synthetic_receipt()
        receipt["claimed_final_image_margin_lower_normalized"] = ["0.95" for _ in range(24)]
        with self.assertRaisesRegex(ValueError, "overstates exact arithmetic"):
            audit_receipt(receipt)

    def test_missing_guard_fails_closed(self):
        receipt = synthetic_receipt()
        receipt["guard_intervals"].pop()
        with self.assertRaisesRegex(ValueError, "guard coverage mismatch"):
            audit_receipt(receipt)

    def test_source_mode_with_absent_artifacts_never_promotes_receipt(self):
        receipt = synthetic_receipt()
        receipt["mode"] = "source"
        with tempfile.TemporaryDirectory() as root:
            result = audit_receipt(receipt, root=root)
        self.assertEqual(result["status"], "SOURCE_INPUTS_UNAVAILABLE")
        self.assertNotEqual(result["status"], "SOURCE_INPUTS_HASHED_CENTER_ARITHMETIC_PASS_ONLY")
        self.assertIn("source_artifact_check", result)

    def test_source_mode_needs_s150_archive_not_unrelated_d15_target_and_disclaims_provenance(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            archive_path = root_path / "source_inputs/s150/original_submission.zip"
            archive_path.parent.mkdir(parents=True)
            with zipfile.ZipFile(archive_path, "w"):
                pass
            archive_sha = hashlib.sha256(archive_path.read_bytes()).hexdigest()

            noncenter_path = root_path / "noncenter.json"
            noncenter_payload = {
                "schema": NONCENTER_SCHEMA,
                "noncenter_image_radius_upper_normalized": ["0.1" for _ in range(24)],
            }
            noncenter_path.write_text(json.dumps(noncenter_payload), encoding="utf-8")
            noncenter_sha = hashlib.sha256(noncenter_path.read_bytes()).hexdigest()

            receipt = synthetic_receipt()
            receipt["mode"] = "source"
            receipt["noncenter_receipt"] = {
                "path": "noncenter.json",
                "sha256": noncenter_sha,
            }
            with patch.dict(
                receipt_module.SOURCE_ARTIFACT_SHA256,
                {"source_inputs/s150/original_submission.zip": archive_sha},
                clear=True,
            ), patch.dict(receipt_module.SOURCE_ARCHIVE_MEMBER_SHA256, {}, clear=True):
                result = audit_receipt(receipt, root=root)
                receipt_path = root_path / "center.json"
                receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
                self.assertEqual(
                    receipt_module.main([str(receipt_path), "--root", str(root_path)]), 0
                )

        self.assertEqual(result["status"], "SOURCE_INPUTS_HASHED_CENTER_ARITHMETIC_PASS_ONLY")
        self.assertEqual(result["noncenter_receipt_status"], "NONCENTER_RECEIPT_HASHED")
        self.assertEqual(result["source_interval_provenance"], "NOT_VALIDATED")
        self.assertEqual(result["source_artifact_check"]["missing"], [])
        self.assertIn("does not derive or validate", result["claim_ceiling"])

    def test_ambiguous_or_legacy_physical_unit_fields_fail_closed(self):
        receipt = synthetic_receipt()
        receipt.pop("image_normalization")
        with self.assertRaisesRegex(ValueError, "image_normalization must be"):
            audit_receipt(receipt)

        receipt = synthetic_receipt()
        receipt["noncenter_image_radius_upper"] = receipt.pop(
            "noncenter_image_radius_upper_normalized"
        )
        with self.assertRaisesRegex(ValueError, "noncenter_image_radius_upper_normalized"):
            audit_receipt(receipt)

    def test_normalized_radii_are_explicitly_dimensionless(self):
        receipt = synthetic_receipt()
        self.assertEqual(receipt["image_normalization"], "coordinatewise_D_x")
        self.assertIn("noncenter_image_radius_upper_normalized", receipt)
        self.assertIn("claimed_final_image_margin_lower_normalized", receipt)
        result = audit_receipt(receipt)
        self.assertTrue(all(
            Fraction(x) > 0 for x in result["computed_image_margin_lower_normalized"]
        ))

    def test_noncenter_receipt_requires_v2_normalized_field(self):
        normalized = ["0.1" for _ in range(24)]
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "noncenter.json"
            payload = {
                "schema": NONCENTER_SCHEMA,
                "noncenter_image_radius_upper_normalized": normalized,
            }
            path.write_text(json.dumps(payload), encoding="utf-8")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            receipt = {"noncenter_receipt": {"path": "noncenter.json", "sha256": digest}}
            self.assertEqual(
                _verify_noncenter_receipt(receipt, Path(root), [Fraction(1, 10)] * 24),
                "NONCENTER_RECEIPT_HASHED",
            )

            payload = {
                "schema": NONCENTER_SCHEMA,
                "noncenter_image_radius_upper": normalized,
            }
            path.write_text(json.dumps(payload), encoding="utf-8")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            receipt = {"noncenter_receipt": {"path": "noncenter.json", "sha256": digest}}
            self.assertEqual(
                _verify_noncenter_receipt(receipt, Path(root), [Fraction(1, 10)] * 24),
                "NONCENTER_RECEIPT_INVALID",
            )


if __name__ == "__main__":
    unittest.main()
