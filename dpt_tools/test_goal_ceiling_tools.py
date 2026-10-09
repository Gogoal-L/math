"""Synthetic, independently checkable mathematical test cases."""
import unittest
import numpy as np

from goal_word_quotient import audit as word_audit
from implicit_goal_certificate import audit as implicit_audit


class WordQuotientTests(unittest.TestCase):
    def test_ordered_command_recovers_a_direction_only_after_two_steps(self):
        a = np.array([[1, 0, 0], [0, 1, 1], [0, 0, 1]], dtype=float)
        b = np.array([[1, 1, 0], [0, 1, 0], [0, 0, 1]], dtype=float)
        c = [[1., 0., 0.]]
        rep = word_audit({"A": a, "B": b}, c, c)
        self.assertEqual([r["goal_rank"] for r in rep["horizons"]], [1, 2, 3, 3])
        self.assertEqual([r["extra_linear_observation_rows"] for r in rep["horizons"]], [0, 1, 2, 2])
        self.assertEqual(rep["saturated_at_horizon"], 2)
        self.assertEqual(rep["minimal_autonomous_goal_rank"], 3)
        self.assertLess(rep["max_update_closure_residual"], 1e-11)
        self.assertEqual(rep["claim_type"], "LINEAR_MODEL_ONLY")

    def test_single_goal_of_scaled_identity_needs_only_one_state(self):
        rep = word_audit({"hold": np.diag([2., 3., 4.])}, [[1., 0., 0.]], [[1., 0., 0.]])
        self.assertEqual(rep["minimal_autonomous_goal_rank"], 1)
        self.assertEqual(rep["horizons"][-1]["extra_linear_observation_rows"], 0)
        self.assertAlmostEqual(rep["reduced_updates"]["hold"][0][0], 2.)

    def test_long_chain_stops_after_finite_n_minus_r_steps(self):
        a = np.eye(6) + np.diag(np.ones(5), 1)
        rep = word_audit({"A": a, "B": np.eye(6), "C": np.eye(6)}, [[1., 0, 0, 0, 0, 0]], [[1., 0, 0, 0, 0, 0]])
        self.assertEqual([s["goal_rank"] for s in rep["horizons"]], [1, 2, 3, 4, 5, 6, 6])
        self.assertEqual(rep["saturated_at_horizon"], 5)

    def test_existing_observation_can_be_distinct_from_goal(self):
        rep = word_audit({"a": np.eye(3)}, [[0., 1., 0.]], [[1., 0., 0.]])
        self.assertEqual(rep["minimal_autonomous_goal_rank"], 1)
        self.assertEqual(rep["horizons"][0]["extra_linear_observation_rows"], 1)
        self.assertEqual(rep["horizons"][-1]["extra_linear_observation_rows"], 1)

    def test_coordinate_change_preserves_exact_ranks(self):
        a = np.array([[1, 0, 0], [0, 1, 1], [0, 0, 1]], dtype=float)
        b = np.array([[1, 1, 0], [0, 1, 0], [0, 0, 1]], dtype=float)
        c = np.array([[1., 0., 0.]])
        s = np.array([[2., 1., 0.], [0., 1., 0.], [0., 0., .5]])
        si = np.linalg.inv(s)
        p = word_audit({"A": a, "B": b}, c, c)
        q = word_audit({"A": s @ a @ si, "B": s @ b @ si}, c @ si, c @ si)
        self.assertEqual([x["goal_rank"] for x in p["horizons"]], [x["goal_rank"] for x in q["horizons"]])

    def test_invalid_updates_and_bad_tolerances_rejected(self):
        with self.assertRaises(ValueError):
            word_audit({"A": np.eye(2)}, [[1., 0., 0.]], [[1., 0., 0.]])
        with self.assertRaises(ValueError):
            word_audit({"A": np.array([[1., np.nan], [0, 1]])}, [[1., 0.]], [[1., 0.]])
        with self.assertRaises(ValueError):
            word_audit({"A": np.eye(2)}, [[1., 0.]], [[1., 0.]], rtol=-1.)


