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


def certify_source_q2_kcl_heat_abs_switch(
    sensor_left_upper_A, sensor_right_lower_A,
    left_thermal_slope_upper_C_per_V,
    right_thermal_slope_lower_C_per_V,
    six_row_contraction_upper,
):
    """Fail-closed IVT and derivative-discontinuity gate for an ORIGINAL row.

    This is an IMPLICATION from separately SHA-proven original source bounds,
    not an algorithm that authenticates those interval inputs. On Pro18E
    stage3616, eliminate Q2 x from original KCL r20=0 and solve the Q2
    body/diode/four-thermal variables uniquely for each declared continuous
    delta in [-.0395,+.0395]V. A continuous sense S(delta) changing strictly
    from negative to positive forces one S=0; H=|ds*S|+(g-g2)^2/9 then has a
    cusp if the one-sided T0(delta) derivatives enclose strictly opposite
    signs. A single smooth C1 Jacobian contractor across this RAW source
    seven-row chart is inadmissible. The remaining 43 coupled original
    source rows have not been solved or excluded; other physical history
    and all-root claims are forbidden.
    """
    left,right,tl,tr,q=map(_fraction,(
        sensor_left_upper_A,sensor_right_lower_A,
        left_thermal_slope_upper_C_per_V,
        right_thermal_slope_lower_C_per_V,
        six_row_contraction_upper,
    ))
    if not(0<=q<1):
        raise ValueError("source six-row thermal contraction not established")
    crossed=(left<0<right and tl<0<tr)
    return {
        "status":("SOURCE_SEVEN_ROW_HEAT_ABS_CUSP_MUST_SPLIT"
                  if crossed else "RETAIN_UNDECIDED"),
        "opposite_slope_jump_lower_C_per_V":(tr-tl if crossed else F(0)),
        "source_interval_inputs_independently_authenticated":False,
        "root_50d_certified":False,
        "full50_history_cover_certified":False,
        "claim_ceiling":("Only ORIGINAL 7-row KCL-eliminated Q2 "
            "conditional chart with separately source-qualified signs and "
            "one-sided derivatives. Preserve BOTH ABS branches in any "
            "full50 interval-Newton/SIVIA lift; no Goal27 claim."),
    }


def source_be_coil_elimination(node_voltage26, old_coil12,
                               incidence_26x12, inductance_H12, h_s):
    """Exact 12-row original source BE coil elimination for given 26 nodes.

    For original source r[26:38]=-B.T@v + source_drive e11 and
    (L/h)*(i_new-i_old), source_drive[11]=+150V, solve:
        i_new = i_old + (h/L)*(B.T@v-150*e11).
    Incidence and inductances must come from independently authenticated
    original source; this function only verifies arithmetic given them.
    """
    v=tuple(map(_fraction,node_voltage26))
    old=tuple(map(_fraction,old_coil12))
    inductance=tuple(map(_fraction,inductance_H12))
    matrix=tuple(tuple(map(_fraction,row)) for row in incidence_26x12)
    h=_fraction(h_s)
    if len(v)!=26 or len(old)!=12 or len(inductance)!=12 or len(matrix)!=26 or any(
        len(row)!=12 for row in matrix
    ) or h<=0 or any(x<=0 for x in inductance):
        raise ValueError("invalid original source coil BE contract")
    drive=[F(0)]*12
    drive[11]=F(150)
    return tuple(old[j]+h/inductance[j]*(
        sum(matrix[k][j]*v[k] for k in range(26))-drive[j])
        for j in range(12))


def certify_source_stage3616_26d_reduction(
    original_old_temperature8_C, h_s, *,
    old_junction_V,
    q1_gs_V,q2_gs_V,q1_d_s_V,q2_d_s_V,
    q1_five_node_V,q2_five_node_V,
    adapter_kappa,source_law_sha256,source_adapter_sha256,
    saved_cal_sha256,
):
    """Conditional exact original source n3616 50D->26D node-KCL root reduction.

    SHA-authenticated read-only source analysis must separately prove that
    original Q1 five node voltages indices3,5,6,8,9 and Q2 indices
    15,17,18,20,21 lie within +/-0.04V of saved stage3616 source center,
    and source diode/ETH/G2/heat envelopes are valid on the declared
    NATIVE-ARITHMETIC CHART: exact stored BE h and old raw thermal in
    [-60,260] C, old vj in (-1590,0]. States outside this chart remain
    UNRESOLVED, not excluded. The ideal real-law all-raw-T lemma is a
    different claim from IEEE execution of the source polynomial.
    Across these ten-node charts Q1 is ETH LOW / G2 OFF and Q2 ETH HIGH
    / G2 ON independent of temperature. Global source body monotonicity,
    exact thermal 4x4 positive inverse and global H derivative Lipschitz
    yield one six-row diode+body+thermal root per leg for each fixed node
    tuple, across heat ABS sign changes. Exact source coil BE inversion
    determines the other twelve currents. Therefore the complete 50D
    single-stage root set IN THIS TEN-NODE CHART corresponds bijectively
    to zeros of remaining 26 nodal KCL equations, provided the supplied
    original bounds and qualified source law are independently certified.
    Source 26D KCL root existence, chart complement, PREP/CAL histories,
    reset, joint observations and H841 Goal27 remain unproved.
    """
    if (source_law_sha256!=LAW_SHA or source_adapter_sha256!=ADAPTER_SHA
            or saved_cal_sha256!=SAVED_SHA):
        raise ValueError("unqualified original source SHA identity")
    if _fraction(adapter_kappa)!=F("1.007"):
        raise ValueError("source adapter kappa unqualified")
    old=tuple(map(_fraction,original_old_temperature8_C))
    jold=tuple(map(_fraction,old_junction_V))
    h=_fraction(h_s)
    if len(old)!=8 or len(jold)!=2 or not all(
            F(-1590)<x<=0 for x in jold):
        raise ValueError("original old junction outside D1 no-breakdown domain")
    if h<=0:
        raise ValueError("source BE dt must be positive")
    # The heat Lipschitz/Banach numbers below are source-qualified for one
    # archived binary64 BE stage, NOT an arbitrary user-supplied h. A longer
    # step changes the inverse thermal map and may destroy contraction.
    source_h=F.from_float(float.fromhex("0x1.b7cdfd9d80000p-37"))
    if h!=source_h:
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: original stage3616 binary64 dt required")
    # This is a scoped NATIVE IEEE arithmetic-safe predecessor chart. ETH
    # intentionally contains UNCLIPPED raw tj polynomial terms. At very
    # large finite raw tj NumPy intermediate multiplications may overflow
    # to NaN despite tjc/ETH output clips; never call such boxes certified.
    # A failure here retains the complement as unresolved; it does not
    # prove that a raw-temperature root outside the chart is impossible.
    if any(not(F(-60)<=t<=F(260)) for t in old):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: old raw temperature outside native arithmetic chart [-60,260] C")
    # The source heat envelope bounds both (d-x) and (g-g2).
    # Merely bounding gs/ds would let arbitrary x voltages through,
    # falsely elevating the global 12-root contractor. Source-center
    # binary64 coordinates are explicitly frozen and ALL ten independent
    # node degrees are checked before any Banach implication is allowed.
    q1center=tuple(F.from_float(float.fromhex(x)) for x in (
        "0x1.2bf0be2eea417p+7","0x1.6d9cb673abfabp+3",
        "0x1.9609c4242a8a7p+3","0x1.2bf0dc944b121p+7",
        "0x1.da4c3edc813bep+3"))
    q2center=tuple(F.from_float(float.fromhex(x)) for x in (
        "0x1.67138b6a8325dp+3","0x1.1bd6737f6c78cp+4",
        "0x1.c441ed8de0342p+3","0x1.67139f1fe1791p+3",
        "0x1.fc4c4bfd24625p+2"))
    q1node=tuple(map(_fraction,q1_five_node_V))
    q2node=tuple(map(_fraction,q2_five_node_V))
    if (len(q1node)!=5 or len(q2node)!=5 or
            any(abs(x-c)>F(".04") for nodes,center in (
                (q1node,q1center),(q2node,q2center))
                for x,c in zip(nodes,center))):
        raise ValueError("original source ten-node chart leave +/-0.04V")
    gs1=tuple(map(_fraction,q1_gs_V))
    gs2=tuple(map(_fraction,q2_gs_V))
    ds1=tuple(map(_fraction,q1_d_s_V))
    ds2=tuple(map(_fraction,q2_d_s_V))
    if any(len(x)!=2 or x[0]>x[1] for x in (gs1,gs2,ds1,ds2)):
        raise ValueError("source physical-node voltage chart malformed")
    if not(gs1[0]>=F("-2.2132") and gs1[1]<=F("-2.0531")
           and gs2[0]>=F("6.1108") and gs2[1]<=F("6.271")
           and ds1[0]>=F(135) and ds1[1]<=F("135.3")
           and ds2[0]>=F("3.19") and ds2[1]<=F("3.36")
           and gs1[1]<F("2.1679956")
           and gs2[0]>F("3.1343316")):
        raise ValueError("node box leaves source stage3616 ON/OFF guard chart")
    beta1,alpha1,_=source_thermal_affine_exact(old[:4],h)
    beta2,alpha2,_=source_thermal_affine_exact(old[4:],h)
    # Original source-wide heat and derivative envelopes are separate
    # SHA-qualified mathematical prerequisites, NOT extracted by this CI.
    H1,H2=F(110000),F(33000)
    q1=F("1.4230884541564563e-16")
    q2=F(".000368894405170418")
    if not all(a>=0 for a in (*alpha1,*alpha2)):
        raise ValueError("thermal M-matrix inverse is not positive")
    if not (q1<1 and q2<1):
        raise ValueError("global heat contraction not established")
    return dict(
        status="CONDITIONAL_50D_TO_26D_STAGE_ROOT_BIJECTION",
        original_stage=3616,
        declared_10_node_chart_radius_V=F(".04"),
        original_ten_nodes_checked_against_saved_center=True,
        q1_guard="ETH_LOW_G2_OFF",
        q2_guard="ETH_HIGH_G2_ON",
        old_junction_domain_qualified=True,
        archived_binary64_step_qualified=True,
        old_raw_temperature_native_chart_qualified=True,
        original_native_float_error_bound_qualified_in_ci=False,
        q1_banach_contraction_upper=q1,
        q2_banach_contraction_upper=q2,
        max_banach_contraction=max(q1,q2),
        q1_thermal_lower_C=beta1,
        q1_thermal_upper_C=tuple(a+b*H1 for a,b in zip(beta1,alpha1)),
        q2_thermal_lower_C=beta2,
        q2_thermal_upper_C=tuple(a+b*H2 for a,b in zip(beta2,alpha2)),
        eliminated_rows=24,
        reduced_node_KCL_rows=26,
        required_10_node_box_source_authenticated_in_ci=False,
        required_source_heat_derivative_enclosures_authenticated_in_ci=False,
        kcl26_roots_exist_certified=False,
        complementary_chart_roots_excluded=False,
        full50_allstage_root_cover_certified=False,
        all_cal_joint_E_certified=False,
        goal27_signed_work_certified=False,
        claim_ceiling=("Only ORIGINAL one-stage ten-node chart, qualified "
            "old-diode state and source-proved global diode/thermal/heat "
            "envelopes and the fixed source BE step / raw predecessor box imply exact 50D-to-26D node-KCL root bijection IN THIS CHART. "
            "No existence/complement certificate for 26 KCL roots, no "
            "history or physical Goal27 upper."),
    )


