"""Exact affine boxes and deliberately conservative correlated states."""
import unittest
import numpy as np
from stage_box_reachability import audit


class StageBoxTests(unittest.TestCase):
    def test_all_switching_boxes_hold_with_uniform_step_error(self):
        # x' = 0.5 x + e, |e| <= 0.1, starting box [-1,1].
        a = np.array([[[.5]],[[.5]],[[.5]]])
        r = audit(a, np.zeros((3,1)), [-1.], [1.],
                  np.full((4,1),-1.),np.full((4,1),1.),np.full((3,1),.1))
        self.assertEqual(r['status'],'CONDITIONAL_AFFINE_BOX_CHAIN')
        self.assertEqual(r['validated_steps'],3)
        self.assertAlmostEqual(r['tube'][-1]['upper'][0], .3)
        self.assertAlmostEqual(r['tube'][-1]['lower'][0], -.3)

    def test_guard_violation_yields_inconclusive_not_native_failure(self):
        r = audit([[[1.2]]],[[0]],[-1],[1],[[-1],[-1]],[[1],[1]],[[0]])
        self.assertEqual(r['status'],'INCONCLUSIVE_BOX_CONTAINMENT')
        self.assertEqual(r['validated_steps'],0)
        self.assertEqual(r['first_failed_stage'],1)
        self.assertGreater(r['violation_by_dimension'][0],0)

    def test_offsets_and_negative_matrix_entry(self):
        r = audit([[[-2.]]],[[1.]],[0.],[.5],[[0.],[-.1]],[[.5],[1.1]],[[.05]])
        # x' range [0,1]+[-1,0]+[-.05,.05] => [-.05, 1.05].
        self.assertEqual(r['status'],'CONDITIONAL_AFFINE_BOX_CHAIN')
        self.assertAlmostEqual(r['tube'][1]['lower'][0],-.05)
        self.assertAlmostEqual(r['tube'][1]['upper'][0],1.05)

    def test_two_stage_correlations_can_make_box_check_inconclusive(self):
        # 1st stage sends a square to x1=x2 diagonal; true next difference zero.
        # Box hull [0,1]^2 loses correlation so 2nd stage over-approximates [-1,1].
        a=np.array([[[1,0],[1,0]],[[1,-1],[0,0]]],float)
        lo=np.array([[0,0],[0,0],[-.1,-.1]])
        hi=np.array([[1,1],[1,1],[.1,.1]])
        r=audit(a,np.zeros((2,2)),[0,0],[1,1],lo,hi,np.zeros((2,2)))
        self.assertEqual(r['status'],'INCONCLUSIVE_BOX_CONTAINMENT')
        self.assertEqual(r['first_failed_stage'],2)
        self.assertEqual(r['validated_steps'],1)
        self.assertAlmostEqual(r['tube'][2]['upper'][0],1.)

    def test_outside_initial_guard_does_not_claim_success(self):
        with self.assertRaises(ValueError):
            audit([[[1]]],[[0]],[-2],[1],[[-1],[-2]],[[1],[2]],[[0]])

    def test_margin_reports_proximity_to_guard_without_changing_containment(self):
        r=audit([[[.5]]],[[0.]],[0.],[1.],[[0.],[0.]],[[1.],[.5]],[[0.]])
        self.assertEqual(r['status'],'CONDITIONAL_AFFINE_BOX_CHAIN')
        self.assertTrue(r['roundoff_margin_warning'])
        self.assertAlmostEqual(r['minimum_guard_margin'],0.)

    def test_zero_stage_validates_only_initial(self):
        r = audit(np.zeros((0,1,1)),np.zeros((0,1)),[-1],[1],[[-1]],[[1]],np.zeros((0,1)))
        self.assertEqual(r['validated_steps'],0)
        self.assertEqual(r['status'],'CONDITIONAL_AFFINE_BOX_CHAIN')

    def test_tiny_guard_escape_cannot_be_certified_using_floating_tolerance(self):
        r = audit([[[1.]]], [[1e-13]], [-1], [1], [[-1], [-1]], [[1],[1]], [[0]], atol=1e-12)
        self.assertEqual(r["status"], "INCONCLUSIVE_BOX_CONTAINMENT")
        self.assertGreater(r["violation_by_dimension"][0], 0)

    def test_tiny_initial_outside_guard_must_fail_closed(self):
        with self.assertRaises(ValueError):
            audit([[[1]]], [[0]], [-1-1e-13], [1], [[-1],[-2]], [[1],[2]], [[0]], atol=1e-12)

    def test_random_small_boxes_match_independent_corner_enumeration(self):
        import itertools
        rng=np.random.default_rng(271828)
        for _ in range(40):
            n=int(rng.integers(1,4))
            a=rng.normal(size=(n,n))
            offset=rng.normal(size=n)
            lo=rng.uniform(-2,0,size=n)
            hi=rng.uniform(0,2,size=n)
            err=rng.uniform(0,.2,size=n)
            guards_lo=np.vstack([lo,np.full(n,-1e4)])
            guards_hi=np.vstack([hi,np.full(n, 1e4)])
            r=audit(a[None,:,:],offset[None,:],lo,hi,guards_lo,guards_hi,err[None,:])
            assert r['status']=='CONDITIONAL_AFFINE_BOX_CHAIN'
            corners=np.array(list(itertools.product(*zip(lo,hi))))
            vals=corners@a.T+offset
            truth_lo=vals.min(axis=0)-err
            truth_hi=vals.max(axis=0)+err
            np.testing.assert_allclose(r['tube'][1]['lower'],truth_lo,atol=1e-12)
            np.testing.assert_allclose(r['tube'][1]['upper'],truth_hi,atol=1e-12)

    def test_invalid_shape_negative_error_nan_rejected(self):
        args=(np.eye(2)[None,:,:],np.zeros((1,2)),[-1,-1],[1,1],
              [[-1,-1],[-1,-1]],[[1,1],[1,1]],np.zeros((1,2)))
        with self.assertRaises(ValueError): audit(*args[:-1], [[-0.1,0]])
        with self.assertRaises(ValueError): audit(*args[:-1], [[np.nan,0]])
        with self.assertRaises(ValueError): audit(*args[:-1], [[0]])
        with self.assertRaises(ValueError): audit(*args[:-1], [[0,0]], atol=-1)



