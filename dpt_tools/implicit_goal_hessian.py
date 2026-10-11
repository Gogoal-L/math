"""Goal derivatives through one implicit source-law state update.

A discrete source transition is defined by residual F(z, x, u)=0
with z the next state, x the previous state and fixed legal command u.
Residual Hessian last axes are ordered [z, x] (2n,2n).
Requires full actual source derivatives; no device/hardware certificate.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np


def implicit_goal_hessian(current_jacobian, previous_jacobian,
                          residual_hessians, next_goal_gradient,
                          next_goal_hessian):
    """Pull back gradient and Hessian via one source Jacobian and adjoint solve."""
    A = np.asarray(current_jacobian, dtype=float)
    B = np.asarray(previous_jacobian, dtype=float)
    F2 = np.asarray(residual_hessians, dtype=float)
    g = np.asarray(next_goal_gradient, dtype=float)
    G = np.asarray(next_goal_hessian, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1] or A.shape[0] < 1:
        raise ValueError('current Jacobian must be square nonempty')
    n = A.shape[0]
    if B.shape != (n,n) or F2.shape != (n,2*n,2*n) or g.shape != (n,) or G.shape != (n,n):
        raise ValueError('derivative dimensions inconsistent with concatenated [next,previous] residual')
    if not all(np.isfinite(q).all() for q in (A,B,F2,g,G)):
        raise ValueError('finite derivatives required')
    if np.linalg.norm(G-G.T)>1e-9*(1+np.linalg.norm(G)) or any(
        np.linalg.norm(q-q.T)>1e-9*(1+np.linalg.norm(q)) for q in F2
    ):
        raise ValueError('supplied Hessians must be symmetric')
    try:
        J = np.linalg.solve(A,-B)
        lam = np.linalg.solve(A.T,g)
    except np.linalg.LinAlgError as error:
        raise ValueError('implicit current Jacobian must be invertible') from error
    P = np.concatenate([J,np.eye(n)],axis=0)  # old-state a -> (Ja,a)
    Hres = np.einsum('k,kab->ab',lam,F2)
    first = J.T@g
    second = J.T@G@J - P.T@Hres@P
    return {
        'status':'IMPLICIT_SOURCE_GOAL_HESSIAN_NUMERIC_AUDIT',
        'state_dim':n,
        'source_update_jacobian':J.tolist(),
        'adjoint':lam.tolist(),
        'goal_gradient_previous':first.tolist(),
        'goal_hessian_previous':((second+second.T)/2).tolist(),
        'source_jacobian_residual':float(np.linalg.norm(A@J+B)),
        'adjoint_residual':float(np.linalg.norm(A.T@lam-g)),
        'condition_number_current':float(np.linalg.cond(A)),
        'scope':'fixed known command; locally invertible current-state source residual; exact supplied current/previous second derivatives including cross terms; no physical SiC certificate'
    }


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input_json',type=Path)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    result=implicit_goal_hessian(**json.loads(args.input_json.read_text(encoding='utf8')))
    out=json.dumps(result,indent=2,allow_nan=False)+'\n'
    if args.output: args.output.write_text(out,encoding='utf8')
    else: print(out,end='')


if __name__=='__main__':
    main()
