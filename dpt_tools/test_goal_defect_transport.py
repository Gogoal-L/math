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


class D12CausalGoalDualTests(unittest.TestCase):
    def test_frozen_and_correction_match_independent_pl_coil_paths(self):
        from goal_defect_transport import s150_causal_coil_signed_goal_bound as bound
        t=np.arange(9,dtype=float)*1e-9
        H=np.array([0,.5,2.3,4.2,6.6,8])*1e-9
        sl=np.array([.6,.8,.9,1.4,1.1,.7,.4,.6,1.])
        vd=np.array([3.,5.,4.,6.,7.,1.,2.,4.,3.])
        L=4e-9;rho=.01
        s=np.r_[.3,.3+np.cumsum(np.diff(t)*sl[1:]/L)]
        # Same prepared full node/current at t0, both alternative coil rows exact.
        dvd=np.array([0,1,-1,1,-1,1,1,-1,1])*rho
        dsl=np.array([0,-1,1,1,1,-1,1,-1,1])*rho
        vdp=vd+dvd;slp=sl+dsl
        sp=np.r_[s[0],s[0]+np.cumsum(np.diff(t)*slp[1:]/L)]
        def score(v,i):
            hv=np.interp(H,t,v);hi=np.interp(H,t,i)
            return float(np.dot(np.diff(H),(hv[:-1]*hi[:-1]+hv[1:]*hi[1:])/2))
        for kind in ("frozen","signed_correction"):
            report=bound(t,H,vd,sl,s,L,rho,score=kind)
            delta=score(vdp-slp,sp)-score(vd-sl,s)
            if kind=="signed_correction":
                delta-=np.sum(np.diff(t)*((vdp-slp)[1:]*sp[1:]-(vd-sl)[1:]*s[1:]))
            self.assertLess(abs(delta),report["delta_goal_abs_upper_J"])
            self.assertEqual(report["status"],"CONDITIONAL_CAUSAL_COIL_GOAL")
            self.assertGreater(report["linear_radius_J"],0)

    def test_reject_unqualified_inputs(self):
        from goal_defect_transport import s150_causal_coil_signed_goal_bound as bound
        t=[0.,1e-9,2e-9];H=t;vd=[1.,2.,3.];sl=[0.,0.,0.];s=[1.,1.,1.]
        for rho,er,kind in ((-1,0,"frozen"),(0,-1,"frozen"),(0,0,"bad")):
            with self.assertRaises(ValueError):
                bound(t,H,vd,sl,s,4e-9,rho,score=kind,alt_r36_residual_V=er)
        with self.assertRaises(ValueError):
            bound(t,H,vd,sl,s,0,1e-3)



class D13TwoLCausalGoalTests(unittest.TestCase):
    def test_different_prepared_seeds_finite_L_and_coil_residuals(self):
        from goal_defect_transport import s150_two_l_causal_goal_identity as f
        for seed in (0,1,2):
            rng=np.random.default_rng(seed);n=201;t=np.linspace(0,84e-9,n)
            H=np.linspace(0,84e-9,46)
            H[1:-1]+=.13*(t[1]-t[0])*np.sin(np.arange(1,45)*1.7)
            slA=rng.normal(0,.3,n);slB=slA+rng.normal(0,.02,n)
            vA=slA+100+2*np.sin(np.linspace(0,3,n))
            vB=vA+rng.normal(0,.003,n)
            rA=np.r_[0.,rng.normal(0,2e-8,n-1)]
            rB=np.r_[0.,rng.normal(0,3e-8,n-1)]
            La=4.16e-9;Lb=4.5e-9;h=np.diff(t)
            iA=np.r_[.01,.01+np.cumsum(h*(slA[1:]+rA[1:])/La)]
            iB=np.r_[.012,.012+np.cumsum(h*(slB[1:]+rB[1:])/Lb)]
            for score in ("frozen","signed_correction"):
                z=f(t,H,vA,slA,iA,La,vB,slB,iB,Lb,score=score)
                self.assertLess(z["closure_abs_J"],1e-17)
                self.assertGreater(abs(z["terms_J"]["static_L_J"]),1e-13)
                self.assertGreater(abs(z["terms_J"]["prepared_current_J"]),1e-13)
                self.assertEqual(z["status"],"CONDITIONAL_TWO_L_BE_GOAL_IDENTITY")

    def test_two_l_contract_rejects_invalid_source_arguments(self):
        from goal_defect_transport import s150_two_l_causal_goal_identity as f
        t=[0.,1e-9,2e-9];q=[0.,.1,.3];z=[.01,.02,.03]
        for La,Lb,score in ((-1,4e-9,"frozen"),(4e-9,0,"frozen"),(4e-9,5e-9,"invalid")):
            with self.assertRaises(ValueError):
                f(t,t,q,q,z,La,q,q,z,Lb,score=score)
        with self.assertRaises(ValueError):
            f([0,0,1e-9],t,q,q,z,4e-9,q,q,z,5e-9)



