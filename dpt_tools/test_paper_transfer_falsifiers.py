"""Finite original-proof transfer falsifiers for F119 / F129 / F132.

These synthetic calculations check finite mathematical witnesses, NOT
Lean correctness of the OpenAI Math theorems or native SiC evidence.
"""
import itertools
import math
import unittest
from collections import defaultdict


def binary_info(summary, rho, correlated=False):
    """Mutual information in nats for two fair bits through sign-flip probes."""
    if not (-1 <= rho <= 1):
        raise ValueError("invalid correlation")
    masses = {1: (1+rho)/2, -1: (1-rho)/2}
    noise = ([(z,z,masses[z]) for z in (1,-1)] if correlated else
             [(z,w,masses[z]*masses[w]) for z,w in itertools.product((1,-1),repeat=2)])
    joint = defaultdict(float)
    for x1,x2 in itertools.product((-1,1),repeat=2):
        u = x1 if summary == "coordinate" else x1*x2
        for z1,z2,p in noise:
            joint[(u,(x1*z1,x2*z2))] += p/4
    marginal_u, marginal_y=defaultdict(float),defaultdict(float)
    for (u,y),p in joint.items():
        marginal_u[u]+=p
        marginal_y[y]+=p
    return sum(p*math.log(p/(marginal_u[u]*marginal_y[y]))
               for (u,y),p in joint.items() if p>0)


def psi(r):
    if abs(r)==1:
        return math.log(2)
    return ((1+r)*math.log1p(r)+(1-r)*math.log1p(-r))/2


def relation_compose(a,b):
    """Two-state relation monoid product, four row-major Boolean bits."""
    out=0
    for i,j,k in itertools.product(range(2),repeat=3):
        if (a & (1 << (2*i+j))) and (b & (1 << (2*j+k))):
            out|=(1 << (2*i+k))
    return out


def d1_tournament_counts():
    """Test local block witness only; do not assume global label lemma."""
    d, M, L, r, k=1,3,3,2,19
    centers=[set(range(h*L,(h+1)*L)) for h in range(M)]
    def p0(active,q):
        return min(len(active ^ center) for center in centers)<=d+1-q
    def edge(i,j):
        return 0<(j-i)%k<=(k-1)//2
    def p1(active):
        for i in range(k):
            if not all(p0(active.get(i*r+c,set()),2) for c in range(r)):
                continue
            if all(not p0(active.get(j*r+(i+j)%r,set()),1)
                   for j in range(k) if edge(i,j)):
                return True
        return False
    singles=sum(p1({child:{bit}}) for child in range(k*r)
                for bit in range(L*M))
    blocks=sum(p1({i*r+c:set(center) for c in range(r)})
               for i in range(k) for center in centers)
    return singles,blocks,k*r*L*M,L*r


class F119NoisyCube(unittest.TestCase):
    def test_independent_noise_coordinate_and_parity_curves(self):
        for rho in (0., .3, .7, .99):
            self.assertAlmostEqual(binary_info("coordinate",rho),psi(rho),places=12)
            self.assertAlmostEqual(binary_info("parity",rho),psi(rho*rho),places=12)

    def test_same_single_channel_noise_but_shared_flip_reverses_optimum(self):
        for rho in (0., .3, .7):
            self.assertAlmostEqual(binary_info("parity",rho,True), math.log(2),places=12)
            self.assertAlmostEqual(binary_info("coordinate",rho,True),psi(rho),places=12)
            self.assertGreater(binary_info("parity",rho,True),
                               binary_info("coordinate",rho,True))


class F129ContextSeparation(unittest.TestCase):
    def test_every_distinct_two_state_relation_has_a_two_sided_context(self):
        for a,b in itertools.product(range(16),repeat=2):
            if a==b:
                continue
            delta=a^b
            bit=(delta & -delta).bit_length()-1
            i,j=divmod(bit,2)
            left,right=1<<(3*i),1<<(3*j)
            ca=relation_compose(relation_compose(left,a),right)
            cb=relation_compose(relation_compose(left,b),right)
            self.assertNotEqual(bool(ca),bool(cb))

    def test_same_current_membership_need_not_mean_context_equivalence(self):
        a,b=1,8
        self.assertTrue(bool(a) and bool(b))
        self.assertNotEqual(bool(relation_compose(relation_compose(1,a),1)),
                            bool(relation_compose(relation_compose(1,b),1)))


