"""Exact Q3 source-coil/charge dual controls and raw-ETH source behavior.

The tests only exercise explicit mathematical models and source-literal decimals.
They do NOT certify a full S150 50D root or a deployable charge sensor.
"""
import importlib
import unittest
from fractions import Fraction as F


class SourceCoilChargeCheckpointCertificate(unittest.TestCase):
    def load(self):
        try:
            return importlib.import_module("goal_charge_checkpoint")
        except ModuleNotFoundError as error:
            self.fail(f"missing certifier implementation: {error}")

    def test_exact_primal_dual_matches_joint_two_checkpoint_radius(self):
        cert = self.load()
        result = cert.certify_two_zero_charge_rows(
            [3, 4, 1, 2],
            [[1, 0, 1, 0], [0, 1, 0, 1]],
            (2, 3),
        )
        self.assertEqual(result["radius"], F(4))
        self.assertEqual(result["unconstrained_radius"], F(10))
        self.assertEqual(result["primal"], result["dual"])
        self.assertEqual(result["witness"], (F(1), F(1), F(-1), F(-1)))
        self.assertEqual(result["checkpoint_residuals"], (F(0), F(0)))

    def test_coupled_checkpoint_pivot_cramer_exact(self):
        # Nonzero off-diagonal entries expose the wrong c0[q]/c1[p] cofactor.
        result = self.load().certify_two_zero_charge_rows(
            [4, 6, 0], [[1, 2, 1], [3, 4, 1]], (0, 1)
        )
        self.assertEqual(result["radius"], F(2))
        self.assertEqual(result["witness"], (F(-1), F(1), F(-1)))
        self.assertEqual(result["checkpoint_residuals"], (F(0), F(0)))
        self.assertEqual(result["primal"], result["dual"])

    def test_bad_pivot_cannot_fake_a_sharp_radius(self):
        cert = self.load()
        with self.assertRaisesRegex(ValueError, "infeasible pivot"):
            cert.certify_two_zero_charge_rows(
                [0, 0, 10000, 2],
                [[1, 0, 100, 0], [0, 1, 0, 1]],
                (0, 1),
            )

    def test_one_charge_row_exact_primal_dual_and_bad_pivot(self):
        cert = self.load()
        got = cert.certify_one_zero_charge_row([3, 1], [1, 1], pivot=1)
        self.assertEqual(got["radius"], F(2))
        self.assertEqual(got["unconstrained_radius"], F(4))
        self.assertEqual(got["witness"], (F(1), F(-1)))
        self.assertEqual(got["checkpoint_residual"], F(0))
        with self.assertRaisesRegex(ValueError, "infeasible pivot"):
            cert.certify_one_zero_charge_row([0, 100], [1, 100], pivot=0)

    def test_coil_be_and_trapezoid_charge_rows(self):
        cert = self.load()
        b, charge = cert.coil_be_goal_charge_rows(
            [0, 1, 2, 3, 4], F(1), F(1), F(1), 2
        )
        self.assertEqual(b, (F(10), F(9), F(7), F(4)))
        self.assertEqual(charge[0], (F(3, 2), F(1, 2), F(0), F(0)))
        self.assertEqual(charge[1], (F(2), F(2), F(3, 2), F(1, 2)))

    def test_nonuniform_binary64_source_time_steps_change_exact_charge_rows(self):
        cert=self.load()
        b,C=cert.coil_be_goal_charge_rows(
            [0,1,2,3,4],[1,2,1,3],1,1,2)
        self.assertEqual(b,(F(10),F(18),F(7),F(12)))
        self.assertEqual(C[0],(F(5,2),F(2),F(0),F(0)))
        self.assertEqual(C[1],(F(4),F(8),F(7,2),F(9,2)))
        self.assertNotEqual(C[1],(F(2),F(2),F(3,2),F(1,2)))
        with self.assertRaises(ValueError):
            cert.coil_be_goal_charge_rows([0,1,2,3,4],[1,2,3],1,1,2)

    def test_raw_temperature_source_eth_does_not_flatten_after_260c(self):
        cert = self.load()
        low0 = cert.original_eth_fraction(F(-4), F(260))
        low1 = cert.original_eth_fraction(F(-4), F(261))
        hi0 = cert.original_eth_fraction(F(14), F(260))
        hi1 = cert.original_eth_fraction(F(14), F(261))
        self.assertEqual((low0, low1), (F("-0.709724832"), F("-0.714812832")))
        self.assertEqual((hi0, hi1), (F("10.556083680"), F("10.285127680")))
        self.assertEqual(low1 - low0, F("-0.005088"))
        self.assertEqual(hi1 - hi0, F("-0.270956"))


    def test_three_read_shared_bias_exact_primal_dual_50pct_threshold(self):
        cert=self.load()
        from fractions import Fraction as F
        b=(F(7,4),F(-3,4),F(2),F(1))
        C=((F(1,4),F(1,4),F(1),F(0)),
           (F(1,4),F(-1,4),F(0),F(1)))
        u=(F(1),F(-1),F(3,8),F(-1,2))
        rho0=F(3,16)
        for B,rho in ((F(0),F(3,8)),(F(3,32),F(9,32)),
                      (F(3,16),F(3,16)),(F(1),F(3,16))):
            m=min(B,rho)
            e=(m,m-F(3,8),m-F(3,8))
            got=cert.certify_three_read_shared_bias_dual(
                b,C,(F(2),F(1)),rho,B,
                witness=u,measurement_errors=e,
            )
            self.assertEqual(got["radius"],F(11,4))
            self.assertEqual(got["primal"],got["dual"])
            self.assertEqual(got["unconstrained_radius"],F(11,2))
            self.assertEqual(got["charge_residuals"],(F(0),F(0)))
            self.assertEqual(rho,rho0+max(F(0),rho0-B))

    def test_three_read_joint_error_rejects_independent_difference_and_bad_bias(self):
        cert=self.load()
        from fractions import Fraction as F
        b=(F(7,4),F(-3,4),F(2),F(1))
        C=((F(1,4),F(1,4),F(1),F(0)),
           (F(1,4),F(-1,4),F(0),F(1)))
        with self.assertRaises(ValueError):
            cert.certify_three_read_shared_bias_dual(
                b,C,(2,1),F(3,16),F(0),
                witness=(1,-1,F(3,8),F(-1,2)),
                measurement_errors=(F(3,16),F(-3,16),F(-3,16)),
            )
        with self.assertRaises(ValueError):
            cert.certify_three_read_shared_bias_dual(
                b,C,(2,1),F(-1),F(0))


if __name__ == "__main__":
    unittest.main()
