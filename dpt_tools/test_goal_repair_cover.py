"""Known-answer and independent enumeration tests for deterministic box-noise feature cover."""
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np

import goal_repair_cover as grc


class RepairCoverTests(unittest.TestCase):
    def _run(self, obs, goals, candidates, so, sp, tau, costs, **kwargs):
        return grc.audit(obs, goals, candidates, observation_radii=so,
                         candidate_radii=sp, goal_tolerances=tau,
                         candidate_costs=costs, **kwargs)

    def _three_pairs(self, costs=(1., 1., 10.), **kw):
        # Only three pairs share base observation; A covers 0,1; B 1,2; C 0,2.
        obs = np.repeat([[0.], [10.], [20.]], 2, axis=0)
        goals = np.tile([[0., 0.], [4., 6.]], (3, 1))
        candidates = np.array([[0, 0, 0], [1, 0, 1],
                               [0, 0, 0], [1, 1, 0],
                               [0, 0, 0], [0, 1, 1]], dtype=float)
        return self._run(obs, goals, candidates, [0], [0, 0, 0], [1, 2],
                         costs, candidate_names=['A', 'B', 'C'],
                         command_names=['pulseA', 'pulseB'], **kw)

    def test_three_conflicts_need_two_features_and_match_hand_solution(self):
        r = self._three_pairs()
        self.assertEqual(r['status'], 'EXACT_MIN_COST_REPAIR')
        self.assertEqual(r['goal_conflict_pair_count'], 3)
        self.assertEqual(r['selected_names'], ['A', 'B'])
        self.assertEqual(r['baseline_minimax_error_by_command'], [2, 3])
        self.assertEqual(r['selected_minimax_error_by_command'], [0, 0])
        self.assertAlmostEqual(r['total_cost'], 2)

    def test_cost_weighted_solution_is_not_minimum_cardinality_preference(self):
        r = self._three_pairs(costs=(1, 1, .2))
        self.assertEqual(r['status'], 'EXACT_MIN_COST_REPAIR')
        self.assertEqual(len(r['selected_indices']), 2)
        self.assertIn('C', r['selected_names'])
        self.assertAlmostEqual(r['total_cost'], 1.2)

    def test_goal_interval_uncertainty_makes_nominally_safe_pair_conflict(self):
        r = self._run([[0], [0]], [[0], [1]], [[0], [2]], [0], [0.1], [1], [1],
                      goal_uncertainty=[[.6], [.6]])
        self.assertEqual(r['baseline_minimax_error_by_command'], [1.1])
        self.assertEqual(r['selected_minimax_error_by_command'], [.6])
        self.assertEqual(r['status'], 'EXACT_MIN_COST_REPAIR')

    def test_self_uncertainty_cannot_be_repaired_even_with_perfect_feature(self):
        r = self._run([[0]], [[1]], [[0]], [0], [0], [1], [1],
                      goal_uncertainty=[[1.1]])
        self.assertEqual(r['status'], 'INTRINSIC_GOAL_UNCERTAINTY')
        self.assertEqual(r['history'], 0)

    def test_just_touching_noise_intervals_are_indistinguishable(self):
        r = self._run([[0], [0]], [[0], [4]], [[0], [1]], [0], [.5], [1], [1])
        self.assertEqual(r['status'], 'NO_LIBRARY_REPAIR')
        self.assertEqual(r['uncovered_history_pair'], [0, 1])

    def test_box_noise_is_not_joint_euclidean_noise(self):
        # Two 0.8 gaps are each below 2*0.5, but Euclidean norm exceeds 1.
        r = self._run([[0], [0]], [[0], [4]], [[0, 0], [.8, .8]], [0], [.5, .5], [1], [1, 1])
        self.assertEqual(r['status'], 'NO_LIBRARY_REPAIR')

    def test_goal_gap_equal_to_double_tolerance_is_safe(self):
        r = self._run([[0], [0]], [[0], [2]], np.zeros((2, 0)), [0], [], [1], [])
        self.assertEqual(r['status'], 'NO_REPAIR_NEEDED')
        self.assertEqual(r['baseline_minimax_error_by_command'], [1.0])

    def test_no_cross_command_leak_from_nonbinding_command(self):
        r = self._run([[0], [0]], [[0, 0], [0, 5]], [[0], [1]], [0], [0], [1, 1], [1],
                      command_names=['benign', 'difficult'])
        self.assertEqual(r['status'], 'EXACT_MIN_COST_REPAIR')
        self.assertEqual(r['baseline_minimax_error_by_command'], [0, 2.5])

    def test_many_candidates_greedy_is_feasible_not_misreported_exact(self):
        r = self._three_pairs(exact_candidate_cap=1)
        self.assertEqual(r['status'], 'GREEDY_FEASIBLE_NOT_PROVEN_MINIMUM')
        self.assertFalse(r['minimum_cost_proven_within_candidate_library'])
        self.assertEqual(r['selected_minimax_error_by_command'], [0, 0])

    def test_bad_shapes_and_nonfinite_inputs_rejected(self):
        cases = [
            dict(observation_radii=[-1], candidate_radii=[0], goal_tolerances=[1], candidate_costs=[1]),
            dict(observation_radii=[0], candidate_radii=[0], goal_tolerances=[1], candidate_costs=[0]),
            dict(observation_radii=[0], candidate_radii=[-1], goal_tolerances=[1], candidate_costs=[1]),
        ]
        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    grc.audit([[0], [0]], [[0], [4]], [[0], [2]], **case)
        with self.assertRaises(ValueError):
            self._run([[0]], [[np.inf]], [[0]], [0], [0], [1], [1])
        with self.assertRaises(ValueError):
            self._run([[0]], [[0]], [[0]], [0], [0], [1], [1], candidate_names=['A','A'])

    def test_random_exact_minimum_matches_independent_brute_force_oracle(self):
        rng = np.random.default_rng(20261010)
        for case in range(80):
            groups = int(rng.integers(1, 6))
            q = int(rng.integers(1, 8))
            obs = np.repeat(np.arange(groups, dtype=float)[:, None] * 10, 2, axis=0)
            goals = np.tile([0., 4.], groups)[:, None]
            binary = rng.integers(0, 2, size=(groups, q))
            p = np.zeros((groups * 2, q))
            p[1::2] = binary
            costs = rng.integers(1, 6, size=q).astype(float)
            report = self._run(obs, goals, p, [0], [0] * q, [1], costs)
            optimum = float('inf')
            for mask in range(1 << q):
                idx = [j for j in range(q) if mask & (1 << j)]
                if all(any(binary[row, j] for j in idx) for row in range(groups)):
                    optimum = min(optimum, float(sum(costs[j] for j in idx)))
            if optimum == float('inf'):
                self.assertEqual(report['status'], 'NO_LIBRARY_REPAIR', msg=str(case))
            else:
                self.assertEqual(report['status'], 'EXACT_MIN_COST_REPAIR', msg=str(case))
                self.assertAlmostEqual(report['total_cost'], optimum, msg=str(case))
                self.assertLessEqual(report['selected_minimax_error_by_command'][0], 1)

    def test_random_general_noisy_intervals_vs_independent_all_subsets(self):
        rng = np.random.default_rng(418)
        for case in range(65):
            n = int(rng.integers(2, 6))
            q = int(rng.integers(0, 6))
            obs = rng.choice([0., .5, 1., 2.], size=(n, 2))
            ps = rng.choice([0., .5, 1., 2.], size=(n, q))
            goals = rng.choice([0., 1., 2., 4.], size=(n, 2))
            eta = rng.choice([0., .1, .3], size=(n, 2))
            so = np.array([.25, .5])
            sp = rng.choice([0., .25, .5], size=q)
            costs = rng.integers(1, 4, size=q).astype(float)
            tau = np.array([.6, .8])
            rep = self._run(obs, goals, ps, so, sp, tau, costs, goal_uncertainty=eta)
            brute = []
            for mask in range(1 << q):
                chosen = [a for a in range(q) if mask & (1 << a)]
                diameter = np.max(eta, axis=0).astype(float)
                for i in range(n):
                    for j in range(i + 1, n):
                        same_o = np.all(np.abs(obs[i] - obs[j]) <= 2 * so)
                        same_p = all(abs(ps[i, a] - ps[j, a]) <= 2 * sp[a] for a in chosen)
                        if same_o and same_p:
                            gap = (np.abs(goals[i] - goals[j]) + eta[i] + eta[j]) / 2
                            diameter = np.maximum(diameter, gap)
                if np.all(diameter <= tau):
                    brute.append(float(sum(costs[a] for a in chosen)))
            if brute:
                self.assertIn(rep['status'], {'EXACT_MIN_COST_REPAIR', 'NO_REPAIR_NEEDED'}, case)
                self.assertEqual(rep['total_cost'], min(brute), case)
            else:
                self.assertIn(rep['status'], {'NO_LIBRARY_REPAIR', 'INTRINSIC_GOAL_UNCERTAINTY'}, case)

    def test_subpicocost_is_not_rounded_out_of_minimum_search(self):
        r = self._three_pairs(costs=(1e-15, 1e-15, 2e-15))
        self.assertEqual(r['status'], 'EXACT_MIN_COST_REPAIR')
        self.assertEqual(r['selected_indices'], [0, 1])
        self.assertAlmostEqual(r['total_cost'], 2e-15, places=27)

    def test_cli_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            fn = Path(tmp) / 'case.npz'
            out = Path(tmp) / 'report.json'
            np.savez(fn, observations=np.array([[0.], [0.]]),
                     goals=np.array([0., 4.]), candidates=np.array([[0.], [2.]]),
                     observation_radii=np.array([0.]), candidate_radii=np.array([.1]),
                     goal_tolerances=np.array([1.]), candidate_costs=np.array([3.]))
            cp = subprocess.run([sys.executable, str(Path(grc.__file__)), str(fn),
                                 '--output', str(out)], check=False, capture_output=True, text=True)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            r = json.loads(out.read_text())
            self.assertEqual(r['status'], 'EXACT_MIN_COST_REPAIR')
            self.assertEqual(r['selected_indices'], [0])



