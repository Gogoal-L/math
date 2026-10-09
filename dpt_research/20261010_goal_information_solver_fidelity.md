# DPT-R1 frontier note: goal information x solver fidelity (2026-10-10)

**Status: independent mathematics + synthetic executable tests; NOT a newly accepted native SiC result.** This note extends the 2026-10-09 research map and leaves S09, the controller's scientific authority, and native budgets unchanged.

## Why this is a potentially stronger research object

The current DPT-R1 has (a) actual-law, prospective 150/600 V command predictions, including ordered commands, (b) an Eth local consistent chart/lift with qualified numerical derivatives, (c) a fixed two-row Q summary with radius/goal dependence, and (d) same-law one-Newton predictions that are often close to a fully solved finite law. These are different resources:

1. **Predictive information:** which initial physical directions are indispensable for a specified collection of future goals and command words?
2. **Numerical fidelity:** once the information and constitutive law are fixed, how accurately must an implicit step/trajectory be solved to meet the same goal tolerance?

The proposed next object is a **goal-, horizon-, radius-, and solver-conditional information/computation boundary**. This is a research hypothesis for *actual SiC*; its two calculable mathematical components below are well-known types of finite-dimensional results, not claims of newly invented universal theorems.

## I. All-word minimal goal quotient for a fixed linear switched model

Assume one fixed common state chart, finite alphabet `A`, and an exact linear homogeneous model

\[
 x_{k+1}=A_a x_k,\qquad g_k=Cx_k,\qquad y_0=Ox_0.
\]

Each `A_a` must be a specified matrix **valid after every reachable admissible prefix**. This strong condition is not established by one Jacobian of a nonlinear DPT. The current observation `O` is known at preparation; it is not automatically an autonomously updating state.

Define row spaces

\[
 W_0=\operatorname{row}(C),\quad
 W_{h+1}= W_h + \sum_{a\in\mathcal A} W_h A_a.
\]

**Proposition (standard switched-linear realization/observability argument; elementary proof here).** The sequence stabilizes after at most `n-rank(C)` strict rank increments. Write its least fixed space as `W_*`, of dimension `d_*`, and choose any full-row-rank matrix `B` with `row(B)=W_*`. Then:

- `z=Bx` contains every future goal `C A_{a_k}...A_{a_1}x` of this model, for *all finite words*, even though the word set is infinite;
- each command has a well-defined **exact autonomous** reduced update `z'=M_a z` because `BA_a=M_a B`, and `Cx=Dz` for some `D`;
- `d_*` is **minimal among autonomous linear goal-only state representations valid for all x in R^n**;
- given already available noiseless preparation rows `O`, the minimum count of additional **arbitrarily designed scalar linear measurements** needed to recover all-word goal data is

\[
 k_{\mathrm{free}}=\operatorname{rank}\begin{bmatrix}O\\B\end{bmatrix}-\operatorname{rank}(O).
\]

**Proof.** `W_h` is nested, so any genuine strict step raises rank by at least one and rank is at most `n`. Equality `W_{h+1}=W_h` makes `W_h A_a \subseteq W_h` for all `a`, so it contains all word rows by induction. Choosing `B` as a basis of `W_*` gives `BA_a=M_a B` and `C=DB`. Conversely, any valid linear state `Px`, updated by all commands with output `Cx`, must have row(P) containing `C` and be invariant under all `A_a`; hence it contains `W_*`. The measurement formula follows by completing row(O) to span row(O)+`W_*`. □

The new `dpt_tools/goal_word_quotient.py` computes the iterative row-space basis without enumerating exponentially many words and reports both `d_*` and `k_free` plus reduced matrices and closure residuals. Each numerical rank is tolerance-dependent: finite floating-point ranks are **diagnostics**, not an interval-certified exact rank theorem.

**Counterexample: primitive adequacy does not imply BA adequacy.** For

\[
 A=\begin{pmatrix}1&0&0\\0&1&1\\0&0&1\end{pmatrix},\quad
 B=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix},\quad C=O=(1,0,0),
\]

`C e3=CA e3=CB e3=0`, while `CBA e3=1`. For words of length at most `0,1,2`, ranks of goal information are `1,2,3`; missing free linear measurement counts beyond O are `0,1,2`. An extra hidden direction is exposed only by command A followed by B. The demonstration is exact algebra, not a DPT-native BA claim.

