#!/usr/bin/env python3
"""Finite-bank scalar goal stability with box-noisy features and a fixed gain limit.

For each fixed future command, computes the EXACT minimax error among globally
K-Lipschitz real-valued decoders on the supplied finite-bank observation boxes.
Selects a minimum-price subset of declared pretarget scalar features when the
candidate count permits exhaustive search. No native DPT or future-word closure
claim follows from a synthetic/finite-bank pass.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


def _arr(value, name, ndim, *, nonnegative=False, positive=False):
    a = np.asarray(value, dtype=float)
    if a.ndim != ndim or not np.all(np.isfinite(a)):
        raise ValueError(f"{name} must be a finite {ndim}D array")
    if nonnegative and np.any(a < 0):
        raise ValueError(f"{name} must be nonnegative")
    if positive and np.any(a <= 0):
        raise ValueError(f"{name} must be strictly positive")
    return a


def _gain_needed(distance, target_gaps, goal_uncertainties, tolerance):
    """Minimum feasible scalar decoder gain at the requested tolerance."""
    if np.any(goal_uncertainties > tolerance):
        return "INF"
    numerator = target_gaps + goal_uncertainties - 2 * tolerance
    positive = numerator > 0
    if np.any(positive & (distance == 0)):
        return "INF"
    if not np.any(positive):
        return 0.0
    return float(np.max(numerator[positive] / distance[positive]))


def decoder_value(readout, centers, radii, goals, goal_uncertainty, error_radius, gain):
    """Explicit scalar McShane-Whitney envelope midpoint for a given input readout.

    Guaranteed on declared finite-bank boxes ONLY when error_radius is at
    least the exact risk for the same scalar goal, noise and gain contract.
    """
    x = _arr(readout, "readout", 1)
    c = _arr(centers, "centers", 2)
    r = _arr(radii, "radii", 1, nonnegative=True)
    g = _arr(goals, "goals", 1)
    eta = _arr(goal_uncertainty, "goal_uncertainty", 1, nonnegative=True)
    if c.shape[0] < 1 or c.shape[1] != x.size or r.shape != (x.size,) or g.shape != (len(c),) or eta.shape != g.shape:
        raise ValueError("inconsistent decoder center/readout/goal dimensions")
    eps = float(error_radius)
    gain = float(gain)
    if not np.isfinite(eps) or eps < 0 or not np.isfinite(gain) or gain < 0:
        raise ValueError("error_radius and gain must be finite nonnegative")
    dist = np.linalg.norm(np.maximum(np.abs(c - x) - r, 0.), axis=1)
    lower = float(np.max(g + eta - eps - gain * dist))
    upper = float(np.min(g - eta + eps + gain * dist))
    if lower > upper + 1e-10 * max(1., abs(lower), abs(upper)):
        raise ValueError("inconsistent Lipschitz envelope: supplied radius is insufficient")
    return (lower + upper) / 2.



def transition_pair_floor(current_states, next_states, update_lipschitz):
    """Necessary uniform next-state closure-defect floor on matched legal pairs.

    The same command and qualified physical transition must be used for
    EVERY row. This pairwise lower bound is NOT sufficient for a global
    vector-valued Lipschitz update to exist or have the same defect.
    """
    x = _arr(current_states, "current_states", 2)
    xp = _arr(next_states, "next_states", 2)
    gain = float(update_lipschitz)
    if not np.isfinite(gain) or gain < 0:
        raise ValueError("update_lipschitz must be finite nonnegative")
    if len(x) < 1 or x.shape != xp.shape or x.shape[1] < 1:
        raise ValueError("current and next states must have the same nonempty shape")
    ii, jj = np.triu_indices(len(x), k=1)
    if not len(ii):
        return {"status":"NECESSARY_PAIR_FLOOR_ONLY",
                "minimum_uniform_update_defect_lower_bound":0.,
                "witness_indices":None}
    separation = np.linalg.norm(xp[ii] - xp[jj],axis=1)
    permitted = gain*np.linalg.norm(x[ii] - x[jj],axis=1)
    residual = np.maximum(separation - permitted, 0.) / 2.
    if not np.all(np.isfinite(residual)):
        raise ValueError("nonfinite pair comparison; rescale coordinates")
    loc=int(np.argmax(residual))
    return {"status":"NECESSARY_PAIR_FLOOR_ONLY",
            "minimum_uniform_update_defect_lower_bound":float(residual[loc]),
            "witness_indices":[int(ii[loc]),int(jj[loc])],
            "target_separation":float(separation[loc]),
            "current_separation":float(np.linalg.norm(x[ii[loc]]-x[jj[loc]])),
            "update_lipschitz":gain}


def audit(observations, goals, candidates, *, observation_radii,
          candidate_radii, goal_uncertainty, goal_tolerances,
          lipschitz_limits, candidate_costs, candidate_names=None,
          command_names=None, exact_cap=18):
    """Exact finite-bank robust K-Lipschitz goal radius and feature-price search.

    Separate columns use independent *admissible intervals*, not independent
    random noise. The stable decoder is real-valued per fixed command; the
    selected feature set is common across commands. No optimizer is fitted.
    """
    obs = _arr(observations, "observations", 2)
    cand = _arr(candidates, "candidates", 2)
    g = np.asarray(goals, dtype=float)
    if g.ndim == 1:
        g = g[:, None]
    g = _arr(g, "goals", 2)
    if obs.shape[0] < 1 or g.shape[1] < 1 or cand.shape[0] != obs.shape[0] or g.shape[0] != obs.shape[0]:
        raise ValueError("bank must have >=1 history and >=1 goal, with aligned rows")
    n, m = obs.shape
    p, k = cand.shape[1], g.shape[1]
    ro = _arr(observation_radii, "observation_radii", 1, nonnegative=True)
    rp = _arr(candidate_radii, "candidate_radii", 1, nonnegative=True)
    eta = _arr(goal_uncertainty, "goal_uncertainty", 2, nonnegative=True)
    tau = _arr(goal_tolerances, "goal_tolerances", 1, nonnegative=True)
    gain = _arr(lipschitz_limits, "lipschitz_limits", 1, nonnegative=True)
    cost = _arr(candidate_costs, "candidate_costs", 1, positive=True)
    if ro.shape != (m,) or rp.shape != (p,) or eta.shape != (n,k) or tau.shape != (k,) or gain.shape != (k,) or cost.shape != (p,):
        raise ValueError("radii, uncertainty, tolerance, gain and candidate costs have incompatible shapes")
    if not isinstance(exact_cap, int) or exact_cap < 0 or exact_cap > 22:
        raise ValueError("exact_cap must be an integer from 0 to 22")
    def names(values, length, prefix):
        if values is None:
            return [f"{prefix}_{j}" for j in range(length)]
        if len(values) != length or len(set(str(v) for v in values)) != length:
            raise ValueError(f"{prefix} names must be unique and correctly sized")
        return [str(v) for v in values]
    pn = names(candidate_names, p, "candidate")
    cn = names(command_names, k, "command")
    ii, jj = np.triu_indices(n, k=1)
    o_gap = np.maximum(np.abs(obs[ii] - obs[jj]) - 2 * ro, 0.)
    p_gap = np.maximum(np.abs(cand[ii] - cand[jj]) - 2 * rp, 0.)
    base_d2 = np.einsum("ij,ij->i", o_gap, o_gap)
    add_d2 = p_gap * p_gap
    pair_gaps = np.abs(g[ii] - g[jj]) + eta[ii] + eta[jj]
    eta_max = np.max(eta, axis=0)
    if not np.all(np.isfinite(base_d2)) or not np.all(np.isfinite(add_d2)) or not np.all(np.isfinite(pair_gaps)):
        raise ValueError("overflow in finite-bank differences; normalize inputs")

    def risk(distance_sq):
        if len(ii) == 0:
            return eta_max.copy()
        d = np.sqrt(distance_sq)
        rad = np.max((pair_gaps - gain * d[:,None]) / 2., axis=0)
        return np.maximum(rad, eta_max)

    def kmin(distance_sq):
        d = np.sqrt(distance_sq)
        out=[]
        for c in range(k):
            num = pair_gaps[:,c]
            # Objective includes self-interval: this is a hard lower floor.
            if eta_max[c] > tau[c]:
                out.append("INF")
            else:
                out.append(_gain_needed(d, num, np.zeros_like(num), tau[c]))
        return out

    def report_base(status, selected=None, kind=None):
        b = risk(base_d2)
        full_sq = base_d2 + np.sum(add_d2,axis=1)
        full = risk(full_sq)
        take = [] if selected is None else list(selected)
        r = risk(base_d2 + (np.sum(add_d2[:,take],axis=1) if take else 0.)) if selected is not None else None
        return {
            "schema_version": 1,
            "model_type": "FINITE_BANK_SCALAR_K_LIPSCHITZ_BOX_NOISE",
            "status": status,
            "number_of_histories": n,
            "number_of_commands": k,
            "command_names": cn,
            "candidate_names": pn,
            "lipschitz_limits": gain.tolist(),
            "goal_tolerances": tau.tolist(),
            "baseline_radii": b.tolist(),
            "all_feature_radii": full.tolist(),
            "selected_radii": None if r is None else r.tolist(),
            "minimum_required_gain_before": kmin(base_d2),
            "minimum_required_gain_all_features": kmin(full_sq),
            "selected_indices": take,
            "selected_names": [pn[j] for j in take],
            "selected_cost": float(math.fsum(cost[take])) if selected is not None else None,
            "optimality": kind,
            "claim_ceiling": (
                "Exact best scalar K-Lipschitz decoder radius for the supplied finite bank, "
                "independent coordinatewise interval input uncertainty and independent goal "
                "intervals; no physical, all-reachable, hardware, autonomous state, or "
                "multi-word qualification follows without externally validated provenance. "
                "Cost optimality means only a fixed candidate library and floating inputs."
            ),
        }

    baseline = risk(base_d2)
    if np.all(baseline <= tau):
        return report_base("BASELINE_SUFFICIENT", selected=[], kind="EXACT_NO_REPAIR")
    if np.any(eta_max > tau):
        return report_base("INTRINSIC_GOAL_UNCERTAINTY")
    full_sq = base_d2 + np.sum(add_d2,axis=1)
    if not np.all(risk(full_sq) <= tau):
        return report_base("NO_LIBRARY_STABLE_REPAIR")

    def sufficient(d2):
        return bool(np.all(risk(d2) <= tau))

    # Positive-price squared-distance contributions permit lower-cost pruning.
    # Feasibility is finally evaluated in ORIGINAL unsquared goal units.
    remaining = np.zeros((p+1,len(ii)))
    for j in range(p-1,-1,-1):
        remaining[j] = remaining[j+1] + add_d2[:,j]

    # Strict cost ordering retains tiny positive differences; comparisons are
    # numerical over the supplied float values, not exact symbolic arithmetic.
    best_cost = float(math.fsum(cost))
    best_choice = list(range(p))
    if p <= exact_cap:
        def visit(j, chosen, cum_cost, d2):
            nonlocal best_cost, best_choice
            if sufficient(d2):
                if (cum_cost,len(chosen),chosen) < (best_cost,len(best_choice),best_choice):
                    best_cost, best_choice = cum_cost, chosen.copy()
                return
            if j >= p or cum_cost >= best_cost:
                return
            if not sufficient(d2 + remaining[j]):
                return
            visit(j+1, chosen, cum_cost, d2)
            if cum_cost + cost[j] <= best_cost:
                visit(j+1, chosen+[j], float(math.fsum([cum_cost,float(cost[j])])),d2+add_d2[:,j])
        visit(0, [], 0., base_d2.copy())
        return report_base("EXACT_MIN_COST_STABLE_REPAIR", best_choice, "EXHAUSTIVE_BRANCH_AND_BOUND")

    # For large libraries, cost-weighted squared-separation deficit is merely
    # a selection heuristic; it has no asserted set-cover approximation ratio.
    selected=[]
    current=base_d2.copy()
    unused=set(range(p))
    needed = np.zeros(len(ii))
    for c in range(k):
        stress = np.maximum(pair_gaps[:,c] - 2*tau[c], 0.)
        if gain[c] > 0:
            needed = np.maximum(needed,(stress/gain[c])**2)
    if not np.all(np.isfinite(needed)):
        raise ValueError("gain-scaled required separations overflow; normalize inputs")
    while not sufficient(current):
        deficit = np.maximum(needed-current,0.)
        choices=[]
        for j in sorted(unused):
            improvement=float(np.sum(np.minimum(deficit,add_d2[:,j])))/float(cost[j])
            choices.append((improvement,-j,j))
        if not choices:
            raise ValueError("internal error: full candidate library was feasible")
        pick = max(choices)[2]
        selected.append(pick)
        unused.remove(pick)
        current += add_d2[:,pick]
        if len(selected)>p:
            raise AssertionError("feature selection did not terminate")
    selected.sort()
    return report_base("GREEDY_FEASIBLE_NOT_PROVEN_MINIMUM",selected,"FEASIBLE_ONLY")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path,help="NPZ bank: observations, goals, candidates, radii, uncertainties, gains, tolerances, costs")
    parser.add_argument("--output",type=Path)
    parser.add_argument("--exact-cap",type=int,default=18)
    a = parser.parse_args()
    required = ["observations","goals","candidates","observation_radii","candidate_radii","goal_uncertainty","goal_tolerances","lipschitz_limits","candidate_costs"]
    with np.load(a.input, allow_pickle=False) as data:
        absent = [x for x in required if x not in data.files]
        if absent:
            parser.error("missing NPZ arrays: "+", ".join(absent))
        opts = {key:data[key] for key in required}
        for key in ("candidate_names","command_names"):
            if key in data.files:
                opts[key] = [str(z) for z in data[key]]
        rep = audit(**opts,exact_cap=a.exact_cap)
    s = json.dumps(rep,indent=2,sort_keys=True,allow_nan=False)
    if a.output:
        a.output.write_text(s+"\n",encoding="utf-8")
    else:
        print(s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
