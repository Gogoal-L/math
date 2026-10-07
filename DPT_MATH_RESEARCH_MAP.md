# DPT Math Research Map

**Purpose.** This is a living, fork-specific research ledger for using `Gogoal-L/math` in DPT-R1 / Pro17D and later power-semiconductor work. It records which OpenAI Math families have actually been inspected, what part of each manuscript is useful, what can and cannot be transferred, and what concrete DPT theorem, analysis, or acquisition it motivates.

**Baseline revision reviewed:** `adc7f1241b42e322a6451854ab7e4b4c146bf78a`  
**Initial DPT mapping date:** 2026-10-07

The upstream release contains hundreds of manuscripts and explicitly notes that verification/formalization coverage varies. A manuscript in this repository is therefore a source of mathematical ideas and candidate proof architectures, not an automatic authority for a DPT claim. See the original [README](README.md), [CONTENTS](CONTENTS.md), [overview](overview.pdf), and the [Lean formalization catalogue](lean/formalization.yaml).

## 1. Reading-status convention

This map distinguishes reading depth from scientific transfer status.

| Tag | Meaning |
|---|---|
| **D3 - deep source read** | The manuscript source/derivation sections relevant to DPT were read, including theorem assumptions and proof mechanism. |
| **D2 - structural read** | Formalization scope, introduction, or decisive sections were read; enough to bound the possible transfer. |
| **D1 - catalogue read** | The family was screened from `overview.tex` / README and retained only as a possible later source. |
| **T0 - no transfer** | Interesting mathematics, but no current DPT use. |
| **T1 - analogy/watchlist** | Useful conceptual warning or future direction only. |
| **T2 - proof architecture** | A proof/design pattern can be adapted after a new DPT derivation. |
| **T3 - active DPT construction** | The source already changes a current DPT theorem, experiment, or certificate plan. |

**PDF note.** The repository PDF bytes are the canonical rendered manuscripts. In the current connected runtime, binary PDF rendering was not reliably available, so the present pass used the exact manuscript build/source TeX plus Lean scope files. No claim is made here that every PDF figure/layout was visually inspected. Where figures or page layout become scientifically material, add a separate visual-PDF pass and record it below.

## 2. Current DPT scientific object

The most promising unifying object is not a generic waveform predictor. It is a **goal-dependent finite predictive representation** for switching histories.

Let

- (mathcal H): admissible preparation/history states;
- (mathcal C): future command family;
- (O:mathcal H	omathcal Y): available observation map;
- (G_c:mathcal H	omathbb R^p): goal under future command (c).

Define goal equivalence

[
h_1sim_G h_2
quadLongleftrightarrowquad
G_c(h_1)=G_c(h_2);;	ext{for every }cinmathcal C.
]

The DPT question is then:

> What is the smallest information-bearing coordinate that is sufficient for the declared future goals, how can it be updated under commands, and what new measurement is minimally required when the current observation collapses goal-distinct histories?

Pro17D already contains an exact reduced-law example of this distinction: the same one-dimensional gate coordinate is sufficient for the declared increment/zero-sum goals, while an absolute drain goal requires an additional drain/charge anchor in that law class. Full-native observation-fiber sufficiency remains open.

This map uses the OpenAI Math repository to push that object in six directions:

1. information lower bounds;
2. minimal measurement repair;
3. noncommutative command representation;
4. identifiability and regularity boundaries;
5. approximate algebra/stability;
6. certificate-grade computation.

## 3. Ranked family map