**DPT bridge and falsifier.** Construct *common-chart* transition Jacobians only after composing the qualified Eth lift, moving-event derivatives and all coordinate transforms. With the genuinely prefix-dependent nonlinear native map, do **not** pretend that one constant `A_a` works globally. If such a fixed-switching approximation fails an admissible two-command sensitivity replay, treat that as evidence for **mode-/prefix-indexed derivatives or nonlinear finite-radius analysis**, not an excuse to remove the counterexample. For actual archived ordered commands, the finite-word pathwise Jacobians are the correct initial evidence, and the all-word quotient is a strong **conditional comparator** to attempt only once its fixed-model contract is met.

## II. Conditional goal certificate from an implicit same-law residual

Suppose a previously frozen preparation and future command induce a *square smooth* implicit system `F(y)=0` on one qualified branch. Here `y` may contain one BE stage or the **entire stacked stage trajectory** after a legal consistency lift. Evaluate the full-law residual and Jacobian at a cheaper predicted state `yhat`:

\[
 r=F(\widehat y),\quad J=DF(\widehat y),\quad q=Dg(\widehat y).
\]

Assume, in a complete closed ball `B(yhat,R)` contained in the *same smooth physical/DAE branch*:

- `J` is invertible, with independently established `||J^{-1}||_2 <= beta`;
- `||J^{-1}r||_2 <= eta`;
- `||DF(u)-DF(v)||_2 <= L ||u-v||_2` for all points of the ball;
- for a **scalar smooth goal** `g`, `||D^2 g||_2 <= H_g` throughout the ball.

Let `h=beta*L*eta`. For `h<=1/2`, set

\[
 \rho=\frac{2\eta}{1+\sqrt{1-2h}}\qquad (\rho=\eta\text{ when }L=0).
\]

If `rho<=R`, the standard Newton--Kantorovich result supplies a nearby full-law root `y*` with `||y*-yhat||<=rho` (with the usual domain hypotheses). Solve one adjoint system `J^T lambda=q^T`. Then our elementary **goal-specific correction and remainder** is:

\[
 \boxed{
 \left|\,[g(y^*)-g(\widehat y)]+\lambda^T r\,\right|
 \le \tfrac12(\|\lambda\|_2 L + H_g)\rho^2 .
 }
\]

**Proof of the goal bound.** Put `d=y*-yhat`. Taylor's theorem gives `0=r+Jd+R_F`, with `||R_F||<=L||d||²/2`. Thus `d=-J^{-1}r-J^{-1}R_F`. Taylor-expanding the goal gives `g(y*)-g(yhat)=q d+R_g`, `|R_g|<=H_g||d||²/2`. Since `qJ^{-1}=lambda^T`, the formula follows from the triangle inequality and `||d||<=rho`. □

Therefore, the **pretarget-computable** signed correction to the cheap prediction is `-lambda^T r`, with conditional post-correction error no larger than the right-hand side. The code in `dpt_tools/implicit_goal_certificate.py` evaluates this conditional formula, including inconclusive outcomes when curvature or domain constraints fail. Its input regularity/norm bounds are NOT discovered or rigorously validated by the code.

**Synthetic comparison.** `F(y)=y+y²-0.09`, `yhat=0`, goal `g(y)=y`, `beta=1`, `eta=0.09`, `L=2`, `H_g=0`, `R=0.2`. Here `rho=0.1`, `lambda=1`, first-order correction `+0.09`, conditional remainder `0.01`; the positive exact root is `(-1+sqrt(1.36))/2≈0.083095`, so the actual corrected error is about `0.006905`. The error bound holds; it is deliberately conservative.

**Why this matters for DPT.** If a one-Newton trajectory is cheap, full-law residuals and a stage/trajectory adjoint may establish *ahead of the native outcome* that it is adequate for smooth `work` or a fixed-time smooth readout. This can separate:

- `INFORMATION_LIMIT`: two legal preparation histories with the same retained summary but goal-divergent futures;
- `SOLVER_LIMIT`: same-law and same preparation information, but insufficient implicit root accuracy for the goal;
- `CONSTITUTIVE_LIMIT`: full-law model does not predict native/vendor outcome despite adequate same-law solution;
- `EVENT/DOMAIN_LIMIT`: a changing guard, inconsistent chart, disappearing root branch, or nonsmooth peak invalidates the smooth certificate.

For complete *multistage* claims, form `F` across all steps, including previous-state derivatives, Eth consistency equations and moving-event terms; a certificate at one stage with frozen previous states is **not** automatically a whole-command certificate. Fixed-window maxima are only eligible where the active peak is unique, separated and smooth with a controlled continuation; event switching otherwise needs a distinct nonsmooth analysis. The same-law goal certificate does **not** certify vendor-to-hardware physics.