# S-L41: exact-source x-node KCL exclusion, two further 50D -> 24D eliminations.
# This is an ideal exact-real charge certificate. The original SciPy hyp2f1
# evaluation and all its binary64 errors are NOT outward-enclosed by this code.
_SOURCE_X_SPECS={
    "Q1":{
        "d":"0x1.2bf0be2eea417p+7","x":"0x1.2bf0dc944b121p+7",
        "s":"0x1.da4c3edc813bep+3",
        "old_d":"0x1.2c10e46fba814p+7","old_s":"0x1.d453559cc49d6p+3",
        "cap":("135","136","110","125"),"max_heat_W":F(110000),
    },
    "Q2":{
        "d":"0x1.67138b6a8325dp+3","x":"0x1.67139f1fe1791p+3",
        "s":"0x1.fc4c4bfd24625p+2",
        "old_d":"0x1.64640b421faa8p+3","old_s":"0x1.f6cdb13c29792p+2",
        "cap":("3.19","3.36","600","650"),"max_heat_W":F(33000),
    },
}
_STAGE3616_H=F.from_float(float.fromhex("0x1.b7cdfd9d80000p-37"))


def _source_x_box(v):
    pair=tuple(map(_fraction,v))
    if len(pair)!=2 or pair[0]>pair[1]:
        raise ValueError("invalid source closed voltage box")
    return pair


def _source_dq_sign_outer(delta, lo_cap, hi_cap):
    """Exact interval for integral C(v) dv when lo<=C<=hi."""
    return (lo_cap*delta,hi_cap*delta) if delta>=0 else (hi_cap*delta,lo_cap*delta)


def certify_original_source_x_kcl_outer(
        *, leg, d_V, s_V, x_V, h_s, source_law_sha256,
        source_adapter_sha256, saved_cal_sha256):
    """Stage3616 necessary root exclusion for x KCL under a closed node box.

    Original source row r8/r20 is exactly
      10000*(x-d) + 1e-7*(x-s) + (Q12(ds)-Q12(ds_old))/h.
    Q12' = 1108pF/[1+(v/4.5)^(63/100)] for 0.1<=v<=460.
    The original x node has NO other KCL terms. Its unique exact-real lift
    for fixed d,s is x=(10000*d+1e-7*s-dQ12/h)/(10000+1e-7).
    The two x rows can therefore be eliminated from the 26D KCL residual
    exactly, leaving 24 remaining KCL rows, *only* on the preimage of the
    original ten-node +/-0.04V chart and qualified predecessor.
    Source SHA strings identify, but do not replay, the private original.
    """
    if (source_law_sha256!=LAW_SHA or source_adapter_sha256!=ADAPTER_SHA
            or saved_cal_sha256!=SAVED_SHA):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: original source SHA mismatch")
    if _fraction(h_s)!=_STAGE3616_H:
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: archived binary64 h required")
    if leg not in _SOURCE_X_SPECS:
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: unqualified source leg")
    cfg=_SOURCE_X_SPECS[leg]
    d,s,x=map(_source_x_box,(d_V,s_V,x_V))
    radius=F("0.04")
    for box,name in ((d,"d"),(s,"s"),(x,"x")):
        center=F.from_float(float.fromhex(cfg[name]))
        if box[0]<center-radius or box[1]>center+radius:
            raise ValueError("UNRESOLVED_SOURCE_DOMAIN: ten-node chart exceeded")
    lower,upper,cl_pF,cu_pF=map(F,cfg["cap"])
    old_ds=(F.from_float(float.fromhex(cfg["old_d"]))-
            F.from_float(float.fromhex(cfg["old_s"])))
    ds=(d[0]-s[1],d[1]-s[0])
    if not(lower<=old_ds<=upper and lower<=ds[0]<=ds[1]<=upper):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: G12 branch not enclosed")
    # Exact integer-power comparison replaces float evaluation of z^0.63.
    # C12 decreases with v. These inequalities establish cl<=C12<=cu
    # for EVERY real voltage between lower and upper, including old ds.
    rat_lo=F(1108)/cu_pF-1
    rat_hi=F(1108)/cl_pF-1
    if not (lower>=F(".1") and upper<=F(460) and
            0<cl_pF<=cu_pF and rat_lo>0 and rat_hi>0 and
            (lower/F("4.5"))**63>=rat_lo**100 and
            (upper/F("4.5"))**63<=rat_hi**100):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: G12 cap enclosure unproved")
    cl,cu=cl_pF/F(10**12),cu_pF/F(10**12)
    qlo=_source_dq_sign_outer(ds[0]-old_ds,cl,cu)[0]
    qhi=_source_dq_sign_outer(ds[1]-old_ds,cl,cu)[1]
    a,b=F(10000),F(1,10**7)
    residual_lo=a*(x[0]-d[1])+b*(x[0]-s[1])+qlo/_STAGE3616_H
    residual_hi=a*(x[1]-d[0])+b*(x[1]-s[0])+qhi/_STAGE3616_H
    dx_tube=((b*ds[0]+qlo/_STAGE3616_H)/(a+b),
             (b*ds[1]+qhi/_STAGE3616_H)/(a+b))
    # NEW strict SOURCE joint contractor, not the Cartesian residual box.
    # On this exact-real original G12 chart, C12>0 and Cmax/h<a.
    # For x*(d,s)=[a*d+b*s-(Q12(d-s)-Q12(old))/h]/(a+b),
    # partial_d x*=(a-C12/h)/(a+b)>0,
    # partial_s x*=(b+C12/h)/(a+b)>0. The extrema on D x S
    # therefore use the TWO COMONOTONE corners (dlo,slo),(dhi,shi)
    # rather than the independent d/s/ds endpoints in residual_lo/hi.
    if not(cu/_STAGE3616_H<a):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: G12 joint corner derivative")
    dsl=d[0]-s[0]-old_ds
    dsh=d[1]-s[1]-old_ds
    q_upper_low_corner=_source_dq_sign_outer(dsl,cl,cu)[1]
    q_lower_high_corner=_source_dq_sign_outer(dsh,cl,cu)[0]
    x_necessary_lower=(a*d[0]+b*s[0]-
                       q_upper_low_corner/_STAGE3616_H)/(a+b)
    x_necessary_upper=(a*d[1]+b*s[1]-
                       q_lower_high_corner/_STAGE3616_H)/(a+b)
    if x_necessary_lower>x_necessary_upper:
        raise ArithmeticError("invalid source monotone x necessary enclosure")
    joint_residual_lower=(a+b)*(x[0]-x_necessary_upper)
    joint_residual_upper=(a+b)*(x[1]-x_necessary_lower)
    residual_lo=max(residual_lo,joint_residual_lower)
    residual_hi=min(residual_hi,joint_residual_upper)
    if residual_lo>residual_hi:
        raise ArithmeticError("inconsistent source residual outer contractors")
    excluded=residual_lo>0 or residual_hi<0
    return dict(
        status=("SOURCE_EXACT_REAL_X_KCL_BOX_EXCLUDED" if excluded else
                "RETAIN_SOURCE_X_CELL_UNRESOLVED"),
        exact_original_law_row=(8 if leg=="Q1" else 20),
        residual_lower_A=residual_lo,residual_upper_A=residual_hi,
        strict_abs_residual_margin_A=(residual_lo if residual_lo>0 else
                                      -residual_hi if residual_hi<0 else F(0)),
        necessary_d_minus_x_V=dx_tube,
        necessary_x_V=(x_necessary_lower,x_necessary_upper),
        joint_monotone_x_corner_qualified=True,
        joint_corner_strict_lower_residual_A=joint_residual_lower,
        joint_corner_strict_upper_residual_A=joint_residual_upper,
        capacitance_interval_rational_verified=True,
        source_exact_real_x_row_unique_lift=True,
        conditional_full50_to_24d_KCL_preimage=True,
        old_source_npz_bytes_authenticated_in_ci=False,
        native_float_error_certified=False,
        all50_stage_roots_certified=False,
        any_24d_KCL_zero_certified=False,
        all_cal_joint_E_certified=False,goal27_certified=False,
    )


