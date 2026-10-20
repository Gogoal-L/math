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



def s150_causal_coil_signed_goal_bound(t_s, H_s, vD_V, vsl_V, source_current_A,
                                      source_Ls_H, node_radius_V, *, score="frozen",
                                      alt_r36_residual_V=0.0):
    """Conditional H841 signed W or BE-to-H Q radius from the exact BE coil row.

    All legal compared futures must have the SAME initial prepared full
    node state and current, same fixed L, source grid and H. Every later
    D/sl node voltage must be within node_radius_V of the supplied
    saved source reference, and alternative r36 within the declared bound.
    Point IEEE64 coefficient calculation only: not a verified root tube.
    """
    t=np.asarray(t_s,float); H=np.asarray(H_s,float)
    vd=np.asarray(vD_V,float); sl=np.asarray(vsl_V,float)
    s=np.asarray(source_current_A,float)
    if (t.ndim!=1 or H.ndim!=1 or len(t)<2 or len(H)<2 or
            any(z.shape!=t.shape for z in (vd,sl,s)) or
            not all(np.isfinite(z).all() for z in (t,H,vd,sl,s)) or
            np.any(np.diff(t)<=0) or np.any(np.diff(H)<=0) or
            H[0]<t[0] or H[-1]>t[-1]):
        raise ValueError("aligned finite source t/H and raw D/sl/current required")
    L=float(source_Ls_H);rho=float(node_radius_V);er=float(alt_r36_residual_V)
    if (not all(np.isfinite(z) for z in (L,rho,er)) or
            L<=0 or min(rho,er)<0 or score not in ("frozen","signed_correction")):
        raise ValueError("positive L, nonnegative radii and valid scorer required")
    h=np.diff(t);n=len(t)
    omega=np.empty_like(H)
    omega[0]=(H[1]-H[0])/2;omega[-1]=(H[-1]-H[-2])/2
    omega[1:-1]=(H[2:]-H[:-2])/2
    right=np.clip(np.searchsorted(t,H,side="right"),1,n-1);left=right-1
    alpha=np.clip((H-t[left])/(t[right]-t[left]),0,1)

    def apply(z):
        hz=(1-alpha)*z[left]+alpha*z[right]
        out=np.zeros(n)
        np.add.at(out,left,omega*(1-alpha)*hz)
        np.add.at(out,right,omega*alpha*hz)
        if score=="signed_correction":out[1:]-=h*z[1:]
        return out

    v=vd-sl;g=apply(s);a=apply(v)
    b=np.zeros(n);b[1:]=h/L*np.cumsum(a[1:][::-1])[::-1]
    r36=-sl[1:]+L*np.diff(s)/h
    linear=rho*(np.sum(abs(g[1:]))+np.sum(abs(b[1:]-g[1:])))
    center_bias=abs(float(np.dot(b[1:],r36)))
    alternate_error=er*float(np.sum(abs(b[1:])))
    cross=2*rho*(rho+float(np.max(abs(r36)))+er)/L*(
        float(np.dot(omega,H-t[0]))+float(np.dot(h,t[1:]-t[0])))
    return {"status":"CONDITIONAL_CAUSAL_COIL_GOAL",
            "score":score,
            "point_goal_J":float(np.dot(v,g)),
            "linear_radius_J":float(linear),
            "reference_coil_bias_abs_J":center_bias,
            "alternate_coil_residual_radius_J":alternate_error,
            "bilinear_radius_J":float(cross),
            "delta_goal_abs_upper_J":float(linear+center_bias+alternate_error+cross),
            "claim_ceiling":"Only supplied IEEE64 source point plus independently CERTIFIED "
                "all-legal same-prepared-full-state, same-grid fixed-L node tube and "
                "source coil residual; not interval rounding, full50 root/fiber, "
                "sensor E or actual Goal27 goal-diameter certification."}