class ImplicitGoalTests(unittest.TestCase):
    def test_linear_equation_goal_correction_is_exact(self):
        rep = implicit_audit([-1.], [[2.]], [3.], inverse_norm_upper=.5,
                             newton_step_upper=.5, jacobian_lipschitz_upper=0.,
                             goal_hessian_upper=0., domain_radius=.5)
        self.assertEqual(rep["status"], "CONDITIONAL_KANTOROVICH")
        self.assertAlmostEqual(rep["root_distance_upper"], .5)
        self.assertAlmostEqual(rep["signed_goal_correction"], 1.5)
        self.assertAlmostEqual(rep["corrected_goal_error_upper"], 0.)

    def test_nonlinear_root_correction_has_analytic_truth_inside_bound(self):
        # F(y) = y + y**2 - 0.09, y_hat=0; goal G(y)=y.
        rep = implicit_audit([-.09], [[1.]], [1.], inverse_norm_upper=1.,
                             newton_step_upper=.09, jacobian_lipschitz_upper=2.,
                             goal_hessian_upper=0., domain_radius=.2)
        truth = (-1. + np.sqrt(1.36)) / 2.
        self.assertEqual(rep["status"], "CONDITIONAL_KANTOROVICH")
        self.assertLessEqual(abs(truth - rep["signed_goal_correction"]), rep["corrected_goal_error_upper"] + 1e-12)
        self.assertAlmostEqual(rep["root_distance_upper"], .1)
        self.assertAlmostEqual(rep["corrected_goal_error_upper"], .01)

    def test_zero_first_order_goal_has_nonzero_hessian_error(self):
        # G(y)=y^2, y_hat=0; true value ~0.0069, leading signed term is zero.
        rep = implicit_audit([-.09], [[1.]], [0.], inverse_norm_upper=1.,
                             newton_step_upper=.09, jacobian_lipschitz_upper=2.,
                             goal_hessian_upper=2., domain_radius=.2)
        truth = ((-1. + np.sqrt(1.36)) / 2.) ** 2
        self.assertAlmostEqual(rep["signed_goal_correction"], 0.)
        self.assertLessEqual(truth, rep["corrected_goal_error_upper"] + 1e-12)

    def test_kantorovich_failure_is_inconclusive_not_false(self):
        rep = implicit_audit([-.5], [[1.]], [1.], inverse_norm_upper=1.,
                             newton_step_upper=.5, jacobian_lipschitz_upper=2.,
                             goal_hessian_upper=0., domain_radius=2.)
        self.assertEqual(rep["status"], "INCONCLUSIVE_CURVATURE")
        self.assertIsNone(rep["corrected_goal_error_upper"])

    def test_branch_domain_too_narrow_is_inconclusive(self):
        rep = implicit_audit([-.09], [[1.]], [1.], inverse_norm_upper=1.,
                             newton_step_upper=.09, jacobian_lipschitz_upper=2.,
                             goal_hessian_upper=0., domain_radius=.05)
        self.assertEqual(rep["status"], "INCONCLUSIVE_DOMAIN")

    def test_inconsistent_supplied_inverse_or_step_bounds_rejected(self):
        base = dict(jacobian_lipschitz_upper=0., goal_hessian_upper=0., domain_radius=1.)
        with self.assertRaises(ValueError):
            implicit_audit([-.2], [[1.]], [1.], inverse_norm_upper=.9, newton_step_upper=.2, **base)
        with self.assertRaises(ValueError):
            implicit_audit([-.2], [[1.]], [1.], inverse_norm_upper=1., newton_step_upper=.19, **base)

    def test_nonsquare_singular_and_nan_inputs_rejected(self):
        base = dict(inverse_norm_upper=1., newton_step_upper=.2,
                    jacobian_lipschitz_upper=0., goal_hessian_upper=0., domain_radius=1.)
        with self.assertRaises(ValueError):
            implicit_audit([-.2], [[0.]], [1.], **base)
        with self.assertRaises(ValueError):
            implicit_audit([-.2], [[1., 0.]], [1.], **base)
        with self.assertRaises(ValueError):
            implicit_audit([float('nan')], [[1.]], [1.], **base)


if __name__ == "__main__":
    unittest.main()