def certify_source_thermal_predecessor_memory_gap(
        leg, *, h_s, source_law_sha256, source_adapter_sha256,
        saved_cal_sha256):
    """Sharp necessary OLD-temperature-memory lower bound, conditional.

    Compare two independently admissible six-row predecessors, with all
    four old thermal temperatures -60 or +260 deg C, at identical fixed
    present ten-node and old-junction inputs. If both six-row roots satisfy
    0<=H<=Hmax, their new T0 gap is at least
         [beta0(hot)-beta0(cold)] - alpha0*Hmax >0.
    No two full-26D-KCL roots or legal PREP histories are asserted.
    """
    if (source_law_sha256!=LAW_SHA or source_adapter_sha256!=ADAPTER_SHA
            or saved_cal_sha256!=SAVED_SHA or
            _fraction(h_s)!=_STAGE3616_H or leg not in _SOURCE_X_SPECS):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: original stage identity")
    hot,alpha,_=source_thermal_affine_exact((260,)*4,_STAGE3616_H)
    cold,alpha2,_=source_thermal_affine_exact((-60,)*4,_STAGE3616_H)
    if alpha!=alpha2 or any(a<0 for a in alpha):
        raise ArithmeticError("nonpositive exact source thermal M inverse")
    Hmax=_SOURCE_X_SPECS[leg]["max_heat_W"]
    gap=hot[0]-cold[0]-alpha[0]*Hmax
    if gap<=0:
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: no positive memory gap")
    return dict(
        status="CONDITIONAL_SIX_ROW_OLD_THERMAL_PREDECESSOR_SEPARATION",
        conditional_temperature_gap_lower_C=gap,
        conditional_minimax_radius_C=gap/2,
        original_binary64_h_verified=True,
        old_thermal_both_in_native_chart=True,
        heat_nonnegativity_and_upper_assumed=True,
        source_heat_global_majorants_authenticated_in_ci=False,
        same_full26d_KCL_legal_roots_verified=False,
        legal_prep_two_worlds_verified=False,
    )


def certify_guard_cell_bernstein_tail_exclusion(
        coefficient_lowers,coefficient_uppers,analytic_tail_abs_bound):
    """Conditional CLOSED-cell row exclusion after all guard/source bounds.

    An exact Bernstein basis is nonnegative and sums to one. Therefore a
    rigorous uniform remainder |R|<=rho and min lower coefficient>rho
    (or max upper<-rho) excludes a zero of this residual on the whole cell.
    All omitted/guard-switch branches remain UNRESOLVED, NEVER 'no root'.
    Inspired by OpenAI Math F090 finite-sign plus analytic-tail separation.
    """
    lo=tuple(map(_fraction,coefficient_lowers))
    hi=tuple(map(_fraction,coefficient_uppers))
    rho=_fraction(analytic_tail_abs_bound)
    if not lo or len(lo)!=len(hi) or rho<0 or any(
            l>u for l,u in zip(lo,hi)):
        raise ValueError("invalid Bernstein coefficient/remainder enclosure")
    gap=max(min(lo)-rho,-max(hi)-rho)
    return dict(
        status=("CONDITIONAL_BERNSTEIN_FULL_CELL_ROW_EXCLUSION" if gap>0
                else "RETAIN_GUARD_CELL_UNRESOLVED"),
        strict_signed_gap=max(gap,F(0)),
        uniform_analytic_tail_assumed=True,
        source_coefficient_bounds_authenticated_in_ci=False,
        complete_guard_closed_cover_certified=False,
        all50_root_cover_certified=False,
    )


def certify_schur_finite_tail_coupling(M,B,delta,eta):
    """F090-inspired exact Schur complement whole-tail sufficient criterion.

    For A=I-S partitioned into finite and tail, M bounds A_ff^-1,
    B bounds S_ft, delta bounds S_tf and eta bounds S_tt.  theta<1
    supplies a FULL block inverse, not just a finite-block inverse.
    Source/DPT matrix norm, branch and rounding hypotheses are external.
    """
    M,B,delta,eta=map(_fraction,(M,B,delta,eta))
    if M<=0 or any(v<0 for v in (B,delta,eta)):
        raise ValueError("invalid nonnegative Schur block norm bounds")
    theta=eta+delta*M*B
    if theta>=1:
        return dict(status="RETAIN_BLOCK_COUPLING_UNRESOLVED",theta=theta,
                    dpt_44row_coupling_authenticated_in_ci=False)
    inv=1/(1-theta)
    rf_to_xf=M*(1+B*delta*M*inv)
    rt_to_xf=M*B*inv
    rf_to_xt=delta*M*inv
    rt_to_xt=inv
    return dict(
        status="CONDITIONAL_WHOLE_BLOCK_INVERTIBLE",
        theta=theta,rf_to_xf_bound=rf_to_xf,rt_to_xf_bound=rt_to_xf,
        rf_to_xt_bound=rf_to_xt,rt_to_xt_bound=rt_to_xt,
        rf_to_full_bound=rf_to_xf+rf_to_xt,
        rt_to_full_bound=rt_to_xf+rt_to_xt,
        dpt_44row_coupling_authenticated_in_ci=False,
        complete_non_smooth_source_chart_certified=False,
    )


# S-L43: the original SOURCE passive package has fourteen exact linear
# voltages after the ten package coil BE currents are substituted. All
# identities below are for the SHA-declared real-decimal source expression;
# the protected ZIP/NPZ is NOT replayed by the public CI.
_SOURCE_PACKAGE_NODES=("D","sl")+tuple(
    tag+":"+name for tag in ("Q1","Q2")
    for name in ("da","d","gb","g2","g","w","x","s","sv","sb","k","sa"))
_SOURCE_PACKAGE_P=(2,4,5,10,11,12,13,14,16,17,22,23,24,25)
_SOURCE_PACKAGE_B=(0,1,3,6,7,8,9,15,18,19,20,21)