def s150_two_l_causal_goal_identity(t_s, H_s, vD_a_V, vsl_a_V, current_a_A,
                                    La_H, vD_b_V, vsl_b_V, current_b_A,
                                    Lb_H, *, score="frozen"):
    """Exact two-static-L BE coil identity for a frozen signed PL(H) goal.

    Accept supplied aligned full source paths ONLY; do not generate futures.
    Both own-PREP current seeds, actual coil residual and the finite
    voltage-current bilinear term remain explicit. Floating coefficients,
    not verified 50D source roots, common CAL fiber, or hardware error.
    """
    t=np.asarray(t_s,float);H=np.asarray(H_s,float)
    va=np.asarray(vD_a_V,float);sa=np.asarray(vsl_a_V,float)
    ia=np.asarray(current_a_A,float);vb=np.asarray(vD_b_V,float)
    sb=np.asarray(vsl_b_V,float);ib=np.asarray(current_b_A,float)
    paths=(t,H,va,sa,ia,vb,sb,ib)
    La=float(La_H);Lb=float(Lb_H)
    if (any(x.ndim!=1 or not np.isfinite(x).all() for x in paths)
        or len(t)<2 or len(H)<2 or any(x.shape!=t.shape for x in (va,sa,ia,vb,sb,ib))
        or np.any(np.diff(t)<=0) or np.any(np.diff(H)<=0)
        or H[0]<t[0] or H[-1]>t[-1]
        or not np.isfinite(La) or not np.isfinite(Lb) or min(La,Lb)<=0
        or score not in ("frozen","signed_correction")):
        raise ValueError("finite same-grid paths, positive static L and known goal required")
    h=np.diff(t);om=np.empty(len(H))
    om[0]=(H[1]-H[0])/2;om[-1]=(H[-1]-H[-2])/2
    om[1:-1]=(H[2:]-H[:-2])/2
    right=np.clip(np.searchsorted(t,H,side="right"),1,len(t)-1)
    left=right-1;alpha=(H-t[left])/(t[right]-t[left])
    def apply(z):
        zh=(1-alpha)*z[left]+alpha*z[right];out=np.zeros(len(t))
        np.add.at(out,left,om*(1-alpha)*zh)
        np.add.at(out,right,om*alpha*zh)
        if score=="signed_correction":out[1:]-=h*z[1:]
        return out
    v=va-sa;vnext=vb-sb;dv=vnext-v;di=ib-ia
    rA=-sa[1:]+La*np.diff(ia)/h
    rB=-sb[1:]+Lb*np.diff(ib)/h
    g=apply(ia);a=apply(v);b=h/Lb*np.cumsum(a[1:][::-1])[::-1]
    terms={"voltage_J":float(np.dot(g,dv)),
           "prepared_current_J":float(np.sum(a)*di[0]),
           "static_L_J":float((La/Lb-1)*np.dot(a,ia-ia[0])),
           "sl_feedback_J":float(np.dot(b,sb[1:]-sa[1:])),
           "coil_residual_J":float(np.dot(b,rB-rA)),
           "bilinear_J":float(np.dot(dv,apply(di)))}
    vhA=(1-alpha)*v[left]+alpha*v[right]
    vhB=(1-alpha)*vnext[left]+alpha*vnext[right]
    ihA=(1-alpha)*ia[left]+alpha*ia[right]
    ihB=(1-alpha)*ib[left]+alpha*ib[right]
    direct=float(np.dot(om,vhB*ihB-vhA*ihA))
    if score=="signed_correction":
        direct-=float(np.dot(h,vnext[1:]*ib[1:]-v[1:]*ia[1:]))
    calc=sum(terms.values())
    return {"status":"CONDITIONAL_TWO_L_BE_GOAL_IDENTITY","score":score,
            "direct_J":direct,"algebra_J":float(calc),
            "closure_abs_J":float(abs(calc-direct)),
            "terms_J":terms,
            "reference_coil_residual_max_abs_V":float(max(abs(rA))),
            "alternative_coil_residual_max_abs_V":float(max(abs(rB))),
            "initial_flux_difference_Wb":float(Lb*ib[0]-La*ia[0]),
            "claim_ceiling":"An algebraic source-row identity for TWO SUPPLIED paths; "
                "not full50 legality, common full-CAL fiber, sensor error "
                "qualification or any signed-work diameter."}



