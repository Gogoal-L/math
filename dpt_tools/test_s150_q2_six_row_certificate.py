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



class OriginalSevenReadingJointOuterTests(unittest.TestCase):
    def test_singleton_bandwidth_is_valid_source_rc_midpoint(self):
        from s150_q2_six_row_certificate import original_rc_band_filter_fraction
        o=original_rc_band_filter_fraction(
            [F(0), F(1,10**11), F(2,10**11)],
            [F(0), F(1), F(0)], F(100), F(100),
            selected_stages=(1,2))
        self.assertEqual(o["steps_covered"],2)
        for lo,hi in o["sample_bounds_A"].values():
            self.assertLessEqual(lo,hi)

    def test_joint_band_envelope_cancels_offsets_and_preserves_nuisance(self):
        from s150_q2_six_row_certificate import certify_original_seven_reading_joint_outer
        bands=[(F(90)+F(j,4), F(90)+F(j+1,4), F(-1,100), F(1,100))
               for j in range(80)]
        o=certify_original_seven_reading_joint_outer(
            observed_dual=F("1.253692790291920247338006144666"),
            source_voltage_dual=(F(-1,10**6),F(1,10**6)),
            source_current_band_outers=bands,
            clock_V_bound=F(".00105"),clock_I_bound=F(".00045"))
        self.assertEqual(o["status"],"STORED_POINT_CONDITIONAL_NECESSARY_EXCLUSION")
        self.assertGreater(o["strict_margin"],0)
        self.assertFalse(o["full50_root_cover_certified"])
        self.assertEqual(o["weights_sum"],(F(0),F(0)))
        self.assertEqual(o["source_band_count"],80)
        with self.assertRaisesRegex(ValueError,"gap|band"):
            certify_original_seven_reading_joint_outer(
                observed_dual=F("1.253692790291920247338006144666"),
                source_voltage_dual=(F(0),F(0)),
                source_current_band_outers=bands[:-1],
                clock_V_bound=F(".00105"),clock_I_bound=F(".00045"))

    def test_per_coefficient_phase_box_is_not_a_waveform_amplitude_contract(self):
        from s150_q2_six_row_certificate import certify_original_seven_reading_joint_outer
        bands=[(F(90)+F(j,4), F(90)+F(j+1,4), F(-1,100),F(1,100))
               for j in range(80)]
        kwargs=dict(observed_dual=F("1.253692790291920247338006144666"),
                    source_voltage_dual=(F(-1,10**6),F(1,10**6)),
                    source_current_band_outers=bands,
                    clock_V_bound=F(".00105"),clock_I_bound=F(".00045"))
        disk=certify_original_seven_reading_joint_outer(**kwargs)
        self.assertGreater(disk["strict_margin"],0)
        coeff_box=certify_original_seven_reading_joint_outer(
            **kwargs,phase_V=F(".0283"),phase_I=F(".07075"))
        self.assertEqual(coeff_box["status"],"CANNOT_EXCLUDE")

    def test_source_replay_missing_original_hash_inputs_fail_closed(self):
        from s150_q2_six_row_certificate import replay_original_s150_seven_reading_80band
        with self.assertRaisesRegex(ValueError,"SOURCE_INPUTS_UNAVAILABLE"):
            replay_original_s150_seven_reading_80band(None,None,None)

    def test_root_tube_and_joint_noise_can_defeat_candidate_rejection(self):
        from s150_q2_six_row_certificate import certify_original_seven_reading_joint_outer
        bands=[(F(90)+F(j,4), F(90)+F(j+1,4), F(0),F(0))
               for j in range(80)]
        kwargs=dict(observed_dual=F("1.253692790291920247338006144666"),
                    source_voltage_dual=(F(0),F(0)),
                    source_current_band_outers=bands,
                    clock_V_bound=F(".00105"),clock_I_bound=F(".00045"))
        point=certify_original_seven_reading_joint_outer(**kwargs)
        tube=certify_original_seven_reading_joint_outer(
            **kwargs,root_radii=(F(1,100),F(1,100),F(1,100)))
        self.assertLess(tube["strict_margin"],point["strict_margin"])
        self.assertEqual(tube["status"],"CANNOT_EXCLUDE")
        noisy=certify_original_seven_reading_joint_outer(
            **kwargs,epsilon_V=F(1),epsilon_I=F(1))
        self.assertEqual(noisy["status"],"CANNOT_EXCLUDE")
        with self.assertRaises(ValueError):
            certify_original_seven_reading_joint_outer(
                **kwargs,root_radii=(F(-1),F(0),F(0)))


