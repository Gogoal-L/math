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


if __name__=='__main__':
    unittest.main()
