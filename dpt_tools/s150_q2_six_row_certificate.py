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
    diode_current_temperature_derivative_bound_A_per_C="6.58e-17",
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
    dibT=_fraction(diode_current_temperature_derivative_bound_A_per_C)
    if dibT<0:
        raise ValueError("diode current thermal derivative majorant must be nonnegative")
    Lipschitz_H=dspan*(kappa*dch+dibT)
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


def exact_machin_pi_interval():
    """Exact 32-term Machin alternating rational pi enclosure."""
    def atan_band(u, count=32):
        u=F(u)
        subtotal=sum(((-1)**k)*u**(2*k+1)/F(2*k+1)
                     for k in range(count))
        return subtotal,subtotal+u**(2*count+1)/F(2*count+1)
    a=atan_band(F(1,5))
    b=atan_band(F(1,239))
    lo,hi=16*a[0]-4*b[1],16*a[1]-4*b[0]
    if not(F("3.14159265358979")<lo<hi<F("3.14159265358980")):
        raise ArithmeticError("exact pi interval construction failed")
    return lo,hi


def original_rc_band_filter_fraction(
    time_s, raw_source_current_A, bandwidth_lo_MHz, bandwidth_hi_MHz,
    *, selected_stages=(), integer_scale=10**12, expected_sample_count=None
):
    """Directed original first-order PL RC source-current filter *point* outer.

    f_new = exp(-x)*f_old
            +((1-exp(-x))/x-exp(-x))*i_old
            +(1-(1-exp(-x))/x)*i_new,
    x=2*pi*bandwidth*dt. Raw current is the SOURCE CAL coil36 history.
    Each original stage is outward integer-rounded at the declared scale.
    This is SOURCE CANDIDATE/RC-MEMORY arithmetic, not any 50D source-root
    complement, sensor-noise contract, or future target certificate.
    """
    from math import factorial
    ts=tuple(map(_fraction,time_s))
    current=tuple(map(_fraction,raw_source_current_A))
    low,high=map(_fraction,(bandwidth_lo_MHz,bandwidth_hi_MHz))
    n=len(ts)
    if (n<2 or n!=len(current) or low<=0 or high<low or
            integer_scale<1 or not isinstance(integer_scale,int) or
            (expected_sample_count is not None and n!=expected_sample_count)
            or any(ts[j]>=ts[j+1] for j in range(n-1))):
        raise ValueError("invalid original RC source/time/frequency chart")
    need=tuple(selected_stages)
    if any(not isinstance(j,int) or j<0 or j>=n for j in need):
        raise ValueError("sample outside source PREP/CAL grid")
    piL,piU=exact_machin_pi_interval()
    S=integer_scale
    def to_int_interval(v):
        lower=v*S
        return ((lower.numerator//lower.denominator),
                -((-lower).numerator//(-lower).denominator))
    def mul(c,v):
        a=(c[0]*v[0],c[0]*v[1],c[1]*v[0],c[1]*v[1])
        return (min(a)//S,-(-max(a)//S))
    def exp_alt(x,n_terms):
        return sum(((-1)**k)*x**k/F(factorial(k))
                   for k in range(n_terms+1))
    def coefficients(dt):
        xl=2*piL*low*10**6*dt
        xu=2*piU*high*10**6*dt
        if not(0<xl<=xu<F("0.05")):
            raise ValueError("RC exponential enclosure requires x<.05")
        aL,aU=exp_alt(xu,17),exp_alt(xl,16)
        qL,qU=(1-aU)/xu,(1-aL)/xl
        return tuple(to_int_interval(lo),to_int_interval(hi)) if False else (
            to_int_interval(aL),to_int_interval(aU))
    # Each SOURCE step has three independently outward-enclosed affine
    # coefficients; precompute once for each distinct exact stored dt.
    ccache={}
    def coeff3(dt):
        if dt in ccache:
            return ccache[dt]
        xl=2*piL*low*10**6*dt
        xu=2*piU*high*10**6*dt
        if not(0<xl<=xu<F("0.05")):
            raise ValueError("RC exponential enclosure requires x<.05")
        aL,aU=exp_alt(xu,17),exp_alt(xl,16)
        qL,qU=(1-aU)/xu,(1-aL)/xl
        def coeff_interval(lo,hi):
            p=to_int_interval(lo)[0]
            q=to_int_interval(hi)[1]
            return p,q
        result=(coeff_interval(aL,aU),
                coeff_interval(qL-aU,qU-aL),
                coeff_interval(1-qU,1-qL))
        ccache[dt]=result
        return result
    samples={}
    f=to_int_interval(current[0])
    if 0 in need:
        samples[0]=(F(f[0],S),F(f[1],S))
    raw_intervals=tuple(map(to_int_interval,current))
    for j in range(n-1):
        a,b,c=coeff3(ts[j+1]-ts[j])
        terms=(mul(a,f),mul(b,raw_intervals[j]),
               mul(c,raw_intervals[j+1]))
        f=(sum(x[0] for x in terms),sum(x[1] for x in terms))
        if j+1 in need:
            samples[j+1]=(F(f[0],S),F(f[1],S))
    return {
        "status":"RC_FILTER_INTERVAL_OUTER_NOT_ROOT_COVER",
        "sample_bounds_A":samples,
        "source_raw_bytes_authenticated":False,
        "all_source_roots_covered":False,
        "steps_covered":n-1,
        "distinct_exact_time_steps":len(ccache),
        "fractional_pi_interval":(piL,piU),
        "claim_ceiling":"Exact rational/source-candidate PL filter outer for one saved raw-current trace, bounded bandwidth and one initial filter state. Not all 50D source roots, joint CAL sensor E, guard/reset reachability or Goal27.",
    }


# Signed dimensionless seven-reading functional from ORIGINAL S150 H4801;
# independently zero-sum in the two ports removes two arbitrary shared offsets.
SEVEN_V_W=(F(-3159911,2000000),F(71229,625000),F(14659891,10000000))
SEVEN_I_W=(F(-221897,2000000),F(-1589547,5000000),
           F(35459,5000000),F(4217661,10000000))
SEVEN_V_H=(3800,2614,4147)
SEVEN_I_H=(1853,4041,2907,3660)


def certify_original_seven_reading_joint_outer(
    *, observed_dual, source_voltage_dual, source_current_band_outers,
    epsilon_V="0.30558", epsilon_I="0.0401",
    phase_V="0.02", phase_I="0.05",
    clock_V_bound, clock_I_bound, initial_filter_I="0.1",
    gain_V=("0.9","1.1"), gain_I=("0.9","1.1"),
    clock_V_weighted_support=None,
    root_radii=(0,0,0),
):
    """Exact necessary exclusion for a declared SOURCE-CENTER band outer.

    Every row in source_current_band_outers must independently contain the
    SAME source candidate's weighted RC port-current output for *every*
    bandwidth in its frequency band. These bounds are hypotheses, not proved
    by passing them as arguments. In particular this API does NOT certify
    their original-source provenance or a 50D root cell. The associated
    SHA-checking original NPZ replay validates that input obligation.
    Both gain parameters are SHARED across all reads in their respective
    channel; offsets cancel by exact zero-sum weights. Arbitrary per-read
    phase/clock residuals and 0.1A initial filter discrepancy are enlarged
    independently for a sound, deliberately conservative outer.
    Normalization: divide V observations by 1V and I by 1A first.
    """
    if sum(SEVEN_V_W) or sum(SEVEN_I_W):
        raise ArithmeticError("seven-read offset annihilator is not exact")
    if len(source_current_band_outers)!=80:
        raise ValueError("expected exactly 80 source-current bands")
    o=_fraction(observed_dual)
    v=tuple(map(_fraction,source_voltage_dual))
    if len(v)!=2 or v[0]>v[1]:
        raise ValueError("invalid source-voltage outer")
    rv=tuple(map(_fraction,root_radii))
    if len(rv)!=3 or any(x<0 for x in rv):
        raise ValueError("invalid source-root tube radii")
    gv=tuple(map(_fraction,gain_V));gi=tuple(map(_fraction,gain_I))
    if len(gv)!=2 or len(gi)!=2 or not (0<gv[0]<=gv[1] and 0<gi[0]<=gi[1]):
        raise ValueError("shared gains must be positive closed intervals")
    errors=tuple(map(_fraction,(epsilon_V,epsilon_I,phase_V,phase_I,
                                clock_V_bound,clock_I_bound,initial_filter_I)))
    if any(x<0 for x in errors):
        raise ValueError("sensor and clock errors must be nonnegative")
    lv=sum(map(abs,SEVEN_V_W));li=sum(map(abs,SEVEN_I_W))
    eV,eI,pV,pI,cV,cI,initI=errors
    # Offset contributions vanish exactly. Other error sources may be
    # correlated: the sum of their absolute supports remains a valid outer.
    # phase_V/phase_I are SENSOR-OUTPUT per-reading waveform bounds,
    # AFTER gain; independent sine/cos coefficient boxes must first be
    # converted into actual waveform sup-bounds (usually sqrt(2) larger).
    cvsupport=(lv*cV if clock_V_weighted_support is None
               else _fraction(clock_V_weighted_support))
    if cvsupport<0:
        raise ValueError("negative source clock support")
    total_err=lv*(eV+pV+gv[1]*(rv[0]+rv[1])) + gv[1]*cvsupport
    total_err+=li*(eI+pI+gi[1]*(cI+initI+rv[2]))

    def mult_interval(x,g):
        corners=(x[0]*g[0],x[0]*g[1],x[1]*g[0],x[1]*g[1])
        return min(corners),max(corners)

    pv=mult_interval(v,gv)
    prev=F(90)
    margins=[]
    normalized=[]
    for item in source_current_band_outers:
        if len(item)!=4:
            raise ValueError("source-current band entry needs lo,hi,lower,upper")
        blo,bhi,cl,cu=map(_fraction,item)
        if blo!=prev or not (blo<bhi<=110) or cl>cu:
            raise ValueError("source bandwidth gap/overlap or invalid band outer")
        prev=bhi
        pi=mult_interval((cl,cu),gi)
        pred=(pv[0]+pi[0]-total_err,pv[1]+pi[1]+total_err)
        normalized.append(pred)
        margins.append(max(F(0),o-pred[1],pred[0]-o))
    if prev!=110:
        raise ValueError("source bandwidth gap: last band misses 110 MHz")
    minimum=min(margins)
    return dict(
        status=("STORED_POINT_CONDITIONAL_NECESSARY_EXCLUSION"
                if minimum>0 else "CANNOT_EXCLUDE"),
        strict_margin=minimum,
        zero_offset_annihilator=True,
        weights_sum=(sum(SEVEN_V_W),sum(SEVEN_I_W)),
        dual_port_l1=(lv,li),
        total_nuisance_support=total_err,
        predicted_outer_per_band=tuple(normalized),
        source_band_count=80,
        source_band_bounds_authenticated=False,
        full50_root_cover_certified=False,
        joint_full_CAL_E_certified=False,
        future_H841_goal_certified=False,
        claim_ceiling=("Conditional ORIGINAL-SOURCE stored-point/verified band "
                       "outer rejection only. No complete 50D source-root "
                       "complement, physical joint E or Goal27 certificate."),
    )


def replay_original_s150_seven_reading_80band(
    observed_e_npz, candidate_a_npz, original_law_zip,
    *, root_radii=(0,0,0),
):
    """Read-only SHA-qualified original E/A first-PREP seven-reading replay.

    No original bytes are copied to a repository, printed or uploaded. Missing
    original files/hash mismatch fail closed. This is a source STORED-CANDIDATE
    necessary exclusion, not an exhaustive source-root or joint-CAL certificate.
    The 80 exact RC midpoint enclosures and a uniform b-Lipschitz source
    derivative cover the WHOLE 90..110 MHz frequency continuum.
    """
    import hashlib
    import zipfile
    from pathlib import Path
    try:
        import numpy as np
    except ImportError as ex:
        raise RuntimeError("NumPy is required for local source NPZ replay") from ex
    expect_e="baafdd8cb489adb186677658c4a8031130cc53a9a1854c4997211d437daf8b3e"
    expect_a="98f83174aef3345d81e0c500789ae59c16330874c045cfd85639d6da685c61e1"
    expect_zip="250aa4ea17514ffdeda3a51d95bedf8e034b181f97bdc254db29ddc36281b9c8"
    def hashed_path(path, expected):
        if path is None:
            raise ValueError("SOURCE_INPUTS_UNAVAILABLE")
        p=Path(path)
        if not p.is_file():
            raise FileNotFoundError("SOURCE_INPUTS_UNAVAILABLE: "+str(p))
        digest=hashlib.sha256(p.read_bytes()).hexdigest()
        if digest!=expected:
            raise ValueError("SOURCE_INPUT_SHA_MISMATCH: "+str(p))
        return p
    ep=hashed_path(observed_e_npz,expect_e)
    ap=hashed_path(candidate_a_npz,expect_a)
    zp=hashed_path(original_law_zip,expect_zip)
    with zipfile.ZipFile(zp) as z:
        members=[name for name in z.namelist() if name.endswith("actual_law.py")]
        if not members or not any(
                hashlib.sha256(z.read(name)).hexdigest()==LAW_SHA
                for name in members):
            raise ValueError("SOURCE_LAW_MEMBER_SHA_MISMATCH")
    with np.load(ep,allow_pickle=False) as e, np.load(ap,allow_pickle=False) as a:
        times_e=e["time_s"];times_a=a["t_s"]
        state_e=e["state50"];state_a=a["state50"]
        cmd_e=e["command_V"];cmd_a=a["command_V"]
        cal=e["measurement_V_A"];H_e=e["H_s"];H_a=a["H_s"]
        if (times_e.shape!=(4927,) or times_a.shape!=(4927,) or
                state_e.shape!=(4927,50) or state_a.shape!=(4927,50) or
                cal.shape!=(4801,2) or H_a.shape!=(4801,) or
                H_e.shape!=(4801,) or cmd_e.shape!=(4927,) or
                cmd_a.shape!=(4927,) or
                not np.array_equal(times_e,times_a) or
                not np.array_equal(H_e,H_a) or
                not np.array_equal(H_a,times_a[126:]) or
                not np.array_equal(cmd_e,cmd_a) or
                not np.array_equal(state_e[0],state_a[0])):
            raise ValueError("SOURCE_PREP_COMMAND_OR_GRID_IDENTITY_MISMATCH")
        ts=tuple(F(float(x)) for x in times_a)
        current=tuple(F(float(x)) for x in state_a[:,36])
        voltage=tuple(F(float(u))-F(float(v)) for u,v in zip(state_a[:,0],state_a[:,1]))
        ys=sum(w*F(float(cal[i,0])) for w,i in zip(SEVEN_V_W,SEVEN_V_H))
        ys+=sum(w*F(float(cal[i,1])) for w,i in zip(SEVEN_I_W,SEVEN_I_H))
    if any(ts[i]>=ts[i+1] for i in range(4926)):
        raise ValueError("SOURCE_TIME_NOT_INCREASING")
    # Bound derivative of exact piecewise-linear source port currents.
    current_slope=max(abs((current[i+1]-current[i])/(ts[i+1]-ts[i]))
                      for i in range(4926))
    if current_slope>=F(3*10**9):
        raise ValueError("SOURCE_CURRENT_LIPSCHITZ_NOT_QUALIFIED")
    raw_V_lipschitz=max(
        abs((voltage[k+s]-voltage[k+s-1])/(ts[k+s]-ts[k+s-1]))
        for h in SEVEN_V_H for k in (h+126,) for s in (0,1))
    if raw_V_lipschitz>=F(7*10**9):
        raise ValueError("SOURCE_CLOCK_VOLTAGE_SLOPE_NOT_QUALIFIED")
    source_V=sum(w*voltage[h+126] for w,h in zip(SEVEN_V_W,SEVEN_V_H))
    stage_indices=tuple(h+126 for h in SEVEN_I_H)
    piL,_=exact_machin_pi_interval()
    l1I=sum(map(abs,SEVEN_I_W))
    bands=[]
    for k in range(80):
        blo=F(90)+F(k,4);bhi=blo+F(1,4)
        mid=(blo+bhi)/2
        center=original_rc_band_filter_fraction(
            ts,current,mid,mid,selected_stages=stage_indices,
            expected_sample_count=4927,integer_scale=10**12)
        fc=center["sample_bounds_A"]
        i_lo=i_hi=F(0)
        for w,j in zip(SEVEN_I_W,stage_indices):
            lo,hi=fc[j]
            if w<0:
                lo,hi=hi,lo
            i_lo+=w*lo
            i_hi+=w*hi
        # Filter derivative wrt bandwidth b, with SAME b for all samples:
        # f_b=I-int_0^t exp(-2*pi*b*(t-s))*I'(s)ds (when f0=I0).
        # Drift from a center midpoint to any b in this band, valid for all
        # t and all signs of the piecewise-linear I' source.
        inv_diff=max(F(1)/(blo*10**6)-F(1)/(mid*10**6),
                     F(1)/(mid*10**6)-F(1)/(bhi*10**6))
        delta=F(3*10**9)*inv_diff/(2*piL)
        bands.append((blo,bhi,i_lo-l1I*delta,i_hi+l1I*delta))
    weighted_V_clock_slope=sum(
        abs(w)*max(
            abs((voltage[j]-voltage[j-1])/(ts[j]-ts[j-1])),
            abs((voltage[j+1]-voltage[j])/(ts[j+1]-ts[j])))
        for w,h in zip(SEVEN_V_W,SEVEN_V_H) for j in (h+126,)
    )
    result=certify_original_seven_reading_joint_outer(
        observed_dual=ys,
        source_voltage_dual=(source_V,source_V),
        source_current_band_outers=bands,
        root_radii=root_radii,
        clock_V_bound=F(7*10**9)*F("150e-15"),
        clock_V_weighted_support=weighted_V_clock_slope*F("150e-15"),
        clock_I_bound=F(3*10**9)*F("150e-15"),
    )
    result["source_band_bounds_authenticated"]=True
    result["source_input_sha256"]=(expect_e,expect_a,expect_zip,LAW_SHA)
    result["source_stages"]=4926
    result["max_current_slope_A_per_s"]=current_slope
    result["max_selected_voltage_slope_V_per_s"]=raw_V_lipschitz
    result["observed_seven_reading_exact_dual"]=ys
    result["source_v_seven_reading_exact_dual"]=source_V
    result["source_exact_physical_sensor_error_qualified"]=False
    result["source_full50_history_roots_covered"]=False
    return result
