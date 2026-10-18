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



def s150_two_coil_scorer_bridge(t_s, H_s, voltage_V, current_A,
                                load_current_A, Ls_H, LD_H,
                                *, coil_residual_each_V=None):
    """Source BE-right versus frozen PL(H) signed-work, preserving correlations.

    K=A(H,t)^T diag(trapezoid_H) A(H,t)-diag(0,dt_source), Q=V^T K I.
    Source coil rows give V_j=150+LD*d(load_i)/h-Ls*d(I)/h+r36-r37
    for j>0. If |r36|,|r37|<=eps, and the COMPLETE source currents
    are fixed, |Q-Q_coil|<=2 eps ||(K I)[1:]||_1. NOT full fiber.
    """
    t=np.asarray(t_s,float); H=np.asarray(H_s,float)
    V=np.asarray(voltage_V,float); s=np.asarray(current_A,float)
    d=np.asarray(load_current_A,float)
    if (t.ndim!=1 or H.ndim!=1 or len(t)<2 or len(H)<2
        or any(a.shape!=t.shape for a in (V,s,d))):
        raise ValueError("times and source currents must align")
    if (not all(np.isfinite(a).all() for a in (t,H,V,s,d))
        or not np.all(np.diff(t)>0) or not np.all(np.diff(H)>0)
        or H[0]<t[0] or H[-1]>t[-1]):
        raise ValueError("ordered finite source and H seconds without extrapolation required")
    Ls=float(Ls_H);Ld=float(LD_H)
    if not np.isfinite(Ls+Ld) or min(Ls,Ld)<=0:
        raise ValueError("positive source inductances required")
    h=np.diff(t)
    omega=np.empty_like(H)
    omega[0]=(H[1]-H[0])/2; omega[-1]=(H[-1]-H[-2])/2
    omega[1:-1]=(H[2:]-H[:-2])/2
    right=np.clip(np.searchsorted(t,H,side="right"),1,len(t)-1)
    left=right-1
    alpha=np.clip((H-t[left])/(t[right]-t[left]),0,1)
    Hs=(1-alpha)*s[left]+alpha*s[right]
    Hv=(1-alpha)*V[left]+alpha*V[right]
    Ks=np.zeros_like(t);Ks[1:]=-h*s[1:]
    np.add.at(Ks,left,omega*(1-alpha)*Hs)
    np.add.at(Ks,right,omega*alpha*Hs)
    W_H=float(omega@(Hs*Hv));W_BE=float(np.sum(h*V[1:]*s[1:]))
    Vcoil=np.empty_like(V);Vcoil[0]=V[0]
    Vcoil[1:]=150-Ls*np.diff(s)/h+Ld*np.diff(d)/h
    residual=V[1:]-Vcoil[1:]
    out={"status":"POINT_SOURCE_CURRENT_COIL_BRIDGE","W_H_J":W_H,
         "W_BE_right_J":W_BE,"Q_H_J":float(V@Ks),
         "Q_H_direct_J":W_H-W_BE,"Q_coil_J":float(Vcoil@Ks),
         "Q_residual_J":float(residual@Ks[1:]),
         "r36_minus_r37_maxabs_V":float(np.max(abs(residual))),
         "residual_support_A_s":float(np.sum(abs(Ks[1:]))),
         "claim_ceiling":"Source-row algebra at one supplied full current path, not source-wide 50D future-work/root interval."}
    if coil_residual_each_V is not None:
        eps=float(coil_residual_each_V)
        if not np.isfinite(eps) or eps<0:
            raise ValueError("nonnegative residual voltage budget needed")
        out["conditional_Q_radius_J"]=2*eps*out["residual_support_A_s"]
        out["residual_qualified_at_point"]=bool(out["r36_minus_r37_maxabs_V"]<=2*eps)
    return out



