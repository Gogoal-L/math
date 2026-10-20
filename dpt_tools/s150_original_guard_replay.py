"""Fail-closed replay of original S150 Pro18E saved point ETH guard only.

Reads SHA-pinned, caller-owned original source ZIP and saved CAL NPZ in place.
Never validates complete source roots, guards other than ETH, sensor E or Goal27.
"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

import numpy as np


SOURCE_ZIP_SHA256 = "250aa4ea17514ffdeda3a51d95bedf8e034b181f97bdc254db29ddc36281b9c8"
ACTUAL_LAW_SHA256 = "51b78f729393d29745f59ca150adfef69e1847bf26a8853c6cef3d6be9e2083d"
E_SAVED_CAL_SHA256 = "baafdd8cb489adb186677658c4a8031130cc53a9a1854c4997211d437daf8b3e"
ADAPTER_SHA256 = "7f03e36809caf3dea1295cf58d7dd70c413ef7991472a5e6eec3405da18f5669"
ACTUAL_LAW_MEMBER = "analysis/actual_law.py"
STATUS = "POINT_SOURCE_GUARD_ONLY_NOT_ALL_ROOT"
NET3_LIPSCHITZ_V_PER_C = .00570172  # sup derivative after original [-60,260] T clip


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for buf in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(buf)
    return digest.hexdigest()


def scan_original_eth_guard(time_s, state50):
    """Source-point Q2 ETH sign scan: no root existence/complement inference."""
    t = np.asarray(time_s, dtype=float)
    y = np.asarray(state50, dtype=float)
    if (t.ndim != 1 or len(t) < 2 or y.shape != (len(t), 50)
        or not np.isfinite(t).all() or not np.isfinite(y).all()
        or not np.all(np.diff(t) > 0)):
        raise ValueError("requires finite strictly increasing t, matching 50D source states")
    # SHA-pinned source node order: 26 nodes, 12 coils, 2 diode A, 2 junction V, 8 T.
    # Q2 g=18, Q2 s=21, Q2 junction temperature=46 in original actual_law.py.
    g_minus_s = np.clip(y[:, 18] - y[:, 21], -8., 19.)
    T = np.clip(y[:, 46], -60., 260.)
    net3 = np.clip(8.381e-6 * T*T - 4.696e-3 * T + 2.8224, 1.7, 3.2)
    margin = g_minus_s - net3
    absolute = np.abs(margin)
    idx = int(np.argmin(absolute))
    pairs = [[int(i), int(i+1)] for i in np.flatnonzero(
        (margin[:-1] > 0) & (margin[1:] < 0) |
        (margin[:-1] < 0) & (margin[1:] > 0))]
    # One common source center is NOT a parameter/history outer.
    strip_08 = .0008 + .0008 + NET3_LIPSCHITZ_V_PER_C*.001
    perturb_1 = .001 + .001
    return {
        "status": STATUS,
        "source_stage_count": int(len(t)-1),
        "min_abs_margin_index": idx,
        "min_abs_margin_V": float(absolute[idx]),
        "signed_margin_at_min_V": float(margin[idx]),
        "time_at_min_s": float(t[idx]),
        "sign_crossing_pairs": pairs,
        "independent_0p8mV_plus_0p001C_preserves_saved_signs": bool(
            np.all(absolute > strip_08)),
        "positive_margin_under_declared_strip_V": float(np.min(absolute)-strip_08),
        "independent_1mV_gate_source_can_flip_weakest": bool(
            np.any((margin < 0) & (margin + perturb_1 > 0))
            or np.any((margin > 0) & (margin - perturb_1 < 0))),
        "claim_ceiling": "SAVED_POINTS_ETH_ONLY; no 50D root existence, all-root/guard cover, reset, joint CAL E or H841 Goal27 certificate",
    }


def replay_original_archive(original_zip, e_saved_cal):
    """Require exact source/NPZ bytes; reject substitutions or re-labeled histories."""
    if _sha256(original_zip) != SOURCE_ZIP_SHA256:
        raise ValueError("original source ZIP SHA mismatch")
    with zipfile.ZipFile(original_zip) as archive:
        member = archive.read(ACTUAL_LAW_MEMBER)
    if hashlib.sha256(member).hexdigest() != ACTUAL_LAW_SHA256:
        raise ValueError("actual_law.py member SHA mismatch")
    if _sha256(e_saved_cal) != E_SAVED_CAL_SHA256:
        raise ValueError("Pro18E saved CAL SHA mismatch")
    with np.load(e_saved_cal, allow_pickle=False) as saved:
        needed = {"time_s", "command_V", "state50", "H_s",
                  "measurement_V_A", "source_identity_json"}
        if not needed.issubset(saved.files):
            raise ValueError("missing saved source/history or observation member")
        t = saved["time_s"]
        state = saved["state50"]
        command = saved["command_V"]
        H = saved["H_s"]
        obs = saved["measurement_V_A"]
        identity = json.loads(str(saved["source_identity_json"].item()))
    if (state.shape != (4927, 50) or command.shape != (4927,)
        or H.shape != (4801,) or obs.shape != (4801, 2)):
        raise ValueError("invalid PREP126/CAL4800 source/observation shape")
    expected = {
        "actual_law_sha256": ACTUAL_LAW_SHA256,
        "source_adapter_sha256": ADAPTER_SHA256,
        "schema": "PRO18E_RETROSPECTIVE_CAL_COVERAGE_V1",
        "time_samples_including_prep_and_cal": 4927,
        "time_interval_count": 4926,
        "prep_sample_count": 127,
        "cal_H_sample_count": 4801,
    }
    if any(identity.get(k) != v for k, v in expected.items()):
        raise ValueError("saved history identity contract mismatch")
    if float(identity.get("L_h", 0)) != 4.3e-9 or float(identity.get("Rg_ohm", 0)) != 7.5:
        raise ValueError("wrong source condition: do not mix Pro18C/Pro18E")
    result = scan_original_eth_guard(t, state)
    result["archive_zip_sha256"] = SOURCE_ZIP_SHA256
    result["saved_cal_sha256"] = E_SAVED_CAL_SHA256
    result["actual_law_member_sha256"] = ACTUAL_LAW_SHA256
    result["source_identity"] = identity
    # This is the recorded point-replay benchmark, NOT a strict interval root cert.
    if (result["min_abs_margin_index"] != 1707 or
        not (-.001750 < result["signed_margin_at_min_V"] < -.001748) or
        [1707,1708] not in result["sign_crossing_pairs"]):
        raise ValueError("archived ETH reference point guard benchmark drift")
    return result



def certify_original_eth_seam_band():
    """Exact rational real-source ETH guard-interface certificate.

    The source decimal literals are from ACTUAL_LAW_SHA256; callers must use
    replay_original_archive to authenticate the separate original source bytes.
    This fixed temperature band certificate is not a full-50D root/reset proof.
    """
    from fractions import Fraction as F

    def q(x):
        return F(str(x))

    def add(a, b):
        out = [F(0)] * max(len(a), len(b))
        for i, x in enumerate(a):
            out[i] += x
        for i, x in enumerate(b):
            out[i] += x
        return out

    def mul(a, b):
        out = [F(0)] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i+j] += x*y
        return out

    def scale(a, s):
        return [x*q(s) for x in a]

    def sub(a, b):
        return add(a, scale(b, -1))

    def power(a, n):
        out = [F(1)]
        for _ in range(n):
            out = mul(out, a)
        return out

    def poly(coefficients, x):
        out = [F(0)]
        for coefficient in coefficients:
            out = add(mul(out, x), [q(coefficient)])
        return out

    def eval_exact(coefficients, z):
        out = F(0)
        for coefficient in coefficients[::-1]:
            out = out*z + coefficient
        return out

    def interval_horner(coefficients, radius):
        def times(a, b):
            items = [x*y for x in a for y in b]
            return min(items), max(items)
        interval = (coefficients[-1], coefficients[-1])
        for coefficient in coefficients[-2::-1]:
            lo, hi = times(interval, (-radius, radius))
            interval = (lo+coefficient, hi+coefficient)
        return interval

    def derivative(coefficients):
        return [i*x for i,x in enumerate(coefficients)][1:] or [F(0)]

    T = [q("25.00855"), F(1)]  # z=T-25.00855, |z| <= 0.00015 C
    z_radius = q("0.00015")
    g = add(add(scale(power(T, 2), "8.381e-6"),
                scale(T, "-4.696e-3")), [q("2.8224")])

    high = [
        poly(["-22.48e-6", "5.637e-3", "87.27e-3", "-59.02"], T),
        poly(["567.2e-6", "-0.1404", "-2.866", "1502.6"], T),
        poly(["-3.728e-3", "0.9245", "20.77", "-9359.8"], T),
        poly(["5.447e-3", "-1.424", "-31.8", "13239.5"], T),
    ]
    low = [
        poly(["3.788e-6", "-2.125e-3", "0.2401", "-10.98"], T),
        poly(["18.97e-6", "-8.24e-3", "1.272", "-339.4"], T),
        poly(["20.94e-6", "6.024e-3", "-3.617", "-1063.7"], T),
    ]
    def compose(c):
        out = [F(0)]
        for term in c:
            out = add(mul(out, g), term)
        return scale(out, F(1, 1000))

    high = compose(high)
    low = compose(low)
    difference = sub(high, low)
    reff = sub([q(".07")],
               poly(["239.024e-9", "-17.829e-6", "296.341e-6"], T))

    # Directed rational interval-Horner derivatives prove monotonicity
    # of the *fully composed* source polynomials on the complete band.
    dderiv = interval_horner(derivative(difference), z_radius)
    gderiv = interval_horner(derivative(g), z_radius)
    rderiv = interval_horner(derivative(reff), z_radius)
    if not (dderiv[0] > 0 and gderiv[1] < 0 and rderiv[0] > 0):
        raise ArithmeticError("source polynomial monotonicity unproved")
    lo_d, hi_d = (eval_exact(difference, z)
                  for z in (-z_radius, z_radius))
    gmin, gmax = (eval_exact(g, z) for z in (z_radius, -z_radius))
    rmin, rmax = (eval_exact(reff, z)
                  for z in (-z_radius, z_radius))

    # Even coarse exact interval-Horner images stay away from every clip:
    # source temperature, clipped gate, threshold and two ETH output clips.
    hi_box = interval_horner(high, z_radius)
    lo_box = interval_horner(low, z_radius)
    if not (q("1.7") < gmin <= gmax < q("3.2")
            and q("-8") < gmin and gmax < q("15")
            and all(q("-3") < z < q("15") for z in (*hi_box, *lo_box))):
        raise ArithmeticError("source ETH branch clipping not excluded")
    # These are fixed outward decimal bounds, independently checked against
    # exact rational endpoint values rather than asserted as data.
    d_bound = (q("-0.006297989895415"), q("-0.006292235773735"))
    g_bound = (q("2.710200916147"), q("2.710202199233"))
    r_bound = (q("0.070000043356052"), q("0.070000045119393"))
    if not (d_bound[0] <= lo_d <= hi_d <= d_bound[1]
            and g_bound[0] <= gmin <= gmax <= g_bound[1]
            and r_bound[0] <= rmin <= rmax <= r_bound[1]
            and d_bound[1] < 0 and r_bound[0] > 0):
        raise ArithmeticError("claimed outward source band not certified")

    return {
        "status": "ORIGINAL_SOURCE_DECIMAL_REAL_INTERVAL_ONLY",
        "actual_law_sha256": ACTUAL_LAW_SHA256,
        "temperature_C_closed": ["25.0084", "25.0087"],
        "eth_high_minus_low_V_outward": [str(x) for x in d_bound],
        "threshold_gstar_V_outward": [str(x) for x in g_bound],
        "body_reff_ohm_outward": [str(x) for x in r_bound],
        "minimum_compensating_body_voltage_V_strict": str(-d_bound[1]),
        "source_root_status": "NOT_CERTIFIED",
        "guard_reset_status": "UNRESOLVED",
        "full_CAL_goal27_status": "NOT_CERTIFIED",
    }


def classify_original_eth_guard_rectangle(temperature_C, gate_minus_source_V):
    """All-point exact-decimal source guard proof on one T/g box; NOT 50D roots."""
    from fractions import Fraction as F

    def limits(value, label):
        if not isinstance(value, (tuple, list)) or len(value) != 2 or any(
                not isinstance(v, str) for v in value):
            raise ValueError(label + " requires two exact rational strings")
        try:
            lo, hi = [F(v) for v in value]
        except (ValueError, ZeroDivisionError):
            raise ValueError(label + " has invalid rational bounds") from None
        if lo > hi:
            raise ValueError(label + " has reversed bounds")
        return lo, hi

    def clip(v, lo, hi):
        return min(hi, max(lo, v))

    raw_Tl, raw_Th = limits(temperature_C, "T")
    raw_Gl, raw_Gh = limits(gate_minus_source_V, "g-s")
    Tl, Th = raw_Tl, raw_Th
    Gl, Gh = raw_Gl, raw_Gh
    Tl, Th = clip(Tl, F(-60), F(260)), clip(Th, F(-60), F(260))
    Gl, Gh = clip(Gl, F(-8), F(19)), clip(Gh, F(-8), F(19))

    def net3(T):
        return clip(F("8.381e-6")*T*T-F("4.696e-3")*T+F("2.8224"),
                    F("1.7"), F("3.2"))

    assert (2*F("8.381e-6")*F(-60)-F("4.696e-3") < 0
            and 2*F("8.381e-6")*F(260)-F("4.696e-3") < 0)
    th_lo, th_hi = net3(Th), net3(Tl)
    if Gh < th_lo:
        mode, margin = "STRICT_LOW", th_lo-Gh
    elif Gl > th_hi:
        mode, margin = "STRICT_HIGH", Gl-th_hi
    else:
        mode, margin = "RETAIN_BOTH_FRONTIER", F(0)
    return {
        "status": "SOURCE_DECIMAL_GUARD_ONLY_NOT_50D_ROOT",
        "actual_law_member_sha256": ACTUAL_LAW_SHA256,
        "raw_temperature_C": [str(raw_Tl), str(raw_Th)],
        "raw_gate_minus_source_V": [str(raw_Gl), str(raw_Gh)],
        "effective_clipped_temperature_C": [str(Tl), str(Th)],
        "effective_clipped_gate_minus_source_V": [str(Gl), str(Gh)],
        "temperature_C": [str(Tl), str(Th)],
        "gate_minus_source_V": [str(Gl), str(Gh)],
        "threshold_V": [str(th_lo), str(th_hi)],
        "mode": mode,
        "strict_margin_V": str(margin),
        "all_roots": False,
        "goal27": "NOT_CERTIFIED",
    }


def bisect_original_eth_guard_rectangle(temperature_C, gate_minus_source_V,
                                        *, depth=0):
    """A complete closed 2D rectangular guard partition, with all undecided kept."""
    from fractions import Fraction as F
    if type(depth) is not int or not 0 <= depth <= 12:
        raise ValueError("depth must be an integer in [0,12]")
    leaves = []

    def go(t, g, n):
        report = classify_original_eth_guard_rectangle(t, g)
        if n == 0 or report["mode"] != "RETAIN_BOTH_FRONTIER":
            leaves.append(report)
            return
        gl, gh = map(F, g)
        if gl < gh:
            mid = (gl+gh)/2
            go(t, (str(gl), str(mid)), n-1)
            go(t, (str(mid), str(gh)), n-1)
        else:
            tl, th = map(F, t)
            if tl < th:
                mid = (tl+th)/2
                go((str(tl), str(mid)), g, n-1)
                go((str(mid), str(th)), g, n-1)
            else:
                leaves.append(report)

    go(temperature_C, gate_minus_source_V, depth)
    return {
        "status": "CLOSED_2D_GUARD_COVER_NOT_ROOT_COVER",
        "leaves": leaves,
        "count_by_mode": {mode: sum(x["mode"] == mode for x in leaves)
                          for mode in ("STRICT_LOW", "STRICT_HIGH",
                                       "RETAIN_BOTH_FRONTIER")},
        "all_roots": False,
        "goal27": "NOT_CERTIFIED",
    }


def classify_original_eth_guard_state50_box(state50_intervals):
    """Project a FULL 50D physical source-state BOX onto exact Q2 ETH guard.

    This is a NECESSARY guard constraint and cannot prove 50D root existence.
    Uses interval subtraction for correlated g/s (conservative if correlated).
    """
    from fractions import Fraction as F
    if not isinstance(state50_intervals, (list, tuple)) or len(state50_intervals) != 50:
        raise ValueError("state50_intervals requires all 50 source coordinates")
    for i, interval in enumerate(state50_intervals):
        if (not isinstance(interval, (list,tuple)) or len(interval)!=2
                or not all(isinstance(v,str) for v in interval)):
            raise ValueError("state coordinate must be two exact rational strings: "+str(i))
        try:
            lo,hi=[F(v) for v in interval]
        except (ValueError,ZeroDivisionError):
            raise ValueError("state coordinate invalid rational: "+str(i)) from None
        if lo>hi:
            raise ValueError("state coordinate reversed: "+str(i))
    gl,gh=map(F,state50_intervals[18])
    sl,sh=map(F,state50_intervals[21])
    t=state50_intervals[46]
    result=classify_original_eth_guard_rectangle(
        t,(str(gl-sh),str(gh-sl)))
    result["full50_input_projection"] = {
        "gate_index":18,
        "source_index":21,
        "temperature_index":46,
        "joint_gate_source_correlation": "OUTER_INTERVAL_SUBTRACTION",
    }
    result["source_root_qualified"] = False
    result["valid_predecessor_history"] = False
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original-zip", required=True)
    parser.add_argument("--saved-cal", required=True)
    args = parser.parse_args()
    report = replay_original_archive(args.original_zip, args.saved_cal)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
