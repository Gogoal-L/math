"""Analytic, adversarial and independent subset enumeration tests.

All cases are synthetic. No physical SiC or S09 claim is tested.
"""
import itertools
import unittest

import numpy as np

import goal_lipschitz_stability as gls


def _audit(obs, goals, cand, *, obsrad=None, candrad=None, eta=None,
           tau=(1.,), gain=(1.,), costs=None, cap=18):
    obs = np.asarray(obs, dtype=float)
    cand = np.asarray(cand, dtype=float)
    g = np.asarray(goals, dtype=float)
    n = len(obs)
    k = g.shape[1] if g.ndim == 2 else 1
    return gls.audit(obs, g, cand,
                     observation_radii=np.zeros(obs.shape[1]) if obsrad is None else obsrad,
                     candidate_radii=np.zeros(cand.shape[1]) if candrad is None else candrad,
                     goal_uncertainty=np.zeros((n, k)) if eta is None else eta,
                     goal_tolerances=tau, lipschitz_limits=gain,
                     candidate_costs=np.ones(cand.shape[1]) if costs is None else costs,
                     exact_cap=cap)


class LipschitzFiniteBank(unittest.TestCase):
    def test_analytic_two_history_recovery(self):
        r = _audit([[0.], [1.]], [[0.], [4.]], [[0.], [1.]], tau=[1.4])
        self.assertAlmostEqual(r['baseline_radii'][0], 1.5)
        self.assertAlmostEqual(r['selected_radii'][0], (4-np.sqrt(2))/2)
        self.assertEqual(r['selected_indices'], [0])
        self.assertEqual(r['status'], 'EXACT_MIN_COST_STABLE_REPAIR')

    def test_synergistic_two_coordinates_cannot_be_reduced_to_set_cover(self):
        # Target separation 4, tolerance 1, K=1 demands distance at least 2.
        # Each candidate distance sqrt(2) is insufficient; two together give 2.
        v=np.sqrt(2)
        r=_audit([[0.], [0.]], [[0.],[4.]], [[0.,0.,0.],[v,v,v]], tau=[1.],
                 costs=[1.,1.,3.])
        self.assertEqual(r['selected_indices'], [0,1])
        self.assertAlmostEqual(r['selected_cost'], 2.)
        self.assertAlmostEqual(r['selected_radii'][0], 1.)

    def test_uncertainty_box_gap_is_distance_of_boxes_not_center_distance(self):
        r = _audit([[0.],[0.]], [[0.],[4.]], [[0.],[0.8]], candrad=[0.5],tau=[1.],gain=[5.])
        self.assertEqual(r['status'], 'NO_LIBRARY_STABLE_REPAIR')
        self.assertAlmostEqual(r['all_feature_radii'][0], 2.)

    def test_intrinsic_goal_uncertainty_cannot_be_repaired(self):
        r=_audit([[0.]],[[0.]],[[3.]],eta=[[2.]],tau=[1.])
        self.assertEqual(r['status'], 'INTRINSIC_GOAL_UNCERTAINTY')
        self.assertAlmostEqual(r['baseline_radii'][0],2.)

    def test_zero_lipschitz_gain_is_constant_decoder_even_after_new_sensor(self):
        r=_audit([[0.],[1.]],[[0.],[4.]],[[0.],[100.]],tau=[1.],gain=[0.])
        self.assertEqual(r['status'],'NO_LIBRARY_STABLE_REPAIR')
        self.assertAlmostEqual(r['baseline_radii'][0],2.)
        self.assertAlmostEqual(r['all_feature_radii'][0],2.)

    def test_k_minimal_gain_vs_target_tolerance(self):
        r=_audit([[0.],[2.]],[[0.],[4.]],np.zeros((2,0)),tau=[1.],gain=[0.5])
        self.assertEqual(r['status'],'NO_LIBRARY_STABLE_REPAIR')
        self.assertAlmostEqual(r['minimum_required_gain_before'][0],1.)
        # K=0.5 incurs radius 1.5 while K_min for tau=1 is exactly 1.
        self.assertAlmostEqual(r['baseline_radii'][0],1.5)

    def test_multi_command_shared_measurement_set(self):
        r=_audit([[0.],[0.]], [[0.,0.],[4.,2.]], [[0.],[2.]],tau=[1.,0.5],gain=[1.,1.])
        self.assertEqual(r['selected_indices'],[0])
        self.assertAlmostEqual(r['selected_radii'][0],1.)
        self.assertAlmostEqual(r['selected_radii'][1],0.)

    def test_touching_box_boundaries_remain_compatible(self):
        r=_audit([[0.],[2.]],[[0.],[4.]],np.zeros((2,0)),obsrad=[1.],tau=[1.],gain=[999.])
        self.assertAlmostEqual(r['baseline_radii'][0],2.)

    def test_invalid_input_rejected(self):
        with self.assertRaises(ValueError):
            _audit([[0.],[1.]],[[0.],[3.]],[[0.],[1.]],candrad=[-0.1])
        with self.assertRaises(ValueError):
            _audit([[0.],[1.]],[[0.],[3.]],[[0.],[1.]],gain=[-1])

    def test_constructive_decoder_is_lipschitz_and_uniform_on_boxes(self):
        # 1D interval boxes, K=1, goal intervals centered 0, 3.
        centers=np.array([[0.],[2.]])
        widths=np.array([0.2])
        goals=np.array([0.,3.]);unc=np.array([0.1,0.2]);K=1.
        r=_audit(centers,goals,np.zeros((2,0)),obsrad=widths,eta=unc[:,None],tau=[2.],gain=[K])
        eps=r['baseline_radii'][0]
        self.assertAlmostEqual(eps,0.85)   # (3+0.3-1*1.6)/2
        ys=np.arange(-1.,3.01,0.025)
        vals=np.array([gls.decoder_value([y],centers,widths,goals,unc,eps,K) for y in ys])
        for i,c in enumerate(centers[:,0]):
            for y in np.linspace(c-widths[0],c+widths[0],7):
                v=gls.decoder_value([y],centers,widths,goals,unc,eps,K)
                self.assertLessEqual(abs(v-goals[i])+unc[i],eps+1e-12)
        self.assertTrue(np.all(np.abs(np.diff(vals)) <= K*0.025+1e-11))

    def test_stage_closure_alias_lower_bound_even_when_immediate_goal_agrees(self):
        rep=gls.transition_pair_floor([[0.],[0.]], [[-1.],[1.]], 1.)
        self.assertAlmostEqual(rep['minimum_uniform_update_defect_lower_bound'],1.)
        self.assertEqual(rep['witness_indices'],[0,1])

    def test_stage_pair_floor_allows_nonzero_initial_distance(self):
        rep=gls.transition_pair_floor([[0.],[1.]], [[0.],[4.]], 2.)
        self.assertAlmostEqual(rep['minimum_uniform_update_defect_lower_bound'],1.)

    def test_stage_pair_floor_is_only_lower_not_vector_sufficiency(self):
        rep=gls.transition_pair_floor([[0.,0.],[0.,0.]], [[2.,1.],[2.,1.]], 1.)
        self.assertAlmostEqual(rep['minimum_uniform_update_defect_lower_bound'],0.)
        self.assertEqual(rep['status'],'NECESSARY_PAIR_FLOOR_ONLY')

    def test_goal_unit_rescaling_keeps_optimal_subset(self):
        o=np.array([[0.],[1.]])
        g=np.array([[0.],[4.]])
        p=np.array([[0.,0.],[1.,2.]])
        a=_audit(o,g,p,tau=[1.],gain=[0.5],costs=[1.,2.])
        b=_audit(o,10*g,p,tau=[10.],gain=[5.],costs=[1.,2.])
        self.assertEqual(a['selected_indices'],b['selected_indices'])
        np.testing.assert_allclose(10*np.array(a['baseline_radii']), b['baseline_radii'])

    def test_large_library_greedy_reports_only_feasible_not_optimal(self):
        q=np.vstack([np.zeros(19),np.ones(19)])
        r=_audit([[0.],[0.]],[[0.],[4.]],q,tau=[1.],gain=[1.],cap=18)
        self.assertEqual(r['status'],'GREEDY_FEASIBLE_NOT_PROVEN_MINIMUM')
        self.assertLessEqual(r['selected_radii'][0],1.)
        self.assertGreaterEqual(len(r['selected_indices']),4)

    def test_end_to_end_npz_cli_schema(self):
        import tempfile
        import subprocess
        import sys
        import json
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            file=Path(tmp)/'bank.npz'
            out=Path(tmp)/'result.json'
            np.savez(file,observations=np.zeros((2,1)),goals=np.array([[0.],[4.]]),
                     candidates=np.array([[0.],[3.]]),observation_radii=np.array([0.]),
                     candidate_radii=np.array([0.]),goal_uncertainty=np.zeros((2,1)),
                     goal_tolerances=np.array([1.]),lipschitz_limits=np.array([1.]),
                     candidate_costs=np.array([2.]))
            subprocess.run([sys.executable,str(Path(gls.__file__)),str(file),'--output',str(out)],
                           check=True,capture_output=True,text=True)
            data=json.loads(out.read_text())
            self.assertEqual(data['selected_indices'],[0])
            self.assertEqual(data['status'],'EXACT_MIN_COST_STABLE_REPAIR')

    def test_random_independent_all_subset_oracle(self):
        rng=np.random.default_rng(8641)
        for _ in range(90):
            n=int(rng.integers(2,6));m=int(rng.integers(1,3));p=int(rng.integers(0,6));k=int(rng.integers(1,4))
            o=rng.normal(size=(n,m));g=rng.normal(size=(n,k))*3
            q=rng.normal(size=(n,p));ro=rng.uniform(0,.3,size=m)
            rp=rng.uniform(0,.3,size=p);eta=rng.uniform(0,.15,size=(n,k))
            tau=rng.uniform(.2,1.5,size=k);ks=rng.uniform(.1,4,size=k)
            costs=rng.uniform(.01,3,size=p)
            r=_audit(o,g,q,obsrad=ro,candrad=rp,eta=eta,tau=tau,gain=ks,costs=costs)
            values=[]
            feasible=[]
            for mask in range(1<<p):
                keep=[i for i in range(p) if mask>>i&1]
                rs=[]
                for c in range(k):
                    v=float(np.max(eta[:,c]))
                    for i,j in itertools.combinations(range(n),2):
                        gaps=np.maximum(0.,np.abs(o[i]-o[j])-2*ro)
                        if keep:
                            gaps=np.r_[gaps,np.maximum(0.,np.abs(q[i,keep]-q[j,keep])-2*rp[keep])]
                        d=float(np.linalg.norm(gaps))
                        v=max(v,float((abs(g[i,c]-g[j,c])+eta[i,c]+eta[j,c]-ks[c]*d)/2))
                    rs.append(v)
                values.append(rs)
                if all(a<=t+1e-10 for a,t in zip(rs,tau)):
                    feasible.append((float(sum(costs[keep])),len(keep),tuple(keep)))
            np.testing.assert_allclose(r['baseline_radii'], values[0], atol=1e-12)
            if feasible:
                optimum=min(feasible)
                self.assertIn(r['status'],['BASELINE_SUFFICIENT','EXACT_MIN_COST_STABLE_REPAIR'])
                self.assertAlmostEqual(r['selected_cost'],optimum[0],places=10)
            else:
                self.assertIn(r['status'],['INTRINSIC_GOAL_UNCERTAINTY','NO_LIBRARY_STABLE_REPAIR'])

if __name__=='__main__':
    unittest.main()
