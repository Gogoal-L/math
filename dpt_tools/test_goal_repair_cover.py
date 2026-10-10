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


if __name__ == '__main__':
    unittest.main()
