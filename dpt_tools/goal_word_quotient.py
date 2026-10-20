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


def source_s150_be_predecessor_key(old50, *, discretization="BE",
                                   include_current_port=False):
    """Exact original-law 28D old-state key for one BE step (set-valued).

    Source actual_law.py member SHA256
    51b78f729393d29745f59ca150adfef69e1847bf26a8853c6cef3d6be9e2083d.
    For the ORIGINAL _source_operator and _turnoff_operator, when
    old_command=None and old D1 history is within the qualified law,
    ALL old-state arguments in F(y, old, dt, command) factor through
       (W.T v_old [6], coil_currents_old [12],
        junction_voltages_old [2], thermal_old [8]).
    G11 old charge change is also determined by W.T v_old. Thus identical
    keys give IDENTICAL next ROOT SETS (including all guarded choices)
    for every command and positive BE step, and induction gives an exact
    set-valued right-congruence for any finite BE command word. This is
    algebraic factorizability, NOT proof any two distinct legal original
    PREP/CAL histories share the key, that a root exists, or that a
    consumer can infer this key from external observations.

    Any trapezoidal old_command argument evaluates static(old) and breaks
    this reduction. Literal hybrid resets/other integrators require a
    separate root/guard/reset proof; fail closed rather than upgrade BE.
    Optionally add current V(D)-V(sl) as a 29th observable-coordinate key.
    """
    from fractions import Fraction as F
    if discretization!="BE":
        raise ValueError("ONLY_SOURCE_BE_OLD_COMMAND_NONE_QUALIFIED")
    try:
        vals=tuple(F(x) if not isinstance(x,bool) else (_ for _ in ()).throw(
            ValueError("boolean old state not permitted")) for x in old50)
    except (TypeError,ValueError,ZeroDivisionError,OverflowError) as ex:
        raise ValueError("invalid source old50 rational") from ex
    if len(vals)!=50:
        raise ValueError("source predecessor must have 50 coordinates")
    # Original 26 source nodes:
    # ['D','sl', Q1{da,d,gb,g2,g,w,x,s,sv,sb,k,sa},
    #             Q2{da,d,gb,g2,g,w,x,s,sv,sb,k,sa}]
    # The original source control map W.T v is (gs,gd,ds) in each Q.
    controls=(vals[6]-vals[9],vals[6]-vals[7],vals[3]-vals[9],
              vals[18]-vals[21],vals[18]-vals[19],vals[15]-vals[21])
    key=controls+vals[26:38]+vals[40:42]+vals[42:50]
    if len(key)!=28:
        raise ArithmeticError("original source BE key dimension drift")
    return key+((vals[0]-vals[1],) if include_current_port else ())