class SourceQ2OneKCLHeatAbsCuspTests(unittest.TestCase):
    def test_source_bounds_force_a_real_heat_abs_switch_on_the_kcl_lift(self):
        from s150_q2_six_row_certificate import certify_source_q2_kcl_heat_abs_switch
        from fractions import Fraction as F
        got=certify_source_q2_kcl_heat_abs_switch(
            sensor_left_upper_A="-0.04158004546562281",
            sensor_right_lower_A="3.4157913530608375",
            left_thermal_slope_upper_C_per_V="-2.705796e-6",
            right_thermal_slope_lower_C_per_V="2.705796e-6",
            six_row_contraction_upper="0.000278",
        )
        self.assertEqual(got["status"],"SOURCE_SEVEN_ROW_HEAT_ABS_CUSP_MUST_SPLIT")
        self.assertEqual(got["root_50d_certified"],False)
        self.assertGreater(got["opposite_slope_jump_lower_C_per_V"],F("5e-6"))

    def test_source_kcl_abs_non_crossing_or_zero_slope_never_asserts_cusp(self):
        from s150_q2_six_row_certificate import certify_source_q2_kcl_heat_abs_switch as check
        self.assertEqual(check(1,3,-1,1,"0.001")["status"],
                         "RETAIN_UNDECIDED")
        self.assertEqual(check(-1,1,0,1,"0.001")["status"],
                         "RETAIN_UNDECIDED")
        with self.assertRaises(ValueError):
            check(-1,1,-1,1,"1")