| Priority | Family | Read / transfer | DPT value |
|---|---|---|---|
| **S+** | **F140 - Memory-sample lower bounds** | D3 / T3 | Turns “small sufficient state” into an information-budget question and suggests lower bounds on predictive representation size. |
| **S+** | **F355 - Tangent-flow uniqueness** | D3 / T3 | Gives a concrete kernel-killing observation architecture for deriving the minimum number of extra measurements. |
| **S** | **F116 - Noncommutative identity testing** | D3 / T3 | Ordered iterated-integral encoding can organize command order, mixed words, and higher interaction terms. Multiplicity machinery is already used in Pro17D. |
| **S** | **F365 + F372 - inverse uniqueness / nonuniqueness** | D2-D3 / T3 | Provides the right claim grammar: identifiability depends on model class, observation operator, regularity, goal, and symmetry; uniqueness is not finite sufficiency or stable reconstruction. |
| **A** | **F251 - Strong Ulam stability** | D2 / T2 | Defines the right future question for native “almost command algebra”: when does small composition defect imply proximity to a true reusable representation? |
| **A** | **F266 - certified computation** | D3 / T3 | Supplies a disciplined certificate architecture separating candidate generation, exact verification, arithmetic assumptions, provenance, bounded failure handling, and terminal acceptance. |
| **B** | **F139 - query complexity** | D2 / T2 | Useful for defining characterization-query budget and upper/lower query complexity, not a direct DPT theorem. |
| **B** | **F289 - Kadison-Kastler stability** | D2 / T1-T2 | Strong warning that structural stability needs a symmetric metric and an explicit nearby-structure theorem; one-sided closeness is not enough. |
| **B** | **F325 - complete Crouzeix** | D2 / T1-T2 | Potential operator-norm control for polynomial/rational functions of future nonnormal reduced propagators. Not load-bearing yet. |
| **C** | **F357, F374, F098, F119, F229** | D1-D2 / T1 | Stable-coordinate, stability-exponent, finite-embedding, information-contraction, and reconstruction-threshold analogies. Keep as a watchlist, not current proof support. |

## 4. F140 - information lower bounds and observation fibers

**Files inspected**

- [Lean scope](lean/docs/140.md)
- [Replacing Gaussian observations - PDF](preprints/Replacing-Gaussian-observations-in-memory-constrained-inference-September-27-2026/paper.pdf)
- [Introduction source](preprints/Replacing-Gaussian-observations-in-memory-constrained-inference-September-27-2026/build/sections/00-introduction.tex)
- [Finite Gaussian-fiber comparison source](preprints/Replacing-Gaussian-observations-in-memory-constrained-inference-September-27-2026/build/sections/06-fiber.tex)

### What the family actually contributes

The family studies exact Gaussian observations under a finite persistent state. Its formalized results include memory-sample lower bounds, conditional-information comparisons, exact observation fibers, and two-point/fiber-block estimates. In the observation-replacement manuscript, conditioning on a finite message changes the law of the rows that produced that message; the proof compares those actual rows with fresh projections and explicitly accounts for the information cost.

### DPT transfer

The Gaussian model itself does **not** transfer. The transferable object is the separation of:

- physical observation history;
- retained finite state;
- the observation fiber left unresolved by that state;
- information required to distinguish goal-relevant points on that fiber.

Define a DPT goal pseudometric

[
d_G(h_1,h_2)=sup_{cinmathcal C}
|G_c(h_1)-G_c(h_2)|.
]

For an (M)-bit representation that must predict every (G_c) with uniform error at most (arepsilon), any subset of histories separated by more than (2arepsilon) in (d_G) must receive distinct codes. This suggests the elementary lower bound

[
Mge
log_2 mathcal P(mathcal H,d_G,2arepsilon),
]

where (mathcal P) is an appropriate packing number.

**Status:** this is a **candidate DPT theorem / bound to formulate precisely**, not a theorem imported from F140. F140 is the methodological precedent for taking the observation fiber and finite retained information seriously.

### Why this matters for the paper

It would give both sides of a representation-complexity story:

- **upper bound:** a constructive finite sufficient state, such as the exact reduced-law gate quotient already obtained;
- **lower bound:** a proof that fewer distinguishable states cannot uniformly support the declared future goals.

That is stronger than merely saying the representation is “small.”

### Next concrete work

1. Specify the admissible history set and future-command set actually claimed in DPT-R1.
2. Define (d_G) for scalar terminal goals first.
3. Compute/construct goal-distinct packings in the reduced law and in any executable native preparation family.
4. Only then consider noisy or probabilistic analogues.

## 5. F355 - kernel-killing observations and goal-visible nullity

**Files inspected**

- [Tangent-flow manuscript - PDF](preprints/Tangent-flow-uniqueness-2026-09-24/paper.pdf)
- [Normalized family / compact observations](preprints/Tangent-flow-uniqueness-2026-09-24/build/sections/linear.tex)
- [Finite-jet obstruction](preprints/Tangent-flow-uniqueness-2026-09-24/build/sections/finite-jet.tex)

### What is useful

