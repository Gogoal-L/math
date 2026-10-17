"""Saved controller-proxy float64 coefficients: scoped mathematical receipt.

Read-only source: Power Semiconductor/docs/derivations/replay/
goal27_projective_bank.json (2026-10-12). Not a source/native replay.
Only m0, M5, g6, G0 and six radii are copied to this math fixture.
"""
import itertools
import unittest
from fractions import Fraction as F
from projective_command_proxy import certify, decode, forward, sensor_certificate

DATA = {
    "m0": [-0.0016640707277048579, 3.7571537612733383,
           5.883248703375352, 4.526171063051257, 5.459951588672399],
    "M": [
        [-0.000023895279967453196, -0.000026813609720260868,
         0.0000684200679268785, 0.00006385537052217241, 0,
         -0.000005078342006996796],
        [0.05112501880271227, 0.056025885267838874, 0.061413660163346886,
         -0.04196500769328335, 3.428494078379359, 0.013561735822562274],
        [-0.08896202887928366, -0.09749379769442325, -0.10684234884821434,
         0.03881664387867946, -12.04706992551107, -0.026519406772024925],
        [0.04284693450714974, 0.046956238204106444,
         0.05145817505174866, -0.19481116671395332,
         5.2596208562387226, 0.0016019459671505732],
        [-0.012080216552727787, -0.013238773899610172,
         -0.014508025108265637, 0.17355663076678793,
         -1.4537656119859788, -0.0008656574519533596]
    ],
    "g": [1.5991445248105335e-10, 1.4328682864291714e-10,
          2.308001252833172e-10, -9.124633382950655e-8,
          -0.0000030612283425329477, 0],
    "G0": 1.1175844305356859e-05,
    "radius": [0.14, 0.14, 0.14, 0.28, 0.018, 10]
}


class CommandConditionedProxy(unittest.TestCase):
    def test_full_prep_cube_exact_det_sign(self):
        out = certify(DATA)
        self.assertEqual(out["status"], "CERTIFIED_STORED_PROXY_ONLY")
        self.assertLess(out["det_max"], 0)
        self.assertGreater(out["D_min"], 0)
        self.assertAlmostEqual(float(out["det_min"]), -0.012864031844605972, 14)
        self.assertAlmostEqual(float(out["det_max"]), -0.012844315469064994, 14)

    def test_exact_all_729_command_and_unknown_corners(self):
        for a in itertools.product((-1, 0, 1), repeat=3):
            for u in itertools.product((-1, 0, 1), repeat=3):
                m = forward(DATA, a, u)
                out = decode(DATA, a, m)
                self.assertEqual(out["u"], tuple(map(F, u)))
                self.assertEqual(out["record_gain"], 1)

    def test_common_gain_offset_invariance(self):
        a = (F(1, 2), F(-1, 4), F(0))
        u = (F(3, 5), F(-1, 2), F(1, 3))
        currents = forward(DATA, a, u)
        gain, offset = F(1001535, 1000000), F(3, 100)
        y = tuple(gain*x+offset for x in currents)
        out = decode(DATA, a, y)
        self.assertEqual(out["u"], u)
        self.assertEqual(out["record_gain"], gain)

    def test_full_proxy_hypothetical_joint_sensor_corners(self):
        out = sensor_certificate(DATA, F(1, 1000), F(9, 10))
        self.assertEqual(out["status"], "FINITE_CORNER_CERTIFIED_STORED_PROXY")
        self.assertEqual(out["count"], 2048)
        self.assertGreater(out["minimum_effective_gain"], 0)
        self.assertAlmostEqual(float(out["minimum_effective_gain"]),
                               0.8995834925637282, 12)
        self.assertAlmostEqual(float(out["max_abs_goal_error_nJ"]),
                               2.939193801102625, 11)

    def test_cross_command_q_only_witness_is_not_same_information(self):
        a_pos, a_neg = (F(1),)*3, (F(-1),)*3
        self.assertNotEqual(a_pos, a_neg)
        self.assertNotEqual(forward(DATA, a_pos, (0, 0, 0)),
                            forward(DATA, a_neg, (0, 0, 0)))

    def test_fails_closed_without_denominator_or_rank(self):
        invalid = {**DATA, "m0": [0]*5,
                   "M": [[0]*6 for _ in range(5)]}
        with self.assertRaises(ValueError):
            certify(invalid)
        with self.assertRaises(ValueError):
            decode(DATA, (2, 0, 0), [0, 1, 2, 3, 4])


class SourceGapIdentity(unittest.TestCase):
    def test_exact_common_dynamic_gain_and_offset_cancel(self):
        from projective_command_proxy import audit_source_gap
        a=(F(1,2),F(-1,4),F(1,5))
        u=(F(1,3),F(-1,5),F(1,2))
        m=forward(DATA,a,u)
        gain,offset=F(5,4),F(2,7)
        actual=tuple(gain*x+offset for x in m)
        goal=decode(DATA,a,m)["goal_J"]
        receipt=audit_source_gap(DATA,a,u,actual,goal)
        self.assertEqual(receipt["homogeneous_gain"],gain)
        self.assertEqual(receipt["joint_numerator_J"],0)
        self.assertEqual(receipt["goal_error_J"],0)

    def test_nonzero_correlated_observation_and_work_gaps_cancel(self):
        from projective_command_proxy import audit_source_gap
        a=(F(1,2),F(-1,4),F(1,5))
        u=(F(1,3),F(-1,5),F(1,2))
        shifted=(u[0]+F(1,10),u[1]-F(1,7),u[2]+F(1,9))
        actual=forward(DATA,a,shifted)
        goal=decode(DATA,a,actual)["goal_J"]
        receipt=audit_source_gap(DATA,a,u,actual,goal)
        self.assertEqual(receipt["joint_numerator_J"],0)
        self.assertEqual(receipt["goal_error_J"],0)
        self.assertNotEqual(receipt["goal_model_gap_J"],0)

    def test_reversed_source_readout_orientation_rejected(self):
        from projective_command_proxy import audit_source_gap
        a=(F(0),)*3
        u=(F(0),)*3
        reversed_currents=tuple(-m for m in forward(DATA,a,u))
        with self.assertRaises(ValueError):
            audit_source_gap(DATA,a,u,reversed_currents,F(1))

