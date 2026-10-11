"""Global scalar-goal optimal recovery in a declared linear ellipsoidal chart.

Not a nonlinear/native DPT certificate. State perturbations are B @ z,
||z||_2 <= 1; additive observation errors are E @ e, ||e||_2 <= 1.
The sensor, prior and goal must share a physically qualified state chart.
"""
from __future__ import annotations

import numpy as np


def recover_scalar_goal(state_factor, observation, noise_factor, goal):
    """Minimax scalar-goal radius with possibly rank-deficient joint noise.

    B (n,n), H (m,n), E (m,p), g (n,). E need not be square
    or full rank. Singular E exposes exact *noiseless channel contrasts*.
    All rank decisions are numerical and require physical qualification.
    """
    B = np.asarray(state_factor, dtype=float)
    H = np.asarray(observation, dtype=float)
    E = np.asarray(noise_factor, dtype=float)
    g = np.asarray(goal, dtype=float)
    if B.ndim != 2 or B.shape[0] != B.shape[1] or B.shape[0] == 0:
        raise ValueError("state_factor must have square positive dimension")
    n = B.shape[0]
    if (H.ndim != 2 or H.shape[1] != n or E.ndim != 2
            or E.shape[0] != H.shape[0] or g.shape != (n,)):
        raise ValueError("inconsistent observation/noise/goal shapes")
    if not all(np.isfinite(v).all() for v in (B, H, E, g)):
        raise ValueError("all inputs must be finite")

    m, p = E.shape
    HB = H @ B
    c = B.T @ g
    # Exactly shared/noiseless combinations live in orthogonal complement
    # of the range of E. This includes a zero-width E with no noise.
    U, sv_E, _ = np.linalg.svd(E, full_matrices=True)
    tol_E = 100 * np.finfo(float).eps * max(m, p, 1) * (sv_E[0] if sv_E.size else 0.)
    r_E = int(np.count_nonzero(sv_E > tol_E))
    U_r, U_0 = U[:, :r_E], U[:, r_E:]
    C = U_0.T @ HB  # exact observation equality constraints on z
    _, sv_C, Vtc = np.linalg.svd(C, full_matrices=True)
    tol_C = 100 * np.finfo(float).eps * max(C.shape[0], n, 1) * (sv_C[0] if sv_C.size else 0.)
    r_C = int(np.count_nonzero(sv_C > tol_C))
    Z = Vtc[r_C:].T  # orthonormal basis of ker(C)
    k = Z.shape[1]
    # Coordinate covariance in the noisy subspace equals diag(s_E**2).
    A = (U_r.T @ HB @ Z) / sv_E[:r_E, None] if r_E else np.empty((0,k))
    c_red = Z.T @ c

    _, s, vt = np.linalg.svd(A, full_matrices=True)
    s2 = np.zeros(k)
    s2[:s.size] = s**2
    cproj = vt @ c_red

    def square_radius(q):
        denom = 1.0 - q + q*s2
        if np.any((denom == 0) & (cproj != 0)):
            return float("inf")
        return float(np.sum(np.divide(cproj**2, denom,
                      out=np.zeros_like(cproj), where=denom > 0)))

    def derivative(q):
        denom = 1.0 - q + q*s2
        if np.any((denom == 0) & (cproj != 0)):
            return float("inf")
        return float(np.sum(np.divide(cproj**2*(1-s2), denom**2,
                      out=np.zeros_like(cproj), where=denom > 0)))

    if np.linalg.norm(c_red)==0 or derivative(0.) >= 0:
        q=0.0
    elif np.isfinite(square_radius(1.)) and derivative(1.) <= 0:
        q=1.0
    else:
        lo,hi=0.,1.
        for _ in range(90):
            mid=(lo+hi)/2
            if derivative(mid)>0: hi=mid
            else: lo=mid
        q=(lo+hi)/2
    f=square_radius(q)
    denom=1.0-q+q*s2
    v=vt.T @ np.divide(cproj, denom, out=np.zeros_like(cproj), where=denom>0)
    w=q*(A @ v)
    # Recover a linear decoder in original unwhitened sensor coordinates.
    # The U0 component is free of sensor noise and projects away C's rowspace.
    a_r=U_r @ (w/sv_E[:r_E]) if r_E else np.zeros(m)
    if U_0.shape[1]:
        t=np.linalg.lstsq(C.T, c-HB.T @ a_r, rcond=None)[0]
        a=a_r+U_0 @ t
    else:
        a=a_r
    # Tiny sensor noise drives q toward an endpoint: numerical leakage
    # into ker(A) can corrupt the q-based decoder by many orders.
    # Keep only independently valid dual upper candidates.
    ls_decoder=np.linalg.lstsq(HB.T,c,rcond=None)[0]
    def decoder_upper(a_vec):
        return float(np.linalg.norm(c-HB.T @ a_vec)+np.linalg.norm(E.T @ a_vec))
    a=min((a,ls_decoder,np.zeros(m)),key=decoder_upper)
    upper=decoder_upper(a)
    scale=max(float(np.linalg.norm(v)), float(np.linalg.norm(A @ v)))
    if scale==0: scale=1.0
    # Normalize and score the feasible primal witness in the reduced
    # coordinate system to avoid ill-conditioned SVD round trips.
    v_w=v/scale
    safe=max(1.0,float(np.linalg.norm(v_w)),float(np.linalg.norm(A @ v_w)))
    v_w=v_w/(safe*(1.0+8*np.finfo(float).eps))
    lower=float(abs(c_red @ v_w))
    return {
        "status": "LINEAR_ELLIPSOID_NUMERIC_DIAGNOSTIC",
        "radius": float(np.sqrt(max(f, 0.))),
        "q": float(q),
        "measurement_weights": a.tolist(),
        "algorithm_upper": upper,
        "feasible_witness_lower": lower,
        "numerical_gap": max(0., upper-lower),
        "witness_prior_norm": float(np.linalg.norm(v_w)),
        "witness_whitened_observation_norm": float(np.linalg.norm(A @ v_w)),
        "witness_noiseless_constraint_norm": float(np.linalg.norm(C @ (Z @ v_w))),
        "noise_rank": r_E,
        "noise_free_readout_count": m-r_E,
        "exact_observation_constraint_rank": r_C,
        "noise_rank_threshold": float(tol_E),
        "model_semantics": "global linear centered L2 prior and correlated bounded noise; numerical rank only; not nonlinear SiC",
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
