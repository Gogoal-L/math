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
    If a strictly positive noise singular value is discarded by the numerical
    tolerance, radius becomes a conservative numeric decoder DUAL upper,
    not a sharp minimax estimate, and status explicitly marks uncertainty.
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
    # A strictly POSITIVE but much smaller singular value is not exact noise
    # nullspace. It is numerically unresolved by this floating-point SVD.
    # Treating it as zero would manufacture a noiseless observation and
    # potentially report a goal radius of zero when a nonzero radius is legal.
    ambiguous_positive_noise = bool(np.any((sv_E > 0) & (sv_E <= tol_E)))
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
        "status": ("LINEAR_ELLIPSOID_RANK_UNCERTAIN_UPPER_ONLY"
                   if ambiguous_positive_noise else
                   "LINEAR_ELLIPSOID_NUMERIC_DIAGNOSTIC"),
        # Numerical rank-uncertainty must not be presented as a sharp radius.
        # The independently evaluated decoder dual upper is valid for
        # the declared prior/noise ellipsoids; it is not outward-rounded.
        "radius": float(upper if ambiguous_positive_noise else
                        np.sqrt(max(f, 0.))),
        "radius_kind": ("DUAL_UPPER_NUMERIC_ONLY" if ambiguous_positive_noise
                        else "MINIMAX_NUMERIC_ESTIMATE"),
        "noise_rank_definitive": not ambiguous_positive_noise,
        "rank_ambiguous_positive_singular_values": [
            float(s) for s in sv_E if 0 < s <= tol_E
        ],
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



def _gaussian_oed_array(value, shape, name):
    a = np.asarray(value, dtype=float)
    if a.shape != shape or not np.all(np.isfinite(a)):
        raise ValueError(f"{name} must be finite with shape {shape}")
    return a


def _gaussian_oed_symmetric_psd(value, name, *, strict=False):
    scale = max(1.0, float(np.max(np.abs(value))) if value.size else 0.0)
    if not np.allclose(value, value.T, rtol=1e-12, atol=1e-12 * scale):
        raise ValueError(f"{name} must be symmetric")
    eigenvalues = np.linalg.eigvalsh(value)
    tol = 1e-10 * scale * max(1, len(value))
    if eigenvalues.size and (eigenvalues[0] <= 0 if strict
                             else eigenvalues[0] < -tol):
        raise ValueError(f"{name} must be {'positive definite' if strict else 'positive semidefinite'}")


def quadratic_goal_design(prior_mean, prior_cov, goal_gradient,
                          goal_hessian, observation_jacobian, noise_cov,
                          *, expansion_center=None, discrepancy_cov=None,
                          state_discrepancy_cross_cov=None):
    """Bayes goal risk for joint-Gaussian *affine observations*, quadratic goal.

    x~N(mu,P), jointly Gaussian discrepancy d with covariance D and
    Cov(x,d)=C; measurement y=H*x+d+epsilon with independent Gaussian
    epsilon~N(0,R), R positive definite.  A non-Gaussian, nonlinear DPT
    measurement does NOT meet this contract merely because H is its Jacobian.
    Gradient/Hessian describe a quadratic Taylor approximation of the future
    goal about expansion_center (defaults to prior_mean).
    """
    mu = np.asarray(prior_mean, dtype=float)
    if mu.ndim != 1 or not mu.size or not np.all(np.isfinite(mu)):
        raise ValueError("prior_mean must be a finite nonempty vector")
    n = len(mu)
    H = np.asarray(observation_jacobian, dtype=float)
    if H.ndim != 2 or H.shape[1] != n or not np.all(np.isfinite(H)):
        raise ValueError("observation_jacobian must be a finite (m,n) matrix")
    m = H.shape[0]
    P = _gaussian_oed_array(prior_cov, (n,n), "prior_cov")
    b = _gaussian_oed_array(goal_gradient, (n,), "goal_gradient")
    Q = _gaussian_oed_array(goal_hessian, (n,n), "goal_hessian")
    R = _gaussian_oed_array(noise_cov, (m,m), "noise_cov")
    center = mu if expansion_center is None else _gaussian_oed_array(
        expansion_center, (n,), "expansion_center")
    D = (np.zeros((m,m)) if discrepancy_cov is None else
         _gaussian_oed_array(discrepancy_cov, (m,m), "discrepancy_cov"))
    C = (np.zeros((n,m)) if state_discrepancy_cross_cov is None else
         _gaussian_oed_array(state_discrepancy_cross_cov,
                             (n,m), "state_discrepancy_cross_cov"))
    _gaussian_oed_symmetric_psd(P, "prior_cov")
    _gaussian_oed_symmetric_psd(R, "noise_cov", strict=m>0)
    _gaussian_oed_symmetric_psd(D, "discrepancy_cov")
    if not np.allclose(Q, Q.T, rtol=1e-12, atol=1e-12):
        raise ValueError("goal_hessian must be symmetric")
    # A model-error covariance must include the state/discrepancy cross block.
    _gaussian_oed_symmetric_psd(np.block([[P,C],[C.T,D]]),
                                 "joint state and discrepancy covariance")
    covariance_y = H @ P @ H.T + H @ C + C.T @ H.T + D + R
    covariance_xy = P @ H.T + C
    if m:
        posterior = P - covariance_xy @ np.linalg.solve(
            covariance_y, covariance_xy.T)
        posterior = .5 * (posterior + posterior.T)
    else:
        posterior = P.copy()
    _gaussian_oed_symmetric_psd(posterior, "posterior_cov")
    effective_gradient = b + Q @ (mu-center)
    Gl = float(effective_gradient @ posterior @ effective_gradient)
    quadratic = float(np.trace(P@Q@posterior@Q)
                      -.5*np.trace((posterior@Q)@(posterior@Q)))
    Gq = Gl + quadratic
    prior_goal_variance = float(
        effective_gradient@P@effective_gradient
        + .5*np.trace((P@Q)@(P@Q)))
    parameter_MI = None
    if not m:
        parameter_MI = 0.0
    elif np.linalg.eigvalsh(P)[0] > 1e-11*max(1.,float(np.max(abs(P)))):
        # Conditionally correlated d contributes only its residual variance.
        conditional_error = R + D - C.T @ np.linalg.solve(P,C)
        sy,ly = np.linalg.slogdet(covariance_y)
        sc,lc = np.linalg.slogdet(conditional_error)
        if sy<=0 or sc<=0:
            raise ValueError("invalid Gaussian measurement covariance")
        parameter_MI = max(0., .5*float(ly-lc))
    return {
        "status": "JOINT_GAUSSIAN_QUADRATIC_GOAL_DIAGNOSTIC",
        "Gq": max(0.,float(Gq)),
        "Gl": max(0.,float(Gl)),
        "A": float(np.trace(posterior)),
        "parameter_MI": parameter_MI,
        "prior_goal_variance": max(0.,float(prior_goal_variance)),
        "goal_hessian_energy": float(quadratic),
        "posterior_cov": posterior.tolist(),
        "observation_cov": covariance_y.tolist(),
        "scope": ("Joint Gaussian state/discrepancy, affine observation,"
                  " quadratic Taylor future goal; stochastic posterior"
                  " variance, not minimax or validated native SiC")
    }