def s150_package_two_coil_goal_bound(t_s, H_s, vD_V, vsl_V, vsa_V, vsv_V,
                                    source_current_A, package_i34_A, L_H, *,
                                    port_radius_V, sv_radius_V,
                                    seed_s_radius_A, seed_j_radius_A,
                                    alt_forcing_residual_V=0.0):
    """Conditional H841 signed-work radius from the exact 2-coil package Schur.

    Source rows 1,25,34,36 eliminate sl/sa KCL and Ls2 package coil.
    x=(i36,-i34) follows an SPD 2x2 M-matrix BE recurrence driven
    by Q2:sv (original node22). Both PREP current seeds are retained.
    Requires supplied source-raw paths and independently bounded
    alternative electric node22, port voltage and residual forcing;
    floating coefficients are NOT source-wide/50D interval enclosures.
    """
    t=np.asarray(t_s,float);H=np.asarray(H_s,float)
    vd=np.asarray(vD_V,float);sl=np.asarray(vsl_V,float)
    sa=np.asarray(vsa_V,float);sv=np.asarray(vsv_V,float)
    s=np.asarray(source_current_A,float);j=-np.asarray(package_i34_A,float)
    vals=(t,H,vd,sl,sa,sv,s,j)
    radius=np.asarray([port_radius_V,sv_radius_V,seed_s_radius_A,
                       seed_j_radius_A,alt_forcing_residual_V],float)
    if (any(a.ndim!=1 or not np.isfinite(a).all() for a in vals)
        or len(t)<2 or len(H)<2
        or any(a.shape!=t.shape for a in (vd,sl,sa,sv,s,j))
        or np.any(np.diff(t)<=0) or np.any(np.diff(H)<=0)
        or H[0]<t[0] or H[-1]>t[-1]
        or radius.shape!=(5,) or not np.isfinite(radius).all()
        or np.any(radius<0) or not np.isfinite(float(L_H)) or float(L_H)<=0):
        raise ValueError("finite aligned source rows, positive L and nonnegative radii required")
    L=float(L_H);L2=3.435e-9;R=.003322;Rp=100.
    h=np.diff(t);n=len(t)
    # Literal original source row residuals; KCL is in A, coils in V.
    r1=(sl[1:]-sa[1:])/R+s[1:]
    r25=(sa[1:]-sl[1:])/R+(sa[1:]-sv[1:])/Rp-j[1:]
    r34=-(sa[1:]-sv[1:])-L2*np.diff(j)/h
    r36=-sl[1:]+L*np.diff(s)/h
    f1=r36+(R+Rp)*r1+Rp*r25
    f2=-r34-Rp*(r1+r25)
    d11=L/h+R+Rp;d22=L2/h+Rp;det=d11*d22-Rp**2
    inv00=d22/det;inv01=Rp/det;inv11=d11/det
    p00=inv00*(L/h);p01=inv01*(L2/h)
    p10=inv01*(L/h);p11=inv11*(L2/h)
    right=np.clip(np.searchsorted(t,H,side="right"),1,n-1);left=right-1
    alpha=(H-t[left])/(t[right]-t[left])
    omega=np.empty(len(H))
    omega[0]=(H[1]-H[0])/2;omega[-1]=(H[-1]-H[-2])/2
    omega[1:-1]=(H[2:]-H[:-2])/2
    def apply(z):
        hz=(1-alpha)*z[left]+alpha*z[right]
        a=np.zeros(n)
        np.add.at(a,left,omega*(1-alpha)*hz)
        np.add.at(a,right,omega*alpha*hz)
        return a
    v=vd-sl;a=apply(v);g=apply(s)
    z0=np.zeros(2);zz=np.array([a[-1],0.])
    c_sv=0.;c_f=0.
    er=float(radius[4])
    for i in range(n-2,-1,-1):
        w0=zz[0]*inv00[i]+zz[1]*inv01[i]
        w1=zz[0]*inv01[i]+zz[1]*inv11[i]
        c_sv+=abs(w0)
        c_f+=abs(w0)*(abs(f1[i])+er)+abs(w1)*(abs(f2[i])+er)
        zz=np.array([a[i]+p00[i]*zz[0]+p10[i]*zz[1],
                     p01[i]*zz[0]+p11[i]*zz[1]])
    z0=zz
    # Positive comparison for the future source-current infinity outer.
    us,uj=float(radius[2]),float(radius[3]);umax=us
    for i in range(n-1):
        ef1=abs(f1[i])+er;ef2=abs(f2[i])+er
        ns=p00[i]*us+p01[i]*uj+inv00[i]*(radius[1]+ef1)+inv01[i]*ef2
        nj=p10[i]*us+p11[i]*uj+inv01[i]*(radius[1]+ef1)+inv11[i]*ef2
        us,uj=ns,nj;umax=max(umax,us)
    linear=(float(radius[0])*float(np.sum(abs(g)))
            +float(radius[2])*abs(z0[0])+float(radius[3])*abs(z0[1])
            +float(radius[1])*c_sv+c_f)
    cross=float(radius[0])*(H[-1]-H[0])*umax
    return {"status":"CONDITIONAL_PACKAGE_2COIL_GOAL",
            "point_signed_work_J":float(np.dot(omega,
                ((1-alpha)*v[left]+alpha*v[right])*
                ((1-alpha)*s[left]+alpha*s[right]))),
            "goal_radius_J":float(linear+cross),
            "linear_radius_J":float(linear),
            "bilinear_radius_J":float(cross),
            "prepared_adjoint_J_per_A":z0.tolist(),
            "sv_adjoint_L1_J_per_V":float(c_sv),
            "max_source_current_difference_A":float(umax),
            "source_residual_maxabs":{"r1_A":float(max(abs(r1))),
                "r25_A":float(max(abs(r25))),"r34_V":float(max(abs(r34))),
                "r36_V":float(max(abs(r36))),
                "schur_forcing_V":float(max(np.max(abs(f1)),np.max(abs(f2))))},
            "claim_ceiling":"Finite-H original signed-work radius ONLY for the "
               "supplied reference and a source-legal SAME STATIC L, same-grid "
               "future family with separately certified node22/port/seed/forcing "
               "radii. Source row residuals and coefficients are float64. "
               "Not a future 50D root tube, certified sensor model, "
               "interventional DeltaL response, or Goal27 fiber diameter."}

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