def certify_original_source_package14_linear_lift(
    *, boundary_node12_V, old_package_coil10_A, command_V,
    h_s, source_law_sha256, source_adapter_sha256, saved_cal_sha256
):
    """Original Pro18E n3616 14-node passive package, exact Fraction.

    Reconstruct Q1/Q2 (da,gb,g2,sv,sb,k,sa) after source 5+5
    package coil BE rows. Original nodal residual is Gv+B i-D ib
    -forcing+charge/h+G2; its 14 listed package rows contain ONLY G,
    package coils, and three source forcing stamps. No nonlinear D1,
    G2, ETH, thermal, G11, G12 or 1pF D D.T stamp touches these rows.
    Every internal package component reaches a retained boundary/ground
    through positive resistors and inductors, so exact A_PP is SPD.
    This algebraic lift is NOT existence of the remaining nodal root,
    diode/thermal/guard admissibility, CAL history or Goal27.
    """
    if (source_law_sha256!=LAW_SHA or source_adapter_sha256!=ADAPTER_SHA
            or saved_cal_sha256!=SAVED_SHA or
            _fraction(h_s)!=_STAGE3616_H or
            _fraction(command_V)!=F(15)):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: original n3616 inputs")
    if len(boundary_node12_V)!=12 or len(old_package_coil10_A)!=10:
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: 12 boundary/10 coil entries required")
    boundary=tuple(map(_fraction,boundary_node12_V))
    old=tuple(map(_fraction,old_package_coil10_A))
    locations={name:i for i,name in enumerate(_SOURCE_PACKAGE_NODES)}
    p=_SOURCE_PACKAGE_P
    b=_SOURCE_PACKAGE_B
    values={j:v for j,v in zip(b,boundary)}
    M=[[F(0)]*14 for _ in range(14)]
    rhs=[F(0)]*14

    def edge(a,c=None):
        e=[F(0)]*26
        e[locations[a]]+=1
        if c is not None:
            e[locations[c]]-=1
        return e

    def stamp(e,conductance,old_current=F(0)):
        g=_fraction(conductance)
        if g<=0:
            raise ValueError("UNRESOLVED_SOURCE_DOMAIN: nonpositive source branch")
        known=sum(e[i]*values[i] for i in b)
        for i,node in enumerate(p):
            v=e[node]
            if not v:
                continue
            rhs[i]-=g*v*known+v*old_current
            for j,col in enumerate(p):
                M[i][j]+=g*v*e[col]

    coils=[]
    for tag in ("Q1","Q2"):
        n=lambda a:tag+":"+a
        resistances=(
            (n("da"),"D" if tag=="Q2" else None,"87.416e-6"),
            (n("gb"),n("k"),"5.03785" if tag=="Q1" else "12.53785"),
            (n("g2"),n("g"),"9"),
            (n("w"),n("d"),"1"),
            (n("x"),n("d"),"1e-4"),
            (n("x"),n("s"),"1e7"),
            (n("g"),n("s"),"1e7"),
            (n("g"),n("d"),"1e7"),
            (n("g"),n("w"),"1e7"),
            (n("d"),n("s"),"1e7"),
            (n("d"),n("s"),"1e7"),
            (n("d"),n("s"),"4e8"),
            (n("sb"),n("k"),".02488"),
            (n("sa"),"sl" if tag=="Q2" else "D",".003322"),
        )
        for a,c,Rohm in resistances:
            stamp(edge(a,c),1/F(Rohm))
        package=(
            ("da","d","4.3659e-9","5"),
            ("gb","g2","11.364e-9","100"),
            ("sb","sv","7.574e-9","100"),
            ("sa","sv","3.435e-9","100"),
            ("sv","s",".2e-9","100"),
        )
        for a,c,L_H,R_parallel_ohm in package:
            e=edge(n(a),n(c))
            stamp(e,1/F(R_parallel_ohm))
            coils.append((e,F(L_H)))

    forcing=(
        (edge("Q1:da"),F(150)/F("87.416e-6")),
        (edge("Q1:gb","Q1:k"),-F(4)/F("5.03785")),
        (edge("Q2:gb","Q2:k"),F(15)/F("12.53785")),
    )
    for e,amp in forcing:
        for j,node in enumerate(p):
            rhs[j]+=e[node]*amp
    for j,(e,L) in enumerate(coils):
        stamp(e,_STAGE3616_H/L,old[j])
    if len(coils)!=10 or any(
        M[i][j]!=M[j][i] for i in range(14) for j in range(i+1,14)
    ):
        raise ArithmeticError("original passive package matrix symmetry failed")

    # Exact unpivoted LDL; every positive diagonal establishes SPD rather
    # than trusting a floating eigenvalue or 14 accidental solver pivots.
    L=[[F(0)]*14 for _ in range(14)]
    D=[F(0)]*14
    for i in range(14):
        L[i][i]=F(1)
        D[i]=M[i][i]-sum(L[i][k]*L[i][k]*D[k] for k in range(i))
        if D[i]<=0:
            raise ArithmeticError("original source package matrix not SPD")
        for j in range(i+1,14):
            L[j][i]=(M[j][i]-sum(L[j][k]*L[i][k]*D[k]
                                  for k in range(i)))/D[i]
    solution=_solve(M,rhs)
    if any(sum(M[i][j]*solution[j] for j in range(14))!=rhs[i]
           for i in range(14)):
        raise ArithmeticError("original source package linear residual nonzero")
    return dict(
        status="ORIGINAL_SOURCE_PACKAGE14_UNIQUE_EXACT_LINEAR_LIFT",
        package_node_indices=p,retained_node_indices=b,
        node_voltage14_V=solution,
        strict_positive_ldl_pivots_S=tuple(D),
        exact_package_matrix_S=tuple(tuple(row) for row in M),
        exact_package_rhs_A=tuple(rhs),
        eliminated_package_kcl_rows=14,
        conditional_from_50_to_10_stage_reduction=True,
        source_nonlinear_rows_absent_in_package=True,
        original_archive_bytes_authenticated_in_ci=False,
        native_ieee_outward_enclosed=False,
        reconstructed_x_g2_original_chart_qualified=False,
        complete_source_stage_root_certified=False,
        full_prepared_history_covered=False,
        goal27_certified=False,
    )


_SOURCE_G11_W_SPECS={
    "Q1":dict(
        g="0x1.9609c4242a8a7p+3",d="0x1.2bf0be2eea417p+7",
        old_g="0x1.9020fd0767b7cp+3",old_w="0x1.2c3935046b043p+7",
        q_lower=F(31132,5),q_upper=F(6395),
        cap_lower_pF=F(39,10),cap_upper_pF=F(4),
        max_abs_q_derivative=F(46)+F(27,4)*139),
    "Q2":dict(
        g="0x1.c441ed8de0342p+3",d="0x1.67138b6a8325dp+3",
        old_g="0x1.c17c22194a28bp+3",old_w="0x1.6e8cb5b6c794fp+3",
        q_lower=F(11,10),q_upper=F(449,400),
        cap_lower_pF=F(500),cap_upper_pF=F(555),
        max_abs_q_derivative=F(27,40)),
}


