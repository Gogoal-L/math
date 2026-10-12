"""Synthetic, independently checkable mathematical test cases."""
import unittest
import numpy as np
from goal_ambiguity_audit import gaussian_replicate_goal_pair, audit_marginal_sensor_coupling

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


class MarginalDependenceSensorFusionTests(unittest.TestCase):
    """Independent finite-discrete coupling reconstructions, strong rivals and CLI."""

    @staticmethod
    def _product_joint(factors):
        factors = np.asarray(factors, dtype=float)
        shape = (factors.shape[1],) * factors.shape[0]
        return np.array([np.prod([factors[j, x[j]]
                                 for j in range(factors.shape[0])])
                         for x in np.ndindex(shape)]).reshape(shape)

    def test_independent_two_binary_sensor_transport_grid_oracle(self):
        # Independently minimize TV by enumerating each history's free 2x2
        # coupling cell q(0,0). This oracle never calls the witness builder.
        rng = np.random.default_rng(416)
        for _ in range(12):
            raw = rng.uniform(.05, 1., size=(2,2,2))
            p = raw / raw.sum(axis=2, keepdims=True)
            report = audit_marginal_sensor_coupling(p, [0.,4.], 1.)
            joints = []
            for h in range(2):
                a = p[h,0,0]
                b = p[h,1,0]
                lo = max(0.,a+b-1.)
                hi = min(a,b)
                t = np.linspace(lo,hi,121)
                joints.append(np.stack([t,a-t,b-t,1.-a-b+t],axis=0))
            finite_grid = .5*np.abs(
                joints[0][:,:,None] - joints[1][:,None,:]).sum(axis=0)
            oracle = float(finite_grid.min())
            self.assertGreaterEqual(oracle+1e-12,report["worst_case_joint_tv"])
            self.assertLess(oracle-report["worst_case_joint_tv"], .02)

    def test_constructive_worst_case_joint_matches_all_marginals(self):
        rng = np.random.default_rng(9201)
        for n_sensors in (1, 2, 3):
            for bins in (2, 3):
                for _ in range(16):
                    raw = rng.uniform(.04, 1., size=(2, n_sensors, bins))
                    p = raw / raw.sum(axis=-1, keepdims=True)
                    r = audit_marginal_sensor_coupling(
                        p, future_goals=[0., 3.], goal_tolerance=1.)
                    w = r["attaining_coupling"]
                    common = (w["shared_mass"] *
                              self._product_joint(w["common_sensor_pmfs"]))
                    out = []
                    for h in range(2):
                        q = common + w["residual_mass"] * self._product_joint(
                            w["residual_sensor_pmfs"][h])
                        out.append(q)
                        self.assertAlmostEqual(float(q.sum()), 1., places=10)
                        for j in range(n_sensors):
                            axes = tuple(t for t in range(n_sensors) if t != j)
                            np.testing.assert_allclose(
                                q.sum(axis=axes) if axes else q, p[h,j],
                                atol=2e-11, rtol=0.)
                    actual = .5 * float(np.abs(out[0]-out[1]).sum())
                    self.assertAlmostEqual(
                        actual, r["worst_case_joint_tv"], places=10)
                    self.assertAlmostEqual(
                        r["worst_case_joint_tv"],
                        max(.5*np.abs(p[0]-p[1]).sum(axis=-1)), places=11)

    def test_identical_single_sensor_marginals_allow_complete_joint_synergy(self):
        marginal = np.full((2, 2, 2), .5)
        joint = np.array([
            [[.5, 0.], [0., .5]],
            [[0., .5], [.5, 0.]],
        ])
        r = audit_marginal_sensor_coupling(
            marginal, [0., 4.], 1., joint_probabilities=joint)
        self.assertEqual(r["worst_case_joint_tv"], 0.)
        self.assertAlmostEqual(
            r["worst_case_equal_prior_goal_failure"], .5)
        self.assertAlmostEqual(r["qualified_joint"]["tv"], 1.)
        self.assertAlmostEqual(
            r["qualified_joint"]["equal_prior_goal_failure"], 0.)
        self.assertAlmostEqual(r["qualified_joint"]["tv_gain_over_best_single"], 1.)

    def test_three_independent_binary_sensors_have_real_not_robust_gain(self):
        p = np.array([[[.8,.2]]*3, [[.2,.8]]*3])
        p0 = self._product_joint(p[0])
        p1 = self._product_joint(p[1])
        r = audit_marginal_sensor_coupling(
            p, [0., 4.], 1., joint_probabilities=np.stack([p0,p1]))
        self.assertAlmostEqual(r["worst_case_joint_tv"], .6)
        self.assertAlmostEqual(r["qualified_joint"]["tv"], .792)
        self.assertAlmostEqual(r["worst_case_equal_prior_goal_failure"], .2)
        self.assertAlmostEqual(
            r["qualified_joint"]["equal_prior_goal_failure"], .104)

    def test_hall_feasible_disjoint_source_support_restores_per_history_prediction(self):
        p=np.full((2,2,2),.5)
        masks=np.array([[[1,0],[0,1]], [[0,1],[1,0]]])
        r=audit_marginal_sensor_coupling(p,[0.,4.],1.,
                                          allowed_joint_supports=masks)
        self.assertAlmostEqual(r["worst_case_joint_tv"],0.)
        support=r["support_certificate"]
        self.assertTrue(support["source_supports_disjoint"])
        self.assertTrue(support["exact_feasibility_checked"])
        self.assertEqual(support["conditional_goal_failure_upper_bounds"],[0.,0.])
        self.assertEqual(support["support_inferred_joint_tv_lower_bound"],1.)

    def test_hall_row_cut_rejects_infeasible_zero_pattern(self):
        p=np.array([[[.9,.1],[.1,.9]],
                    [[.5,.5],[.5,.5]]])
        masks=np.array([[[1,0],[0,1]], [[1,1],[1,1]]])
        with self.assertRaisesRegex(ValueError,"Hall"):
            audit_marginal_sensor_coupling(p,[0.,4.],1.,
                                           allowed_joint_supports=masks)

    def test_soft_disjoint_support_certifies_conditional_not_average_only(self):
        p=np.full((2,2,2),.5)
        masks=np.array([[[1,0],[0,1]], [[0,1],[1,0]]])
        r=audit_marginal_sensor_coupling(
            p,[0.,4.],1., allowed_joint_supports=masks,
            support_leakage_bounds=[.03,.06])
        support=r["support_certificate"]
        self.assertFalse(support["exact_feasibility_checked"])
        self.assertEqual(support["conditional_goal_failure_upper_bounds"],
                         [.03,.06])
        self.assertAlmostEqual(
            support["equal_prior_goal_failure_upper_bound"],.045)
        self.assertAlmostEqual(r["worst_case_equal_prior_goal_failure"],.5)

    def test_supplied_joint_must_obey_declared_leakage(self):
        p=np.full((2,2,2),.5)
        joint=np.full((2,2,2),.25)
        masks=np.array([[[1,0],[0,1]], [[0,1],[1,0]]])
        with self.assertRaisesRegex(ValueError,"support"):
            audit_marginal_sensor_coupling(
                p,[0.,4.],1.,joint_probabilities=joint,
                allowed_joint_supports=masks)
        # A source-qualified 50% tail in each state is consistent, but
        # it cannot establish the strong perfect-separation conclusion.
        r=audit_marginal_sensor_coupling(
            p,[0.,4.],1.,joint_probabilities=joint,
            allowed_joint_supports=masks,
            support_leakage_bounds=[.5,.5])
        self.assertEqual(r["support_certificate"]["conditional_goal_failure_upper_bounds"],[.5,.5])

    def test_overlapping_supports_and_more_than_two_sensors_not_overpromoted(self):
        p=np.full((2,2,2),.5)
        masks=np.ones((2,2,2),dtype=bool)
        r=audit_marginal_sensor_coupling(p,[0.,4.],1.,
                                          allowed_joint_supports=masks)
        self.assertFalse(r["support_certificate"]["source_supports_disjoint"])
        self.assertIsNone(r["support_certificate"]["conditional_goal_failure_upper_bounds"])
        with self.assertRaisesRegex(ValueError,"two sensor"):
            audit_marginal_sensor_coupling(
                np.full((2,3,2),.5),[0.,4.],1.,
                allowed_joint_supports=masks)

    def test_goal_intervals_overlap_then_prediction_needs_no_sensor(self):
        p = np.array([[[1.,0.]], [[0.,1.]]])
        r = audit_marginal_sensor_coupling(p, [0.,2.], 1.)
        self.assertEqual(r["status"], "GOAL_WITHIN_TOLERANCE_NO_SENSING")
        self.assertEqual(r["worst_case_equal_prior_goal_failure"], 0.)
        self.assertAlmostEqual(r["worst_case_joint_tv"], 1.)

    def test_perfect_marginal_is_perfect_joint_even_without_correlation(self):
        p = np.array([[[1.,0.],[.5,.5]],
                      [[0.,1.],[.5,.5]]])
        r = audit_marginal_sensor_coupling(p, [0.,4.], 1.)
        self.assertAlmostEqual(r["worst_case_joint_tv"], 1.)
        self.assertEqual(r["worst_case_equal_prior_goal_failure"], 0.)
        self.assertAlmostEqual(r["attaining_coupling"]["shared_mass"], 0.)

    def test_identical_marginals_have_identical_coupling_witness(self):
        p = np.array([[[.6,.4],[.1,.9]], [[.6,.4],[.1,.9]]])
        r = audit_marginal_sensor_coupling(p, [0.,4.], 1.)
        self.assertAlmostEqual(r["worst_case_joint_tv"], 0.)
        self.assertAlmostEqual(r["attaining_coupling"]["shared_mass"], 1.)

    def test_reject_wrong_or_unnormalized_joint_models(self):
        p=np.full((2,2,2),.5)
        valid=np.stack([np.full((2,2),.25)]*2)
        r=audit_marginal_sensor_coupling(p,[0.,4.],1.,
                                          joint_probabilities=valid)
        self.assertAlmostEqual(r["qualified_joint"]["tv"], 0.)
        bad_joint=valid.copy()
        bad_joint[0,0,0]=.5;bad_joint[0,1,1]=0.
        with self.assertRaises(ValueError):
            audit_marginal_sensor_coupling(
                p,[0.,4.],1.,joint_probabilities=bad_joint)
        with self.assertRaises(ValueError):
            audit_marginal_sensor_coupling(
                p,[0.,4.],1.,joint_probabilities=np.zeros((2,3,2)))

    def test_reject_nan_negative_bad_marginals_and_names(self):
        p=np.full((2,2,2),.5)
        cases=[p.copy(),p.copy(),p.copy()]
        cases[0][0,0,0]=-1.
        cases[1][1,1,1]=float("nan")
        cases[2][0,0,:]=[.4,.4]
        for x in cases:
            with self.assertRaises(ValueError):
                audit_marginal_sensor_coupling(x,[0.,4.],1.)
        with self.assertRaises(ValueError):
            audit_marginal_sensor_coupling(p,[0.,4.],1.,
                                           sensor_names=["same","same"])
        with self.assertRaises(ValueError):
            audit_marginal_sensor_coupling(p,[0.,4.],-1.)

    def test_single_sensor_decision_rule_exactly_attains_equal_prior_risk(self):
        r = audit_marginal_sensor_coupling(
            np.array([[[.8,.2],[.6,.4]], [[.2,.8],[.55,.45]]]),
            [0.,4.], 1., sensor_names=["A","B"])
        rule = r["best_single_sensor_rule"]
        self.assertEqual(r["best_single_sensor"], "A")
        self.assertEqual(rule["decision_by_bin"], [0,1])
        self.assertAlmostEqual(rule["equal_prior_failure_if_separated"],
                               r["worst_case_equal_prior_goal_failure"])
        self.assertAlmostEqual(rule["maximum_conditional_failure_of_this_rule_if_separated"],.2)

    def test_worst_history_risk_is_not_reported_as_equal_prior_optimum(self):
        # Bayes error 0.25, but randomized minimax maximum conditional error
        # is 1/3 for P0=(1,0), P1=(.5,.5).
        p=np.array([[[1.,0.]], [[.5,.5]]])
        r=audit_marginal_sensor_coupling(p,[0.,4.],1.)
        self.assertAlmostEqual(r["worst_case_equal_prior_goal_failure"], .25)
        self.assertNotIn("exact_minimax_worst_history_error", r)
        self.assertAlmostEqual(r["best_single_sensor_rule"]["equal_prior_failure_if_separated"],.25)
        self.assertAlmostEqual(r["best_single_sensor_rule"]["maximum_conditional_failure_of_this_rule_if_separated"],.5)
        self.assertIn("not the worst-history", r["scope"])

    def test_finite_marginal_fusion_cli_npz_round_trip(self):
        import json
        import subprocess
        import tempfile
        import sys
        from pathlib import Path
        from goal_ambiguity_audit import __file__ as tool_file
        p=np.array([[[.8,.2]]*3, [[.2,.8]]*3])
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/"marginal_bank.npz"
            dest=Path(folder)/"report.json"
            np.savez(source,marginal_probabilities=p,
                     future_goals=np.array([0.,4.]),
                     goal_tolerance=np.array(1.),
                     sensor_names=np.array(["VDS","ID","VGS"]))
            command=[sys.executable,tool_file,str(source),
                     "--marginal-only-fusion","--output",str(dest)]
            proc=subprocess.run(command,capture_output=True,text=True)
            self.assertEqual(proc.returncode,0,proc.stderr)
            result=json.loads(dest.read_text(encoding="utf8"))
            self.assertEqual(result["best_single_sensor"],"VDS")
            self.assertAlmostEqual(result["worst_case_joint_tv"],.6)
            self.assertEqual(result["source_law_status"],
                             "CONDITIONAL_FINITE_CATEGORICAL_ONLY")


if __name__ == "__main__":
    unittest.main()
