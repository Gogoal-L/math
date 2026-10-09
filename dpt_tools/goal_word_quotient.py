#!/usr/bin/env python3
"""Unbounded-command GOAL quotient of a *fixed linear switched* model.

This is a polynomial-time row-space closure, not enumeration of exponentially
many words. Inputs MUST be in one common, correctly scaled state chart:
    x_next = A[command] @ x;  future_goal = C @ x.
For nonlinear DPT, a single Jacobian at each command does NOT define such a
model across new preparations, mode changes, or arbitrary command histories.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def _matrix(value, name: str) -> np.ndarray:
    a = np.asarray(value, dtype=float)
    if a.ndim != 2 or not np.all(np.isfinite(a)):
        raise ValueError(f"{name} must be a finite 2D matrix")
    return a


def _basis(rows: np.ndarray, rtol: float, atol: float) -> np.ndarray:
    n = rows.shape[1]
    if not rows.shape[0]:
        return np.zeros((0, n))
    _, s, vt = np.linalg.svd(rows, full_matrices=False)
    threshold = max(atol, rtol * float(s[0]))
    return vt[:int(np.count_nonzero(s > threshold)), :].copy()


def audit(updates, observation, goal, *, rtol=1e-10, atol=1e-12) -> dict:
    """Find the smallest right-invariant goal-row space containing C.

    The resulting rank is the minimal autonomous *linear goal-only* state
    dimension across ALL finite command words for the supplied linear model.
    Observation O affects only the extra freely chosen scalar-measurement
    dimension, not the autonomous goal quotient itself.
    """
    if not all(np.isfinite(x) and x >= 0 for x in (rtol, atol)):
        raise ValueError("rtol/atol must be finite and nonnegative")
    o, c = _matrix(observation, "observation"), _matrix(goal, "goal")
    if c.shape[0] == 0 or c.shape[1] == 0 or o.shape[1] != c.shape[1]:
        raise ValueError("goal must have positive shape and observation must share state dimension")
    n = c.shape[1]
    if not isinstance(updates, dict) or not updates:
        raise ValueError("updates must be a nonempty command-to-matrix dictionary")
    matrices = {}
    for key, v in updates.items():
        if not isinstance(key, str) or not key or "/" in key:
            raise ValueError("command keys must be nonempty names without a slash")
        a = _matrix(v, f"updates[{key}]")
        if a.shape != (n, n):
            raise ValueError(f"updates[{key}] must be ({n}, {n})")
        matrices[key] = a
    # O is a current observation, not automatically an autonomously updated state.
    o_rank = _basis(o, rtol, atol).shape[0]
    w = _basis(c, rtol, atol)
    def report(depth, basis):
        all_rows = np.vstack((o, basis))
        return {"horizon": int(depth), "goal_rank": int(basis.shape[0]),
                "extra_linear_observation_rows": int(_basis(all_rows, rtol, atol).shape[0] - o_rank)}

    stages = [report(0, w)]
    saturated = None
    for depth in range(1, n + 2):
        generated = [w] + [w @ a for a in matrices.values()]
        w_new = _basis(np.vstack(generated), rtol, atol)
        stages.append(report(depth, w_new))
        if w_new.shape[0] < w.shape[0]:
            raise ValueError("numerical row-rank lost monotonicity; rescale state and tolerance")
        if w_new.shape[0] == w.shape[0]:
            saturated = depth - 1
            w = w_new
            break
        w = w_new
    if saturated is None:
        raise ValueError("goal row-space did not saturate within state dimension")
    # Orthonormal rows give an explicit exact (in ideal arithmetic) quotient.
    red = {name: (w @ a @ w.T).tolist() for name, a in matrices.items()}
    closure = [float(np.linalg.norm(w @ a - (w @ a @ w.T) @ w, ord=2))
               if w.shape[0] else 0.0 for a in matrices.values()]
    readout = (c @ w.T).tolist()
    factor_residual = float(np.linalg.norm(c - (c @ w.T) @ w, ord=2))
    return {
        "schema_version": 1,
        "claim_type": "LINEAR_MODEL_ONLY",
        "state_dimension": n,
        "observation_rank": o_rank,
        "horizons": stages,
        "saturated_at_horizon": saturated,
        "minimal_autonomous_goal_rank": int(w.shape[0]),
        "additional_free_linear_observation_rows": stages[-1]["extra_linear_observation_rows"],
        "goal_state_basis_rows": w.tolist(),
        "goal_readout_from_quotient": readout,
        "reduced_updates": red,
        "max_update_closure_residual": max(closure),
        "goal_readout_factor_residual": factor_residual,
        "rank_tolerances": {"relative": float(rtol), "absolute": float(atol)},
        "claim_ceiling": "Row-span saturation proves the minimal goal-only autonomous linear quotient "
                         "only for an exact fixed common-chart linear switched model. This "
                         "floating-point calculation is tolerance-sensitive. Added observation "
                         "rows assume freely designed scalar linear sensors, not deployable ports. "
                         "No nonlinear, guard, cross-chart, finite-radius or native certificate."
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path, help="NPZ with updates (k,n,n), observation (m,n), goal (q,n), command_names (k,)")
    p.add_argument("--rtol", type=float, default=1e-10)
    p.add_argument("--atol", type=float, default=1e-12)
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    with np.load(a.input, allow_pickle=False) as data:
        keys = set(data.files)
        if not {"updates", "observation", "goal", "command_names"}.issubset(keys):
            p.error("NPZ needs updates, observation, goal, command_names")
        tensors, names = data["updates"], [str(v) for v in data["command_names"]]
        if tensors.ndim != 3 or len(names) != len(tensors) or len(set(names)) != len(names):
            p.error("updates and unique command_names must be aligned")
        result = audit(dict(zip(names, tensors)), data["observation"], data["goal"],
                       rtol=a.rtol, atol=a.atol)
    output = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if a.output:
        a.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
