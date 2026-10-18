"""Independent reference cases for a command-ordered goal-error auditor."""
import json
import unittest

import numpy as np

from goal_defect_transport import audit


class GoalDefectTransportTests(unittest.TestCase):
    def test_hidden_state_is_invisible_initially_but_visible_after_stage(self):
        a = np.array([[[0.5, 6.0], [0.0, 0.5]]])
        result = audit(a, [[1.0, 0.0]], [1.0, 0.0], 0.01, [0.0])
        self.assertAlmostEqual(result['stages'][0]['information_radius'], 0.0)
        self.assertAlmostEqual(result['stages'][1]['information_radius'], 0.06)
        self.assertAlmostEqual(result['worst_stage']['total_radius'], 0.06)
        self.assertAlmostEqual(result['max_absolute_witness']['goal_deviation'], 0.06)
        self.assertAlmostEqual(result['max_absolute_witness']['observation_residual'], 0.0)
        self.assertTrue(all(abs(ev - 0.5) < 1e-12 for ev in result['stage_spectral_radii']))

    def test_two_distinct_stage_defects_add_exactly_in_goal_direction(self):
        a = np.array([[[2.0]], [[3.0]]])
        result = audit(a, np.array([[1.0]]), np.array([1.0]), 0.0, [0.1, 0.2])
        self.assertAlmostEqual(result['stages'][1]['defect_radius'], 0.1)
        self.assertAlmostEqual(result['stages'][2]['defect_radius'], 0.5)
        self.assertAlmostEqual(result['max_absolute_witness']['goal_deviation'], 0.5)
        self.assertEqual(result['worst_stage']['stage'], 2)

    def test_hidden_state_and_solver_budgets_are_separately_reported(self):
        result = audit([np.eye(2)], [[1, 0]], [0, 1], 0.3, [0.2])
        self.assertAlmostEqual(result['worst_stage']['information_radius'], 0.3)
        self.assertAlmostEqual(result['worst_stage']['defect_radius'], 0.2)
        self.assertAlmostEqual(result['worst_stage']['total_radius'], 0.5)
        self.assertAlmostEqual(result['max_absolute_witness']['goal_deviation'], 0.5)

    def test_full_observation_removes_hidden_information_not_solver_error(self):
        result = audit([np.eye(2)], np.eye(2), [1, 0], 5.0, [0.04])
        self.assertAlmostEqual(result['worst_stage']['information_radius'], 0.0)
        self.assertAlmostEqual(result['worst_stage']['defect_radius'], 0.04)

    def test_different_goals_at_different_command_stages(self):
        a = np.array([np.eye(2), np.eye(2)])
        g = np.array([[1, 0], [0, 1], [1, 0]])
        result = audit(a, [[1, 0]], g, 0.3, [0, 0])
        self.assertEqual([round(s['information_radius'], 4) for s in result['stages']], [0., .3, 0.])
        self.assertEqual(result['worst_stage']['stage'], 1)

    def test_no_stages_is_allowed_and_exact_initial_goal_radius(self):
        a = np.zeros((0, 2, 2))
        result = audit(a, np.zeros((0, 2)), [1, 0], 0.5, [])
        self.assertAlmostEqual(result['worst_stage']['total_radius'], 0.5)
        self.assertEqual(result['stages'][0]['stage'], 0)

    def test_noncommuting_order_changes_hidden_goal_leakage(self):
        a = np.array([[1., 1.], [0., 1.]])
        b = np.array([[1., 0.], [0., 0.]])
        # The matrix applied first is leftmost in [a,b]; final state is b@a@x.
        ab = audit([a, b], [[1, 0]], [1, 0], 1., [0, 0])
        ba = audit([b, a], [[1, 0]], [1, 0], 1., [0, 0])
        self.assertAlmostEqual(ab['stages'][2]['information_radius'], 1.)
        self.assertAlmostEqual(ba['stages'][2]['information_radius'], 0.)

    def test_degenerate_zero_goal_zero_radii_witness_stays_zero(self):
        out = audit([np.eye(2)], [[1, 0]], [0, 0], 3., [1.])
        self.assertAlmostEqual(out['worst_stage']['total_radius'], 0.)
        self.assertAlmostEqual(out['max_absolute_witness']['goal_deviation'], 0.)

    def test_scalar_disturbance_signs_exhaustively_recover_bound(self):
        # Independent oracle by enumerating all +- extremes of three 1D balls.
        from itertools import product
        stages = [-2.0, 0.25]
        rho, eps = 0.3, [0.1, 0.2]
        model = audit(np.array(stages)[:, None, None], np.zeros((0, 1)),
                      [1.0], rho, eps)
        actual = []
        for signs in product((-1, 1), repeat=3):
            x = signs[0] * rho
            x = stages[0] * x + signs[1] * eps[0]
            x = stages[1] * x + signs[2] * eps[1]
            actual.append(abs(x))
        self.assertAlmostEqual(model['stages'][2]['total_radius'], max(actual))
        self.assertAlmostEqual(model['stages'][2]['information_radius'], 0.15)
        self.assertAlmostEqual(model['stages'][2]['defect_radius'], 0.225)

    def test_fail_closed_on_negative_nan_misalignment(self):
        with self.assertRaises(ValueError):
            audit([np.eye(2)], [[1, 0]], [1, 0], -1., [0])
        with self.assertRaises(ValueError):
            audit([np.eye(2)], [[1, 0]], [1, 0], 1., [np.nan])
        with self.assertRaises(ValueError):
            audit([np.eye(2)], [[1, 0]], [1, 0], 1., [])
        with self.assertRaises(ValueError):
            audit([np.eye(2)], [[1, 0, 0]], [1, 0], 1., [0])
        with self.assertRaises(ValueError):
            audit([np.eye(2)], [[1, 0]], [1, 0], 1., [0], rtol=-1)

    def test_witness_matches_the_reported_exact_product_ball_support(self):
        a = np.array([[[0, 2], [1, 0]], [[0.1, 0.4], [-0.1, 0.2]], [[1, 0], [0, 2]]], dtype=float)
        out = audit(a, [[1, 1]], [0.7, -1.2], 0.4, [0.1, 0.03, 0.2])
        w = out['max_absolute_witness']
        self.assertAlmostEqual(abs(w['goal_deviation']), out['worst_stage']['total_radius'], places=11)
        self.assertLessEqual(w['observation_residual'], 1e-11)
        self.assertLessEqual(w['initial_norm'], 0.4 + 1e-11)
        self.assertTrue(all(norm <= lim+1e-11 for norm, lim in zip(w['defect_norms'], [0.1, 0.03, 0.2])))


