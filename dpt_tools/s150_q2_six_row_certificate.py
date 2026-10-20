"""Original S150 Q2 ON six-row local root proof implication (Fraction).

SOURCE AUTHENTICATION IS EXTERNAL. Original saved floats/source coefficients
must be independently SHA verified; these formula-only tests cannot prove the
other 44 full-50 source rows or the complementary root/guard histories.
"""
from fractions import Fraction as F

LAW_SHA="51b78f729393d29745f59ca150adfef69e1847bf26a8853c6cef3d6be9e2083d"
ADAPTER_SHA="7f03e36809caf3dea1295cf58d7dd70c413ef7991472a5e6eec3405da18f5669"
SAVED_SHA="baafdd8cb489adb186677658c4a8031130cc53a9a1854c4997211d437daf8b3e"
C=tuple(map(F,("0.00131","0.006698","0.01941","0.07301")))
R=tuple(map(F,("0.06378","0.1553","0.09942","0.1417")))


def _fraction(x):
    if isinstance(x,bool):
        raise ValueError("boolean is not a physical rational")
    return F(x)


def _solve(M, rhs):
    """Small square Gauss-Jordan over exact rationals, no float rank tests."""
    n=len(M)
    x=[[F(t) for t in M[i]]+[F(rhs[i])] for i in range(n)]
    for j in range(n):
        k=next((k for k in range(j,n) if x[k][j]),None)
        if k is None:
            raise ValueError("singular original thermal matrix")
        x[k],x[j]=x[j],x[k]
        pivot=x[j][j]
        x[j]=[e/pivot for e in x[j]]
        for i in range(n):
            if i!=j:
                q=x[i][j]
                x[i]=[a-q*b for a,b in zip(x[i],x[j])]
    return tuple(x[i][-1] for i in range(n))


def source_thermal_affine_exact(old_temperature_C, h_s):
    """Real-decimal source thermal 4x4 linear BE elimination.

    Original actual_law.py _memory_rev6_thermal_matrices uses C and R
    listed above. Solve (K+C/h)T=K*25*1+(C/h)*T_old+e0*heat.
    """
    old=tuple(map(_fraction,old_temperature_C))
    h=_fraction(h_s)
    if len(old)!=4 or h<=0:
        raise ValueError("expected four source old thermal nodes and h>0")
    gg=[1/r for r in R]
    g0,g1,g2,g3=gg
    K=((g0,-g0,F(0),F(0)),
       (-g0,g0+g1,-g1,F(0)),
       (F(0),-g1,g1+g2,-g2),
       (F(0),F(0),-g2,g2+g3))
    A=[[K[i][j]+(C[i]/h if i==j else 0) for j in range(4)]
       for i in range(4)]
    beta_rhs=[sum(K[i][j]*25 for j in range(4))+C[i]*old[i]/h
              for i in range(4)]
    beta=_solve(A,beta_rhs)
    alpha=_solve(A,(1,0,0,0))
    old0_transfer=_solve(A,(C[0]/h,0,0,0))[0]
    return beta,alpha,old0_transfer


def certify_q2_on_subsystem(
    old_temperature_C,h_s,*,source_kappa,source_law_sha256,
    source_adapter_sha256,saved_cal_sha256,
    body_left_upper_V,body_right_lower_V,
    channel_temperature_derivative_bound_A_per_C,
    drain_span_abs_bound_V,heat_upper_W,
    T0_interval_C=("25","25.04"),
    other_temperature_interval_C=("24.99","25.05"),
):
    """Strict one-branch six-row existence/uniqueness *given* source outers.

    The body source bounds and source-channel derivative bound must be proved
    over every declared Q2 ON candidate voltage/thermal point independently:
    this routine verifies their Banach CONSEQUENCES, not original ZIP bytes.
    Original Pro18E n=3616 old full50 and adapter kappa=1.007 are pinned.
    """
    if (source_law_sha256!=LAW_SHA or source_adapter_sha256!=ADAPTER_SHA
            or saved_cal_sha256!=SAVED_SHA):
        raise ValueError("unqualified source SHA identity")
    kappa=_fraction(source_kappa)
    if kappa!=F("1.007"):
        raise ValueError("source adapter kappa must match saved original 1.007")
    left,right=map(_fraction,(body_left_upper_V,body_right_lower_V))
    if not (left<0<right):
        raise ValueError("body root bracket must have strict opposite signs")
    dch,dspan,Hmax=map(_fraction,(
        channel_temperature_derivative_bound_A_per_C,
        drain_span_abs_bound_V,heat_upper_W))
    Tlo,Thi=map(_fraction,T0_interval_C)
    Olo,Ohi=map(_fraction,other_temperature_interval_C)
    if dch<0 or dspan<0 or Hmax<0 or Tlo>=Thi or Olo>=Ohi:
        raise ValueError("invalid source heat/temperature envelope")
    beta,alpha,zeta=source_thermal_affine_exact(old_temperature_C,h_s)
    if any(a<0 for a in alpha):
        raise ValueError("thermal affine heating direction not positive")
    root_image=(beta[0],beta[0]+alpha[0]*Hmax)
    if not (Tlo<root_image[0]<=root_image[1]<Thi):
        raise ValueError("thermal self-map not strictly inside source cell")
    if any(not(Olo<beta[i]<=beta[i]+alpha[i]*Hmax<Ohi)
           for i in range(1,4)):
        raise ValueError("other thermal root image outside declared box")
    Lipschitz_H=kappa*dspan*dch
    contraction=alpha[0]*Lipschitz_H
    if not(0<=contraction<1):
        raise ValueError("thermal Banach contraction failed")
    if zeta<=0:
        raise ValueError("old thermal predecessor influence not positive")
    inner=((Tlo-beta[0])/zeta,
           (Thi-beta[0]-alpha[0]*Hmax)/zeta)
    outside=((Tlo-beta[0]-alpha[0]*Hmax)/zeta,
             (Thi-beta[0])/zeta)
    if not(inner[0]<inner[1] and outside[0]<inner[0]
           and inner[1]<outside[1]):
        raise ArithmeticError("source heat predecessor bounds not nested")
    return {
        "status":"SIX_ROW_SOURCE_ENVELOPE_CERTIFIED_CONDITIONAL",
        "source_sha_pins_declaration_only":True,
        "source_raw_bytes_authenticated_in_ci":False,
        "source_adapter_kappa":kappa,
        "thermal_beta_C":beta,"thermal_alpha_C_per_W":alpha,
        "old_T0_transfer":zeta,
        "banach_contraction":contraction,
        "heat_lipschitz_bound_W_per_C":Lipschitz_H,
        "root_thermal_interval_C":root_image,
        "diode_root_vj_interval_V":(F(-3),F(-2)),
        "old_T0_delta_inner_interval_C":inner,
        "old_T0_delta_outer_exclusion_C":outside,
        "all_fifty_rows_certified":False,
        "all_root_history_covered":False,
        "claim_ceiling":("Existence/uniqueness of 6 ORIGINAL SOURCE EQUATIONS "
            "on the fixed Pro18E ON Q2 predecessor and node-voltage chart, "
            "given separately source-proved H,B and derivative enclosures. "
            "Not 50D root, all-stage root covering, joint CAL E or Goal27."),
    }