class D16PackageTwoCoilGoalTests(unittest.TestCase):
    def test_positive_two_coil_synthetic_nonzero_both_prepared_seeds(self):
        from goal_defect_transport import s150_package_two_coil_goal_bound as bound
        t=np.linspace(0,10e-9,101);h=np.diff(t);H=np.linspace(t[0],t[-1],27)
        H[1:-1]+=0.2*h[0]*np.sin(np.arange(1,len(H)-1))
        L=4.16e-9;Lp=3.435e-9;R=.003322;Rp=100.
        sv=.5+.04*np.sin(np.linspace(0,3,len(t)))
        sv2=sv+1e-6*np.sin(np.linspace(0,5,len(t)))
        def run(inp,s0,j0):
            s=np.empty(len(t));j=np.empty(len(t));s[0],j[0]=s0,j0
            for k in range(1,len(t)):
                A=np.array([[L/h[k-1]+R+Rp,-Rp],
                            [-Rp,Lp/h[k-1]+Rp]])
                rhs=np.array([L/h[k-1]*s[k-1]+inp[k],Lp/h[k-1]*j[k-1]])
                s[k],j[k]=np.linalg.solve(A,rhs)
            sl=inp+Rp*j-(R+Rp)*s
            sa=sl+R*s
            return s,j,sl,sa
        s,j,sl,sa=run(sv,.001,.003)
        sb,jb,slb,sab=run(sv2,.0010004,.0030008)
        vport=3+.2*np.cos(np.linspace(0,4,len(t)))
        vp2=vport+2e-6*np.sin(np.linspace(0,7,len(t)))
        report=bound(t,H,sl+vport,sl,sa,sv,s,-j,L,
                     port_radius_V=2e-6,sv_radius_V=1e-6,
                     seed_s_radius_A=4e-7,seed_j_radius_A=8e-7)
        def goal(v,i):
            vv=np.interp(H,t,v);ii=np.interp(H,t,i)
            return float(np.sum(np.diff(H)*(vv[:-1]*ii[:-1]+vv[1:]*ii[1:])/2))
        direct=goal(vp2,sb)-goal(vport,s)
        self.assertLess(abs(direct),report["goal_radius_J"])
        self.assertLess(report["source_residual_maxabs"]["schur_forcing_V"],2e-12)
        self.assertTrue(all(x>0 for x in report["prepared_adjoint_J_per_A"]))
        self.assertGreater(report["sv_adjoint_L1_J_per_V"],0)
        self.assertEqual(report["status"],"CONDITIONAL_PACKAGE_2COIL_GOAL")

    def test_reject_wrong_history_grid_and_negative_input_contract(self):
        from goal_defect_transport import s150_package_two_coil_goal_bound as f
        t=[0.,1e-9,2e-9];a=[.01,.02,.03];z=[0.,0.,0.]
        def call(t0=t,L=4e-9,rad=1e-6):
            return f(t0,t,a,a,a,z,a,z,L,port_radius_V=rad,
                     sv_radius_V=1e-6,seed_s_radius_A=1e-6,
                     seed_j_radius_A=1e-6)
        with self.assertRaises(ValueError):call(t0=[0.,0.,2e-9])
        with self.assertRaises(ValueError):call(L=-1)
        with self.assertRaises(ValueError):call(rad=-1e-6)