def certify_original_source_g11_w_guard(
    *, leg, g_V, d_V, h_s, source_law_sha256,
    source_adapter_sha256, saved_cal_sha256, w_V=None
):
    """Qualified full-GUARD exact-real source G11 Gauss32 w-KCL contractor.

    Original 32-point split Gauss source charge, restricted to the one
    smooth panel [u_old,u], is exactly (u-u_old) sum_j p_j Cgd(
    u_old+xi_j*(u-u_old)), with positive p_j summing to 1 and
    xi_j in (0,1). Thus it has the correct SIGN for u-u_old of
    either polarity (no |delta| error). The source cgd has
      Cgd(u)=555pF*(1+clip(-u,.1,600)
                  *(1+22.5*(1+tanh(-.3*u-6))))^(-113/200).
    For the source old u and full |u-u_old|<=1V:
    Q1 has -139<u<-136, tanh>=.99 and q in [31132/5,6395];
    Q2 u>1, clip=.1, tanh<=-.99, q in [1.1,449/400].
    These tanh signs follow from exp(12)>2^12>199 and their
    arguments >=6 / <=-6; no floating tanh is used. Rational
    200th/113th power comparisons enclose *every* Gauss node's
    physical capacitance. Log-derivative upper alpha<1/V makes
    each term C+delta*xi*C' positive for |delta|<=1V.
    Consequently H(u)=(1+1e-7)u+Q_G11(u)/h strictly increases.
    Every original g,d +/-0.04V chart input has exactly one
    G11-w KCL root strictly INSIDE this guarded branch. Root interval
    uses the exact effective Gauss-capacitance convex average k in
    [Cmin/h,Cmax/h], hence u=(g-d+k*u_old)/(1+1e-7+k).
    Source SciPy/NumPy outward error, remaining KCL and legal
    PREP/CAL histories are NOT authenticated by this theorem.
    """
    if (source_law_sha256!=LAW_SHA or source_adapter_sha256!=ADAPTER_SHA
            or saved_cal_sha256!=SAVED_SHA or
            _fraction(h_s)!=_STAGE3616_H or leg not in _SOURCE_G11_W_SPECS):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: source G11 law/step")
    cfg=_SOURCE_G11_W_SPECS[leg]
    g=_source_x_box(g_V)
    d=_source_x_box(d_V)
    rad=F(".04")
    for name,box in (("g",g),("d",d)):
        center=F.from_float(float.fromhex(cfg[name]))
        if box[0]<center-rad or box[1]>center+rad:
            raise ValueError("UNRESOLVED_SOURCE_DOMAIN: G11 g,d chart")
    old=(F.from_float(float.fromhex(cfg["old_g"]))-
         F.from_float(float.fromhex(cfg["old_w"])))
    guard=(old-1,old+1)
    if ((leg=="Q1" and not(F(-139)<=guard[0]<guard[1]<=F(-136)))
         or (leg=="Q2" and not(guard[0]>F(1)))):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: G11 panel/clip guard")
    clp,cup=cfg["cap_lower_pF"],cfg["cap_upper_pF"]
    qlo,qhi=cfg["q_lower"],cfg["q_upper"]
    if not(0<clp<=cup and
           (F(555)/clp)**200>=qhi**113 and
           (F(555)/cup)**200<=qlo**113):
        raise ArithmeticError("exact G11 capacitance 113/200 enclosure fails")
    rel_derivative=F(113,200)*cfg["max_abs_q_derivative"]/qlo
    if not(0<=rel_derivative<1):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: G11 derivative guard")
    cmin=clp/F(10**12)
    cmax=cup/F(10**12)
    kl,ku=cmin/_STAGE3616_H,cmax/_STAGE3616_H
    b=F(1,10**7)
    y=(g[0]-d[1],g[1]-d[0])
    root=tuple((v+k*old)/(1+b+k)
               for v in y for k in (kl,ku))
    roots=(min(root),max(root))
    # Signed Gauss charge at the guard faces is delta*C_bar with
    # C_bar in [cl,cu]; these two strict inequalities prove existence
    # for every y in the ENTIRE source g,d node chart.
    left_H_upper=(1+b)*(old-1)-kl
    right_H_lower=(1+b)*(old+1)+kl
    if not(left_H_upper<y[0] and right_H_lower>y[1]
            and guard[0]<roots[0]<=roots[1]<guard[1]):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: G11 guard faces")
    w_outer=(g[0]-roots[1],g[1]-roots[0])
    status="ORIGINAL_SOURCE_G11_GUARDED_W_UNIQUE_LIFT"
    lower=None
    upper=None
    margin=F(0)
    if w_V is not None:
        w=_source_x_box(w_V)
        u=(g[0]-w[1],g[1]-w[0])
        if not(guard[0]<=u[0]<=u[1]<=guard[1]):
            raise ValueError("UNRESOLVED_SOURCE_DOMAIN: w box beyond G11 guard")
        def signed_charge_bounds(t):
            diff=t-old
            return (cmin*diff,cmax*diff) if diff>=0 else (cmax*diff,cmin*diff)
        lower=y[0]-(1+b)*u[1]-signed_charge_bounds(u[1])[1]/_STAGE3616_H
        upper=y[1]-(1+b)*u[0]-signed_charge_bounds(u[0])[0]/_STAGE3616_H
        if lower>0 or upper<0:
            status="ORIGINAL_SOURCE_G11_W_KCL_CLOSED_BOX_EXCLUDED"
            margin=lower if lower>0 else -upper
        else:
            status="RETAIN_ORIGINAL_G11_W_CELL_UNRESOLVED"
    return dict(
        status=status,
        source_G11_KCL_row=(7 if leg=="Q1" else 19),
        full_guard_old_gd_V=old,
        qualified_source_gd_guard_V=guard,
        gauss32_signed_charge_single_panel_qualified=True,
        capacitance_interval_pF=(clp,cup),
        relative_capacitance_derivative_upper_per_V=rel_derivative,
        gauss_charge_derivative_lower_F_per_s=cmin*(1-rel_derivative)/_STAGE3616_H,
        effective_G11_schur_edge_conductance_lower_S=(
            (b+cmin*(1-rel_derivative)/_STAGE3616_H)/
            (1+b+cmin*(1-rel_derivative)/_STAGE3616_H)),
        necessary_g_minus_w_V=roots,
        necessary_w_V=w_outer,
        original_w_KCL_residual_lower_A=lower,
        original_w_KCL_residual_upper_A=upper,
        strict_abs_residual_margin_A=margin,
        forall_source_current_g_d_chart_w_root_exists=True,
        source_mathematical_guard_root_unique=True,
        conditional_further_ten_to_eight_reduction=True,
        full50_allroot_cover_certified=False,
        all50_stage_roots_certified=False,
        original_source_npz_bytes_authenticated_in_ci=False,
        native_ieee_gl32_outward_enclosed=False,
        full_prepared_history_covered=False,
        all_cal_joint_E_certified=False,
        goal27_certified=False,
    )


def certify_atomic_shared_nuisance_tail_cell(
    *,finite_bernstein_rows,shared_nuisance_matrix,
    nuisance_annihilator,residual_tail_coupling,
    tail_q_bernstein,tail_D,tail_terms,error_bounds,cell
):
    """Atomic/F090-inspired finite, source-agnostic closed-cell exclusion.

    Exact rational model on x in [0,1]:
       R_i(x,b,w)=f_i(x)+A_i.b+B_i*w+e_i,
       |e_i|<=eps_i, w=q(x)+D*w, |D|<1,
       b arbitrary but SHARED across all rows.
    f_i and q are Bernstein coefficient arrays of a COMMON degree.
    If lambda.T A ==0 EXACTLY, a nonzero lambda.T R root requires
       lambda.T(f+B*sum_{j=0}^N D^j q)
    to be within the certified tail and correlated-noise support.
    The remainder uses max|q_Bernstein_coeff| and geometric |D| bound,
    rather than using the source paper's numerical constants as DPT
    assumptions. Exact De Casteljau subdivision restricts the GLOBAL
    polynomial onto any closed subcell. No source 50D/guard/E certification.
    """
    n=len(finite_bernstein_rows)
    if (n<2 or len(shared_nuisance_matrix)!=n or
        len(nuisance_annihilator)!=n or
        len(residual_tail_coupling)!=n or len(error_bounds)!=n or
        not isinstance(tail_terms,int) or tail_terms<0 or len(cell)!=2):
        raise ValueError("invalid atomic certificate row or term count")
    fs=tuple(tuple(map(_fraction,row)) for row in finite_bernstein_rows)
    q=tuple(map(_fraction,tail_q_bernstein))
    deg=len(q)-1
    if deg<1 or any(len(row)!=len(q) for row in fs):
        raise ValueError("inconsistent finite and tail Bernstein degrees")
    A=tuple(tuple(map(_fraction,row)) for row in shared_nuisance_matrix)
    if not A[0] or any(len(row)!=len(A[0]) for row in A):
        raise ValueError("invalid shared nuisance shape")
    lam=tuple(map(_fraction,nuisance_annihilator))
    if not any(lam) or any(
        sum(lam[i]*A[i][j] for i in range(n))!=0
        for j in range(len(A[0]))
    ):
        raise ValueError("uneliminated shared nuisance invalidates certificate")
    B=tuple(map(_fraction,residual_tail_coupling))
    noise=tuple(map(_fraction,error_bounds))
    delta=_fraction(tail_D)
    a,b=tuple(map(_fraction,cell))
    if not(0<=a<b<=1 and abs(delta)<1 and all(v>=0 for v in noise)):
        raise ValueError("invalid tail contraction, cell or error caps")
    geo=sum((delta**j for j in range(tail_terms+1)),F(0))
    lb=sum((lam[i]*B[i] for i in range(n)),F(0))
    poly=tuple(
        sum((lam[i]*fs[i][k] for i in range(n)),F(0))+
        lb*geo*q[k] for k in range(deg+1))
    qmax=max(map(abs,q))
    tail=abs(lb)*abs(delta)**(tail_terms+1)*qmax/(1-abs(delta))
    epsilon=sum((abs(lam[i])*noise[i] for i in range(n)),F(0))
    error=tail+epsilon

    def split_bernstein(coeff,t):
        levels=[tuple(coeff)]
        while len(levels[-1])>1:
            prev=levels[-1]
            levels.append(tuple((1-t)*prev[i]+t*prev[i+1]
                                for i in range(len(prev)-1)))
        left=tuple(z[0] for z in levels)
        right=tuple(z[-1] for z in reversed(levels))
        return left,right

    local=poly
    if b<1:
        local,_=split_bernstein(local,b)
    if a>0:
        _,local=split_bernstein(local,a/b)
    pos=min(local)-error
    neg=-max(local)-error
    if pos>0:
        status="CONDITIONAL_BERNSTEIN_POSITIVE_CLOSED_CELL_EXCLUSION"
        margin=pos
    elif neg>0:
        status="CONDITIONAL_BERNSTEIN_NEGATIVE_CLOSED_CELL_EXCLUSION"
        margin=neg
    else:
        status="RETAIN_CLOSED_CELL_UNRESOLVED"
        margin=F(0)
    return dict(
        status=status,cell=(a,b),finite_terms=tail_terms,
        global_combined_bernstein_coefficients=poly,
        local_combined_bernstein_coefficients=local,
        analytic_tail_and_noise_error_bound=error,
        analytic_tail_bound=tail,shared_nuisance_noise_support=epsilon,
        strict_abs_row_dual_margin=margin,
        nuisance_annihilator_verified=True,
        whole_tail_bound_derived_from_q_bernstein=True,
        source_predecessor_and_cell_hypotheses_qualified_in_ci=False,
        original_atomic_analytic_theorem_verified_in_ci=False,
        source_full50_root_cover_certified=False,
        all_legal_hybrid_cells_covered=False,
        goal27_certified=False,
    )