## III. Join the axes into an actual decision

For each declared `(preparation family, command family, goal, tolerance)`, use the following independent tests before choosing more physical complexity:

| What fails? | Diagnosis | Next evidence |
|---|---|---|
| Extra goal rows grow with horizon | current summary merges future-distinct states | look for legal reachable alias / add allowed preparation information |
| Goal rank stable but cheap prediction differs from full | solver or constitutive approximation, not necessarily missing state | evaluate full-law residual and adjoint at cheap trajectory; check Newton ball |
| Cheap and full agree, both depart from native | discrepancy in physical model/ports/events | choose frozen rival model & intervention, not more Newton iterations |
| Linear quotient passes only on one nominal chart | unqualified nonlinear/prefix/DAE continuation | first qualify Eth lift and trajectory-dependent derivatives |

This defines a **joint information–computation adequacy map**, not a new established experimental result. A meaningful paper-level advance would show one native domain where both costs can be reduced simultaneously, and another frozen command/goal where an independently predicted boundary is crossed.

## IV. Primary-source provenance and prior art

- **OpenAI Math F149:** [uniform permanence: introduction](../preprints/Uniform-Permanence-in-Weakly-Reversible-Mass-Action-Systems-October-5-2026/build/sections/introduction.tex) and [trapping construction](../preprints/Uniform-Permanence-in-Weakly-Reversible-Mass-Action-Systems-October-5-2026/build/sections/trapping.tex). Its convex invariant sets are for weakly reversible mass-action ODEs, not SiC; the transferable *proof tactic* is a domain invariant region. `lean/docs/149.md` formalizes an earlier boundedness/persistence scope, not automatically the October classwise permanence refinement.
- **OpenAI Math F328:** [nonexpansive fixed-point proof](../preprints/Fixed-Points-of-Nonexpansive-Maps-in-Reflexive-Banach-Spaces-September-24-2026/build/sections/00-introduction.tex), [resolvent/anchor construction](../preprints/Fixed-Points-of-Nonexpansive-Maps-in-Reflexive-Banach-Spaces-September-24-2026/build/sections/02-anchor.tex). A nonexpansive fixed-point theorem alone supplies neither unique Eth lift nor the DPT residual goal radius; only an analogy for explicit iterative/domain construction.
- **OpenAI Math F121:** [interval connection geometry](../preprints/An-Almost-Linear-Approximation-Scheme-for-Edit-Distance-September-24-2026/build/sections/02-geometry.tex). The matching/connection estimate concerns symbol edit distance; any event-timing waveform analogue must be derived afresh.
- **Classical essential competitor:** Petreczky, Bako and van Schuppen (2013), *Realization theory of discrete-time linear switched systems*, Automatica 49, 3337–3344, DOI [10.1016/j.automatica.2013.07.022](https://doi.org/10.1016/j.automatica.2013.07.022). Therefore the row-space quotient is not claimed as a new realization theorem.
- **Classical essential competitor:** Newton–Kantorovich theorem; e.g. Kelley, *Iterative Methods for Linear and Nonlinear Equations*, SIAM (1995), chapter 5; [accessible proof context](https://doi.org/10.1007/s40314-025-03158-2). Goal-oriented dual-weighted residual error analysis also long predates this DPT transfer (e.g. [2024 review](https://www.sciencedirect.com/science/article/pii/S0065215624000279)).

## V. Concrete handoff to DPT controller (without route authorization)

1. **Zero-fresh:** take one qualified native-preparation/prefix and a named set of modes/commands; decide if exact same-chart constant `A_a` is *scientifically legitimate*. If not, retain finite observed-word Jacobians instead of passing an invalid surrogate to the all-word rank algorithm.
2. **Zero-fresh:** evaluate `F_full(yhat)` on a frozen one-Newton trajectory and its smooth fixed scalar goal; compare `-lambda^T r` with retrospective full-vs-cheap deviation **only as an exploratory replay**, with no native target used to choose `r` or `lambda`.
3. If promising, obtain defensible ball-wide `beta, eta, L, H_g, R` from actual vendor/source derivatives, interval or conservative adaptive bounds and verified guard/branch containment. Then rerun the *conditional* goal certificate. Failure is an informative finding; no extrapolation from the synthetic test.
4. Continue to preserve the already accepted native prediction and the 2026-10-09 MAP as local scientific authority. These two new mathematical components are `THEOREM_IN_FIXED_CLASS / SYNTHETIC_TESTED / DPT_NATIVE_UNTESTED` until separately adjudicated.