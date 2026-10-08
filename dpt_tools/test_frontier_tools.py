"""Behavioral tests of finite command congruence and noisy-goal ambiguity."""
import unittest
import numpy as np

import goal_ambiguity_audit as gaa
import command_word_audit as cwa


class GoalAmbiguityAuditTests(unittest.TestCase):
    def test_two_sigma_bound_exact_minimax_on_finite_bank(self):
        # Pair 0-1 and 1-2 can share a radius-0.25 measurement; 0-2 cannot.
        obs = np.array([[0.0], [0.5], [1.0]])
        goal = np.array([0.0, 2.0, 5.0])
        result = gaa.audit(obs, goal, 0.25)
        self.assertAlmostEqual(result["baseline"]["goal_diameter"], 3.0)
        self.assertAlmostEqual(result["baseline"]["minimax_scalar_error"], 1.5)
        self.assertEqual(result["baseline"]["witness_indices"], [1, 2])

    def test_reused_archived_feature_resolves_compressed_ambiguity(self):
        # An additional feature of existing raw data can still help when O was lossy.
        obs = np.zeros((2, 1))
        goal = np.array([2.0, 7.0])
        candidates = np.array([[0.0], [1.0]])
        result = gaa.audit(obs, goal, 0.0, candidates=candidates,
                           candidate_noise_radius=0.0, candidate_names=["archived_feature"])
        self.assertAlmostEqual(result["baseline"]["minimax_scalar_error"], 2.5)
        self.assertAlmostEqual(result["candidates"][0]["minimax_scalar_error"], 0.0)
        self.assertEqual(result["candidates"][0]["name"], "archived_feature")

    def test_noisy_candidate_can_fail_to_discriminate(self):
        obs = np.zeros((2, 1))
        goal = np.array([0.0, 4.0])
        candidates = np.array([[0.0], [0.9]])
        result = gaa.audit(obs, goal, 0.0, candidates=candidates,
                           candidate_noise_radius=0.5)
        self.assertAlmostEqual(result["candidates"][0]["minimax_scalar_error"], 2.0)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            gaa.audit(np.array([[0.0], [float("nan")]]), np.array([0.0, 1.0]), 0.1)
        with self.assertRaises(ValueError):
            gaa.audit(np.array([[0.0]]), np.array([0.0]), -1.0)


class CommandWordAuditTests(unittest.TestCase):
    @staticmethod
    def _model():
        return {"commands": ["A", "B"], "states": {
            "h0": {"observation": "same", "goal": 0, "transitions": {"A": "a0", "B": "b0"}},
            "h1": {"observation": "same", "goal": 0, "transitions": {"A": "a1", "B": "b1"}},
            "a0": {"observation": "a", "goal": 0, "transitions": {"B": "yes"}},
            "a1": {"observation": "a", "goal": 0, "transitions": {"B": "no"}},
            "b0": {"observation": "b", "goal": 0, "transitions": {}},
            "b1": {"observation": "b", "goal": 0, "transitions": {}},
            "yes": {"observation": "y", "goal": 1, "transitions": {}},
            "no": {"observation": "n", "goal": 0, "transitions": {}},
        }}

    def test_two_step_word_separates_primitive_aliased_histories(self):
        report = cwa.audit(self._model())
        witnesses = [w for w in report["observation_alias_witnesses"]
                     if set(w["states"]) == {"h0", "h1"}]
        self.assertEqual(len(witnesses), 1)
        self.assertEqual(witnesses[0]["word"], ["A", "B"])
        self.assertEqual(witnesses[0]["kind"], "goal")
        self.assertNotEqual(report["state_to_class"]["h0"], report["state_to_class"]["h1"])

    def test_undefined_command_is_a_distinguishing_observation(self):
        model = {"commands": ["A"], "states": {
            "x": {"observation": "same", "goal": 0, "transitions": {"A": "x"}},
            "y": {"observation": "same", "goal": 0, "transitions": {}},
        }}
        report = cwa.audit(model)
        self.assertEqual(report["observation_alias_witnesses"][0]["word"], ["A"])
        self.assertEqual(report["observation_alias_witnesses"][0]["kind"], "definedness")

    def test_equivalent_states_merge_into_one_transition_class(self):
        model = {"commands": ["A"], "states": {
            "x": {"observation": "same", "goal": 5, "transitions": {"A": "x"}},
            "y": {"observation": "same", "goal": 5, "transitions": {"A": "y"}},
        }}
        report = cwa.audit(model)
        self.assertEqual(report["minimal_classes"], 1)
        self.assertEqual(report["observation_alias_witnesses"], [])

    def test_bad_transition_target_rejected(self):
        bad = {"commands": ["A"], "states": {"x": {"goal": 0, "transitions": {"A": "missing"}}}}
        with self.assertRaises(ValueError):
            cwa.audit(bad)


