#!/usr/bin/env python3
"""Second-order goal leakage on a REGULAR nonlinear observation fiber.

A local C^2 observation map O:R^n->R^m is a submersion at x0 when
DO(x0) has full row rank. If DG(x0)=b*DO(x0), the goal's second
variation along an exact observation-equality curve with tangent
v in ker DO is v.T * [D2G-sum_i b_i D2O_i] * v.

This elementary implicit-function calculation is a local curvature
WITNESS, not a finite-radius bound or a proof of physical reachability.
The input coordinates must parametrize admissible histories, and each
second derivative must be from the same pretarget goal/observation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def _finite_array(data, name, shape):
    a = np.asarray(data, dtype=float)
    if a.shape != shape or not np.all(np.isfinite(a)):
        raise ValueError(f'{name} must have finite shape {shape}; got {a.shape}')
    return a


def _tolerance(v, name):
    x = float(v)
    if not np.isfinite(x) or x < 0:
        raise ValueError(f'{name} must be nonnegative finite')
    return x


def audit(observation_jacobian, goal_gradient, observation_hessians,
          goal_hessian, *, rtol=1e-10, atol=1e-12,
          factorization_tol=1e-8, symmetry_tol=1e-10,
          curvature_tol=1e-10):
    rt = _tolerance(rtol, 'rtol')
    at = _tolerance(atol, 'atol')
    ft = _tolerance(factorization_tol, 'factorization_tol')
    st = _tolerance(symmetry_tol, 'symmetry_tol')
    ct = _tolerance(curvature_tol, 'curvature_tol')
    jo = np.asarray(observation_jacobian, dtype=float)
    if jo.ndim != 2 or jo.shape[0] < 1 or jo.shape[1] < jo.shape[0] or not np.all(np.isfinite(jo)):
        raise ValueError('observation_jacobian must be finite (m,n), 1 <= m <= n')
    m, n = jo.shape
    dg = _finite_array(goal_gradient, 'goal_gradient', (n,))
    ho = _finite_array(observation_hessians, 'observation_hessians', (m,n,n))
    hg = _finite_array(goal_hessian, 'goal_hessian', (n,n))
    for name, matrices in [('goal_hessian', hg[None,:,:]),
                           ('observation_hessians', ho)]:
        for h in matrices:
            if np.linalg.norm(h-h.T, ord='fro') > st * max(1.0, np.linalg.norm(h, ord='fro')):
                raise ValueError(name + ' must contain symmetric Hessians')
    ho = .5*(ho + ho.transpose(0,2,1))
    hg = .5*(hg + hg.T)
    _, singular, vt = np.linalg.svd(jo, full_matrices=True)
    cutoff = max(at, rt*float(singular[0]))
    rank = int(np.count_nonzero(singular > cutoff))
    if rank != m:
        raise ValueError('observation Jacobian is not full row rank at declared cutoff; submersion not qualified')
    null = vt[m:,:].T
    hidden = n-m
    b = np.linalg.lstsq(jo.T, dg, rcond=None)[0]
    linear_residual = float(np.linalg.norm(dg-b@jo))
    hidden_gain = float(np.linalg.norm(dg@null))
    report = {
        'schema_version':1,
        'status': None,
        'observation_rows':m,
        'state_dimension':n,
        'hidden_dimension':hidden,
        'observation_rank':rank,
        'first_order_hidden_gain':hidden_gain,
        'first_order_factorization_residual':linear_residual,
        'goal_observation_factor':b.tolist(),
        'max_absolute_fiber_curvature':None,
        'quadratic_goal_gap_coefficient':None,
        'witness':None,
        'rank_tolerances':{'relative':rt,'absolute':at,'factorization_absolute':ft, 'curvature_absolute':ct},
        'claim_ceiling': (
            'Second-order Taylor coefficient only for a C2 scalar goal and regular '
            'C2 observation submersion on an admissible history chart; no '
            'uniform finite-radius bound or native DPT prediction is implied. '
            'Numerical rank/tolerance and near-zero factorization are not certified. Zero quadratic curvature '
            'does not establish exact sufficiency: cubic and higher terms remain.'
        ),
    }
    if hidden == 0:
        report['status']='NO_HIDDEN_DIRECTIONS'
        return report
    if max(linear_residual,hidden_gain) > ft:
        report['status']='FIRST_ORDER_LEAK'
        return report
    # Even a small nonzero linear leak eventually dominates a quadratic one.
    numeric_zero = 64*np.finfo(float).eps*max(1.,float(np.linalg.norm(dg)))
    if max(linear_residual,hidden_gain) > numeric_zero:
        report['status']='NEAR_FIRST_ORDER_FACTOR'
        return report
    effective = hg - np.tensordot(b,ho,axes=(0,0))
    effective = .5*(effective+effective.T)
    reduced = null.T @ effective @ null
    ev, eig = np.linalg.eigh(reduced)
    index = int(np.argmax(np.abs(ev)))
    curvature = float(ev[index])
    v = null @ eig[:,index]
    # Pick a minimum-norm second derivative x'' satisfying the exact
    # observation fiber equation DO x'' + D2O[v,v] = 0.
    hobs=np.einsum('i,aij,j->a',v,ho,v)
    w=-np.linalg.lstsq(jo,hobs,rcond=None)[0]
    actual_goal_second = float(v @ hg @ v + dg @ w)
    quadratic = .5*abs(curvature)
    report.update({
        'status':'QUADRATIC_WITNESS' if quadratic > ct else 'QUADRATIC_ZERO_NOT_SUFFICIENCY',
        'max_absolute_fiber_curvature':abs(curvature),
        'quadratic_goal_gap_coefficient':quadratic,
        'signed_extremal_curvature':curvature,
        'witness': {
            'hidden_unit_tangent': v.tolist(),
            'fiber_second_derivative':w.tolist(),
            'observation_tangent_residual':float(np.linalg.norm(jo@v)),
            'observation_second_order_residual':float(np.linalg.norm(jo@w + hobs)),
            'goal_second_derivative':actual_goal_second,
            'effective_hessian_prediction':float(v@effective@v),
        },
    })
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path,help='JSON: observation_jacobian, goal_gradient, observation_hessians, goal_hessian')
    p.add_argument('--output',type=Path)
    p.add_argument('--rtol',type=float,default=1e-10)
    p.add_argument('--atol',type=float,default=1e-12)
    p.add_argument('--factorization-tol',type=float,default=1e-8)
    a=p.parse_args()
    data=json.loads(a.input.read_text(encoding='utf-8'))
    keys=['observation_jacobian','goal_gradient','observation_hessians','goal_hessian']
    missing=[x for x in keys if x not in data]
    if missing:p.error('missing fields: '+', '.join(missing))
    result=audit(*(data[k] for k in keys),rtol=a.rtol,atol=a.atol,
                 factorization_tol=a.factorization_tol)
    text=json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+'\n'
    if a.output:a.output.write_text(text,encoding='utf-8')
    else:print(text,end='')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