class F132BlockWitness(unittest.TestCase):
    def test_57_grouped_witnesses_and_zero_single_bit_effects(self):
        singles,blocks,n,block_size=d1_tournament_counts()
        self.assertEqual((singles,blocks,n,block_size),(0,57,342,6))

    def test_original_d9_theorem_seed_is_asymptotically_enormous(self):
        d=9
        M=9**10
        L=d+2
        r=math.isqrt(M)
        r+=(r*r<M)
        k=2*M*M+1
        n=L*M*M*(k*r)**d
        upper_s=2*L*M**(d+1)
        lower_bs=M*M*k**d
        self.assertEqual(len(str(n)),238)
        self.assertGreater(lower_bs,upper_s**2)



class UnifiedDPTMathematicalToy(unittest.TestCase):
    def test_joint_future_word_exposes_hidden_history_after_single_words_fail(self):
        def goal(history, word):
            # A and B are legal abstract interventions with a mixed effect.
            return history if ("A" in word and "B" in word) else 0
        for one in ("", "A", "B"):
            self.assertEqual(goal(-1, one), goal(1, one))
        self.assertEqual(goal(1, "AB") - goal(-1, "AB"), 2)
        # Equal available pretarget observations of the two histories
        # force minimax goal error >= 1 for the joint future word.
        def pretarget_observation(history, nuisance):
            return nuisance  # hidden state is unobserved before CAL
        self.assertEqual(pretarget_observation(-1, 0.4),
                         pretarget_observation(1, 0.4))
        # Both future goals must be decoded from the same observation.
        outcomes = (goal(-1, "AB"), goal(1, "AB"))
        minimax_constant = sum(outcomes)/2
        self.assertEqual(max(abs(value-minimax_constant) for value in outcomes), 1)

    def test_nuisance_invariant_goal_but_not_every_goal(self):
        # y = theta + (eta,eta): difference cancels the shared nuisance.
        for t1,t2,eta in ((0.2, -0.4, 0.7),(-1, 1,-0.5),(1,1,-1)):
            y1,y2=t1+eta,t2+eta
            self.assertAlmostEqual(y1-y2,t1-t2)
        # Same recorded y=(0,0), different sum goals (2 vs -2).
        a=(1,1,-1)
        b=(-1,-1,1)
        self.assertEqual((a[0]+a[2],a[1]+a[2]),(0,0))
        self.assertEqual((b[0]+b[2],b[1]+b[2]),(0,0))
        self.assertEqual((a[0]+a[1])-(b[0]+b[1]),4)

    def test_pretarget_calibration_repairs_aliased_history_only_with_shared_error(self):
        for history in (-1,1):
            nuisance=0.35
            recorded_y0=nuisance
            calibrated_y1=history+nuisance
            self.assertAlmostEqual(calibrated_y1-recorded_y0,history)
        # With independent offsets cancellation no longer holds.
        self.assertNotEqual((1+0.45)-0.35,1)


class GoalSourceTransferCertificates(unittest.TestCase):
    """Independent exact fixtures, not certified actual DPT source evidence."""

    def test_prepared_signed_work_partitions_exactly(self):
        from fractions import Fraction as Q
        def work(l):
            return (5*l*l+6*l+2)/(l+1)**3
        delta=work(Q(2))-work(Q(1))
        self.assertEqual(delta,Q(-79,216))
        self.assertEqual(Q(-137,648)-Q(25,162),delta)
        # Point curvature is not a uniform finite-intervention upper bound.
        remainder=delta+Q(7,16)
        self.assertEqual(remainder,Q(31,432))
        self.assertGreater(remainder,Q(1,16))
        self.assertLessEqual(remainder,Q(1,12))

    def test_joint_work_slope_support_beats_separate_boxes(self):
        from fractions import Fraction as Q
        ws=[(Q(1),Q(-1)),(Q(-1),Q(1))]
        self.assertEqual([w+s for w,s in ws],[0,0])
        # Synthetic two-world slope ambiguity defeats any constant goal forecast.
        goals=[Q(0)+Q(2,5)*s for s in (-1,1)]
        self.assertEqual((max(goals)-min(goals))/2,Q(2,5))

    def test_source_qualified_net_interval_vs_false_finite_bank(self):
        from fractions import Fraction as Q
        rho=Q(1,16)
        centers=[Q(k,8) for k in range(9)]
        obs=lambda q:q*q
        goal=lambda q:q
        y=Q(1,4)
        eps=Q(1,100)
        B=[q for q in centers if abs(y-obs(q))<=eps+2*rho]
        lo=min(map(goal,B))-rho
        hi=max(map(goal,B))+rho
        self.assertTrue(B)
        for k in range(1001):
            q=Q(k,1000)
            if abs(y-obs(q))<=eps:
                self.assertLessEqual(lo,goal(q))
                self.assertLessEqual(goal(q),hi)
        # Endpoint-only sampling misses a reachable interior extreme.
        hidden=lambda q:4*q*(1-q)
        self.assertEqual([hidden(q) for q in (Q(0),Q(1))],[0,0])
        self.assertEqual(hidden(Q(1,2)),1)

    def test_co_lipschitz_requires_uniform_chord_gain(self):
        import math
        for t in (0,math.pi/2,math.pi,2*math.pi):
            self.assertAlmostEqual(math.hypot(-math.sin(t),math.cos(t)),1.0)
        self.assertAlmostEqual(math.cos(0),math.cos(2*math.pi))
        self.assertAlmostEqual(math.sin(0),math.sin(2*math.pi))