class D19OriginalCoilScorerCountercontrol(unittest.TestCase):
    def test_source_BE_right_work_can_cancel_while_frozen_H841_does_not(self):
        from goal_defect_transport import s150_two_coil_scorer_bridge
        t=np.arange(6721,dtype=float)*12.5e-12
        H=t[::8]
        current=np.ones(t.size)
        va=np.ones(t.size)
        vb=va.copy()
        vb[80]+=1.0
        vb[81]-=1.0
        def j_of(v):
            return np.r_[0.,np.cumsum((v[1:]-150.)*np.diff(t)/100e-6)]
        a=s150_two_coil_scorer_bridge(t,H,va,current,j_of(va),
                                       4.16e-9,100e-6)
        b=s150_two_coil_scorer_bridge(t,H,vb,current,j_of(vb),
                                       4.16e-9,100e-6)
        self.assertLess(abs(b['W_BE_right_J']-a['W_BE_right_J']),1e-17)
        self.assertLess(abs(b['W_H_J']-a['W_H_J']-1e-10),1e-17)
        self.assertLess(abs(b['Q_H_direct_J']-a['Q_H_direct_J']-1e-10),1e-17)
        self.assertLess(abs(b['Q_H_J']-a['Q_H_J']-1e-10),1e-17)
        self.assertLess(abs(b['Q_H_J']-b['Q_H_direct_J']),1e-16)
        self.assertLess(max(a['r36_minus_r37_maxabs_V'],
                            b['r36_minus_r37_maxabs_V']),1e-7)


class Q4ThreeCornerIdentifiabilityTests(unittest.TestCase):
    def test_saved_fine_h2_corner_predictions_and_interaction_threshold(self):
        from goal_defect_transport import audit_two_factor_pretarget_interaction as f
        pairs=(
          ("62.4118949371027","69.66234860335713","28.034528346669244",
           "0.6682027537302077","0.44918566204281746",
           (35.28498201292368,32.879301452253735,31.291328176856513)),
          ("62.38734299174475","69.641430064909","28.00641553024535",
           "0.6681974524680616","0.44891181748117126",
           (35.2605026034096,32.853578032515195,31.262860942426183)),
        )
        for base,e,b,r,q,expected in pairs:
            got=f(base,e,b,current_ratio=r,work_ratio=q)
            self.assertEqual(got["status"],
                             "THREE_CORNER_UNIDENTIFIED_NO_MIXED_BOUND")
            self.assertIsNone(got["conditional_E150_interval_nJ"])
            values=got["candidate_predictions_nJ"]
            for key,want in zip(("additive","current_scaled","work_scaled"),
                                expected):
                self.assertAlmostEqual(float(values[key]),want,places=10)
            self.assertGreater(float(got["minimum_candidate_gap_nJ"]),1.58)
            self.assertLess(float(got["minimum_candidate_gap_nJ"]),1.60)
            alt=f(base,e,b,current_ratio=r,work_ratio=q,
                  mixed_derivative_abs_bound_nJ="3")
            self.assertIn("work_scaled",alt["excluded_if_M_source_qualified"])
            self.assertNotIn("current_scaled",alt["excluded_if_M_source_qualified"])

    def test_arbitrary_mixed_term_preserves_three_corners(self):
        from fractions import Fraction as Q
        a,b,c=Q(62),Q(70),Q(28)
        def W(h,l,k):
            return a+(b-a)*h+(c-a)*l+k*h*l
        for k in (Q(0),Q(-1000000),Q(1000000)):
            self.assertEqual((W(0,0,k),W(1,0,k),W(0,1,k)),(a,b,c))
            self.assertEqual(W(1,1,k),b+c-a+k)
        from goal_defect_transport import audit_two_factor_pretarget_interaction as f
        for bad in (-1,"NaN","Infinity",True):
            with self.assertRaises(ValueError):
                f(1,2,3,current_ratio=1,work_ratio=1,
                  mixed_derivative_abs_bound_nJ=bad)


