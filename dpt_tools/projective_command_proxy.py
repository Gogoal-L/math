"""Exact projective PREP-conditioned decoder for a stored six-axis affine proxy.

Given five current samples (I12,I31,I42,I46,I60), three KNOWN
normalized digital-PREP amplitudes a and three unknown normalized coordinates
u=(L,kappa,filter bandwidth), use m=m0+M diag(radius)*(a,u).
The same positive gain and offset act on all five currents.

This is NOT a nonlinear-source, root/guard, instrument or native certificate.
All JSON numeric literals are interpreted as exact binary64 rationals.
"""
from fractions import Fraction as F
from itertools import permutations, product


def _coefs(data):
    data = data.get("proxy", data)
    m = tuple(F(x) for x in data.get("m0_A", data.get("m0", ())))
    M = data.get("M5_A_per_parameter", data.get("M"))
    rad = data.get("bank_radius", data.get("radius"))
    g = data.get("g6_J_per_parameter", data.get("g"))
    G0 = F(data.get("G0_J", data.get("G0", 0)))
    if len(m) != 5 or len(M) != 5 or len(rad) != 6 or len(g) != 6:
        raise ValueError("expected five currents and six proxy parameters")
    if any(len(row) != 6 for row in M) or any(F(x) <= 0 for x in rad):
        raise ValueError("invalid 5x6 proxy or nonpositive radii")
    C = tuple(tuple(F(M[i][j])*F(rad[j]) for j in range(6)) for i in range(5))
    c = tuple(F(g[j])*F(rad[j]) for j in range(6))
    return m, C, c, G0


def _dot(v, w):
    return sum((a*b for a, b in zip(v, w)), F(0))


def _det4(mat):
    total = F(0)
    for perm in permutations(range(4)):
        sign = (-1)**sum(perm[i] > perm[j] for i in range(4)
                         for j in range(i+1, 4))
        value = F(sign)
        for i in range(4):
            value *= mat[i][perm[i]]
        total += value
    return total


def _inverse4(mat):
    A = [[F(mat[i][j]) for j in range(4)] +
         [F(i == j) for j in range(4)] for i in range(4)]
    for j in range(4):
        k = next((k for k in range(j, 4) if A[k][j]), None)
        if k is None:
            raise ValueError("singular projective observation matrix")
        A[j], A[k] = A[k], A[j]
        pivot = A[j][j]
        A[j] = [x/pivot for x in A[j]]
        for i in range(4):
            if i != j:
                mul = A[i][j]
                A[i] = [A[i][k]-mul*A[j][k] for k in range(8)]
    return tuple(tuple(row[4:]) for row in A)


def matrix(data, a):
    m, C, _, _ = _coefs(data)
    aa = tuple(F(x) for x in a)
    if len(aa) != 3 or any(abs(x) > 1 for x in aa):
        raise ValueError("normalized recorded PREP outside [-1,1]^3")
    base = [m[i]+_dot(C[i][:3], aa) for i in range(5)]
    return tuple(tuple([base[i]-base[0]] +
                       [C[i][j]-C[0][j] for j in range(3, 6)])
                 for i in (4, 1, 2, 3))


def forward(data, a, u):
    m, C, _, _ = _coefs(data)
    x = tuple(F(t) for t in (*a, *u))
    if len(x) != 6 or any(abs(t) > 1 for t in x):
        raise ValueError("normalized proxy coordinates outside [-1,1]^6")
    return tuple(m[i]+_dot(C[i], x) for i in range(5))


def decode(data, a, observed_currents):
    """Return conditional proxy goal in J; do not label real noisy inputs exact."""
    _, _, c, G0 = _coefs(data)
    y = tuple(F(t) for t in observed_currents)
    if len(y) != 5:
        raise ValueError("expected five measured currents in A")
    inv = _inverse4(matrix(data, a))
    d = tuple(y[i]-y[0] for i in (4, 1, 2, 3))
    v = tuple(_dot(row, d) for row in inv)
    if v[0] <= 0:
        raise ValueError("invalid positive common-gain orientation")
    u = tuple(v[i]/v[0] for i in range(1, 4))
    goal = G0+_dot(c[:3], tuple(F(x) for x in a))+_dot(c[3:], u)
    return {"u": u, "record_gain": v[0], "goal_J": goal,
            "status": "CONDITIONAL_STORED_AFFINE_PROXY_ESTIMATE"}


