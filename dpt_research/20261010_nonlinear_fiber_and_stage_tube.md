# DPT-R1 mathematical frontier IV: nonlinear goal fibers and finite-stage admissible tubes

**Date:** 2026-10-10. **Authority:** independent mathematical research; no native SiC validation, no S09/S10 budget or owner decision. **Upstream OpenAI Math identity:** [`fd4aeeb2`](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb). The preceding [all-word + solver-fidelity note](20261010_goal_information_solver_fidelity.md) and [ordered goal-error note](20261010_ordered_goal_defect_transport.md) remain valid within their stated model classes.

## 1. Domain brief: what is now missing?

The MAP records: actual-law prospective 150/600 V command predictions; a qualified local Eth consistent chart with moving-event derivative; source-based K/Q and two-command summary tests; the larger-radius failure of the one-row fixed-Q summary; a well-performing one-Newton competitor. The earlier executable bridge covers *linear* all-word observability, *linear* ordered error transport and a *conditional* smooth implicit-solver bound. Two distinct mathematical gaps remain:

1. **Curved observation fiber:** even when `DG = B DO` and the *tangent* goal-visible hidden dimension is zero, can two admissible histories with exactly the same retained observation have different next-command goals at order `r^2`?
2. **Verified stage domain:** does a qualified Eth tangent and a list of successful trajectories suffice to carry an entire declared preparation neighborhood through subsequent guards/branches? It does not by itself. Can a small but mathematically genuine finite-stage enclosure be constructed?

**Evidence ledger.** Source-backed: the current MAP reports the above *model-level accepted evidence*; F049/F149/F360 and classical nonlinear-observability/DAE results state their own mathematical theorems. Inference: these proof structures suggest concrete tests on DPT `O,G,Eth` and stage intervals. Unknown: actual `D2O,D2G`, physical reachable-fiber tangent, certified BE remainder/guard tubes and real DPT finite-radius sharpness. These unknowns must be supplied by the local controller rather than invented here.

## 2. Independent proposition A: second-order goal leakage on an observation fiber

Let `U` be an open neighborhood of a physically admissible **history-coordinate** `x0` in `R^n`. Let `O:U -> R^m` and scalar `G:U -> R` be `C^2`, with `1 <= m < n`, and assume `DO(x0)` has full row rank. Here `G` is the *fixed future command and goal*, not an arbitrary post-target readout. Suppose additionally that the first-order factorization **is exact**:

\[
DG(x_0)=b\,DO(x_0),\qquad b\in\mathbb R^{1\times m}.
\]

Let `K=ker DO(x0)` and define the *observation-fiber goal Hessian* (quadratic form on `K`):

\[
\boxed{Q_{G\mid O}(v)=v^T\left[D^2G(x_0)-\sum_{i=1}^{m}b_iD^2O_i(x_0)\right]v,\qquad v\in K.}
\]

**Claim (elementary local implicit-function consequence).** For any unit `v` in `K`, there is a local `C^2` curve `x(t)` through `x0` such that `O(x(t))=O(x0)`, `x'(0)=v`, and

\[
G(x(t))-G(x_0)=\frac12 Q_{G\mid O}(v)t^2+o(t^2).
\]

If `Q(v) != 0`, no exact predictor depending only on the retained `O` can be correct for both `x0` and `x(t)`: the two-point minimax scalar error is at least `|Q(v)|t^2/4+o(t^2)`. Under the *Euclidean metric of the declared scaled history chart*, the greatest absolute second-order coefficient is

\[
\frac12\rho\bigl(K^T[D^2G-\sum_i b_iD^2O_i]K\bigr),
\]

where columns of `K` form an orthonormal nullspace basis and `rho` means **maximum absolute eigenvalue**, not the stage-state radius. This is an *asymptotic coefficient*, **not** an unconditional finite-radius error bound. It does not prove the new variable needed for repair is minimal or an external sensor.

**Proof.** The constant-rank (submersion) theorem gives a local observation-level manifold. Pick its curve with prescribed tangent `v`. Twice differentiating `O(x(t))=O(x0)` gives `DO x''(0)+D2O[v,v]=0`. By exact factorization, `DG x''(0)=-b D2O[v,v]`. Twice differentiating the scalar goal yields exactly `Q(v)`. The Taylor expansion and two-point indistinguishability bound follow. Maximizing `|v^T M v|` on the unit sphere in `K` gives the spectral radius of the symmetric restriction `M` by the Rayleigh quotient. QED.

