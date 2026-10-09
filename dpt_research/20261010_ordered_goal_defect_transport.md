# 2026-10-10 frontier: command-ordered goal-error transport and information/computation allocation

**Scientific status:** exact elementary theorem for a supplied finite-dimensional linear switched model, with constructive synthetic tests; **DPT-native stage transport, nonlinearity envelopes, and physical admissibility NOT verified**. This note extends the already accepted DPT-R1 S09 results without updating its evidence or owner decisions.

**Source identity:** current upstream [OpenAI Math](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb) at fd4aeeb2, fork scientific baseline 2026-10-09 and 2026-10-10 [goal-information × solver-fidelity note](20261010_goal_information_solver_fidelity.md). Manuscripts are *preprints* and their proof patterns are not DPT theorems.

## 1. What changed relative to the previous frontier?

The previous tools independently answer (i) whether an exact switched-linear model possesses a smaller **all-word autonomous goal quotient** (goal_word_quotient.py), (ii) how large a finite-bank observation/goal ambiguity remains (goal_ambiguity_audit.py), and (iii) whether a cheap implicit solve has a small **single-system goal-weighted residual**, conditionally on its Newton–Kantorovich envelopes (implicit_goal_certificate.py).

None of these three automatically determines **which initially hidden direction or which numerical defect at which stage will be magnified by an ordered A/B command and become the final goal error**. Eigenvalues of individual stage Jacobians are insufficient, while multiplying ambient operator norms may be needlessly conservative for a fixed VDS/J5 readout.

The new research object is a **goal- and command-word-specific transport of independently bounded information and computational defects**. The exact algebra is classical linear reachability/support-function mathematics. Its potential DPT contribution is a defensible, physical-input-specific answer to *where new information versus more accurate computation is actually needed*.

## 2. Exact conditional finite-word result

Fix one known command word of length H and one **common, dimensionless/physically scaled state chart**, with known matrices A_0,...,A_{H-1} and scalar goal rows c_k:

\[
\delta x_{j+1}=A_j\delta x_j+\xi_j,\qquad
\delta g_k=c_k\delta x_k,\quad k=0,\ldots,H.
\]

The admissible uncertainty set is explicitly the Cartesian product of Euclidean balls:

\[
O\,\delta x_0=0,\quad \|\delta x_0\|_2\le \rho,\qquad
\|\xi_j\|_2\le\epsilon_j \quad\text{independently for }j=0,\ldots,H-1.
\]

The first condition is **exact observation equality**, not a claim about noisy sensors or a nonlinear reachable family. Let K=ker(O) and P_K be its orthogonal projector (in the declared physically scaled metric). Define backward goal rows

\[
q_{k,k}=c_k,\qquad q_{k,j}=q_{k,j+1}A_j \quad (j=k-1,\ldots,0).
\]

**Proposition (elementary, independently derived).** For every endpoint k, under exactly the conditions above,

\[
\boxed{
\sup_{\delta x_0,\xi_0,\ldots,\xi_{k-1}} |\delta g_k|
=
\underbrace{\rho\,\|q_{k,0}P_K\|_2}_{\mathcal I_k:\;\text{hidden preparation information}}
+
\underbrace{\sum_{j=0}^{k-1}\epsilon_j\,\|q_{k,j+1}\|_2}_{\mathcal E_k:\;\text{stage defects}}.
}
\]

For the worst endpoint in this **finite sampled stage set**, the sharp result is \(\max_{0\le k\le H}(\mathcal I_k+\mathcal E_k)\).

**Proof.** Substitute the linear recurrence into the scalar readout:

\[
\delta g_k=q_{k,0}\delta x_0+\sum_{j<k}q_{k,j+1}\xi_j.
\]

Since \(\delta x_0\in K\), the initial term is bounded by \(\rho\|q_{k,0}P_K\|\). Each independent Euclidean disturbance ball contributes its dual-norm support function \(\epsilon_j\|q_{k,j+1}\|\). The sum is attained *simultaneously* by aligning each admissible vector with its corresponding backward row (and reversing all signs for the negative extreme). Thus the sum is **exact for the stated product-ball model**, not merely a triangle-inequality upper bound. The finite maximum commutes with the supremum over disturbances. QED.

This equality is generally **not sharp for actual DPT** if physical reachability, current-temperature coupling, KCL/KVL, source residuals, or event constraints couple/distort these uncertainty balls. If each actual disturbance belongs to the assumed ball, the calculated value is still an upper bound within the linear model; it is not a guarantee when A_k themselves are unvalidated local approximations.

### Numerical witness and nonnormal counterexample

