#!/usr/bin/env python3
"""Cost-aware goal-tolerance repair on a FINITE bank of matched histories.

All retained/candidate measurements have independent deterministic interval
noise bounds (coordinatewise boxes), not a shared Euclidean noise ball.
Each command's true scalar goal lies in a supplied closed interval.
A result is exact only relative to the supplied bank and candidate library.
No physics, reachability, acquisition cost or command legality is inferred.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def _array(value, shape, name, *, nonnegative=False, positive=False):
    a = np.asarray(value, dtype=float)
    if a.shape != shape or not np.all(np.isfinite(a)):
        raise ValueError(f"{name} must be finite and have shape {shape}")
    if (nonnegative and np.any(a < 0)) or (positive and np.any(a <= 0)):
        raise ValueError(f"{name} must contain {'positive' if positive else 'nonnegative'} values")
    return a


def _names(value, n, name):
    names = [str(x) for x in (value if value is not None else [f"{name}_{j}" for j in range(n)])]
    if len(names) != n or len(set(names)) != len(names) or any(not v.strip() for v in names):
        raise ValueError(f"{name} must supply {n} distinct nonempty names")
    return names


def _greedy(cover_masks, prices, all_mask):
    missing = all_mask
    picked = []
    while missing:
        options = [(float(prices[j]) / count, j)
                   for j, bits in enumerate(cover_masks)
                   if j not in picked and (count := (bits & missing).bit_count())]
        if not options:
            raise RuntimeError("internal uncovered conflict")
        j = min(options)[1]
        picked.append(j)
        missing &= ~cover_masks[j]
    return tuple(sorted(picked))


def _exact(cover_masks, prices, all_mask, first_choice):
    best = first_choice
    best_cost = float(np.sum(prices[list(best)]))
    options_for_pair = [[] for _ in range(all_mask.bit_count())]
    for j, mask in enumerate(cover_masks):
        while mask:
            low = mask & -mask
            options_for_pair[low.bit_length() - 1].append(j)
            mask ^= low

    def visit(missing, chosen, total):
        nonlocal best, best_cost
        if not missing:
            candidate = tuple(sorted(chosen))
            if total < best_cost or (total == best_cost and candidate < best):
                best, best_cost = candidate, total
            return
        if total >= best_cost:
            return
        # Branch on the remaining conflict having fewest covering features.
        bits = missing
        pivot = None
        fewest = float("inf")
        while bits:
            bit = bits & -bits
            idx = bit.bit_length() - 1
            viable = [j for j in options_for_pair[idx] if j not in chosen]
            if len(viable) < fewest:
                fewest, pivot = len(viable), idx
                if fewest <= 1:
                    break
            bits ^= bit
        for j in sorted(options_for_pair[pivot], key=lambda t: (float(prices[t]), t)):
            if j in chosen:
                continue
            new_cost = total + float(prices[j])
            if new_cost >= best_cost:
                continue
            visit(missing & ~cover_masks[j], chosen + (j,), new_cost)

    visit(all_mask, (), 0.0)
    return best


def audit(observations, goals, candidates, *, observation_radii,
          candidate_radii, goal_tolerances, candidate_costs,
          goal_uncertainty=None, candidate_names=None, command_names=None,
          exact_candidate_cap=18):
    """Solve robust feature cover; K goals mean same bank, K fixed legal commands.

    Returns a nonadaptive common feature subset, with separate decoders
    allowed for each known command. Never uses a posttarget goal as input.
    """
    o = np.asarray(observations, dtype=float)
    g = np.asarray(goals, dtype=float)
    p = np.asarray(candidates, dtype=float)
    if o.ndim != 2 or o.shape[0] < 1:
        raise ValueError("observations must be (N,m), N >= 1; m may be zero")
    n, m = o.shape
    if g.ndim == 1:
        g = g[:, None]
    if g.ndim != 2 or g.shape[0] != n or g.shape[1] < 1:
        raise ValueError("goals must be (N,K) or (N,), K >= 1")
    k = g.shape[1]
    if p.ndim != 2 or p.shape[0] != n:
        raise ValueError("candidates must be (N,P); P may be zero")
    q = p.shape[1]
    o = _array(o, (n, m), "observations")
    g = _array(g, (n, k), "goals")
    p = _array(p, (n, q), "candidates")
    so = _array(observation_radii, (m,), "observation_radii", nonnegative=True)
    sp = _array(candidate_radii, (q,), "candidate_radii", nonnegative=True)
    tau = _array(goal_tolerances, (k,), "goal_tolerances", nonnegative=True)
    costs = _array(candidate_costs, (q,), "candidate_costs", positive=True)
    eta = _array(np.zeros((n, k)) if goal_uncertainty is None else goal_uncertainty,
                 (n, k), "goal_uncertainty", nonnegative=True)
    labels = _names(candidate_names, q, "candidate")
    commands = _names(command_names, k, "command")
    if not isinstance(exact_candidate_cap, int) or exact_candidate_cap < 0:
        raise ValueError("exact_candidate_cap must be a nonnegative integer")

    # Every history must itself admit a decoder within its goal interval.
    self_bad = np.argwhere(eta > tau[None, :])
    if len(self_bad):
        i, c = map(int, self_bad[0])
        return {"status": "INTRINSIC_GOAL_UNCERTAINTY", "history": i,
                "command": commands[c], "goal_uncertainty": float(eta[i, c]),
                "goal_tolerance": float(tau[c]),
                "claim_ceiling": "Even perfect history identification cannot meet this requested tolerance."}

    # Coordinatewise error intervals intersect exactly at distances <= 2*sigma.
    base_pairs = []
    conflict_pairs = []
    feature_masks = [0] * q
    for i in range(n):
        for j in range(i + 1, n):
            if not np.all(np.abs(o[i] - o[j]) <= 2 * so):
                continue
            base_pairs.append((i, j))
            different = np.abs(g[i] - g[j]) + eta[i] + eta[j]
            if not np.any(different > 2 * tau):
                continue
            t = len(conflict_pairs)
            violating = np.flatnonzero(different > 2 * tau)
            conflict_pairs.append((i, j, [commands[c] for c in violating]))
            for a in range(q):
                if abs(float(p[i, a] - p[j, a])) > 2 * sp[a]:
                    feature_masks[a] |= (1 << t)

    def radii_for(chosen):
        answer = eta.max(axis=0).astype(float)
        for i, j in base_pairs:
            if chosen and any(abs(float(p[i, a] - p[j, a])) > 2 * sp[a] for a in chosen):
                continue
            answer = np.maximum(answer, (np.abs(g[i] - g[j]) + eta[i] + eta[j]) / 2)
        return [float(x) for x in answer]

    output = {
        "schema_version": 1,
        "history_count": n,
        "command_names": commands,
        "candidate_names": labels,
        "base_indistinguishable_pair_count": len(base_pairs),
        "goal_conflict_pair_count": len(conflict_pairs),
        "baseline_minimax_error_by_command": radii_for(()),
        "goal_tolerances": [float(x) for x in tau],
        "claim_ceiling": (
            "Exact deterministic robust minimax on the supplied finite bank, "
            "fixed common legal commands and candidate library, under independent "
            "coordinatewise measurement intervals and per-history goal intervals. "
            "Cover feasibility is not sufficient on a larger physical reachable class, "
            "not a hardware measurement plan, and not an autonomous stage-update proof."
        ),
    }
    if not conflict_pairs:
        return {**output, "status": "NO_REPAIR_NEEDED", "selected_indices": [],
                "selected_names": [], "total_cost": 0.0,
                "selected_minimax_error_by_command": radii_for(())}
    mask = (1 << len(conflict_pairs)) - 1
    all_covered = 0
    for cm in feature_masks:
        all_covered |= cm
    if all_covered != mask:
        first = ((mask & ~all_covered) & -(mask & ~all_covered)).bit_length() - 1
        i, j, cs = conflict_pairs[first]
        return {**output, "status": "NO_LIBRARY_REPAIR", "uncovered_history_pair": [i, j],
                "uncovered_commands": cs, "best_possible_under_library": False}
    chosen = _greedy(feature_masks, costs, mask)
    exact = q <= exact_candidate_cap
    if exact:
        chosen = _exact(feature_masks, costs, mask, chosen)
    picked = list(chosen)
    value = radii_for(chosen)
    if not np.all(np.asarray(value) <= tau):
        raise RuntimeError("internal cover/diameter mismatch")
    return {**output,
            "status": "EXACT_MIN_COST_REPAIR" if exact else "GREEDY_FEASIBLE_NOT_PROVEN_MINIMUM",
            "selected_indices": picked,
            "selected_names": [labels[j] for j in chosen],
            "total_cost": float(np.sum(costs[picked])),
            "selected_minimax_error_by_command": value,
            "selected_feature_noise_radii": [float(sp[j]) for j in picked],
            "greedy_set_cover_factor_bound": float(sum(1.0 / j for j in range(1, len(conflict_pairs) + 1))),
            "minimum_cost_proven_within_candidate_library": bool(exact),
            "example_goal_conflict_pair": list(conflict_pairs[0][:2]),
            }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="NPZ with bank, candidate features and bounds")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--exact-candidate-cap", type=int, default=18)
    args = parser.parse_args()
    with np.load(args.input, allow_pickle=False) as data:
        fields = ["observations", "goals", "candidates", "observation_radii",
                  "candidate_radii", "goal_tolerances", "candidate_costs"]
        absent = [f for f in fields if f not in data.files]
        if absent:
            parser.error("missing NPZ fields: " + ", ".join(absent))
        optional = {field: data[field] if field in data.files else None
                    for field in ["goal_uncertainty", "candidate_names", "command_names"]}
        report = audit(data["observations"], data["goals"], data["candidates"],
                       observation_radii=data["observation_radii"],
                       candidate_radii=data["candidate_radii"],
                       goal_tolerances=data["goal_tolerances"],
                       candidate_costs=data["candidate_costs"],
                       exact_candidate_cap=args.exact_candidate_cap, **optional)
    body = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(body, encoding="utf-8")
    else:
        print(body, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
