#!/usr/bin/env python3
"""Audit every inverse occurrence in a sampled rational/matrix expression tree.

Definedness is checked on the original expression path. Algebraic
simplification is deliberately not used to erase an undefined intermediate
inverse. This is a mechanical sampled-domain auditor, not a proof that an
inverse stays defined on a continuous command domain.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


class UndefinedInverse(RuntimeError):
    pass


def _to_array(value: Any) -> np.ndarray:
    arr = np.asarray(value, dtype=float)
    if arr.ndim > 2:
        raise ValueError(f"only scalars, vectors and matrices are supported, got {arr.shape}")
    return arr


def _inverse_metrics(value: np.ndarray, rtol: float, atol: float) -> dict[str, Any]:
    arr = np.asarray(value, dtype=float)
    if arr.ndim == 0:
        mag = abs(float(arr))
        threshold = max(atol, rtol * mag)
        defined = mag > threshold
        return {
            "kind": "scalar",
            "abs_value": mag,
            "threshold": threshold,
            "defined": defined,
            "condition_number_2norm": 1.0 if defined else float("inf"),
        }
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError(f"inverse requires a scalar or square matrix, got {arr.shape}")
    s = np.linalg.svd(arr, compute_uv=False)
    smax = float(s[0]) if s.size else 0.0
    smin = float(s[-1]) if s.size else 0.0
    threshold = max(atol, rtol * smax)
    defined = smin > threshold
    cond = float(smax / smin) if defined and smin > 0 else float("inf")
    return {
        "kind": "matrix",
        "shape": list(arr.shape),
        "singular_values": s.tolist(),
        "min_singular_value": smin,
        "max_singular_value": smax,
        "threshold": threshold,
        "defined": defined,
        "condition_number_2norm": cond,
    }


def evaluate(node: Any, env: dict[str, np.ndarray], log: list[dict[str, Any]], sample_id: str, rtol: float, atol: float) -> np.ndarray:
    if not isinstance(node, dict) or "op" not in node:
        raise ValueError("each expression node must be an object with an 'op' field")
    op = node["op"]

    if op == "const":
        return _to_array(node["value"])
    if op == "var":
        name = node["name"]
        if name not in env:
            raise KeyError(f"missing variable {name!r} in sample {sample_id}")
        return env[name]
    if op == "eye":
        n = int(node["n"])
        return np.eye(n)
    if op == "neg":
        return -evaluate(node["arg"], env, log, sample_id, rtol, atol)

    if op in {"add", "sub", "mul", "matmul"}:
        args = node.get("args")
        if not isinstance(args, list) or len(args) < 2:
            raise ValueError(f"{op} requires at least two args")
        vals = [evaluate(x, env, log, sample_id, rtol, atol) for x in args]
        out = vals[0]
        for rhs in vals[1:]:
            if op == "add":
                out = out + rhs
            elif op == "sub":
                out = out - rhs
            elif op == "mul":
                out = out * rhs
            else:
                out = out @ rhs
        return out

    if op == "inv":
        value = evaluate(node["arg"], env, log, sample_id, rtol, atol)
        metrics = _inverse_metrics(value, rtol, atol)
        entry = {
            "sample_id": sample_id,
            "label": str(node.get("label", "<unlabeled inverse>")),
            **metrics,
        }
        log.append(entry)
        if not metrics["defined"]:
            raise UndefinedInverse(
                f"inverse {entry['label']!r} undefined/ill-conditioned at sample {sample_id}"
            )
        if value.ndim == 0:
            return np.asarray(1.0 / float(value))
        return np.linalg.inv(value)

    raise ValueError(f"unsupported op {op!r}")


def audit(expression: dict[str, Any], samples: list[dict[str, Any]], rtol: float, atol: float) -> dict[str, Any]:
    inverse_log: list[dict[str, Any]] = []
    sample_results: list[dict[str, Any]] = []
    for idx, sample in enumerate(samples):
        sample_id = str(sample.get("id", idx))
        values = sample.get("vars", sample)
        if "id" in values and values is sample:
            values = {k: v for k, v in values.items() if k != "id"}
        env = {name: _to_array(value) for name, value in values.items()}
        try:
            result = evaluate(expression, env, inverse_log, sample_id, rtol, atol)
            sample_results.append({
                "sample_id": sample_id,
                "defined": True,
                "result_shape": list(result.shape),
                "result_norm_2": float(np.linalg.norm(result, ord=2)) if result.ndim == 2 else float(np.linalg.norm(result)),
            })
        except UndefinedInverse as exc:
            sample_results.append({"sample_id": sample_id, "defined": False, "error": str(exc)})

    by_label: dict[str, dict[str, Any]] = {}
    for entry in inverse_log:
        label = entry["label"]
        agg = by_label.setdefault(label, {
            "samples_checked": 0,
            "undefined_samples": [],
            "worst_condition_number_2norm": 0.0,
            "minimum_singular_margin": float("inf"),
        })
        agg["samples_checked"] += 1
        if not entry["defined"]:
            agg["undefined_samples"].append(entry["sample_id"])
        cond = float(entry["condition_number_2norm"])
        agg["worst_condition_number_2norm"] = max(float(agg["worst_condition_number_2norm"]), cond)
        if entry["kind"] == "scalar":
            margin = float(entry["abs_value"] - entry["threshold"])
        else:
            margin = float(entry["min_singular_value"] - entry["threshold"])
        agg["minimum_singular_margin"] = min(float(agg["minimum_singular_margin"]), margin)

    all_defined = all(x["defined"] for x in sample_results)
    return {
        "schema_version": 1,
        "all_samples_defined": all_defined,
        "sample_results": sample_results,
        "inverse_occurrences": inverse_log,
        "inverse_summary_by_label": by_label,
        "claim_ceiling": (
            "Passing this sampled audit proves definedness only at the supplied samples. "
            "Continuous-domain closure requires an analytic/interval/optimization bound on each inverse occurrence."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expression", type=Path, help="JSON expression tree")
    parser.add_argument("samples", type=Path, help="JSON list of variable samples")
    parser.add_argument("--output", type=Path, help="JSON output path; defaults to stdout")
    parser.add_argument("--rtol", type=float, default=1e-10)
    parser.add_argument("--atol", type=float, default=1e-12)
    args = parser.parse_args()

    expression = json.loads(args.expression.read_text(encoding="utf-8"))
    samples = json.loads(args.samples.read_text(encoding="utf-8"))
    if not isinstance(samples, list):
        raise ValueError("samples JSON must be a list")
    report = audit(expression, samples, args.rtol, args.atol)
    payload = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0 if report["all_samples_defined"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
