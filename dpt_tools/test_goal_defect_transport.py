"""Independent reference cases for a command-ordered goal-error auditor."""
import json
import unittest

import numpy as np

from goal_defect_transport import audit


class GoalDefectTransportTests(unittest.TestCase):
    def test_hidden_state_is_invisible_initially_but_visible_after_stage(self):
        a = np.array([[[0.5, 6.0], [0.0, 0.5]]])
        result = audit(a, [[1.0, 0.0]], [1.0, 0.0], 0.01, [0.0])
        self.assertAlmostEqual(result['stages'][0]['information_radius'], 0.0)
        self.assertAlmostEqual(result['stages'][1]['information_radius'], 0.06)
        self.assertAlmostEqual(result['worst_stage']['total_radius'], 0.06)
        self.assertAlmostEqual(result['max_absolute_witness']['goal_deviation'], 0.06)
        self.assertAlmostEqual(result['max_absolute_witness']['observation_residual'], 0.0)
        self.assertTrue(all(abs(ev - 0.5) < 1e-12 for ev in result['stage_spectral_radii']))

    def test_two_distinct_stage_defects_add_exactly_in_goal_direction(self):
        a = np.array([[[2.0]], [[3.0]]])
        result = audit(a, np.array([[1.0]]), np.array([1.0]), 0.0, [0.1, 0.2])
        self.assertAlmostEqual(result['stages'][1]['defect_radius'], 0.1)
        self.assertAlmostEqual(result['stages'][2]['defect_radius'], 0.5)
        self.assertAlmostEqual(result['max_absolute_witness']['goal_deviation'], 0.5)
        self.assertEqual(result['worst_stage']['stage'], 2)

    def test_hidden_state_and_solver_budgets_are_separately_reported(self):
        result = audit([np.eye(2)], [[1, 0]], [0, 1], 0.3, [0.2])
        self.assertAlmostEqual(result['worst_stage']['information_radius'], 0.3)
        self.assertAlmostEqual(result['worst_stage']['defect_radius'], 0.2)
        self.assertAlmostEqual(result['worst_stage']['total_radius'], 0.5)
        self.assertAlmostEqual(result['max_absolute_witness']['goal_deviation'], 0.5)

    def test_full_observation_removes_hidden_information_not_solver_error(self):
        result = audit([np.eye(2)], np.eye(2), [1, 0], 5.0, [0.04])
        self.assertAlmostEqual(result['worst_stage']['information_radius'], 0.0)
        self.assertAlmostEqual(result['worst_stage']['defect_radius'], 0.04)

    def test_different_goals_at_different_command_stages(self):
        a = np.array([np.eye(2), np.eye(2)])
        g = np.array([[1, 0], [0, 1], [1, 0]])
        result = audit(a, [[1, 0]], g, 0.3, [0, 0])
        self.assertEqual([round(s['information_radius'], 4) for s in result['stages']], [0., .3, 0.])
        self.assertEqual(result['worst_stage']['stage'], 1)

    def test_no_stages_is_allowed_and_exact_initial_goal_radius(self):
        a = np.zeros((0, 2, 2))
        result = audit(a, np.zeros((0, 2)), [1, 0], 0.5, [])
        self.assertAlmostEqual(result['worst_stage']['total_radius'], 0.5)
        self.assertEqual(result['stages'][0]['stage'], 0)

    def test_noncommuting_order_changes_hidden_goal_leakage(self):
        a = np.array([[1., 1.], [0., 1.]])
        b = np.array([[1., 0.], [0., 0.]])
        # The matrix applied first is leftmost in [a,b]; final state is b@a@x.
        ab = audit([a, b], [[1, 0]], [1, 0], 1., [0, 0])
        ba = audit([b, a], [[1, 0]], [1, 0], 1., [0, 0])
        self.assertAlmostEqual(ab['stages'][2]['information_radius'], 1.)
        self.assertAlmostEqual(ba['stages'][2]['information_radius'], 0.)

    def test_degenerate_zero_goal_zero_radii_witness_stays_zero(self):
        out = audit([np.eye(2)], [[1, 0]], [0, 0], 3., [1.])
        self.assertAlmostEqual(out['worst_stage']['total_radius'], 0.)
        self.assertAlmostEqual(out['max_absolute_witness']['goal_deviation'], 0.)

    def test_scalar_disturbance_signs_exhaustively_recover_bound(self):
        # Independent oracle by enumerating all +- extremes of three 1D balls.
        from itertools import product
        stages = [-2.0, 0.25]
        rho, eps = 0.3, [0.1, 0.2]
        model = audit(np.array(stages)[:, None, None], np.zeros((0, 1)),
                      [1.0], rho, eps)
        actual = []
        for signs in product((-1, 1), repeat=3):
            x = signs[0] * rho
            x = stages[0] * x + signs[1] * eps[0]
            x = stages[1] * x + signs[2] * eps[1]
            actual.append(abs(x))
        self.assertAlmostEqual(model['stages'][2]['total_radius'], max(actual))
        self.assertAlmostEqual(model['stages'][2]['information_radius'], 0.15)
        self.assertAlmostEqual(model['stages'][2]['defect_radius'], 0.225)

    def test_fail_closed_on_negative_nan_misalignment(self):
        with self.assertRaises(ValueError):
            audit([np.eye(2)], [[1, 0]], [1, 0], -1., [0])
        with self.assertRaises(ValueError):
            audit([np.eye(2)], [[1, 0]], [1, 0], 1., [np.nan])
        with self.assertRaises(ValueError):
            audit([np.eye(2)], [[1, 0]], [1, 0], 1., [])
        with self.assertRaises(ValueError):
            audit([np.eye(2)], [[1, 0, 0]], [1, 0], 1., [0])
        with self.assertRaises(ValueError):
            audit([np.eye(2)], [[1, 0]], [1, 0], 1., [0], rtol=-1)

    def test_witness_matches_the_reported_exact_product_ball_support(self):
        a = np.array([[[0, 2], [1, 0]], [[0.1, 0.4], [-0.1, 0.2]], [[1, 0], [0, 2]]], dtype=float)
        out = audit(a, [[1, 1]], [0.7, -1.2], 0.4, [0.1, 0.03, 0.2])
        w = out['max_absolute_witness']
        self.assertAlmostEqual(abs(w['goal_deviation']), out['worst_stage']['total_radius'], places=11)
        self.assertLessEqual(w['observation_residual'], 1e-11)
        self.assertLessEqual(w['initial_norm'], 0.4 + 1e-11)
        self.assertTrue(all(norm <= lim+1e-11 for norm, lim in zip(w['defect_norms'], [0.1, 0.03, 0.2])))

if __name__ == '__main__':
    unittest.main()
