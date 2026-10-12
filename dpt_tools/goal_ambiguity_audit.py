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



def gaussian_replicate_goal_pair(
    observed_means, future_goals, *, goal_tolerance,
    independent_sigma, shared_sigma, failure_probability,
):
    """Exact MINIMAX repeat count for two legal histories under common Gaussian drift.

    Given hypothesis h in {0,1}, each repeat of a genuinely reproducible
    PRETARGET sensor returns y_r = observed_means[h] + U + eps_r.
    U ~ N(0,shared_sigma**2) is shared across repeats in one campaign;
    eps_r are iid N(0,independent_sigma**2). Both laws share these
    known variances. The future scalar G_h is FIXED but never observed
    before prediction. A possibly randomized decoder must achieve
    |Ghat - G_h| <= goal_tolerance under EACH law with probability
    >= 1 - failure_probability.

    No equipment reference, physical noise calibration, independent
    preparation, source-law validation or multi-history minimax is
    established by this mathematical two-hypothesis report.
    """
    from statistics import NormalDist
    import math

    mu = np.asarray(observed_means, dtype=float)
    target = np.asarray(future_goals, dtype=float)
    if (mu.shape != (2,) or target.shape != (2,)
            or not np.all(np.isfinite(mu)) or not np.all(np.isfinite(target))):
        raise ValueError("observed_means and future_goals must be finite two-element vectors")
    tol = _radius(goal_tolerance, "goal_tolerance")
    within = _radius(independent_sigma, "independent_sigma")
    common = _radius(shared_sigma, "shared_sigma")
    alpha = float(failure_probability)
    if not np.isfinite(alpha) or not (0 < alpha < .5) or 1 - alpha >= 1:
        raise ValueError("failure_probability must be in (0,0.5) and resolvable in float64")
    delta = float(abs(mu[0] - mu[1]))
    goal_gap = float(abs(target[0] - target[1]))
    normal = NormalDist()

    def error(m):
        if m == 0:
            return .5
        variance = common * common + within * within / m
        if variance == 0:
            return 0. if delta > 0 else .5
        return float(normal.cdf(-delta / (2 * math.sqrt(variance))))

    floor = (0. if delta > 0 and common == 0 else
             float(normal.cdf(-delta / (2 * common))) if common > 0
             else .5)
    base = {
        "model": "TWO_LEGAL_HISTORY_SAME_VARIANCE_GAUSSIAN_REPEAT_TEST",
        "source_law_status": "CONDITIONAL_MATHEMATICAL_ONLY",
        "goal_gap": goal_gap,
        "goal_tolerance": tol,
        "sensor_mean_gap": delta,
        "independent_sigma": within,
        "shared_sigma": common,
        "failure_probability": alpha,
        "single_repeat_failure": error(1),
        "asymptotic_failure_floor": floor,
        "minimum_repeats": None,
        "minimax_failure_at_repeats": None,
        "minimax_failure_at_previous_repeats": None,
        "boundary": ("Repeated identical legal preparation and frozen future scalar goal;"
                     " one Gaussian offset common to all repetitions plus independent"
                     " Gaussian per-repeat noise. No nuisance estimation from future"
                     " outcomes. No hardware/state validity or source-law uncertainty certificate."),
    }
    if goal_gap <= 2 * tol:
        return dict(base, status="GOAL_WITHIN_TOLERANCE_WITHOUT_SENSING",
                    minimum_repeats=0, minimax_failure_at_repeats=0.,
                    minimax_failure_at_previous_repeats=None)
    if delta == 0:
        return dict(base, status="IDENTICAL_SENSOR_LAWS")
    z = float(normal.inv_cdf(1 - alpha))
    max_allowed_variance = (delta / (2 * z)) ** 2
    if (common * common > max_allowed_variance or
            (within > 0 and common * common >= max_allowed_variance)):
        return dict(base, status="SHARED_NUISANCE_INFORMATION_FLOOR")
    if within == 0:
        count = 1
    else:
        remaining = max_allowed_variance - common * common
        if remaining <= 0:
            return dict(base, status="SHARED_NUISANCE_INFORMATION_FLOOR")
        required_float = (within * within) / remaining
        if not np.isfinite(required_float) or required_float >= 1e15:
            return dict(base, status="NUMERICALLY_UNRESOLVED_REPEAT_COUNT")
        count = max(1, math.ceil(required_float))
        # Guard rounding at exact integer thresholds, checking achieved error.
        while error(count) > alpha:
            count += 1
        while count > 1 and error(count - 1) <= alpha:
            count -= 1
    return dict(base, status="EXACT_GAUSSIAN_MINIMAX_REPEAT_COUNT",
                minimum_repeats=int(count),
                minimax_failure_at_repeats=error(count),
                minimax_failure_at_previous_repeats=error(count - 1))



def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="NPZ with finite-bank or paired Gaussian history data")
    parser.add_argument("--observation-noise-radius", type=float,
                        help="Required for the legacy bounded Euclidean-noise audit")
    parser.add_argument("--candidate-noise-radius", type=float, default=0.0)
    parser.add_argument("--gaussian-repeat-goal", action="store_true",
                        help="Separate two-history repeated-noise goal-testing model")
    parser.add_argument("--output", type=Path)
    a = parser.parse_args()
    with np.load(a.input, allow_pickle=False) as data:
        if a.gaussian_repeat_goal:
            fields = ["observed_means", "future_goals", "goal_tolerance",
                      "independent_sigma", "shared_sigma", "failure_probability"]
            absent = [k for k in fields if k not in data.files]
            if absent:
                parser.error("missing Gaussian-repeat NPZ arrays: " + ", ".join(absent))
            scalar = {k: float(data[k].item()) for k in fields[2:]}
            result = gaussian_replicate_goal_pair(
                data["observed_means"], data["future_goals"], **scalar)
        else:
            if a.observation_noise_radius is None:
                parser.error("--observation-noise-radius is required for the finite-bank audit")
            if "observations" not in data.files or "goals" not in data.files:
                parser.error("NPZ requires observations and goals")
            result = audit(
                data["observations"], data["goals"], a.observation_noise_radius,
                candidates=data["candidates"] if "candidates" in data.files else None,
                candidate_noise_radius=a.candidate_noise_radius,
                candidate_names=[str(z) for z in data["candidate_names"]]
                if "candidate_names" in data.files else None)
    body = json.dumps(result, indent=2, sort_keys=True)
    if a.output:
        a.output.write_text(body + "\n", encoding="utf-8")
    else:
        print(body)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