# Seven PREVIOUSLY EXPOSED, NONPROTECTED actual-S150 BE/filtered-CAL/target
# records (2026-10-11 accepted). They are NOT seven same-digital-PREP worlds,
# not a prospective holdout, and not a whole-source/root/guard certificate.
# Source identity: Power Semiconductor/pro_runs/20261010_pro18_goal_adequacy_frontier/
# artifacts/run_C/pro18c_submission/evidence.json, original_submission.zip
# SHA256 250aa4ea17514ffdeda3a51d95bedf8e034b181f97bdc254db29ddc36281b9c8.
# Records: pro18c_final_same_fiber_observations.json::records T00–T06 and
# pro18c_final_same_fiber_results.json::members T00–T06.
EXPOSED_SOURCE_POINT_RECEIPTS = [
    ((.2145431754097475, .1989710249221997, .26),
     (-.0016662905239417055, 3.755624581366593, 5.880856040851975,
      4.524329335110529, 5.457730705802027), 1.1175682423019277e-05),
    ((.24299803229881015, .23265778690598232, .2733333333333333),
     (-.0016655562650208966, 3.756134006102819, 5.8816531956177025,
      4.524942833021625, 5.458470574599871), 1.1175735258683418e-05),
    ((.2714847162858332, .26633529219614527, .2866666666666667),
     (-.001664816599379838, 3.75664375086834, 5.8824508478854725,
      4.525556715043073, 5.459210905747265), 1.117578930058725e-05),
    ((.3, .3, .3),
     (-.001664071488953948, 3.757153765114533, 5.883248919391443,
      4.526170920753471, 5.459951626164625), 1.1175844563502935e-05),
    ((.3285466058668199, .3336573710798238, .31333333333333335),
     (-.0016633210170261478, 3.757664115803705, 5.884047468824628,
      4.526785505145808, 5.460692813212907), 1.1175901060027933e-05),
    ((.3571222954486464, .36730204858967713, .32666666666666666),
     (-.001662565124926676, 3.758174703992945, 5.884846481633284,
      4.527400427118551, 5.46143438374844), 1.1175958779206933e-05),
    ((.38572942594214493, .4009383662254762, .33999999999999997),
     (-.0016618038452613643, 3.7586856143043756, 5.885645954234172,
      4.5280157126959555, 5.462176401904682), 1.1176017726225357e-05),
]


class ArchivedNonlinearSourcePointGate(unittest.TestCase):
    def _norm_prep(self, amplitudes):
        # Lift EACH binary64 stored input independently before subtraction.
        return tuple((F(amplitudes[j])-F(.3))/F(.14) for j in range(3))

    def test_original_accepted_seven_source_readouts_and_exact_noise_threshold(self):
        from projective_command_proxy import known_source_point_noise_gate
        rows = []
        for a_volts, current_A, signed_work_J in EXPOSED_SOURCE_POINT_RECEIPTS:
            self.assertEqual(len(current_A), 5)
            out = known_source_point_noise_gate(
                DATA, self._norm_prep(a_volts), current_A, signed_work_J,
                gain_lower=F(9,10), noise_abs_A=F(1,1000),
                goal_tolerance_J=F(1,10**9))
            self.assertEqual(out["status"], "POSTHOC_EXPOSED_SOURCE_POINT_ONLY")
            self.assertEqual(out["joint_noise_corners"], 32)
            self.assertGreater(out["minimum_effective_gain"], 0)
            rows.append(out)
        worst = max(float(out["worst_error_nJ"]) for out in rows)
        threshold = min(float(out["max_noise_for_goal_tolerance_A"])*1000
                        for out in rows)
        self.assertAlmostEqual(worst, 2.9283647861895816, places=10)
        self.assertAlmostEqual(threshold, 0.3402710153664446, places=11)
        self.assertEqual(rows[-1]["limiting_signs"], (1,-1,-1,1,1))
        self.assertEqual(rows[-1]["limiting_constraint"], "goal_lower")
        self.assertLess(threshold, 1)  # hypothetical 1mA does NOT meet 1nJ.

    def test_exposed_real_source_has_nonzero_model_error_at_zero_noise(self):
        from projective_command_proxy import known_source_point_noise_gate
        a, measured, future_goal = EXPOSED_SOURCE_POINT_RECEIPTS[-1]
        out = known_source_point_noise_gate(
            DATA, self._norm_prep(a), measured, future_goal,
            gain_lower=F(9,10), noise_abs_A=F(0),
            goal_tolerance_J=F(1,10**9))
        self.assertAlmostEqual(float(out["worst_error_nJ"]),
                               0.005601739350126236, places=11)
        self.assertGreater(out["max_noise_for_goal_tolerance_A"],0)

    def test_noise_orientation_rejected_and_no_spurious_forecast_claim(self):
        from projective_command_proxy import known_source_point_noise_gate
        a, measured, future_goal = EXPOSED_SOURCE_POINT_RECEIPTS[3]
        with self.assertRaises(ValueError):
            known_source_point_noise_gate(
                DATA, self._norm_prep(a), [-z for z in measured], future_goal,
                gain_lower=F(9,10), noise_abs_A=F(1,1000),
                goal_tolerance_J=F(1,10**9))

if __name__ == "__main__":
    unittest.main()