Set \(A=\begin{psmallmatrix}0.5&6\\0&0.5\end{psmallmatrix}\), \(O=c=(1,0)\), \(\rho=0.01\), \(\epsilon_0=0\). Both eigenvalues are 0.5, yet the initial hidden direction \(e_2\) is invisible at k=0 and produces goal deviation 0.06 at k=1. Therefore the spectral-radius test misses a goal-visible transient gain. The new auditor constructs and replays this exact worst-case perturbation.

A second synthetic counterexample uses two noncommuting command matrices and gives a nonzero hidden-goal radius after A then B but zero after B then A. This is not an explanation of existing native AB/BA results; it establishes why order must remain literal in a valid goal-error calculation.

## 3. New executable tool and relation to existing code

- [goal_defect_transport.py](../dpt_tools/goal_defect_transport.py): ordered matrix sequence, exact-observation nullspace, initial hidden radius, per-stage additive error radii and one scalar goal at each stage; computes \(\mathcal I_k\), \(\mathcal E_k\), total radius, worst stage, spectral/operator-norm context, and an explicit maximizing witness.
- [test_goal_defect_transport.py](../dpt_tools/test_goal_defect_transport.py): 11 synthetic/analytic tests, including independently enumerated scalar disturbances, nonnormal hidden leakage, command order, exact observation removal, stage-dependent readouts, invalid inputs and constructive witness validation.

The auditor **does not** infer \(\epsilon_j\) from RAW, trust a local derivative outside its regime, infer instrument noise, or certify a nonlinear physical state. Input stages are stored in an NPZ with five arrays: updates (H,n,n), observation (m,n), goal (n,) or (H+1,n), initial_radius (scalar), defect_radii (H,). Its output status is a conditional model diagnostic. It is complementary to the all-word row-span quotient: the previous algorithm measures *how many hidden directions exist*, while this one measures *how strongly they matter for a given finite command word and goal*.

## 4. OpenAI Math original-proof inspection: retained and rejected transfers

| Family and source | Exact paper object / proof feature examined | New DPT value | Transfer ceiling |
|---|---|---|---|
| **F325** [complete Crouzeix direct proof](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-direct-proof-of-the-complete-Crouzeix-inequality-September-26-2026/build/main.tex) | Numerical range and matrix-coefficient polynomial functional calculus; \(\|P[A]\|\le2\max_{z\in W(A)}\|P(z)\|\), with fixed base operator A | Reinforces nonnormal growth and output-specific operator norm rather than eigenvalues; the new tool computes **literal ordered products and dual rows** | F325's constant 2 is **not** asserted for arbitrary products \(A_{k-1}\cdots A_0\); our finite-word formula follows from elementary duality, not F325 |
| **F251** [October Strong Ulam stability](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Strong-Ulam-Stability-Characterizes-Amenability-October-5-2026/build/strong-ulam-stability.tex) | Main theorem characterizes when uniformly small composition defect of unitary maps on a **countable group**, in all Hilbert dimensions, can be corrected uniformly to an exact representation; nonamenable counterconstruction | Forces us to distinguish local composition error from global exact reduced command algebra | Physical DPT commands form a constrained partial switching semigroup, not the unitary group; do **not** transfer its amenability criterion or theorem |
| **F289** [near-inclusion obstruction](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Near-Inclusions-of-von-Neumann-Algebras-Without-Small-Spatial-Embeddings-October-5-2026/build/sections/obstruction.tex) | Clock/shift matrices almost commute but a trace-log winding invariant prevents nearby commuting unitaries; one-sided near inclusion need not yield near-identity spatial implementation | Warns against promoting near-zero observed closure residual to existence of a globally exact lift; provides a useful **structural counterexample template**, not a circuit mechanism | No identified unitary/topological obstruction in Eth has been shown |
| **F129** [one-way liveness state bound](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/build/sections/introduction.tex) | Context-separation through the relation monoid gives exponential deterministic-state costs for a *growing command alphabet* | Reinforces the idea that representational complexity depends on future contexts; check whether an apparently invisible DPT direction becomes visible in a later command | The exponential exponent and automata complexity do not apply to fixed finite DPT commands |
| **F363** [October local-conservation nonuniqueness](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Nonuniqueness-with-local-conservation-for-the-hard-sphere-Boltzmann-equation-October-5-2026/build/paper/01-introduction.tex) | Two renormalized kinetic solutions share data and exact local conserved moments while differing dynamically in a rough weak-solution class | Keep charge/energy balance, unique state evolution and goal prediction as separate scientific checks | Does not imply nonuniqueness of smooth finite-dimensional SiC ODE/DAE solutions |
| **F151** [C1 entropy counterexample](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-C1-Counterexample-to-the-Entropy-Conjecture-September-25-2026/build/source/entropy.tex) | Constructs an entropy-localization argument and counterexample at the exact C1/noninvertible regularity boundary | A reminder that orbit behavior cannot be inferred from a convenient partial invariant under weaker regularity | No immediate executable DPT transfer: **WATCH**, not a new workstream |

