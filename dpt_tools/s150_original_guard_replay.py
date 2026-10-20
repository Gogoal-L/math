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
