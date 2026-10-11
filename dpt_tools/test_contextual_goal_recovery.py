"""Analytic and CLI oracles for mixed-nuisance finite-command goal radii."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from contextual_goal_recovery import audit_contextual_goal_recovery


class MixedNuisanceGoalRadius(unittest.TestCase):
    def model(self, **kw):
        d=dict(
            updates=np.array([np.diag([1.,-1.])]),
            state_factor=np.eye(2),
            observation=np.eye(2),
            unbounded_nuisance=np.ones((2,1)),
            bounded_noise=np.empty((2,0)),
            goal=np.array([[1.,-1.]]),
            words=[[],[0]],
            goal_tolerances=[.2])
        d.update(kw)
        return audit_contextual_goal_recovery(**d)

    def test_future_command_can_destroy_instantaneous_exact_recovery(self):
        q=self.model()
        self.assertAlmostEqual(q["rows"][0]["radius"],0,places=8)
        self.assertAlmostEqual(q["rows"][1]["radius"],np.sqrt(2),places=8)
        self.assertAlmostEqual(q["max_radius_relative_to_tolerance"],np.sqrt(2)/.2)
        for row in q["rows"]:
            self.assertLess(row["numerical_gap"],1e-7)
            self.assertLess(row["nuisance_weight_residual"],1e-7)

    def test_precommand_shared_offset_calibration_repairs_future(self):
        q=self.model(observation=np.array([[1.,0.],[0.,1.],[0.,0.]]),
                     unbounded_nuisance=np.ones((3,1)),
                     bounded_noise=np.empty((3,0)))
        self.assertLess(max(r["radius"] for r in q["rows"]),1e-8)
        self.assertTrue(q["meets_all_goal_tolerances"])

    def test_independent_error_destroys_exact_difference(self):
        q=self.model(words=[[]],bounded_noise=.1*np.eye(2),
                     goal=np.array([[1.,-1.],[1.,1.]]),
                     goal_tolerances=[1.,2.])
        self.assertAlmostEqual(q["rows"][0]["radius"],.1*np.sqrt(2),places=7)
        self.assertAlmostEqual(q["rows"][1]["radius"],np.sqrt(2),places=7)

    def test_common_bounded_error_cancels_in_difference(self):
        q=self.model(words=[[]],bounded_noise=np.array([[.2],[.2]]),
                     goal=np.array([[1.,-1.],[1.,1.]]),
                     goal_tolerances=[1.,2.])
        self.assertAlmostEqual(q["rows"][0]["radius"],0,places=8)
        self.assertAlmostEqual(q["rows"][1]["radius"],np.sqrt(2),places=8)

    def test_calibration_plus_bounded_noise_residual(self):
        q=self.model(observation=np.array([[1.,0.],[0.,1.],[0.,0.]]),
                     unbounded_nuisance=np.ones((3,1)),
                     bounded_noise=np.array([[.1,0.],[0.,.1],[0.,0.]]),
                     words=[[0]])
        self.assertAlmostEqual(q["rows"][0]["radius"],.1*np.sqrt(2),places=7)
        self.assertTrue(q["meets_all_goal_tolerances"])

    def test_noncommuting_commands_have_different_goal_rows(self):
        a=np.array([[1.,1.],[0.,1.]])
        b=np.diag([1.,-1.])
        q=self.model(updates=np.array([a,b]),observation=np.empty((0,2)),
                     unbounded_nuisance=np.empty((0,0)),
                     bounded_noise=np.empty((0,0)),
                     goal=np.array([[1.,0.]]),
                     words=[[0,1],[1,0]],goal_tolerances=[3.])
        np.testing.assert_allclose(q["rows"][0]["future_goal_row"],[1.,1.])
        np.testing.assert_allclose(q["rows"][1]["future_goal_row"],[1.,-1.])

    def test_reject_illegal_command_and_invalid_noise_or_tolerance(self):
        with self.assertRaises(ValueError):
            self.model(words=[[5]])
        with self.assertRaises(ValueError):
            self.model(goal_tolerances=[0])
        with self.assertRaises(ValueError):
            self.model(bounded_noise=np.eye(3))

    def test_tiny_tolerance_is_not_overridden_by_fixed_absolute_slack(self):
        q=self.model(words=[[]],bounded_noise=1e-10*np.eye(2),
                     goal_tolerances=[1e-12])
        self.assertGreater(q["rows"][0]["radius"],1e-12)
        self.assertFalse(q["meets_all_goal_tolerances"])

    def test_small_noise_goal_can_pass_appropriate_tolerance(self):
        q=self.model(words=[[]],bounded_noise=1e-10*np.eye(2),
                     goal_tolerances=[1e-8])
        self.assertLess(q["rows"][0]["radius"],1e-8)
        self.assertTrue(q["meets_all_goal_tolerances"])

    def test_cli_json_replay(self):
        d=dict(updates=[[[1.,0.],[0.,-1.]]],
               state_factor=[[1.,0.],[0.,1.]],
               observation=[[1.,0.],[0.,1.]],
               unbounded_nuisance=[[1.],[1.]],
               bounded_noise=[[],[]],goal=[[1.,-1.]],
               words=[[],[0]],goal_tolerances=[2.])
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/"input.json";dst=Path(tmp)/"result.json"
            src.write_text(json.dumps(d),encoding="utf-8")
            p=subprocess.run([sys.executable,str(Path(__file__).parent/"contextual_goal_recovery.py"),
                              str(src),"--output",str(dst)],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            out=json.loads(dst.read_text(encoding="utf-8"))
            self.assertTrue(out["meets_all_goal_tolerances"])
            self.assertAlmostEqual(out["rows"][1]["radius"],np.sqrt(2))


if __name__=="__main__":
    unittest.main()