class E150MidpointInteractionCurvatureTests(unittest.TestCase):
    def test_actual_saved_additive_baseline_curvature_both_paths(self):
        from goal_defect_transport import audit_e150_midpoint_interaction as audit
        fine=("35.35647830357767","35.28498201292368","35.15145166258552")
        h2=("35.33074380007019","35.2605026034096","35.131729510528395")
        for saved,expect in ((fine,31.017029842083),(h2,29.265948110307)):
            r=audit(("5.0","5.25","5.5"),saved)
            self.assertEqual(r["status"],
                "NO_FINITE_INTERACTION_BOUND_EVEN_WITH_ENDPOINTS")
            self.assertIsNone(r["conditional_E150_midpoint_interval_nJ"])
            self.assertAlmostEqual(
                float(r["known_additive_midpoint_curvature_pJ"]),expect,places=6)
            self.assertEqual(r["exact_interpolation_factor_nH2"],"0.03125")
            self.assertFalse(r["future_midpoint_target_observed"])

    def test_even_two_precise_endpoints_need_a_curvature_contract(self):
        from goal_defect_transport import audit_e150_midpoint_interaction as audit
        from fractions import Fraction as F
        P=("35","34","33")
        L=("5","5.25","5.5")
        noK=audit(L,P,E150_endpoint_work_nJ=("37","35"))
        self.assertIsNone(noK["conditional_E150_midpoint_interval_nJ"])
        self.assertEqual(noK["status"],
                         "NO_FINITE_INTERACTION_BOUND_EVEN_WITH_ENDPOINTS")
        # For ANY A, C_A(L)=2+A*(L-5)*(L-5.5)/(-.0625)
        # agrees at BOTH off-target E150 corners but alters mid by A.
        for A in (F(-100),F(0),F(1),F(123456789,1000000)):
            C0=C1=F(2)
            Cmid=F(2)+A
            self.assertEqual(C0,C1)
            self.assertEqual(Cmid-F(2),A)
        bound=audit(L,P,E150_endpoint_work_nJ=("37","35"),
                    interaction_second_derivative_abs_bound_nJ_per_nH2=".32",
                    joint_total_error_nJ=".002")
        lo,hi=map(F,bound["conditional_E150_midpoint_interval_nJ"])
        self.assertEqual((lo,hi),(F("35.988"),F("36.012")))
        self.assertEqual(bound["status"],"CONDITIONAL_SECOND_DERIVATIVE_INTERVAL")
        self.assertFalse(bound["source_prep_endpoints_qualified"])
        self.assertFalse(bound["future_midpoint_target_observed"])
        for bad in ("-1","NaN","Infinity",True):
            with self.assertRaises(ValueError):
                audit(L,P,interaction_second_derivative_abs_bound_nJ_per_nH2=bad)
        with self.assertRaises(ValueError):
            audit(("5","5.5","5.25"),P)