class OriginalS150FullTwelveRowToKCL26Tests(unittest.TestCase):
    def test_original_10_node_chart_eliminates_both_diodes_and_eight_thermal_rows(self):
        from s150_q2_six_row_certificate import certify_source_stage3616_26d_reduction
        from fractions import Fraction as F
        old_hex=(
            "0x1.90d8da971d80cp+4","0x1.9000d706653a8p+4",
            "0x1.9000001c3c2dcp+4","0x1.90000000018f6p+4",
            "0x1.90446617cedf0p+4","0x1.9000620e38254p+4",
            "0x1.900000161fde1p+4","0x1.9000000001912p+4",
        )
        old=tuple(F.from_float(float.fromhex(x)) for x in old_hex)
        output=certify_source_stage3616_26d_reduction(
            old,original_dt(),
            old_junction_V=(-130,-2),
            q1_gs_V=("-2.2132","-2.0531"),
            q2_gs_V=("6.1108","6.271"),
            q1_d_s_V=("135","135.3"),
            q2_d_s_V=("3.19","3.36"),
            q1_five_node_V=tuple(F.from_float(float.fromhex(x)) for x in (
                "0x1.2bf0be2eea417p+7","0x1.6d9cb673abfabp+3",
                "0x1.9609c4242a8a7p+3","0x1.2bf0dc944b121p+7",
                "0x1.da4c3edc813bep+3")),
            q2_five_node_V=tuple(F.from_float(float.fromhex(x)) for x in (
                "0x1.67138b6a8325dp+3","0x1.1bd6737f6c78cp+4",
                "0x1.c441ed8de0342p+3","0x1.67139f1fe1791p+3",
                "0x1.fc4c4bfd24625p+2")),
            adapter_kappa="1.007",
            source_law_sha256=LAW,source_adapter_sha256=ADAPTER,
            saved_cal_sha256=ARCHIVE)
        self.assertEqual(output["status"],"CONDITIONAL_50D_TO_26D_STAGE_ROOT_BIJECTION")
        self.assertEqual(output["eliminated_rows"],24)
        self.assertFalse(output["kcl26_roots_exist_certified"])
        self.assertTrue(output["q1_thermal_upper_C"][0] < F("25.054"))
        self.assertTrue(output["q2_thermal_upper_C"][0] < F("25.018"))
        self.assertTrue(output["max_banach_contraction"]<F(".000369"))

    def test_source_coil_be_elimination_and_drive_150V_sign(self):
        from s150_q2_six_row_certificate import source_be_coil_elimination
        from fractions import Fraction as F
        B=[[F(0)]*12 for _ in range(26)]
        B[0][0]=1;B[1][0]=-1
        B[0][11]=1;B[1][11]=-1
        result=source_be_coil_elimination([2,1]+[0]*24,[0]*12,B,[1]*12,F(1,10))
        self.assertEqual(result[0],F(1,10))
        self.assertEqual(result[11],-F(149,10))
        with self.assertRaises(ValueError):
            source_be_coil_elimination([0]*26,[0]*12,B,[0]+[1]*11,F(1,10))

    def test_source_26d_rejects_wrong_dt_or_unsafe_raw_thermal_predecessor(self):
        # The old contractor silently reused the source-stage q=0.00036889
        # at h=1 us, although the actual thermal contraction upper is >29.
        # These are UNRESOLVED input charts, not proofs of root exclusion.
        from s150_q2_six_row_certificate import certify_source_stage3616_26d_reduction
        centers1=tuple(F.from_float(float.fromhex(x)) for x in (
            "0x1.2bf0be2eea417p+7","0x1.6d9cb673abfabp+3",
            "0x1.9609c4242a8a7p+3","0x1.2bf0dc944b121p+7",
            "0x1.da4c3edc813bep+3"))
        centers2=tuple(F.from_float(float.fromhex(x)) for x in (
            "0x1.67138b6a8325dp+3","0x1.1bd6737f6c78cp+4",
            "0x1.c441ed8de0342p+3","0x1.67139f1fe1791p+3",
            "0x1.fc4c4bfd24625p+2"))
        kw=dict(old_junction_V=(-130,-2),
                q1_gs_V=("-2.2132","-2.0531"),q2_gs_V=("6.1108","6.271"),
                q1_d_s_V=("135","135.3"),q2_d_s_V=("3.19","3.36"),
                q1_five_node_V=centers1,q2_five_node_V=centers2,
                adapter_kappa="1.007",source_law_sha256=LAW,
                source_adapter_sha256=ADAPTER,saved_cal_sha256=ARCHIVE)
        source_dt=original_dt()
        ok=certify_source_stage3616_26d_reduction([F(25)]*8,source_dt,**kw)
        self.assertTrue(ok["archived_binary64_step_qualified"])
        self.assertTrue(ok["old_raw_temperature_native_chart_qualified"])
        self.assertFalse(ok["original_native_float_error_bound_qualified_in_ci"])
        with self.assertRaisesRegex(ValueError,"UNRESOLVED_SOURCE_DOMAIN.*binary64 dt"):
            certify_source_stage3616_26d_reduction([F(25)]*8,F("1e-6"),**kw)
        # Original NumPy ETH has RAW-tj terms; finite 1e307 can overflow
        # to NaN although effective tjc=260. No false certification.
        with self.assertRaisesRegex(ValueError,"UNRESOLVED_SOURCE_DOMAIN.*raw temperature"):
            certify_source_stage3616_26d_reduction([F("1e307")]*8,source_dt,**kw)
        with self.assertRaisesRegex(ValueError,"UNRESOLVED_SOURCE_DOMAIN.*raw temperature"):
            certify_source_stage3616_26d_reduction([F(261)]*8,source_dt,**kw)

    def test_26d_reduction_fail_closed_on_guard_and_old_diode_domain(self):
        from s150_q2_six_row_certificate import certify_source_stage3616_26d_reduction
        from fractions import Fraction as F
        old=[F(25)]*8
        centers1=tuple(F.from_float(float.fromhex(x)) for x in (
            "0x1.2bf0be2eea417p+7","0x1.6d9cb673abfabp+3",
            "0x1.9609c4242a8a7p+3","0x1.2bf0dc944b121p+7",
            "0x1.da4c3edc813bep+3"))
        centers2=tuple(F.from_float(float.fromhex(x)) for x in (
            "0x1.67138b6a8325dp+3","0x1.1bd6737f6c78cp+4",
            "0x1.c441ed8de0342p+3","0x1.67139f1fe1791p+3",
            "0x1.fc4c4bfd24625p+2"))
        kw=dict(q1_five_node_V=centers1,q2_five_node_V=centers2,
                old_junction_V=(-130,-2),q1_gs_V=(-3,-2.5),
                q2_gs_V=(6,7),q1_d_s_V=(135,136),q2_d_s_V=(3,4),
                adapter_kappa="1.007",source_law_sha256=LAW,
                source_adapter_sha256=ADAPTER,saved_cal_sha256=ARCHIVE)
        with self.assertRaises(ValueError):
            certify_source_stage3616_26d_reduction(
                old,original_dt(),**dict(kw,q1_gs_V=(2,3)))
        with self.assertRaises(ValueError):
            certify_source_stage3616_26d_reduction(
                old,original_dt(),**dict(kw,old_junction_V=(-130,1)))
        # Same gs/ds but a malicious out-of-box x would invalidate global heat.
        x_bad=list(centers1);x_bad[3]+=F(9,100)
        with self.assertRaisesRegex(ValueError,"ten-node|node chart"):
            certify_source_stage3616_26d_reduction(
                old,original_dt(),**dict(kw,q1_five_node_V=tuple(x_bad)))




