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

if __name__ == "__main__":
    unittest.main()