**Constructive tests.** (a) `O(x,y)=x`, `G(x,y)=x+y^2`: at `(0,0)` the first-order nullspace audit passes, yet the equal-observation histories `(0,0)` and `(0,t)` differ by `t^2` in goal. (b) `O(x,y)=x+y^2`, `G=x`: exact fiber `(-t^2,t)`, target difference `-t^2`. (c) `G=O` has zero curvature; (d) `G=x+y^3` also has zero *quadratic* curvature but is *not* sufficient—higher order cannot be dismissed. (e) `G=x+10^-9 y+y^2` fails exact first-order factorization even if a loose numerical tolerance would accept it; its linear leakage dominates for sufficiently small `t`.

**Executable:** [fiber_curvature_audit.py](../dpt_tools/fiber_curvature_audit.py) accepts `DO,DG,D2O,D2G`, verifies declared first-order factorization at a numerical tolerance and differentiability data consistency, returns the maximal hidden curvature and a tangent/second-derivative witness satisfying the level-set constraints. `QUADRATIC_WITNESS` is a **conditional mathematical candidate** dependent on exact identities, not a native DPT claim. `NEAR_FIRST_ORDER_FACTOR` prevents a small residual from masquerading as genuine second-order leakage. Full-row-rank/underflow failure refuses the submersion theorem. Mathematically nonzero curvature smaller than an absolute reporting tolerance may be classified as below threshold; that is no proof of its absence.

**Why DPT cares:** the fixed Q second row becoming important at larger preparation radii could come from `Q_{G|O}` along source-reachable directions; the alternative is a *different command-horizon tangent direction* (earlier `goal_word_quotient.py`), an event branch change, or merely increased numerical error. Distinguish them on the same source/command/goal with native-approved data. In particular the physical reachable preparation set may be a lower-dimensional submanifold. Compute derivatives **in a valid chart of that set** rather than using arbitrary 28-coordinate displacements.

## 3. Independent proposition B: finite-stage box inclusion with certified envelopes as inputs

Let `B_k=[l_k,u_k]` be stage-valid state boxes in one common physical/scaled chart. For one frozen command sequence suppose **throughout** `B_k` the actual state map admits

\[
x_{k+1}=A_kx_k+b_k+r_k(x_k),\qquad |r_{k,i}(x_k)|\le \epsilon_{k,i}.
\]

For any input box `[p,q] subset B_k`, define the interval image by coordinates

\[
L_{k,i}=b_{k,i}+\sum_j\min(A_{k,ij}p_j,A_{k,ij}q_j)-\epsilon_{k,i},
\quad U_{k,i}=b_{k,i}+\sum_j\max(A_{k,ij}p_j,A_{k,ij}q_j)+\epsilon_{k,i}.
\]

**Finite-stage conditional inclusion theorem.** If the initial uncertainty box lies in `B0` and at each step `[L_k,U_k] subset B_{k+1}`, then every physically admissible trajectory satisfying these particular map/remainder contracts remains within the declared stage-valid boxes throughout the specified command sequence. Proof is induction using the exact affine coordinatewise extrema of a box and the separately justified remainder bounds. This is **not** F149 permanence, a uniform infinite-time invariant region, or a complete nonlinear SiC certificate.

**Why a failed check is not a counterexample:** after a stage, a box hull discards correlations. Example `x -> (x_1,x_1)` followed by `z=x_1-x_2` gives true `z=0` but interval hull allows `[-1,1]`. Failure says *the conservative certificate cannot qualify that domain*; it does not prove the physical state escaped.

**Executable:** [stage_box_reachability.py](../dpt_tools/stage_box_reachability.py) accepts ordered affine maps, offsets, initial bounds, stage-valid boxes and **externally certified** componentwise remainder radii. It returns the propagated hull, validated prefix length, first unqualified stage, and the smallest numerical margin to a guard (with a roundoff-level warning). Its `CONDITIONAL_AFFINE_BOX_CHAIN` status means **the exact-algebra containment conditions are met numerically under the supplied contracts**, not that floating-point calculations are verified outward-rounded interval arithmetic. A numerically marginal result requires outward interval evaluation before formal certification. No native evidence is claimed.

**Natural next DPT evidence:** from Sol9 Eth implicit lift, obtain a valid local coordinate continuation; on one frozen preparation tube, derive actual finite-range `A,b` and interval/remainder/guard bounds from the coupled BE equations rather than a single point Jacobian. If the interval hull fails, first preserve physical constraints using a polytope or zonotope before asking for new LTspice; do not react by choosing arbitrary larger boxes.