class OriginalSourceXKCLAndPaperFiniteTailProofTests(unittest.TestCase):
    """Independent exact-rational positive and adversarial certificate checks."""

    def source_kwargs(self):
        return dict(
            h_s=original_dt(),source_law_sha256=LAW,
            source_adapter_sha256=ADAPTER,saved_cal_sha256=ARCHIVE)

    def test_source_two_x_KCL_corners_exclude_all_50D_roots_in_cells(self):
        from s150_q2_six_row_certificate import certify_original_source_x_kcl_outer
        centers={
            "Q1":("0x1.2bf0be2eea417p+7","0x1.2bf0dc944b121p+7",
                  "0x1.da4c3edc813bep+3"),
            "Q2":("0x1.67138b6a8325dp+3","0x1.67139f1fe1791p+3",
                  "0x1.fc4c4bfd24625p+2"),
        }
        for leg,(dd,xx,ss) in centers.items():
            d,x,s=[F.from_float(float.fromhex(z)) for z in (dd,xx,ss)]
            radius,thick=F(".04"),F(".001")
            # A WHOLE closed source cell, not just a stored source point:
            out=certify_original_source_x_kcl_outer(
                leg=leg,d_V=(d+radius-thick,d+radius),
                x_V=(x-radius,x-radius+thick),
                s_V=(s-radius,s+radius),**self.source_kwargs())
            self.assertEqual(out["status"],"SOURCE_EXACT_REAL_X_KCL_BOX_EXCLUDED")
            self.assertLess(out["residual_upper_A"],-F(700))
            self.assertGreater(out["strict_abs_residual_margin_A"],F(700))
            self.assertTrue(out["capacitance_interval_rational_verified"])
            self.assertTrue(out["conditional_full50_to_24d_KCL_preimage"])
            self.assertFalse(out["all50_stage_roots_certified"])
            self.assertFalse(out["native_float_error_certified"])

    def test_saved_q1_q2_x_node_point_keeps_possible_root(self):
        from s150_q2_six_row_certificate import certify_original_source_x_kcl_outer
        centers={
            "Q1":("0x1.2bf0be2eea417p+7","0x1.2bf0dc944b121p+7",
                  "0x1.da4c3edc813bep+3"),
            "Q2":("0x1.67138b6a8325dp+3","0x1.67139f1fe1791p+3",
                  "0x1.fc4c4bfd24625p+2"),
        }
        for leg,(dd,xx,ss) in centers.items():
            d,x,s=[F.from_float(float.fromhex(z)) for z in (dd,xx,ss)]
            tiny=F(1,1000000)
            out=certify_original_source_x_kcl_outer(
                leg=leg,d_V=(d-tiny,d+tiny),x_V=(x-tiny,x+tiny),
                s_V=(s-tiny,s+tiny),**self.source_kwargs())
            self.assertEqual(out["status"],"RETAIN_SOURCE_X_CELL_UNRESOLVED")
            self.assertLess(out["residual_lower_A"],0)
            self.assertGreater(out["residual_upper_A"],0)
            # A source-node chart outside certificate is NOT an excluded root.
            with self.assertRaisesRegex(ValueError,"UNRESOLVED_SOURCE_DOMAIN"):
                certify_original_source_x_kcl_outer(
                    leg=leg,d_V=(d,d+F(".041")),x_V=(x,x),s_V=(s,s),
                    **self.source_kwargs())
            with self.assertRaisesRegex(ValueError,"archived binary64"):
                certify_original_source_x_kcl_outer(
                    leg=leg,d_V=(d,d),x_V=(x,x),s_V=(s,s),
                    **dict(self.source_kwargs(),h_s=F("1e-6")))

    def test_two_source_thermal_predecessors_require_nearly_160C_memory_radius(self):
        from s150_q2_six_row_certificate import certify_source_thermal_predecessor_memory_gap
        for leg,strict_lower in (
                ("Q1",F("159.9994751909182")),
                ("Q2",F("159.9998425572754"))):
            out=certify_source_thermal_predecessor_memory_gap(
                leg,**self.source_kwargs())
            self.assertGreater(out["conditional_minimax_radius_C"],strict_lower)
            self.assertLess(out["conditional_minimax_radius_C"],F(160))
            self.assertFalse(out["same_full26d_KCL_legal_roots_verified"])
            self.assertFalse(out["legal_prep_two_worlds_verified"])

    def test_original_paper_bernstein_closed_cells_and_two_unresolved_roots(self):
        from s150_q2_six_row_certificate import certify_guard_cell_bernstein_tail_exclusion
        tail=F(1,512)
        for co,excluded in (
            ((F(3,32),F(7,128),F(1,32)),True),
            ((F(1,32),-F(5,128),F(1,32)),False),
            ((F(1,32),F(1,8),F(15,32)),True),
        ):
            out=certify_guard_cell_bernstein_tail_exclusion(co,co,tail)
            self.assertEqual(
                out["status"]=="CONDITIONAL_BERNSTEIN_FULL_CELL_ROW_EXCLUSION",
                excluded)
            self.assertFalse(out["all50_root_cover_certified"])
        def full_f(x):
            return (x-F(1,4))*(x-F(3,8))+x**4/(1024*(1-x/2))
        self.assertGreater(full_f(F(1,4)),0)
        self.assertLess(full_f(F(5,16)),0)
        self.assertGreater(full_f(F(3,8)),0)
        with self.assertRaises(ValueError):
            certify_guard_cell_bernstein_tail_exclusion((1,),(0,),tail)

    def test_original_paper_schur_finite_tail_coupling_and_singular_control(self):
        from s150_q2_six_row_certificate import certify_schur_finite_tail_coupling
        a=certify_schur_finite_tail_coupling(90,28,F(5,10**10),F(5,10**10))
        self.assertEqual(a["theta"],F(2521,2000000000))
        self.assertEqual(a["status"],"CONDITIONAL_WHOLE_BLOCK_INVERTIBLE")
        self.assertLess(a["rf_to_full_bound"],F(91))
        self.assertLess(a["rt_to_full_bound"],F(2540))
        self.assertFalse(a["dpt_44row_coupling_authenticated_in_ci"])
        # The finite A_ff=1 is invertible, but full A=I-[[0,2],[1/2,0]]
        # annihilates (2,1). theta=1 MUST NOT pass.
        b=certify_schur_finite_tail_coupling(1,2,F(1,2),0)
        self.assertEqual(b["theta"],1)
        self.assertEqual(b["status"],"RETAIN_BLOCK_COUPLING_UNRESOLVED")
        with self.assertRaises(ValueError):
            certify_schur_finite_tail_coupling(1,-1,0,0)



