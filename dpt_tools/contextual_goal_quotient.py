"""Finite-word goal observability modulo an arbitrary shared nuisance.

Conditional common-state linear algebra: x_next=A_command @ x,
y=H @ x + N @ eta, future goals C @ F_word @ x.
eta is arbitrary (unbounded), not a bounded stochastic/ellipsoid error.
Added ideal scalar source-state measurements are nuisance-free.
Floating SVD ranks require physically justified units and tolerance.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np


def _rank(singular_values, shape, rtol):
    return int(np.count_nonzero(singular_values >
               rtol * max(shape[0], shape[1], 1)
               * (singular_values[0] if singular_values.size else 0)))


def audit_contextual_goal_quotient(updates, observation, nuisance, goal, words, *, rtol=1e-12):
    """Report exact-model finite-word row-rank deficits and aliasing witness.

    All inputs must use a single physically scaled linear-state chart.
    Each word is a list of zero-based command indices; [] is the identity.
    Unlisted (even legal) words are outside this computation.
    """
    A = np.asarray(updates, dtype=float)
    H = np.asarray(observation, dtype=float)
    N = np.asarray(nuisance, dtype=float)
    C = np.asarray(goal, dtype=float)
    if A.ndim != 3 or A.shape[1] != A.shape[2] or A.shape[1] < 1:
        raise ValueError("updates must be (commands,n,n) with n>0")
    n = A.shape[1]
    if (H.ndim != 2 or H.shape[1] != n or N.ndim != 2 or
            N.shape[0] != H.shape[0] or C.ndim != 2 or C.shape[1] != n):
        raise ValueError("inconsistent observation/nuisance/goal dimensions")
    if not all(np.isfinite(x).all() for x in (A, H, N, C)) or not np.isfinite(rtol) or rtol <= 0:
        raise ValueError("finite inputs and positive rank tolerance required")
    if not isinstance(words, (list, tuple)) or not words:
        raise ValueError("provide at least one declared command word")

    m = H.shape[0]
    U, sN, _ = np.linalg.svd(N, full_matrices=True)
    rn = _rank(sN, N.shape, rtol)
    O0 = U[:, rn:].T @ H  # sensor rows annihilating unknown eta
    _, sO, vto = np.linalg.svd(O0, full_matrices=True)
    ro = _rank(sO, O0.shape, rtol)
    Q = vto[:ro]  # orthonormal row basis in state coordinates
    P = Q.T @ Q

    raw = []
    for word in words:
        if not isinstance(word, (list, tuple)):
            raise ValueError("each word must be a sequence of indexes")
        F = np.eye(n)
        for index in word:
            if not isinstance(index, (int, np.integer)) or index < 0 or index >= A.shape[0]:
                raise ValueError("unknown/illegal command index")
            F = A[int(index)] @ F
        raw.append(C @ F)
    G = np.concatenate(raw, axis=0)
    _, sG, _ = np.linalg.svd(G, full_matrices=False)
    rg = _rank(sG, G.shape, rtol)
    aug = np.concatenate([O0, G], axis=0)
    _, sAug, _ = np.linalg.svd(aug, full_matrices=False)
    r_aug = _rank(sAug, aug.shape, rtol)

    rem = G - G @ P
    per_row = np.linalg.norm(rem, axis=1)
    chosen = int(np.argmax(per_row)) if per_row.size else None
    if chosen is not None and per_row[chosen] > 0:
        h = rem[chosen] / per_row[chosen]
        witness_gap = float(2 * (G[chosen] @ h))
    else:
        h = np.zeros(n)
        witness_gap = 0.0
    # Identical output for +/-h can be achieved by adjusting unbounded eta
    # if H@h belongs to range(N), which is checked by this residual.
    eta_diff = np.linalg.lstsq(N, -H @ h, rcond=None)[0]
    obs_res = float(np.linalg.norm(H @ h + N @ eta_diff))
    return {
        "status": "LINEAR_FINITE_WORD_UNBOUNDED_NUISANCE_NUMERIC_AUDIT",
        "nuisance_rank": rn,
        "nuisance_free_readout_count": m - rn,
        "current_nuisance_invariant_rank": ro,
        "future_goal_rank": rg,
        "minimum_extra_ideal_scalar_rows": r_aug - ro,
        "stacked_goal_rows": G.tolist(),
        "goal_remainder_by_row": per_row.tolist(),
        "maximum_goal_remainder": float(per_row.max()) if per_row.size else 0.0,
        "witness_history_direction": h.tolist(),
        "witness_goal_row": chosen,
        "witness_goal_gap": witness_gap,
        "witness_current_observation_residual": obs_res,
        "rank_tolerance": float(rtol),
        "scope": "given finite words, exact linear updates, unbounded nuisance, arbitrary ideal extra noiseless rows",
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", help="JSON with updates, observation, nuisance, goal, words")
    parser.add_argument("--output", help="optional JSON report")
    args = parser.parse_args()
    payload = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    result = audit_contextual_goal_quotient(**payload)
    txt = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.output:
        Path(args.output).write_text(txt, encoding="utf-8")
    else:
        print(txt, end="")


if __name__ == "__main__":
    main()
