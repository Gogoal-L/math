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



def _greedy_history_coloring(neighbors):
    """A feasible deterministic DSATUR coloring; not necessarily minimum."""
    n = len(neighbors)
    colors = [-1] * n
    for _ in range(n):
        uncolored = [i for i in range(n) if colors[i] < 0]
        v = max(uncolored, key=lambda i:
                (len({colors[j] for j in neighbors[i] if colors[j] >= 0}),
                 len(neighbors[i]), -i))
        used = {colors[j] for j in neighbors[v] if colors[j] >= 0}
        colors[v] = next(k for k in range(n) if k not in used)
    return colors, max(colors, default=-1) + 1


def _greedy_clique_bound(neighbors):
    """Construct an actual clique: its size is a valid chromatic lower bound."""
    if not neighbors:
        return 0
    best = 1
    for start in sorted(range(len(neighbors)),
                        key=lambda i: (-len(neighbors[i]), i)):
        clique = [start]
        for candidate in sorted(neighbors[start],
                                key=lambda i: (-len(neighbors[i]), i)):
            if all(candidate in neighbors[v] for v in clique):
                clique.append(candidate)
        best = max(best, len(clique))
    return best


def _exact_k_colorable(neighbors, k):
    """Decision search with color-label symmetry eliminated; returns witness."""
    n = len(neighbors)
    colors = [-1] * n

    def search(used_colors):
        if all(c >= 0 for c in colors):
            return colors.copy()
        uncolored = [v for v in range(n) if colors[v] < 0]
        v = max(uncolored, key=lambda i:
                (len({colors[j] for j in neighbors[i] if colors[j] >= 0}),
                 len(neighbors[i]), -i))
        forbidden = {colors[j] for j in neighbors[v] if colors[j] >= 0}
        for choice in range(min(k, used_colors + 1)):
            if choice in forbidden:
                continue
            colors[v] = choice
            answer = search(max(used_colors, choice + 1))
            if answer is not None:
                return answer
            colors[v] = -1
        return None

    return search(0)


def audit_retained_goal_bits(
    observations, goals, transcript_ids, *,
    observation_radii, goal_tolerances, goal_uncertainty=None,
    exact_transcript_cap=17,
):
    """Exact or bounded fixed-length memory for a FINITE source-history bank.

    A pretarget, EXACT archived transcript category is mapped to one fixed
    message. After that message is retained, the predictor receives a later
    side-observation y lying in a per-history coordinatewise interval box.
    The decoder sees (message, y), NOT the future true goals or forgotten
    transcript. Prediction must cover each specified scalar future-command
    goal and its deterministic interval uncertainty within its own tolerance.

    This is one-shot deterministic finite-bank zero-error FUNCTION coding
    with side information. It is NOT a Gaussian-streaming sample theorem,
    a raw-waveform memory lower bound, or physical SiC sensor validation.
    """
    o = np.asarray(observations, dtype=float)
    g = np.asarray(goals, dtype=float)
    if o.ndim != 2 or g.ndim != 2 or o.shape[0] < 1 or g.shape[0] != o.shape[0]:
        raise ValueError("observations and goals must be 2D with identical positive history count")
    n, m = o.shape
    q = g.shape[1]
    if q < 1 or not np.all(np.isfinite(o)) or not np.all(np.isfinite(g)):
        raise ValueError("goals must have positive column count and all arrays must be finite")
    radii = _array(observation_radii, (m,), "observation_radii", nonnegative=True)
    tau = _array(goal_tolerances, (q,), "goal_tolerances", nonnegative=True)
    eta = (np.zeros((n, q)) if goal_uncertainty is None
           else _array(goal_uncertainty, (n, q), "goal_uncertainty", nonnegative=True))
    if not isinstance(exact_transcript_cap, int) or exact_transcript_cap < 1:
        raise ValueError("exact_transcript_cap must be a positive integer")
    ids = np.asarray(transcript_ids, dtype=object)
    if ids.shape != (n,) or any(not isinstance(x, str) or not x.strip()
                                for x in ids.tolist()):
        raise ValueError("transcript_ids must contain one nonempty exact string per history")

    group_index = {}
    groups = []
    by_history = []
    for h, label in enumerate(ids.tolist()):
        if label not in group_index:
            group_index[label] = len(groups)
            groups.append(label)
        by_history.append(group_index[label])
    gcount = len(groups)

    intrinsic = np.argwhere(eta > tau[None, :])
    if intrinsic.size:
        return {
            "status": "INTRINSIC_GOAL_INTERVAL",
            "unresolvable_history": int(intrinsic[0, 0]),
            "unresolvable_goal": int(intrinsic[0, 1]),
            "minimum_messages": None, "minimum_retained_bits": None,
            "history_count": n, "transcript_group_count": gcount,
        }

    neighbors = [set() for _ in groups]
    conflict_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            if not np.all(np.abs(o[i] - o[j]) <= 2 * radii):
                continue
            if not np.any(np.abs(g[i] - g[j]) + eta[i] + eta[j] > 2 * tau):
                continue
            conflict_pairs.append((i, j))
            x, y = by_history[i], by_history[j]
            if x == y:
                return {
                    "status": "INTRINSIC_TRANSCRIPT_ALIAS",
                    "unresolvable_history_pair": [i, j],
                    "minimum_messages": None, "minimum_retained_bits": None,
                    "history_count": n, "transcript_group_count": gcount,
                }
            neighbors[x].add(y)
            neighbors[y].add(x)

    greedy, upper = _greedy_history_coloring(neighbors)
    lower = _greedy_clique_bound(neighbors)
    colors = greedy
    exact = lower == upper
    if not exact and gcount <= exact_transcript_cap:
        for k in range(lower, upper):
            winner = _exact_k_colorable(neighbors, k)
            if winner is not None:
                colors, upper, exact = winner, k, True
                break
        else:
            exact = True

    bits = lambda k: (k - 1).bit_length()
    report = {
        "status": ("EXACT_FINITE_BANK_MESSAGE_MINIMUM" if exact
                   else "FEASIBLE_COLORING_NOT_PROVEN_MINIMUM"),
        "history_count": n,
        "transcript_group_count": gcount,
        "exact_transcript_ids": groups,
        "messages_by_history": [colors[c] for c in by_history],
        "messages_by_transcript": colors,
        "conflicting_history_pair_count": len(conflict_pairs),
        "edge_count": sum(len(x) for x in neighbors) // 2,
        "max_clique_lower_bound": lower,
        "message_lower_bound": lower,
        "message_upper_bound": upper,
        "bit_lower_bound": bits(lower),
        "bit_upper_bound": bits(upper),
        "minimum_messages": upper if exact else None,
        "minimum_retained_bits": bits(upper) if exact else None,
        "exact_optimum_proven": exact,
        "scope": ("Finite predeclared legal histories/goals, exact archived transcript "
                  "categories, independent side-observation interval coordinates, "
                  "deterministic per-goal tolerance and fixed-length messages; "
                  "float comparisons, no native DPT or Gaussian streaming theorem."),
    }
    return report