**Lean/verification scope as of fd4aeeb2:** [F325 scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/325.md) covers its numerical-range theorem. [F251 scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/251.md) belongs to its September unitarizability result, not the October Strong Ulam companion; [F289 scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/289.md) covers September two-sided stability, not the October near-inclusion counterexample. [F129 scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/129.md) includes one-way liveness; [F363 scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/363.md) covers the earlier periodic result, not October exact local-conservation refinement. We inspected specific cited theorem/proof sections and scopes; we did **not** reverify every manuscript's full proof.

**Closest prior art:** classical support functions and robust reachable sets (e.g., [Kurzhanski–Varaiya, SIAM JCO](https://doi.org/10.1137/S0363012903437605)), nonnormal matrix transient behavior (Trefethen–Embree, *Spectra and Pseudospectra*), DAE transient growth ([Embree–Keeler, SIAM](https://doi.org/10.1137/15M1055012)), and switched reduced-output error analysis ([Schulze–Unger, SIAM](https://doi.org/10.1137/18M1167887)). This is **not** a newly proven universal model-reduction theorem. The new executable object is specific coupling of already justified mathematical ingredients to the DPT research decision.

## 5. DPT zero-fresh transfer contract and falsifiers

One useful, source-backed unit from the local controller would supply:

1. **Frozen same-law command identity and valid prefix:** command word, source branch, preparation/history ID, exact reference/query identity and goal (VDS/J5/fixed work/peak).
2. **A qualified common state chart:** actual Eth guard, correct local lift derivative, event-time derivative, and explicit mapping of each stage tangent into one physically scaled coordinate system. Without this, products of stage matrices can be dimensionally compatible and still meaningless.
3. **Observation O with acquisition identity:** source-only preparation information, existing prefix/Q summary, and separately accounted internal Tj. No post-target information in O.
4. **Validated radii, not guessed ones:** root uncertainty restricted to the actual physically reachable observation fiber; per-stage nonlinear/local-truncation/inexact-solver errors that are genuine bounds on the same declared branch and norm. If only point estimates are available, label outputs *SENSITIVITY_ONLY*.
5. **Goal row c at each stage:** derived from the same frozen readout, with moving-event/peak nonsmoothness treated appropriately. A whole-pulse peak is not automatically differentiable at a tied event.
6. **Prospective discriminator:** first compare the real archived stage errors against transport sensitivities and check if goal errors localize to the predicted stage/readout. Then, if material separation survives ordinary competitor predictions and source budgets, ask the controller about an authorized future native query.

The most decision-relevant outputs are:
- \(\mathcal I_k\) large, \(\mathcal E_k\) small: candidate need for legal extra information (e.g., a distinguishable goal-visible preparation direction). It does **not** prove which physical sensor is minimal.
- \(\mathcal I_k\) small, \(\mathcal E_k\) large: candidate need for tighter stage solver/finite law. Calculate real residual-based bounds before changing solver.
- Both small but observed native discrepancy large: wrong model class, unqualified transport, goal/event readout mismatch, or underestimated error budgets; reject the proposed certificate rather than claiming success.
- A command with nearly identical full/affine forecast yet small model differences is not a high-value discriminator merely because the stage matrices are nonnormal.

### Strongest rejection risks

First, actual stage matrices may be **prefix-dependent** and linked through singular/ill-conditioned nonlinear DAE charts; the exact linear assumption might fail outside a narrow neighborhood. Second, physical histories may not fill the assumed Euclidean balls, so the equality is not sharp on the reachable set. Third, actual local residuals can be correlated across stages and may cancel in a signed goal, while the product-ball bound assumes independently adversarial directions. Fourth, physical measurement noise breaks exact observation equality. Fifth, full-law solver agreement is still model agreement, not hardware truth.

A **negative or inconclusive result is informative**: it identifies which claimed information/computation certificate requires a better physical state, branch, error envelope or goal functional, without reversing accepted S09 native positives.

## 6. Practical next action

The main controller can perform a *zero-fresh* replay using already qualified Sol9 Eth tangent/lift and Sol10 TT-source / one-Newton material. Compare the source-residual direction and exact ordered goal transport before commissioning new LTspice. Do **not** treat this Math fork as scientific authority and do not update S09 freeze merely because a synthetic test passed.

**Status ledger:** paper-family proof-pattern inspection completed for F251, F289, F325, F129, F363, F151; **NEW mathematical tool:** one exact conditional finite-dimensional formula and constructive witness; **tests:** eleven isolated synthetic/analytic tests; **DPT-native verification:** pending independent evidence and owner adjudication.