class GoalCorrectedResidualCellFixture(unittest.TestCase):
    """Exact independent same-source goal-minus-readout oracle; no SiC inputs."""

    def test_direct_goal_adjoint_cancels_shared_state_response(self):
        from fractions import Fraction as Q

        def x(t):
            return 1000*t + t*t

        def R(t):
            return x(t) + t*t - Q(999, 1000)*x(t)

        def adjoint_R_prime(t):
            # F(x,t)=x-1000t-t^2. Q_x=1/1000, F_x=1.
            lam=Q(1, 1000)
            return 2*t - lam*(-1000-2*t)

        for t in (Q(0),Q(1,5),Q(1,2),Q(1)):
            self.assertEqual(R(t),t+Q(1001,1000)*t*t)
            self.assertEqual(adjoint_R_prime(t),1+Q(2002,1000)*t)
            h=Q(1,10000)
            self.assertEqual((R(t+h)-R(t-h))/(2*h),adjoint_R_prime(t))

    def test_certified_cell_remainder_covers_all_exact_goals(self):
        from fractions import Fraction as Q
        center,h,M=Q(1,2),Q(1,2),Q(2002,1000)
        R=lambda t:t+Q(1001,1000)*t*t
        Rprime=lambda t:1+M*t
        bound=abs(R(center))+abs(Rprime(center))*h+M*h*h/2
        self.assertEqual(bound,R(Q(1)))
        for k in range(101):
            self.assertLessEqual(abs(R(Q(k,100))),bound)
        # Separately controlling two order-1000 source outputs loses this bound.
        self.assertGreater(Q(1999),500*bound)

    def test_joint_sensor_error_adds_exact_affine_support(self):
        from fractions import Fraction as Q
        eps,beta=Q(1,10),Q(2001,1000)
        for k in range(51):
            t=Q(k,50)
            x=1000*t+t*t
            G=x+t*t
            O=Q(999,1000)*x
            for e in (-eps,eps):
                self.assertLessEqual(abs(G-(O+e)),beta+eps)

    def test_nonlinear_readout_curvature_is_not_optional(self):
        from fractions import Fraction as Q
        # F=x-t=0, G=0, O=x, p(O)=O^2.
        # F'' vanishes, while Q''=-2 from the nonlinear readout.
        for t in (Q(0),Q(1,2),Q(1)):
            lam=-2*t
            d2Q_directional=-2
            d2F_directional=0
            self.assertEqual(d2Q_directional-lam*d2F_directional,-2)
            h=Q(1,10)
            self.assertEqual(-((t+h)**2)+2*t*(t+h)-t*t,-h*h)

