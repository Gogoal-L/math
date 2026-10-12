# Continuous goal-information radius under correlated bounded observation error

**Date:** 2026-10-11. **Scientific state:** exact finite-dimensional centered-ellipsoid **linear** model and numerically checked synthetic implementation. **Not** an accepted DPT source result, certified nonlinear reachability, calibrated metrology, hardware sensor minimum, or new universal optimal-recovery theorem. The DPT controller retains scientific authority.

## Missing bridge and definitions

The existing Math tools cover finite-bank ambiguity and repair (goal_ambiguity_audit, goal_repair_cover, goal_lipschitz_stability) and supplied linear ordered-stage dynamics (goal_defect_transport). None of them directly evaluates a continuous, deterministic, *correlated-noise* goal-information radius. This module fills only that gap; it does not replace the DPT native constitutive-law forward model.

Fix one qualified finite-dimensional state/parameter chart and one future command:

```math
x=x_0+Bz,\quad\|z\|_2\le1;\qquad
y=Hx+Ee,\quad\|e\|_2\le1;\qquad
G(x)=G(x_0)+g^\top(x-x_0).
```

The entire ellipsoid B must be physically admissible, not just its tangent; H contains *pretarget* measurement rows; E specifies a **joint deterministic** error ellipsoid (not automatically the data covariance); g is the same-law gradient of a smooth future goal. E may be rectangular or rank deficient; B may be rank deficient and physical units stay explicit.

Set A=E^{-1}HB and $`c=B^\top g`$. Then the **global** scalar minimax risk over all estimators, possible observations and admissible states/noise is

```math
\boxed{
R=\max_{\|z\|\le1,\,\|Az\|\le1}|c^\top z|
=\min_w(\|c-A^\top w\|_2+\|w\|_2)
=\sqrt{\min_{0\le q\le1}c^\top[(1-q)I+qA^\top A]^{-1}c}.
}
```

For a singular endpoint the last expression means its finite interior limit, or the pseudoinverse when c lies in the relevant range. R is expressed in the chosen **goal's units** (V, J etc.). The minimax-optimal linear predictor has unwhitened measurement weights a=E^{-T}w and an absolute offset G(x0)-$`a^\top Hx_0`$.

**Proof capsule.** Opposite admissible states z and -z produce an identical possible observation when $`\|Az\|_2\le1`$, with appropriate opposite errors; their goal gap $`2|c^\top z|`$ yields a lower bound for every estimator. For any whitened linear decoder w, the error is bounded by $`\|c-A^\top w\|`$+$`\|w\|_2`$. Convex support-function duality equates these extrema, establishing linear minimax optimality in this bounded symmetric *linear* model. Dualizing the two squared Euclidean constraints and eliminating the positive common Lagrange-multiplier scale gives the single parameter q. In an SVD basis of A its squared objective is f(q)=sum(c_i^2/(1-q+q s_i^2)), which is convex on the domain where finite. Its derivative admits globally convergent bisection, no SciPy dependency. At minimizing q, $`v=[(1-q)I+qA^\top A]^{-1}c`$, w=qAv. Numerical implementation reports the achieved decoder upper bound and a feasible z-witness lower bound, **floating diagnostics only**, not an outward-rounded interval certificate.

**Exact mathematical prior (not OpenAI Math):** Simon Foucart and Chunyang Liao, *Radius of Information for Two Intersected Centered Hyperellipsoids and Implications in Optimal Recovery from Inaccurate Data*, Journal of Complexity 83 (2024), 101841, DOI https://doi.org/10.1016/j.jco.2024.101841, preprint https://arxiv.org/abs/2401.11112; compare Theorems 1 and 8. These mathematical facts predate our implementation. What may be new in DPT is a source-grounded application combining legal reachable sets, correlated probes and prospective target scoring.

## Synthetic verification and false claims excluded

Run from dpt_tools/:

    python -m unittest -v test_goal_ellipsoid_recovery.py

For B=I, H=[1,0], E=[0.2], the observed x1-goal has radius 0.2, while the unobserved x2-goal has radius 1. The complete state remains unidentified even though the first goal is robust. For target x1+x2, the radius is 0.2+sqrt(1-0.2^2), exercising an interior bottleneck; elliptical prior B=diag(2,1) has a separate analytic case. With H=I and E=[[0.1,0],[0.08,0.06]], the target x1+x2 radius when B=10I is ||E.T[1,1]||, preserving joint measurement-error geometry. An additional independent measurement reduces or preserves the information radius if the same original uncertainty budget remains available. Tests also cover m=0, shapes, singular E and actual NPZ-to-JSON CLI replay.