class S150TwoCoilSignedWorkTests(unittest.TestCase):
    """Independent finite-mesh source-row controls, not future fiber truth."""

    def test_exact_two_mesh_coil_bridge_and_residual_budget(self):
        from goal_defect_transport import s150_two_coil_scorer_bridge as bridge
        t=np.linspace(0,1e-9,11);H=t[::2]
        s=np.sin(np.linspace(0,2,11));j=np.cos(np.linspace(0,1,11))
        V=np.empty_like(t);V[0]=12
        V[1:]=150-4.16e-9*np.diff(s)/np.diff(t)+1e-4*np.diff(j)/np.diff(t)
        r=bridge(t,H,V,s,j,4.16e-9,1e-4,coil_residual_each_V=3e-8)
        self.assertTrue(r['residual_qualified_at_point'])
        self.assertLess(abs(r['Q_H_J']-r['Q_H_direct_J']),1e-18)
        self.assertLess(abs(r['Q_H_J']-r['Q_coil_J']-r['Q_residual_J']),1e-18)

    def test_nonaligned_interpolation_cross_term_not_dropped(self):
        from goal_defect_transport import s150_two_coil_scorer_bridge as bridge
        t=np.linspace(0,1e-9,11);H=np.array([.03,.17,.35,.83,1.])*1e-9
        s=np.sin(np.linspace(0,2,11));j=np.cos(np.linspace(0,1,11))
        V=np.linspace(5,30,11)
        r=bridge(t,H,V,s,j,4.16e-9,1e-4,coil_residual_each_V=3e-8)
        self.assertFalse(r['residual_qualified_at_point'])
        self.assertLess(abs(r['Q_H_J']-r['Q_H_direct_J']),1e-18)
        self.assertLess(abs(r['Q_H_J']-r['Q_coil_J']-r['Q_residual_J']),1e-18)

    def test_unordered_times_and_negative_residual_budget(self):
        from goal_defect_transport import s150_two_coil_scorer_bridge as bridge
        with self.assertRaises(ValueError):
            bridge([0,0],[0,1],[0,0],[0,0],[0,0],1,1)
        with self.assertRaises(ValueError):
            bridge([0,1],[0,1],[0,0],[0,0],[0,0],1,1,coil_residual_each_V=-1)



    def test_two_coil_raw_port_reconstruct_load_current(self):
        from goal_defect_transport import s150_load_current_from_raw_ports as recover
        t=np.linspace(0,1e-9,11);i=np.sin(np.linspace(0,2,11))
        j=-.04+np.cos(np.linspace(0,1,11))
        h=np.diff(t);v=np.empty_like(t);v[0]=145
        v[1:]=150-4.16e-9*np.diff(i)/h+1e-4*np.diff(j)/h
        r=recover(t,v,i,source_Ls_H=4.16e-9,seed_load_A=j[0])
        np.testing.assert_allclose(r["j_A"],j,atol=1e-13,rtol=0)
        self.assertEqual(r["status"],"CONDITIONAL_RAW_PORT_LOAD_HISTORY")

    def test_raw_port_recovery_error_radius_and_invalid(self):
        from goal_defect_transport import s150_load_current_from_raw_ports as recover
        t=[0,1e-8,2e-8]
        r=recover(t,[150]*3,[0]*3,source_Ls_H=4e-9,seed_load_A=0,
                  voltage_error_V=.1,current_error_A=.01,
                  seed_error_A=.001,coil_residual_error_V=3e-8)
        expected=.001+(2e-8*.1+2*4e-9*.01+2*2e-8*3e-8)/1e-4
        self.assertAlmostEqual(r["uniform_error_bound_A"][-1],expected)
        with self.assertRaises(ValueError):
            recover(t,[150]*3,[0]*3,source_Ls_H=-4e-9,seed_load_A=0)