import measurement_factor_audit as mfa

class MeasurementFactorTests(unittest.TestCase):
    def test_all_direction_factor_requires_existing_observation_term(self):
        do = np.array([[1.0, 0.0]])
        dp = np.array([[0.0, 1.0]])
        dg = np.array([[1.0, 1.0]])
        rep = mfa.audit(do, dg, dp, radius=0.2, c_obs=0.0, c_goal=0.0, c_measurement=0.0)
        self.assertTrue(rep["factorization_exact_at_tangent"])
        self.assertAlmostEqual(rep["observation_gain_2norm"], 1.0)
        self.assertAlmostEqual(rep["measurement_gain_2norm"], 1.0)
        self.assertAlmostEqual(rep["conditional_prediction_bound"], 0.0)

    def test_exact_observation_fiber_requires_observation_curvature(self):
        do = np.array([[1.0, 0.0]])
        dp = np.array([[0.0, 1.0]])
        dg = np.array([[1.0, 1.0]])
        rep = mfa.audit(do, dg, dp, radius=0.2, c_obs=1.0, c_goal=0.0, c_measurement=0.0)
        self.assertAlmostEqual(rep["conditional_prediction_bound"], 0.04)

    def test_missing_observation_remainder_never_emits_certificate(self):
        do = np.array([[1.0, 0.0]])
        dp = np.array([[0.0, 1.0]])
        dg = np.array([[1.0, 1.0]])
        rep = mfa.audit(do, dg, dp, radius=0.2, c_obs=None, c_goal=0.0, c_measurement=0.0)
        self.assertIsNone(rep["conditional_prediction_bound"])
        self.assertEqual(rep["status"], "MISSING_REMAINDER_ASSUMPTIONS")

    def test_linear_residual_is_charged_when_unrecoverable_goal(self):
        do = np.array([[1.0, 0.0]])
        dp = np.zeros((0, 2))
        dg = np.array([[0.0, 1.0]])
        rep = mfa.audit(do, dg, dp, radius=0.2, c_obs=0.0, c_goal=0.0, c_measurement=0.0)
        self.assertGreaterEqual(rep["conditional_prediction_bound"], 0.2-1e-12)
        self.assertFalse(rep["factorization_exact_at_tangent"])


import expression_domain_inventory as edi

class ExpressionDomainInventoryTests(unittest.TestCase):
    def test_static_inverse_inventory_retains_unreached_nodes(self):
        expr = {"op": "matmul", "args": [
            {"op": "inv", "label": "R", "arg": {"op": "var", "name": "bad"}},
            {"op": "inv", "label": "R", "arg": {"op": "var", "name": "good"}},
        ]}
        tree = edi.enumerate_inverse_occurrences(expr)
        self.assertEqual([x["path"] for x in tree], ["$.args[0]", "$.args[1]"])
        logs = [{"sample_id": "s", "node_path": "$.args[0]", "defined": False,
                 "min_singular_value": 0.0, "kind": "matrix", "threshold": 1e-12}]
        coverage = edi.coverage(tree, ["s"], logs)
        self.assertEqual([x["status"] for x in coverage], ["SINGULAR", "NOT_REACHED_DEPENDENCY"])
        self.assertFalse(edi.complete_coverage(coverage))

    def test_all_reached_paths_report_complete_even_when_labels_repeat(self):
        expr = {"op": "add", "args": [
            {"op": "inv", "label": "dup", "arg": {"op": "var", "name": "x"}},
            {"op": "inv", "label": "dup", "arg": {"op": "var", "name": "y"}},
        ]}
        tree = edi.enumerate_inverse_occurrences(expr)
        logs = [{"sample_id": "s", "node_path": x["path"], "defined": True, "kind": "scalar"} for x in tree]
        coverage = edi.coverage(tree, ["s"], logs)
        self.assertTrue(edi.complete_coverage(coverage))
        self.assertEqual(len(set(x["path"] for x in coverage)), 2)


if __name__ == "__main__":
    unittest.main()