class OriginalSourceStage3616EightDStructuralBridgeTests(unittest.TestCase):
    """Behavioral source-topology tests: passive package and G11 signed guard."""

    def auth(self):
        return dict(
            h_s=original_dt(),source_law_sha256=LAW,
            source_adapter_sha256=ADAPTER,saved_cal_sha256=ARCHIVE)

    def test_original_package_14d_spd_and_exact_linear_root_for_arbitrary_boundary(self):
        from s150_q2_six_row_certificate import certify_original_source_package14_linear_lift
        from fractions import Fraction as F
        boundary=tuple(F(i,10) for i in range(12))
        old=tuple(F(j+1,100) for j in range(10))
        result=certify_original_source_package14_linear_lift(
            boundary_node12_V=boundary,old_package_coil10_A=old,
            command_V=15,**self.auth())
        self.assertEqual(result["status"],"ORIGINAL_SOURCE_PACKAGE14_UNIQUE_EXACT_LINEAR_LIFT")
        self.assertEqual(result["package_node_indices"],
            (2,4,5,10,11,12,13,14,16,17,22,23,24,25))
        self.assertEqual(len(result["node_voltage14_V"]),14)
        self.assertEqual(len(result["strict_positive_ldl_pivots_S"]),14)
        self.assertTrue(all(x>0 for x in result["strict_positive_ldl_pivots_S"]))
        self.assertTrue(all(
            sum(a*b for a,b in zip(row,result["node_voltage14_V"]))==rhs
            for row,rhs in zip(result["exact_package_matrix_S"],
                               result["exact_package_rhs_A"])))
        self.assertFalse(result["native_ieee_outward_enclosed"])
        self.assertFalse(result["complete_source_stage_root_certified"])
        # OLD-coil memory is algebraically essential; dropping it is unsound.
        changed=list(old);changed[0]+=F(1,1000)
        other=certify_original_source_package14_linear_lift(
            boundary_node12_V=boundary,old_package_coil10_A=changed,
            command_V=15,**self.auth())
        self.assertNotEqual(result["node_voltage14_V"],other["node_voltage14_V"])

    def test_package_elimination_rejects_wrong_source_domain(self):
        from s150_q2_six_row_certificate import certify_original_source_package14_linear_lift
        from fractions import Fraction as F
        kwargs=dict(boundary_node12_V=[0]*12,
                    old_package_coil10_A=[0]*10,command_V=15,**self.auth())
        for update in (dict(h_s=F("1e-6")),
                       dict(command_V=F(10)),
                       dict(source_law_sha256="WRONG"),
                       dict(boundary_node12_V=[0]*11),
                       dict(old_package_coil10_A=[0]*9)):
            with self.assertRaisesRegex(ValueError,"UNRESOLVED_SOURCE_DOMAIN"):
                certify_original_source_package14_linear_lift(
                    **dict(kwargs,**update))

    def test_original_g11_split_Gauss32_guard_monotone_and_narrow_roots(self):
        from s150_q2_six_row_certificate import certify_original_source_g11_w_guard
        from fractions import Fraction as F
        spec={
            "Q1":("0x1.9609c4242a8a7p+3","0x1.2bf0be2eea417p+7",
                  "0x1.2c18d8d76b477p+7",F(".124")),
            "Q2":("0x1.c441ed8de0342p+3","0x1.67138b6a8325dp+3",
                  "0x1.71159b94e7b55p+3",F(".0045")),
        }
        for leg,(gg,dd,ww,strict_width) in spec.items():
            g,d,w=[F.from_float(float.fromhex(x)) for x in (gg,dd,ww)]
            eps=F(".04")
            out=certify_original_source_g11_w_guard(
                leg=leg,g_V=(g-eps,g+eps),
                d_V=(d-eps,d+eps),**self.auth())
            self.assertEqual(out["status"],"ORIGINAL_SOURCE_G11_GUARDED_W_UNIQUE_LIFT")
            self.assertTrue(out["gauss32_signed_charge_single_panel_qualified"])
            self.assertTrue(out["forall_source_current_g_d_chart_w_root_exists"])
            self.assertGreater(out["gauss_charge_derivative_lower_F_per_s"],0)
            lo,hi=out["necessary_g_minus_w_V"]
            self.assertLess(hi-lo,strict_width)
            self.assertLess(lo,g-w)
            self.assertGreater(hi,g-w)
            self.assertFalse(out["all50_stage_roots_certified"])
            self.assertFalse(out["full_prepared_history_covered"])

    def test_g11_both_closed_corner_complements_exclude_full_source_root(self):
        from s150_q2_six_row_certificate import certify_original_source_g11_w_guard
        from fractions import Fraction as F
        spec={
            "Q1":("0x1.9609c4242a8a7p+3","0x1.2bf0be2eea417p+7",
                  "0x1.2c18d8d76b477p+7"),
            "Q2":("0x1.c441ed8de0342p+3","0x1.67138b6a8325dp+3",
                  "0x1.71159b94e7b55p+3"),
        }
        for leg,(gg,dd,ww) in spec.items():
            g,d,w=[F.from_float(float.fromhex(x)) for x in (gg,dd,ww)]
            eps,t=F(".04"),F(".001")
            out=certify_original_source_g11_w_guard(
                leg=leg,g_V=(g+eps-t,g+eps),d_V=(d-eps,d+eps),
                w_V=(w-eps,w-eps+t),**self.auth())
            self.assertEqual(out["status"],
                             "ORIGINAL_SOURCE_G11_W_KCL_CLOSED_BOX_EXCLUDED")
            self.assertLess(out["original_w_KCL_residual_upper_A"],0)
            self.assertGreater(out["strict_abs_residual_margin_A"],0)
            self.assertFalse(out["full50_allroot_cover_certified"])
            mid=certify_original_source_g11_w_guard(
                leg=leg,g_V=(g-F("1e-6"),g+F("1e-6")),
                d_V=(d-F("1e-6"),d+F("1e-6")),
                w_V=(w-F("1e-6"),w+F("1e-6")),**self.auth())
            self.assertEqual(mid["status"],"RETAIN_ORIGINAL_G11_W_CELL_UNRESOLVED")
            with self.assertRaisesRegex(ValueError,"UNRESOLVED_SOURCE_DOMAIN"):
                certify_original_source_g11_w_guard(
                    leg=leg,g_V=(g,g),d_V=(d,d),
                    w_V=(w-F(2),w-F(2)),**self.auth())