class D8CorrelatedFutureFamilyBoundTests(unittest.TestCase):
    def test_small_grid_matches_independent_dense_gram_and_source_bound(self):
        from goal_defect_transport import s150_goal_family_weighted_bound as bound
        t=np.arange(6,dtype=float)*1e-9
        H=np.array([0.,1.5,3.5,5.])*1e-9
        V=np.array([2,3,6,4,5,7],float)
        I=np.array([.2,.3,.4,.6,.7,.8],float)
        h=np.diff(t)
        omega=np.array([.75,1.75,1.75,.75])*1e-9
        A=np.zeros((len(H),len(t)))
        for k,v in enumerate(H):
            j=min(max(np.searchsorted(t,v,side="right"),1),len(t)-1)
            a=(v-t[j-1])/(t[j]-t[j-1])
            A[k,j-1],A[k,j]=1-a,a
        gram=A.T@np.diag(omega)@A
        for name,E in [("frozen",gram),
                       ("signed_correction",gram-np.diag([0.,*h]))]:
            rs,rp,rr=.003,.004,.002
            r=bound(t,H,V,I,rs,rp,rr,score=name)
            self.assertAlmostEqual(r['C_s_V_root_s'],
                                   np.linalg.norm((E@V)[1:]/np.sqrt(h)))
            self.assertAlmostEqual(r['C_phi_A_root_s'],
                                   np.linalg.norm((E@I)[1:]/np.sqrt(h)))
            # Dense spectral norm must not exceed Gershgorin support.
            W=np.diag(1/np.sqrt(h))
            self.assertLessEqual(np.linalg.norm(W@E[1:,1:]@W,2),
                                 r['sigma_float_gershgorin']+1e-12)
            dx=np.array([0,.0001,-.0001,.0002,-.0003,.0004])
            q=np.array([0,.0008,.0004,-.0003,.0005,-.0001])
            delta=float((V+q)@E@(I+dx)-V@E@I)
            self.assertLess(abs(delta),r['delta_goal_abs_upper_J'])
            self.assertEqual(r['status'],'CONDITIONAL_SOURCE_FAMILY_NORM')

    def test_require_same_grid_and_nonnegative_certified_radii(self):
        from goal_defect_transport import s150_goal_family_weighted_bound as bound
        for t,H,rs in (([0,0],[0,1],0),([0,1],[-1,1],0),
                       ([0,1],[0,1],-1)):
            with self.assertRaises(ValueError):
                bound(t,H,[2,3],[0,1],rs,0,0)


if __name__ == '__main__':
    unittest.main()