## 4. Additional OpenAI Math deep reads and proof transfers

All OpenAI links below are pinned to `fd4aeeb2` and the papers are treated as preprints; selected Lean formalization scopes are recorded individually, not promoted to DPT.

| Family, primary manuscript and exact result | Useful proof idea / challenge | What would make it load-bearing in DPT? |
|---|---|---|
| **F049** [stable coordinate counterexample](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-stable-coordinate-that-is-not-a-coordinate-in-four-variables-October-5-2026/build/source/sections/01-introduction.tex), [explicit stabilization construction](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-stable-coordinate-that-is-not-a-coordinate-in-four-variables-October-5-2026/build/source/sections/02-construction.tex) | Exhibits a complex polynomial that becomes a coordinate after adding an auxiliary variable but is not one in the original four variables; even affine-space fibers need not be ambiently straightenable. | Evidence that the proposed Eth/storage representation has a legal *physical* near-identity lift, rather than naming an augmented numerical chart a globally valid physical state. Algebraic counterexample is **not** a counterexample to actual DPT. [Lean selected scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/049.md) includes its explicit four-variable polynomial. |
| **F149** [finite affine trapping proof](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Uniform-Permanence-in-Weakly-Reversible-Mass-Action-Systems-October-5-2026/build/sections/trapping.tex) | Uses finitely many affine barriers/plateaux, sign comparisons and monotonicity to establish trapping and eventual entry in weakly reversible mass-action networks. | Motivates a *different elementary* affine interval-box containment pilot in switching dynamics; F149 network theorems cannot certify it. Its [selected Lean scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/149.md) covers the earlier persistence result, not automatically every stronger October assertion. |
| **F360** [weak-MTW to convex tangent injectivity domains](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Global-Support-and-Convex-Injectivity-Domains-under-Weak-MTW-September-25-2026/build/sections/introduction.tex) | Proves *specific* transverse cost curvature conditions imply global convexity on a Riemannian manifold; strong global inference requires a verified hypothesis, not scattered local tangents. | Suggests asking whether any actual DPT finite-radius valid domain has proven convex/monotonic geometry. Without an analogous condition, use conservative explicit guard boxes instead. [Lean scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/360.md) covers the specified convex-injectivity result. |
| **F334** [smooth metric without a local isometric immersion](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Smooth-Metric-with-No-Local-Isometric-Immersion-into-Three-Space-September-24-2026/build/main.tex) | A smooth metric can have the same *full* Taylor jet as Euclidean at a point and yet fail local smooth realization into 3D. | A sharp analogy for refusing to turn an Eth pointwise Taylor audit into a neighborhood representation without a continuation theorem. The result is about geometry, not DPT circuit states. |
| **F093** [log-Sobolev from subgaussian linear marginals](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-dimension-free-logarithmic-Sobolev-inequality-for-subgaussian-log-concave-measures-September-23-2026/build/sections/01-introduction.tex) | Dimension-free concentration requires a centered **log-concave distribution with all linear marginals subgaussian** as defined in the theorem. | An eventual stochastic noise-certified companion to deterministic radius analysis *only if* the preparation/noise distribution is measured and those hypotheses validated. Not used as an error bar now. No `lean/docs/093.md` was located at the inspected commit. |
| **F377** [infinity-harmonic interior C1-alpha regularity](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Uniform-Interior-C1alpha-Estimates-for-Infinity-Harmonic-Functions-October-4-2026/build/manuscript/sections/01-introduction.tex) | Provides `C^{1,alpha}` for **bounded infinity-harmonic functions**, not generic nonlinear maps. | Reminder that second derivatives must be explicitly available; generic `C1`/Holder systems do not license the Hessian test. WATCH until a valid differentiability model exists. No `lean/docs/377.md` found in this inspection. |

### Source-audit and closest-prior subtraction

