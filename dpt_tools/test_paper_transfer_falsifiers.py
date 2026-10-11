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


if __name__ == "__main__":
    unittest.main()