# S-L45: original 12-coil passive source Schur stage (D, sl, package14).
# The last D-coil KVL contains +150 V; its BE-affine stamp is
# old_iD + h*(D-150)/100uH, NOT old_iD + h*D/100uH.
def certify_original_source_passive16_port_lift(
    *, retained_node10_V, old_coil12_A, command_V,
    h_s, source_law_sha256, source_adapter_sha256, saved_cal_sha256
):
    """Exact source-real 16-node lift, conditional on original stage domain.

    Original retained order: Q1(d,g,w,x,s),Q2(d,g,w,x,s).
    External source rows D,sl have no charge/G2/diode/thermal terms.
    The package14 and exact 2x2 Schur complement are SPD; the full
    eliminated original 50D equation requires S-L40 and all guards.
    """
    if (source_law_sha256!=LAW_SHA or source_adapter_sha256!=ADAPTER_SHA
            or saved_cal_sha256!=SAVED_SHA or
            _fraction(h_s)!=_STAGE3616_H or
            _fraction(command_V)!=F(15) or
            len(retained_node10_V)!=10 or len(old_coil12_A)!=12):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: original 16-node source identity")
    v=tuple(map(_fraction,retained_node10_V))
    old=tuple(map(_fraction,old_coil12_A))
    auth=dict(h_s=h_s,source_law_sha256=source_law_sha256,
              source_adapter_sha256=source_adapter_sha256,
              saved_cal_sha256=saved_cal_sha256,command_V=command_V)
    def residual_ports(D,sl):
        P=certify_original_source_package14_linear_lift(
            boundary_node12_V=(D,sl)+v,old_package_coil10_A=old[:10],
            **auth)
        pp=dict(zip(P["package_node_indices"],P["node_voltage14_V"]))
        rD=(D-pp[14])/F("87.416e-6")+(D-pp[13])/F(".003322")+old[11]+(
            _STAGE3616_H/F("100e-6"))*(D-F(150))
        rsl=(sl-pp[25])/F(".003322")+old[10]+(
            _STAGE3616_H/F("4.3e-9"))*sl
        return (rD,rsl),P
    zero,_=residual_ports(F(0),F(0))
    ex,_=residual_ports(F(1),F(0))
    ey,_=residual_ports(F(0),F(1))
    S=((ex[0]-zero[0],ey[0]-zero[0]),
       (ex[1]-zero[1],ey[1]-zero[1]))
    if S[0][1]!=S[1][0] or S[0][0]<=0 or (
        S[0][0]*S[1][1]-S[0][1]*S[1][0]<=0):
        raise ArithmeticError("original 16-node Schur not SPD")
    port=_solve(S,(-zero[0],-zero[1]))
    rr,P=residual_ports(*port)
    if rr!=(F(0),F(0)):
        raise ArithmeticError("original passive port residual not exactly zero")
    return dict(
        status="ORIGINAL_SOURCE_PASSIVE16_UNIQUE_EXACT_LINEAR_LIFT",
        eliminated_node_indices=(0,1)+_SOURCE_PACKAGE_P,
        retained_node_indices=(3,6,7,8,9,15,18,19,20,21),
        port_D_sl_V=port,
        package_voltage14_V=P["node_voltage14_V"],
        strict_package_ldl_pivots_S=P["strict_positive_ldl_pivots_S"],
        strict_schur_pivots_S=(S[0][0],
          S[1][1]-S[1][0]*S[0][1]/S[0][0]),
        original_two_port_residual_A=rr,
        old_external_sl_current_A=old[10],
        old_external_D_current_A=old[11],
        original_D_coil_150V_offset_A=F(150)*_STAGE3616_H/F("100e-6"),
        conditional_full50_to_eight_node_reduction=True,
        conditional_to_six_nonlinear_node_reduction_after_G11_G12=True,
        complete_original_six_node_roots_certified=False,
        original_full_predecessor_chart_qualified_in_ci=False,
        original_native_ieee_outward_enclosed=False,
        all_cal_joint_E_certified=False,
        goal27_certified=False
    )


