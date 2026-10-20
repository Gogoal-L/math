"""Source-original Q2 ON subsystem proof gates, exact rational algebra."""
import importlib
import unittest
from fractions import Fraction as F

OLD_T_HEX=(
    "0x1.90446617cedf0p+4",
    "0x1.9000620e38254p+4",
    "0x1.900000161fde1p+4",
    "0x1.9000000001912p+4",
)
DT_HEX="0x1.b7cdfd9d80000p-37"
ARCHIVE="baafdd8cb489adb186677658c4a8031130cc53a9a1854c4997211d437daf8b3e"
LAW="51b78f729393d29745f59ca150adfef69e1847bf26a8853c6cef3d6be9e2083d"
ADAPTER="7f03e36809caf3dea1295cf58d7dd70c413ef7991472a5e6eec3405da18f5669"

def original_old_T():
    return tuple(F.from_float(float.fromhex(x)) for x in OLD_T_HEX)
def original_dt():
    return F.from_float(float.fromhex(DT_HEX))


class SourceQ2OnSixRowCertificateTests(unittest.TestCase):
    def auditor(self):
        try:
            return importlib.import_module("s150_q2_six_row_certificate")
        except ModuleNotFoundError as error:
            self.fail(f"missing behavior implementation: {error}")

    def test_source_thermal_matrix_exact_old50_projection(self):
        cert=self.auditor()
        beta,alpha,zeta=cert.source_thermal_affine_exact(original_old_T(),original_dt())
        self.assertEqual(len(beta),4)
        self.assertEqual(len(alpha),4)
        self.assertAlmostEqual(float(beta[0]),25.016698923488022,places=10)
        self.assertAlmostEqual(float(alpha[0]),9.541983305290374e-9,places=14)
        self.assertAlmostEqual(float(zeta),.9999998503922385,places=11)
        self.assertTrue(all(x>0 for x in alpha))

    def test_declared_original_on_cell_has_one_six_row_root(self):
        cert=self.auditor()
        out=cert.certify_q2_on_subsystem(
            original_old_T(), original_dt(), source_kappa="1.007",
            source_law_sha256=LAW,source_adapter_sha256=ADAPTER,
            saved_cal_sha256=ARCHIVE,
            body_left_upper_V="-.129999999999",
            body_right_lower_V=".119999999999",
            channel_temperature_derivative_bound_A_per_C="397.305",
            drain_span_abs_bound_V="3.5",heat_upper_W="24000",
        )
        self.assertEqual(out["status"],"SIX_ROW_SOURCE_ENVELOPE_CERTIFIED_CONDITIONAL")
        self.assertLess(out["banach_contraction"],F("2e-5"))
        self.assertGreater(out["root_thermal_interval_C"][0],F(25))
        self.assertLess(out["root_thermal_interval_C"][1],F("25.04"))
        self.assertEqual(out["diode_root_vj_interval_V"],(F(-3),F(-2)))
        self.assertFalse(out["all_fifty_rows_certified"])
        self.assertFalse(out["all_root_history_covered"])
        self.assertLess(out["old_T0_delta_inner_interval_C"][0],F("-.016"))
        self.assertGreater(out["old_T0_delta_inner_interval_C"][1],F(".023"))
        self.assertLess(out["old_T0_delta_outer_exclusion_C"][0],F("-.0169"))
        self.assertGreater(out["old_T0_delta_outer_exclusion_C"][1],F(".0233"))

    def test_source_adapter_or_uncertified_bounds_fail_closed(self):
        cert=self.auditor()
        common=dict(source_law_sha256=LAW,source_adapter_sha256=ADAPTER,
                    saved_cal_sha256=ARCHIVE,
                    body_left_upper_V="-.129999999999",
                    body_right_lower_V=".119999999999",
                    channel_temperature_derivative_bound_A_per_C="397.305",
                    drain_span_abs_bound_V="3.5",heat_upper_W="24000")
        with self.assertRaisesRegex(ValueError,"kappa"):
            cert.certify_q2_on_subsystem(
                original_old_T(),original_dt(),source_kappa="1.0",**common)
        with self.assertRaisesRegex(ValueError,"root bracket"):
            cert.certify_q2_on_subsystem(
                original_old_T(),original_dt(),source_kappa="1.007",
                **dict(common,body_left_upper_V="0.1"))
        with self.assertRaisesRegex(ValueError,"self-map"):
            cert.certify_q2_on_subsystem(
                original_old_T(),original_dt(),source_kappa="1.007",
                **dict(common,heat_upper_W="1e10"))


class OriginalSourceRCBandwidthOuterTests(unittest.TestCase):
    def test_exact_rational_two_step_filter_outer_covers_direct_ode_solution(self):
        import math
        from s150_q2_six_row_certificate import (
            original_rc_band_filter_fraction as verify,
            exact_machin_pi_interval,
        )
        piL,piU=exact_machin_pi_interval()
        self.assertTrue(F("3.14159265358979") < piL < piU < F("3.14159265358980"))
        times=[F(0),F(1,10**11),F(2,10**11)]
        currents=[F(0),F(1),F(0)]
        out=verify(times,currents,F(90),F(110),selected_stages=(1,2))
        self.assertEqual(out["status"],"RC_FILTER_INTERVAL_OUTER_NOT_ROOT_COVER")
        for mhz in (90.,95.,100.,105.,110.):
            x=2*math.pi*mhz*1e6*float(times[1]-times[0])
            E=math.exp(-x)
            c0,c1,c2=E,(1-E)/x-E,1-(1-E)/x
            f1=c2
            f2=c0*f1+c1
            for index,value in ((1,f1),(2,f2)):
                lo,hi=out["sample_bounds_A"][index]
                self.assertLess(float(lo)-1e-11,value)
                self.assertGreater(float(hi)+1e-11,value)
        self.assertTrue(out["sample_bounds_A"][1][1]>out["sample_bounds_A"][1][0])

    def test_source_rc_invalid_frequency_and_clock_fail_closed(self):
        from s150_q2_six_row_certificate import original_rc_band_filter_fraction as verify
        with self.assertRaises(ValueError):
            verify([0,1,1],[0,1,2],90,110)
        with self.assertRaises(ValueError):
            verify([0,1],[0,1],110,90)
        with self.assertRaises(ValueError):
            verify([0,1],[0,1],90,110,selected_stages=(2,))



if __name__=="__main__":
    unittest.main()