The `Symmetric enlargement` lemma in `linear.tex` starts from a linearized operator (L) with finite-dimensional kernel (K). It chooses finitely many compact observations whose pairing with a basis of (K) is nonsingular, making the augmented operator

[
(u,lambda)mapsto(Lu+P^*lambda,Pu)
]

invertible. The proof explicitly separates the invisible kernel component from the invertible complement and then enlarges the observation list to control additional finite directions.

The later finite-jet argument is also methodologically useful: absence of a formal critical arc is converted into a finite analytic inequality, with the obstruction exponent fixed before the finite truncation order.

### DPT transfer: goal-visible hidden dimension

At a reference history (h_*), define

[
K=ker DO(h_*),
]

the tangent directions invisible to current measurements. Then define

[
N=
Kcap
igcap_{cinmathcal C}
ker DG_c(h_*),
]

the invisible directions that are also irrelevant to every declared future goal.

The quotient

[
oxed{
r_G=dim(K/N)
}
]

is a natural **goal-visible hidden dimension**.

For (k) added scalar measurements (P=(P_1,ldots,P_k)), first-order goal sufficiency requires at minimum

[
ker(DP|_K)subseteq N.
]

By a dimension argument,

[
kge r_G.
]

If (r_G) carefully chosen measurements are injective on (K/N), then under appropriate constant-rank / local-coordinate assumptions they are candidates for a locally sufficient repair.

**Status:** this is a DPT theorem to prove in its own setting. F355 supplies the proof architecture, not the result.

### Exact connection to the current reduced-law result

The existing drain-translation direction is invisible to the gate observation.

- For the increment/zero-sum goal, that direction is also goal-null. It lies in (N), so no repair is needed.
- For the absolute drain goal, the same direction is goal-visible. It survives in (K/N), producing a one-dimensional deficiency and explaining why one independent drain/charge anchor is both sufficient and necessary in the declared law class.

This is a particularly strong route because it turns a model-specific one-scalar repair into a worked example of a general local measurement theorem.

### Next concrete work

1. Write the finite-dimensional tangent theorem cleanly, independent of the particular DPT equations.
2. Verify constant-rank assumptions for the reduced model.
3. Express candidate native preparation directions and compute a numerical (DO) / (DG_c) rank test only after an executable native preparation interface exists.
4. Use the quotient (K/N), not raw state dimension, to rank future sensors.

## 6. F116 - ordered command words, iterated integrals, and bounded detection

**Files inspected**

- [Lean scope](lean/docs/116.md)
- [One Rational Matrix Hitting Point - PDF](preprints/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026.pdf)
- [Introduction / proof route](preprints/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026/build/introduction.tex)
- [Faithful iterated-integral encoding](preprints/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026/build/iterated-integrals.tex)
- [Multiplicity estimate](preprints/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026/build/multiplicity.tex)

### What the paper actually proves

For bounded-size division-free noncommutative formulas, the manuscript constructs a universal rational matrix tuple that detects every nonzero formula. Its proof has two parts particularly relevant to DPT:

1. ordered words are faithfully encoded by iterated integrals
   [
   h_{iw}(z)=int_0^zrac{h_w(t)}{t+i},dt;
   ]
2. a rational differential-system multiplicity estimate bounds how many Taylor coefficients can vanish before a nonzero scalar component is detected.

The source explicitly shows that word order survives the encoding; e.g. the commutator (x_1x_2-x_2x_1) maps to a nonzero series even though cancellation delays its first nonzero coefficient.

### DPT transfer

The most useful new transfer is **not** another multiplicity claim. Pro17D has already used the rational differential-system/multiplicity side. The higher-value object is a graded ordered-command signature.

For primitive commands (A,B,ldots), organize response information by word degree:

- degree 0: prepared baseline;
- degree 1: primitive response (A,B,ldots);
- degree 2: (AA,BB,AB,BA,ldots);
- higher degree: longer ordered command words.

This fits the existing empirical fact that equal aggregate command area does not imply equal terminal response when the order changes. It also gives a principled way to distinguish:

- axis characterization;
- mixed simultaneous interaction;
- ordered sequential interaction;
- higher-order memory.

### Connection to S09 fusion

The current prospective fusion query is naturally interpreted as the first acquisition of a coefficient not fixed by the primitive axes. In the declared quadratic class

