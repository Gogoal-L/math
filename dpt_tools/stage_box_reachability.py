#!/usr/bin/env python3
"""Conservative stage-by-stage affine box-inclusion certificate.

For a known common-chart stage map x_next = A_k x + b_k + r_k with
componentwise |r_k| <= eps_k throughout a specified admissible box,
propagate an interval outer approximation. If each resulting box lies
inside the declared next-stage admissible box, all trajectories
admissible under these premises remain qualified at every stage.

A negative check is INCONCLUSIVE, not a proof of physical failure;
interval boxes discard correlations. Point Jacobians, unqualified
nonlinear remainders, guard changes, and DAE chart changes do not
satisfy the premises automatically.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def _finite(data,name,ndim):
    v=np.asarray(data,dtype=float)
    if v.ndim!=ndim or not np.all(np.isfinite(v)):
        raise ValueError(f'{name} must be finite {ndim}D array')
    return v


def audit(updates, offsets, initial_lower, initial_upper,
          admissible_lower, admissible_upper, remainder_radii, *, atol=1e-12):
    tol=float(atol)
    if not np.isfinite(tol) or tol<0:raise ValueError('atol must be finite nonnegative')
    a=_finite(updates,'updates',3)
    steps,n,n2=a.shape
    if n<1 or n2!=n:raise ValueError('updates must have shape (H,n,n) with n >= 1')
    b=_finite(offsets,'offsets',2)
    lo=_finite(initial_lower,'initial_lower',1)
    hi=_finite(initial_upper,'initial_upper',1)
    guards_lo=_finite(admissible_lower,'admissible_lower',2)
    guards_hi=_finite(admissible_upper,'admissible_upper',2)
    e=_finite(remainder_radii,'remainder_radii',2)
    if (b.shape!=(steps,n) or lo.shape!=(n,) or hi.shape!=(n,)
        or e.shape!=(steps,n) or guards_lo.shape!=(steps+1,n)
        or guards_hi.shape!=(steps+1,n)):
        raise ValueError('offsets, initial, stage domains and remainder radii have inconsistent shapes')
    if (np.any(lo>hi) or np.any(guards_lo>guards_hi) or np.any(e<0)):
        raise ValueError('box bounds must be ordered and errors nonnegative')
    if np.any(lo<guards_lo[0]) or np.any(hi>guards_hi[0]):
        raise ValueError('initial uncertainty box lies outside stage-0 admissible domain')
    tube=[{'stage':0,'lower':lo.tolist(),'upper':hi.tolist()}]
    min_margin=float(min(np.min(lo-guards_lo[0]),np.min(guards_hi[0]-hi)))
    result={
        'schema_version':1,
        'model_type':'AFFINE_STAGE_BOX_WITH_COMPONENTWISE_REMAINDER',
        'status':'CONDITIONAL_AFFINE_BOX_CHAIN',
        'state_dimension':n,
        'command_steps':steps,
        'validated_steps':0,
        'first_failed_stage':None,
        'violation_by_dimension':None,
        'tube':tube,
        'atol':tol,
        'minimum_guard_margin':min_margin,
        'roundoff_margin_warning':bool(min_margin<=tol),
        'claim_ceiling':(
            'Positive containment is a conditional floating-point outer-box check ONLY '
            'if each given affine map and absolute componentwise remainder bound '
            'hold on the ENTIRE supplied stage box, and all guards/charts match. '
            'A failed conservative interval check does NOT imply actual physical '
            'escape; correlated reachable states can be much smaller than the box. '
            'Floating arithmetic is not directed interval arithmetic; roundoff-level cases need rigorous outward rounding before certification. Point Jacobians or synthetic tests do not verify native DPT or hardware.'
        ),
    }
    for k in range(steps):
        # Exact coordinatewise interval hull of the affine image of a box.
        lower_terms=np.minimum(a[k]*lo[None,:],a[k]*hi[None,:])
        upper_terms=np.maximum(a[k]*lo[None,:],a[k]*hi[None,:])
        next_lo=b[k] + lower_terms.sum(axis=1) - e[k]
        next_hi=b[k] + upper_terms.sum(axis=1) + e[k]
        if not np.all(np.isfinite(next_lo)) or not np.all(np.isfinite(next_hi)):
            raise ValueError('nonfinite propagated stage box; rescale coordinates')
        tube.append({'stage':k+1,'lower':next_lo.tolist(),'upper':next_hi.tolist()})
        margin=float(min(np.min(next_lo-guards_lo[k+1]),np.min(guards_hi[k+1]-next_hi)))
        min_margin=min(min_margin,margin)
        result['minimum_guard_margin']=min_margin
        result['roundoff_margin_warning']=bool(min_margin<=tol)
        violated=np.maximum(guards_lo[k+1]-next_lo,0)+np.maximum(next_hi-guards_hi[k+1],0)
        if np.any(violated>0):
            result.update({'status':'INCONCLUSIVE_BOX_CONTAINMENT','first_failed_stage':k+1,
                           'violation_by_dimension':violated.tolist()})
            return result
        result['validated_steps']=k+1
        lo,hi=next_lo,next_hi
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path,help='NPZ with updates, offsets, initial_lower/upper, admissible_lower/upper, remainder_radii')
    p.add_argument('--output',type=Path)
    p.add_argument('--atol',type=float,default=1e-12)
    args=p.parse_args()
    keys=['updates','offsets','initial_lower','initial_upper','admissible_lower',
          'admissible_upper','remainder_radii']
    with np.load(args.input,allow_pickle=False) as data:
        missing=[k for k in keys if k not in data]
        if missing:p.error('missing required NPZ fields: '+', '.join(missing))
        report=audit(*(data[k] for k in keys),atol=args.atol)
    text=json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(text,encoding='utf-8')
    else:print(text,end='')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
