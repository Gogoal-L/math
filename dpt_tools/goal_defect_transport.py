#!/usr/bin/env python3
"""Goal-directed disturbance transport along an ORDERED linear stage sequence.

This audits a supplied common-chart finite-dimensional model
    dx[k+1] = A[k] @ dx[k] + e[k],    dg[k] = c[k] @ dx[k]
with exact preparation observation O @ dx[0] = 0, ||dx[0]|| <= rho,
and independently selectable ||e[k]||_2 <= eps[k].  The per-stage
worst-case scalar goal error is an exact Euclidean product-ball support
function in *this* linear model, not a verified SiC-native error bound.

If A[k] are local Jacobians of nonlinear laws, or eps[k] are estimates
rather than true bounds on a valid branch and reachable tube, the report
is a sensitivity diagnostic only. State coordinates and uncertainty
norms must be physically scaled and match every stage and readout.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def _array(data, name: str, ndim: int) -> np.ndarray:
    arr = np.asarray(data, dtype=float)
    if arr.ndim != ndim or not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must be a finite {ndim}D array")
    return arr


def _nonnegative(value, name: str) -> float:
    try:
        z = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be finite and nonnegative") from exc
    if not np.isfinite(z) or z < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return z


def _unseen_basis(o: np.ndarray, n: int, rtol: float, atol: float) -> tuple[np.ndarray, int]:
    if not o.shape[0]:
        return np.eye(n), 0
    _, s, vt = np.linalg.svd(o, full_matrices=True)
    cutoff = max(atol, rtol * float(s[0])) if s.size else atol
    rank = int(np.count_nonzero(s > cutoff))
    return vt[rank:, :].T.copy(), rank


def audit(updates, observation, goal, initial_radius, defect_radii,
          *, rtol=1e-10, atol=1e-12) -> dict:
    """Calculate sharp scalar goal error on an assumed product of L2 balls.

    updates: (H,n,n), goal: (n,) or (H+1,n), observation: (m,n),
    defect_radii: (H,). A single goal row is read at all H+1 endpoints.
    Each source disturbance is free to vary independently. If real
    disturbance families are correlated/reachable-subset constrained,
    these radii remain conservative upper bounds, not sharp there.
    """
    rt, at = _nonnegative(rtol, "rtol"), _nonnegative(atol, "atol")
    rho = _nonnegative(initial_radius, "initial_radius")
    aa = _array(updates, "updates", 3)
    h = aa.shape[0]
    n = aa.shape[1]
    if n < 1 or aa.shape[2] != n:
        raise ValueError("updates must have shape (H,n,n) with n >= 1")
    oo = _array(observation, "observation", 2)
    if oo.shape[1] != n:
        raise ValueError("observation columns must equal state dimension")
    gg = np.asarray(goal, dtype=float)
    if gg.ndim == 1 and gg.shape == (n,):
        gg = np.repeat(gg[None, :], h+1, axis=0)
    if gg.ndim != 2 or gg.shape != (h+1, n) or not np.all(np.isfinite(gg)):
        raise ValueError("goal must have shape (n,) or (H+1,n)")
    ee = _array(defect_radii, "defect_radii", 1)
    if ee.shape != (h,) or np.any(ee < 0):
        raise ValueError("defect_radii must be nonnegative, length H")
    hidden, obs_rank = _unseen_basis(oo, n, rt, at)
    stages = []
    adjoint_by_stage = []
    for end in range(h + 1):
        # adj[j] = c[end] A[end-1] ... A[j], with A applied in path order.
        adj = [np.zeros(n) for _ in range(end+1)]
        adj[end] = gg[end].copy()
        for j in range(end-1, -1, -1):
            adj[j] = adj[j+1] @ aa[j]
        info = rho * float(np.linalg.norm(adj[0] @ hidden))
        solver = float(sum(float(ee[j]) * np.linalg.norm(adj[j+1]) for j in range(end)))
        if not all(np.isfinite(x) for x in (info, solver, info+solver)):
            raise ValueError("nonfinite bound; rescale physical coordinates")
        stages.append({"stage": end, "information_radius": info,
                       "defect_radius": solver, "total_radius": info+solver,
                       "initial_hidden_goal_row_norm": float(np.linalg.norm(adj[0] @ hidden))})
        adjoint_by_stage.append(adj)
    worst = max(stages, key=lambda d: d["total_radius"])
    end = worst["stage"]
    adj = adjoint_by_stage[end]
    p = hidden @ (hidden.T @ adj[0])
    pn = float(np.linalg.norm(p))
    dx = rho * p / pn if pn else np.zeros(n)
    dx0 = dx.copy()
    injected = []
    norms = []
    for j in range(end):
        row = adj[j+1]
        rn = float(np.linalg.norm(row))
        e = float(ee[j]) * row / rn if rn else np.zeros(n)
        injected.append(e)
        norms.append(float(np.linalg.norm(e)))
        dx = aa[j] @ dx + e
    goal_dev = float(gg[end] @ dx)
    obs_dev = float(np.linalg.norm(oo @ dx0))
    # Norms in the witness are zero for stages after the worst endpoint.
    norms += [0.] * (h - end)
    output = {
        "schema_version": 1,
        "model_type": "ORDERED_LINEAR_COMMON_CHART_PRODUCT_BALLS",
        "state_dimension": n,
        "command_steps": h,
        "preparation_observation_rank": obs_rank,
        "initial_hidden_dimension": int(hidden.shape[1]),
        "stages": stages,
        "worst_stage": worst,
        "stage_spectral_radii": [float(max(abs(np.linalg.eigvals(a)))) for a in aa],
        "stage_operator_norms_2": [float(np.linalg.norm(a, ord=2)) for a in aa],
        "max_absolute_witness": {
            "stage": end,
            "initial_perturbation": dx0.tolist(),
            "initial_norm": float(np.linalg.norm(dx0)),
            "observation_residual": obs_dev,
            "defect_vectors": [v.tolist() for v in injected],
            "defect_norms": norms,
            "goal_deviation": goal_dev,
        },
        "rank_tolerances": {"relative": rt, "absolute": at},
        "claim_ceiling": (
            "Exact scalar worst-case per endpoint and finite-horizon maximum ONLY "
            "under this linear common-chart model, exact observation equality and "
            "independent Euclidean balls for initial hidden state and stage errors. "
            "Floating SVD ranks and computed witnesses are numerical diagnostics. "
            "For native DPT, externally certify stage maps, physical scales, "
            "reachable branch/guard, additive defect radii and smooth goal readouts. "
            "Not a nonlinear, hardware, stochastic, all-command or time-continuous certificate."
        ),
    }
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="NPZ: updates, observation, goal, initial_radius, defect_radii")
    parser.add_argument("--rtol", type=float, default=1e-10)
    parser.add_argument("--atol", type=float, default=1e-12)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    with np.load(args.input, allow_pickle=False) as bank:
        required = {"updates", "observation", "goal", "initial_radius", "defect_radii"}
        if not required.issubset(bank.files):
            parser.error("NPZ missing: " + ", ".join(sorted(required - set(bank.files))))
        report = audit(bank["updates"], bank["observation"], bank["goal"],
                       bank["initial_radius"], bank["defect_radii"],
                       rtol=args.rtol, atol=args.atol)
    content = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