[
F(alpha,eta)
=
F_0+alpha L_A+eta L_B
+alpha^2D_A+eta^2D_B
+alphaeta C_{AB},
]

the axis measurements do not determine (C_{AB}). One mixed point with (alphaeta
eq0) identifies this scalar coefficient in that exact class.

This is stronger experimental logic than “try another pulse amplitude”: the query purchases the first missing mixed functional.

### Prior-art boundary

Iterated-integral / word representations of nonlinear input-output systems have a substantial Chen-Fliess and nonlinear realization literature. Before any novelty claim, perform a closest-prior subtraction against that literature. The DPT novelty, if any, should come from the exact device-physics object, goal-dependent information budget, bounded characterization, or prospective falsification - not from claiming noncommutative word expansions themselves are new.

### Next concrete work

1. Build a DPT command-word notation that separates simultaneous mixed terms from sequential (AB) vs (BA).
2. Derive the lowest-order word coefficients for the reduced law where possible.
3. Decide whether optional S10 should target an ordered interaction that S09 cannot resolve.
4. Read `formula-systems.tex` and `construction.tex` only if a finite universal detection argument becomes necessary.

## 7. F365 + F372 - identifiability is conditional on class, data, and symmetry

**Files inspected**

- [F365 Lean scope](lean/docs/365.md)
- [Joint metric/connection recovery - PDF](preprints/Determination-of-a-metric-and-a-unitary-connection-from-one-boundary-patch-October-5-2026/paper.pdf)
- [Joint recovery introduction](preprints/Determination-of-a-metric-and-a-unitary-connection-from-one-boundary-patch-October-5-2026/build/sections/01-introduction.tex)
- [F372 Lean scope](lean/docs/372.md)
- [Smooth isotropic elasticity - PDF](preprints/Global-Uniqueness-for-the-Smooth-Isotropic-Elasticity-Inverse-Problem-September-24-2026/article.pdf)
- [Coefficient recovery](preprints/Global-Uniqueness-for-the-Smooth-Isotropic-Elasticity-Inverse-Problem-September-24-2026/build/sections/coefficient-recovery.tex)

### Core lesson

The same broad inverse-problem family exhibits both strong uniqueness and nonuniqueness depending on regularity/model class. The positive joint-recovery result is also only unique up to intrinsic diffeomorphism/gauge. F372 proves uniqueness from the **full** displacement-to-traction operator and explicitly does not provide a reconstruction algorithm.

The correct DPT grammar is therefore:

[
	ext{identifiability}
=
(	ext{model class},
	ext{observation operator},
	ext{goal},
	ext{allowed symmetry}).
]

Do not ask “is the device identifiable?” without all four qualifiers.

### Three distinctions to preserve

[
oxed{
	ext{uniqueness}

eq
	ext{finite sufficiency}

eq
	ext{stable reconstruction}
}
]

A full response operator may determine a coefficient uniquely while a finite experiment bank does not. A finite set may be locally sufficient but poorly conditioned. A reduced structured class may be identifiable while a broader native class is not.

### DPT use

This directly supports the current claim boundary:

- exact one-coordinate sufficiency is a theorem only inside the declared reduced law/goal class;
- one extra scalar is a minimal repair only for that declared absolute-goal class;
- full-vendor native finite sufficiency remains open;
- adding unknown nonlinear charge surfaces, thermal/diode state, or additional parasitic modes changes the unknown class and therefore changes the identifiability question.

## 8. F251 - approximate command algebra as a future theorem

**Files inspected**

- [Strong Ulam Stability - PDF](preprints/Strong-Ulam-Stability-Characterizes-Amenability-October-5-2026/strong-ulam-stability.pdf)
- [Source](preprints/Strong-Ulam-Stability-Characterizes-Amenability-October-5-2026/build/strong-ulam-stability.tex)

The manuscript defines the multiplicative defect of a normalized unitary map

[
operatorname{def}(mu)
=
sup_{g,h}
|mu(gh)-mu(g)mu(h)|
]

and asks when small defect guarantees proximity to a genuine representation. Its theorem is specifically about countable groups and unitary representations; those assumptions do not match a causal, generally noninvertible/nonunitary DPT command semigroup.

### DPT research question

For an estimated native command map (widehat R), define

[
delta_{m comp}
=
sup_{c_1,c_2}
|
widehat R(c_2circ c_1)
-
widehat R(c_2)widehat R(c_1)
|.
]