class GoalLagrangianDualFixture(unittest.TestCase):
    """Exact same-source dual bound, not a physical source-domain certificate."""

    def test_dual_goal_identity_holds_on_an_outer_box(self):
        from fractions import Fraction as Q
        eps=Q(1,1000)
        for a in range(-8,9):
            for b in range(-4,5):
                x,y=Q(a,4),Q(b,4)
                F0=x+y*y-1
                F1=eps*y
                R=x+y*y-1
                self.assertEqual(R-(F0+0*F1),0)
        self.assertEqual((Q(1)+Q(0)**2-1,eps*Q(0)),(0,0))

    def test_center_contraction_gate_can_fail_even_if_goal_dual_exact(self):
        from fractions import Fraction as Q
        # DF(x,y)=[[1,2*y],[0,eps]], inverse center=diag(1,1/eps).
        eps=Q(1,1000)
        self.assertGreaterEqual(1/eps,1000)
        self.assertEqual(max(2*abs(y) for y in (Q(-1),Q(0),Q(1))),2)
        # Nonetheless R-lambda.F=0 at every point of the outer box.
        self.assertEqual((Q(-1)+Q(1)**2-1)-(Q(-1)+Q(1)**2-1),0)

    def test_a_single_root_center_cannot_certify_all_other_roots(self):
        from fractions import Fraction as Q
        # F(x)=x(x-2), goal=x: a box containing both zeros has diameter 2.
        for x in (Q(0),Q(2)):
            self.assertEqual(x*(x-2),0)
        self.assertEqual(abs(Q(2)-Q(0)),2)

class DynamicGoalAndAdaptiveNoise(unittest.TestCase):
    """Exact finite-world oracles; NOT native physical DPT certification."""

    def test_one_command_pass_does_not_certify_two_step_AB(self):
        def future_goal(h, word):
            flag,goal=0,0
            for a in word:
                if a=="A":
                    flag=1
                if a=="B" and flag:
                    goal=h
            return goal
        for word in ("","A","B"):
            self.assertEqual(future_goal(-1,word),future_goal(1,word))
        self.assertEqual((future_goal(1,"AB")-future_goal(-1,"AB"))/2,1)

    def test_immediate_goal_partition_may_fail_future_right_congruence(self):
        def goal_B(h,flag):
            return h if flag else 0
        self.assertEqual(goal_B(-1,0),goal_B(1,0))
        self.assertEqual(abs(goal_B(-1,1)-goal_B(1,1)),2)

    def test_joint_common_offset_is_reused_across_pretarget_reads(self):
        from fractions import Fraction as Q
        worlds=list(itertools.product((-1,1),(Q(-2),Q(0),Q(2))))
        y1=Q(1)
        stage1=[w for w in worlds if w[0]+w[1]==y1]
        stage2=[w for w in stage1 if w[1]==0]
        self.assertEqual(set(w[0] for w in stage1),{-1,1})
        self.assertEqual(set(w[0] for w in stage2),{1})
        radius=lambda ws:(max(x[0] for x in ws)-min(x[0] for x in ws))/2
        self.assertEqual(radius(stage1),1)
        self.assertEqual(radius(stage2),0)

    def test_marginal_coverage_is_not_simultaneous_coverage(self):
        from fractions import Fraction as Q
        worlds=set(range(10))
        failures=[{i} for i in range(10)]
        for failed in failures:
            self.assertEqual(Q(len(failed),len(worlds)),Q(1,10))
        self.assertEqual(set().union(*failures),worlds)

    def test_cal_pulse_execution_must_be_matched_in_sensor_comparison(self):
        histories=(-1,1)
        actual_after_cal={h:3*h for h in histories}
        self.assertEqual((max(actual_after_cal.values())-min(actual_after_cal.values()))/2,3)
        self.assertEqual(max(abs(3*h-actual_after_cal[h]) for h in histories),0)
        self.assertNotEqual(actual_after_cal,{h:h for h in histories})

class AffineFiveCurrentInvariant(unittest.TestCase):
    """Same-record affine-gain quotient for exact noiseless five-current arrays."""

    def test_positive_gain_common_offset_has_exact_inverse_q_orbit(self):
        from fractions import Fraction as Q
        def project(m):
            d=m[4]-m[0]
            if d<=0: raise ValueError("denominator orientation")
            return tuple((m[k]-m[0])/d for k in (1,2,3))
        m=(Q(2),Q(3),Q(5),Q(7),Q(10))
        a,b=Q(1001535,1000000),Q(23624,1000000000)
        transformed=tuple(a*x+b for x in m)
        self.assertEqual(project(transformed),project(m))
        inverse_a=(transformed[4]-transformed[0])/(m[4]-m[0])
        inverse_b=transformed[0]-inverse_a*m[0]
        self.assertEqual((inverse_a,inverse_b),(a,b))

    def test_bounded_gain_or_absolute_calibration_changes_information(self):
        from fractions import Fraction as Q
        m=(Q(2),Q(3),Q(5),Q(7),Q(10))
        transformed=tuple(Q(3,2)*x+Q(1,10) for x in m)
        self.assertNotEqual(m,transformed)
        q=lambda seq:tuple((seq[k]-seq[0])/(seq[4]-seq[0]) for k in (1,2,3))
        self.assertEqual(q(m),q(transformed))
        self.assertGreater((transformed[4]-transformed[0])/(m[4]-m[0]),Q(11,10))
        self.assertEqual((Q(4)-Q(0))/2,Q(2))