These numerical tests are **not** source-native DPT evidence. The code's algorithm_upper, feasible_witness_lower and numerical_gap fields diagnose optimizer arithmetic under its **assumed** linear chart, not the chart's physical validity.

## Additional primary OpenAI Math reading

Inspected the listed original LaTeX statements and selected proof sections at openai/math main on 2026-10-11. This is targeted source inspection, **not** a full-proof or Lean audit. The new optimal-recovery formula does not come from these papers.

| Family | Original source / inspected locator | What transfers and what does not |
| --- | --- | --- |
| **F132** | [Sensitivity and block sensitivity introduction](https://github.com/openai/math/blob/main/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/00-introduction.tex), [Proposition prop:recurrences](https://github.com/openai/math/blob/main/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/02-recurrences.tex), [quantitative separation](https://github.com/openai/math/blob/main/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/03-separation.tex) | **Design analogy**: grouped legal interventions can reveal a response missed by one-coordinate perturbations; existing DPT mixed_interaction_audit is the relevant test. Boolean exponent and sensitivity theorem do **not** transfer to analog SiC. |
| **F129** | [Two-way deterministic state lower bound introduction](https://github.com/openai/math/blob/main/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/build/sections/introduction.tex), [rank-loss theorem](https://github.com/openai/math/blob/main/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/build/sections/rank.tex) | **PARK**: finite control must distinguish context words in that special *full relation monoid/growing alphabet* model. This does not prove minimum physical memory for nonlinear SiC. Existing DPT command_word_audit/goal_word_quotient cover restricted, relevant meanings. |
| **F119** | [Binary information-contraction theorem](https://github.com/openai/math/blob/main/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/main.tex), [entropy joining proof](https://github.com/openai/math/blob/main/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/sections/canonical.tex) | **REJECT for the present gate**: independent Bernoulli corruption of uniform binary inputs and mutual-information objective are not correlated bounded oscilloscope noise and voltage/work minimax accuracy. Reopen only if a separate calibrated stochastic measurement model becomes authoritative. |

**Research judgment revision:** the strongest new route is not transferring any of those top-line theorems. It is using an existing sharp optimal-recovery result to design a falsifiable DPT legal-observation comparator. Paper counts and thematic analogies must not become evidence of native identifiability.

## Source-to-controller admission contract

1. **Select one reference.** Never combine 100-V scalar R1, 150-V active CAL/goal and 600-V native finite-command branches as if sharing a single B/H/E/g chart. Freeze model/topology, exact preparation and future command, ports/reference/window, target scorer and nuisance range.
2. **Prove joint eligibility.** Entire x0+B B2 must satisfy source constitutive law, implicit-solver branch/guard, Eth lift, valid state and parameter bounds. Calibrate a physically justified deterministic joint E including skew/gain correlations. A sample covariance without coverage evidence is insufficient.
3. **Take gradients on the same law.** H must use only truly obtainable pretarget information. g comes from same-law tangent/adjoint on the future goal; moving/tied peaks require an event-regularity analysis or a nonsmooth goal bound. Ordinary finite differences at one center are not a whole-domain certificate.
4. **Keep ordinary comparator and cost.** Compare NO_CAL against a genuinely legal active CAL row or already archived source/preparation information with identical prior and target, correctly adjusted joint E and sensor/command costs. Report R in goal units and engineering tolerance; don't rank by parameter sensitivity rank alone.
5. **Hold-out falsification.** If two actually legal histories satisfy the same observed-error budget but their future goal gap exceeds 2R plus independently qualified nonlinear/evaluation allowances, the proposed continuous chart is falsified. Passing finite source members does not prove a global continuous bound.

**First input to request from the local controller:** one actual-law **150-V Pro18C** B/H/E/g packet with units, legal-region identity, full correlated deterministic error budget, goal-gradient check, source-complete ordinary predictor and one predeclared holdout active-CAL query. Compare NO_CAL against CAL while respecting access time. The Pro18C seven-member near-observation work diameter (0.335303 nJ) becomes a consistency challenge **only if** these are the same observation and goal contracts. Pro18B's dynamic failure requires a separate recursive-state/update analysis and is not repaired by this static one-command result.

**Strongest counterexamples.** G(x)=x^2 on [-1,1] centered at 0 has derivative g=0 and therefore zero linearized radius but nonzero true goal variation: a linear chart cannot certify a nonlinear DPT goal without an independent remainder. Correlated measurement error cannot be reinterpreted as unrelated axis-aligned boxes without changing the uncertainty set. A source-complete ordinary native predictor may already satisfy the declared work/peak tolerance without added information; this is a valid NO_NEW_MEASUREMENT outcome.

**Terminal:** Math-only conditional construction and synthetic numerical validation. Do not promote, freeze S09, or claim a native performance improvement until the local scientific owner supplies and scores a legal same-reference prospective packet.


## Extension: rank-deficient/common-mode deterministic observation uncertainty (2026-10-11)

**Motivation from a deliberately invalid F119 transfer.** The OpenAI Math F119 binary-coordinate optimum requires *independently* corrupted channels. With perfectly correlated sensor noise, a goal-aligned contrast can be exact although neither individual sensor is noiseless. The original E^{-1} implementation silently excludes this physically important regime. The extension allows E in R^{m x p} of any rank (including 0), with a **joint hard error ball** ||e||_2<=1; it does not assume independent sensor errors.

**Reduction and proof.** Start with the same centered prior ||z||<=1, observations H B z+E e, and goal c.T z. Take a full left SVD E=U_r Sigma_r V_r.T and complement U_0. Two opposite states z and -z are observation-indistinguishable exactly when H B z belongs to E(B2), equivalent to the pair of conditions

    C z=0,                        C=U_0.T @ H @ B;
    ||Sigma_r^-1 U_r.T H B z|| <=1.

Choose orthonormal columns Z spanning ker C. Then the information radius reduces without approximation (for **mathematically exact ranks**) to

    R = max_{||v||<=1, ||A v||<=1} |c_red.T v|,
    A=Sigma_r^-1 U_r.T H B Z,  c_red=Z.T c.

It is the same convex two-ellipsoid problem **after** enforcing exact noiseless observations. An optimal full linear decoder a is obtained by (i) solving the dual in noisy U_r directions, (ii) adding U_0 components to match the goal response in row(C), which costs zero measurement error because E.T U_0=0. The code returns the achieved upper ||c-(HB).T a||+||E.T a||, a feasible opposite-state lower, and their floating gap. No pseudo-inverse of the full E is used for inversion on its nullspace.

**Independent analytic fixtures and numerically checkable consequences.**

- H=B=I_2, E=[0.2,0.2].T, target g=(1,-1): observation difference exactly cancels the common factor, R=0, a=(1,-1).
- Same prior/measurement, g=(1,1): common source uncertainty remains, R=0.4.
- Add an *independent* uncertainty factor (0,0.05).T to E: target g=(1,-1) now has R=0.05.
- Make E a two-column rank-one matrix; the same R=0 holds.
- E shape (2,0) represents ideal noiseless recording; full H=I removes all uncertainty for a linear goal.
- Legacy full-rank correlated-noise, elliptical prior, no-observation and independent-measurement fixtures remain in the test suite.

This feature was developed with a failing-test-first record (old model rejected valid E), then corrected the older test that still expected such rejection; 13 focused tests and 350 seeded heterogeneous random matrix diagnostics were executed locally. **GitHub Actions run** [38178623705](https://github.com/Gogoal-L/math/actions/runs/38178623705) after source+test update ran all 128 current branch tests and passed. Conditional mathematical validity and floating arithmetic are separate from a physically qualified SiC instrument.

**Critical numerical/scientific qualification.** This computation branches on floating SVD thresholds. If a tiny *nonzero* unshared noise mode is truncated, it can spuriously label a noisy contrast exact and understate physical risk. Noise covariance alone is neither an absolute error ball nor a certificate that a small singular value is zero. Set and justify signal units, correlation drift, common gain/offset/skew origin, acquisition timing, and a reliable bound on all unshared components. In particular, the ideal R=0 in the synthetic rank-one model is **not** a prediction of 0-V or 0-nJ physical uncertainty in an actual DPT waveform. Nonlinear remainder and legally reachable ellipsoid still require separate certificates.

**Closest original mathematical foundation:** Foucart--Liao (2024) remains the general optimal-recovery prior. This is a structured reduction for singular sensor uncertainty, not a claimed new theorem. The F119/F129/F132 deep proof audit and three-mechanism DPT test are maintained on main at [20261011_F119_F129_F132_proof_level_DPT_bridge.md](../dpt_research/20261011_F119_F129_F132_proof_level_DPT_bridge.md).