class AtomicFiniteTailSharedNuisanceBernsteinCoverTests(unittest.TestCase):
    def test_exact_shared_offset_tail_three_closed_cells_and_two_real_roots(self):
        from fractions import Fraction as F
        from s150_q2_six_row_certificate import certify_atomic_shared_nuisance_tail_cell
        # R1=b+x+w+e1, R2=b+x-1/4+2w+e2, w=x/4+w/2.
        # lambda=(1,-1) kills arbitrary common b; N=2 finite tail
        # gives pN=1/4-7x/16 and certified remainder 9/128.
        kw=dict(
            finite_bernstein_rows=((0,1),(-F(1,4),F(3,4))),
            shared_nuisance_matrix=((1,),(1,)),
            nuisance_annihilator=(1,-1),
            residual_tail_coupling=(1,2),
            tail_q_bernstein=(0,F(1,4)),tail_D=F(1,2),
            tail_terms=2,error_bounds=(F(1,256),F(1,256)))
        for cell,expect in (
           ((F(0),F(1,4)),"CONDITIONAL_BERNSTEIN_POSITIVE_CLOSED_CELL_EXCLUSION"),
           ((F(1,4),F(3,4)),"RETAIN_CLOSED_CELL_UNRESOLVED"),
           ((F(3,4),F(1)),"CONDITIONAL_BERNSTEIN_NEGATIVE_CLOSED_CELL_EXCLUSION"),
        ):
            got=certify_atomic_shared_nuisance_tail_cell(cell=cell,**kw)
            self.assertEqual(got["status"],expect)
            self.assertEqual(got["analytic_tail_and_noise_error_bound"],F(9,128))
            self.assertEqual(got["global_combined_bernstein_coefficients"],
                (F(1,4),-F(3,16)))
            self.assertFalse(got["source_full50_root_cover_certified"])
        x,w,b=F(1,2),F(1,4),-F(3,4)
        self.assertEqual(b+x+w,0)
        self.assertEqual(b+x-F(1,4)+2*w,0)

    def test_atomic_checker_hard_fail_on_undefined_tail_and_wrong_nuisance(self):
        from fractions import Fraction as F
        from s150_q2_six_row_certificate import certify_atomic_shared_nuisance_tail_cell
        kw=dict(
            finite_bernstein_rows=((0,1),(-F(1,4),F(3,4))),
            shared_nuisance_matrix=((1,),(1,)),
            nuisance_annihilator=(1,-1),residual_tail_coupling=(1,2),
            tail_q_bernstein=(0,F(1,4)),tail_D=F(1,2),
            tail_terms=2,error_bounds=(F(1,256),F(1,256)),
            cell=(F(0),F(1,4)))
        for changed in (
            dict(tail_D=1),
            dict(shared_nuisance_matrix=((1,),(-1,))),
            dict(error_bounds=(F(-1,256),F(1,256))),
            dict(cell=(F(1,2),F(1,4))),
        ):
            with self.assertRaises(ValueError):
                certify_atomic_shared_nuisance_tail_cell(
                    **dict(kw,**changed))



