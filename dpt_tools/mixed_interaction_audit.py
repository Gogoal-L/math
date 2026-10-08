#!/usr/bin/env python3
"""Bounded mixed-intervention audit for one scalar DPT goal readout.

If F has a continuous mixed derivative on the rectangle joining (0,0) and
(a,b), and
 |F_ab(u,v) - F_ab(0,0)| <= M_a*|u| + M_b*|v|,
then the four-corner contrast divided by a*b estimates F_ab(0,0) with
bias at most (M_a*|a| + M_b*|b|)/2. With absolute numerical/measurement
errors eta on the four values, add sum(eta)/abs(a*b).

This is elementary finite-difference calculus, not a new theorem of an
OpenAI Math preprint. Input remainder and noise bounds are unverified.
One mixed query alone does NOT identify arbitrary cubic interaction laws.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

KEYS = ("f00", "fa0", "f0b", "fab")


def nonnegative(value: object, label: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{label} must be nonnegative and finite")
    return number


def nonzero(value: object, label: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number == 0:
        raise ValueError(f"{label} must be nonzero and finite")
    return number


def _params(raw: dict) -> tuple[float, float, dict[str, float]]:
    if not isinstance(raw, dict):
        raise ValueError("configuration must be a JSON object")
    bounds = raw.get("mixed_derivative_variation")
    if not isinstance(bounds, dict) or "alpha" not in bounds or "beta" not in bounds:
        raise ValueError("mixed_derivative_variation needs alpha and beta bounds")
    ma = nonnegative(bounds["alpha"], "M_alpha")
    mb = nonnegative(bounds["beta"], "M_beta")
    noise_raw = raw.get("absolute_readout_error")
    if not isinstance(noise_raw, dict) or set(noise_raw) != set(KEYS):
        raise ValueError(f"absolute_readout_error must have exactly {KEYS}")
    noise = {k: nonnegative(noise_raw[k], f"absolute_readout_error.{k}") for k in KEYS}
    return ma, mb, noise


def bound(a: float, b: float, ma: float, mb: float, noise: dict[str, float]) -> dict:
    a = nonzero(a, "alpha")
    b = nonzero(b, "beta")
    truncation = (ma * abs(a) + mb * abs(b)) / 2.0
    numerical = sum(noise.values()) / abs(a * b)
    radius = truncation + numerical
    if not math.isfinite(radius):
        raise ValueError("error bound overflowed; rescale variables")
    return {"alpha": a, "beta": b, "truncation_bound": truncation,
            "readout_error_bound": numerical, "total_bound": radius}


def audit(raw: dict) -> dict:
    ma, mb, noise = _params(raw)
    result = {
        "schema_version": 1,
        "claim_ceiling": (
            "Conditional scalar mixed-derivative coefficient interval, assuming "
            "specified C2 regularity, pointwise mixed-derivative variation on "
            "the complete query rectangle, correctly matched primitive anchors, "
            "and supplied absolute readout error bounds. None are verified by "
            "this tool. Not a native LTspice certificate."
        ),
        "assumption": "|F_ab(u,v)-F_ab(0,0)| <= M_alpha*|u|+M_beta*|v| on the complete rectangle",
        "readout_error_sum": sum(noise.values()),
    }
    if "samples" in raw:
        vals = raw["samples"]
        if not isinstance(vals, dict) or set(vals) != set(KEYS):
            raise ValueError(f"samples must contain exactly {KEYS}")
        samples = {k: float(vals[k]) for k in KEYS}
        if not all(math.isfinite(v) for v in samples.values()):
            raise ValueError("samples must be finite")
        score = bound(raw["alpha"], raw["beta"], ma, mb, noise)
        contrast = samples["fab"] - samples["fa0"] - samples["f0b"] + samples["f00"]
        center = contrast / (score["alpha"] * score["beta"])
        rad = score["total_bound"]
        lo, hi = center - rad, center + rad
        result["observation"] = {
            **score, "mixed_finite_difference": contrast,
            "central_mixed_derivative_estimate": center,
            "conditional_coefficient_interval": [lo, hi],
            "zero_excluded": bool(lo > 0 or hi < 0),
            "conditional_sign": "POSITIVE" if lo > 0 else ("NEGATIVE" if hi < 0 else "INCONCLUSIVE"),
        }
    if "candidate_amplitudes" in raw:
        candidates = raw["candidate_amplitudes"]
        if not isinstance(candidates, dict) or set(candidates) != {"alpha", "beta"}:
            raise ValueError("candidate_amplitudes needs alpha and beta lists")
        aa, bb = candidates["alpha"], candidates["beta"]
        if not isinstance(aa, list) or not isinstance(bb, list) or not aa or not bb:
            raise ValueError("candidate_amplitudes must contain nonempty lists")
        proposals = [bound(a, b, ma, mb, noise) for a in aa for b in bb]
        proposals.sort(key=lambda d: (d["total_bound"], abs(d["alpha"] * d["beta"]), d["alpha"], d["beta"]))
        result["candidate_design"] = {
            "best": proposals[0], "runner_ups": proposals[1:5],
            "criterion": "Minimize worst-case absolute central mixed-derivative estimation bound",
            "scope": "Only candidate amplitudes with valid rectangles, matched archive primitive anchors and certified error envelopes are admissible",
        }
    error_sum = sum(noise.values())
    if ma > 0 and mb > 0 and error_sum > 0:
        ra, rb = ma / 2.0, mb / 2.0
        t = (error_sum * ra * rb) ** (1.0 / 3.0)
        result["unconstrained_positive_optimum"] = {
            "abs_alpha": t / ra, "abs_beta": t / rb,
            "error_bound": 3 * t,
            "scope": "Mathematical optimum over unrestricted positive amplitudes; may be outside valid physical/derivative domain",
        }
    else:
        result["unconstrained_positive_optimum"] = None
    if "samples" not in raw and "candidate_amplitudes" not in raw:
        raise ValueError("supply samples and/or candidate_amplitudes")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON bounded four-corner acquisition inputs")
    parser.add_argument("--output", type=Path, help="optional JSON report")
    args = parser.parse_args()
    report = audit(json.loads(args.input.read_text(encoding="utf-8")))
    payload = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