def audit_two_factor_pretarget_interaction(
        B100_nJ, E100_nJ, B150_nJ, *, current_ratio, work_ratio,
        mixed_derivative_abs_bound_nJ=None):
    """Sharp three-corner E150 identifiability gate, without held-out truth.

    The two normalized coordinates label legal B/E own-PREP and 100/150uH.
    An E150 interval requires independently SOURCE-QUALIFIED smooth lawful
    history rectangle and |partial_h partial_l W|<=M over the ENTIRE area.
    With no certified M, three exact corners cannot bound the fourth one.
    """
    from decimal import Decimal, localcontext
    from fractions import Fraction

    def q(value, label):
        if isinstance(value, bool):
            raise ValueError(label + " must be a finite decimal")
        try:
            z = Decimal(str(value))
            if not z.is_finite():
                raise ValueError("nonfinite")
            return Fraction(z)
        except (ValueError, TypeError, ArithmeticError, OverflowError) as exc:
            raise ValueError(label + " must be a finite decimal") from exc

    base = q(B100_nJ, "B100")
    e100 = q(E100_nJ, "E100")
    b150 = q(B150_nJ, "B150")
    r = q(current_ratio, "current_ratio")
    w = q(work_ratio, "work_ratio")
    M = (None if mixed_derivative_abs_bound_nJ is None else
         q(mixed_derivative_abs_bound_nJ, "mixed derivative bound"))
    if M is not None and M < 0:
        raise ValueError("mixed derivative bound must be nonnegative")

    delta = e100-base
    predictions = {
        "additive": b150+delta,
        "current_scaled": b150+r*delta,
        "work_scaled": b150+w*delta,
    }
    interactions = {key: value-predictions["additive"]
                    for key, value in predictions.items()}
    separations = [abs(predictions[a]-predictions[b]) for a,b in (
        ("additive","current_scaled"),("additive","work_scaled"),
        ("current_scaled","work_scaled"))]
    with localcontext() as context:
        context.prec = 65
        def dec(z):
            return format(Decimal(z.numerator)/Decimal(z.denominator), "f")
        return {
            "status": ("THREE_CORNER_UNIDENTIFIED_NO_MIXED_BOUND" if M is None
                       else "CONDITIONAL_UNQUALIFIED_MIXED_DERIVATIVE_BOUND"),
            "evidence": "CALLER_DECIMAL_CORNER_INPUTS_NO_SOURCE_REPLAY",
            "source_root_and_prep_status": "NOT_VERIFIED",
            "E150_new_condition_status": "NOT_OBSERVED_OR_FROZEN",
            "history_delta_nJ": dec(delta),
            "additive_E150_nJ": dec(predictions["additive"]),
            "candidate_predictions_nJ": {k:dec(z) for k,z in predictions.items()},
            "required_interactions_nJ": {k:dec(z) for k,z in interactions.items()},
            "minimum_candidate_gap_nJ": dec(min(separations)),
            "half_minimum_candidate_gap_nJ": dec(min(separations)/2),
            "mixed_derivative_bound_nJ": None if M is None else dec(M),
            "conditional_E150_interval_nJ": None if M is None else [
                dec(predictions["additive"]-M),
                dec(predictions["additive"]+M)],
            "excluded_if_M_source_qualified": ([] if M is None else [
                key for key,z in interactions.items() if abs(z)>M]),
            "claim_ceiling": ("Three original saved history/load corners alone do "
                "not identify the E150 signed-work fourth corner. M needs a "
                "source-qualified lawful smooth PREP/load rectangle and "
                "all-guard H scorer/error outer. Not a true prospective "
                "predictor, source-root certificate or Goal27 range."),
        }
