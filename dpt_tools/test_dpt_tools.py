import unittest

import numpy as np

import command_domain_audit as cda
import predictive_state_audit as psa


class PredictiveStateAuditTests(unittest.TestCase):
    def test_discarded_measurement_direction_cannot_enter_goal_factor(self):
        rep = psa._linear_measurement_audit(
            np.zeros((1, 2)), np.array([[0.0, 1.0]]),
            np.array([[0.0, 1e-14]]), 1e-9, 1e-12, 1e-8)
        m = rep["measurement"]
        self.assertEqual(m["rank_on_hidden"], 0)
        self.assertFalse(m["tangent_goal_sufficient"])
        self.assertAlmostEqual(m["minimum_norm_goal_from_measurement_gain_2norm"], 0)
        self.assertAlmostEqual(m["factorization_residual_rel"], 1)

    def test_one_measurement_repairs_one_goal_visible_direction(self):
        do = np.array([[1.0, 0.0, 0.0]])
        dg = np.array([[0.0, 1.0, 0.0]])
        dp = np.array([[0.0, 1.0, 0.0]])
        rep = psa._linear_measurement_audit(do, dg, dp, 1e-10, 1e-12, 1e-9)
        self.assertEqual(rep["goal_visible_hidden_dim"], 1)
        self.assertTrue(rep["measurement"]["tangent_goal_sufficient"])

    def test_mixed_measurement_can_fail_despite_nonzero_goal_projection(self):
        do = np.array([[1.0, 0.0, 0.0]])
        dg = np.array([[0.0, 1.0, 0.0]])
        dp = np.array([[0.0, 1.0, 1.0]])
        rep = psa._linear_measurement_audit(do, dg, dp, 1e-10, 1e-12, 1e-9)
        self.assertFalse(rep["measurement"]["tangent_goal_sufficient"])

    def test_candidate_subset_needs_two_rows_when_each_is_mixed(self):
        do = np.array([[1.0, 0.0, 0.0]])
        dg = np.array([[0.0, 1.0, 0.0]])
        candidates = np.array([
            [0.0, 1.0, 1.0],
            [0.0, 0.0, 1.0],
        ])
        rep = psa._candidate_subset_report(
            do, dg, candidates, ["b+c", "c"], 1e-10, 1e-12, 1e-9, 4, 100
        )
        self.assertEqual(rep["minimal_size_within_search_cap"], 2)
        self.assertEqual(rep["exact_subset"], [0, 1])


class CommandDomainAuditTests(unittest.TestCase):
    def test_each_inverse_occurrence_is_logged(self):
        expr = {
            "op": "matmul",
            "args": [
                {"op": "inv", "label": "left", "arg": {"op": "var", "name": "A"}},
                {"op": "inv", "label": "right", "arg": {"op": "var", "name": "B"}},
            ],
        }
        samples = [{"id": "ok", "vars": {"A": [[2.0, 0.0], [0.0, 1.0]], "B": [[1.0, 0.0], [0.0, 3.0]]}}]
        rep = cda.audit(expr, samples, 1e-10, 1e-12)
        self.assertTrue(rep["all_samples_defined"])
        self.assertEqual({x["label"] for x in rep["inverse_occurrences"]}, {"left", "right"})

    def test_undefined_intermediate_inverse_fails(self):
        expr = {
            "op": "matmul",
            "args": [
                {"op": "inv", "label": "singular", "arg": {"op": "var", "name": "A"}},
                {"op": "var", "name": "A"},
            ],
        }
        samples = [{"id": "singular", "vars": {"A": [[1.0, 0.0], [0.0, 0.0]]}}]
        rep = cda.audit(expr, samples, 1e-10, 1e-12)
        self.assertFalse(rep["all_samples_defined"])
        self.assertEqual(rep["inverse_summary_by_label"]["singular"]["undefined_samples"], ["singular"])



class RepairedMultiscaleBoundTests(unittest.TestCase):
    def _run(self, *, include_observation_curvature):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as folder:
            path = Path(folder) / "finite.npz"
            kwargs = {
                "DO": np.array([[1.0, 0.0]]),
                "DG": np.array([[1.0, 1.0]]),
                "DP": np.array([[0.0, 1.0]]),
                "DO_scales": np.array([[[1.0, 0.0]]]),
                "DG_scales": np.array([[[1.0, 1.0]]]),
                "DP_scales": np.array([[[0.0, 1.0]]]),
                "radii": np.array([0.2]),
                "remainder_goal_coeff": np.array([0.0]),
                "remainder_measurement_coeff": np.array([0.0]),
            }
            if include_observation_curvature:
                kwargs["remainder_observation_coeff"] = np.array([1.0])
            np.savez(path, **kwargs)
            return psa.audit_npz(path, 1e-10, 1e-12, 1e-9, 4, 100)["multiscale"][0]

    def test_missing_observation_remainder_prohibits_quadratic_report(self):
        row = self._run(include_observation_curvature=False)
        self.assertNotIn("certified_quadratic_prediction_bound", row)
        self.assertNotIn("conditional_all_direction_prediction", row)
        self.assertEqual(row["prediction_status"], "MISSING_OBSERVATION_GOAL_MEASUREMENT_REMAINDER_OR_RADIUS")

    def test_general_bound_contains_observation_factor_and_curvature(self):
        row = self._run(include_observation_curvature=True)
        factor = row["conditional_all_direction_prediction"]
        self.assertAlmostEqual(factor["observation_gain_2norm"], 1.0)
        self.assertAlmostEqual(factor["measurement_gain_2norm"], 1.0)
        self.assertAlmostEqual(factor["conditional_prediction_bound"], 0.04)


class InverseOccurrenceCoverageRegressionTests(unittest.TestCase):
    def test_fail_fast_keeps_unreached_original_inverse(self):
        expr = {"op": "matmul", "args": [
            {"op": "inv", "label": "same", "arg": {"op": "var", "name": "A"}},
            {"op": "inv", "label": "same", "arg": {"op": "var", "name": "B"}},
        ]}
        samples = [{"id": "bad", "vars": {"A": [[1.0, 0.0], [0.0, 0.0]],
                                            "B": [[1.0, 0.0], [0.0, 1.0]]}}]
        report = cda.audit(expr, samples, 1e-10, 1e-12)
        self.assertFalse(report["all_samples_defined"])
        self.assertFalse(report["all_original_inverse_occurrences_evaluated"])
        self.assertEqual(len(report["static_inverse_inventory"]), 2)
        status = {x["path"]: x["status"] for x in report["inverse_coverage_by_sample"]}
        self.assertEqual(status["$.args[0]"], "SINGULAR")
        self.assertEqual(status["$.args[1]"], "NOT_REACHED_DEPENDENCY")

    def test_same_labels_still_have_distinct_path_identifiers(self):
        expr = {"op": "add", "args": [
            {"op": "inv", "label": "duplicated", "arg": {"op": "var", "name": "A"}},
            {"op": "inv", "label": "duplicated", "arg": {"op": "var", "name": "B"}},
        ]}
        samples = [{"id": "ok", "vars": {"A": 2.0, "B": 4.0}}]
        report = cda.audit(expr, samples, 1e-10, 1e-12)
        self.assertTrue(report["all_samples_defined"])
        self.assertEqual(set(report["inverse_summary_by_path"]), {"$.args[0]", "$.args[1]"})


if __name__ == "__main__":
    unittest.main()
