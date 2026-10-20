"""Conditional exact two-checkpoint box/goal dual and original S150 ETH arithmetic.

This is a *model-domain* certificate. Input source vectors need separate SHA,
state/guard qualification and full-source rooted history validation.
"""
from __future__ import annotations
from fractions import Fraction as F


def _f(value):
    if isinstance(value, bool):
        raise ValueError("boolean is not a rational input")
    return F(value)


def certify_two_zero_charge_rows(goal, charge_rows, pivots, bound=1):
    """Prove sharp max a.u for |u_i|<=bound and C.u=(0,0).

    Equal primal/dual values are checked in exact rational arithmetic. A bad
    vertex/pivot must fail closed; a successful certificate says nothing about
    source legality of the coordinatewise box or about pretarget sensor access.
    """
    a=tuple(map(_f,goal))
    if len(a)<3 or len(charge_rows)!=2:
        raise ValueError("expected at least 3 coordinates and two charge rows")
    c0,c1=(tuple(map(_f,row)) for row in charge_rows)
    if len(c0)!=len(a) or len(c1)!=len(a):
        raise ValueError("charge row dimensions mismatch")
    bound=_f(bound)
    if bound<=0:
        raise ValueError("positive box bound required")
    if len(pivots)!=2 or len(set(pivots))!=2 or any(
        not isinstance(i,int) or i<0 or i>=len(a) for i in pivots
    ):
        raise ValueError("two distinct valid pivot indices required")
    p,q=pivots
    det=c0[p]*c1[q]-c0[q]*c1[p]
    if not det:
        raise ValueError("singular checkpoint pivot")
    lam0=(a[p]*c1[q]-a[q]*c1[p])/det
    lam1=(c0[p]*a[q]-c0[q]*a[p])/det
    residual=[a[i]-lam0*c0[i]-lam1*c1[i] for i in range(len(a))]
    u=[bound*(1 if x>0 else -1 if x<0 else 0) for x in residual]
    u[p]=u[q]=F(0)
    target0=-sum(c0[i]*u[i] for i in range(len(a)))
    target1=-sum(c1[i]*u[i] for i in range(len(a)))
    u[p]=(target0*c1[q]-target1*c0[q])/det
    u[q]=(c0[p]*target1-c1[p]*target0)/det
    if max(map(abs,u))>bound:
        raise ValueError("infeasible pivot: zero-charge primal violates box")
    checkpoints=(sum(x*y for x,y in zip(c0,u)),
                 sum(x*y for x,y in zip(c1,u)))
    primal=sum(x*y for x,y in zip(a,u))
    dual=bound*sum(map(abs,residual))
    if checkpoints!=(0,0) or primal!=dual:
        raise ArithmeticError("invalid exact primal/dual witness")
    return {
        "radius":primal,"unconstrained_radius":bound*sum(map(abs,a)),
        "primal":primal,"dual":dual,
        "witness":tuple(u),"checkpoint_residuals":checkpoints,
        "dual_weights":(lam0,lam1),
        "claim_ceiling":"SHARP_TWO_ROW_LINEAR_BOX_ONLY_NOT_SOURCE_50D",
    }



def certify_one_zero_charge_row(goal, charge_row, pivot, bound=1):
    """Exact sharp support of |u|<=D and ONE zero charge constraint.

    A bad pivot is not an approximate certificate: it is rejected. This
    operation does not supply source legality or a pretarget sensor contract.
    """
    a=tuple(map(_f,goal))
    c=tuple(map(_f,charge_row))
    D=_f(bound)
    if len(a)<2 or len(c)!=len(a):
        raise ValueError("goal/charge dimensions mismatch")
    if D<=0 or not isinstance(pivot,int) or not (0<=pivot<len(a)):
        raise ValueError("invalid box bound or pivot")
    if not c[pivot]:
        raise ValueError("singular checkpoint pivot")
    lam=a[pivot]/c[pivot]
    residual=tuple(a[j]-lam*c[j] for j in range(len(a)))
    u=[D*(1 if x>0 else -1 if x<0 else 0) for x in residual]
    u[pivot]=-sum(c[j]*u[j] for j in range(len(a)) if j!=pivot)/c[pivot]
    if abs(u[pivot])>D:
        raise ValueError("infeasible pivot: zero-charge primal violates box")
    cp=sum(c[j]*u[j] for j in range(len(a)))
    primal=sum(a[j]*u[j] for j in range(len(a)))
    dual=D*sum(abs(x) for x in residual)
    if cp or primal!=dual:
        raise ArithmeticError("invalid exact one-row primal/dual witness")
    return {
        "radius":primal,"unconstrained_radius":D*sum(map(abs,a)),
        "primal":primal,"dual":dual,"witness":tuple(u),
        "checkpoint_residual":cp,"dual_weight":lam,
        "claim_ceiling":"SHARP_ONE_ROW_LINEAR_BOX_ONLY_NOT_SOURCE_50D",
    }