def decode_retained_goal(
    side_observation, retained_message, report, observations, goals, *,
    observation_radii, goal_tolerances, goal_uncertainty=None,
):
    """Construct an admissible interval-center goal readout for a valid coloring."""
    o = np.asarray(observations, dtype=float)
    g = np.asarray(goals, dtype=float)
    if o.ndim != 2 or g.ndim != 2 or o.shape[0] != g.shape[0] or g.shape[1] < 1:
        raise ValueError("invalid observation/goal matrices")
    n, m = o.shape
    q = g.shape[1]
    if report.get("status") not in {
        "EXACT_FINITE_BANK_MESSAGE_MINIMUM", "FEASIBLE_COLORING_NOT_PROVEN_MINIMUM"
    }:
        raise ValueError("no feasible retained-message encoder in report")
    y = _array(side_observation, (m,), "side_observation")
    rad = _array(observation_radii, (m,), "observation_radii", nonnegative=True)
    tau = _array(goal_tolerances, (q,), "goal_tolerances", nonnegative=True)
    eta = (np.zeros((n, q)) if goal_uncertainty is None
           else _array(goal_uncertainty, (n, q), "goal_uncertainty", nonnegative=True))
    codes = report["messages_by_history"]
    if len(codes) != n or not isinstance(retained_message, (int, np.integer)):
        raise ValueError("invalid codeword or incompatible report")
    indices = [i for i in range(n)
               if codes[i] == retained_message and np.all(abs(o[i] - y) <= rad)]
    if not indices:
        raise ValueError("no declared source history compatible with message and live observation")
    low = np.max(g[indices] + eta[indices] - tau[None, :], axis=0)
    high = np.min(g[indices] - eta[indices] + tau[None, :], axis=0)
    if np.any(low > high):
        raise RuntimeError("decoded interval empty: invalid coloring or altered input contract")
    return (low + high) / 2



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="NPZ bank and declared observation/error contracts")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--exact-candidate-cap", type=int, default=18)
    parser.add_argument("--retained-goal-bits", action="store_true",
                        help="Exact/qualified finite-bank memory bits with later side observation")
    parser.add_argument("--exact-transcript-cap", type=int, default=17)
    args = parser.parse_args()
    with np.load(args.input, allow_pickle=False) as data:
        if args.retained_goal_bits:
            required = ["observations", "goals", "transcript_ids",
                        "observation_radii", "goal_tolerances"]
            missing = [x for x in required if x not in data.files]
            if missing:
                parser.error("missing retained-goal-bits NPZ fields: " + ", ".join(missing))
            report = audit_retained_goal_bits(
                data["observations"], data["goals"],
                [str(x) for x in data["transcript_ids"]],
                observation_radii=data["observation_radii"],
                goal_tolerances=data["goal_tolerances"],
                goal_uncertainty=(data["goal_uncertainty"]
                                  if "goal_uncertainty" in data.files else None),
                exact_transcript_cap=args.exact_transcript_cap)
        else:
            fields = ["observations", "goals", "candidates", "observation_radii",
                      "candidate_radii", "goal_tolerances", "candidate_costs"]
            missing = [x for x in fields if x not in data.files]
            if missing:
                parser.error("missing NPZ fields: " + ", ".join(missing))
            optional = {field: data[field] if field in data.files else None
                        for field in ["goal_uncertainty", "candidate_names", "command_names"]}
            report = audit(
                data["observations"], data["goals"], data["candidates"],
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
