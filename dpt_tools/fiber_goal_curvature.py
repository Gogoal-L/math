#!/usr/bin/env python3
"""Second-order scalar goal recovery on a *regular exact observation fiber*.

At h0, let O(h)=O(h0) be a C3 submersion and G be a C3 scalar goal.
Require DG(h0) restricted to ker(DO(h0)) = 0. If DG=lambda @ DO and Z
spans ker(DO), the relative fiber Hessian is
 Q=Z.T @ (D2G-sum(lambda_j D2O_j)) @ Z.
For orthonormal tangent chart coordinates v within radius r, the quadratic
minimax scalar risk is r^2/4 times the Hessian eigenvalue span including 0.
A certified uniform third derivative on the *composed true fiber goal*
provides a +/-r^3/6 error band. This tool does NOT certify physical source
replay, nonlinear chart existence on finite r, source reachability or guards.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np


def audit_fiber_goal_curvature(
    observation_jacobian, goal_gradient, observation_hessians,
    goal_hessian, radius, fiber_third_derivative_bound=None, *,
    rank_rtol=1e-11
):
    O=np.asarray(observation_jacobian,dtype=float)
    g=np.asarray(goal_gradient,dtype=float)
    OH=np.asarray(observation_hessians,dtype=float)
    GH=np.asarray(goal_hessian,dtype=float)
    if O.ndim!=2:
        raise ValueError('observation_jacobian must be a two-dimensional array')
    m,n=O.shape
    if n<1 or g.shape!=(n,) or OH.shape!=(m,n,n) or GH.shape!=(n,n):
        raise ValueError('incompatible gradient and Hessian dimensions')
    if not all(np.isfinite(a).all() for a in (O,g,OH,GH)):
        raise ValueError('nonfinite source derivatives')
    if not (np.isfinite(rank_rtol) and 0<rank_rtol<1):
        raise ValueError('rank_rtol must be between 0 and 1')
    if not np.isfinite(radius) or radius<=0:
        raise ValueError('radius must be positive')
    if fiber_third_derivative_bound is not None and (
        not np.isfinite(fiber_third_derivative_bound)
        or fiber_third_derivative_bound<0
    ):
        raise ValueError('fiber third derivative bound must be nonnegative')
    if np.linalg.norm(GH-GH.T)>rank_rtol*(1+np.linalg.norm(GH)) or any(
        np.linalg.norm(a-a.T)>rank_rtol*(1+np.linalg.norm(a)) for a in OH
    ):
        raise ValueError('Hessian matrices must be symmetric')
    _,s,vt=np.linalg.svd(O,full_matrices=True)
    rank=int(np.count_nonzero(
        s>rank_rtol*max(m,n,1)*(s[0] if s.size else 0)))
    if rank!=m:
        raise ValueError('observation Jacobian must have full row rank (regular submersion)')
    multiplier=np.linalg.lstsq(O.T,g,rcond=None)[0]
    residual=float(np.linalg.norm(g-O.T@multiplier))
    if residual>rank_rtol*max(1.,float(np.linalg.norm(g))):
        raise ValueError('goal tangent gradient must vanish for a second-order-only audit')
    Z=vt[m:,:].T.copy()
    Hrelative=GH-np.einsum('j,jkl->kl',multiplier,OH)
    Q=Z.T@Hrelative@Z
    Q=(Q+Q.T)/2
    vals=np.linalg.eigvalsh(Q)
    eigmax=float(vals[-1]) if vals.size else 0.
    eigmin=float(vals[0]) if vals.size else 0.
    upper_quad=.5*radius**2*max(0.,eigmax)
    lower_quad=.5*radius**2*min(0.,eigmin)
    rquad=(upper_quad-lower_quad)/2
    if fiber_third_derivative_bound is None:
        radius_lower=radius_upper=None
        remainder=None
    else:
        remainder=float(fiber_third_derivative_bound)*radius**3/6
        radius_lower=max(0.,rquad-remainder)
        radius_upper=rquad+remainder
    threshold=rank_rtol*max(1.,float(np.max(np.abs(vals))) if vals.size else 0.)
    return {
        'status':'REGULAR_FIBER_SECOND_ORDER_NUMERIC_AUDIT',
        'state_dim':n,
        'observation_rank':m,
        'fiber_dim':n-m,
        'multipliers':multiplier.tolist(),
        'null_basis':Z.tolist(),
        'factorization_residual':residual,
        'relative_hessian':Q.tolist(),
        'curvature_eigenvalues':vals.tolist(),
        'curvature_inertia':{
            'positive':int(np.count_nonzero(vals>threshold)),
            'negative':int(np.count_nonzero(vals<-threshold)),
            'zero':int(np.count_nonzero(np.abs(vals)<=threshold))},
        'quadratic_minimax_radius':float(rquad),
        'goal_quadratic_min':float(lower_quad),
        'goal_quadratic_max':float(upper_quad),
        'third_order_radius_error':remainder,
        'radius_lower':radius_lower,
        'radius_upper':radius_upper,
        'rank_rtol':rank_rtol,
        'scope':'local exact regular observation fiber; orthonormal tangent chart norm<=radius; finite-r bounds require externally verified C3 fiber third derivative; not physical SiC proof',
    }


def pullback_goal_derivatives(update_jacobian, update_hessians,
                              next_goal_gradient, next_goal_hessian):
    """Exact single-command backward gradient/Hessian pullback on one source trajectory.

    For f:R^n->R^n and scalar next goal g, computes derivatives of g(f(x)).
    Repeat in reverse chronological command order, with every stage evaluated
    at its proper legally reached state; no forward Hessian of full word needed.
    """
    J=np.asarray(update_jacobian,dtype=float)
    HF=np.asarray(update_hessians,dtype=float)
    g=np.asarray(next_goal_gradient,dtype=float)
    H=np.asarray(next_goal_hessian,dtype=float)
    if J.ndim!=2 or J.shape[0]!=J.shape[1]:
        raise ValueError('command Jacobian must be square')
    n=J.shape[0]
    if HF.shape!=(n,n,n) or g.shape!=(n,) or H.shape!=(n,n):
        raise ValueError('command derivatives and next-goal dimensions disagree')
    if not all(np.isfinite(t).all() for t in (J,HF,g,H)):
        raise ValueError('command derivatives must be finite')
    if np.linalg.norm(H-H.T)>1e-9*(1+np.linalg.norm(H)) or any(
        np.linalg.norm(q-q.T)>1e-9*(1+np.linalg.norm(q)) for q in HF
    ):
        raise ValueError('command and goal Hessians must be symmetric')
    first=J.T@g
    second=J.T@H@J+np.einsum('i,ijk->jk',g,HF)
    return first,(second+second.T)/2


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input_json',type=Path)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    obj=json.loads(args.input_json.read_text(encoding='utf8'))
    result=audit_fiber_goal_curvature(**obj)
    output=json.dumps(result,indent=2,allow_nan=False)+'\n'
    if args.output: args.output.write_text(output,encoding='utf8')
    else: print(output,end='')


if __name__=='__main__':
    main()
