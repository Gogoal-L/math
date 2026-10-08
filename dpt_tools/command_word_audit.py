#!/usr/bin/env python3
"""Exact future-goal/definedness quotient of a FINITE partial command model.

This is partition refinement / Myhill-Nerode-style equivalence, not a
proof about native LTspice, continuous switching commands, or unbounded
history spaces. It detects distinguishable current-observation aliases.
"""
from __future__ import annotations

import argparse
from collections import deque
import json
from pathlib import Path


def _key(value) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _model(raw):
    if not isinstance(raw, dict) or not isinstance(raw.get("states"), dict) or not raw["states"]:
        raise ValueError("states must be a nonempty state dictionary")
    cmds = raw.get("commands")
    if not isinstance(cmds, list) or len(set(cmds)) != len(cmds) or not all(isinstance(c, str) and c for c in cmds):
        raise ValueError("commands must be unique nonempty strings")
    states = raw["states"]
    for name, entry in states.items():
        if not isinstance(name, str) or not isinstance(entry, dict) or "goal" not in entry:
            raise ValueError("every state needs a name and goal")
        transitions = entry.get("transitions", {})
        if not isinstance(transitions, dict) or any(c not in cmds for c in transitions):
            raise ValueError(f"invalid command at {name}")
        for cmd, dst in transitions.items():
            if dst is not None and dst not in states:
                raise ValueError(f"unknown transition target {dst!r} at {name}/{cmd}")
    return states, cmds


def _step(states: dict, state: str, command: str):
    return states[state].get("transitions", {}).get(command)


def _witness(states: dict, commands: list, a: str, b: str) -> dict:
    todo = deque([(a, b, [])])
    seen = {(a, b)}
    while todo:
        x, y, word = todo.popleft()
        if _key(states[x]["goal"]) != _key(states[y]["goal"]):
            return {"word": word, "kind": "goal", "endpoint_states": [x, y]}
        for c in commands:
            dx, dy = _step(states, x, c), _step(states, y, c)
            if (dx is None) != (dy is None):
                return {"word": word + [c], "kind": "definedness", "endpoint_states": [dx, dy]}
            if dx is None:
                continue
            if (dx, dy) not in seen:
                seen.add((dx, dy))
                todo.append((dx, dy, word + [c]))
    raise AssertionError("pair expected distinguishable but no distinguishing word found")


def audit(raw: dict, *, max_witnesses: int = 100) -> dict:
    states, commands = _model(raw)
    if max_witnesses < 0:
        raise ValueError("max_witnesses must be nonnegative")
    names = sorted(states)
    classes = {}
    for name in names:
        classes[name] = _key(states[name]["goal"])

    # Stable signatures refine the goal partition until future commands
    # preserve each class; classes are then a right congruence.
    refinements = 0
    while True:
        signatures = {}
        for name in names:
            successors = tuple(("U" if _step(states, name, c) is None
                                else classes[_step(states, name, c)]) for c in commands)
            signatures[name] = (classes[name], successors)
        known = {}
        next_classes = {}
        for name in names:
            sig = signatures[name]
            if sig not in known:
                known[sig] = len(known)
            next_classes[name] = known[sig]
        refinements += 1
        if all(classes[x] == classes[y] for x in names for y in names if next_classes[x] == next_classes[y]) and (
            all(next_classes[x] == next_classes[y] for x in names for y in names if classes[x] == classes[y])
        ):
            classes = next_classes
            break
        classes = next_classes
        if refinements > len(names) + 1:
            raise AssertionError("finite partition refinement did not terminate")

    partitions = {}
    for name in names:
        partitions.setdefault(classes[name], []).append(name)
    observations = {}
    for name in names:
        observations.setdefault(_key(states[name].get("observation")), []).append(name)
    witnesses = []
    total = 0
    for group in observations.values():
        for i, a in enumerate(group):
            for b in group[i + 1:]:
                if classes[a] != classes[b]:
                    total += 1
                    if len(witnesses) < max_witnesses:
                        witnesses.append({"states": [a, b], **_witness(states, commands, a, b)})
    return {
        "schema_version": 1,
        "state_count": len(names),
        "minimal_classes": len(partitions),
        "classes": [members for _, members in sorted(partitions.items())],
        "state_to_class": classes,
        "refinement_rounds": refinements,
        "current_observation_alias_pairs_distinguishable": total,
        "observation_alias_witnesses": witnesses,
        "witness_truncated": total > len(witnesses),
        "claim_ceiling": (
            "Exact future-word goal/definedness quotient on this explicitly enumerated "
            "finite partial deterministic transition system only. No native or continuous-class conclusion."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON with states, goals, optional observations, and partial command transitions")
    parser.add_argument("--max-witnesses", type=int, default=100)
    parser.add_argument("--output", type=Path)
    a = parser.parse_args()
    result = audit(json.loads(a.input.read_text(encoding="utf-8")), max_witnesses=a.max_witnesses)
    output = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)
    if a.output:
        a.output.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