# S-L46: source Q1 gate row after the exact passive16 and guarded G11 lift.
# All predecessor package+external coil currents enter ONE common affine image.
def certify_original_source_q1_gate_six_cell(
    *, six_current_node_boxes_V, old_coil12_boxes_A, h_s,
    source_law_sha256, source_adapter_sha256, saved_cal_sha256
):
    """Exact original n3616 Q1 gate-KCL necessary six-current-node exclusion.

    Current Q1(d,g,s),Q2(d,g,s) are source chart boxes; the twelve old
    coil currents are simultaneously bounded by ONE 12D predecessor box.
    Old Q1 g/s/w voltages are the frozen original binary64 n3615 anchors.
    The original G11 single-panel guarded root supplies w-d, the BE GS
    charge supplies 1388pF/h, and the 16x16 Schur lift supplies Q1:g2.
    Source G2/ETH/diode/thermal cannot cancel a nonzero r6: they do not
    stamp the Q1 gate row. A strict sign excludes the WHOLE declared
    source-exact real single-stage cell. No other stage or CAL claim.
    """
    if (source_law_sha256!=LAW_SHA or source_adapter_sha256!=ADAPTER_SHA
            or saved_cal_sha256!=SAVED_SHA or
            _fraction(h_s)!=_STAGE3616_H or
            len(six_current_node_boxes_V)!=6 or len(old_coil12_boxes_A)!=12):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: original Q1 gate six-cell")
    cur=tuple(map(_source_x_box,six_current_node_boxes_V))
    old=tuple(map(_source_x_box,old_coil12_boxes_A))
    centers=(
        _SOURCE_X_SPECS["Q1"]["d"],_SOURCE_G11_W_SPECS["Q1"]["g"],
        _SOURCE_X_SPECS["Q1"]["s"],_SOURCE_X_SPECS["Q2"]["d"],
        _SOURCE_G11_W_SPECS["Q2"]["g"],_SOURCE_X_SPECS["Q2"]["s"],
    )
    radius=F(".04")
    for box,hx in zip(cur,centers):
        center=F.from_float(float.fromhex(hx))
        if box[0]<center-radius or box[1]>center+radius:
            raise ValueError("UNRESOLVED_SOURCE_DOMAIN: original six-node chart")
    kw=dict(h_s=h_s,source_law_sha256=source_law_sha256,
            source_adapter_sha256=source_adapter_sha256,
            saved_cal_sha256=saved_cal_sha256,command_V=15)
    def q1_g2(v6,i12,dummy=None):
        # For this ORIGINAL resistor/coil topology, passive g2 has zero
        # coefficients on the four w/x ports, checked exactly below.
        boundary=[v6[0],v6[1],F(0),F(0),v6[2],
                  v6[3],v6[4],F(0),F(0),v6[5]]
        if dummy is not None:
            boundary[dummy]=F(1)
        lifted=certify_original_source_passive16_port_lift(
            retained_node10_V=boundary,old_coil12_A=i12,**kw)
        return lifted["package_voltage14_V"][_SOURCE_PACKAGE_P.index(5)]
    low6=tuple(box[0] for box in cur)
    lowold=tuple(box[0] for box in old)
    g20=q1_g2(low6,lowold)
    for dummy in (2,3,7,8):
        if q1_g2(low6,lowold,dummy)!=g20:
            raise ArithmeticError("omitted w/x was not passive-independent")
    g2lo=g2hi=g20
    for j,box in enumerate(cur):
        other=list(low6);other[j]=box[1]
        diff=q1_g2(other,lowold)-g20
        g2lo+=min(F(0),diff)
        g2hi+=max(F(0),diff)
    for j,box in enumerate(old):
        other=list(lowold);other[j]=box[1]
        diff=q1_g2(low6,other)-g20
        g2lo+=min(F(0),diff)
        g2hi+=max(F(0),diff)
    if g2lo>g2hi:
        raise ArithmeticError("invalid common-predecessor g2 image")
    auth=dict(h_s=h_s,source_law_sha256=source_law_sha256,
              source_adapter_sha256=source_adapter_sha256,
              saved_cal_sha256=saved_cal_sha256)
    q1w=certify_original_source_g11_w_guard(
        leg="Q1",g_V=cur[1],d_V=cur[0],**auth)
    q2w=certify_original_source_g11_w_guard(
        leg="Q2",g_V=cur[4],d_V=cur[3],**auth)
    if any(z["status"]!="ORIGINAL_SOURCE_G11_GUARDED_W_UNIQUE_LIFT"
           for z in (q1w,q2w)):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: original G11 guard")
    xrequired=[]
    for leg,dd,ss in (("Q1",cur[0],cur[2]),("Q2",cur[3],cur[5])):
        center=F.from_float(float.fromhex(_SOURCE_X_SPECS[leg]["x"]))
        source_x=certify_original_source_x_kcl_outer(
            leg=leg,d_V=dd,s_V=ss,
            x_V=(center-radius,center+radius),**auth)
        xrequired.append(source_x["necessary_x_V"])
    g,d,s=cur[1],cur[0],cur[2]
    old_g=F.from_float(float.fromhex(_SOURCE_G11_W_SPECS["Q1"]["old_g"]))
    old_w=F.from_float(float.fromhex(_SOURCE_G11_W_SPECS["Q1"]["old_w"]))
    old_s=F.from_float(float.fromhex(_SOURCE_X_SPECS["Q1"]["old_s"]))
    old_u=old_g-old_w
    bleed=F(1,10**7)
    # On this strict original source guard the signed finite GL32
    # effective Cbar is enclosed by [3.9,4.0]pF (ideal exact-real
    # quadrature). Native NumPy weights/rounding are NOT outward proved.
    kl=F("3.9e-12")/_STAGE3616_H
    ku=F("4.0e-12")/_STAGE3616_H
    def w_minus_d(gg,dd,k):
        return ((bleed+k)*(gg-dd)-k*old_u)/(1+bleed+k)
    corners=tuple(w_minus_d(gg,dd,k)
                  for gg in g for dd in d for k in (kl,ku))
    wdlo,wdhi=min(corners),max(corners)
    gs_charge_S=F("1388e-12")/_STAGE3616_H
    lower=((g[0]-g2hi)/9+bleed*(g[0]-s[1])+bleed*(g[0]-d[1])+
           wdlo+gs_charge_S*((g[0]-s[1])-(old_g-old_s)))
    upper=((g[1]-g2lo)/9+bleed*(g[1]-s[0])+bleed*(g[1]-d[0])+
           wdhi+gs_charge_S*((g[1]-s[0])-(old_g-old_s)))
    if lower>upper:
        raise ArithmeticError("invalid original gate residual enclosure")
    excluded=lower>0 or upper<0
    return dict(
        status=("SOURCE_REAL_Q1_GATE_SIX_CLOSED_CELL_EXCLUDED" if excluded
                else "RETAIN_SOURCE_Q1_GATE_SIX_CELL_UNRESOLVED"),
        original_gate_row=6,original_g11_row=7,
        exact_r6_lower_A=lower,exact_r6_upper_A=upper,
        strict_abs_r6_margin_A=(lower if lower>0
                                else -upper if upper<0 else F(0)),
        source_q1_g2_passive16_V=(g2lo,g2hi),
        necessary_w_minus_d_Q1_V=(wdlo,wdhi),
        necessary_w_Q1_Q2_V=(q1w["necessary_w_V"],q2w["necessary_w_V"]),
        necessary_x_Q1_Q2_V=tuple(xrequired),
        common_old_coil12_box_used=True,
        g11_guard_and_g12_branch_qualified=True,
        omitted_w_x_passive_coefficients_checked_zero=True,
        original_old_g_s_w_from_frozen_hex=True,
        physical_old_coil_predecessor_boxes_verified_in_ci=False,
        native_ieee_gl32_hyp2f1_outward_enclosed=False,
        complete_6d_stage_roots_certified=False,
        full_prep_cal_history_certified=False,
        goal27_certified=False,
    )


# S-L47: exact-real guarded Q1 gate root for every remaining five-node fiber.
def certify_original_source_q1_gate_unique_bracket(
    *,six_current_node_boxes_V,old_coil12_boxes_A,h_s,
    source_law_sha256,source_adapter_sha256,saved_cal_sha256
):
    """Source n3616 six-to-five Q1 gate row lift with strict face witnesses.

    G11 r7 has one smooth finite-Gauss guarded root w for every g,d in
    chart, and its signed derivative gives dw/dg>0. Source P16 makes Q1
    g2 affine with exact slope a_g on g, hence along r7=0:
       d r6/dg > 1388pF/h + 2e-7 + (1-a_g)/9.
    If BOTH full-parameter gate faces have opposite strict KCL signs,
    the scalar root g exists and is unique for EVERY common old-coil
    predecessor / other five coordinates. Remaining five original
    KCL roots, other hybrid branches, PREP/CAL and native rounding OPEN.
    """
    boxes=tuple(map(_source_x_box,six_current_node_boxes_V))
    olds=tuple(map(_source_x_box,old_coil12_boxes_A))
    if len(boxes)!=6 or len(olds)!=12 or boxes[1][0]>=boxes[1][1]:
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: gated six-cell bracket")
    auth=dict(h_s=h_s,source_law_sha256=source_law_sha256,
              source_adapter_sha256=source_adapter_sha256,
              saved_cal_sha256=saved_cal_sha256)
    g11=certify_original_source_g11_w_guard(
        leg="Q1",g_V=boxes[1],d_V=boxes[0],**auth)
    if (g11["status"]!="ORIGINAL_SOURCE_G11_GUARDED_W_UNIQUE_LIFT" or
            g11["gauss_charge_derivative_lower_F_per_s"]<=0):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: G11 derivative sign")
    six=tuple(v[0] for v in boxes)
    old=tuple(v[0] for v in olds)
    boundary=[six[0],six[1],F(0),F(0),six[2],
              six[3],six[4],F(0),F(0),six[5]]
    kw=dict(auth,command_V=15)
    def q1_g2(b):
        result=certify_original_source_passive16_port_lift(
            retained_node10_V=b,old_coil12_A=old,**kw)
        return result["package_voltage14_V"][_SOURCE_PACKAGE_P.index(5)]
    before=q1_g2(boundary)
    perturbed=list(boundary)
    perturbed[1]+=F(1)
    source_g2_slope=q1_g2(perturbed)-before
    # G11 derivative adds a strictly positive dw/dg in its whole guard.
    strict_slope_lower=(
        F("1388e-12")/_STAGE3616_H+
        F(2,10**7)+(1-source_g2_slope)/9)
    if strict_slope_lower<=0:
        return dict(status="RETAIN_Q1_GATE_MONOTONICITY_UNRESOLVED",
                    certified_gate_slope_lower_A_per_V=strict_slope_lower,
                    goal27_certified=False)
    face_left=list(boxes)
    face_right=list(boxes)
    face_left[1]=(boxes[1][0],boxes[1][0])
    face_right[1]=(boxes[1][1],boxes[1][1])
    left=certify_original_source_q1_gate_six_cell(
        six_current_node_boxes_V=face_left,
        old_coil12_boxes_A=olds,**auth)
    right=certify_original_source_q1_gate_six_cell(
        six_current_node_boxes_V=face_right,
        old_coil12_boxes_A=olds,**auth)
    bracket=(left["exact_r6_upper_A"]<0 and
             right["exact_r6_lower_A"]>0)
    return dict(
        status=("ORIGINAL_SOURCE_G11_Q1_GATE_UNIQUE_SIX_TO_FIVE_LIFT"
                if bracket else "RETAIN_GATE_BRACKET_UNRESOLVED"),
        necessary_q1_g_V=boxes[1],
        left_face_r6_upper_A=left["exact_r6_upper_A"],
        right_face_r6_lower_A=right["exact_r6_lower_A"],
        certified_gate_slope_lower_A_per_V=strict_slope_lower,
        exact_passive_q1_g2_vs_g_slope=source_g2_slope,
        original_finite_G11_charge_derivative_positive=True,
        shared_old_coil12_box_used=True,
        original_q1_gate_root_exists_per_fiber=bracket,
        original_q1_gate_root_unique_per_fiber=bracket,
        conditional_source_50d_to_five_node_on_guard_preimage=bracket,
        every_legal_prepared_history_covered=False,
        complete_five_kcl_source_root_cover_certified=False,
        original_w_x_g2_chart_preimage_authenticated_in_ci=False,
        native_ieee_outward_enclosed=False,
        all_cal_joint_E_certified=False,
        goal27_certified=False,
    )


