"""Analytic tests derived from exact observation fibers, not audit output."""
import unittest
import numpy as np
from fiber_curvature_audit import audit


class FiberCurvatureTests(unittest.TestCase):
    def test_straight_observation_fiber_quadratic_goal_leak(self):
        # O(x,y)=x, G(x,y)=x+y^2; at (0,0), O equal for (0,0),(0,t)
        r = audit([[1,0]], [1,0], np.zeros((1,2,2)), [[0,0],[0,2]])
        self.assertEqual(r['status'], 'QUADRATIC_WITNESS')
        self.assertAlmostEqual(r['quadratic_goal_gap_coefficient'], 1)
        self.assertAlmostEqual(abs(r['witness']['goal_second_derivative']), 2)
        self.assertAlmostEqual(r['first_order_hidden_gain'], 0)
        self.assertAlmostEqual(r['witness']['observation_tangent_residual'], 0)

    def test_curved_observation_fiber_requires_second_order_lift(self):
        # O=x+y^2, G=x. Fiber O=0: x=-t^2, goal=-t^2.
        r = audit([[1,0]], [1,0], [[[0,0],[0,2]]], [[0,0],[0,0]])
        self.assertAlmostEqual(r['witness']['goal_second_derivative'], -2)
        self.assertAlmostEqual(r['quadratic_goal_gap_coefficient'], 1)
        self.assertAlmostEqual(r['witness']['observation_second_order_residual'], 0)

    def test_exact_goal_factor_has_no_quadratic_leak(self):
        # G=O=x+y^2. Curvature in O cancels identically.
        h = [[[0,0],[0,2]]]
        r = audit([[1,0]], [1,0], h, [[0,0],[0,2]])
        self.assertEqual(r['status'], 'QUADRATIC_ZERO_NOT_SUFFICIENCY')
        self.assertAlmostEqual(r['quadratic_goal_gap_coefficient'], 0)

    def test_linear_leak_preempts_quadratic_certificate(self):
        r = audit([[1,0]], [0,1], np.zeros((1,2,2)), np.zeros((2,2)))
        self.assertEqual(r['status'], 'FIRST_ORDER_LEAK')
        self.assertAlmostEqual(r['first_order_hidden_gain'], 1)
        self.assertIsNone(r['quadratic_goal_gap_coefficient'])

    def test_full_state_observed_has_no_fiber(self):
        r = audit(np.eye(2), [0,1], np.zeros((2,2,2)), np.eye(2))
        self.assertEqual(r['status'], 'NO_HIDDEN_DIRECTIONS')
        self.assertEqual(r['hidden_dimension'], 0)

    def test_multi_hidden_eigen_direction_is_extremal(self):
        hg = np.array([[0,0,0],[0,2,3],[0,3,-4]],float)
        r = audit([[1,0,0]], [1,0,0], np.zeros((1,3,3)), hg)
        self.assertAlmostEqual(r['max_absolute_fiber_curvature'], 1+np.sqrt(18))
        v = np.array(r['witness']['hidden_unit_tangent'])
        self.assertAlmostEqual(float(v @ hg @ v), r['witness']['goal_second_derivative'])
        self.assertAlmostEqual(np.linalg.norm(v),1)
        self.assertAlmostEqual(v[0],0)

    def test_cubic_leak_is_not_excluded_by_zero_curvature(self):
        # O=x, G=x+y^3 has exactly zero Hessians but is NOT sufficient.
        r = audit([[1,0]], [1,0], np.zeros((1,2,2)), np.zeros((2,2)))
        self.assertEqual(r['status'], 'QUADRATIC_ZERO_NOT_SUFFICIENCY')
        self.assertIn('not',r['claim_ceiling'].lower())

    def test_singular_observation_chart_rejected(self):
        with self.assertRaises(ValueError):
            audit([[0,0]], [0,1], np.zeros((1,2,2)), np.zeros((2,2)))
        with self.assertRaises(ValueError):
            audit([[1,0],[2,0]], [0,1], np.zeros((2,2,2)), np.zeros((2,2)))

    def test_nonsymmetric_and_nan_hessians_rejected(self):
        with self.assertRaises(ValueError):
            audit([[1,0]], [1,0], np.zeros((1,2,2)), [[0,1],[0,0]])
        with self.assertRaises(ValueError):
            audit([[1,0]], [1,0], [[[0,np.nan],[np.nan,0]]], np.zeros((2,2)))

    def test_near_factorization_must_not_be_promoted_to_quadratic_witness(self):
        # G=x+1e-9*y + y**2 has a first-order leak at arbitrarily small radius.
        r = audit([[1,0]], [1,1e-9], np.zeros((1,2,2)), [[0,0],[0,2]],
                  factorization_tol=1e-8)
        self.assertEqual(r["status"], "NEAR_FIRST_ORDER_FACTOR")
        self.assertIsNone(r["quadratic_goal_gap_coefficient"])

    def test_exact_nonlinear_fiber_matches_asymptotic_quadratic_coefficient(self):
        # O(x,y)=x+y^2, G=x: x(t)=-t^2 gives exact same O, G=-t^2.
        r = audit([[1,0]], [1,0], [[[0,0],[0,2]]], [[0,0],[0,0]])
        for t in [0.1,0.01,0.001]:
            x=np.array([-t*t,t])
            self.assertAlmostEqual(x[0]+x[1]*x[1],0.,places=14)
            observed_goal=x[0]
            self.assertAlmostEqual(observed_goal/t**2, r['witness']['goal_second_derivative']/2,places=10)

    def test_absolute_rank_cutoff_rejects_near_underflow(self):
        with self.assertRaises(ValueError):
            audit([[1e-16,0]], [1,0], np.zeros((1,2,2)), np.zeros((2,2)), atol=1e-12)


if __name__ == '__main__':
    unittest.main()