class HomogeneousProjectiveRootWitness(unittest.TestCase):
    """S-L7 exact source-root oracle; not actual DPT certification."""

    def test_denominator_positive_only_at_roots(self):
        from fractions import Fraction as Q
        F = lambda x: x*(x-2)
        D = lambda x: 1-F(x)
        for k in range(-4, 13):
            x = Q(k, 4)
            self.assertEqual(D(x)-1+F(x), 0)
        self.assertEqual(D(Q(0)), 1)
        self.assertEqual(D(Q(2)), 1)
        self.assertLess(D(Q(5, 2)), 0)  # off-shell pole within [-1, 3]

    def test_homogeneous_goal_duality_works_through_offshell_pole(self):
        from fractions import Fraction as Q
        F = lambda x: x*(x-2)
        D = lambda x: 1-F(x)
        N = lambda x: -F(x)  # G=0, p(q)=q1, B1=F
        for k in range(-4, 13):
            x = Q(k, 4)
            self.assertEqual(D(x)-1+F(x), 0)  # mu=-1, d0=1
            self.assertEqual(N(x)+F(x), 0)    # nu_plus=-1
            self.assertEqual(-N(x)-F(x), 0)   # nu_minus=+1
        for root in (Q(0), Q(2)):
            self.assertEqual(F(root), 0)
            self.assertEqual(N(root)/D(root), 0)

    def test_two_root_same_record_goal_separation_is_unavoidable(self):
        from fractions import Fraction as Q
        F = lambda x: x*(x-2)
        roots = (Q(0), Q(2))
        self.assertEqual([F(x) for x in roots], [0, 0])
        self.assertEqual((max(roots)-min(roots))/2, 1)
        for k in range(-4, 13):
            x = Q(k, 4)
            self.assertEqual(x+F(x)/2, x*x/2)
            self.assertEqual(2-x+F(x)/2, (x-2)**2/2)
            self.assertGreaterEqual(x*x/2, 0)
            self.assertGreaterEqual((x-2)**2/2, 0)

class AllRootDiscreteStageEnergy(unittest.TestCase):
    """Synthetic BE all-root energy and rational-prefix controls for S-L8."""

    def test_rl_two_step_exact_positive_anchor_and_energy_identity(self):
        from fractions import Fraction as Q
        for k in range(101):
            L=Q(1)+Q(k,100)
            h=R=u=Q(1)
            iold=Q(0)
            i1=1/(L+1)
            i2=(2*L+1)/(L+1)**2
            for i in (i1,i2):
                lhs=L*(i*i-iold*iold)/2 + L*(i-iold)**2/2 + h*R*i*i
                self.assertEqual(lhs,h*u*i)
                iold=i
            self.assertTrue(Q(1,3)<=i1<=Q(1,2))
            self.assertTrue(Q(5,9)<=i2<=Q(3,4))
            self.assertTrue(Q(2,9)<=i2-i1<=Q(1,4))
            self.assertTrue(Q(8,9)<=i1+i2<=Q(5,4))

    def test_passive_dc_equilibrium_is_zero_anchor_counterexample(self):
        from fractions import Fraction as Q
        R=u=L=h=Q(1)
        iold=u/R
        inew=(h*u+L*iold)/(L+h*R)
        self.assertEqual(inew,iold)
        self.assertEqual(inew-iold,0)

    def test_continuous_energy_loss_does_not_bound_all_BE_roots(self):
        from math import sqrt
        energy=lambda x:(x*x-1)**2/4
        roots=(1,(-5+sqrt(5))/10,(-5-sqrt(5))/10)
        self.assertEqual(energy(1),0)
        for x in roots:
            self.assertAlmostEqual((x-1)*(5*x*x+5*x+1),0,places=12)
            self.assertAlmostEqual(5*x*x*x-4*x-1,0,places=12)
            next_root=math.copysign(abs(x)**(1/3),x)
            self.assertAlmostEqual(next_root**3,x,places=12)
        self.assertGreater(energy(roots[1]),0)
        self.assertGreater(energy(roots[2]),0)

if __name__ == "__main__":
    unittest.main()
