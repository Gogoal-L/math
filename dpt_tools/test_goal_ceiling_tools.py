"""Synthetic, independently checkable mathematical test cases."""
import unittest
import numpy as np
from goal_ambiguity_audit import gaussian_replicate_goal_pair

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


class NoisyRepeatGoalTests(unittest.TestCase):
    """Analytically sharp two-history goal testing under repeated Gaussian reads."""

    def test_goal_irrelevance_requires_no_measurement(self):
        report = gaussian_replicate_goal_pair(
            observed_means=[0, 0], future_goals=[0, 2],
            goal_tolerance=1., independent_sigma=1., shared_sigma=1.,
            failure_probability=.05)
        self.assertEqual(report["minimum_repeats"], 0)
        self.assertEqual(report["status"], "GOAL_WITHIN_TOLERANCE_WITHOUT_SENSING")

    def test_independent_repeat_threshold_is_exact(self):
        report = gaussian_replicate_goal_pair(
            observed_means=[0, 1], future_goals=[0, 4],
            goal_tolerance=.5, independent_sigma=1., shared_sigma=0.,
            failure_probability=.05)
        self.assertEqual(report["minimum_repeats"], 11)
        self.assertLessEqual(report["minimax_failure_at_repeats"], .05)
        self.assertGreater(report["minimax_failure_at_previous_repeats"], .05)
        self.assertAlmostEqual(report["single_repeat_failure"],
                               .3085375387259869, places=8)

    def test_shared_calibration_floor_makes_repeat_budget_infinite(self):
        report = gaussian_replicate_goal_pair(
            observed_means=[0, 1], future_goals=[0, 4],
            goal_tolerance=.5, independent_sigma=1., shared_sigma=.4,
            failure_probability=.05)
        self.assertEqual(report["status"], "SHARED_NUISANCE_INFORMATION_FLOOR")
        self.assertIsNone(report["minimum_repeats"])
        self.assertGreater(report["asymptotic_failure_floor"], .05)

    def test_shared_noise_changes_repeat_budget_with_same_single_run_law(self):
        a = gaussian_replicate_goal_pair(
            observed_means=[0, 1], future_goals=[0, 4],
            goal_tolerance=1., independent_sigma=np.sqrt(1.04),
            shared_sigma=0., failure_probability=.05)
        b = gaussian_replicate_goal_pair(
            observed_means=[0, 1], future_goals=[0, 4],
            goal_tolerance=1., independent_sigma=1.,
            shared_sigma=.2, failure_probability=.05)
        self.assertAlmostEqual(a["single_repeat_failure"], b["single_repeat_failure"])
        self.assertLess(a["minimum_repeats"], b["minimum_repeats"])
        self.assertEqual(b["minimum_repeats"], 20)

    def test_identical_single_run_laws_can_have_three_different_repeat_limits(self):
        expected = []
        for independent, shared in ((np.sqrt(1.04), 0.), (1., .2), (np.sqrt(.88), .4)):
            r = gaussian_replicate_goal_pair(
                observed_means=[0,1], future_goals=[0,4],
                goal_tolerance=1., independent_sigma=independent,
                shared_sigma=shared, failure_probability=.05)
            expected.append(r)
        for r in expected[1:]:
            self.assertAlmostEqual(r["single_repeat_failure"],
                                   expected[0]["single_repeat_failure"], places=12)
        self.assertEqual(expected[0]["minimum_repeats"], 12)
        self.assertEqual(expected[1]["minimum_repeats"], 20)
        self.assertEqual(expected[2]["status"], "SHARED_NUISANCE_INFORMATION_FLOOR")
        self.assertIsNone(expected[2]["minimum_repeats"])

    def test_equal_sensor_means_cannot_separate_different_goals(self):
        report = gaussian_replicate_goal_pair(
            observed_means=[3, 3], future_goals=[0, 4],
            goal_tolerance=1., independent_sigma=.1, shared_sigma=.0,
            failure_probability=.05)
        self.assertEqual(report["status"], "IDENTICAL_SENSOR_LAWS")
        self.assertIsNone(report["minimum_repeats"])

    def test_exact_sensor_discrimination_requires_one_read(self):
        report = gaussian_replicate_goal_pair(
            observed_means=[0, 1], future_goals=[0, 4],
            goal_tolerance=1., independent_sigma=0., shared_sigma=0.,
            failure_probability=.05)
        self.assertEqual(report["minimum_repeats"], 1)
        self.assertEqual(report["minimax_failure_at_repeats"], 0.)

    def test_gaussian_threshold_equals_simulated_symmetry_test(self):
        rng = np.random.default_rng(191)
        mu_gap, sigma_shared, sigma_independent, repeats = 1., .2, 1., 20
        draws = 120000
        shared = rng.normal(0,sigma_shared,size=draws)
        mean_error = rng.normal(0,sigma_independent/np.sqrt(repeats),size=draws)
        observed = shared + mean_error
        simulated = np.mean(observed > mu_gap / 2)
        out = gaussian_replicate_goal_pair(
            observed_means=[0,mu_gap], future_goals=[0,4],
            goal_tolerance=1., independent_sigma=sigma_independent,
            shared_sigma=sigma_shared, failure_probability=.05)
        self.assertAlmostEqual(simulated,out["minimax_failure_at_repeats"],delta=.008)

    def test_repeat_goal_cli_npz_round_trip_without_legacy_noise_flag(self):
        import subprocess
        import tempfile
        import json
        import sys
        from pathlib import Path
        from goal_ambiguity_audit import __file__ as cli_path
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "paired.npz"
            out = Path(tmp) / "report.json"
            np.savez(p, observed_means=np.array([0., 1.]),
                     future_goals=np.array([0., 4.]),
                     goal_tolerance=np.array(1.),
                     independent_sigma=np.array(1.),
                     shared_sigma=np.array(.2),
                     failure_probability=np.array(.05))
            proc = subprocess.run(
                [sys.executable, cli_path, str(p),
                 "--gaussian-repeat-goal", "--output", str(out)],
                capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads(out.read_text())
            self.assertEqual(result["minimum_repeats"], 20)
            self.assertEqual(result["source_law_status"],
                             "CONDITIONAL_MATHEMATICAL_ONLY")

    def test_invalid_gaussian_contract_rejected(self):
        base=dict(observed_means=[0,1],future_goals=[0,4],
                  goal_tolerance=1.,independent_sigma=1.,
                  shared_sigma=0.,failure_probability=.05)
        for key,bad in (
            ("observed_means",[0]),("future_goals",[0, float('nan')]),
            ("goal_tolerance",-1),("independent_sigma",-1),
            ("shared_sigma",-1),("failure_probability",.7)
        ):
            with self.subTest(key=key):
                args=dict(base);args[key]=bad
                with self.assertRaises(ValueError):
                    gaussian_replicate_goal_pair(**args)


if __name__ == "__main__":
    unittest.main()
