"""Finite-word goal-oriented recovery with unbounded shared and bounded joint nuisance.

Declared linear chart only: x=Bz, ||z||_2<=1,
y=H x+N eta+E e, eta arbitrary, ||e||_2<=1.
For word w, goal=C A_(last)...A_(first) x. Results are conditional on
common reference, prior, instrument rank and physically legal commands.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from goal_ellipsoid_recovery import recover_scalar_goal


def audit_contextual_goal_recovery(
    updates, state_factor, observation, unbounded_nuisance,
    bounded_noise, goal, words, goal_tolerances, *, rank_rtol=1e-12
):
    """Exact ideal-linear minimax radii for finite words under L-infinity target loss.

    z and e have separate joint unit Euclidean balls; N eta is unbounded.
    Floating rank decisions are diagnostics rather than physical certificates.
    """
    A=np.asarray(updates,dtype=float)
    B=np.asarray(state_factor,dtype=float)
    H=np.asarray(observation,dtype=float)
    N=np.asarray(unbounded_nuisance,dtype=float)
    E=np.asarray(bounded_noise,dtype=float)
    C=np.asarray(goal,dtype=float)
    T=np.asarray(goal_tolerances,dtype=float)
    if A.ndim!=3 or A.shape[1]==0 or A.shape[1]!=A.shape[2]:
        raise ValueError("updates must have shape (commands,n,n), n>0")
    n=A.shape[1]
    if B.shape!=(n,n) or H.ndim!=2 or H.shape[1]!=n:
        raise ValueError("state_factor/observation dimension mismatch")
    m=H.shape[0]
    if N.ndim!=2 or N.shape[0]!=m or E.ndim!=2 or E.shape[0]!=m:
        raise ValueError("nuisance/error factors need m sensor rows")
    if C.ndim!=2 or C.shape[1]!=n or C.shape[0]==0:
        raise ValueError("goals must have at least one state row")
    if T.shape!=(C.shape[0],) or np.any(T<=0):
        raise ValueError("one positive tolerance required per goal")
    if not isinstance(words,(tuple,list)) or not words:
        raise ValueError("provide a nonempty finite command word list")
    if not np.isfinite(rank_rtol) or rank_rtol<=0:
        raise ValueError("rank_rtol must be positive finite")
    if not all(np.isfinite(v).all() for v in (A,B,H,N,E,C,T)):
        raise ValueError("nonfinite model inputs")

    U,sN,_=np.linalg.svd(N,full_matrices=True)
    cutoff=rank_rtol*max(N.shape[0],N.shape[1],1)*(sN[0] if sN.size else 0.)
    rn=int(np.count_nonzero(sN>cutoff))
    U0=U[:,rn:]
    H0=U0.T@H
    E0=U0.T@E

    rows=[]
    for word in words:
        if not isinstance(word,(tuple,list)):
            raise ValueError("words must be index sequences")
        F=np.eye(n)
        for ix in word:
            if not isinstance(ix,(int,np.integer)) or not 0<=ix<len(A):
                raise ValueError("illegal command index")
            F=A[int(ix)]@F
        for index,g in enumerate(C@F):
            r=recover_scalar_goal(B,H0,E0,g)
            w=U0@np.asarray(r["measurement_weights"])
            rows.append({
                "word":[int(ix) for ix in word],
                "goal_index":index,
                "future_goal_row":g.tolist(),
                "radius":r["radius"],
                "goal_tolerance":float(T[index]),
                "relative_radius":r["radius"]/float(T[index]),
                "measurement_weights":w.tolist(),
                "nuisance_weight_residual":float(np.linalg.norm(N.T@w)),
                "algorithm_upper":r["algorithm_upper"],
                "feasible_witness_lower":r["feasible_witness_lower"],
                "numerical_gap":r["numerical_gap"],
                "witness_prior_norm":r["witness_prior_norm"],
                "witness_noiseless_constraint_norm":r["witness_noiseless_constraint_norm"],
                "rank_e":r["noise_rank"],
            })
    return {
        "status":"LINEAR_CONTEXTUAL_MINIMAX_NUMERIC_DIAGNOSTIC",
        "source_state_dimension":n,
        "unbounded_nuisance_rank":rn,
        "nuisance_invariant_sensor_count":int(m-rn),
        "rank_relative_threshold":float(rank_rtol),
        "rows":rows,
        "max_absolute_radius":max(q["radius"] for q in rows),
        "max_radius_relative_to_tolerance":max(q["relative_radius"] for q in rows),
        "meets_all_goal_tolerances":all(q["algorithm_upper"]<=q["goal_tolerance"] for q in rows),
        "scope":"specified finite words, common global linear chart, unrestricted shared nuisance, independent joint B2 state/error bounds; numerical ranks only"
    }


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("input_json")
    p.add_argument("--output")
    a=p.parse_args()
    d=json.loads(Path(a.input_json).read_text(encoding="utf-8"))
    result=audit_contextual_goal_recovery(**d)
    out=json.dumps(result,indent=2,allow_nan=False)+"\n"
    if a.output:
        Path(a.output).write_text(out,encoding="utf-8")
    else:
        print(out,end="")


if __name__=="__main__":
    main()