class E150StrongOrdinaryProfileControls(unittest.TestCase):
    """Actual saved-corner *coefficient* arithmetic, not new E150 target truth."""

    def test_source_saved_six_rivals_and_tiny_minimum_margin(self):
        try:
            from goal_defect_transport import audit_e150_waveform_ordinary_coefficients as audit
        except ImportError as error:
            self.fail(f"new same-information ordinary audit unavailable: {error}")
        source_cases = (
            # B100, E100, B150, profile add-minus-scalar, profile quadratic,
            # current ratio, work ratio, six prior saved predictions.
            ("62.4118949371027","69.66234860335713","28.034528346669244",
             "-2.325198849754582",".19909821697010338",
             ".6682027537302077",".44918566204281746",
             (35.28498201292368,32.879301452253735,31.291328176856513,
              32.95978316316908,31.281455543511857,30.197621728802968),
             .009872633344656),
            ("62.38734299174475","69.641430064909","28.00641553024535",
             "-2.327774260871655",".1993719349754971",
             ".6681974524680616",".44891181748117126",
             (35.2605026034096,32.853578032515195,31.262860942426183,
              32.93272834253794,31.253962526139404,30.168572945775924),
             .008898416286779),
        )
        for b,e,c,A,Q,r,q,wants,minimum in source_cases:
            got=audit(b,e,c,profile_add_minus_scalar_nJ=A,
                      profile_quadratic_nJ=Q,current_ratio=r,work_ratio=q)
            self.assertEqual(got["status"],"SIX_RIVALS_PRETARGET_NOT_FROZEN")
            values=got["candidate_predictions_nJ"]
            for key,want in zip((
                "scalar_add","scalar_r","scalar_q",
                "wave_add","wave_r","wave_q"),wants):
                self.assertAlmostEqual(float(values[key]),want,places=9)
            self.assertAlmostEqual(float(got["minimum_six_way_gap_nJ"]),
                                   minimum,places=9)
            self.assertLess(float(got["half_minimum_gap_nJ"]),.005)
            self.assertFalse(got["future_target_observed"])

    def test_negative_curvature_direction_and_invalid_source_contract(self):
        from fractions import Fraction as F
        from goal_defect_transport import audit_e150_waveform_ordinary_coefficients as audit
        got=audit(10,14,5,profile_add_minus_scalar_nJ=-2,
                  profile_quadratic_nJ=F(1,2),current_ratio=F(1,2),
                  work_ratio=F(1,4))
        x=got["candidate_predictions_nJ"]
        self.assertEqual(F(x["scalar_add"]),9)
        self.assertEqual(F(x["wave_add"]),7)
        self.assertEqual(F(x["scalar_r"]),7)
        self.assertEqual(F(x["wave_r"]),F(47,8))
        for bad in ("NaN","Infinity",True):
            with self.assertRaises(ValueError):
                audit(10,14,5,profile_add_minus_scalar_nJ=bad,
                      profile_quadratic_nJ=0,current_ratio=1,work_ratio=1)


class E150AbsoluteHessianContractorNoGoTests(unittest.TestCase):
    def test_three_archived_source_curvatures_forbid_naive_absolute_hessian_triangle(self):
        from fractions import Fraction as F
        from goal_defect_transport import absolute_hessian_triangle_resolution_gate as check
        for mode, mids, gap, factor in (
            ("fine",("46.8635215205125","48.290091856445","29.5904595061475"),
             "9.872633344656",19),
            ("h2",("43.9381406012025","45.21851853427","27.985570177243"),
             "8.898416286779",20),
        ):
            got=check(mids,gap,per_archived_work_error_pJ=F(gap)/2,
                      endpoint_span_nH=F(1,2))
            self.assertEqual(got["status"],"ABSOLUTE_HESSIAN_TRIANGLE_CANNOT_RESOLVE")
            self.assertGreater(got["minimum_known_hessian_sum_nJ_per_nH2"],
                               F(factor)*got["six_way_resolution_threshold_nJ_per_nH2"])
            self.assertFalse(got["joint_interaction_curvature_qualified"])

    def test_zero_curvature_or_wide_archived_errors_must_not_forge_no_go(self):
        from goal_defect_transport import absolute_hessian_triangle_resolution_gate as check
        self.assertEqual(check((0,0,0),"1",0)["status"],"NOT_EXCLUDED_BY_THIS_BOUND")
        self.assertEqual(check((1,1,1),"10","100")["status"],"NOT_EXCLUDED_BY_THIS_BOUND")
        for bad in (-1,"NaN",True):
            with self.assertRaises(ValueError):
                check((1,2,3),"1",bad)


if __name__ == '__main__':
    unittest.main()