def coil_be_goal_charge_rows(fine_current_goal_coeff, dt_s, voltage_bound_V,
                             source_Ls_H, half_fine_index):
    """Original-coil BE and two fine-PL port-charge rows, exact rational.

    dt_s is either a common positive step or the FULL sequence of n-1 actual
    stored binary64 fine-grid steps. Source replay MUST supply those steps;
    rounding every interval to a nominal 12.5ps is NOT bitwise source-exact.
    The first prepared source-current perturbation is fixed at zero.
    Charge rows divide out ONE common positive factor
    voltage_bound*steps[0]**2/Ls. This is harmless for PERFECT zero-charge
    equalities, but not for actual sensor-error units until restored.
    """
    a=tuple(map(_f,fine_current_goal_coeff))
    n=len(a)
    eps,L=map(_f,(voltage_bound_V,source_Ls_H))
    if isinstance(dt_s,(str,bytes)):
        steps=(_f(dt_s),)*(n-1)
    else:
        try:
            steps=tuple(map(_f,dt_s))
        except TypeError:
            steps=(_f(dt_s),)*(n-1)
    if (n<3 or len(steps)!=n-1 or
            not isinstance(half_fine_index,int) or
            not (0<half_fine_index<n-1) or eps<=0 or L<=0 or
            any(s<=0 for s in steps)):
        raise ValueError("invalid source coil grid or positive units")
    suffix=F(0)
    b=[F(0)]*(n-1)
    for m in range(n-1,0,-1):
        suffix+=a[m]
        b[m-1]=eps*steps[m-1]/L*suffix

    def normalized_charge_row(lo,hi):
        # Integrate ds at adjacent fine time nodes using the ACTUAL PL dt.
        weights=[F(0)]*n
        for j in range(lo,hi):
            weights[j]+=steps[j]/2
            weights[j+1]+=steps[j]/2
        suffix=F(0)
        row=[F(0)]*(n-1)
        scale=steps[0]*steps[0]
        for m in range(n-1,0,-1):
            suffix+=weights[m]
            row[m-1]=steps[m-1]*suffix/scale
        return tuple(row)
    return tuple(b),(
        normalized_charge_row(0,half_fine_index),
        normalized_charge_row(half_fine_index,n-1),
    )


def original_eth_fraction(gate_minus_source_V, raw_temperature_C):
    """S150 actual_law.py eth_literal, exact decimal coefficients, real law.

    Source ZIP SHA256 250aa4ea17514ffdeda3a51d95bedf8e034b181f97bdc254db29ddc36281b9c8;
    source member 51b78f729393d29745f59ca150adfef69e1847bf26a8853c6cef3d6be9e2083d.
    Raw tj (NOT tjc) occurs in HIGH gr^2/gr, LOW gr coefficients.
    This does not prove original binary64/libm outward enclosure or any root.
    """
    clip=lambda x,lo,hi:max(F(lo),min(F(hi),x))
    tj=_f(raw_temperature_C)
    g=_f(gate_minus_source_V)
    u=clip(g,-8,19);gr=clip(g,-8,15);tc=clip(tj,-60,260)
    t=tc
    net3=clip(F("8.381e-6")*t**2-F("4.696e-3")*t+F("2.8224"),
              F("1.7"),F("3.2"))
    if u>net3:
        val=(
            (-F("22.48e-6")*t**3+F("5.637e-3")*t**2+F("87.27e-3")*t-F("59.02"))*gr**3
            +(F("567.2e-6")*t**3-F("0.1404")*t**2-F("2.866")*tj+F("1502.6"))*gr**2
            +(-F("3.728e-3")*t**3+F("0.9245")*t**2+F("20.77")*tj-F("9359.8"))*gr
            +(F("5.447e-3")*t**3-F("1.424")*t**2-F("31.8")*t+F("13239.5"))
        )/1000
    else:
        val=(
            (F("3.788e-6")*t**3-F("2.125e-3")*t**2+F("0.2401")*t-F("10.98"))*gr**2
            +(F("18.97e-6")*t**3-F("8.24e-3")*t**2+F("1.272")*tj-F("339.4"))*gr
            +(F("20.94e-6")*t**3+F("6.024e-3")*t**2-F("3.617")*t-F("1063.7"))
        )/1000
    return clip(val,-3,15)


