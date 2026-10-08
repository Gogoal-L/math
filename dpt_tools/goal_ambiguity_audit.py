#!/usr/bin/env python3
"""Deterministic scalar-goal minimax error for a finite history bank.

For observation noise in a known Euclidean ball of radius sigma, two
histories are indistinguishable if their observation distance is <= 2*sigma.
The minimax uniform scalar-goal error on THIS FINITE BANK is half the largest
goal gap between indistinguishable histories. It is a LOWER bound for any
larger physical history class containing the bank; no Bayesian/noise law or
finite-radius native certificate is claimed.

Observation columns must already have compatible scales or be whitened.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np


def _matrix(value, name: str) -> np.ndarray:
    a = np.asarray(value, dtype=float)
    if a.ndim != 2 or a.shape[0] < 1 or not np.all(np.isfinite(a)):
        raise ValueError(f"{name} must be a finite nonempty 2D array")
    return a


def _radius(x: float, name: str) -> float:
    x = float(x)
    if not np.isfinite(x) or x < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return x


def _score(goals: np.ndarray, indistinguishable: np.ndarray) -> dict:
    gaps = np.abs(goals[:, None] - goals[None, :])
    masked = np.where(indistinguishable, gaps, -1.0)
    i, j = np.unravel_index(int(np.argmax(masked)), masked.shape)
    return {
        "goal_diameter": float(gaps[i, j]),
        "minimax_scalar_error": float(gaps[i, j] / 2),
        "witness_indices": [int(i), int(j)],
        "indistinguishable_unordered_pairs": int((np.count_nonzero(indistinguishable) - len(goals)) // 2),
    }


def _empirical_gain(observations: np.ndarray, goals: np.ndarray):
    """Exact pairwise scalar-goal gain on this bank, not whole-class stability."""
    gain = 0.0
    for i in range(len(goals)):
        for j in range(i + 1, len(goals)):
            gap = abs(float(goals[i] - goals[j]))
            distance = float(np.linalg.norm(observations[i] - observations[j]))
            if distance == 0.0:
                if gap > 0.0:
                    return "INF_GOAL_COLLISION"
            else:
                gain = max(gain, gap / distance)
    return gain


def audit(observations, goals, observation_noise_radius: float, *,
          candidates=None, candidate_noise_radius: float = 0.0,
          candidate_names=None) -> dict:
    obs = _matrix(observations, "observations")
    goal = np.asarray(goals, dtype=float)
    if goal.ndim != 1 or goal.size != obs.shape[0] or not np.all(np.isfinite(goal)):
        raise ValueError("goals must be a finite scalar vector aligned with observations")
    sig_o = _radius(observation_noise_radius, "observation_noise_radius")
    sig_p = _radius(candidate_noise_radius, "candidate_noise_radius")
    delta = obs[:, None, :] - obs[None, :, :]
    common_o = np.linalg.norm(delta, axis=-1) <= (2 * sig_o)
    np.fill_diagonal(common_o, True)
    baseline = _score(goal, common_o)
    result = {
        "schema_version": 1,
        "number_of_histories": int(obs.shape[0]),
        "observation_noise_radius": sig_o,
        "empirical_scalar_goal_lipschitz_gain": _empirical_gain(obs, goal),
        "baseline": baseline,
        "claim_ceiling": (
            "Exact deterministic minimax scalar-goal error on the supplied finite bank, "
            "under bounded Euclidean observation noise. For a larger admissible history "
            "class, the result is only a lower bound. Inputs require common unit/scale conventions."
        ),
    }
    if candidates is None:
        return result
    p = _matrix(candidates, "candidates")
    if p.shape[0] != obs.shape[0]:
        raise ValueError("candidates rows must match observations")
    if candidate_names is None:
        candidate_names = [f"candidate_{i}" for i in range(p.shape[1])]
    if len(candidate_names) != p.shape[1]:
        raise ValueError("candidate_names count must match candidate columns")
    report = []
    for j, name in enumerate(candidate_names):
        cdist = np.abs(p[:, None, j] - p[None, :, j])
        same = common_o & (cdist <= 2 * sig_p)
        score = _score(goal, same)
        report.append({"index": j, "name": str(name), **score})
    result["candidate_noise_radius"] = sig_p
    result["candidates"] = report
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="NPZ containing observations (N,m), goals (N,), optional candidates (N,p) and candidate_names")
    parser.add_argument("--observation-noise-radius", type=float, required=True)
    parser.add_argument("--candidate-noise-radius", type=float, default=0.0)
    parser.add_argument("--output", type=Path)
    a = parser.parse_args()
    with np.load(a.input, allow_pickle=False) as data:
        if "observations" not in data.files or "goals" not in data.files:
            parser.error("NPZ requires observations and goals")
        result = audit(data["observations"], data["goals"], a.observation_noise_radius,
                       candidates=data["candidates"] if "candidates" in data.files else None,
                       candidate_noise_radius=a.candidate_noise_radius,
                       candidate_names=[str(z) for z in data["candidate_names"]] if "candidate_names" in data.files else None)
    body = json.dumps(result, indent=2, sort_keys=True)
    if a.output:
        a.output.write_text(body + "\n", encoding="utf-8")
    else:
        print(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