class S150G11GuardedPartialTests(unittest.TestCase):
    """Two actual saved source *rows*, not full 50D root existence tests."""

    def test_named_archived_target_q1_guard_face(self):
        from stage_box_reachability import s150_g11_guarded_w_fiber
        x=np.zeros((2,50))
        x[0,6],x[0,7]=129.74605937135485,142.1413477808394
        x[1,6],x[1,3]=129.5965704807869,143.57686678307795
        r=s150_g11_guarded_w_fiber([6.946425e-6,6.946437499999999e-6],x)
        self.assertTrue(r["legs"][0]["strict_opposing_faces"])
        self.assertGreater(float(r["legs"][0]["lower_left_A"]),.3)
        self.assertEqual(r["status"],"CONDITIONAL_UNIQUE_GUARDED_G11_SCALAR_ROOTS")

    def test_named_archived_target_q2_guard_face(self):
        from stage_box_reachability import s150_g11_guarded_w_fiber
        x=np.zeros((2,50))
        x[0,18],x[0,19]=-11.892524976449714,.036539288141262456
        x[1,18],x[1,15]=-11.954191759915119,-1.7578110621945489
        r=s150_g11_guarded_w_fiber([6.9509375e-6,6.95095e-6],x)
        self.assertTrue(r["legs"][1]["strict_opposing_faces"])
        self.assertGreater(float(r["legs"][1]["lower_right_A"]),.22)

    def test_original_first_prep_old_diode_not_static_equilibrium(self):
        # Archival initial50 values and literal original source diode law.
        import math
        kB,qe=1.380649e-23,1.602176634e-19
        T,Tnom,n=298.15,300.15,5.4
        Is=.88e-12*(T/Tnom)**(3/n)*math.exp(
            qe*1.11*(T-Tnom)/(kB*n*T*Tnom))
        av=n*kB*T/qe
        ib_old=5.193079316339365
        vj_old=4.087729751223548
        eta0=Is*math.exp(vj_old/av)-Is-ib_old
        self.assertGreater(eta0, .000249)
        self.assertLess(eta0,.000251)
        # Source BE identity is delta ib=(1+TT/h) delta z+eta0.
        # Dropping eta0 invalidates the claimed radial monotonic product.

    def test_bad_source_face_and_old_charge_shift_fail_closed(self):
        from stage_box_reachability import s150_g11_guarded_w_fiber as gate
        x=np.zeros((2,50));x[1,3]=500.
        self.assertEqual(gate([0,1e-11],x)["status"],"INCONCLUSIVE_GUARD_FACES")
        # An old-u shift changes the GL32 *charge*, not just the Ohmic KCL.
        x[:]=0.;x[0,6]=-.5;x[1,3]=-41.06956801685769
        self.assertEqual(gate([0,12.5e-12],x)["status"],"INCONCLUSIVE_GUARD_FACES")
        for t,state,eps in (([0,0],x,.01),([0,1],x,1),
                            ([0,1],np.zeros((2,49)),.01)):
            with self.assertRaises(ValueError):gate(t,state,radius_V=eps)


if __name__=='__main__':
    unittest.main()