def rank_quadratic_goal_designs(
    prior_mean, prior_cov, goal_gradient, goal_hessian,
    candidate_observations, candidate_noise_cov, *,
    candidate_names=None, goal_expansion_center=None,
    candidate_discrepancy_cov=None,
    candidate_state_discrepancy_cross_cov=None,
):
    """Rank declared legal candidate sensors; never infer candidate legality."""
    H = np.asarray(candidate_observations, dtype=float)
    if H.ndim != 3 or H.shape[0] < 1:
        raise ValueError("candidate_observations must be (k,m,n), k>=1")
    k,m,n = H.shape
    R = _gaussian_oed_array(candidate_noise_cov,
                             (k,m,m), "candidate_noise_cov")
    D = (np.zeros((k,m,m)) if candidate_discrepancy_cov is None else
         _gaussian_oed_array(candidate_discrepancy_cov,
                             (k,m,m), "candidate_discrepancy_cov"))
    C = (np.zeros((k,n,m)) if candidate_state_discrepancy_cross_cov is None
         else _gaussian_oed_array(candidate_state_discrepancy_cross_cov,
                                  (k,n,m), "candidate_state_discrepancy_cross_cov"))
    names = ([f"sensor_{j}" for j in range(k)] if candidate_names is None
             else list(candidate_names))
    if (len(names)!=k or any(not isinstance(s,str) or not s.strip()
                             for s in names) or len(set(names))!=len(names)):
        raise ValueError("candidate_names must be k distinct nonempty names")
    candidates=[]
    for j in range(k):
        report = quadratic_goal_design(
            prior_mean, prior_cov, goal_gradient, goal_hessian,
            H[j], R[j], expansion_center=goal_expansion_center,
            discrepancy_cov=D[j], state_discrepancy_cross_cov=C[j])
        candidates.append(dict(candidate_name=names[j],**report))
    best = {field:names[min(range(k),
                             key=lambda j:(candidates[j][field],j))]
            for field in ("Gq","Gl","A")}
    best["parameter_MI"] = (
        names[max(range(k),key=lambda j:(candidates[j]["parameter_MI"],-j))]
        if all(x["parameter_MI"] is not None for x in candidates) else None)
    return {
        "status":"GAUSSIAN_QUADRATIC_DESIGN_RANKING",
        "rank_best":best,
        "candidates":candidates,
        "scope":("Source candidate legality, units, prior/cross-covariance and"
                 " future-goal Hessian require independent qualification;"
                 " stochastic surrogate cannot certify SiC hardware")
    }


def main():
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("npz", help="NPZ with legacy minimax or quadratic-goal design fields")
    parser.add_argument("--output", help="Optional JSON report path")
    parser.add_argument("--quadratic-design", action="store_true",
                        help="Rank Gaussian quadratic-goal sensor candidates (separate model)")
    args = parser.parse_args()
    with np.load(args.npz, allow_pickle=False) as data:
        if args.quadratic_design:
            required = ("prior_mean", "prior_cov", "goal_gradient", "goal_hessian",
                        "candidate_observations", "candidate_noise_cov")
            missing = [x for x in required if x not in data.files]
            if missing:
                parser.error("missing quadratic-design fields: " + ", ".join(missing))
            optional = {
                "candidate_names": ([str(x) for x in data["candidate_names"]]
                                    if "candidate_names" in data.files else None),
                "goal_expansion_center": (
                    data["goal_expansion_center"]
                    if "goal_expansion_center" in data.files else None),
                "candidate_discrepancy_cov": (
                    data["candidate_discrepancy_cov"]
                    if "candidate_discrepancy_cov" in data.files else None),
                "candidate_state_discrepancy_cross_cov": (
                    data["candidate_state_discrepancy_cross_cov"]
                    if "candidate_state_discrepancy_cross_cov" in data.files else None),
            }
            result = rank_quadratic_goal_designs(
                *(data[x] for x in required), **optional)
        else:
            result = recover_scalar_goal(*(data[k] for k in
                                          ("state_factor", "observation",
                                           "noise_factor", "goal")))
    output = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")

if __name__ == "__main__":
    main()
