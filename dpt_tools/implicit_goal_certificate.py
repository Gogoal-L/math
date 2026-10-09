#!/usr/bin/env python3
"""Conditional Newton-Kantorovich, scalar GOAL-weighted residual audit.

Given F(y_hat), J=DF(y_hat) and Dg(y_hat), compute the first-order goal
correction -Dg J^-1 F and, ONLY UNDER INDEPENDENTLY VALIDATED BALL-WIDE
regularity and inverse bounds, a finite-radius quadratic goal remainder.
F may be a single implicit stage or a properly stacked whole-trajectory
residual with the event / consistency lift differentiated through.
No rigorous interval evaluation or native solver verification is performed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def _bound(x, name, *, positive=False):
    try:
        z = float(x)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be finite") from None
    if not np.isfinite(z) or z < 0 or (positive and z <= 0):
        raise ValueError(f"{name} must be {'positive' if positive else 'nonnegative'} and finite")
    return z


def audit(residual, jacobian, goal_gradient, *, inverse_norm_upper,
          newton_step_upper, jacobian_lipschitz_upper, goal_hessian_upper,
          domain_radius, rtol=1e-10, atol=1e-12) -> dict:
    """Conditional scalar Newton-Kantorovich root and goal error bound.

    Input beta/eta/L/H/R must be separately justified on the same smooth
    branch and norm. beta and eta are checked against floating estimates
    only; these comparisons do not validate interval upper bounds.
    """
    b = _bound(inverse_norm_upper, "inverse_norm_upper", positive=True)
    eta = _bound(newton_step_upper, "newton_step_upper")
    L = _bound(jacobian_lipschitz_upper, "jacobian_lipschitz_upper")
    H = _bound(goal_hessian_upper, "goal_hessian_upper")
    R = _bound(domain_radius, "domain_radius")
    rt, at = _bound(rtol, "rtol"), _bound(atol, "atol")
    j = np.asarray(jacobian, dtype=float)
    r = np.asarray(residual, dtype=float)
    g = np.asarray(goal_gradient, dtype=float)
    if j.ndim != 2 or j.shape[0] == 0 or j.shape[0] != j.shape[1]:
        raise ValueError("jacobian must be a square nonempty matrix")
    n = j.shape[0]
    if r.shape != (n,) or g.shape != (n,) or not all(np.all(np.isfinite(a)) for a in (j, r, g)):
        raise ValueError("residual and goal_gradient must be finite 1D arrays aligned with jacobian")
    sv = np.linalg.svd(j, compute_uv=False)
    if float(sv[-1]) <= max(at, rt * float(sv[0])):
        raise ValueError("jacobian is singular at the declared numerical rank cutoff")
    beta_est = 1. / float(sv[-1])
    step = np.linalg.solve(j, r)
    eta_est = float(np.linalg.norm(step))
    slack = max(1e-12, 1e-9 * max(1., beta_est, eta_est))
    if b + slack < beta_est or eta + slack < eta_est:
        raise ValueError("independently claimed beta/eta bound below computed estimate")
    adjoint = np.linalg.solve(j.T, g)
    first = -float(adjoint @ r)
    h = b * L * eta
    result = {
        "schema_version": 1,
        "status": None,
        "jacobian_condition_2norm": float(sv[0] / sv[-1]),
        "inverse_norm_estimate": beta_est,
        "newton_step_norm_estimate": eta_est,
        "signed_goal_correction": first,
        "goal_adjoint": adjoint.tolist(),
        "kantorovich_h": float(h),
        "root_distance_upper": None,
        "corrected_goal_error_upper": None,
        "uncorrected_goal_error_upper": None,
        "claim_ceiling": "All positive certificates are CONDITIONAL on independently valid "
          "ball-wide C1-Lipschitz F' / C2 goal bounds, smooth event branch, "
          "consistent full-law residual, correct numerical coordinates, "
          "and rigorous beta/eta upper bounds. Float computations alone "
          "do not certify a native simulator or total-model error."
    }
    if h > .5:
        result["status"] = "INCONCLUSIVE_CURVATURE"
        return result
    # Stable evaluation, including L=0 and eta=0.
    rho = 2. * eta / (1. + np.sqrt(max(0., 1. - 2. * h)))
    if rho > R + max(1e-12, 1e-12 * R):
        result["status"] = "INCONCLUSIVE_DOMAIN"
        return result
    # F(y*)=0, J delta = -r - nonlinear_F_remainder.
    # With ||delta|| <= rho and ||remainder_F|| <= L*rho^2/2,
    # scalar goal remainder is <= (||lambda|| L + H)*rho^2/2.
    remainder = .5 * (float(np.linalg.norm(adjoint)) * L + H) * rho * rho
    if not all(np.isfinite(v) for v in (rho, remainder, h)):
        raise ValueError("numerical overflow; rescale residual and physical state")
    result.update({
        "status": "CONDITIONAL_KANTOROVICH",
        "root_distance_upper": float(rho),
        "corrected_goal_error_upper": float(remainder),
        "uncorrected_goal_error_upper": float(abs(first) + remainder),
        "goal_change_interval": [float(first - remainder), float(first + remainder)],
        "interpretation": "Existing nearby full-law root is enclosed if ALL supplied envelopes "
                          "and branch/ball conditions are independently true."
    })
    return result


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path, help="JSON with residual, jacobian, goal_gradient, bounds")
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    raw = json.loads(a.input.read_text(encoding="utf-8"))
    keys = ["residual", "jacobian", "goal_gradient", "inverse_norm_upper",
            "newton_step_upper", "jacobian_lipschitz_upper", "goal_hessian_upper", "domain_radius"]
    missing = [k for k in keys if k not in raw]
    if missing:
        p.error("missing required fields: " + ", ".join(missing))
    out = audit(**{k: raw[k] for k in keys})
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    if a.output:
        a.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