The OpenAI papers do **not** prove our two mathematical propositions. The fiber argument is classical submersion/implicit-function differential geometry and nonlinear observability; compare [Hermann–Krener 1977](https://doi.org/10.1109/TAC.1977.1101601). Stage box inclusion is elementary robust set propagation; compare [Della Rossa–Egidio–Jungers 2023](https://doi.org/10.1137/22M1482226) and [Cinto et al. 2025](https://doi.org/10.1137/24M1715520), which address harder switched-affine stability/controlled invariance questions. [Trenn 2012](https://doi.org/10.1007/978-1-4471-2885-4_6) describes mode consistency projection for linear switched DAEs. Our proposed DPT contribution is the verified **application and diagnostic role of the specific nonlinear observation-fiber curvature and stage-reachable tubes** using actual preparation and hybrid circuit equations. It is not novelty merely to name a Hessian or a box.

## 5. Short roundtable stress test (simulated, sourced positions; NOT real quotations)

**Moderator's question:** Under the current S09 resource limit, is it more valuable to add an internal state, refine the full solver, or prove a range where the existing reduced state already works?

**Hermann–Krener lens (nonlinear observability; 1977, inference applied to DPT):** The lack of a goal-visible direction in a first-order matrix is a *local rank observation*, not a whole nonlinear input-output equivalence. Ask whether a curved observation fiber gives distinct future outputs for the same summary. The precise derivative and future command matter. [Source](https://doi.org/10.1109/TAC.1977.1101601).

**Trenn lens (switched-DAE mode consistency; 2012, inference applied to DPT):** Before interpreting a hidden direction as a physical mode, establish which variables are algebraic after Eth, which storage is continuous, and whether an implicit stage update is uniquely defined. A tangent in a forbidden or inconsistent DAE chart is not an admissible history. [Source](https://doi.org/10.1007/978-1-4471-2885-4_6).

**Krause lens (robust observation selection; 2008, inference applied to DPT):** Even a mathematically decisive witness is not automatically an economical sensor. Evaluate available readouts, shared prefix, acquisition costs and robustness across multiple actual goals; greedy selection guarantees require the assumptions of the chosen information objective. [Source](https://www.jmlr.org/papers/v9/krause08b.html).

**Round 1 crux:** *Rank deficiency or radius leakage* cannot be diagnosed before defining the legitimate physically reachable fiber. A no-extra-simulation check is: take the same native-qualified Eth/source chart and construct a candidate observation-equal perturbation. The second-order result is meaningful only when this perturbation remains admissible.

**Round 2 crux:** A physically admissible *point* is not a verified *domain*. The affine-box pilot supplies a conservative failure locator; if interval overapproximation fails because of correlated charge constraints, the next mathematics should be a polytope or manifold chart, not a larger solver budget.

```text
valid preparation chart + guard/DAE identities
               |
           JO, DG, Hessians ------> curved-fiber goal witness (lower information boundary)
               |
        qualified stage maps ------> finite-stage box containment (upper domain boundary)
               |                               |
      combined source-specific forecast / repair choice (controller only)
```

**Moderator synthesis:** The strongest two alternative hypotheses are (H1) a genuinely missing, goal-visible preparation direction and (H2) an incorrect/nonuniform stage chart or unqualified approximation region. The two audits discriminate them better than another generic fit refinement. They do not imply that one hypothesis is universally true, and no actual scientist is claimed to have spoken about this SiC project.

## 6. Controller replay gate and rejection outcomes

1. **Same physical source/branch:** obtain valid preparation-parameter coordinates, recorded fixed commands/goals, and complete `O/G` derivative mapping; exclude future outcome data from prediction inputs.
2. **Curvature attack:** run `fiber_curvature_audit.py` on physically reachable chart derivatives. Compare its predicted hidden tangent with archived finite perturbation/goal contrasts; explicitly test first-order leakage and event-branch conditions. If the Hessians are unavailable or charts nonsmooth, record the missing math contract, not an inferred result.
3. **Finite-stage tube attack:** on a *frozen* valid prefix and command sequence, derive `A_k,b_k`, stage boxes, all-coordinate true residual envelopes and guard domains from actual BE storage/constraint law. Run `stage_box_reachability.py`. If the box fails due to correlation, test an exact constrained reachable set/polytope rather than reclassifying native evidence as invalid.
4. **Decision fork:** a nonzero qualified curvature suggests a **local information repair** candidate. A valid small box and certified small solver residual suggest a **cheaper model/solver** regime. Both failing suggests domain/representation needs repair before any new acquisition. Include full/affine/one-Newton ordinary rivals and the current 600 V path qualification.
5. **Formal acceptance:** no automatic modification of S09 freeze, native model claim, extra LTspice, or active owner lane. The local controller decides which math deltas are scientifically material.

**Evidence status:** analytical theorem(s) independently reconstructed; original OpenAI sources read at theorem/proof-architecture level; 23 synthetic/analytic tests including randomized vertex cross-check, numerical margin guard and CLI/compile checks passed locally; actual DPT source Hessians and stage-valid remainder boxes remain unknown. These tools are reusable mathematical probes and **not** native validations.
