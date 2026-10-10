# Goal stability and compositional closure: a mathematical bridge for DPT-R1

**Version:** 2026-10-10. **DPT baseline:** `Gogoal-L/math@f2108c33037c8c82b234db744bbd6fcc5928c49d`. **OpenAI Math:** `openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. **Result status:** independently derived finite-dimensional propositions and synthetic tests; native DPT constitutive/DAE equations, physical histories, and S09 owner acceptance are not part of these proofs. **Route:** source-to-mathematics-to-native-evidence only; no new LTspice, freeze or authority change.

## 1. Locate the missing arrow rather than increase the theorem count

The [goal ambiguity audit](../dpt_tools/goal_ambiguity_audit.py) gives an unrestricted scalar decoder's information floor under Euclidean observation balls. [Goal tolerance repair](20261010_goal_tolerance_repair_cover.md) gives the exact minimum-price feature hitting set under **coordinatewise box** input uncertainty. The [all-word linear quotient](20261010_goal_information_solver_fidelity.md) gives an exact common-chart autonomous **linear** state for every command word, under its strong fixed-model assumptions. The [ordered defect transport](20261010_ordered_goal_defect_transport.md), [nonlinear fiber and admissible tube](20261010_nonlinear_fiber_and_stage_tube.md), and conditional [implicit goal residual](../dpt_tools/implicit_goal_certificate.py) handle different mathematical uncertainties.

**One gap:** separating finite histories is not the same as a **stable decoder**: arbitrarily small separation can require unbounded gain, and a good one-command scalar decoder need not be an **autonomous stage state**. The two issues require distinct proof obligations. This note adds two precise quantitative links and writes the conditional third link explicitly. The general mathematics belongs to classical Lipschitz extension and approximate dynamical realization; DPT novelty, if any, will be in physically qualified source transformations and prospective evidence.

## 2. Exact finite-bank Lipschitz goal radius with goal and sensor intervals

Let a fixed source-defined, legal history bank be \(H=\{h_1,\ldots,h_N\}\). Choose one **pretarget** feature subset \(S\), with retained nominal feature vector \(z_i^S\in\mathbb R^{d_S}\), and an independent **Cartesian box** of possible input readings

\[
 B_i^S=\prod_{r=1}^{d_S}[z_{ir}^S-\sigma_r,z_{ir}^S+\sigma_r].
\]

For each fixed future command/word \(c\), the true scalar goal of history \(i\) is only known to lie in the **independently admissible interval** \([g_{ic}-\eta_{ic},g_{ic}+\eta_{ic}]\). No statistical independence or normality is assumed. The decoder is a single deterministic, globally \(K_c\)-Lipschitz function \(f_c:\mathbb R^{d_S}\to\mathbb R\), evaluated at the *noisy pretarget reading*. The gain \(K_c\ge0\) is fixed as a design/deployment requirement (or explicitly reported as an empirical necessary bound), **not tuned on the test histories and then called a native certificate**.

**Proposition 1 (exact finite-bank stable goal radius).** In the Euclidean input metric, the optimal uniform error over every history, feasible input reading and goal-interval value is

\[
 \boxed{\displaystyle
 \mathcal R_{K_c}(S;c)=\frac12\max_{1\le i,j\le N}
 \bigl[|g_{ic}-g_{jc}|+\eta_{ic}+\eta_{jc}
 -K_c\operatorname{dist}_2(B_i^S,B_j^S)\bigr].}
 \tag{1}
\]

The \(i=j\) terms equal \(\eta_{ic}\), so the right side is nonnegative. This is **minimax over all deterministic gain-limited scalar decoders**, not over the current Q/affine/one-Newton implementation. The same retained feature subset can be used for finitely many commands, each with its **own declared** \(K_c\), target tolerance \(\tau_c\) and scalar decoder.

**Proof: necessity.** If input sets \(B_i^S,B_j^S\) are at distance \(d\), any two feasible readouts \(y_i\in B_i^S,y_j\in B_j^S\) obey \(|f(y_i)-f(y_j)|\le K_cd(y_i,y_j)\). To fit the *upper* true goal \(g_i+\eta_i\) at the first and *lower* true goal \(g_j-\eta_j\) at the second to within \(\varepsilon\), it is necessary that \(g_i+\eta_i-(g_j-\eta_j)-2\varepsilon\le K_c d\). Reverse the labels and take the infimum over the two closed boxes; this proves \(2\varepsilon\ge |g_i-g_j|+\eta_i+\eta_j-K_cd\). The same-history case gives \(\varepsilon\ge\eta_i\).

**Proof: sufficiency and explicit predictor.** Set \(\varepsilon\) equal to the right side of (1); for every input \(y\) define

\[
 \begin{aligned}
 L(y)&=\max_i \bigl[g_{ic}+\eta_{ic}-\varepsilon-K_c\operatorname{dist}(y,B_i^S)\bigr],\\
 U(y)&=\min_i \bigl[g_{ic}-\eta_{ic}+\varepsilon+K_c\operatorname{dist}(y,B_i^S)\bigr].
 \end{aligned}\tag{2}
\]

For each \(i,j\), pairwise condition (1) ensures \(g_i+\eta_i-\varepsilon\le g_j-\eta_j+\varepsilon+K_cd(B_i,B_j)\). The triangle inequality gives \(d(B_i,B_j)\le d(y,B_i)+d(y,B_j)\), hence \(L(y)\le U(y)\) for every \(y\). Each distance-to-set is 1-Lipschitz; finite pointwise maxima/minima of \(K_c\)-Lipschitz scalar functions remain \(K_c\)-Lipschitz. Thus

\[
 f_c(y)=\frac{L(y)+U(y)}2
 \tag{3}
\]

has gain at most \(K_c\). Whenever \(y\in B_i\), the \(i\)-th terms in (2) imply \(L(y)\ge g_i+\eta_i-\varepsilon\) and \(U(y)\le g_i-\eta_i+\varepsilon\); therefore \(|f_c(y)-g_i|+\eta_i\le\varepsilon\). This attains the lower bound. QED.

The extension step is elementary **real-valued McShane–Whitney envelope algebra**; see the [classical exposition](https://doi.org/10.1016/j.exmath.2025.125701). It is not a new universal theorem attributable to OpenAI Math, nor does its sharp no-loss scalar constant generalize automatically to waveform-valued/non-Hilbert targets.

**Exact recovery of the previous unrestricted criterion.** On a *fixed finite bank*, take \(K_c\to\infty\). Every pair with strictly separated boxes has positive set distance and becomes irrelevant; intersecting boxes have zero distance, so (1) reduces **exactly** to the previous arbitrary-decoder minimax over compatible pairs, with the \(\max_i\eta_i\) floor. This connects, rather than replaces, [goal_repair_cover.py](../dpt_tools/goal_repair_cover.py). A strong further result is the **minimum necessary gain** at tolerance \(\tau_c\) for a chosen representation:

\[
 K_{\min,c}(S;\tau_c)=\max_{i<j:\,D_{ij}(S)>0}
 \frac{\bigl[|g_{ic}-g_{jc}|+\eta_{ic}+\eta_{jc}-2\tau_c\bigr]_+}{D_{ij}(S)},
 \quad D_{ij}(S)=\operatorname{dist}(B_i^S,B_j^S),\tag{4}
\]

with \(K_{\min}=\infty\) if a positive numerator has \(D=0\), or if any \(\eta_{ic}>\tau_c\). Otherwise the empty max is 0. This is the **exact lower requirement for a bank-fitting gain-constrained decoder**; it is *not* a claim that the physically true goal map has that global Lipschitz constant.

## 3. A new exact finite-bank acquisition problem: stability is NOT set cover

For Cartesian coordinate intervals with common per-coordinate radii, Euclidean distances factor:

\[
 D_{ij}(S)^2=D_{ij}(\emptyset)^2+
 \sum_{s\in S}\gamma_{ij,s}^2,
 \qquad \gamma_{ij,s}=\bigl[|P_{is}-P_{js}|-2\sigma^P_s\bigr]_+.
 \tag{5}
\]

At each history pair and command, (1) requires

\[
 D_{ij}(S)\ge \frac{[|g_{ic}-g_{jc}|+\eta_{ic}+\eta_{jc}-2\tau_c]_+}{K_c}\quad(K_c>0).
 \tag{6}
\]

For \(K_c=0\), no feature set can repair a pair with positive numerator. The optimization is therefore **minimum additive feature price under joint squared-separation covering constraints**, with one subset shared across all declared commands. It is a nonlinear / additive-margin covering problem, not the binary hitting set from the previous **unrestricted-gain** theorem.

**Counterexample separating the methods.** Take two perfectly observation-aliased histories, scalar future goals 0 and 4, target tolerance 1 and gain budget \(K=1\). Three candidate pretarget scalar features each differ by \(\sqrt2\) between histories, with zero noise; two have unit cost, the third costs 3. Each feature alone gives \(\mathcal R_1=(4-\sqrt2)/2>1\). Two together yield total Euclidean set distance 2 and \(\mathcal R_1=1\); the minimum stable repair costs 2. The unrestricted-decoder hitting set selects **one** unit-cost feature. Thus “one sensor distinguishes the pair” can coexist with “one sensor cannot meet a stable prediction contract.” This mathematical difference is independent of native circuit claims.

The implementation [goal_lipschitz_stability.py](../dpt_tools/goal_lipschitz_stability.py) computes (1), (4), the explicit midpoint predictor (3), and a minimum-price feature subset by exhaustive branch-and-bound with a default 18-candidate cap; larger libraries yield **feasible greedy solutions without an approximation ratio**. Calculations are standard floating arithmetic; tight numerical boundary margins need independent precision/interval checking. An unsuccessful full-library search gives a specific stable-margin impossibility *within the supplied candidate library*, not a proof of impossible new physical information.

## 4. The missing autonomous-update arrow: a necessary pair floor and a conditional upper theorem

Suppose the full native model under command \(a\) admits a well-defined physical map \(F_a:h\mapsto h'\) on a **declared legal source-reachable domain**, including guard and Eth DAE consistency. Let \(z=\pi(h)\) be a fixed, common-chart retained state, and require one \(L_a\)-Lipschitz autonomous reduced update \(T_a(z)\). If

\[
 \|\pi(F_a(h))-T_a(\pi(h))\|\le\delta_a\quad \text{on that domain},\tag{7}
\]

then every pair of **legally reachable histories with the same available command** satisfies

\[
 \boxed{\displaystyle
 \delta_a\ge\tfrac12\Bigl[
 \|\pi(F_a(h_i))-\pi(F_a(h_j))\|
 -L_a\|\pi(h_i)-\pi(h_j)\|\Bigr]_+.}\tag{8}
\]

**Proof:** insert and subtract \(T_a(\pi(h_i))\) and \(T_a(\pi(h_j))\), then apply two defect bounds and the update Lipschitz inequality. The [transition_pair_floor](../dpt_tools/goal_lipschitz_stability.py) function reports the largest pairwise necessary lower bound on the supplied matched bank. It **does not prove sufficiency** of any vector-valued update: scalar extension logic from (1) cannot be applied as an exact vector-valued converse.

**Immediate-goal sufficiency can fail as an autonomous state.** Two legal histories may share \(z=0\) and immediate goal 0 but have projected next states \(-1,+1\) under the same command; (8) gives \(\delta_a\ge1\) for every deterministic update. A later command sensitive to the sign distinguishes them even though the original one-step goal predictor passed. A measurement repair of a fixed final goal is therefore not yet a right-congruence repair.

**Conditional positive closure.** Suppose actual source-equation / interval / DAE checks instead establish (7), and a real reduced update has \(\operatorname{Lip}(T_a)\le L_a\) throughout all required state and numerical tubes. Suppose the *implemented* update \(\widetilde T_a\) differs from \(T_a\) by at most \(\kappa_a\) there. Then for \(\widehat z_{j+1}=\widetilde T_{a_j}(\widehat z_j)\) and \(z_j=\pi(h_j)\):

\[
 e_{j+1}\le L_{a_j}e_j+\delta_{a_j}+\kappa_{a_j},\qquad e_j=\|\widehat z_j-z_j\|.
 \tag{9}
\]

By induction on the **literal command sequence** \(a_0,\ldots,a_{H-1}\),

\[
 e_H\le\left(\prod_{j=0}^{H-1}L_{a_j}\right)e_0
 +\sum_{j=0}^{H-1}(\delta_{a_j}+\kappa_{a_j})
 \prod_{r=j+1}^{H-1}L_{a_r}.
 \tag{10}
\]

For each output taken **at stage j**, assume a physically consistent stage/transition readout \(G_{a_j}(h_j)\) and a reduced scalar \(R_{a_j}(z)\) with source-wide defect \(\eta_{a_j}\) and Lipschitz gain \(K_{a_j}\); if an implemented readout contributes a separate \(\zeta_{a_j}\), then

\[
 |\widehat g_j-G_{a_j}(h_j)|\le K_{a_j}e_j+\eta_{a_j}+\zeta_{a_j}.
 \tag{11}
\]

(9)–(11) are elementary **conditional uniform upper bounds** on a verified domain, whereas (8) and (1) are **necessary finite-bank lower / exact minimax statements** on the specified observation model. They cannot be combined into an unconditional equality. This matches classical [approximate-bisimulation theory](https://doi.org/10.1016/j.automatica.2007.01.019) and [incrementally stable switched systems](https://doi.org/10.1109/TAC.2009.2034922) in spirit, but no source-specific incremental stability or bisimulation has been established for SiC.

**Avoid double counting uncertainty.** Formula (1) already includes all declared observation-coordinate and goal intervals and is a *direct* error certificate for predictor (3). Do **not** add \(K\sigma\) to it again. Likewise, (9) uses a distinct **initial latent-state estimation radius** \(e_0\), not an arbitrary reuse of \(\mathcal R_K\) (a scalar goal radius). The full-law same-history Newton residual certificate controls solver error, not an automatically independent source of information error. If a particular implemented decoder approximates (3) with separately bounded numerical evaluation error \(\epsilon_{\rm eval}\), then and only then can one conservatively add \(\epsilon_{\rm eval}\) to (1).

## 5. OpenAI Math: source mechanisms, transfer distance and rejection risk

Pinned original corpus [fd4aeeb2](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb). Source inspection here is the original LaTeX sections named, not an independently validated page-by-page PDF proof or a proof of all OpenAI claims.

| Manuscript / inspected source | Actually used mathematical insight | Applicability conclusion |
|---|---|---|
| [F332, Metric Markov Cotype Two of ℓ1](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Metric-Markov-Cotype-Two-of-l1-October-5-2026/build/main.tex), sections 2–5 (finite binary cuts, quartic potential, stopped walk, extension corollary) | It proves **Hilbert-to-ℓ1 vector-valued Lipschitz extension with a universal multiplicative gain loss**, by a nontrivial cut embedding and martingale argument. This distinguishes scalar no-loss McShane–Whitney from higher-dimensional/non-Hilbert targets. | **POSITIVE BOUNDARY:** establish (1) rigorously for each **scalar** goal. Do not claim simultaneous waveform-vector recovery with the *same* scalar \(K\) using F332's theorem; it has Hilbert-source / ℓ1-target assumptions and potentially multiplicative loss. |
| [F331, asymptotic midpoint/diamond distortion](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Asymptotic-midpoint-uniform-convexity-and-unbounded-diamond-distortion-in-a-reflexive-tree-space-September-27-2026/build/sections/diamonds.tex), midpoint lens and level-by-level distortion proof | The exact source proof sums per-level squared losses: \(L_m^2\le L_{m+1}^2-1/12\), giving \(D^2\ge1+k/12\). | **PROOF PATTERN ONLY:** local benign geometry need not imply uniformly stable deep-word representations. It gives *no* bound on SiC \(L_a\); obtain those from DPT source trajectories or interval equations. |
| [F110, squared-log randomized k-server](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Squared-logarithmic-randomized-k-server-on-arbitrary-metrics-September-24-2026/build/source/latex/sections/10_transfer.tex), "one policy on an arbitrary metric" proof | Separates a rule tailored to an **input distribution** from one fixed causal rule working for **all finite request sequences**; uses finite separation and product compactness under explicit policy assumptions. | **QUANTIFIER DISCIPLINE:** a different fitted decoder per frozen command is weaker than a single autonomous state and lawful \(T_a\) usable on all admissible future words. Neither k-server competitive ratio nor policy compactness theorem transfers to DPT. |
| [F175, expectation threshold fractional/integral cover](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Integral-and-fractional-expectation-thresholds-are-equivalent-September-23-2026/build/source/sections/rounding.tex) (prior round) | Weight and rounding rules depend on a precise threshold cost model. | **REJECT DIRECT TRANSFER:** stable squared-distance margin cover is not their Bernoulli-price expectation-threshold problem, and ordinary set-cover gain-loss factors do not automatically apply. |
| [F139, subpolynomial query complexity](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026/build/sections/introduction.tex) (prior round) | Separates oracle query count from computational cost. | **BOUNDARY:** source solver calls, retained signal acquisition, storage, and decoder evaluation remain different costs. |

**Closest non-OpenAI mathematical precedents:** [McShane–Whitney scalar Lipschitz extension](https://doi.org/10.1016/j.exmath.2025.125701); [Girard–Pappas 2007](https://doi.org/10.1016/j.automatica.2007.01.019), approximate bisimulation relations; [Girard–Pola–Tabuada 2010](https://doi.org/10.1109/TAC.2009.2034922), symbolic models for incrementally stable switched systems. The exact interval/noise box specialization and DPT prospective acquisition use are **independent derivations / engineering proposals**, not novelty assertions about these mature mathematical fields.

**Simulated methodological roundtable, not quotations:** A McShane/Whitney scalar-extension viewpoint demands a **constructive no-loss scalar Lipschitz decoder** under exactly defined uncertainty sets. A Girard/Pappas dynamics viewpoint demands a **domain-closed approximate transition relation**, not a well-fitted one-step output. An F332 metric-extension viewpoint cautions against silently treating VDS/J5 multi-output waveforms as scalar. Their intersection yields a sharper single question: *Can a low-cost pretarget state be both goal-stable under specified noise and composition-stable under the exact same-law Eth transitions?* The first is now calculable on finite banks; the second is falsifiable by pair floor (8) but awaits source-wide bounds.

## 6. Executable tests and smallest next native input contract

Run independently in the DPT tools folder:

```bash
python -m unittest -v test_goal_lipschitz_stability.py
python goal_lipschitz_stability.py prepared_bank.npz --output stable_goal_report.json
```

The NPZ uses `observations (N,m)`, `goals (N,K)`, `candidates (N,p)`, `observation_radii (m,)`, `candidate_radii (p,)`, `goal_uncertainty (N,K)`, `goal_tolerances (K,)`, `lipschitz_limits (K,)`, `candidate_costs (p,)`; optional `candidate_names` and `command_names`. All arrays must be finite, feature costs strictly positive, uncertainty radii nonnegative; command/goal/scorer units must be declared and consistent. `decoder_value` exposes the explicit function in (3); `transition_pair_floor` reports (8) on current and next vectors for one matched command. Outputs distinguish `BASELINE_SUFFICIENT`, `EXACT_MIN_COST_STABLE_REPAIR`, `NO_LIBRARY_STABLE_REPAIR`, `INTRINSIC_GOAL_UNCERTAINTY`, and `GREEDY_FEASIBLE_NOT_PROVEN_MINIMUM`. Gains and costs are **supplied**, not learned from observed target outcomes.

The local suite covers 17 synthetic tests, including 90 independent random subset-enumeration comparisons, a stable-two-feature synergy against original set cover, interval touching, zero-gain and intrinsic-uncertainty obstructions, a globally constructed scalar decoder tested over multiple query points, and stage-alias necessary floors. An additional 50 randomized box cases tested the constructive envelope at 200 evaluation points per case. No new native runs are claimed.

**Controller's smallest high-value zero-fresh input:** (i) several actual legally reachable histories from the *same constitutive root*, same ports/timing and scorer; (ii) frozen future commands including at least one ordered AB/BA word; (iii) available **pretarget** Q rows/Iload/Tj candidates (distinguish accessible measurements from simulator hidden states); (iv) separately sourced coordinate noise and per-goal/solver uncertainty intervals; (v) actual next retained features after one stage and the Sol9 legal Eth consistency lift. Then compute stable feature-price frontier (1),(4),(6); independently test transition pair floor (8). Only after qualifying full physical tubes and a feasible global reduced update can one use (9)–(11) as a multistage **upper guarantee**. A bank positive supports **finite-bank representability**, not native all-history sufficiency; a qualified bank alias provides a valid **lower-bound witness** for the assumed class.

**Three falsifiers / route splits:**

1. No affordable pretarget feature subset meets specified `(tau,K)` across the frozen command goals: report the pair and gain limit; compare alternative command-conditional decoder or ordinary full model rather than merely adding sensors.
2. Goal-stable bank but projected post-stage pair floor exceeds the predeclared closure tolerance: the representation is **not** an autonomous state under that update, despite its fixed-command fitting.
3. No physical interval region can preserve Eth guard / branch and Lipschitz bounds: retain precise local conditional scope, and ask for source-wise continuation/invariance evidence instead of claiming a global stage guarantee.