class RetainedGoalBitsTests(unittest.TestCase):
    """Exact one-shot finite-bank memory budget with later side observation."""

    def test_five_cycle_requires_three_messages_despite_clique_size_two(self):
        # Congruent 2D sensor boxes realize an induced C5:
        # neighboring history boxes overlap; diagonals do not.
        k = np.arange(5)
        obs = np.c_[np.cos(2 * np.pi * k / 5), np.sin(2 * np.pi * k / 5)]
        r = grc.audit_retained_goal_bits(
            obs, (4 * k)[:, None], [f"prepared_{i}" for i in k],
            observation_radii=[0.6, 0.6], goal_tolerances=[1.0])
        self.assertEqual(r["status"], "EXACT_FINITE_BANK_MESSAGE_MINIMUM")
        self.assertEqual(r["max_clique_lower_bound"], 2)
        self.assertEqual(r["minimum_messages"], 3)
        self.assertEqual(r["minimum_retained_bits"], 2)
        self.assertEqual(r["edge_count"], 5)
        for i in range(5):
            for j in range(i + 1, 5):
                if np.all(abs(obs[i] - obs[j]) <= 1.2):
                    self.assertNotEqual(r["messages_by_history"][i], r["messages_by_history"][j])

    def test_exact_class_cap_does_not_overclaim_chromatic_minimum(self):
        i = np.arange(5)
        obs = np.c_[np.cos(2*np.pi*i/5), np.sin(2*np.pi*i/5)]
        result = grc.audit_retained_goal_bits(
            obs, (4*i)[:, None], [str(j) for j in i],
            observation_radii=[0.6, 0.6], goal_tolerances=[1.],
            exact_transcript_cap=2)
        self.assertEqual(result['status'], 'FEASIBLE_COLORING_NOT_PROVEN_MINIMUM')
        self.assertFalse(result['exact_optimum_proven'])
        self.assertEqual(result['message_lower_bound'], 2)
        self.assertEqual(result['message_upper_bound'], 3)
        self.assertEqual(result['bit_upper_bound'], 2)
        self.assertIsNone(result['minimum_messages'])
        self.assertIsNone(result['minimum_retained_bits'])

    def test_unresolvable_identical_transcript_with_overlapping_live_sensor(self):
        r = grc.audit_retained_goal_bits(
            [[0.0], [0.0]], [[0.0], [4.0]], ["same", "same"],
            observation_radii=[0.0], goal_tolerances=[1.0])
        self.assertEqual(r["status"], "INTRINSIC_TRANSCRIPT_ALIAS")
        self.assertEqual(r["unresolvable_history_pair"], [0, 1])
        self.assertIsNone(r["minimum_retained_bits"])

    def test_shared_transcript_is_permitted_if_live_sensor_separates(self):
        r = grc.audit_retained_goal_bits(
            [[0.0], [10.0]], [[0.0], [4.0]], ["same", "same"],
            observation_radii=[0.1], goal_tolerances=[1.0])
        self.assertEqual(r["minimum_messages"], 1)
        self.assertEqual(r["minimum_retained_bits"], 0)
        self.assertAlmostEqual(grc.decode_retained_goal(
            [0.0], 0, r, [[0.0], [10.0]], [[0.0], [4.0]],
            observation_radii=[0.1], goal_tolerances=[1.0])[0], 0.0)

    def test_an_identical_goal_needs_no_history_bits(self):
        r = grc.audit_retained_goal_bits(
            [[0.0], [0.0], [0.0]], [[3.0], [3.0], [3.0]],
            ["a", "b", "c"], observation_radii=[0.0], goal_tolerances=[0.01])
        self.assertEqual(r["minimum_retained_bits"], 0)

    def test_goal_intervals_and_exact_threshold(self):
        r = grc.audit_retained_goal_bits(
            [[0.0], [0.0]], [[0.0], [2.0]], ["a", "b"],
            observation_radii=[0.0], goal_tolerances=[1.0],
            goal_uncertainty=[[0.0], [0.0]])
        self.assertEqual(r["minimum_retained_bits"], 0)
        z = grc.audit_retained_goal_bits(
            [[0.0], [0.0]], [[0.0], [2.0]], ["a", "b"],
            observation_radii=[0.0], goal_tolerances=[1.0],
            goal_uncertainty=[[0.1], [0.1]])
        self.assertEqual(z["minimum_retained_bits"], 1)
        inf = grc.audit_retained_goal_bits(
            [[0.0]], [[0.0]], ["a"],
            observation_radii=[0.0], goal_tolerances=[1.0],
            goal_uncertainty=[[1.1]])
        self.assertEqual(inf["status"], "INTRINSIC_GOAL_INTERVAL")
        
    def test_decoder_worst_case_on_exact_coloring(self):
        obs = [[0], [0], [0]]
        goals = [[0, 2], [4, 2], [8, 2]]
        r = grc.audit_retained_goal_bits(
            obs, goals, ["a", "b", "c"],
            observation_radii=[0.25], goal_tolerances=[1.0, 0.0])
        self.assertEqual(r["minimum_messages"], 3)
        for i, message in enumerate(r["messages_by_history"]):
            pred = grc.decode_retained_goal(
                [0.0], message, r, obs, goals,
                observation_radii=[0.25], goal_tolerances=[1.0, 0.0])
            np.testing.assert_array_less(np.abs(pred - np.asarray(goals[i])),
                                         np.array([1.0 + 1e-12, 1e-12]))

    def test_random_small_graph_vs_independent_exhaustive_code_enumeration(self):
        rng = np.random.default_rng(527)
        for n in range(2, 7):
            for _ in range(12):
                obs = rng.integers(0, 5, size=(n, 2)).astype(float)
                goal = rng.integers(-3, 6, size=(n, 2)).astype(float)
                rad = np.array([0.5, 0.5])
                tau = np.array([1.0, 2.0])
                conflict = {(i, j) for i in range(n) for j in range(i + 1, n)
                            if np.all(abs(obs[i] - obs[j]) <= 2 * rad)
                            and np.any(abs(goal[i] - goal[j]) > 2 * tau)}
                oracle = next(k for k in range(1, n + 1)
                              if any(all(bits[i] != bits[j] for i, j in conflict)
                                     for bits in itertools.product(range(k), repeat=n)))
                r = grc.audit_retained_goal_bits(
                    obs, goal, [f"h{i}" for i in range(n)],
                    observation_radii=rad, goal_tolerances=tau)
                self.assertEqual(r["minimum_messages"], oracle)
                self.assertEqual(r["minimum_retained_bits"], (oracle - 1).bit_length())

    def test_retained_bits_cli_reads_exact_transcript_categories(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "history.npz"
            output = Path(tmp) / "bits.json"
            np.savez(
                source,
                observations=np.zeros((3, 1)),
                goals=np.array([[0.], [4.], [8.]]),
                transcript_ids=np.array(["first", "second", "third"]),
                observation_radii=np.array([0.0]),
                goal_tolerances=np.array([1.0]),
            )
            cp = subprocess.run(
                [sys.executable, str(Path(grc.__file__)), str(source),
                 "--retained-goal-bits", "--output", str(output)],
                check=False, capture_output=True, text=True,
            )
            self.assertEqual(cp.returncode, 0, cp.stderr)
            report = json.loads(output.read_text())
            self.assertEqual(report["minimum_retained_bits"], 2)
            self.assertEqual(report["minimum_messages"], 3)

    def test_invalid_data_rejected(self):
        for kwargs in (
            {"observations": [[0.0]], "goals": [[2.0]], "transcript_ids": []},
            {"observations": [[0.0]], "goals": [[2.0]], "transcript_ids": [""]},
            {"observations": [[float("nan")]], "goals": [[2.0]], "transcript_ids": ["h"]},
        ):
            with self.assertRaises(ValueError):
                grc.audit_retained_goal_bits(
                    kwargs["observations"], kwargs["goals"], kwargs["transcript_ids"],
                    observation_radii=[0.0], goal_tolerances=[1.0])



if __name__ == '__main__':
    unittest.main()