class MonotoneOriginalG12TwoCornerUpgradeTests(unittest.TestCase):
    def test_original_q2_nonzero_box_old_interval_fails_but_joint_lift_excludes(self):
        """New real source root exclusion that the old Cartesian row box missed."""
        from fractions import Fraction as F
        from s150_q2_six_row_certificate import certify_original_source_x_kcl_outer
        x=lambda z:F.from_float(float.fromhex(z))
        d=x("0x1.67138b6a8325dp+3")
        s=x("0x1.fc4c4bfd24625p+2")
        old=x("0x1.64640b421faa8p+3")-x("0x1.f6cdb13c29792p+2")
        h=original_dt()
        a,b=F(10000),F(1,10**7)
        D=(d-F(".04"),d)
        S=(s-F(".04"),s+F(".04"))
        cl,cu=F(600,10**12),F(650,10**12)
        def qlow(delta):
            return cl*delta if delta>=0 else cu*delta
        # Previous source audit decorrelated d,s from deltaQ during the
        # residual bound, so it cannot prove this strict interior cell.
        naive=(a*D[1]+b*S[1]-qlow(D[0]-S[1]-old)/h)/(a+b)
        # New source monotone derivative ∂x*/∂d>0 and ∂x*/∂s>0
        # pairs BOTH current maxima into one actual corner.
        joint=(a*D[1]+b*S[1]-qlow(D[1]-S[1]-old)/h)/(a+b)
        self.assertGreater(naive-joint,F("0.0002"))
        X=(joint+(naive-joint)/4,joint+(naive-joint)/2)
        self.assertLess(X[1],x("0x1.67139f1fe1791p+3")+F(".04"))
        dsl=D[0]-S[1]-old
        # The old independent-row interval crosses zero: negative control.
        old_row_lower=(a*(X[0]-D[1])+b*(X[0]-S[1])+
                       qlow(dsl)/h)
        self.assertLess(old_row_lower,0)
        got=certify_original_source_x_kcl_outer(
            leg="Q2",d_V=D,s_V=S,x_V=X,h_s=h,
            source_law_sha256=LAW,source_adapter_sha256=ADAPTER,
            saved_cal_sha256=ARCHIVE)
        self.assertEqual(got["status"],"SOURCE_EXACT_REAL_X_KCL_BOX_EXCLUDED")
        self.assertTrue(got["joint_monotone_x_corner_qualified"])
        self.assertGreater(got["joint_corner_strict_lower_residual_A"],F(1,2))
        self.assertGreater(got["strict_abs_residual_margin_A"],F(1,2))
        self.assertFalse(got["native_float_error_certified"])
        self.assertFalse(got["all50_stage_roots_certified"])