def s150_load_current_from_raw_ports(t_s, port_V, port_I, *, source_Ls_H,
                                      load_Ld_H=100e-6, seed_load_A,
                                      residual_r36_V=None, residual_r37_V=None,
                                      voltage_error_V=0.0, current_error_A=0.0,
                                      seed_error_A=0.0,
                                      coil_residual_error_V=0.0):
    """Use exact fixed-L two-coil BE rows to eliminate one hidden load history.

    PRECONDITION: V and I are SOURCE-RAW V=x0-x1 and I=x36, NOT the
    observed 100MHz-filtered I before lawful deconvolution. Both L values
    are constant through own PREP/future, seed_load_A is the SAME source
    load-current sign convention state[37], not a post-CAL reset.
    """
    t=np.asarray(t_s,float);v=np.asarray(port_V,float);i=np.asarray(port_I,float)
    if (t.ndim!=1 or len(t)<2 or v.shape!=t.shape or i.shape!=t.shape
        or not all(np.isfinite(x).all() for x in (t,v,i))
        or not np.all(np.diff(t)>0)):
        raise ValueError("aligned finite raw V/I and increasing seconds required")
    Ls=float(source_Ls_H);Ld=float(load_Ld_H);j0=float(seed_load_A)
    eV=float(voltage_error_V);eI=float(current_error_A)
    ej=float(seed_error_A);er=float(coil_residual_error_V)
    if (not all(np.isfinite(x) for x in (Ls,Ld,j0,eV,eI,ej,er))
        or min(Ls,Ld)<=0 or min(eV,eI,ej,er)<0):
        raise ValueError("positive inductances and finite error allowances required")
    n=len(t)
    r36=np.zeros(n) if residual_r36_V is None else np.asarray(residual_r36_V,float)
    r37=np.zeros(n) if residual_r37_V is None else np.asarray(residual_r37_V,float)
    if r36.shape!=t.shape or r37.shape!=t.shape or not all(np.isfinite(a).all() for a in (r36,r37)):
        raise ValueError("coil residual arrays must align with source time")
    h=np.diff(t)
    j=j0+(Ls/Ld)*(i-i[0])
    j[1:]+=np.cumsum(h*(v[1:]-150+r37[1:]-r36[1:]))/Ld
    T=t-t[0]
    bound=ej+(T*eV+2*Ls*eI+2*T*er)/Ld
    return {"status":"CONDITIONAL_RAW_PORT_LOAD_HISTORY",
            "j_A":j.tolist(),
            "uniform_error_bound_A":bound.tolist(),
            "claim_ceiling":"RAW source ports and known source L/seed/coil errors only. "
              "Not a recovery from filtered CAL with unknown b/xi, not future scorer or 50D root coverage."}



def s150_goal_family_weighted_bound(t_s, H_s, voltage_V, current_A,
                                   R_s_A_root_s, R_phi_V_root_s,
                                   R_r_V_root_s, *, score="frozen"):
    """Conditional signed work-family norm bound from original H PL scorer.

    Two lawful paths must have SAME fine t, H, static L, bus, prepared
    starting V0,I0, and source flux increments; R_s, R_phi, R_r MUST
    enclose their true joint weighted temporal differences. This
    evaluates point floating coefficients, NOT directed source/solver
    bounds or a source-compatible fiber certificate.
    """
    t=np.asarray(t_s,float);H=np.asarray(H_s,float)
    V=np.asarray(voltage_V,float);I=np.asarray(current_A,float)
    if (t.ndim!=1 or H.ndim!=1 or len(t)<2 or len(H)<2 or
        V.shape!=t.shape or I.shape!=t.shape or
        not all(np.all(np.isfinite(a)) for a in (t,H,V,I)) or
        np.any(np.diff(t)<=0) or np.any(np.diff(H)<=0) or
        H[0]<t[0] or H[-1]>t[-1]):
        raise ValueError("aligned finite source t/H/V/I, no extrapolation required")
    radii=np.asarray([R_s_A_root_s,R_phi_V_root_s,R_r_V_root_s],float)
    if np.any(~np.isfinite(radii)) or np.any(radii<0):
        raise ValueError("joint temporal source radii must be finite nonnegative")
    if score not in ("frozen","signed_correction"):
        raise ValueError("score must be frozen or signed_correction")
    h=np.diff(t);n=len(t)
    omega=np.empty_like(H)
    omega[0]=(H[1]-H[0])/2;omega[-1]=(H[-1]-H[-2])/2
    omega[1:-1]=(H[2:]-H[:-2])/2
    right=np.clip(np.searchsorted(t,H,side="right"),1,n-1)
    left=right-1
    alpha=np.clip((H-t[left])/(t[right]-t[left]),0,1)
    diag=np.zeros(n);off=np.zeros(n-1)
    np.add.at(diag,left,omega*(1-alpha)**2)
    np.add.at(diag,right,omega*alpha**2)
    np.add.at(off,left,omega*alpha*(1-alpha))
    if score=="signed_correction":diag[1:]-=h
    def apply(z):
        out=diag*z
        out[1:]+=off*z[:-1]
        out[:-1]+=off*z[1:]
        return out
    cs=float(np.linalg.norm(apply(V)[1:]/np.sqrt(h)))
    cp=float(np.linalg.norm(apply(I)[1:]/np.sqrt(h)))
    # Absolute weighted Gershgorin row-sums upper-bound ||T^-1/2 E T^-1/2||_2.
    rows=np.abs(diag[1:])/h
    weights=np.abs(off[1:])/np.sqrt(h[:-1]*h[1:])
    rows[:-1]+=weights;rows[1:]+=weights
    sigma=float(np.max(rows))
    rs,rp,rr=map(float,radii)
    upper=cs*rs+cp*(rp+rr)+sigma*rs*(rp+rr)
    return {"status":"CONDITIONAL_SOURCE_FAMILY_NORM","score":score,
            "C_s_V_root_s":cs,"C_phi_A_root_s":cp,
            "sigma_float_gershgorin":sigma,"delta_goal_abs_upper_J":float(upper),
            "claim_ceiling":"Valid bound only if supplied joint weighted radii cover ALL "
                "legal same-start/same-source-parameter future paths, with "
                "appropriate source residual/clock/guard and fixed scorer. "
                "All calculations are IEEE64, NOT directed interval arithmetic; "
                "point source outputs cannot certify a full Goal27 goal diameter."}


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