The future theorem would ask:

> Under which DPT-relevant command-semigroup, norm, domain, and regularity assumptions does small (delta_{m comp}) imply the existence of a nearby exact finite reusable command representation?

This is potentially important for deployment because native SPICE or hardware will not satisfy the reduced algebra exactly.

**Status:** T2 only. Do not cite F251 as proving stability of DPT command maps.

## 9. F266 - certificate architecture for a computation-backed DPT theorem

**Files inspected**

- [Lean scope](lean/docs/266.md)
- [Exact Fourier certificates - PDF](preprints/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026.pdf)
- [Exact verification section](preprints/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026/build/sections/05-verification.tex)
- [Maximum MUB execution contract](preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/build/sections/execution.tex)

### Most useful methodological details

1. **Candidate generation is not proof.** Modular elimination or numerical search may locate pivots/substitutions, but exact integer/rational checks establish the certificate.
2. **Formalization scope must be stated literally.** The Lean scope file explicitly says the selected formalization is weaker than the paper's headline (N(6)=3) computation.
3. **Execution provenance is part of the claim.** The computer-assisted result records source hashes, compiler/platform, arithmetic assumptions, control flow, record formats, terminal conditions, and output hashes.
4. **Resource caps fail conservatively.** A cap or unresolved region is retained for fallback; it is never silently interpreted as nonexistence.
5. **Finite execution and mathematical lemmas are separate evidence layers.** Hash/count agreement proves execution identity/completeness, not the analytic inequalities by itself.

### DPT certificate stack

Use four layers:

**C1 - exact algebraic certificate**
- rank/determinant identities where rationalization is legitimate;
- command-matrix composition identities;
- finite linear elimination identities;
- symbolic coefficient relations.

**C2 - one-sided numerical certificate**
- interval or directed-rounding root enclosures;
- saturation/domain margins;
- monotonicity and denominator-separation bounds;
- remainder envelopes when assumptions permit.

**C3 - simulator provenance**
- exact model/library hash;
- LTspice version/operator;
- netlist/configuration hash;
- run commands;
- waveform/CSV hashes;
- scorer version;
- no post-outcome parameter changes.

**C4 - empirical/native validation**
- fresh prospective outcomes;
- convergence/refinement checks;
- hardware data if later available.

This would be a substantial improvement over reporting only machine-precision coherence.

## 10. F139 - characterization query complexity

**Files inspected**

- [PDF](preprints/Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026/article.pdf)
- [Main source](preprints/Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026/build/main.tex)
- [Introduction](preprints/Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026/build/sections/introduction.tex)
- [Lower bound](preprints/Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026/build/sections/lower.tex)

The important methodological feature is the explicit **oracle model**: computation between queries is unrestricted, only information acquired from the unknown object is charged. The paper proves both an upper and lower query bound under a tightly specified object class.

### DPT use

This suggests defining a DPT characterization oracle and separating:

- expensive simulator/hardware acquisitions;
- free offline algebra/computation;
- the model class guaranteed by those acquisitions;
- worst-case vs expected acquisition count;
- accuracy/goal tolerance.

This could eventually make statements such as “four fresh characterization calls are sufficient for this declared class” scientifically sharper.

It does **not** imply a subpolynomial DPT query bound and should not be used as such.

## 11. F289 - structural stability requires the right distance

**Files inspected**

- [PDF](preprints/Universal-strong-Kadison-Kastler-stability-September-23-2026/paper.pdf)
- [Introduction](preprints/Universal-strong-Kadison-Kastler-stability-September-23-2026/build/sections/01-introduction.tex)

The Kadison-Kastler metric is explicitly symmetric: each unit ball must lie near the other. The manuscript's introduction also distinguishes ordinary gap, matrix-level control, spatial implementation, and one-sided near inclusion.

### DPT use

Treat this as a warning for future native-algebra claims:

- closeness of one observed waveform family to a reduced prediction is not the same as structural closeness of two command algebras;
- one-sided fitting error is weaker than a symmetric distance between attainable response sets;
- a stability theorem needs an explicit metric and an explicit nearby exact object.

This family currently supplies claim discipline, not a DPT proof.

## 12. F325 - nonnormal operator control, retained for later

**Files inspected**

