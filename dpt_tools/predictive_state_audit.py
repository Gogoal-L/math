#!/usr/bin/env python3
"""Mechanical audits for DPT goal-visible tangent information.

The script evaluates finite-dimensional linearized claims of the form

    K = ker(DO),
    N = K intersect ker(DG),
    r_G = dim(K / N),

and, when a candidate measurement derivative DP is supplied, checks the
first-order sufficiency condition

    ker(DP|_K) subseteq ker(DG|_K).

This is a numerical auditor, not a proof of finite-radius identifiability.
Only user-supplied observation, measurement and goal Taylor bounds can produce
a CONDITIONAL all-direction finite-radius formula. It is not a certified
native prediction statement without independent remainder/domain evidence.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Any

import numpy as np

import measurement_factor_audit as mfa


SCHEMA_VERSION = 2


def _svd_rank(a: np.ndarray, rtol: float, atol: float) -> tuple[int, np.ndarray, float]:
    a = np.asarray(a, dtype=float)
    if a.ndim != 2:
        raise ValueError(f"expected a matrix, got shape {a.shape}")
    if min(a.shape, default=0) == 0:
        return 0, np.array([], dtype=float), atol
    s = np.linalg.svd(a, compute_uv=False)
    scale = float(s[0]) if s.size else 0.0
    tol = max(atol, rtol * scale)
    rank = int(np.sum(s > tol))
    return rank, s, tol


def _nullspace(a: np.ndarray, rtol: float, atol: float) -> tuple[np.ndarray, dict[str, Any]]:
    a = np.asarray(a, dtype=float)
    if a.ndim != 2:
        raise ValueError(f"expected a matrix, got shape {a.shape}")
    _, n = a.shape
    if n == 0:
        return np.zeros((0, 0)), {"rank": 0, "singular_values": [], "tol": atol}
    u, s, vh = np.linalg.svd(a, full_matrices=True)
    del u
    scale = float(s[0]) if s.size else 0.0
    tol = max(atol, rtol * scale)
    rank = int(np.sum(s > tol))
    basis = vh[rank:, :].T.copy()
    return basis, {"rank": rank, "singular_values": s.tolist(), "tol": tol}


def _row_projection(a: np.ndarray, rtol: float, atol: float) -> tuple[np.ndarray, int, list[float], float]:
    a = np.asarray(a, dtype=float)
    if a.ndim != 2:
        raise ValueError(f"expected a matrix, got shape {a.shape}")
    k = a.shape[1]
    if k == 0:
        return np.zeros((0, 0)), 0, [], atol
    u, s, vh = np.linalg.svd(a, full_matrices=False)
    del u
    scale = float(s[0]) if s.size else 0.0
    tol = max(atol, rtol * scale)
    rank = int(np.sum(s > tol))
    if rank == 0:
        return np.zeros((k, k)), 0, s.tolist(), tol
    v = vh[:rank, :].T
    return v @ v.T, rank, s.tolist(), tol


def _relative_frobenius(residual: np.ndarray, reference: np.ndarray) -> float:
    denom = float(np.linalg.norm(reference, ord="fro"))
    num = float(np.linalg.norm(residual, ord="fro"))
    if denom == 0.0:
        return 0.0 if num == 0.0 else float("inf")
    return num / denom


def _linear_measurement_audit(
    do: np.ndarray,
    dg: np.ndarray,
    dp: np.ndarray | None,
    rtol: float,
    atol: float,
    sufficiency_tol: float,
) -> dict[str, Any]:
    do = np.asarray(do, dtype=float)
    dg = np.asarray(dg, dtype=float)
    if do.ndim != 2 or dg.ndim != 2:
        raise ValueError("DO and DG must be matrices")
    if do.shape[1] != dg.shape[1]:
        raise ValueError(f"DO and DG state dimensions differ: {do.shape[1]} vs {dg.shape[1]}")

    bk, do_info = _nullspace(do, rtol, atol)
    hidden_dim = int(bk.shape[1])
    gk = dg @ bk
    goal_rank, goal_s, goal_tol = _svd_rank(gk, rtol, atol)

    report: dict[str, Any] = {
        "state_dim": int(do.shape[1]),
        "observation_rows": int(do.shape[0]),
        "goal_rows": int(dg.shape[0]),
        "observation_rank": int(do_info["rank"]),
        "hidden_dim": hidden_dim,
        "goal_visible_hidden_dim": int(goal_rank),
        "goal_null_hidden_dim": int(hidden_dim - goal_rank),
        "scalar_measurement_lower_bound": int(goal_rank),
        "observation_singular_values": do_info["singular_values"],
        "goal_on_hidden_singular_values": goal_s.tolist(),
        "rank_tolerances": {
            "observation": float(do_info["tol"]),
            "goal_on_hidden": float(goal_tol),
        },
    }

    if dp is None:
        report["measurement"] = None
        return report

    dp = np.asarray(dp, dtype=float)
    if dp.ndim == 1:
        dp = dp.reshape(1, -1)
    if dp.ndim != 2 or dp.shape[1] != do.shape[1]:
        raise ValueError(f"DP must have shape (p, {do.shape[1]}), got {dp.shape}")

    mk = dp @ bk
    proj_m, rank_m, s_m, tol_m = _row_projection(mk, rtol, atol)
    missing_goal = gk @ (np.eye(hidden_dim) - proj_m)
    residual_abs = float(np.linalg.norm(missing_goal, ord="fro"))
    residual_rel = _relative_frobenius(missing_goal, gk)

    stacked = np.vstack([mk, gk])
    rank_stack, _, _ = _svd_rank(stacked, rtol, atol)
    rank_condition = rank_stack == rank_m
    numerical_condition = residual_rel <= sufficiency_tol
    tangent_sufficient = bool(rank_condition and numerical_condition)

    if mk.size == 0:
        factor = np.zeros((dg.shape[0], dp.shape[0]))
    else:
        factor = gk @ mfa._truncated_pinv(mk, rtol, atol)
    factor_residual = gk - factor @ mk
    factor_residual_rel = _relative_frobenius(factor_residual, gk)
    gain = float(np.linalg.norm(factor, ord=2)) if factor.size else 0.0

    report["measurement"] = {
        "rows": int(dp.shape[0]),
        "rank_on_hidden": int(rank_m),
        "singular_values_on_hidden": s_m,
        "rank_tolerance": float(tol_m),
        "stacked_rank_measurement_plus_goal": int(rank_stack),
        "rowspace_goal_residual_abs": residual_abs,
        "rowspace_goal_residual_rel": residual_rel,
        "factorization_residual_rel": factor_residual_rel,
        "minimum_norm_goal_from_measurement_gain_2norm": gain,
        "tangent_goal_sufficient": tangent_sufficient,
        "interpretation": (
            "First-order only: ker(DP|K) is numerically contained in ker(DG|K)."
            if tangent_sufficient
            else "First-order insufficiency or unresolved numerical rank: some goal-visible hidden direction remains."
        ),
    }
    return report


def _candidate_subset_report(
    do: np.ndarray,
    dg: np.ndarray,
    candidates: np.ndarray,
    labels: list[str] | None,
    rtol: float,
    atol: float,
    sufficiency_tol: float,
    max_subset_size: int,
    max_combinations: int,
) -> dict[str, Any]:
    candidates = np.asarray(candidates, dtype=float)
    if candidates.ndim != 2 or candidates.shape[1] != do.shape[1]:
        raise ValueError(f"DP_candidates must have shape (c, {do.shape[1]}), got {candidates.shape}")
    c = int(candidates.shape[0])
    if labels is None:
        labels = [str(i) for i in range(c)]
    if len(labels) != c:
        raise ValueError("candidate_labels length must match DP_candidates rows")

    empty = _linear_measurement_audit(do, dg, np.zeros((0, do.shape[1])), rtol, atol, sufficiency_tol)
    target_rank = int(empty["goal_visible_hidden_dim"])
    if target_rank == 0:
        return {
            "exact_subset": [],
            "exact_subset_labels": [],
            "minimal_size_within_search_cap": 0,
            "combinations_checked": 0,
            "greedy_subset": [],
            "greedy_subset_labels": [],
            "note": "No goal-visible hidden tangent direction exists at the audited point.",
        }

    checked = 0
    exact_subset: tuple[int, ...] | None = None
    exact_cap = min(max_subset_size, c)
    exhausted = False
    for size in range(1, exact_cap + 1):
        for subset in itertools.combinations(range(c), size):
            checked += 1
            if checked > max_combinations:
                exhausted = True
                break
            rep = _linear_measurement_audit(do, dg, candidates[list(subset), :], rtol, atol, sufficiency_tol)
            if rep["measurement"]["tangent_goal_sufficient"]:
                exact_subset = subset
                break
        if exact_subset is not None or exhausted:
            break

    selected: list[int] = []
    remaining = set(range(c))
    greedy_trace: list[dict[str, Any]] = []
    current_residual = float("inf")
    while remaining and len(selected) < max_subset_size:
        best_idx = None
        best_report = None
        best_score = None
        for idx in sorted(remaining):
            trial = selected + [idx]
            rep = _linear_measurement_audit(do, dg, candidates[trial, :], rtol, atol, sufficiency_tol)
            meas = rep["measurement"]
            score = (
                float(meas["rowspace_goal_residual_rel"]),
                -int(meas["rank_on_hidden"]),
                float(meas["minimum_norm_goal_from_measurement_gain_2norm"]),
                idx,
            )
            if best_score is None or score < best_score:
                best_score = score
                best_idx = idx
                best_report = rep
        assert best_idx is not None and best_report is not None
        selected.append(best_idx)
        remaining.remove(best_idx)
        meas = best_report["measurement"]
        current_residual = float(meas["rowspace_goal_residual_rel"])
        greedy_trace.append({
            "added_index": best_idx,
            "added_label": labels[best_idx],
            "goal_residual_rel": current_residual,
            "rank_on_hidden": int(meas["rank_on_hidden"]),
            "gain_2norm": float(meas["minimum_norm_goal_from_measurement_gain_2norm"]),
            "tangent_goal_sufficient": bool(meas["tangent_goal_sufficient"]),
        })
        if meas["tangent_goal_sufficient"]:
            break

    return {
        "goal_visible_hidden_dim": target_rank,
        "exact_subset": list(exact_subset) if exact_subset is not None else None,
        "exact_subset_labels": [labels[i] for i in exact_subset] if exact_subset is not None else None,
        "minimal_size_within_search_cap": len(exact_subset) if exact_subset is not None else None,
        "combinations_checked": checked,
        "exact_search_exhausted_by_combination_cap": exhausted,
        "max_subset_size": max_subset_size,
        "greedy_subset": selected,
        "greedy_subset_labels": [labels[i] for i in selected],
        "greedy_trace": greedy_trace,
        "greedy_final_goal_residual_rel": current_residual,
    }


def _as_float_vector(value: np.ndarray | None, length: int, name: str) -> np.ndarray | None:
    if value is None:
        return None
    arr = np.asarray(value, dtype=float)
    if arr.ndim == 0:
        return np.full(length, float(arr))
    arr = arr.reshape(-1)
    if arr.size != length:
        raise ValueError(f"{name} must be scalar or length {length}, got {arr.size}")
    return arr


def _multiscale_report(data: Any, rtol: float, atol: float, sufficiency_tol: float) -> list[dict[str, Any]] | None:
    keys = set(data.files)
    required = {"DO_scales", "DG_scales"}
    if not required.issubset(keys):
        return None
    do_s = np.asarray(data["DO_scales"], dtype=float)
    dg_s = np.asarray(data["DG_scales"], dtype=float)
    dp_s = np.asarray(data["DP_scales"], dtype=float) if "DP_scales" in keys else None
    if do_s.ndim != 3 or dg_s.ndim != 3 or do_s.shape[0] != dg_s.shape[0]:
        raise ValueError("DO_scales and DG_scales must be 3D arrays with a common scale axis")
    if do_s.shape[2] != dg_s.shape[2]:
        raise ValueError("DO_scales and DG_scales state dimensions differ")
    scale_count = int(do_s.shape[0])
    if dp_s is not None and (dp_s.ndim != 3 or dp_s.shape[0] != scale_count or dp_s.shape[2] != do_s.shape[2]):
        raise ValueError("DP_scales must be a 3D array aligned with DO_scales")

    radii = _as_float_vector(data["radii"] if "radii" in keys else None, scale_count, "radii")
    cg = _as_float_vector(data["remainder_goal_coeff"] if "remainder_goal_coeff" in keys else None, scale_count, "remainder_goal_coeff")
    cp = _as_float_vector(data["remainder_measurement_coeff"] if "remainder_measurement_coeff" in keys else None, scale_count, "remainder_measurement_coeff")
    co = _as_float_vector(data["remainder_observation_coeff"] if "remainder_observation_coeff" in keys else None, scale_count, "remainder_observation_coeff")
    sigma_o = _as_float_vector(data["observation_noise_radii"] if "observation_noise_radii" in keys else None, scale_count, "observation_noise_radii")
    sigma_p = _as_float_vector(data["measurement_noise_radii"] if "measurement_noise_radii" in keys else None, scale_count, "measurement_noise_radii")

    out: list[dict[str, Any]] = []
    for i in range(scale_count):
        rep = _linear_measurement_audit(
            do_s[i], dg_s[i], None if dp_s is None else dp_s[i], rtol, atol, sufficiency_tol
        )
        item: dict[str, Any] = {"scale_index": i, "audit": rep}
        if radii is not None:
            item["radius"] = float(radii[i])
        # Tangent sufficiency on ker(DO) does not imply a whole-state
        # quadratic prediction bound: the observation contribution B DO
        # and its curvature must also be included.
        supplied = (radii is not None and cg is not None
                    and cp is not None and co is not None)
        if supplied and dp_s is not None:
            conditional = mfa.audit(
                do_s[i], dg_s[i], dp_s[i],
                radius=float(radii[i]), c_obs=float(co[i]),
                c_goal=float(cg[i]), c_measurement=float(cp[i]),
                observation_noise_radius=0.0 if sigma_o is None else float(sigma_o[i]),
                measurement_noise_radius=0.0 if sigma_p is None else float(sigma_p[i]),
                rtol=rtol, atol=atol, factor_residual_tol=sufficiency_tol,
            )
            item["conditional_all_direction_prediction"] = conditional
            item["prediction_status"] = "CONDITIONAL_ON_USER_SUPPLIED_REMAINDER_AND_NOISE_ENVELOPES"
            item["noise_assumption"] = (
                "Zero observation/measurement noise assumed for missing noise-radius arrays; "
                "supplied coefficients and domain are not independently verified."
            )
        else:
            item["prediction_status"] = (
                "MISSING_OBSERVATION_GOAL_MEASUREMENT_REMAINDER_OR_RADIUS"
                if dp_s is not None else "MISSING_MEASUREMENT_JACOBIAN"
            )
        out.append(item)
    return out


def audit_npz(
    path: Path,
    rtol: float,
    atol: float,
    sufficiency_tol: float,
    max_subset_size: int,
    max_combinations: int,
) -> dict[str, Any]:
    with np.load(path, allow_pickle=False) as data:
        if "DO" not in data.files or "DG" not in data.files:
            raise ValueError("input NPZ must contain DO and DG")
        do = np.asarray(data["DO"], dtype=float)
        dg = np.asarray(data["DG"], dtype=float)
        dp = np.asarray(data["DP"], dtype=float) if "DP" in data.files else None
        report: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "source": str(path),
            "tolerances": {
                "rtol": rtol,
                "atol": atol,
                "sufficiency_tol": sufficiency_tol,
            },
            "center": _linear_measurement_audit(do, dg, dp, rtol, atol, sufficiency_tol),
            "claim_ceiling": (
                "Outputs are finite-dimensional numerical linear-algebra certificates. "
                "Tangent sufficiency is not finite-radius injectivity, stability, or native-model uniqueness."
            ),
        }

        if "DP_candidates" in data.files:
            labels = None
            if "candidate_labels" in data.files:
                labels = [str(x) for x in np.asarray(data["candidate_labels"]).reshape(-1).tolist()]
            report["candidate_measurements"] = _candidate_subset_report(
                do,
                dg,
                np.asarray(data["DP_candidates"], dtype=float),
                labels,
                rtol,
                atol,
                sufficiency_tol,
                max_subset_size,
                max_combinations,
            )

        multi = _multiscale_report(data, rtol, atol, sufficiency_tol)
        if multi is not None:
            report["multiscale"] = multi
            report["multiscale_summary"] = {
                "all_scales_tangent_sufficient": bool(
                    all(
                        x["audit"].get("measurement") is not None
                        and x["audit"]["measurement"]["tangent_goal_sufficient"]
                        for x in multi
                    )
                ),
                "goal_visible_hidden_dims": [
                    int(x["audit"]["goal_visible_hidden_dim"]) for x in multi
                ],
                "note": (
                    "Scale persistence is a diagnostic only. Any conditional finite-radius numerical bound is valid only with independently verified observation/measurement/goal remainder, noise and domain envelopes."
                ),
            }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="NPZ containing DO, DG and optional DP/candidate/multiscale arrays")
    parser.add_argument("--output", type=Path, help="JSON output path; defaults to stdout")
    parser.add_argument("--rtol", type=float, default=1e-9, help="relative singular-value rank tolerance")
    parser.add_argument("--atol", type=float, default=1e-12, help="absolute singular-value rank tolerance")
    parser.add_argument(
        "--sufficiency-tol",
        type=float,
        default=1e-8,
        help="maximum relative goal row-space residual for numerical tangent sufficiency",
    )
    parser.add_argument("--max-subset-size", type=int, default=8, help="max candidate subset size for exact/greedy search")
    parser.add_argument("--max-combinations", type=int, default=200000, help="cap on exact candidate combinations")
    args = parser.parse_args()

    if args.rtol < 0 or args.atol < 0 or args.sufficiency_tol < 0:
        parser.error("tolerances must be nonnegative")
    if args.max_subset_size < 0 or args.max_combinations < 1:
        parser.error("subset/search caps must be positive")

    report = audit_npz(
        args.input,
        args.rtol,
        args.atol,
        args.sufficiency_tol,
        args.max_subset_size,
        args.max_combinations,
    )
    payload = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
