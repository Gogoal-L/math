"""Analytic and randomized implicit-source goal Hessian verification."""
import unittest
import numpy as np
from implicit_goal_hessian import implicit_goal_hessian


class ImplicitGoalHessianTest(unittest.TestCase):
    def test_quadratic_command_with_linear_goal(self):
        alpha,x=.3,.4
        A=np.array([[1.]])
        B=np.array([[-(1+2*alpha*x)]])
        F2=np.zeros((1,2,2));F2[0,1,1]=-2*alpha
        r=implicit_goal_hessian(A,B,F2,[1.],[[0.]])
        self.assertAlmostEqual(r['goal_gradient_previous'][0],1+2*alpha*x)
        self.assertAlmostEqual(r['goal_hessian_previous'][0][0],2*alpha)

    def test_implicit_next_and_previous_nonlinearity(self):
        k,b,x=.2,.1,.3
        z=(-1+np.sqrt(1+4*k*(x+b*x*x)))/(2*k)
        A=np.array([[1+2*k*z]])
        B=np.array([[-(1+2*b*x)]])
        F2=np.zeros((1,2,2));F2[0,0,0]=2*k;F2[0,1,1]=-2*b
        q=implicit_goal_hessian(A,B,F2,[1.],[[0.]])
        J=(1+2*b*x)/(1+2*k*z)
        H=(2*b-2*k*J*J)/(1+2*k*z)
        self.assertAlmostEqual(q['goal_gradient_previous'][0],J)
        self.assertAlmostEqual(q['goal_hessian_previous'][0][0],H)

    def test_mixed_previous_next_hessian_must_be_retained(self):
        k,x=.7,.3
        z=x/(1+k*x)
        A=np.array([[1+k*x]])
        B=np.array([[k*z-1.]])
        F2=np.zeros((1,2,2));F2[0,0,1]=k;F2[0,1,0]=k
        q=implicit_goal_hessian(A,B,F2,[1.],[[0.]])
        self.assertAlmostEqual(q['goal_gradient_previous'][0],1/(1+k*x)**2)
        self.assertAlmostEqual(q['goal_hessian_previous'][0][0],-2*k/(1+k*x)**3)

    def test_two_state_implicit_matches_explicit_command(self):
        alpha,gamma,y=.35,.6,.2
        J=np.array([[1,2*alpha*y],[0,1]])
        Hf=np.zeros((2,2,2));Hf[0,1,1]=2*alpha
        F2=np.zeros((2,4,4));F2[:,2:,2:]=-Hf
        g=np.array([1,2*gamma*y])
        H=np.diag([0.,2*gamma])
        q=implicit_goal_hessian(np.eye(2),-J,F2,g,H)
        np.testing.assert_allclose(q['goal_gradient_previous'],J.T@g)
        np.testing.assert_allclose(q['goal_hessian_previous'],
            J.T@H@J+np.einsum('i,ijk->jk',g,Hf))
        self.assertLess(q['source_jacobian_residual'],1e-12)

    def test_reject_singular_implicit_jacobian(self):
        with self.assertRaises(ValueError):
            implicit_goal_hessian([[0.]],[[1.]],np.zeros((1,2,2)),[1.],[[0.]])

    def test_reject_dimension_mismatch(self):
        with self.assertRaises(ValueError):
            implicit_goal_hessian([[1.]],[[1.]],np.zeros((1,3,3)),[1.],[[0.]])

    def test_200_random_explicit_laws_as_implicit_residuals(self):
        rng=np.random.default_rng(13)
        for _ in range(200):
            n=3
            A=rng.normal(size=(n,n))
            while abs(np.linalg.det(A))<.5:
                A=rng.normal(size=(n,n))
            J=rng.normal(size=(n,n))
            h=rng.normal(size=(n,n,n));h=(h+h.transpose(0,2,1))/2
            F2=np.zeros((n,2*n,2*n))
            F2[:,n:,n:]=-np.einsum('ij,jkl->ikl',A,h)
            B=-A@J
            g=rng.normal(size=n)
            G=rng.normal(size=(n,n));G=(G+G.T)/2
            q=implicit_goal_hessian(A,B,F2,g,G)
            np.testing.assert_allclose(q['goal_gradient_previous'],J.T@g,rtol=1e-10,atol=1e-10)
            np.testing.assert_allclose(q['goal_hessian_previous'],
                J.T@G@J+np.einsum('i,ijk->jk',g,h),rtol=1e-10,atol=1e-10)


if __name__=='__main__':
    unittest.main()