- [Lean scope](lean/docs/325.md)
- [Direct proof - PDF](preprints/A-direct-proof-of-the-complete-Crouzeix-inequality-September-26-2026/paper.pdf)
- [Direct proof source](preprints/A-direct-proof-of-the-complete-Crouzeix-inequality-September-26-2026/build/main.tex)

The complete Crouzeix inequality controls matrix-valued polynomial/rational functions of a nonnormal operator by their supremum over the numerical range, with sharp universal constant two.

Potential use appears only if the DPT reduced representation grows beyond the current low-dimensional exact maps and needs certified polynomial/rational functional calculus for a nonnormal propagator. Do not introduce it merely because matrices are present.

## 13. Secondary watchlist

The full `overview.tex` catalogue was screened across all 372 families for inverse/recovery, measurement/observation, memory/information, finite representations, stability, query complexity, certification, moments/interactions, coordinates, and lower bounds.

The following are retained but not promoted:

- **F357 - Bi-Lipschitz coordinates at regular RCD points.** Example of a genuine stable local coordinate theorem requiring strong regularity hypotheses. Useful conceptual contrast to mere injective coordinates.
- **F374 - sharp one-third stability of Brenier maps.** Good reminder that uniqueness and the quantitative stability exponent are different problems.
- **F098 - no finite-dimensional bi-Lipschitz embedding for a compact doubling Hilbert subset.** Caution against assuming “compact/low-complexity-looking” automatically means stably finite-dimensional.
- **F119 - sharp binary information contraction.** Possible information-bottleneck prior; currently too remote from DPT observation geometry.
- **F229 - reconstruction thresholds.** Useful vocabulary for reconstructability/nonreconstructability transitions, but no current DPT mapping.
- **F289 companion counterexamples.** Potentially useful when defining one-sided vs symmetric native distances.

These are **D1/D2 watchlist sources**, not evidence for the present paper.

## 14. Proposed theorem stack for DPT-R1

The repository is most useful if it helps us build a coherent theorem stack rather than collect analogies.

### T1. Exact goal quotient

Prove, for the declared reduced law and command family, that a specified finite coordinate (z(h)) is sufficient and transition-closed for the chosen goals.

**Current status:** substantial exact structure already exists.

### T2. Goal-visible nullity and minimal local measurement count

Define (K=ker DO), (N=Kcapigcap_cker DG_c), and (r_G=dim(K/N)). Prove the tangent-level minimum-measurement bound and a local sufficiency statement under explicit rank assumptions.

**Repository drivers:** F355 + current reduced-law reachable-pair result.

### T3. Predictive information lower bound

Define a goal pseudometric and prove a finite-code/packing lower bound for uniform prediction. Extend only if necessary to noisy or randomized observation.

**Repository driver:** F140.

### T4. Ordered command signature

Define the primitive/mixed/ordered word hierarchy and identify which coefficients are determined by existing axes and which require new acquisitions.

**Repository driver:** F116, with external Chen-Fliess prior subtraction required.

### T5. Approximate command-algebra stability

Define a native composition defect and characterize conditions under which an approximate finite command map lies near an exact reusable representation.

**Repository drivers:** F251, with F289 as a caution on metrics/structural closeness.

### T6. Certificate-grade numerical layer

Give exact or one-sided numerical certificates for every computation that carries a mathematical claim, and a separate provenance contract for simulator outcomes.

**Repository driver:** F266.

## 15. S09 / optional S10 consequence

The existing S09 fusion should remain the primary fresh acquisition unless its freshness contract has already been invalidated.

Its mathematical role is now sharper:

> **S09 is the first mixed-functional acquisition outside the primitive axes.**

For the declared quadratic response class, the primitive axes leave (C_{AB}) free. The mixed query purchases exactly that missing coefficient. This is preferable to another same-axis amplitude point if the main uncertainty is interaction rather than one-dimensional amplitude remainder.

After S09 is scored:

- if interaction is near zero, retain the affine/linear-memory null for this primitive pair only;
- if it supports the Q/phase cluster, record prospective usefulness but do not infer unique charge mechanism;
- if it lands outside all frozen candidates, reject those finite interaction rules and identify the new mixed functional rather than retrofitting gain/phase;
- use post-score charge diagnostics only to localize whether the failure is charge additivity or transverse interaction.