def certify_three_read_shared_bias_dual(
    goal, charge_rows, dual_weights, rho, bias_bound,
    *, witness=None, measurement_errors=None, bound=1,
):
    """Exact conditional signed-goal support with THREE centered port charges.

    The source-row-only model is |u_i|<=bound, goal b.u [nJ], future
    charges Q1=C0.u and Q2=C1.u [nC]. Three raw centered sensor readings
    are y=(0,0,0), true levels q=(0,Q1,Q1+Q2), ONE shared record bias beta
    |beta|<=B [nC], and independent |e0,e1,e2|<=rho [nC].
    Thus e0=-beta, C0.u=e0-e1, C1.u=e1-e2. For lambda=(l1,l2) [V],
    a correct EXACT dual upper is
       ||b-C.T*l||_1*bound +
       rho*(|l1-l2|+|l2|) + min(rho,B)*|l1|.
    This respects the COMMON error/bias geometry, not two independent
    differenced error boxes. A supplied feasible primal with objective
    exactly equal to this dual makes the reported radius SHARP for the
    declared LP; otherwise the result is only a valid upper bound.
    Actual SOURCE 6720D source rows, PRETARGET feasibility, sensor E,
    50D roots, voltage dynamics and future H841 are external obligations.
    """
    b=tuple(map(_f,goal))
    if len(charge_rows)!=2:
        raise ValueError("two cumulative PORT charge rows required")
    C0,C1=(tuple(map(_f,c)) for c in charge_rows)
    if len(b)<2 or len(C0)!=len(b) or len(C1)!=len(b):
        raise ValueError("invalid goal/charge dimensions")
    if len(dual_weights)!=2:
        raise ValueError("two dual multipliers required")
    l1,l2=map(_f,dual_weights)
    rho,B,D=map(_f,(rho,bias_bound,bound))
    if rho<0 or B<0 or D<=0:
        raise ValueError("invalid nonnegative sensor bounds or box")
    remainder=sum((abs(b[i]-l1*C0[i]-l2*C1[i])
                   for i in range(len(b))),F(0))*D
    noise=rho*(abs(l1-l2)+abs(l2))+min(rho,B)*abs(l1)
    dual=remainder+noise
    unconstrained=D*sum(map(abs,b))
    out={
        "dual":dual,"radius_upper":min(dual,unconstrained),
        "unconstrained_radius":unconstrained,
        "correlated_sensor_support":noise,
        "primal":None,"radius":None,"sharp_certified":False,
        "source_50d_goal_certified":False,
        "claim_ceiling":"Sharp ONLY if exact primal=dual in declared linear "
           "future-port source-row LP; no pretarget CAL gain/Goal27.",
    }
    if (witness is None)!=(measurement_errors is None):
        raise ValueError("witness and measurement errors must appear together")
    if witness is None:
        return out
    u=tuple(map(_f,witness))
    e=tuple(map(_f,measurement_errors))
    if len(u)!=len(b) or len(e)!=3 or any(abs(x)>D for x in u):
        raise ValueError("invalid bounded primal")
    if abs(e[0])>B or any(abs(x)>rho for x in e):
        raise ValueError("infeasible shared bias or per-reading sensor errors")
    q1=sum((x*y for x,y in zip(C0,u)),F(0))
    q2=sum((x*y for x,y in zip(C1,u)),F(0))
    cp=(q1-(e[0]-e[1]),q2-(e[1]-e[2]))
    if cp!=(0,0):
        raise ValueError("infeasible cumulative-charge primal")
    p=sum((x*y for x,y in zip(b,u)),F(0))
    if p!=dual:
        raise ArithmeticError("exact shared-bias primal/dual gap not closed")
    out.update(primal=p,radius=p,sharp_certified=True,charge_residuals=cp)
    return out
