import unittest

import numpy as np

import command_domain_audit as cda
import predictive_state_audit as psa


class PredictiveStateAuditTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