class OriginalSourcePassive16PortLiftTests(unittest.TestCase):
    def test_original_external_source_150v_and_spd_schur(self):
        from fractions import Fraction as F
        from s150_q2_six_row_certificate import (
            certify_original_source_passive16_port_lift,
        )
        kw=dict(retained_node10_V=tuple(F(i,10) for i in range(10)),
                old_coil12_A=tuple(F(i,100) for i in range(12)),
                command_V=15,h_s=original_dt(),
                source_law_sha256=LAW,source_adapter_sha256=ADAPTER,
                saved_cal_sha256=ARCHIVE)
        q=certify_original_source_passive16_port_lift(**kw)
        self.assertEqual(q["original_two_port_residual_A"],(0,0))
        self.assertTrue(all(v>0 for v in
                     q["strict_package_ldl_pivots_S"]+
                     q["strict_schur_pivots_S"]))
        self.assertEqual(q["original_D_coil_150V_offset_A"],
                         F(150)*original_dt()/F("100e-6"))
        self.assertFalse(q["complete_original_six_node_roots_certified"])
        # An old external D-current affects the new D/sl root.
        changed=list(kw["old_coil12_A"])
        changed[11]+=F(1)
        qq=certify_original_source_passive16_port_lift(
            **dict(kw,old_coil12_A=changed))
        self.assertNotEqual(q["port_D_sl_V"],qq["port_D_sl_V"])
        with self.assertRaisesRegex(ValueError,"UNRESOLVED_SOURCE_DOMAIN"):
            certify_original_source_passive16_port_lift(
                **dict(kw,command_V=10))

if __name__=="__main__":
    unittest.main()