# S-L48: rigorous independent Q1/Q2 gate fiber brackets after passive16.
def certify_original_source_two_gate_unique_bracket(
    *,six_current_node_boxes_V,old_coil12_boxes_A,h_s,
    source_law_sha256,source_adapter_sha256,saved_cal_sha256
):
    """Original S150 n3616, paired strict gate faces yield conditional 50D->4D.

    Four remaining current coordinates are Q1/Q2 (d,s). For every fixed
    four-coordinate/one-shared-old12 predecessor fiber, P16 exact source
    response has zero cross-gate g2 coefficients; each G11 guarded gate
    row is independently strictly increasing in its own g. If all four
    faces bracket, both gate roots exist uniquely. Every other KCL,
    unknown history, native IEEE and Goal27 remain OPEN.
    """
    cur=tuple(map(_source_x_box,six_current_node_boxes_V))
    old=tuple(map(_source_x_box,old_coil12_boxes_A))
    if len(cur)!=6 or len(old)!=12 or any(
            cur[j][0]>=cur[j][1] for j in (1,4)):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: source two-gate boxes")
    auth=dict(h_s=h_s,source_law_sha256=source_law_sha256,
              source_adapter_sha256=source_adapter_sha256,
              saved_cal_sha256=saved_cal_sha256)
    q1=certify_original_source_q1_gate_unique_bracket(
        six_current_node_boxes_V=cur,old_coil12_boxes_A=old,**auth)
    if q1["status"]=="RETAIN_Q1_GATE_MONOTONICITY_UNRESOLVED":
        return dict(status="RETAIN_TWO_GATES_UNRESOLVED",q1_gate=q1,
                    goal27_certified=False)
    kw=dict(auth,command_V=15)
    def passive_g2(six,prev,w_x_unit=None):
        b=[six[0],six[1],F(0),F(0),six[2],
           six[3],six[4],F(0),F(0),six[5]]
        if w_x_unit is not None:
            b[w_x_unit]=F(1)
        p=certify_original_source_passive16_port_lift(
            retained_node10_V=b,old_coil12_A=prev,**kw)
        idx=dict(zip(_SOURCE_PACKAGE_P,p["package_voltage14_V"]))
        return idx[5],idx[17]
    base6=tuple(a[0] for a in cur)
    base12=tuple(a[0] for a in old)
    base=passive_g2(base6,base12)
    if any(passive_g2(base6,base12,j)!=base for j in (2,3,7,8)):
        raise ArithmeticError("original passive source g2 depends on w/x")
    slopes=[]
    for i in (1,4):
        v=list(base6);v[i]+=F(1)
        q=passive_g2(v,base12)
        slopes.append((q[0]-base[0],q[1]-base[1]))
    if (slopes[0][1]!=0 or slopes[1][0]!=0 or
            not(0<=slopes[0][0]<1 and 0<=slopes[1][1]<1)):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: cross-coupled gates")
    q2w=certify_original_source_g11_w_guard(
        leg="Q2",g_V=cur[4],d_V=cur[3],**auth)
    if (q2w["status"]!="ORIGINAL_SOURCE_G11_GUARDED_W_UNIQUE_LIFT" or
            q2w["gauss_charge_derivative_lower_F_per_s"]<=0):
        raise ValueError("UNRESOLVED_SOURCE_DOMAIN: Q2 G11 panel")
    xc=F.from_float(float.fromhex(_SOURCE_X_SPECS["Q2"]["x"]))
    q2x=certify_original_source_x_kcl_outer(
        leg="Q2",d_V=cur[3],s_V=cur[5],
        x_V=(xc-F(".04"),xc+F(".04")),**auth)
    oldg=F.from_float(float.fromhex(_SOURCE_G11_W_SPECS["Q2"]["old_g"]))
    oldw=F.from_float(float.fromhex(_SOURCE_G11_W_SPECS["Q2"]["old_w"]))
    olds=F.from_float(float.fromhex(_SOURCE_X_SPECS["Q2"]["old_s"]))
    old_u=oldg-oldw
    leak=F(1,10**7)
    gs=F("1388e-12")/_STAGE3616_H
    k=(F("500e-12")/_STAGE3616_H,F("555e-12")/_STAGE3616_H)
    def face_r18(g):
        b=list(cur)
        b[4]=(g,g)
        lo6=list(base6);lo6[4]=g
        baseline=passive_g2(lo6,base12)[1]
        g2lo=g2hi=baseline
        # One original continuous affine lift: do not independently
        # choose nuisance currents for two rows / same world.
        for j,box in enumerate(b):
            v=list(lo6);v[j]=box[1]
            diff=passive_g2(v,base12)[1]-baseline
            g2lo+=min(F(0),diff)
            g2hi+=max(F(0),diff)
        for j,box in enumerate(old):
            v=list(base12);v[j]=box[1]
            diff=passive_g2(lo6,v)[1]-baseline
            g2lo+=min(F(0),diff)
            g2hi+=max(F(0),diff)
        wds=tuple(((leak+cc)*(g-dd)-cc*old_u)/(1+leak+cc)
                  for dd in cur[3] for cc in k)
        lower=(g-g2hi)/9+leak*(g-cur[5][1])+
               leak*(g-cur[3][1])+min(wds)+
               gs*((g-cur[5][1])-(oldg-olds)))
        upper=(g-g2lo)/9+leak*(g-cur[5][0])+
               leak*(g-cur[3][0])+max(wds)+
               gs*((g-cur[5][0])-(oldg-olds)))
        if lower>upper:
            raise ArithmeticError("source Q2 gate residual interval invalid")
        return lower,upper,(g2lo,g2hi)
    left=face_r18(cur[4][0])
    right=face_r18(cur[4][1])
    strict_slope=gs+2*leak+(1-slopes[1][1])/9
    if strict_slope<=0:
        return dict(status="RETAIN_TWO_GATES_UNRESOLVED",q1_gate=q1,
                    goal27_certified=False)
    both=(q1["status"]=="ORIGINAL_SOURCE_G11_Q1_GATE_UNIQUE_SIX_TO_FIVE_LIFT"
          and left[1]<0<right[0])
    return dict(
        status=("ORIGINAL_SOURCE_BOTH_GATES_UNIQUE_SIX_TO_FOUR_LIFT"
                if both else "RETAIN_TWO_GATES_UNRESOLVED"),
        original_gate_KCL_rows=(6,18),
        source_g11_rows=(7,19),
        q1_gate_face_upper_lower_A=(
            q1["left_face_r6_upper_A"],q1["right_face_r6_lower_A"]),
        q2_gate_face_upper_lower_A=(left[1],right[0]),
        q2_g2_face_intervals_V=(left[2],right[2]),
        exact_passive_g2_gate_jacobian=(
            (slopes[0][0],slopes[1][0]),
            (slopes[0][1],slopes[1][1])),
        certified_both_gate_slope_lower_A_per_V=(
            q1["certified_gate_slope_lower_A_per_V"],strict_slope),
        original_q2_w_outer_V=q2w["necessary_w_V"],
        original_q2_x_outer_V=q2x["necessary_x_V"],
        simultaneous_both_gate_roots_unique_per_four_fiber=both,
        source_50d_to_four_nonlinear_nodes_conditional=both,
        original_shared_old12_predecessor_used=True,
        all_other_source_KCL_roots_certified=False,
        source_full_own_prep_cal_history_covered=False,
        source_ieee_outward_certified=False,
        goal27_certified=False,
    )
