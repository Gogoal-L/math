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
        self.assertEqual(hi, -F("0.006292235773735"))
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


class SourceEthContinuousRectangleTests(unittest.TestCase):
    def test_original_polynomial_interval_tiling_keeps_guard_frontier(self):
        from fractions import Fraction as F
        from s150_original_guard_replay import (
            classify_original_eth_guard_rectangle as classify,
            bisect_original_eth_guard_rectangle as cover,
        )
        band = ("25.0084", "25.0087")
        low = classify(band, ("2.70", "2.71"))
        high = classify(band, ("2.711", "2.72"))
        crossing = classify(band, ("2.710200", "2.710203"))
        self.assertEqual(low["mode"], "STRICT_LOW")
        self.assertEqual(high["mode"], "STRICT_HIGH")
        self.assertEqual(crossing["mode"], "RETAIN_BOTH_FRONTIER")
        self.assertGreater(F(low["strict_margin_V"]), 0)
        self.assertGreater(F(high["strict_margin_V"]), 0)
        self.assertEqual(crossing["strict_margin_V"], "0")
        # Even a point exactly on the true original-law switching curve
        # cannot be certified as one strict guard side.
        threshold = classify(
            (band[1],band[1]),("2.7","2.8"))["threshold_V"][0]
        touch = classify((band[1],band[1]),("2.70",threshold))
        self.assertEqual(touch["mode"], "RETAIN_BOTH_FRONTIER")

        partition = cover(band, ("2.70", "2.72"), depth=8)
        counts = partition["count_by_mode"]
        self.assertEqual(sum(counts.values()),len(partition["leaves"]))
        self.assertGreater(counts["STRICT_LOW"],0)
        self.assertGreater(counts["STRICT_HIGH"],0)
        self.assertGreater(counts["RETAIN_BOTH_FRONTIER"],0)
        for leaf in partition["leaves"]:
            a,b=map(F,leaf["gate_minus_source_V"])
            l,h=map(F,leaf["threshold_V"])
            if leaf["mode"] == "STRICT_LOW":
                self.assertLess(b,l)
            elif leaf["mode"] == "STRICT_HIGH":
                self.assertGreater(a,h)
            else:
                self.assertGreaterEqual(b,l)
                self.assertLessEqual(a,h)
            self.assertFalse(leaf["all_roots"])
        self.assertFalse(partition["all_roots"])
        self.assertEqual(partition["goal27"],"NOT_CERTIFIED")

    def test_never_guess_branch_from_reversed_or_unqualified_input(self):
        from s150_original_guard_replay import (
            classify_original_eth_guard_rectangle as classify,
            bisect_original_eth_guard_rectangle as cover,
        )
        with self.assertRaises(ValueError):
            classify(("25.01","25.00"),("2.7","2.8"))
        with self.assertRaises(ValueError):
            classify(("25","25"),("2.71","2.70"))
        with self.assertRaises(ValueError):
            classify(("25","25"),(2.7,2.8))
        with self.assertRaises(ValueError):
            cover(("25","25"),("2.7","2.8"),depth=-1)
        with self.assertRaises(ValueError):
            cover(("25","25"),("2.7","2.8"),depth=True)


    def test_full50_source_box_guard_projection_and_missing_history(self):
        from s150_original_guard_replay import (
            classify_original_eth_guard_state50_box,
        )
        box = [("0","0") for _ in range(50)]
        box[46] = ("25.0084","25.0087")
        box[18] = ("2.700","2.710")
        box[21] = ("0","0")
        low=classify_original_eth_guard_state50_box(box)
        self.assertEqual(low["mode"],"STRICT_LOW")
        self.assertEqual(low["full50_input_projection"]["temperature_index"],46)
        self.assertFalse(low["source_root_qualified"])
        self.assertFalse(low["valid_predecessor_history"])
        box[18] = ("2.711","2.72")
        self.assertEqual(classify_original_eth_guard_state50_box(box)["mode"],
                         "STRICT_HIGH")
        # Actual correlation between g and s is not supplied; interval
        # subtraction MUST retain a possible ETH interface.
        box[18] = ("2.710","2.712")
        box[21] = ("0",".001")
        self.assertEqual(classify_original_eth_guard_state50_box(box)["mode"],
                         "RETAIN_BOTH_FRONTIER")
        with self.assertRaises(ValueError):
            classify_original_eth_guard_state50_box(box[:-1])
        bad = list(box)
        bad[19]=("3","2")
        with self.assertRaises(ValueError):
            classify_original_eth_guard_state50_box(bad)