Optional S10 should be selected by the **remaining goal-visible / interaction nullspace**, not by an arbitrary “largest predicted difference” heuristic. A particularly valuable S10 may distinguish ordered (AB) from (BA) or another nonredundant timing cross if S09 leaves those coefficients unresolved.

## 16. Claim-boundary checklist

Before citing a family in the DPT paper or a Pro-run report, classify the use:

| Question | Required answer |
|---|---|
| Is the OpenAI theorem itself being applied? | State the exact assumptions and prove the DPT object satisfies them. |
| Is only a proof architecture being borrowed? | Say so; rederive the DPT theorem independently. |
| Is it only an analogy? | Keep it out of the load-bearing proof. |
| Does Lean formalize the exact headline used? | Check the family scope file; do not infer full-paper formalization. |
| Does the source prove uniqueness, reconstruction, finite sufficiency, or stability? | Use only the one it actually proves. |
| Is the result about a full operator while DPT has finite trajectories? | Do not collapse the distinction. |
| Is the model group/unitary while DPT is a semigroup/nonunitary? | No theorem transfer without a new argument. |
| Was a computation merely generated numerically? | Separate generation from exact/one-sided verification and provenance. |

## 17. Recommended source bundles for future Pro runs

Do not send the whole 722-manuscript repository to every model. Route only the bundle that matches the scientific bottleneck.

### Measurement sufficiency / P2
- `pro17d_scientific_report.md`
- F355 `linear.tex`
- F140 `06-fiber.tex` + relevant scope
- current reduced-law derivations and reachable-pair evidence

### Command algebra / interaction
- Pro17D A3/N4 material
- F116 `iterated-integrals.tex`, `multiplicity.tex`
- frozen primitive/fusion data and exact command definitions

### Native certification
- F266 verification/execution sections
- simulator/model manifests
- scorer code/results
- numerical-domain and remainder evidence

### Identifiability claim review
- F365 positive + negative pair
- F372 scope and coefficient-recovery structure
- explicit DPT model/observation/goal/symmetry declaration

### Approximate native algebra
- F251 definition/construction
- F289 metric/stability introduction
- measured composition defects for actual DPT command maps

## 18. Reading queue

The next useful deep reads are ordered by expected DPT decision impact:

1. **F140:** `Posterior replicas and conditional information` and `Subsphere methods` - determine whether any sharper finite-fiber lower-bound device survives beyond the simple packing argument.
2. **F355:** finish the finite-dimensional reduction around `finite-linear.tex` and related normalized-coordinate construction - look for a clean theorem template for minimal observation design.
3. **F116:** `formula-systems.tex` and `construction.tex` only if we pursue finite universal tests for command words.
4. **F266:** inspect rounding and verifier code when converting specific Pro17D numerical claims into certificates.
5. **F365:** read the matrix continuation / global sections only if full-native inverse structure becomes central.
6. **F251:** search the proof for quantitative defect-to-distance mechanisms that might inspire a semigroup analogue.
7. **External prior subtraction:** Hermann-Krener nonlinear observability, Chen-Fliess series/realization, predictive-state representations, goal-oriented model reduction, and experiment design. These are required before novelty claims around T2-T5.

## 19. Maintenance protocol

Whenever a new OpenAI Math manuscript changes DPT work, append one entry with:

1. family/manuscript and exact path;
2. date and read depth;
3. theorem actually used;
4. DPT object it maps to;
5. assumptions that survive the mapping;
6. assumptions that fail;
7. new derivation / acquisition / certificate created;
8. claim ceiling after prior subtraction;
9. next falsifier or unresolved dependency.

Do not mark a source as “used” merely because it was cited or discussed. A source becomes **materially used** only if it changes a definition, proof, experiment, certificate, bound, or claim boundary.

---

### Current bottom line

The repository has already contributed more than isolated mathematical tricks. The strongest coherent route is now:

[
oxed{
	ext{finite predictive quotient}
+
	ext{goal-visible measurement lower bound}
+
	ext{information lower bound}
+
	ext{ordered interaction acquisition}
+
	ext{certificate-grade validation}
}
]

F140, F355, and F116 are the most important sources for raising the mathematical ceiling. F365/F372 keep identifiability claims honest, F266 can raise the evidentiary standard, and F251 defines a plausible longer-term route from exact reduced algebra to robust native algebra.
