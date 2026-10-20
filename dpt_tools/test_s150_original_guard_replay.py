"""Original S150 Pro18E gate replay contract (synthetic CI inputs only)."""
import unittest
import numpy as np
from s150_original_guard_replay import scan_original_eth_guard


class OriginalEthGuardReplayTests(unittest.TestCase):

    def test_sha_pinned_original_real_eth_temperature_interval_recomputed(self):
        from fractions import Fraction as F
        from s150_original_guard_replay import certify_original_eth_seam_band
        r = certify_original_eth_seam_band()
        self.assertEqual(r["status"], "ORIGINAL_SOURCE_DECIMAL_REAL_INTERVAL_ONLY")
        self.assertEqual(r["source_root_status"], "NOT_CERTIFIED")
        self.assertEqual(r["guard_reset_status"], "UNRESOLVED")
        lo, hi = [F(x) for x in r["eth_high_minus_low_V_outward"]]
        g_lo, g_hi = [F(x) for x in r["threshold_gstar_V_outward"]]
        r_lo, r_hi = [F(x) for x in r["body_reff_ohm_outward"]]
        self.assertLess(lo, hi)
        self.assertLess(hi, -F("0.006292235773735"))
        self.assertEqual(-hi, F(r["minimum_compensating_body_voltage_V_strict"]))
        self.assertGreater(g_lo, 2)
        self.assertLess(g_hi, 3)
        self.assertGreater(r_lo, 0)
        self.assertLess(r_hi, F("0.071"))
        self.assertGreater((-hi) / r_hi, F(".0898"))
        # The controller must not promote literal-source arithmetic
        # into source-root coverage or a reset/Goal27 certificate.
        self.assertEqual(r["full_CAL_goal27_status"], "NOT_CERTIFIED")

    def test_source_coordinate_orientation_and_guard_margins(self):
        t=np.array([0.,1e-9,2e-9])
        y=np.zeros((3,50),float)
        y[:,46]=25.
        threshold=8.381e-6*25**2-4.696e-3*25+2.8224
        y[:,18]=threshold+np.array([-.010,-.001749,+.003530])
        y[:,21]=0.
        rep=scan_original_eth_guard(t,y)
        self.assertEqual(rep["status"],"POINT_SOURCE_GUARD_ONLY_NOT_ALL_ROOT")
        self.assertEqual(rep["min_abs_margin_index"],1)
        self.assertEqual(rep["sign_crossing_pairs"],[[1,2]])
        self.assertTrue(rep["independent_0p8mV_plus_0p001C_preserves_saved_signs"])
        self.assertTrue(rep["independent_1mV_gate_source_can_flip_weakest"])
        self.assertGreater(rep["min_abs_margin_V"],.001748)
        self.assertLess(rep["min_abs_margin_V"],.001750)

    def test_root_or_guard_unknown_is_never_reported_complete(self):
        t=np.array([0.,1e-9])
        y=np.zeros((2,50));y[:,46]=25.
        threshold=8.381e-6*25**2-4.696e-3*25+2.8224
        y[:,18]=threshold
        rep=scan_original_eth_guard(t,y)
        self.assertFalse(rep["independent_0p8mV_plus_0p001C_preserves_saved_signs"])
        self.assertEqual(rep["status"],"POINT_SOURCE_GUARD_ONLY_NOT_ALL_ROOT")
        with self.assertRaises(ValueError):
            scan_original_eth_guard([0.,0.],y)
        with self.assertRaises(ValueError):
            scan_original_eth_guard(t,np.zeros((2,49)))
