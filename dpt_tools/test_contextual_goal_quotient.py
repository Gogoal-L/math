"""Finite-word goal quotient: independent linear algebra fixtures, not native SiC."""
import unittest
import numpy as np
from contextual_goal_quotient import audit_contextual_goal_quotient


class ContextualGoalQuotientTests(unittest.TestCase):
    def test_immediate_goal_works_but_one_future_word_fails(self):
        report=audit_contextual_goal_quotient(
            updates=np.array([np.diag([1.,-1.])]),
            observation=np.eye(2),nuisance=np.ones((2,1)),
            goal=np.array([[1.,-1.]]),words=[[],[0]])
        self.assertEqual(report["current_nuisance_invariant_rank"],1)
        self.assertEqual(report["future_goal_rank"],2)
        self.assertEqual(report["minimum_extra_ideal_scalar_rows"],1)
        self.assertAlmostEqual(report["goal_remainder_by_row"][0],0.)
        self.assertAlmostEqual(report["goal_remainder_by_row"][1],np.sqrt(2.))
        self.assertAlmostEqual(report["witness_current_observation_residual"],0.)
        self.assertAlmostEqual(report["witness_goal_gap"],2*np.sqrt(2.))

    def test_same_goals_without_nuisance_are_all_observable(self):
        report=audit_contextual_goal_quotient(
            updates=np.array([np.diag([1.,-1.])]),
            observation=np.eye(2),nuisance=np.empty((2,0)),
            goal=np.array([[1.,-1.]]),words=[[],[0]])
        self.assertEqual(report["minimum_extra_ideal_scalar_rows"],0)
        self.assertEqual(report["maximum_goal_remainder"],0.)

    def test_pretarget_shared_offset_calibration_reduces_deficit(self):
        report=audit_contextual_goal_quotient(
            updates=np.array([np.diag([1.,-1.])]),
            observation=np.array([[1.,0.],[0.,1.],[0.,0.]]),
            nuisance=np.ones((3,1)),
            goal=np.array([[1.,-1.]]),words=[[],[0]])
        self.assertEqual(report["current_nuisance_invariant_rank"],2)
        self.assertEqual(report["minimum_extra_ideal_scalar_rows"],0)

    def test_command_order_is_actual_matrix_order(self):
        A=np.array([[1.,1.],[0.,1.]])
        B=np.array([[1.,0.],[0.,-1.]])
        report=audit_contextual_goal_quotient(
            updates=np.array([A,B]),
            observation=np.zeros((0,2)),nuisance=np.empty((0,0)),
            goal=np.array([[1.,0.]]),words=[[0,1],[1,0]])
        np.testing.assert_allclose(report["stacked_goal_rows"][0],[1.,1.])
        np.testing.assert_allclose(report["stacked_goal_rows"][1],[1.,-1.])

    def test_bad_dimensions_and_illegal_commands(self):
        base=(np.array([np.eye(2)]),np.eye(2),np.ones((2,1)),np.ones((1,2)))
        with self.assertRaises(ValueError):
            audit_contextual_goal_quotient(*base,words=[[2]])
        with self.assertRaises(ValueError):
            audit_contextual_goal_quotient(base[0],base[1],np.ones((3,1)),base[3],words=[[]])


if __name__ == "__main__":
    unittest.main()