def certify(data):
    """Exact determinant and true-proxy anchor-D support for the full box."""
    m, C, _, _ = _coefs(data)
    zero = (F(0),)*3
    d0 = _det4(matrix(data, zero))
    slopes = []
    for j in range(3):
        a = list(zero)
        a[j] = F(1)
        slopes.append(_det4(matrix(data, a))-d0)
    variation = sum(map(abs, slopes), F(0))
    lo, hi = d0-variation, d0+variation
    Dmin = (m[4]-m[0])-sum(
        (abs(C[4][j]-C[0][j]) for j in range(6)), F(0))
    if lo <= 0 <= hi or Dmin <= 0:
        raise ValueError("cannot certify global rank or denominator positivity")
    return {"status": "CERTIFIED_STORED_PROXY_ONLY",
            "det_center": d0, "det_slopes": tuple(slopes),
            "det_min": lo, "det_max": hi, "D_min": Dmin}


def sensor_certificate(data, noise_abs_A, gain_lower):
    """Exact 8*8*32 corner error for this *affine proxy* and scenario.

    H(a) differs only in its first column, affine in recorded a. Its
    determinant and adjugate entries are affine in a. The goal error
      [c_u*w_tail - (c_u*u)*w0] / (gain+w0)
    with w=H(a)^-1 times common-anchor noise differences is separately
    linear-fractional in a and sensor errors, affine in u. On a strictly
    positive effective-gain domain, extreme absolute error is at corners.
    At larger gain the absolute error decreases. Each rational result
    is exact for the parsed stored coefficients; no source/physical bound.
    """
    certify(data)
    eps, gam = F(noise_abs_A), F(gain_lower)
    if eps < 0 or gam <= 0:
        raise ValueError("noise must be nonnegative and gain positive")
    _, _, c, _ = _coefs(data)
    max_err, min_gain, witness, count = F(0), gam, None, 0
    for a in product((-1, 1), repeat=3):
        A = _inverse4(matrix(data, a))
        for u in product((-1, 1), repeat=3):
            for signs in product((-1, 1), repeat=5):
                e = [eps*s for s in signs]
                delta = [e[i]-e[0] for i in (4, 1, 2, 3)]
                w = [_dot(row, delta) for row in A]
                gain = gam+w[0]
                count += 1
                min_gain = min(min_gain, gain)
                if gain <= 0:
                    raise ValueError("effective gain not positive for whole box")
                err = abs(_dot(c[3:], tuple(
                    w[i+1]-F(u[i])*w[0] for i in range(3)))/gain)*F(10**9)
                if err > max_err:
                    max_err, witness = err, (a, u, signs)
    return {"status": "FINITE_CORNER_CERTIFIED_STORED_PROXY",
            "count": count, "max_abs_goal_error_nJ": max_err,
            "minimum_effective_gain": min_gain, "witness": witness,
            "claim_ceiling": "Stored affine proxy and hypothetical joint sensor envelope only"}

def audit_source_gap(data, a, u, actual_currents, actual_goal_J):
    """Exact post-hoc source/model correction; not a pretarget predictor.

    Requires matched source-law currents and the future goal for an actual
    same-command member, so this is for source-replay certification only.
    Do not apply to uncalibrated measured currents or fit to heldout goals.
    """
    _, _, c, G0 = _coefs(data)
    ua = tuple(F(x) for x in u)
    aa = tuple(F(x) for x in a)
    if len(ua) != 3 or any(abs(x) > 1 for x in ua):
        raise ValueError("normalized source parameter outside proxy bank")
    nominal_currents = forward(data, aa, ua)
    measured = tuple(F(x) for x in actual_currents)
    if len(measured) != 5:
        raise ValueError("expected five actual law currents")
    difference = [measured[i]-measured[0] -
                  (nominal_currents[i]-nominal_currents[0])
                  for i in (4, 1, 2, 3)]
    inv = _inverse4(matrix(data, aa))
    w = tuple(_dot(row, difference) for row in inv)
    alpha = 1+w[0]
    if alpha <= 0:
        raise ValueError("actual homogeneous coordinate nonpositive")
    nominal_goal = G0+_dot(c[:3], aa)+_dot(c[3:], ua)
    gap = F(actual_goal_J)-nominal_goal
    mixed = _dot(c[3:], tuple(w[i+1]-ua[i]*w[0] for i in range(3)))
    numerator = alpha*gap-mixed
    output = numerator/alpha
    if output != F(actual_goal_J)-decode(data,aa,measured)["goal_J"]:
        raise AssertionError("matched source/goal algebra mismatch")
    return {"status":"POSTHOC_STORED_PROXY_SOURCE_GAP_IDENTITY",
            "homogeneous_gain":alpha,
            "goal_model_gap_J":gap,
            "joint_numerator_J":numerator,
            "goal_error_J":output}
