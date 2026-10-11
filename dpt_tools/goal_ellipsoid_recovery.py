"""Global scalar-goal optimal recovery in a declared linear ellipsoidal chart.

Not a nonlinear/native DPT certificate. State perturbations are B @ z,
||z||_2 <= 1; additive observation errors are E @ e, ||e||_2 <= 1.
The sensor, prior and goal must share a physically qualified state chart.
"""
from __future__ import annotations

import numpy as np


def recover_scalar_goal(state_factor, observation, noise_factor, goal):
    """Return minimax scalar-goal radius, linear decoder and dual diagnostics.

    state_factor B (n,n); observation H (m,n);
    noise_factor E (m,m), nonsingular for m>0; goal g (n,).
    Observation is y=H(x0+Bz)+Ee, goal=G0+g.T Bz.
    The reported decoder weights act on the unwhitened y-Hx0.
    """
    B = np.asarray(state_factor, dtype=float)
    H = np.asarray(observation, dtype=float)
    E = np.asarray(noise_factor, dtype=float)
    g = np.asarray(goal, dtype=float)
    if B.ndim != 2 or B.shape[0] != B.shape[1] or B.shape[0] == 0:
        raise ValueError("state_factor must have square positive dimension")
    n = B.shape[0]
    if H.ndim != 2 or H.shape[1] != n or E.shape != (H.shape[0], H.shape[0]) or g.shape != (n,):
        raise ValueError("inconsistent observation/noise/goal shapes")
    if not all(np.isfinite(v).all() for v in (B, H, E, g)):
        raise ValueError("all inputs must be finite")
    m = H.shape[0]
    if m:
        sv_E = np.linalg.svd(E, compute_uv=False)
        if sv_E[-1] <= 1e-13 * max(1.0, sv_E[0]):
            raise ValueError("noise_factor singular or numerically rank-deficient")
        A = np.linalg.solve(E, H @ B)
    else:
        A = np.empty((0, n))
    c = B.T @ g
    _, s, vt = np.linalg.svd(A, full_matrices=True)
    s2 = np.zeros(n)
    s2[:s.size] = s**2
    cproj = vt @ c

    def square_radius(q):
        denom = (1.0 - q) + q * s2
        if np.any((denom == 0) & (cproj != 0)):
            return float("inf")
        return float(np.sum(np.divide(cproj**2, denom,
                                      out=np.zeros_like(cproj), where=denom > 0)))

    # The squared-radius dual is convex in q; derivative bisection needs
    # NumPy only and checks both endpoint regimes explicitly.
    def derivative(q):
        denom = (1.0 - q) + q * s2
        if np.any((denom == 0) & (cproj != 0)):
            return float("inf")
        return float(np.sum(np.divide(cproj**2 * (1.0 - s2), denom**2,
                                      out=np.zeros_like(cproj), where=denom > 0)))

    if np.linalg.norm(c) == 0 or derivative(0.) >= 0:
        q = 0.0
    elif np.isfinite(square_radius(1.)) and derivative(1.) <= 0:
        q = 1.0
    else:
        lo, hi = 0.0, 1.0
        for _ in range(90):
            mid = (lo + hi) / 2.0
            if derivative(mid) > 0:
                hi = mid
            else:
                lo = mid
        q = (lo + hi) / 2.0
    f = square_radius(q)
    denom = (1.0 - q) + q * s2
    v = vt.T @ np.divide(cproj, denom, out=np.zeros_like(cproj), where=denom > 0)
    w = q * (A @ v)
    a = np.linalg.solve(E.T, w) if m else np.empty(0)
    # Independent primal/dual checks are floating numerical diagnostics,
    # not interval-certified real-arithmetic error control.
    upper = float(np.linalg.norm(c - A.T @ w) + np.linalg.norm(w))
    scale = max(float(np.linalg.norm(v)), float(np.linalg.norm(A @ v)))
    if scale == 0:
        scale = 1.0
    z = v / scale
    lower = float(abs(c @ z))
    radius = float(np.sqrt(max(f, 0.)))
    return {
        "status": "LINEAR_ELLIPSOID_NUMERIC_DIAGNOSTIC",
        "radius": radius,
        "q": float(q),
        "measurement_weights": a.tolist(),
        "algorithm_upper": upper,
        "feasible_witness_lower": lower,
        "numerical_gap": max(0., upper - lower),
        "witness_prior_norm": float(np.linalg.norm(z)),
        "witness_whitened_observation_norm": float(np.linalg.norm(A @ z)),
        "model_semantics": "global worst case, centered prior and correlated L2 noise; not native nonlinear",
    }


def main():
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("npz", help="NPZ with state_factor, observation, noise_factor, goal")
    parser.add_argument("--output", help="Optional JSON report path")
    args = parser.parse_args()
    with np.load(args.npz, allow_pickle=False) as data:
        result = recover_scalar_goal(*(data[k] for k in
                                       ("state_factor", "observation", "noise_factor", "goal")))
    output = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
