"""Independent analytic behavior tests for a continuous goal-information radius."""
import unittest
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import numpy as np

from goal_ellipsoid_recovery import recover_scalar_goal


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


if __name__ == "__main__":
    unittest.main()
