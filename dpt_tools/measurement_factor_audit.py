"""All-direction linear factor and CONDITIONAL Taylor-error bound.

If all maps are differentiable at a common h*, let DO,DP,DG be Jacobians.
The minimum-norm factor on retained singular directions,
[B A] = DG @ truncated_pinv([DO; DP]), gives
E = DG - B DO - A DP. Under ||delta_h||_2 <= r and SUPPLIED bounds
||R_O|| <= C_O r^2, ||R_P|| <= C_P r^2, ||R_G|| <= C_G r^2,
we obtain ||Delta G - B Delta O - A Delta P|| <=
||E||_2*r + (C_G + ||B||_2*C_O + ||A||_2*C_P)*r^2.
Noise on measured O and P adds ||B||*sigma_O + ||A||*sigma_P.

The caller is responsible for verifying remainder bounds and units.
"""
from __future__ import annotations
import numpy as np


def _truncated_pinv(matrix, rtol, atol):
    """Use the same strict cutoff as the numerical rank audits."""
    u, s, vh = np.linalg.svd(matrix, full_matrices=False)
    cutoff = max(atol, rtol * float(s[0])) if s.size else atol
    keep = s > cutoff
    return (vh[keep].T / s[keep]) @ u[:, keep].T


def audit(do, dg, dp, *, radius: float, c_obs=None, c_goal=None,
          c_measurement=None, observation_noise_radius=0.0,
          measurement_noise_radius=0.0, rtol=1e-9, atol=1e-12,
          factor_residual_tol=1e-8) -> dict:
    do, dg, dp = (np.asarray(x, dtype=float) for x in (do, dg, dp))
    if any(x.ndim != 2 for x in (do, dg, dp)) or do.shape[1] != dg.shape[1] or dp.shape[1] != do.shape[1]:
        raise ValueError("DO, DG, DP must be matrices with the same state dimension")
    if not all(np.all(np.isfinite(x)) for x in (do, dg, dp)):
        raise ValueError("Jacobian entries must be finite")
    scalar_args = {"radius": radius, "observation_noise_radius": observation_noise_radius,
                   "measurement_noise_radius": measurement_noise_radius,
                   "rtol": rtol, "atol": atol, "factor_residual_tol": factor_residual_tol}
    for name, value in scalar_args.items():
        if not np.isfinite(float(value)) or float(value) < 0:
            raise ValueError(f"{name} must be finite and nonnegative")
    for name, value in (("c_obs", c_obs), ("c_goal", c_goal), ("c_measurement", c_measurement)):
        if value is not None and (not np.isfinite(float(value)) or float(value) < 0):
            raise ValueError(f"{name} must be finite and nonnegative when provided")
    augmented = np.vstack((do, dp))
    factors = dg @ _truncated_pinv(augmented, rtol, atol)
    b = factors[:, :do.shape[0]]
    a = factors[:, do.shape[0]:]
    e = dg - b @ do - a @ dp
    residual = float(np.linalg.norm(e, ord=2)) if e.size else 0.0
    goal_norm = float(np.linalg.norm(dg, ord=2)) if dg.size else 0.0
    gain_b = float(np.linalg.norm(b, ord=2)) if b.size else 0.0
    gain_a = float(np.linalg.norm(a, ord=2)) if a.size else 0.0
    exact = bool(residual <= max(atol, factor_residual_tol * goal_norm))
    noise_term = gain_b * float(observation_noise_radius) + gain_a * float(measurement_noise_radius)
    if any(x is None for x in (c_obs, c_goal, c_measurement)):
        status = "MISSING_REMAINDER_ASSUMPTIONS"
        bound = None
    else:
        status = "CONDITIONAL_ON_SUPPLIED_REMAINDER_BOUNDS"
        r = float(radius)
        bound = residual * r + (float(c_goal) + gain_b * float(c_obs) + gain_a * float(c_measurement)) * r**2 + noise_term
    return {
        "factorization_exact_at_tangent": exact,
        "linear_residual_2norm": residual,
        "observation_gain_2norm": gain_b,
        "measurement_gain_2norm": gain_a,
        "observation_factor": b.tolist(),
        "measurement_factor": a.tolist(),
        "status": status,
        "conditional_prediction_bound": bound,
        "noise_contribution": noise_term,
        "assumptions": "All map remainders on the same state ball are independently bounded, input/output units and norms fixed; user-supplied bounds not checked by this function.",
    }



def three_sample_affine_voltage_gate(observed_V, candidate_raw_V, indices, noise_sup_V):
    """Reject one ARCHIVED same-command source candidate under one joint voltage error.

    Both arrays must refer to the SAME recorded CAL times, voltage port and
    source law. The caller must validate these identities, legal PREP/guards,
    source/truncation error, and the complete record-level noise contract.
    Independent common gain/offset are eliminated exactly at THREE samples;
    this is a necessary candidate test, not a full-fiber goal certificate.

    Treat stored binary64 values as exact rationals, so rounding in source
    and measurement production is NOT included in this calculation.
    """
    from fractions import Fraction
    from math import isfinite, nextafter, inf

    if len(observed_V) != len(candidate_raw_V) or len(observed_V) < 3:
        raise ValueError("a common >=3-sample CAL timeline is required")
    if len(indices) != 3 or len(set(indices)) != 3 or any(
        type(i) is not int or i < 0 or i >= len(observed_V) for i in indices
    ):
        raise ValueError("three distinct sample indices required")
    samples = ([float(observed_V[i]) for i in indices]
               + [float(candidate_raw_V[i]) for i in indices])
    if not all(map(isfinite, samples)):
        raise ValueError("nonfinite sample")
    try:
        epsilon = Fraction(str(noise_sup_V))
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        raise ValueError("invalid voltage noise budget") from exc
    if epsilon < 0:
        raise ValueError("negative voltage noise budget")
    y = tuple(map(Fraction.from_float, samples[:3]))
    m = tuple(map(Fraction.from_float, samples[3:]))
    w = (m[1]-m[2], m[2]-m[0], m[0]-m[1])
    norm = sum(map(abs, w))
    if norm == 0:
        raise ValueError("chosen candidate samples are all equal")
    assert sum(w) == 0 and sum(v*x for v, x in zip(w, m)) == 0
    necessary = abs(sum(v*x for v, x in zip(w, y))) / norm
    return {
        "status": "STRICT_CANDIDATE_EXCLUDED" if epsilon < necessary else "INCONCLUSIVE",
        "strict_reject": bool(epsilon < necessary),
        "min_necessary_error_V_ratio": (
            str(necessary.numerator), str(necessary.denominator)),
        "min_necessary_error_V_float_lower": nextafter(float(necessary), -inf),
        "stored_binary64_contrast_V": float(necessary),
        "evidence": ("Exact archived binary64 THREE-voltage affine quotient. "
                     "Not actual sensor E, source-rounding, root/guard coverage, "
                     "all-goal-fiber certification, or future-work prediction."),
    }
