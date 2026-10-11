"""Analytic exact-fiber, finite-r cubic and command-pullback regressions."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import numpy as np
from fiber_goal_curvature import audit_fiber_goal_curvature, pullback_goal_derivatives


class FiberCurvatureTests(unittest.TestCase):
    def case(self, *, kappa=1., beta=3., lam=1., r=.4, M=0.):
        return audit_fiber_goal_curvature(
            observation_jacobian=[[1,0]],goal_gradient=[lam,0],
            observation_hessians=[[[0,0],[0,kappa]]],
            goal_hessian=[[0,0],[0,beta]],
            radius=r,fiber_third_derivative_bound=M)

    def test_same_observation_and_goal_curvature_cancel(self):
        a=self.case(kappa=2.,beta=2.,lam=1.)
        self.assertAlmostEqual(a['curvature_eigenvalues'][0],0)
        self.assertAlmostEqual(a['quadratic_minimax_radius'],0)
        self.assertAlmostEqual(a['radius_upper'],0)

    def test_linear_goal_still_hidden_by_nonlinear_observation(self):
        r=.4
        a=self.case(kappa=2.,beta=0.,lam=1.,r=r)
        self.assertAlmostEqual(a['curvature_eigenvalues'][0],-2.)
        self.assertAlmostEqual(a['quadratic_minimax_radius'],r*r/2)
        self.assertAlmostEqual(a['radius_lower'],r*r/2)

    def test_relative_hessian_exact_quadratic_radius(self):
        self.assertAlmostEqual(self.case(kappa=1.,beta=3.)['quadratic_minimax_radius'],.08)

    def test_indefinite_goal_has_both_positive_negative_variation(self):
        a=audit_fiber_goal_curvature(
            observation_jacobian=[[1,0,0]],goal_gradient=[1,0,0],
            observation_hessians=[np.zeros((3,3)).tolist()],
            goal_hessian=np.diag([0,2,-6]).tolist(),radius=.3,
            fiber_third_derivative_bound=0)
        self.assertAlmostEqual(a['quadratic_minimax_radius'],.18)
        self.assertEqual(a['curvature_inertia'],{'positive':1,'negative':1,'zero':0})

    def test_cubic_envelope_contains_exact_scalar_minimax_radius(self):
        r,alpha=.5,.4
        a=audit_fiber_goal_curvature(
            observation_jacobian=[[1,0]],goal_gradient=[0,0],
            observation_hessians=[np.zeros((2,2)).tolist()],
            goal_hessian=np.diag([0,2]).tolist(),radius=r,
            fiber_third_derivative_bound=6*abs(alpha))
        exact=(r*r+alpha*r**3)/2
        self.assertLessEqual(a['radius_lower'],exact)
        self.assertGreaterEqual(a['radius_upper'],exact)
        self.assertAlmostEqual(a['quadratic_minimax_radius'],r*r/2)

    def test_nonlinear_command_creates_curvature_from_linear_future_goal(self):
        HF=np.zeros((2,2,2))
        HF[0,1,1]=4.
        g,H=pullback_goal_derivatives(np.eye(2),HF,[1,0],np.zeros((2,2)))
        np.testing.assert_allclose(g,[1,0])
        np.testing.assert_allclose(H,[[0,0],[0,4]])

    def test_two_command_hessian_pullback_matches_exact_polynomial(self):
        alpha,beta,x,y=.4,.7,.2,.3
        u=x+alpha*y*y
        JB=np.array([[1.,0.],[2*beta*u,1.]])
        HB=np.zeros((2,2,2)); HB[1,0,0]=2*beta
        gB,GB=pullback_goal_derivatives(JB,HB,[0.,1.],np.zeros((2,2)))
        JA=np.array([[1.,2*alpha*y],[0.,1.]])
        HA=np.zeros((2,2,2)); HA[0,1,1]=2*alpha
        g0,G0=pullback_goal_derivatives(JA,HA,gB,GB)
        np.testing.assert_allclose(g0,[2*beta*u,1+4*alpha*beta*u*y])
        np.testing.assert_allclose(G0,[[2*beta,4*alpha*beta*y],
                                       [4*alpha*beta*y,4*alpha*beta*u+8*alpha**2*beta*y*y]])

    def test_120_random_cubic_exact_fibers_within_claimed_r3_range(self):
        rng=np.random.default_rng(1217)
        for _ in range(120):
            kappa,beta,lam,nu,gamma=rng.uniform(-2,2,5)
            r=float(rng.uniform(.1,.7))
            q=beta-lam*kappa
            cubic=gamma-lam*nu
            a=audit_fiber_goal_curvature(
                [[1,0]],[lam,0],[[[0,0],[0,kappa]]],
                [[0,0],[0,beta]],radius=r,
                fiber_third_derivative_bound=6*abs(cubic))
            candidates=[-r,0.,r]
            if abs(cubic)>1e-13:
                critical=-q/(3*cubic)
                if -r<=critical<=r:
                    candidates.append(critical)
            values=[q*v*v/2+cubic*v*v*v for v in candidates]
            exact=(max(values)-min(values))/2
            self.assertLessEqual(a['radius_lower'],exact+1e-10)
            self.assertGreaterEqual(a['radius_upper']+1e-10,exact)

    def test_rejects_goal_with_nonzero_first_order_fiber_gradient(self):
        with self.assertRaisesRegex(ValueError,'goal tangent'):
            audit_fiber_goal_curvature(
                [[1,0]],[1,1],[[[0,0],[0,1]]],[[0,0],[0,2]],.3)

    def test_rejects_singular_nonregular_observation(self):
        with self.assertRaisesRegex(ValueError,'full row rank'):
            audit_fiber_goal_curvature(
                [[0,0]],[0,0],[[[0,0],[0,0]]],[[0,0],[0,2]],.3)

    def test_no_nonzero_radius_certification_without_cubic_bound(self):
        a=audit_fiber_goal_curvature(
            [[1,0]],[1,0],[[[0,0],[0,0]]],[[0,0],[0,2]],.3)
        self.assertIsNone(a['radius_lower'])
        self.assertIsNone(a['radius_upper'])
        self.assertAlmostEqual(a['quadratic_minimax_radius'],.045)

    def test_cli_replays_source_quadratic_chart(self):
        d=dict(observation_jacobian=[[1,0]],goal_gradient=[1,0],
               observation_hessians=[[[0,0],[0,2]]],
               goal_hessian=[[0,0],[0,0]],radius=.5,
               fiber_third_derivative_bound=0)
        with tempfile.TemporaryDirectory() as t:
            src=Path(t)/'input.json'; dst=Path(t)/'output.json'
            src.write_text(json.dumps(d),encoding='utf8')
            proc=subprocess.run([
                sys.executable,str(Path(__file__).with_name('fiber_goal_curvature.py')),
                str(src),'--output',str(dst)],
                capture_output=True,text=True)
            self.assertEqual(proc.returncode,0,proc.stderr)
            self.assertAlmostEqual(
                json.loads(dst.read_text())['quadratic_minimax_radius'],.125)


if __name__=='__main__': unittest.main()
