"""Independent analytic behavior tests for a continuous goal-information radius."""
import unittest
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import numpy as np

from goal_ellipsoid_recovery import recover_scalar_goal
import goal_ellipsoid_recovery as ger


class GoalEllipsoidTests(unittest.TestCase):
    def check_gap(self, report):
        self.assertLess(report["numerical_gap"], 5e-7)
        self.assertLessEqual(report["feasible_witness_lower"], report["algorithm_upper"] + 1e-9)

    def test_unobserved_prior_support(self):
        out = recover_scalar_goal(np.diag([2., 3.]), np.empty((0, 2)),
                                  np.empty((0, 0)), np.array([3., 4.]))
        self.assertAlmostEqual(out["radius"], np.hypot(6., 12.), places=8)
        self.assertEqual(out["measurement_weights"], [])
        self.check_gap(out)

    def test_observable_goal_and_unobservable_parameter(self):
        H = np.array([[1., 0.]])
        for goal, wanted in [(np.array([1., 0.]), 0.2),
                             (np.array([0., 1.]), 1.0)]:
            out = recover_scalar_goal(np.eye(2), H, np.array([[0.2]]), goal)
            self.assertAlmostEqual(out["radius"], wanted, places=6)
            self.check_gap(out)
        self.assertAlmostEqual(recover_scalar_goal(np.eye(2), H, np.array([[0.2]]),
                                                   np.array([1., 0.]))["measurement_weights"][0], 1., places=5)

    def test_mixed_goal_has_interior_bottleneck(self):
        out = recover_scalar_goal(np.eye(2), np.array([[1., 0.]]),
                                  np.array([[0.2]]), np.ones(2))
        self.assertAlmostEqual(out["radius"], 0.2 + np.sqrt(1 - 0.2**2), places=6)
        self.assertGreater(out["q"], 0)
        self.assertLess(out["q"], 1)
        self.check_gap(out)

    def test_elliptical_prior(self):
        out = recover_scalar_goal(np.diag([2., 1.]), np.array([[1., 0.]]),
                                  np.array([[0.5]]), np.array([1., 1.]))
        self.assertAlmostEqual(out["radius"], 0.5 + np.sqrt(1 - (0.5 / 2.)**2), places=6)
        self.check_gap(out)

    def test_joint_correlated_measurement_noise(self):
        E = np.array([[0.1, 0.], [0.08, 0.06]])
        out = recover_scalar_goal(np.eye(2)*10, np.eye(2), E, np.ones(2))
        self.assertAlmostEqual(out["radius"], np.linalg.norm(E.T @ np.ones(2)), places=6)
        np.testing.assert_allclose(out["measurement_weights"], [1, 1], atol=1e-5)
        self.check_gap(out)

    def test_adding_independent_measurement_cannot_worsen_risk(self):
        g = np.array([0., 1.])
        before = recover_scalar_goal(np.eye(2), np.array([[1., 0.]]),
                                     np.array([[0.1]]), g)
        after = recover_scalar_goal(np.eye(2), np.eye(2),
                                    np.diag([0.1, 0.1]), g)
        self.assertGreater(before["radius"], after["radius"])
        self.check_gap(after)

    def test_cli_npz_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "chart.npz"
            outpath = Path(tmp) / "report.json"
            np.savez(data, state_factor=np.eye(2), observation=np.array([[1., 0.]]),
                     noise_factor=np.array([[0.1]]), goal=np.array([1., 0.]))
            proc = subprocess.run([sys.executable, str(Path(__file__).parent / "goal_ellipsoid_recovery.py"),
                                   str(data), "--output", str(outpath)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertAlmostEqual(json.loads(outpath.read_text())["radius"], 0.1, places=8)

    def test_ill_scaled_positive_noise_is_not_exact_noiseless_measurement(self):
        B=np.eye(2)
        H=np.eye(2)
        E=np.diag([1e13, 0.01])
        goal=np.array([0.,1.])
        report=recover_scalar_goal(B,H,E,goal)
        # Two actually feasible SAME observation y=0 worlds:
        # z=(0,+/-0.01), epsilon=(0,-/+1), and ||z||2<=1.
        # Both yield z+E@epsilon=0 but goals differ by 0.02.
        for sign in (-1.,1.):
            z=np.array([0.,sign*0.01])
            e=np.array([0.,-sign])
            self.assertLessEqual(np.linalg.norm(z),1.)
            self.assertLessEqual(np.linalg.norm(e),1.)
            np.testing.assert_allclose(H@(B@z)+E@e,np.zeros(2))
        self.assertGreaterEqual(report["radius"],0.01-1e-12)
        self.assertAlmostEqual(report["algorithm_upper"],0.01,places=9)
        self.assertEqual(report["status"],
                         "LINEAR_ELLIPSOID_RANK_UNCERTAIN_UPPER_ONLY")
        self.assertEqual(report["radius_kind"],"DUAL_UPPER_NUMERIC_ONLY")
        self.assertFalse(report["noise_rank_definitive"])
        self.assertGreater(report["noise_rank_threshold"],0.01)
        self.assertEqual(report["rank_ambiguous_positive_singular_values"],[0.01])

    def test_accept_singular_noise_and_reject_invalid_shapes(self):
        out = recover_scalar_goal(np.eye(2), np.eye(2),
                                  np.diag([0.1, 0.]), np.ones(2))
        self.assertAlmostEqual(out["radius"], 0.1, places=8)
        self.check_gap(out)
        with self.assertRaises(ValueError):
            recover_scalar_goal(np.eye(2), np.eye(1), np.eye(1), np.ones(2))



class SingularCommonModeRecovery(unittest.TestCase):
    def check_gap(self, out, tol=1e-7):
        self.assertLess(out["numerical_gap"], tol)
        self.assertLessEqual(out["feasible_witness_lower"], out["algorithm_upper"]+tol)

    def test_rectangular_shared_nuisance_exact_difference(self):
        E=np.array([[0.2],[0.2]])
        out=recover_scalar_goal(np.eye(2),np.eye(2),E,np.array([1.,-1.]))
        self.assertAlmostEqual(out["radius"],0.,places=8)
        np.testing.assert_allclose(out["measurement_weights"],[1.,-1.],atol=1e-7)
        self.check_gap(out)

    def test_same_shared_nuisance_still_limits_sum_goal(self):
        E=np.array([[0.2],[0.2]])
        out=recover_scalar_goal(np.eye(2),np.eye(2),E,np.array([1.,1.]))
        self.assertAlmostEqual(out["radius"],0.4,places=7)
        self.check_gap(out)

    def test_rank_deficient_square_factor(self):
        E=np.array([[0.2,0.],[0.2,0.]])
        out=recover_scalar_goal(np.eye(2),np.eye(2),E,np.array([1.,-1.]))
        self.assertAlmostEqual(out["radius"],0.,places=8)
        self.check_gap(out)

    def test_small_unshared_noise_restores_nonzero_radius(self):
        E=np.array([[0.2,0.],[0.2,0.05]])
        out=recover_scalar_goal(np.eye(2),np.eye(2),E,np.array([1.,-1.]))
        self.assertAlmostEqual(out["radius"],0.05,places=6)
        self.check_gap(out)

    def test_zero_noise_factor_is_exact_observation(self):
        E=np.empty((2,0))
        out=recover_scalar_goal(np.eye(2),np.eye(2),E,np.array([1.,1.]))
        self.assertAlmostEqual(out["radius"],0.,places=8)
        self.check_gap(out)

    def test_tiny_sensor_noise_dual_and_witness_are_consistent(self):
        u=np.array([[1.,-1.]])/np.sqrt(2.)
        report=recover_scalar_goal(np.eye(2),u,np.array([[1e-10]]),np.array([1.,-1.]))
        self.assertAlmostEqual(report["radius"],np.sqrt(2)*1e-10,delta=2e-13)
        self.assertLess(report["algorithm_upper"],2e-9)
        self.assertLess(report["numerical_gap"],2e-9)
        self.assertLessEqual(report["witness_whitened_observation_norm"],1+1e-8)



class GaussianQuadraticGoalOEDTests(unittest.TestCase):
    """Original-Gq Gaussian moment identities + independently constructed falsifiers."""

    def test_quadratic_target_reverses_parameter_info_sensor_ranking(self):
        H = np.array([[[1., 0.]], [[0., 1.]]])
        out = ger.rank_quadratic_goal_designs(
            [0., 0.], np.diag([9., 1.]), [0., 0.],
            np.diag([0., 2.]), H, np.ones((2, 1, 1)),
            candidate_names=["A", "B"])
        self.assertEqual(out["rank_best"]["Gq"], "B")
        self.assertEqual(out["rank_best"]["A"], "A")
        self.assertEqual(out["rank_best"]["parameter_MI"], "A")
        self.assertEqual(out["rank_best"]["Gl"], "A")
        self.assertAlmostEqual(out["candidates"][0]["Gq"], 2.)
        self.assertAlmostEqual(out["candidates"][1]["Gq"], 1.5)
        self.assertEqual([x["Gl"] for x in out["candidates"]], [0., 0.])

    def test_quadratic_data_average_matches_independent_gaussian_mc(self):
        mu = np.array([.2, -1.])
        P = np.array([[1.5, .3], [.3, .5]])
        b = np.array([.4, -.7])
        Q = np.array([[2., .2], [.2, -1.]])
        H = np.array([[1., .5], [-.2, 1.]])
        R = np.array([[.8, .1], [.1, .6]])
        out = ger.quadratic_goal_design(mu, P, b, Q, H, R,
                                        expansion_center=[0., 0.])
        post = np.asarray(out["posterior_cov"])
        rng = np.random.default_rng(46)
        posterior_means = rng.multivariate_normal(mu, P - post, size=120000)
        grad_at_means = b[None, :] + posterior_means @ Q.T
        mc = np.mean(np.einsum("ni,ij,nj->n", grad_at_means, post, grad_at_means))
        mc += .5 * np.trace((Q @ post) @ (Q @ post))
        self.assertAlmostEqual(out["Gq"], mc, delta=.025)
        self.assertLessEqual(out["Gq"], out["prior_goal_variance"] + 1e-8)

    def test_joint_model_error_cross_covariance_is_crucial(self):
        # The nominal H=0, but discrepancy d=x; a real observed y=d+noise
        # carries x, while treating d independent wrongly says no information.
        opts = dict(discrepancy_cov=[[1.]])
        right = ger.quadratic_goal_design(
            [0.], [[1.]], [0.], [[2.]], [[0.]], [[.1]],
            state_discrepancy_cross_cov=[[1.]], **opts)
        wrong = ger.quadratic_goal_design(
            [0.], [[1.]], [0.], [[2.]], [[0.]], [[.1]],
            state_discrepancy_cross_cov=[[0.]], **opts)
        self.assertAlmostEqual(right["posterior_cov"][0][0], 1/11)
        self.assertAlmostEqual(wrong["posterior_cov"][0][0], 1.)
        self.assertLess(right["Gq"], wrong["Gq"])

    def test_goal_risk_is_coordinate_invariant_but_raw_parameter_trace_is_not(self):
        T = np.diag([100., .01])
        inv = np.linalg.inv(T)
        P = np.array([[1.8, .2], [.2, .6]])
        H = np.array([[1., 2.]])
        b = np.array([.4, 1.])
        Q = np.array([[1.5, .2], [.2, 3.]])
        first = ger.quadratic_goal_design([0., 0.], P, b, Q, H, [[.2]])
        second = ger.quadratic_goal_design(
            [0., 0.], T @ P @ T.T, inv.T @ b, inv.T @ Q @ inv,
            H @ inv, [[.2]])
        self.assertAlmostEqual(first["Gq"], second["Gq"], places=10)
        self.assertAlmostEqual(first["Gl"], second["Gl"], places=10)
        self.assertGreater(abs(first["A"] - second["A"]), 100.)

    def test_nonlinear_observation_counterexample_exposes_missing_information(self):
        # Actual y=x**2 (noise=0) determines G=x**2 exactly, yet the
        # linearized observation at x=0 has H=0 and Gq incorrectly stays 2.
        linearization = ger.quadratic_goal_design(
            [0.], [[1.]], [0.], [[2.]], [[0.]], [[.1]])
        self.assertAlmostEqual(linearization["Gq"], 2.)

    def test_misspecified_discrepancy_can_reverse_candidate_ranking(self):
        no_error = ger.quadratic_goal_design([0.], [[1.]], [0.], [[2.]],
                                             [[1.]], [[.01]])
        alternative = ger.quadratic_goal_design([0.], [[1.]], [0.], [[2.]],
                                                [[.8]], [[.04]])
        large_error = ger.quadratic_goal_design(
            [0.], [[1.]], [0.], [[2.]], [[1.]], [[.01]],
            discrepancy_cov=[[2.]])
        self.assertLess(no_error["Gq"], alternative["Gq"])
        self.assertGreater(large_error["Gq"], alternative["Gq"])

    def test_zero_hessian_reduces_to_goal_gradient_posterior_covariance(self):
        P = np.array([[1., .4], [.4, 2.]])
        H = np.array([[1., -1.]])
        b = np.array([1., 2.])
        output = ger.quadratic_goal_design([0., 0.], P, b,
                                            np.zeros((2, 2)), H, [[.25]])
        expected = P - P @ H.T @ np.linalg.solve(H @ P @ H.T + [[.25]], H @ P)
        self.assertAlmostEqual(output["Gq"], b @ expected @ b)

    def test_rejects_impossible_prior_noise_and_joint_covariances(self):
        with self.assertRaises(ValueError):
            ger.quadratic_goal_design([0.], [[-1.]], [0.], [[2.]], [[1.]], [[1.]])
        with self.assertRaises(ValueError):
            ger.quadratic_goal_design([0.], [[1.]], [0.], [[2.]], [[1.]], [[0.]])
        with self.assertRaises(ValueError):
            ger.quadratic_goal_design(
                [0.], [[1.]], [0.], [[2.]], [[0.]], [[.1]],
                discrepancy_cov=[[1.]], state_discrepancy_cross_cov=[[2.]])

    def test_no_observation_matches_prior_goal_variance(self):
        P = np.diag([2., 1.])
        result = ger.quadratic_goal_design(
            [0., 0.], P, [.3, 2.], np.eye(2),
            np.empty((0, 2)), np.empty((0, 0)))
        self.assertAlmostEqual(result["Gq"], result["prior_goal_variance"])

    def test_quadratic_design_cli_is_end_to_end_and_preserves_legacy_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, dst = Path(tmp) / "oed.npz", Path(tmp) / "out.json"
            np.savez(src, prior_mean=np.zeros(2), prior_cov=np.diag([9., 1.]),
                     goal_gradient=np.zeros(2), goal_hessian=np.diag([0., 2.]),
                     candidate_observations=np.array([[[1., 0.]], [[0., 1.]]]),
                     candidate_noise_cov=np.ones((2, 1, 1)),
                     candidate_names=np.array(["A", "B"]))
            proc = subprocess.run(
                [sys.executable, str(Path(__file__).parent / "goal_ellipsoid_recovery.py"),
                 str(src), "--quadratic-design", "--output", str(dst)],
                text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            report = json.loads(dst.read_text())
            self.assertEqual(report["rank_best"]["Gq"], "B")
            self.assertEqual(report["rank_best"]["A"], "A")


if __name__ == "__main__":
    unittest.main()
