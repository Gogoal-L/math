# Goal stability and compositional closure: a mathematical bridge for DPT-R1

**Version:** 2026-10-10. **DPT baseline:** `Gogoal-L/math@f2108c33037c8c82b234db744bbd6fcc5928c49d`. **OpenAI Math:** `openai/math@fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. **Result status:** independently derived finite-dimensional propositions and synthetic tests; native DPT constitutive/DAE equations, physical histories, and S09 owner acceptance are not part of these proofs. **Route:** source-to-mathematics-to-native-evidence only; no new LTspice, freeze or authority change.

## 1. Locate the missing arrow rather than increase the theorem count

The [goal ambiguity audit](../dpt_tools/goal_ambiguity_audit.py) gives an unrestricted scalar decoder's information floor under Euclidean observation balls. [Goal tolerance repair](20261012_mixed_nuisance_goal_radius_formal_derivation.md) gives the exact minimum-price feature hitting set under **coordinatewise box** input uncertainty. The [all-word linear quotient](20261010_goal_information_solver_fidelity.md) gives an exact common-chart autonomous **linear** state for every command word, under its strong fixed-model assumptions. The [ordered defect transport](20261010_goal_stability_compositional_closure.md), [nonlinear fiber and admissible tube](20261012_second_order_goal_fiber.md), and conditional [implicit goal residual](../dpt_tools/implicit_goal_certificate.py) handle different mathematical uncertainties.

**One gap:** separating finite histories is not the same as a **stable decoder**: arbitrarily small separation can require unbounded gain, and a good one-command scalar decoder need not be an **autonomous stage state**. The two issues require distinct proof obligations. This note adds two precise quantitative links and writes the conditional third link explicitly. The general mathematics belongs to classical Lipschitz extension and approximate dynamical realization; DPT novelty, if any, will be in physically qualified source transformations and prospective evidence.

## 2. Exact finite-bank Lipschitz goal radius with goal and sensor intervals

Let a fixed source-defined, legal history bank be $`H=\{h_1,\ldots,h_N\}`$. Choose one **pretarget** feature subset $`S`$, with retained nominal feature vector $`z_i^S\in\mathbb R^{d_S}`$, and an independent **Cartesian box** of possible input readings

```math
B_i^S=\prod_{r=1}^{d_S}[z_{ir}^S-\sigma_r,z_{ir}^S+\sigma_r].
```

For each fixed future command/word $`c`$, the true scalar goal of history $`i`$ is only known to lie in the **independently admissible interval** $`[g_{ic}-\eta_{ic},g_{ic}+\eta_{ic}]`$. No statistical independence or normality is assumed. The decoder is a single deterministic, globally $`K_c`$-Lipschitz function $`f_c:\mathbb R^{d_S}\to\mathbb R`$, evaluated at the *noisy pretarget reading*. The gain $`K_c\ge0`$ is fixed as a design/deployment requirement (or explicitly reported as an empirical necessary bound), **not tuned on the test histories and then called a native certificate**.

**Proposition 1 (exact finite-bank stable goal radius).** In the Euclidean input metric, the optimal uniform error over every history, feasible input reading and goal-interval value is

**(1)**

```math
\boxed{\displaystyle
 \mathcal R_{K_c}(S;c)=\frac12\max_{1\le i,j\le N}
 \bigl[|g_{ic}-g_{jc}|+\eta_{ic}+\eta_{jc}
 -K_c\mathop{\mathrm{dist}}_2(B_i^S,B_j^S)\bigr].}
```

The $`i=j`$ terms equal $`\eta_{ic}`$, so the right side is nonnegative. This is **minimax over all deterministic gain-limited scalar decoders**, not over the current Q/affine/one-Newton implementation. The same retained feature subset can be used for finitely many commands, each with its **own declared** $`K_c`$, target tolerance $`\tau_c`$ and scalar decoder.

**Proof: necessity.** If input sets $`B_i^S,B_j^S`$ are at distance $`d`$, any two feasible readouts $`y_i\in B_i^S,y_j\in B_j^S`$ obey $`|f(y_i)-f(y_j)|\le K_cd(y_i,y_j)`$. To fit the *upper* true goal $`g_i+\eta_i`$ at the first and *lower* true goal $`g_j-\eta_j`$ at the second to within $`\varepsilon`$, it is necessary that $`g_i+\eta_i-(g_j-\eta_j)-2\varepsilon\le K_c d`$. Reverse the labels and take the infimum over the two closed boxes; this proves $`2\varepsilon\ge |g_i-g_j|+\eta_i+\eta_j-K_cd`$. The same-history case gives $`\varepsilon\ge\eta_i`$.

**Proof: sufficiency and explicit predictor.** Set $`\varepsilon`$ equal to the right side of (1); for every input $`y`$ define

**(2)**

```math
\begin{aligned}
 L(y)&=\max_i \bigl[g_{ic}+\eta_{ic}-\varepsilon-K_c\mathop{\mathrm{dist}}(y,B_i^S)\bigr],\\
 U(y)&=\min_i \bigl[g_{ic}-\eta_{ic}+\varepsilon+K_c\mathop{\mathrm{dist}}(y,B_i^S)\bigr].
 \end{aligned}
```

For each $`i,j`$, pairwise condition (1) ensures $`g_i+\eta_i-\varepsilon\le g_j-\eta_j+\varepsilon+K_cd(B_i,B_j)`$. The triangle inequality gives $`d(B_i,B_j)\le d(y,B_i)+d(y,B_j)`$, hence $`L(y)\le U(y)`$ for every $`y`$. Each distance-to-set is 1-Lipschitz; finite pointwise maxima/minima of $`K_c`$-Lipschitz scalar functions remain $`K_c`$-Lipschitz. Thus

**(3)**

```math
f_c(y)=\frac{L(y)+U(y)}2
```

has gain at most $`K_c`$. Whenever $`y\in B_i`$, the $`i`$-th terms in (2) imply $`L(y)\ge g_i+\eta_i-\varepsilon`$ and $`U(y)\le g_i-\eta_i+\varepsilon`$; therefore $`|f_c(y)-g_i|+\eta_i\le\varepsilon`$. This attains the lower bound. QED.

The extension step is elementary **real-valued McShane–Whitney envelope algebra**; see the [classical exposition](https://doi.org/10.1016/j.exmath.2025.125701). It is not a new universal theorem attributable to OpenAI Math, nor does its sharp no-loss scalar constant generalize automatically to waveform-valued/non-Hilbert targets.

**Exact recovery of the previous unrestricted criterion.** On a *fixed finite bank*, take $`K_c\to\infty`$. Every pair with strictly separated boxes has positive set distance and becomes irrelevant; intersecting boxes have zero distance, so (1) reduces **exactly** to the previous arbitrary-decoder minimax over compatible pairs, with the $`\max_i\eta_i`$ floor. This connects, rather than replaces, [goal_repair_cover.py](../dpt_tools/goal_repair_cover.py). A strong further result is the **minimum necessary gain** at tolerance $`\tau_c`$ for a chosen representation:

**(4)**

```math
\begin{aligned}
b_{ijc}&=\bigl[|g_{ic}-g_{jc}|
+\eta_{ic}+\eta_{jc}-2\tau_c\bigr]_+,\\
K_{\min,c}(S;\tau_c)
&=\max_{i<j:\,D_{ij}(S)>0}
\frac{b_{ijc}}{D_{ij}(S)},\\
D_{ij}(S)&=\mathop{\mathrm{dist}}(B_i^S,B_j^S).
\end{aligned}
```

with $`K_{\min}=\infty`$ if a positive numerator has $`D=0`$, or if any $`\eta_{ic}>\tau_c`$. Otherwise the empty max is 0. This is the **exact lower requirement for a bank-fitting gain-constrained decoder**; it is *not* a claim that the physically true goal map has that global Lipschitz constant.

## 3. A new exact finite-bank acquisition problem: stability is NOT set cover

For Cartesian coordinate intervals with common per-coordinate radii, Euclidean distances factor:

**(5)**

```math
D_{ij}(S)^2=D_{ij}(\emptyset)^2+
 \sum_{s\in S}\gamma_{ij,s}^2,
 \qquad \gamma_{ij,s}=\bigl[|P_{is}-P_{js}|-2\sigma^P_s\bigr]_+.
```

At each history pair and command, (1) requires

**(6)**

```math
D_{ij}(S)\ge \frac{[|g_{ic}-g_{jc}|+\eta_{ic}+\eta_{jc}-2\tau_c]_+}{K_c}\quad(K_c>0).
```

For $`K_c=0`$, no feature set can repair a pair with positive numerator. The optimization is therefore **minimum additive feature price under joint squared-separation covering constraints**, with one subset shared across all declared commands. It is a nonlinear / additive-margin covering problem, not the binary hitting set from the previous **unrestricted-gain** theorem.

**Counterexample separating the methods.** Take two perfectly observation-aliased histories, scalar future goals 0 and 4, target tolerance 1 and gain budget $`K=1`$. Three candidate pretarget scalar features each differ by $`\sqrt2`$ between histories, with zero noise; two have unit cost, the third costs 3. Each feature alone gives $`\mathcal R_1=(4-\sqrt2)/2>1`$. Two together yield total Euclidean set distance 2 and $`\mathcal R_1=1`$; the minimum stable repair costs 2. The unrestricted-decoder hitting set selects **one** unit-cost feature. Thus “one sensor distinguishes the pair” can coexist with “one sensor cannot meet a stable prediction contract.” This mathematical difference is independent of native circuit claims.

The implementation [goal_lipschitz_stability.py](../dpt_tools/goal_lipschitz_stability.py) computes (1), (4), the explicit midpoint predictor (3), and a minimum-price feature subset by exhaustive branch-and-bound with a default 18-candidate cap; larger libraries yield **feasible greedy solutions without an approximation ratio**. Calculations are standard floating arithmetic; tight numerical boundary margins need independent precision/interval checking. An unsuccessful full-library search gives a specific stable-margin impossibility *within the supplied candidate library*, not a proof of impossible new physical information.

## 4. The missing autonomous-update arrow: a necessary pair floor and a conditional upper theorem

Suppose the full native model under command $`a`$ admits a well-defined physical map $`F_a:h\mapsto h'`$ on a **declared legal source-reachable domain**, including guard and Eth DAE consistency. Let $`z=\pi(h)`$ be a fixed, common-chart retained state, and require one $`L_a`$-Lipschitz autonomous reduced update $`T_a(z)`$. If

**(7)**

```math
\|\pi(F_a(h))-T_a(\pi(h))\|\le\delta_a\quad \text{on that domain},
```

then every pair of **legally reachable histories with the same available command** satisfies

**(8)**

```math
\boxed{\displaystyle
 \delta_a\ge\tfrac12\Bigl[
 \|\pi(F_a(h_i))-\pi(F_a(h_j))\|
 -L_a\|\pi(h_i)-\pi(h_j)\|\Bigr]_+.}
```

**Proof:** insert and subtract $`T_a(\pi(h_i))`$ and $`T_a(\pi(h_j))`$, then apply two defect bounds and the update Lipschitz inequality. The [transition_pair_floor](../dpt_tools/goal_lipschitz_stability.py) function reports the largest pairwise necessary lower bound on the supplied matched bank. It **does not prove sufficiency** of any vector-valued update: scalar extension logic from (1) cannot be applied as an exact vector-valued converse.

**Immediate-goal sufficiency can fail as an autonomous state.** Two legal histories may share $`z=0`$ and immediate goal 0 but have projected next states $`-1,+1`$ under the same command; (8) gives $`\delta_a\ge1`$ for every deterministic update. A later command sensitive to the sign distinguishes them even though the original one-step goal predictor passed. A measurement repair of a fixed final goal is therefore not yet a right-congruence repair.

**Conditional positive closure.** Suppose actual source-equation / interval / DAE checks instead establish (7), and a real reduced update has $`\mathop{\mathrm{Lip}}(T_a)\le L_a`$ throughout all required state and numerical tubes. Suppose the *implemented* update $`\widetilde T_a`$ differs from $`T_a`$ by at most $`\kappa_a`$ there. Then for $`\widehat z_{j+1}=\widetilde T_{a_j}(\widehat z_j)`$ and $`z_j=\pi(h_j)`$:

**(9)**

```math
e_{j+1}\le L_{a_j}e_j+\delta_{a_j}+\kappa_{a_j},\qquad e_j=\|\widehat z_j-z_j\|.
```

By induction on the **literal command sequence** $`a_0,\ldots,a_{H-1}`$,

**(10)**

```math
e_H\le\left(\prod_{j=0}^{H-1}L_{a_j}\right)e_0
 +\sum_{j=0}^{H-1}(\delta_{a_j}+\kappa_{a_j})
 \prod_{r=j+1}^{H-1}L_{a_r}.
```

For each output taken **at stage j**, assume a physically consistent stage/transition readout $`G_{a_j}(h_j)`$ and a reduced scalar $`R_{a_j}(z)`$ with source-wide defect $`\eta_{a_j}`$ and Lipschitz gain $`K_{a_j}`$; if an implemented readout contributes a separate $`\zeta_{a_j}`$, then

**(11)**

```math
|\widehat g_j-G_{a_j}(h_j)|\le K_{a_j}e_j+\eta_{a_j}+\zeta_{a_j}.
```

(9)–(11) are elementary **conditional uniform upper bounds** on a verified domain, whereas (8) and (1) are **necessary finite-bank lower / exact minimax statements** on the specified observation model. They cannot be combined into an unconditional equality. This matches classical [approximate-bisimulation theory](https://doi.org/10.1016/j.automatica.2007.01.019) and [incrementally stable switched systems](https://doi.org/10.1109/TAC.2009.2034922) in spirit, but no source-specific incremental stability or bisimulation has been established for SiC.

**Avoid double counting uncertainty.** Formula (1) already includes all declared observation-coordinate and goal intervals and is a *direct* error certificate for predictor (3). Do **not** add $`K\sigma`$ to it again. Likewise, (9) uses a distinct **initial latent-state estimation radius** $`e_0`$, not an arbitrary reuse of $`\mathcal R_K`$ (a scalar goal radius). The full-law same-history Newton residual certificate controls solver error, not an automatically independent source of information error. If a particular implemented decoder approximates (3) with separately bounded numerical evaluation error $`\epsilon_{\rm eval}`$, then and only then can one conservatively add $`\epsilon_{\rm eval}`$ to (1).

## 5. OpenAI Math: source mechanisms, transfer distance and rejection risk

Pinned original corpus [fd4aeeb2](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb). Source inspection here is the original LaTeX sections named, not an independently validated page-by-page PDF proof or a proof of all OpenAI claims.

| Manuscript / inspected source | Actually used mathematical insight | Applicability conclusion |
|---|---|---|
| [F332, Metric Markov Cotype Two of ℓ1](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Metric-Markov-Cotype-Two-of-l1-October-5-2026/build/main.tex), sections 2–5 (finite binary cuts, quartic potential, stopped walk, extension corollary) | It proves **Hilbert-to-ℓ1 vector-valued Lipschitz extension with a universal multiplicative gain loss**, by a nontrivial cut embedding and martingale argument. This distinguishes scalar no-loss McShane–Whitney from higher-dimensional/non-Hilbert targets. | **POSITIVE BOUNDARY:** establish (1) rigorously for each **scalar** goal. Do not claim simultaneous waveform-vector recovery with the *same* scalar $`K`$ using F332's theorem; it has Hilbert-source / ℓ1-target assumptions and potentially multiplicative loss. |
| [F331, asymptotic midpoint/diamond distortion](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Asymptotic-midpoint-uniform-convexity-and-unbounded-diamond-distortion-in-a-reflexive-tree-space-September-27-2026/build/sections/diamonds.tex), midpoint lens and level-by-level distortion proof | The exact source proof sums per-level squared losses: $`L_m^2\le L_{m+1}^2-1/12`$, giving $`D^2\ge1+k/12`$. | **PROOF PATTERN ONLY:** local benign geometry need not imply uniformly stable deep-word representations. It gives *no* bound on SiC $`L_a`$; obtain those from DPT source trajectories or interval equations. |
| [F110, squared-log randomized k-server](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Squared-logarithmic-randomized-k-server-on-arbitrary-metrics-September-24-2026/build/source/latex/sections/10_transfer.tex), "one policy on an arbitrary metric" proof | Separates a rule tailored to an **input distribution** from one fixed causal rule working for **all finite request sequences**; uses finite separation and product compactness under explicit policy assumptions. | **QUANTIFIER DISCIPLINE:** a different fitted decoder per frozen command is weaker than a single autonomous state and lawful $`T_a`$ usable on all admissible future words. Neither k-server competitive ratio nor policy compactness theorem transfers to DPT. |
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

---

## Legacy MAP derivation: future-context goal quotient (M7–M9)

This exact finite-word/common-chart statement is separate from actual switched/guarded native dynamic closure. Historic formula IDs remain stable; [original frozen MAP](https://github.com/Gogoal-L/math/blob/15b3fde162b2f7cb729ec106b847be1ad046d222/DPT_MATH_RESEARCH_MAP.md).

### 0.3 F129：双侧上下文分辨 → 有限未来词的目标商空间

原文：[F129 machines](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/build/sections/machines.tex)、[matching corners](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/build/sections/matching.tex)、[rank-loss proof](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/build/sections/rank.tex)。

F129 不是“模型状态越少越好”的口号。它用完整二元关系字母表（$`2^{h^2}`$ 个 letters）和左右 singleton contexts $`I_i A I_j`$，把关系 $`A`$ 的任意一项 $`(i,j)`$ 转化为非空/空接受判据。匹配图有 idempotent corner、rank 和 common support：32 个共轭共用至多 $`64c`$ 个支持位置却制造 256 个独立关系增量；每次必须损失至少 $`L(h-31)/2`$ 个 rank，因此

**(M7)**

```math
64c\ge256\,L(h-31)/2,\qquad
c\ge2L(h-31),\qquad
L(h)=2^{\lfloor(h-2)/31\rfloor}.
```

**DPT 真正可迁移的对象是右侧未来上下文，不是该指数下界。** 对具有**全局同一线性 chart**的切换模型 $`x_{t+1}=A_u x_t`$，未来 scalar rows $`C A_w`$ 按**实际命令顺序**产生。令

**(M8)**

```math
\begin{aligned}
\mathcal V_0&=\mathop{\mathrm{row}}(C),\\
\mathcal V_{k+1}
&=\mathcal V_k+\sum_{u\in\mathcal A}\mathcal V_kA_u,\\
\mathcal V_\infty
&=\mathop{\mathrm{span}}\nolimits_{w\in\mathcal A^*}\mathop{\mathrm{row}}(CA_w).
\end{aligned}
```

若 $`\dim x=n`$，该升链最多发生 $`n-\dim\mathcal V_0`$ 次严格增维；稳定后 $`\mathcal V_\infty A_u\subseteq\mathcal V_\infty`$，所以以此 row basis $`T`$ 定义 $`z=Tx`$，存在准确 reduced update $`T A_u=\bar A_u T`$。任何线性**自主演化且覆盖所有词目标**的商状态，其 row space 必须含 $`\mathcal V_\infty`$；最小维数为 $`\dim\mathcal V_\infty`$。[goal_word_quotient](dpt_tools/goal_word_quotient.py) 计算这一命题。**有限指定** $`\mathcal W`$ 则只要求 $`\mathop{\mathrm{row}}(CA_w:w\in\mathcal W)`$，不是 all-word autonomous closure。

另一个可以直接测试的结果是**顺序交换缺陷**：

**(M9)**

```math
G_{A\to B}(x)-G_{B\to A}(x)
=C(BA-AB)x=C[B,A]x.
```

若两个短命令是连续 vector fields $`f_A,f_B`$ 的小 $`\Delta t`$ 演化且流光滑，状态交换缺陷的一阶非零项为 $`\Delta t^2(Df_B f_A-Df_A f_B)+O(\Delta t^3)`$；stage 输出/事件守卫仍可能额外产生差异。既有 18B 的 ordered-command 结果与此**问题形式**相符，但 actual switched/guarded law 并非一个全局线性交换子，因此必须用 native legal $`A\to B,B\to A`$ 两次实际执行来判定。

---

## Provenance annex: 20261010 ordered-goal-defect transport

Complete source-specific linear support-function derivation, nonnormal counterexample, prior audit, implementation and DPT boundary. [Immutable source](https://github.com/Gogoal-L/math/blob/15b3fde162b2f7cb729ec106b847be1ad046d222/dpt_research/20261010_ordered_goal_defect_transport.md).

### 2026-10-10 frontier: command-ordered goal-error transport and information/computation allocation

**Scientific status:** exact elementary theorem for a supplied finite-dimensional linear switched model, with constructive synthetic tests; **DPT-native stage transport, nonlinearity envelopes, and physical admissibility NOT verified**. This note extends the already accepted DPT-R1 S09 results without updating its evidence or owner decisions.

**Source identity:** current upstream [OpenAI Math](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb) at fd4aeeb2, fork scientific baseline 2026-10-09 and 2026-10-10 [goal-information × solver-fidelity note](20261010_goal_information_solver_fidelity.md). Manuscripts are *preprints* and their proof patterns are not DPT theorems.

#### 1. What changed relative to the previous frontier?

The previous tools independently answer (i) whether an exact switched-linear model possesses a smaller **all-word autonomous goal quotient** (goal_word_quotient.py), (ii) how large a finite-bank observation/goal ambiguity remains (goal_ambiguity_audit.py), and (iii) whether a cheap implicit solve has a small **single-system goal-weighted residual**, conditionally on its Newton–Kantorovich envelopes (implicit_goal_certificate.py).

None of these three automatically determines **which initially hidden direction or which numerical defect at which stage will be magnified by an ordered A/B command and become the final goal error**. Eigenvalues of individual stage Jacobians are insufficient, while multiplying ambient operator norms may be needlessly conservative for a fixed VDS/J5 readout.

The new research object is a **goal- and command-word-specific transport of independently bounded information and computational defects**. The exact algebra is classical linear reachability/support-function mathematics. Its potential DPT contribution is a defensible, physical-input-specific answer to *where new information versus more accurate computation is actually needed*.

#### 2. Exact conditional finite-word result

Fix one known command word of length H and one **common, dimensionless/physically scaled state chart**, with known matrices A_0,...,A_{H-1} and scalar goal rows c_k:

```math
\delta x_{j+1}=A_j\delta x_j+\xi_j,\qquad
\delta g_k=c_k\delta x_k,\quad k=0,\ldots,H.
```

The admissible uncertainty set is explicitly the Cartesian product of Euclidean balls:

```math
\begin{aligned}
O\,\delta x_0&=0,\qquad
\|\delta x_0\|_2\le\rho,\\
\|\xi_j\|_2&\le\epsilon_j
\quad (j=0,\ldots,H-1).
\end{aligned}
```

The first condition is **exact observation equality**, not a claim about noisy sensors or a nonlinear reachable family. Let K=ker(O) and P_K be its orthogonal projector (in the declared physically scaled metric). Define backward goal rows

```math
q_{k,k}=c_k,\qquad q_{k,j}=q_{k,j+1}A_j \quad (j=k-1,\ldots,0).
```

**Proposition (elementary, independently derived).** For every endpoint k, under exactly the conditions above,

```math
\boxed{
\sup_{\delta x_0,\xi_0,\ldots,\xi_{k-1}} |\delta g_k|
=
\underbrace{\rho\,\|q_{k,0}P_K\|_2}_{\mathcal I_k:\;\text{hidden preparation information}}
+
\underbrace{\sum_{j=0}^{k-1}\epsilon_j\,\|q_{k,j+1}\|_2}_{\mathcal E_k:\;\text{stage defects}}.
}
```

For the worst endpoint in this **finite sampled stage set**, the sharp result is $`\max_{0\le k\le H}(\mathcal I_k+\mathcal E_k)`$.

**Proof.** Substitute the linear recurrence into the scalar readout:

```math
\delta g_k=q_{k,0}\delta x_0+\sum_{j<k}q_{k,j+1}\xi_j.
```

Since $`\delta x_0\in K`$, the initial term is bounded by $`\rho\|q_{k,0}P_K\|`$. Each independent Euclidean disturbance ball contributes its dual-norm support function $`\epsilon_j\|q_{k,j+1}\|`$. The sum is attained *simultaneously* by aligning each admissible vector with its corresponding backward row (and reversing all signs for the negative extreme). Thus the sum is **exact for the stated product-ball model**, not merely a triangle-inequality upper bound. The finite maximum commutes with the supremum over disturbances. QED.

This equality is generally **not sharp for actual DPT** if physical reachability, current-temperature coupling, KCL/KVL, source residuals, or event constraints couple/distort these uncertainty balls. If each actual disturbance belongs to the assumed ball, the calculated value is still an upper bound within the linear model; it is not a guarantee when A_k themselves are unvalidated local approximations.

##### Numerical witness and nonnormal counterexample

Set $`A=\begin{psmallmatrix}0.5&6\\0&0.5\end{psmallmatrix}`$, $`O=c=(1,0)`$, $`\rho=0.01`$, $`\epsilon_0=0`$. Both eigenvalues are 0.5, yet the initial hidden direction $`e_2`$ is invisible at k=0 and produces goal deviation 0.06 at k=1. Therefore the spectral-radius test misses a goal-visible transient gain. The new auditor constructs and replays this exact worst-case perturbation.

A second synthetic counterexample uses two noncommuting command matrices and gives a nonzero hidden-goal radius after A then B but zero after B then A. This is not an explanation of existing native AB/BA results; it establishes why order must remain literal in a valid goal-error calculation.

#### 3. New executable tool and relation to existing code

- [goal_defect_transport.py](../dpt_tools/goal_defect_transport.py): ordered matrix sequence, exact-observation nullspace, initial hidden radius, per-stage additive error radii and one scalar goal at each stage; computes $`\mathcal I_k`$, $`\mathcal E_k`$, total radius, worst stage, spectral/operator-norm context, and an explicit maximizing witness.
- [test_goal_defect_transport.py](../dpt_tools/test_goal_defect_transport.py): 11 synthetic/analytic tests, including independently enumerated scalar disturbances, nonnormal hidden leakage, command order, exact observation removal, stage-dependent readouts, invalid inputs and constructive witness validation.

The auditor **does not** infer $`\epsilon_j`$ from RAW, trust a local derivative outside its regime, infer instrument noise, or certify a nonlinear physical state. Input stages are stored in an NPZ with five arrays: updates (H,n,n), observation (m,n), goal (n,) or (H+1,n), initial_radius (scalar), defect_radii (H,). Its output status is a conditional model diagnostic. It is complementary to the all-word row-span quotient: the previous algorithm measures *how many hidden directions exist*, while this one measures *how strongly they matter for a given finite command word and goal*.

#### 4. OpenAI Math original-proof inspection: retained and rejected transfers

| Family and source | Exact paper object / proof feature examined | New DPT value | Transfer ceiling |
|---|---|---|---|
| **F325** [complete Crouzeix direct proof](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-direct-proof-of-the-complete-Crouzeix-inequality-September-26-2026/build/main.tex) | Numerical range and matrix-coefficient polynomial functional calculus; $`\|P[A]\|\le2\max_{z\in W(A)}\|P(z)\|`$, with fixed base operator A | Reinforces nonnormal growth and output-specific operator norm rather than eigenvalues; the new tool computes **literal ordered products and dual rows** | F325's constant 2 is **not** asserted for arbitrary products $`A_{k-1}\cdots A_0`$; our finite-word formula follows from elementary duality, not F325 |
| **F251** [October Strong Ulam stability](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Strong-Ulam-Stability-Characterizes-Amenability-October-5-2026/build/strong-ulam-stability.tex) | Main theorem characterizes when uniformly small composition defect of unitary maps on a **countable group**, in all Hilbert dimensions, can be corrected uniformly to an exact representation; nonamenable counterconstruction | Forces us to distinguish local composition error from global exact reduced command algebra | Physical DPT commands form a constrained partial switching semigroup, not the unitary group; do **not** transfer its amenability criterion or theorem |
| **F289** [near-inclusion obstruction](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Near-Inclusions-of-von-Neumann-Algebras-Without-Small-Spatial-Embeddings-October-5-2026/build/sections/obstruction.tex) | Clock/shift matrices almost commute but a trace-log winding invariant prevents nearby commuting unitaries; one-sided near inclusion need not yield near-identity spatial implementation | Warns against promoting near-zero observed closure residual to existence of a globally exact lift; provides a useful **structural counterexample template**, not a circuit mechanism | No identified unitary/topological obstruction in Eth has been shown |
| **F129** [one-way liveness state bound](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/build/sections/introduction.tex) | Context-separation through the relation monoid gives exponential deterministic-state costs for a *growing command alphabet* | Reinforces the idea that representational complexity depends on future contexts; check whether an apparently invisible DPT direction becomes visible in a later command | The exponential exponent and automata complexity do not apply to fixed finite DPT commands |
| **F363** [October local-conservation nonuniqueness](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Nonuniqueness-with-local-conservation-for-the-hard-sphere-Boltzmann-equation-October-5-2026/build/paper/01-introduction.tex) | Two renormalized kinetic solutions share data and exact local conserved moments while differing dynamically in a rough weak-solution class | Keep charge/energy balance, unique state evolution and goal prediction as separate scientific checks | Does not imply nonuniqueness of smooth finite-dimensional SiC ODE/DAE solutions |
| **F151** [C1 entropy counterexample](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-C1-Counterexample-to-the-Entropy-Conjecture-September-25-2026/build/source/entropy.tex) | Constructs an entropy-localization argument and counterexample at the exact C1/noninvertible regularity boundary | A reminder that orbit behavior cannot be inferred from a convenient partial invariant under weaker regularity | No immediate executable DPT transfer: **WATCH**, not a new workstream |

**Lean/verification scope as of fd4aeeb2:** [F325 scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/325.md) covers its numerical-range theorem. [F251 scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/251.md) belongs to its September unitarizability result, not the October Strong Ulam companion; [F289 scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/289.md) covers September two-sided stability, not the October near-inclusion counterexample. [F129 scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/129.md) includes one-way liveness; [F363 scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/363.md) covers the earlier periodic result, not October exact local-conservation refinement. We inspected specific cited theorem/proof sections and scopes; we did **not** reverify every manuscript's full proof.

**Closest prior art:** classical support functions and robust reachable sets (e.g., [Kurzhanski–Varaiya, SIAM JCO](https://doi.org/10.1137/S0363012903437605)), nonnormal matrix transient behavior (Trefethen–Embree, *Spectra and Pseudospectra*), DAE transient growth ([Embree–Keeler, SIAM](https://doi.org/10.1137/15M1055012)), and switched reduced-output error analysis ([Schulze–Unger, SIAM](https://doi.org/10.1137/18M1167887)). This is **not** a newly proven universal model-reduction theorem. The new executable object is specific coupling of already justified mathematical ingredients to the DPT research decision.

#### 5. DPT zero-fresh transfer contract and falsifiers

One useful, source-backed unit from the local controller would supply:

1. **Frozen same-law command identity and valid prefix:** command word, source branch, preparation/history ID, exact reference/query identity and goal (VDS/J5/fixed work/peak).
2. **A qualified common state chart:** actual Eth guard, correct local lift derivative, event-time derivative, and explicit mapping of each stage tangent into one physically scaled coordinate system. Without this, products of stage matrices can be dimensionally compatible and still meaningless.
3. **Observation O with acquisition identity:** source-only preparation information, existing prefix/Q summary, and separately accounted internal Tj. No post-target information in O.
4. **Validated radii, not guessed ones:** root uncertainty restricted to the actual physically reachable observation fiber; per-stage nonlinear/local-truncation/inexact-solver errors that are genuine bounds on the same declared branch and norm. If only point estimates are available, label outputs *SENSITIVITY_ONLY*.
5. **Goal row c at each stage:** derived from the same frozen readout, with moving-event/peak nonsmoothness treated appropriately. A whole-pulse peak is not automatically differentiable at a tied event.
6. **Prospective discriminator:** first compare the real archived stage errors against transport sensitivities and check if goal errors localize to the predicted stage/readout. Then, if material separation survives ordinary competitor predictions and source budgets, ask the controller about an authorized future native query.

The most decision-relevant outputs are:
- $`\mathcal I_k`$ large, $`\mathcal E_k`$ small: candidate need for legal extra information (e.g., a distinguishable goal-visible preparation direction). It does **not** prove which physical sensor is minimal.
- $`\mathcal I_k`$ small, $`\mathcal E_k`$ large: candidate need for tighter stage solver/finite law. Calculate real residual-based bounds before changing solver.
- Both small but observed native discrepancy large: wrong model class, unqualified transport, goal/event readout mismatch, or underestimated error budgets; reject the proposed certificate rather than claiming success.
- A command with nearly identical full/affine forecast yet small model differences is not a high-value discriminator merely because the stage matrices are nonnormal.

##### Strongest rejection risks

First, actual stage matrices may be **prefix-dependent** and linked through singular/ill-conditioned nonlinear DAE charts; the exact linear assumption might fail outside a narrow neighborhood. Second, physical histories may not fill the assumed Euclidean balls, so the equality is not sharp on the reachable set. Third, actual local residuals can be correlated across stages and may cancel in a signed goal, while the product-ball bound assumes independently adversarial directions. Fourth, physical measurement noise breaks exact observation equality. Fifth, full-law solver agreement is still model agreement, not hardware truth.

A **negative or inconclusive result is informative**: it identifies which claimed information/computation certificate requires a better physical state, branch, error envelope or goal functional, without reversing accepted S09 native positives.

#### 6. Practical next action

The main controller can perform a *zero-fresh* replay using already qualified Sol9 Eth tangent/lift and Sol10 TT-source / one-Newton material. Compare the source-residual direction and exact ordered goal transport before commissioning new LTspice. Do **not** treat this Math fork as scientific authority and do not update S09 freeze merely because a synthetic test passed.

**Status ledger:** paper-family proof-pattern inspection completed for F251, F289, F325, F129, F363, F151; **NEW mathematical tool:** one exact conditional finite-dimensional formula and constructive witness; **tests:** eleven isolated synthetic/analytic tests; **DPT-native verification:** pending independent evidence and owner adjudication.

## 2026-10-17 addendum: finite-message dynamic goal closure as a right-congruence test (D1)

**Scope (independent DPT finite automaton theorem).** Fix a finite legal set of *complete information histories* $`H`$ after source identity, pretarget PREP/CAL digital command, external raw observation and joint noise contract are declared. Future update tokens $`a`$ include the legal commanded intervention and any new **pretarget** observation that can be used before the next prediction; write the deterministic realized history extension as $`h\mapsto h a`$ wherever legal. A future word $`w`$ induces a set $`K(h,w)\subset\mathbb R`$ of physically allowed signed terminal-work goals (J), including declared model/error uncertainty. Fix nonnegative tolerances $`\tau_w`$ and a desired memory alphabet with at most $`2^M`$ symbols. To avoid the classical loophole that one decoder can remember the entire preceding transcript outside the claimed $`M`$ bits, demand a **deterministic autonomous** representation $`z=\pi(h)`$, update $`U(z,a)=\pi(ha)`$ and a goal decoder $`d(z,w)`$, all using only legitimate new tokens and the same frozen future-word/scorer contract. This formal statement does not assign a physical measurement cost to an abstract token or claim that the controller's full recorded command is absent.

**(D1) A finite state is sufficient if and only if the legal histories admit a right-congruent $`\tau`$-compatible partition.** Such an $`M`$-bit autonomous predictor exists precisely when there is a partition $`\{C_i\}_{i=1}^k`$ with $`k\le 2^M`$ satisfying (a) every token allowed to all histories in $`C_i`$ has successors in one common class, with the legality/guard domain represented consistently; (b) for every future word $`w`$, the union $`\bigcup_{h\in C_i}K(h,w)`$ is nonempty and has diameter at most $`2\tau_w`$. **Proof (necessity):** fibers of any deterministic $`\pi`$ are stable under allowed common update tokens, and a shared scalar decoder within $`\tau_w`$ of all goal values forces their union diameter $`\le2\tau_w`$. **Proof (sufficiency):** label each partition cell, advance to its uniquely determined next class, and predict the midpoint of the class's goal union. The bound is elementary scalar interval geometry. If the future word changes a guard/legality domain, that domain must be included in the represented output or the partition must split accordingly. No finite-bank partition ensures correctness on the unseen continuous source domain without a qualified coverage/remainder argument; the single-transcript conflict-graph chromatic number in P19–P22 is only a one-time message minimum and need not be an autonomous-update minimum.

**Exact two-stage counterexample, status synthetic.** Let the hidden prepared bit be $`h\in\{-1,+1\}`$ and an internal flag $`f\in\{0,1\}`$ initially $`0`$. The lawful abstract command $`A`$ sets $`f=1`$ and reveals no $`h`$; command $`B`$ produces zero signed goal when $`f=0`$, but produces signed goal $`h`$ when $`f=1`$. All pretarget raw/digital observations are equal across the two hidden histories by construction, and an $`A`$-only or $`B`$-only goal test sees no difference; the ordered word $`AB`$ yields goals $`-1,+1`$ (dimensionless scaled J), so any shared predictor incurs error at least $`1`$ for $`\tau<1`$. A full-record ordinary that actually distinguishes $`h`$ is a strictly stronger information condition and predicts both; no source-law SiC two-world is asserted. More economical state messages need be compared at equal pretarget information and memory/replay cost. A physically legal update also needs branch/guard/moving-event time and *same* complete source continuation across stages, rather than a formal letter sequence.

**Original-paper boundaries.** F229, *Exact reconstruction threshold for the three-state symmetric channel*, Theorem 1.1 (original PDF p.3), Proposition 2.3 (p.8) and §6 (pp.27–33) assume an independent broadcast tree / channel eigenvalue threshold; its finite experiment is allowed to reveal hidden spin in a comparison, which is not a legal DPT sensor. F376-A, *Finite Instructions and Solenoidal Shear Flows*, Lemma 2.1 (p.3), Theorem 3.2 (p.6), and F376-B, *Incompressible Box Transport and Finite Computation*, Theorems 3.4 (p.10) and 4.1 (p.12), concern deterministic full-information incompressible flow constructions, not robust finite-bit DPT memory. F129's relation monoid/full alphabet state count is not a bound on our fixed few physical commands. We borrow the questions of whether information is recorded and can be autonomously updated; D1 is independently proved, not a corollary of those theorems. Candidate Main evidence: one **same S150 source**, qualified full pretarget recorded command/CAL and joint noise, a pair of source-reachable histories, a **predeclared ordered two-stage future command** and post-$`A`$ permissible observation, fixed work scoring. If the pair is still full-CAL compatible after $`A`$ but $`AB`$ goal gap exceeds $`2\tau`$, autonomous-state sufficiency fails; if post-$`A`$ observation separates the pair, that is a legal sensor repair candidate, subject to same-information full-record ordinary.

## 2026-10-17 D2: continuous-command goal pseudometric, guarded finite-memory tubes and passive two-branch counterexample

**Independent strengthening of finite-alphabet D1.** Fix a single complete source-law/PREP reference, a finite future horizon $T$, all admissible continuous (or piecewise-continuous) future digital/analogue commands, full recorded pretarget external CAL, a **joint persistent** nuisance/error trajectory, and the terminal current/voltage identity. A source-history state $x$ is augmented with all live preparation/DAE/filter/guard memory required to define future continuous signed terminal power $p_x^w(t)=V_{\rm term}^w(t)I_{\rm term,x}^w(t)$. For histories sharing the same legal future word set and compatible event labels/guard timing, define
```math
d_T(x,x')=\sup_{\substack{w\text{ legal for both}\\|w|\le T}}
\int_0^{|w|}|p_x^w(t)-p_{x'}^w(t)|\,dt\quad[\mathrm J].

```
If branch legality/event identity differs in a way the scorer cannot align, report $+\infty$ / ABSTAIN rather than force a false quotient. On one legal domain $d_T$ is a **pseudometric** (zero can identify physically distinct states) and dominates $|W_w(x)-W_w(x')|$ for each future word. For every common legal command prefix $a$ of duration $h$ and compatible disturbance continuation,
```math
d_{T-h}(\Phi_a x,\Phi_a x')\le d_T(x,x').
```
**Proof:** triangle inequality holds after taking each signed-power absolute value and supremum. Each suffix $w$ of the updated states corresponds to the original concatenated word $aw$; the integral of *absolute* power mismatch along the suffix is at most its value over the full prefix-plus-suffix because the prefix contribution is nonnegative. Supremize over suffixes. The absolute signed-work *difference alone*, without absolute power *inside the time integral*, can have cancellation between prefix and suffix and need not satisfy this right-congruence inequality. This exact behavioral distance is not automatically computable or bounded by finitely many source simulations; a DAE guard mismatch destroys the certified domain.

**(D2-b) A conditional constructive finite-bit streaming tube.** For a compact actual-source and joint-nuisance augmented history set, suppose a finite cover of at most $`N`$ cells $`C_i`$ of diameter $`\rho`$ in a stated dimensionless state metric, every legal hybrid transition has **qualified complete** guard/consistency propagation, and the source-validated same-input transition map is $`\kappa`$-incrementally contractive $`\|\Phi_a x-\Phi_a x'\|\le\kappa\|x-x'\|`$ for each allowed segment, $`\kappa\le1`$. Let a sound directed OUTER reachability operator $`\widehat\Phi_a(B)`$ contain **all** legal true successors of $`B`$, with extra overhang from its exact image at most $`\beta`$ in the same norm. Represent the compatible histories as a length-$`N`$ cell mask (cost $`N`$ bits plus clock/mode/command metadata), propagate **all** possible successor cells, and intersect only with the *same* temporally joint nuisance-feasible new pretarget observation. If $`D_k`$ denotes diameter of the selected union, the conservative recurrence is
```math
D_{k+1}\le\kappa D_k+2(\rho+\beta).
```
Proof: each survivor lies within $\rho+\beta$ of a truly reachable predecessor state; insert two such nearby witnesses and use the incremental gain. Joint measurement intersection can only reduce diameter if the augmented latent error state is carried consistently. Iteration gives $D_k\le\kappa^kD_0+2(\rho+\beta)(1-\kappa^k)/(1-\kappa)$ for $\kappa<1$, otherwise $D_k\le D_0+2k(\rho+\beta)$. If every frozen source-legal future signed goal obeys a **validated** $L_G$-Lipschitz bound with a separate solver/scorer remainder $\epsilon_G$ J, the midpoint error is bounded by $L_GD_k/2+\epsilon_G$, enabling a conditional $\tau$-adequate decision or ABSTAIN. This is a sufficient **all-source** contract, not a claim that $N$ is economical or that S150 has a certified $\kappa$, invariant augmented set or global DAE branch.

**A physically interpretable exact positive and stronger failure than the D1 flag toy.** Take an ideal port capacitor $C_0>0$ in parallel with two passive identical R–L branches, driven by the same terminal voltage $u(t)$, with $R,L>0$. Let $s=i_1+i_2$, hidden differential $d=i_1-i_2$. The full port measurement is $I=C_0\dot u+s$. For **all continuous legal common voltage words** with unchanged symmetric branches,
```math
\dot s=(2u-Rs)/L,\qquad \dot d=-Rd/L.
```
Thus $`s`$ alone is an exact autonomous goal state for every future external signed work $`\int u(C_0\dot u+s)dt`$ in this *symmetry-preserving* command class; nonzero hidden $`d`$ is behaviorally irrelevant even if it has not been recovered. Moreover $`|s_u(t)-s'_v(t)|\le e^{-Rt/L}|\Delta s_0|+(2/R)(1-e^{-Rt/L})\|u-v\|_\infty`$. On equal voltage samples a scalar quantizer mesh $`\rho`$ updates with contraction $`e^{-Rh/L}`$ and quantization recurrence $`r_{k+1}\le e^{-Rh/L}r_k+\rho/2`$, conditional on a source-certified initialization from the **full** joint-CAL record.

If the **future legal action alphabet is enlarged** to a branch-1-only finite inductance intervention $L\mapsto L+\delta$ with $\delta>0$, and the initial hidden splits $i_1=(s\pm a)/2,\ i_2=(s\mp a)/2$ are both source-legal under identical complete recorded PREP and full port CAL, the quotient breaks. Assume flux continuity at the change, $(L+\delta)i_1(0+)=Li_1(0-)$ (account for external actuator energy separately); drive with common constant $u=U$ for time $T$. Direct linear solution yields a **signed external work gap**
```math
|\Delta W|=\frac{|Ua|L}{R}
\left[e^{-RT/(L+\delta)}-e^{-RT/L}\right]>0.
```
Hence any same full-port record-only scalar decoder for this *new* action class has minimax error at least $`|\Delta W|/2`$; a full true-state oracle knows $`d`$ but purchases extra hidden information and is not an ordinary at equal budget. Synthetic values $`L=5`$nH, $`\delta=0.2`$nH, $`R=0.1\Omega`$, $`U=150`$V, $`a=1`$A, $`T=10`$ns give approximately $`47.416604269`$ nJ difference (never an actual S150 number). If documented PREP forces $`d=0`$, the branch-specific $`\delta`$ is not a legal DPT intervention, or guard/flux-reset physics is different, the counterexample is **inapplicable**, not evidence for actual hidden memory. A legal zero-input dwell before the intervention shrinks $`|d|`$ by $`e^{-Rt_p/L}`$; with no other errors a $`\tau`$-goal requirement can be repaired without new sensor only when
```math
t_p\ge(L/R)\max\{0,\log(|\Delta W_0|/(2\tau))\},
```
provided the changed preparation remains legal and its time cost is included. Any independent residual work bound must reduce the remaining $\tau$ budget first. Alternative genuine branch current/flux measurement costs are separate; an N100 third observed voltage is not silently such a sensor.

**Primary literature, correctly limited.** Willems, “Dissipative Dynamical Systems Part I” (1972), §2 pp.323–327, motivates equivalence by **all future behavior**; van der Schaft, “Bisimulation of Dynamical Systems,” HSCC (2004), Definition 1 p.4 and Definition 4 p.12 require matching inputs/outputs and hybrid event occurrence, not merely a common point Jacobian. Pola, Girard & Tabuada, “Approximately Bisimilar Symbolic Models for Nonlinear Control Systems,” [arXiv:0706.0246](https://arxiv.org/abs/0706.0246), Theorems 4.1 (PDF p.6) and 5.1 (p.9), assume smooth δ-GAS/δ-ISS systems with explicit incremental bounds and quantized inputs; they do not establish switched electrothermal DAE root/guard or persistent-noise qualification. Hermann–Krener (1977) Theorem 3.1 is a local smooth observability-rank result, not global external-inverse sufficiency; F229/F376 finite-tree/real-flow construction assumptions are different. D2 is a **project-owned** sufficient construction plus passive-law comparator, not a literature theorem transplanted to SiC. The smallest Main decision-changing observation remains source-qualified **same digital PREP + full raw CAL/joint noise** hidden pair or certified same-source goal tube under a frozen lawful finite $`\Delta L`$ word, alongside the strongest full-record ordinary. **Status SIDE_VERIFIED mathematics / actual physical new-word closure OPEN.**

## 2026-10-18 D3: actual-type electrothermal feedback invalidates a tempting scalar BE-memory shortcut

**Specific active S150 source question, not a reproof of D2.** Local controller derivations README (2026-10-17, lines 133–137) accepts strict positive diode charge $z=I_s\exp(v_j/V_T)$ and a *fixed electrical and thermal forcing* scalar BE response with old-charge gain below $\tau/(\tau+h)$. This is a legitimate partial one-dimensional fact for fixed $g,d,T$, not a bound on the fully coupled 50-state electrothermal response when electrical current and heat change together. Original S-L8 all-root energy envelopes do not imply incremental contraction of the DAE update.

**D3 source-type passive electrothermal counterexample (fully analytic synthetic circuit, not S150).** Consider a driven positive-current diode with state $x=(i,v,z,T)$, supply $V_s$, series $L,R_s>0$, shunt $C>0$, stored diffusion charge $\tau z$, diode series resistance $r>0$, and thermal $C_{\rm th},H>0$:
```math
\begin{aligned}
L\dot i&=V_s-R_s i-v,& C\dot v&=i-j,\\
\tau\dot z&=j-z,&
C_{\rm th}\dot T&=v_j z+rj^2-H(T-T_a),\\
j&=(v-v_j)/r,&
v_j&=V_T\log(z/I_s)-\alpha V_T(T-T_a).
\end{aligned}
```
In the forward guard $i,j,z>0$ and $v_j>0$, heat production $v_j z+rj^2\ge0$. For **fixed $v,T$** implicit BE gives
```math
v_j(z_+,T)+r[(1+\tau/h)z_+-(\tau/h)z_{\rm old}]=v,
```
whose monotone-root old-charge derivative is
```math
\frac{\partial z_+}{\partial z_{\rm old}}
=\frac{r\tau/h}{V_T/z_++r(1+\tau/h)}
\in(0,\tau/(\tau+h)).
```
Nevertheless choose $z_\ast=i_\ast=j_\ast=10\mathrm A,\ v_\ast=1.5\mathrm V,\ T_\ast=225^\circ\mathrm C,\ T_a=25^\circ\mathrm C,\ V_T=0.05\mathrm V,\ \alpha=0.08/\mathrm K,\ r=0.06\Omega,\ R_s=0.001\Omega,\ H=0.075\mathrm{W/K},\ I_s=10e^{-34}\mathrm A,\ V_s=1.51\mathrm V$. Then $v_j=0.9\mathrm V$, recombination heat $9\mathrm W$, resistor heat $6\mathrm W$ and cooling $15\mathrm W$: a physically sign-consistent equilibrium. Define $q=V_T/z_\ast=0.005\Omega$, $a=\alpha V_T=0.004\mathrm{V/K}$, let $F=M f$ denote the four unscaled right-hand sides and $M=\mathrm{diag}(L,C,\tau,C_{\rm th})>0$. Direct differentiation and elimination give
```math
\begin{gathered}\det D_xF=\frac{H(R_s+r+q)-a(v_\ast-R_s z_\ast)}r\\=\frac{0.00495-0.00596}{0.06}\\=-0.0168333333\ldots<0\end{gathered}
```
As $\det Df=\det DF/\det M<0$ in **even dimension 4**, the characteristic polynomial $\det(\lambda I-Df)$ is negative at $\lambda=0$ and positive for sufficiently large positive $\lambda$; it has a real $\lambda_+>0$. For any sufficiently small positive BE step $h<1/\lambda_+$ with local implicit solvability, $D\Phi_h=(I-hDf)^{-1}$ has eigenvalue $1/(1-h\lambda_+)>1$. A positive local diode scalar storage-memory derivative therefore coexists with a growing **full coupled** mode; no source-wide $\kappa<1$ or stable signed future work follows from the one-dimensional inequality. This is a valid **negative inference test**, not a finding that the real S150 source is unstable, and it does not prove any actual full-CAL observation alias.

**(D3) Constructive alternative that tests the full source rather than scalar z.** On one convex, guard-invariant, completely source-consistent smooth BE region with *all* algebraic constraints eliminated via a separately verified regular index-one Schur map, suppose one common $`P\succ0`$ and $`\mu>0`$ satisfy
```math
J(x,u,\theta)^\top P+P\,J(x,u,\theta)\preceq-2\mu P
```
for the **FULL electrical, charge, thermal and memory-coupled** vector field Jacobian $`J=D_xf`$ along every segment, and source parameter perturbations obey $`\|f(x,u,\theta)-f(x,u,\theta')\|_P\le b\|\theta-\theta'\|`$. Subtract two same-input BE equations, pair with $`\Delta x_+`$ in the $`P`$-inner product and use the secant Jacobian: 
```math
\|\Delta x_+\|_P\le
\frac{\|\Delta x_{\rm old}\|_P+h b\|\Delta\theta\|}{1+h\mu}.
```
This may support an ordered finite signed-work goal tube after separately bounding $`|D_x(VI)|`$, actual charge/GL32 quadrature, shared PREP and filter states, jump consistency and transversality. A passive energy storage, diagonal partial diode memory, *point* Jacobian eigenvalues, or a generic barrier does NOT substitute for the full $`P`$-inequality. If the future command is a **feedback policy** $`u=\pi(H(x,\xi))`$ rather than a precommitted identical open-loop word, the required full Jacobian is $`J_{\rm closed}=f_x+f_u D\pi\,H_x`$ with the persistent joint sensor nuisance $`\xi`$ carried as a single *unchanging latent*; never assign $`\xi`$ fictitious strict contraction or fresh iid error. Threshold feedback requires mode/saltation checks; if worlds take different future legal command branches, same-input estimate does not compare them automatically.

**Original theorem/proof boundaries.** Lohmiller & Slotine, “On Contraction Analysis for Non-linear Systems” (Automatica 1998), [author manuscript](https://www.mit.edu/~nsl/preprints/contraction.pdf) Definition 1/Theorem 1, original PDF p4, requires uniformly negative full symmetric Jacobian part on a source-invariant region. Forni & Sepulchre, “A Differential Lyapunov Framework for Contraction Analysis” [arXiv:1208.2943v4](https://arxiv.org/abs/1208.2943), Theorem 1 PDF p4 and quadratic full $P$-LMI (29)–(30) p8, assumes smooth forward-complete incremental tangent dynamics; not a switched 50-state DAE theorem. Forni, Sepulchre & van der Schaft, “On Differential Passivity of Physical Systems” [arXiv:1309.2558](https://arxiv.org/abs/1309.2558), Theorems 1–2 PDF p3 require both connected subsystems to be differentially passive for negative-feedback preservation. Maghenem & Sanfelice (2021) Theorem 1 PDF p5 proves conditional hybrid forward pre-invariance, not contraction; Kong et al. [arXiv:2306.06862](https://arxiv.org/abs/2306.06862), Definition 2/Eq.(9) PDF p6, requires transverse guards and proper saltation derivative. D3's discrete inequality and electrothermal toy are **independently derived** here, not transplanted SiC confirmations.

**Controller decision:** The correct smallest zero-new-native discriminator is the archived same-source **full** electrical/thermal source Schur Jacobian over a legal PREP+CAL+unseen future stage, with qualified root/guard/mode domain and coupled signed terminal-work derivative, not another fixed-forcing scalar z test. If a full incremental $P$ or source-validated goal-only contraction exists, use it to narrow compatible future signed-work; if not, retain S-L7/P38 actual-source interval alternatives. S150 actual all-root/closed-loop/J bounds remain OPEN, historic whole-fork q>1 remains PARK, and a positive eigenvalue in this SYNTHETIC example is not a native-run authorization.

## 2026-10-18 D4: finite-command signed-work Bellman super/subsolutions (distinct positive closure strategy)

**Sufficient theorem.** Let the full recorded PREP command, all 4801-point CAL and **one joint persistent error law** define the nonempty all-source-compatible set $C_0$ of prepared physical/filter states. Freeze a source-legal *future* finite $\Delta L$ intervention, actual command policy (including feedback branches if any), original 50-state BE/diode/thermal/GL32/guards, reset/consistent flux contract and the original fixed **841-point trapezoidal signed port work**. For a finite future horizon, denote by $x\to x'$ **every** source-legal stage or event/reset transition and by $g_n(x,x')$ the exactly matched signed trapezoidal VI increment (including event work when present). If stage functions $D_n,U_n$ satisfy $D_N\le0\le U_N$ and, for *every* admissible transition,
```math
\begin{gathered}
D_n(x)\le g_n(x,x')+D_{n+1}(x'),\\
g_n(x,x')+U_{n+1}(x')\le U_n(x),
\end{gathered}
```
then simple telescoping gives **every** compatible future work $G$ in $[\inf_{C_0}D_0,\sup_{C_0}U_0]$. This construction neither assumes a global inverse/root uniqueness, all-state contraction, nor a preselected five-current decoder; unlike P42 it bounds one future trajectory at a time. Source-root/guard coverage and nonemptiness of $C_0$ are nevertheless mandatory, so a candidate with only selected root trajectories cannot certify actual S150. A fixed finite $\Delta L$ after CAL is legal only if the source reference supports this physical intervention with correct flux/actuation work; do not silently reinterpret a parameter frozen during PREP as an allowed switch.

**Independent positive toy and limits.** An analytic **non-S150** 3-stage electrothermal BE series circuit with $`h=0.1`$ ns, $`U=2`$ V, $`R=1`$ ohm, $`L=1.2`$ nH, current zero at intervention and $`v_D=0.05\log(1+i)-10^{-4}(T-T_a)`$ V has positive monotone current root each step and $`T-T_a<0.123`$ C. Bounding $`0<v_D<0.055`$ V gives monotone lower/upper BE current updates and a literal **trapezoidal** work interval $`[0.1289879380974,0.1326354119254]`$ nJ for the three steps; a separate bisection source-toy calculation yields $`0.1319516108282121`$ nJ strictly inside. The interface is a true one-step directed Bellman test, not a claim of S150 future adequacy. The strongest same-information ordinary is still the full legal goal-fiber interval midpoint; Bellman can only make its proof more computationally economical. To change Main's decision without native, reuse a saved lawful pair $`x_{\rm old},x_{\rm new}`$, mode and original signed VI stage scorer (e.g. target6846 row41 vicinity) to falsify a proposed Bellman inequality; a positive result requires all-branch interval/stage qualification across the full pretarget-compatible set. Serban & Recuero, [*Sensitivity Analysis for Hybrid Systems and Systems with Memory*](https://arxiv.org/abs/1904.08734) (2019), original §4.2 Eq.(29)–(38), Algorithm 1, describes explicit last-event-memory adjoint terms; those are **already accounted for** when complete Markov memory is truly included in the full stacked S150 BE state, and cannot be invoked as an automatic missing physical correction. Status **SIDE_VERIFIED analytic conditional theorem/toy; actual finite-$`\Delta L`$ source goal OPEN**; regression in [existing falsifiers](../dpt_tools/test_paper_transfer_falsifiers.py).



## 2026-10-18 D5: actual S150 two-coil signed-work BE gate and finite-DeltaL legality

The ORIGINAL S150 source, nonprotected ZIP analysis/actual_law.py L174–202,235–240,276–295, fixes external L_s=4.3 nH at coil index10 (i_s=y[36]) and bus L_D=100 microH at index11 (i_D=y[37]). Their exact source rows are r36=-v_sl+L_s*delta(i_s)/h, r37=-v_D+150+L_D*delta(i_D)/h. The original external signed-port power is p=(v_D-v_sl)i_s (pro18c_replay.py L25,69–74). With E_s=L_s*i_s^2/2, at ANY candidate BE state pair (including nonzero residuals) the following **source-specific correlation-preserving identity** holds:
```math
\begin{gathered}
h p+\Delta E_s
=150h\,i_s+L_D i_s\Delta i_D\\
-\tfrac12 L_s(\Delta i_s)^2
+h(r_{36}-r_{37})i_s.
\end{gathered}
```
Every genuine original fixed-L exact source root satisfies h*p+delta E_s<=150h*i_s+L_D*i_s*delta(i_D), since the omitted BE dissipation is nonnegative; neither signed power nor i_s can be assumed positive. This is an actual one-step **Bellman super-solution component** requiring a *joint/correlated* interval for i_s*delta(i_D), not a full 50D trajectory or final 841-point work bound. The frozen original scorer first piecewise-linearly resamples external VI on 841 future times and then trapezoid-integrates; the signed quadrature correction W_H - sum(h*p) is a separate indispensable proof obligation.

Archived nonprotected law_known_answers.npz::source150_old,state,residual demonstrates one actual first-PREP step with h*p=-9.937727701017668 pJ, 150h*i_s=-9.648757442729671 pJ, bus cross term=-0.2883813507132653 pJ, delta E_s=+0.000549618245033 pJ and BE decrement=0.000039289312369 pJ; source coil residuals r36~-6.94e-18 V and r37~-2.694e-10 V. [Exact Fraction regression](../dpt_tools/test_paper_transfer_falsifiers.py) reconstructs the identity from **archived decimal input**, without new native simulation.

**Critical legality obstruction to unqualified future-DeltaL promises:** the accepted source constructor freezes L_s before PREP and reuses it for CAL and future; no source-valid post-CAL L change, flux reset, jump energy or actuator API is specified. If one proposes flux-consistent BE for variable L, blind replacement of L_old with L_new in the fixed-L current equation omits (delta L)*i_old/h. At the same saved PREP state and hypothetical +0.2 nH, this omission is -2.76550409 mV, ~92,183 times the published ~3e-8 V coil tolerance. That is a **negative control of naive equation substitution**, not an actual legal finite-DeltaL two-world example or proof no physical actuator exists. A future goal interval is still OPEN until Main qualifies an actual intervention/guard/flux and mechanical-energy ledger; the strongest ordinary uses all 4801 pretarget V/I, recorded command, joint sensor law and legitimate fixed scorer. Static L variants each with their own lawful PREP remain permissible.


## 2026-10-18 D6: exact source BE-to-frozen-H signed work bridge (one real 84-ns S150 source path)

**Separate the three work objects.** In original Pro18C ZIP::pro18c_replay.py L25,66–74, the source step port is V=y0-y1 [V], I=y36 [A]. The frozen score interpolates EACH port separately from the source BE grid to fixed H(841) before trapezoidal VI integration. It is neither source fine-grid BE right-endpoint work nor the continuous product integral of coarse H-linearized ports. For a frozen H node in fine BE cell [t_j,t_j+1], alpha=(H_k-t_j)/(t_j+1-t_j), exact algebra gives:
```math
\begin{gathered}
P(H_k)=(1-\alpha)P_j+\alpha P_{j+1}\\
-\alpha(1-\alpha)(V_{j+1}-V_j)(I_{j+1}-I_j),\\
Q_H=\sum_k\omega_kP(H_k)
-\sum_j h_jP_{j+1}.
\end{gathered}
```
Here P_j=V_j I_j and omega_k are exact trapezoid H weights; the second line is an explicitly **signed** source-to-scorer correction. The interval widths/overlap, two-channel covariance and source history must remain coupled: a per-block absolute upper can be orders of magnitude looser. For a purely H-piecewise-linear port interpolation, a DIFFERENT exact identity is W_H - integral V_HPL I_HPL = sum DeltaH*DeltaV*DeltaI/6; this is not Q_H.

**New archived original S150 numerical evaluation, without source solver/native.** Allowed analysis/acceptance/pro18c_prediction_extension.npz SHA256 af7299434d7dcde687da3bf56b5ce31babbc4e0c1c0e12b1a849b5f5530ae8fd supplies target_t(6721),target_y(6721x50),target_H(841),target_ports(841x2) at distinct original-source query a=(.23,.37,.23) V, static L=4.16 nH, kappa=1.009, b=95 MHz (do NOT splice into historical centered q row9/41). Source QA reports 6720 accepted numerical steps. Rebuilding both portfolios gives W_H=1.1161291889185969e-05 J and W_BE,right=1.1161314481383648e-05 J; signed Q_H **=-2.259219767949234e-11 J = -0.02259219767949234 nJ**. Two different decompositions check the sign: W_H−fine-BE-trap=+0.00130350318010 nJ, fine-BE-trap−BE-right=−0.0238957008596 nJ; exact coarse-H product correction alone would be +0.26001725265 nJ, nearly canceled by fine-to-coarse PL remapping of −0.25465011624 nJ. Archived H[841] matches t[0,8,...,6720] within 8.5e-22 s. An outward IEEE64 arithmetic-only error receipt <2.56e-7 nJ supports the **stored-number interval** Q_H in [-0.022593,-0.022591] nJ; this excludes neither source solver/truncation nor another compatible future. Signed per-H-block terms have sum absolute 21.47816498 nJ versus net .0225922 nJ: an independent-block unsigned error budget destroys cancellation.

One candidate's stored Q_H is a **RETROSPECTIVE actual-source-point scorer correction**, NOT a prospective all-source Q_H interval. For any source-compatible trajectory set C, the D5 future Bellman upper and lower can be transferred only after validating sup/inf of the joint expression Q_H(C) with common old-state, guards, BE voltages/currents and the original future scorer. The stronger same-information full-record ordinary can use this identical exact scorer. The model still defines only static-L own-PREP branches; post-CAL finite DeltaL requires a new physical flux/reset/actuator-work contract, not numerical coefficient substitution. Reference: [source-row D5 identity](#2026-10-18-d5-actual-s150-two-coil-signed-work-be-gate-and-finite-deltal-legality), [existing work regression](../dpt_tools/test_paper_transfer_falsifiers.py).


## 2026-10-18 D7: source-coupled two-copy frozen scorer and 50D coil-residual support

**New exact conditional family form, not a certified future fiber.** Let A be the actual H841-by-source-time(6721) piecewise-linear sampling matrix, Omega the H trapezoid diagonal in seconds, and D the source BE-right diagonal diag(0,h1,...,h6720) in seconds. For a *single common source time grid and frozen H* define K=A^T Omega A-D, so the real-valued binary-grid scorer correction is Q_H(V,I)=V^T K I [J]. Unlike treating the coarse H grid as a new continuum, K retains tiny off-diagonal interpolation weights when H differs from source t[8k] by binary64 rounding. For any TWO putatively legal future paths a,b on that SAME t/H grid, polarize exactly:
```math
\begin{gathered}
Q_H^a-Q_H^b=
(V_a-V_b)^T K\,\overline I
+\overline V^T K\,(I_a-I_b),\\
\overline I=(I_a+I_b)/2,\qquad
\overline V=(V_a+V_b)/2 .
\end{gathered}
```
There is NO independent delta-V times delta-I term in this centered two-copy difference. This exact identity can be optimized by a P42 two-copy objective bound **only after** a correlated, root- and history-qualified source-compatible current/voltage relation has been supplied. No all-source set is presently enclosed.

**Actual two-coil BE source rows turn Q into a goal-only current/residual form.** Original actual_law.py L200–202,235–240,276–295 gives r36=-vsl+Ls Delta I/h and r37=-vD+150+LD Delta j/h, where j=state[37], Ls static per own PREP, LD=100 microH and V=vD-vsl. For w=K I, exact algebra at ANY candidate BE stage pair is:
```math
\begin{gathered}
Q_H=w_0V_0+150\sum_{n\ge1}w_n
-L_s\sum_{n\ge1}\frac{w_n\Delta I_n}{h_n}\\
+L_D\sum_{n\ge1}\frac{w_n\Delta j_n}{h_n}
+\sum_{n\ge1}w_n(r_{36,n}-r_{37,n}).
\end{gathered}
```
This preserves the same stored source current path, bus/load cancellation, and correlated residuals. In particular, if the *full* I and j paths are FIXED and each source coil voltage residual independently belongs to [-eps,eps] V, the residual contribution is a signed support interval of radius 2 eps sum_{n>=1}|w_n| [J]. This is sharp for the declared rectangular residual set, not a root/continuous-source/error guarantee.

**Named actual S150 numerical receipt.** Nonprotected analysis/acceptance/pro18c_prediction_extension.npz SHA256 af7299434d7dcde687da3bf56b5ce31babbc4e0c1c0e12b1a849b5f5530ae8fd supplies target6721x50 and H841 with a=(.23,.37,.23)V, static Ls=4.16nH, kappa1.009, b95MHz. Fresh independent original-array recomputation yields Q_H≈−0.02259219766 nJ, with signed source-coil terms in nJ: initial +.0038003812478, bus −4.850786424625, external coil +.003221094127, load coil +4.821172735126, residual +1.64636e−8. Source-row closure <1e−12 nJ; max |r36-r37|≈3.55212e−9 V. Here sum_{n>=1}|w_n|≈5.52286436823e−7 A s, so under independently supplied **hypothetical** |r36|,|r37|<=3e−8V, the FIXED-path Q_H coil-substitution interval centered near −0.02259221413 nJ has radius **3.313718621e−5 nJ**, approximately [−0.02262535131,−0.02255907694] nJ. A 0.000033nJ residual allowance must NOT be advertised as complete nonlinear BE/source discretization error, and a single stored current path cannot bound the whole original Goal27 source-compatible future fiber. [Reusable coefficient-based API](../dpt_tools/goal_defect_transport.py) and [regressions](../dpt_tools/test_goal_defect_transport.py) preserve the original scorer.

**Fixed-L/source-law limitation.** The source does not define post-CAL L switching or flux reset; only a fixed L chosen before its own-PREP and reused by CAL/future can enter the above equalities. The strong same-information ordinary consumes all original legal PREP/full V-I CAL and uses exactly K; no five-sample comparison, direct future-label feed, or broken history handoff is allowed.


## 2026-10-18 D8: source-flux coupled FAMILY bounds for frozen signed work

**An actual-source goal-only norm relation, conditional on a jointly legal future fiber.** Let A be the frozen H841-by-source6721 piecewise-linear sampling matrix, Ω its H trapezoidal time weights [s], D=diag(0,h1,...,h6720) [s], G=AᵀΩA and K=G−D. Original signed terminal work W_H=VᵀGs and D7 BE-right correction Q_H=VᵀKs. The frozen fixed-L original coil BE source rows actual_law.py L200–202,235–240,276–295 give r36=−vsl+Ls Δs/h and r37=−vD+150+LD Δj/h; define physical flux φ=LD j−Ls s [Wb], r=r36−r37. On each fine BE step j>=1, V_j=150+Δφ_j/h_j+r_j.

For any TWO source-legal futures on the SAME grid and with the SAME PREPARED starting s0,V0, set x_j=Δs_j [A], q_j=Δ(φ_j−φ_{j−1})/h_j [V], e_j=Δr_j [V] and x0=ΔV0=0. For either E=G (frozen full work) or E=K (D7 signed correction), exact polarization around the first path gives
```math
\Delta(V^\top E s)=(EV)_{1:}^\top x+(Es)_{1:}^\top(q+e)
+x^\top E_{1:,1:}(q+e).
```
With T=diag(h1,...,h6720), let Rs=||T^{1/2}x|| [A sqrt(s)], Rphi=||T^{1/2}q|| [V sqrt(s)], Rr=||T^{1/2}e|| [V sqrt(s)]. Define Cs=||T^{-1/2}(EV)_{1:}|| [V sqrt(s)], Cphi=||T^{-1/2}(Es)_{1:}|| [A sqrt(s)] and sigma=||T^{-1/2}E_{1:,1:}T^{-1/2}||. Then this **joint goal-family** bound follows by weighted Cauchy-Schwarz and spectral norm:
```math
|\Delta G_E|\le C_s R_s+C_\phi(R_\phi+R_r)
+\sigma R_s(R_\phi+R_r).
```
The radii are JOINT correlated temporal source uncertainty, not per-sample boxes. This inequality is not yet an ACTUAL Goal27 full-CAL diameter until each radius is bounded for every legal guarded same-information future world. Different own-PREP fixed-L worlds require explicit starting-endpoint terms instead of x0=ΔV0=0.

**New directed stored-binary64 real-lift coefficient receipt.** Nonprotected acceptance/pro18c_prediction_extension.npz SHA256 af7299434d7dcde687da3bf56b5ce31babbc4e0c1c0e12b1a849b5f5530ae8fd provides actual 84ns/H841 t6721/V=x0−x1/s=x36/j=x37, query (.23,.37,.23)V,Ls4.16nH,LD100microH. Independent exact Fraction evaluation reconstructs A,Ω,G,K on the saved grids; every nonnegative weighted sum term is rational outward CEILED to 1e−19 and the Gershgorin bound uses exact rational 1/sqrt(h_i*h_j)≤(1/h_i+1/h_j)/2. Strict STORED-VALUE upper bounds, not solver/domain error certificates:

| Goal matrix | Cs [V sqrt(s)] | Cphi [A sqrt(s)] | sigma [dimensionless] |
|---|---:|---:|---:|
| G for frozen W_H | <0.084797 | <0.004130 | <8.000001 |
| K for signed Q_H | <0.079327 | <0.003864 | <7.000001 |

Fresh floating diagnostics respectively (0.0847967522634,0.0041298213837,8.0000000005082) and (0.0793266786565,0.0038630291613,7.0000000005082). Source flux endpoint check phi0≈−0.0005192794483166381Wb, phiN≈−0.0005257303404755968Wb; Δphi=−6.450892158958656e−6Wb and sum h(V−150)≈−6.450892158959148e−6Wb, residual difference≈4.92e−19Wb. Frozen W_H≈1.116129188918598e−5J and Q_H≈−0.02259219766nJ. These are real-lifted ONE source-point coefficients: numerical source truncation, actual sensor E, other branches and Rs/Rphi/Rr remain OPEN.

**A legal two-source polarity crosscheck in a DIFFERENT frozen future.** Accepted nonprotected Pro18D artifacts/run_D/primitives/evaluation_ports.npz SHA256 2bc0926d2b757be3e1cadb2c8300aa669ea3234dbed5cbc893f0fee22f22a234 and pro18d_design_freeze.json L4–29,55–81 contain TWO lawful static L4.3/5.2nH own-PREP source traces, identical initial50 and D1 continuous future command, H561/56ns. Independently rescored source Q0≈−0.104531427024nJ, Q1≈−0.059556138216nJ, ΔQ≈+.044975288806nJ. The exact two-copy identity separates +.041450546248nJ from ΔVᵀK mean(s) and +.003524742561nJ from mean(V)ᵀKΔs (closure <3e−12nJ). Their PREPARED endpoint port states differ, so they check general D7 polarization, NOT the new same-initial-point radius formula; H561 and command are not original Goal27 H841. Fixed L chosen before own PREP is legal; the source has no post-CAL ΔL switch, magnetic-flux reset or actuator-work law.

**Decision ceiling.** D8 supplies a finite-family norm bound with actual-source, exact-stored coefficient upper constants. D7's ±3.313718621e−5nJ is only a separate fixed-current residual box. Neither is a full original source-compatible future goal interval. Require legal jointly guarded Rs/Rphi/Rr over PREP/full4801 CAL/target6721 at same full-record information, or an accepted common-record second future source path, before asserting physical Goal27 shrinkage.

## 2026-10-18 D10: exact finite-command Q2 gate-coil BE transport, not a nonlinear response claim

**New source-row finite relation.** Original `actual_law.py` L180–203,235–245,276–301 has Q2 gb KCL row16 and Lg coil BE row32 (node gb=16, g2=17, k=24, current iLg=y32). Set `R2=Rg+5.03785=12.53785 ohm, Lg=11.364 nH, Leff=Lg(1+R2/100)=12.788801274 nH`, and residuals `r16` [A], `r32` [V]. Eliminating gb gives for EVERY source BE stage with command u, on- or off-branch:
`(Leff/h+R2) iLg_new=(Leff/h) iLg_old +u−(v_g2−v_k)+(1+R2/100)r32+R2 r16`.
This is a finite-amplitude law at fixed installation and prior state, independent of a small-signal Jacobian. Two legal own-PREP paths with a common prefix obey an EXACT difference recurrence with positive `alpha_n=(Leff/h)/(Leff/h+R2)` and `beta_n=1/(Leff/h+R2)` multiplying the future command difference minus internal gap difference plus signed source-row residual differences. Independent read-only archived target6721 check reconstructs the actual gate command from row16 with maximum absolute error `4.31e−14 V` (FLOAT diagnostic).

**A falsifiable conditional 0.1 V finite gate.** Consider a continuous triangle Delta u(t)=0.1V max(0,1−|t−32ns|/8ns), zero before24ns, on the same target 12.5ps fine grid and matched prepared state. If BOTH worlds satisfy per-step `|r16|<=3 microA, |r32|<=4e−8 V` and the WHOLE 24–32ns window obeys `|Delta(v_g2−v_k)|<=50 mV`, the ordered positive recurrence encloses `Delta iLg(32ns)` in **[+2.9650760,+10.9535871] mA**; tightening the unverified internal-gap budget to 20mV gives [5.356846,8.561817] mA. Conversely a claimed tube with `|Delta(v_gb−v_k)|, |Delta(v_gb−v_g2)|<=10 mV`, `|Delta iLg|<=1 mA` at the 0.1V crest violates row16 (it requires >7.072 mA at the stated residual budget). These are rigorous signed inequalities **conditional on unsupplied internal-voltage-gap and residual slabs**, not observed second source roots, a certified legal continuous command response or future work bound. The prior D8 source-flux radii and full H841 physical future interval are still OPEN. At the archived crest the base gate command already reaches 15 V, so this positive 0.1 V trial reaches 15.1 V; a frozen **admissible continuous-command upper bound permitting that perturbation has not been established**. The finite response remains an input-legal-if-qualified conditional theorem, not a new authorised forward intervention. No post-CAL L-switch/flux-reset law was assumed.

## 2026-10-18 D11/D12: legal source gate-k recursion, causal signed H841 goal dual and 84ns Q1 thermal tube

**D11 — original producer-API-legal finite intervention.** Original nonprotected `original_submission.zip::pro18c_replay.py` L172–180 restricts the future command to THREE ordered knot TIMES and hardcodes levels (−4,15,15)V. Previous proposed ±0.1V triangle with extra knots is NOT legal under this producer, even when in amplitude range. A legitimate prospective finite command pair is identical own PREP/CAL, static L4.16nH, and future knots (0,18,84)ns→(0,18.1,84)ns, which share the original fine6721/H841 and constant future beyond18.1ns. At18ns delta command=−.104972375691V; neither new future source root nor new actual work label was generated. From Q2 source KCL rows16 (gb),17 (g2) and original BE coil row32, exact for any two source BE paths:
`(L*/h+R*) i32,n=(L*/h) i32,old+u_n−(v18−v24)_n+e*_n`,
`R*=12.53785+9=21.53785ohm`, `L*=11.364nH(1+R*/100)=13.811561274nH`, `e*=(1+R*/100)r32+12.53785r16−9r17`. With identical initial source state, alt row16/17 residual≤3microA, coil≤4e−8V, and independently VERIFIED full0..18ns |delta(v18−v24)|≤30mV, positive BE weights bound delta iLg(18ns) in [−6.096135,−3.304304]mA. Archived ordered tangent gate-k max25.6424mV is only a plausibility check, not full nonlinear path qualification. A claimed |delta iLg|≤1mA REQUIRES the signed weighted gate-k gap in [−122.836,−79.630]mV; this single scalar oracle could falsify an unqualified future tube. The frozen signed H841 work of the affine tangent trial changes only +.258913nJ via ~+94.117/−94.334nJ cancellation; its nonlinear source residual is large, so it does **not** establish the true work sign or magnitude. No post-CAL L switch or magnetic flux reset was introduced.

**D12 — exact SOURCE-COIL causal signed work identity.** On common original H841/source t6721 grids let `P` be the frozen PL interpolation, `M=PᵀΩP`, `K=M−diag(0,h1,...,h6720)`. For A=M (true frozen signed external `W_H`) or A=K (D7 correction `Q_H`), define saved v=vD−vsl, s=i36, `g=A s`, `a=A v`, `b_m=h_m/Ls·sum_{j≥m}a_j`, static `Ls=4.16nH`. Any SECOND exact root with identical prepared s0,V0 and constant source L satisfies `delta s_j=1/Ls·sum_{m≤j}h_m(delta vsl_m−r36_ref,m)` from ORIGINAL coil BE row36. The following identity is FINITE amplitude, including the voltage-current cross term:
`delta Goal= sum_{m≥1}[g_m delta vD_m+(b_m−g_m)delta vsl_m]−sum_{m≥1}b_m r36_ref,m + delta vᵀ A delta s`.
For any independently certified FULL SOURCE family with each D/sl fine nodal voltage within ±1µV of archived reference, same prepared state/clock/command and exact alternate coil root, the original H841 `W_H` conditional point-centered radius is <**0.030400 nJ**, while `Q_H` is <**0.001126 nJ** (actual binary64 numerical respective 0.0303993308014630 and .00112553773514318nJ). The latter is ~240× smaller than D8 weighted Gram radius .270306029nJ on the SAME artificial node tube. An independent coil-only adversary attains Q difference +.00112553524748nJ, close to this linear support; it is NOT a legal 50D alternate world. This bound is sharper because it retains the source BE current history and exact H interpolation correlation. New `dpt_tools.s150_causal_coil_signed_goal_bound` computes FLOAT point coefficients only; none of its user radii or coefficients are physically directed source/fiber certificates. If prepared endpoints differ, add `delta s0·sum_j(A v)_j`, `g0 delta V0` and corresponding quadratic endpoint terms; do not erase own-PREP differences.

**Whole-target source thermal partial reachability.** Q1 G2 channel is OFF at all saved original PREP/CAL/target nodes, minimum frozen target ETH clearance 4.3380717176V. After exact G2-OFF heat/body wiring the Q1 heat is temperature-INDEPENDENT, and its four-node BE thermal subsystem has positive M-matrix inverse and substochastic predecessor operator. For ANY prospective electrical/body path on SAME 84ns target grid with ALL 26 node voltages within ±1µV, |delta ib_Q1|≤10microA, and identical prepared Q1 thermal seed, the exact source heat nonlinearity, INCLUDING ABS-sign crossings, has |delta H|<3.863W. The original Q1 saved raw thermal row residual maximum3.48518617e−6W (<5e−6W conservative); by the exact M-matrix comparison, the UNIQUE causal Q1 thermal continuation obeys `sup_t ||delta T_Q1||∞ <(84ns/.00131J/K)(3.863+5e−6)W <0.000248 degC`, even when heat sign flips. If own-PREP seeds differ, add their Q1 thermal maxnorm difference. This is a *conditional 4D thermal source-root tube*, not a 50D source trajectory family or signed work range. Q2 actually crosses ETH at CAL 1581→1582 and target 1842→1843, and Q1 heat changes sign on the saved future; one full-horizon classical C1 Jacobian is invalid. Remaining all-electrical/body/diode GL32 Q2 branch covering and joint full-CAL fiber OPEN.

## 2026-10-18 D13/D14: different-own-PREP fixed-L signed-goal dual and hybrid-mode thermal subsolver

**D13 exact two-copy source-coil identity, extending D12 without a shared prepared seed.** For two source BE paths a,b with distinct STATIC inductances La,Lb installed before their own legal PREP, same ordered fine t6721/H841 readout and source coil sign convention `r36=-vsl+L(s_n-s_old)/h`, set `deltaL=Lb-La`, `deltaPhi0=Lb*s_b0-La*s_a0` and `delta r=r36_b-r36_a`. At every future index j the following is an EXACT finite-amplitude source-row necessary identity, with no post-CAL switch or flux reset: `delta s_j=[deltaPhi0-deltaL*s_a,j+sum_{m<=j} h_m*(delta vsl_m+delta r_m)]/Lb`. For the original frozen H scorer let `A=P.T Omega P` for signed terminal W_H or `A=P.T Omega P-diag(0,h)` for the separate correction Q_H; `v_a=vD_a-vsl_a`, `g=A*s_a`, `a=A*v_a`, `b_m=h_m/Lb*sum_{j>=m}a_j`, `Gamma=sum_j a_j*(s_a,j-s_a,0)`. Then exact (not a tangent) signed two-path identity:
```text
deltaGoal = g.T*delta(vD-vsl) + sum(a)*delta_s0
          + (La/Lb - 1)*Gamma
          + sum_{m>=1} b_m*(delta vsl_m + delta r36_m)
          + delta(vD-vsl).T*A*delta s .
```
This retains initial flux/current differences, the convolutional internal sl forcing and the H interpolation BILINEAR cross. New `dpt_tools.s150_two_l_causal_goal_identity` computes the identity on two SUPPLIED paths and reports direct scorer closure, without generating physics trajectories or certifying full50. Cloud independent nonaligned synthetic grids, three random seeds, both score types and different initial seeds/source coil residuals give |direct−dual|<7e−22J, and three independent mutants removing static-L, prepared-current or bilinear term are detected by regression. This code requires no extra files in Math; the source data remain original nonprotected archives.

**Actual-source meaning and strongest falsifier.** Accepted original Pro18C target6721/H841 saved center has W_H=11161.291889185964nJ; source-only fixed-node illustration at La=4.16nH gives a very large derivative `dW/dL|vsl,seed fixed≈-2682.275411594 nJ/nH`, while Q_H gives +.0055444807784 nJ/nH. These are NOT physical L response derivatives. A coil-row-only constructed alternative at Lb=4.577933656nH, with another archived prepared seed but artificially FROZEN future vD,vsl, yields W difference−1018.527377591nJ; its exact dual closes to ~2.3e−11nJ, but the DIFFERENT full50 archived B06 member has W difference only −25.095434584nJ. Missing **closed-loop electrical feedback** contributes ~+993.431943nJ in this mismatched-source comparison. B06 differs other PREP/physics/CAL parameters, so this is a falsifier of naive frozen-field transfer, not an isolated physical ∂W/∂L. In original accepted restricted-PREP T00/T06 with L4.278747833→4.321330602nH, the exact coil-endpoint flux source row forces an 84ns mean grounded sl change **+2.527152537599mV** with archived coil QA mean error ±7.103e−9V. Their actual W difference only +.335303206nJ, from voltage signed contribution **−21.491173nJ** and current **+21.826476nJ** (strong cancellation). T00/T06 share ONLY restricted PREP features, NOT original full CAL, so neither is an actual original Goal27 same-information diameter witness.

**D14 actual Q2 ON/OFF thermal separate-branch contractor.** On the nonprotected Pro18C accepted extension `pro18c_prediction_extension.npz` original SHA256 `af7299434d7dcde687da3bf56b5ce31babbc4e0c1c0e12b1a849b5f5530ae8fd`, with own-PREP (.23,.37,.23)V, L4.16nH, κ1.009, original 84ns target, fix ALL present stage electrical/body variables and predecessor four thermal states. The source thermal 4x4 positive M-matrix `M=Ct/h+Kt` reduces exactly to `Tj=beta+alpha*H(Tj)`, where alpha=(M^-1)00~9.5419833053e−9 degC/W on h12.5ps target. At actual source target n2883 (ON branch, g2-overdrive>4.2999V), finite source-channel/heat interval differentiation over Tj_saved±.0001C proves |dH/dT|<9.562157 W/C and contraction q<**9.1242e−8**; one UNIQUE fixed-electrical 4D thermal subroot lies within ~5.866145e−16C of the saved junction center, with positive source sign/clip/κ and correct gg=(g−g2) gate-heating edge. Nine separate true saved PREP/CAL/target OFF/ON stages pass local interval thermal inclusion (not full trajectory), including target stage1842 OFF with overdrive−2.330793mV and stage1843 ON +2.945929mV. If thermal states at target1841 are exact and electrical/body coordinates are FROZEN at both subsequent saved stages, the positive predecessor M-matrix transports their local residuals to a two-stage four-state thermal bound <**2.862085e−15C** at1843. This tests the idea of a hybrid per-step interval thermal solver; it is NOT a certified 6720-step 50D electrical/body trajectory or history fiber.


**Full-target Q2 thermal chain, stronger than nine isolated spot stages.** At EVERY index 1..6720 of the ORIGINAL saved target, retain the given source electrical/body values, the actual κ1.009 G2 channel formula and initial 4D thermal state. Worker4 ran 36-digit directed source-real interval arithmetic on Tj_saved±0.0001°C for every step, including all heat ABS, G2 OFF/ON and ETH masks, solving the 4D BE source M-matrix with its exact predecessor (no independent TH reset). Each of 6720 thermal-only maps is strictly self-contained, zero failed guard stage. Worst local thermal-feedback contraction q=1.0870274468516121e−7 at index3101; worst centered normalized M^-1 thermal residual mu=1.660128410034795e−11°C at index420. Positive M^-1 predecessor operator is substochastic, hence propagation η_n<=(η_old+mu_n)/(1-q_n) starting η0=0 yields complete fixed-electrical **Q2 four-thermal-subsystem** max error <4.090268e−11°C at final index6720. Smallest widened signed gate-threshold distance remains >2.330323mV at stage1842, so no local thermal box crosses an ETH branch face. PRIME independently recomputed all 6720 source-center M^-1 residuals, minimum ETH gate distance and finite-difference thermal feedback: worst mu=1.660128410033105e−11°C (index420), q≈1.08695605e−7(index3101), and 6720 recurrence with q enlarged 1.01 gives 4.090271e−11°C. The matching center values are a strong independent check; global directed heat-derivative/branch validation remains worker4's source-real interval computation. This is an actual 6720-step **conditional thermal subroot chain**, NOT a certified full50 electrical/body/diode source trajectory, heterogeneous own-PREP/clock L-world, or signed work tube.

**D13 minimal observation-repair oracle under an exact raw-port alias assumption.** Original double-coil BE rows36/37 with LOAD Ld=100microH imply that if TWO legitimate own-PREP worlds with distinct static L share the IDENTICAL source-raw full CAL Vport and Iport (not filtered CAL) then their *load* current-difference increment obeys `delta j_D(t)-delta j_D(t0)=deltaL/Ld*(I(t)-I(t0))`. Pro18F saved L4.50 raw CAL I swing is 13.02864333477A. A hypothetical two-time pretarget load-current readout with per-measurement absolute error eta_j could distinguish a pair with |deltaL|=.34nH if eta_j<**11.0743468microA** (true differential gap44.2973873microA divided across both measurements/two worlds), or |deltaL|=.05nH if eta_j<**1.6285804microA**. This is an exact source-law conditional necessary-information threshold, NOT evidence an actual second full50 CAL-alias world exists, that such a sensor is noninvasive/qualified, or that current original Goal27 goals already shrink. The strongest ordinary receives exactly the same extra reading.

**Original-paper transfer and strict discontinuity boundary.** Alefeld–Chen–Potra, *Numerical validation of solutions of complementarity problems: The nonlinear case*, Numerische Mathematik 92 (2002)1–16, DOI [10.1007/s002110100351](https://doi.org/10.1007/s002110100351), original authored PDF printed p3 Eq2.1 F=min(f,x), p4 Lemma2.1 slope and p8 Thm3.1 interval slope, requires a CONTINUOUS underlying f and interval slopes; valid only for appropriately continuous source branch equations, not across literal ETH jumps. Existing S-L15 already proved ETH branch discontinuity at T25 and80C; this round additionally intervalizes high−low ETH at T∈[25,25.1]C strictly negative ~[−6.484,−4.516]mV and tests actual Q2 target1842/1843 separate heat contractors; no global Clarke map across jump. Rauh–Brill–Günther (2009) DAE interval work DOI [10.2478/v10006-009-0032-4](https://doi.org/10.2478/v10006-009-0032-4) is a prospective consistency-space method only: original official PDF theorem/page not available; do not transfer its assumptions without proof. The Sep24 2026 OpenAI nonexpansive reflexive-Banach fixed-point manuscript (official openai/math TeX introduction/anchor lemma) does not supply a verified DPT local numerical root, contraction metric or global-source guard, so paper prestige is not source evidence. No hardware/sensor E, full root, all-fiber, or MAIN_ACCEPTED status is changed.

## 2026-10-18 D15: source Q2 input-to-thermal 6720-stage interval contractor with a quantitative electric missing input

**New over D14's FROZEN-electrical thermal chain.** Take the already qualified nonprotected original Pro18C (L4.16nH, κ1.009, a=.23/.37/.23V) accepted target6721 source SHA256 `af7299434d7dcde687da3bf56b5ce31babbc4e0c1c0e12b1a849b5f5530ae8fd`. For Q2 original source nodal groups `g=y18-y21, d=y15-y21, dx=y15-y20, gg=y18-y17, ib=y39`, define `S=κ I_ch(g,d,T)+1e4 dx+1.025e-7 d-ib`, `heat=abs(d*S)+gg^2/9`; use `M=Ct/h+Kt` positive M-matrix and `P=M^-1 Ct/h>=0`, row-sum≤1. Bound `U_g=|dκ ∂g Ich|, U_d=|S+d(κ∂d Ich+1.025e-7)|, U_dx=1e4|d|, U_gg=2|gg|/9, U_ib=|d|` using per-box outward intervals, including clip/mode panels and the ABS Lipschitz `||x|-|y||<=|x-y|` at heat-sign kinks. With `α=(M^-1 e1)_1, q_n=α sup|∂T heat|, μ_n=||M^-1 r_th(saved)||inf` and an independently certified source-electrical radius vector ρ_n, the valid causality bound is `η_n <= (η_{n-1}+μ_n+α Σ U_i ρ_i)/(1-q_n)`.

**Actual archived full H841 target computation, still conditional on source electric outer.** Worker4 direct 40dps source-real intervals of all 6720 stage channel masks/net2/net5/p8/ETH, and Q2 4 thermal rows, prove strict local thermal self-inclusion with electrical Q2 *each node* ±1mV, body ib±1microA and ADDITIONAL source-correlated narrow `|δ(y15-y20)|<=1.5microV`. η_final≤**8.5472357099e-5 degC**, below the declared 1e-4 degC radius; worst q≤1.11927756e-7 at target3103; the six archived heat temporal sign changes are retained, and 2031 widened heat sign boxes themselves intersect zero, so the Lipschitz heat contractor (not a frozen-sign differentiable J) is essential. The smallest ETH guard under ±1mV node boxes remains >0.330323mV at target1842. Source interval cumulative U gains [g,d,dx,gg,ib]≤[.00732179545,.00040119013,46.61997644,.00004585921,.00466199765] K per [V,V,V,V,A]; PRIME independently recomputed from all saved source rows the corresponding point gains [.00725701,.00039309,46.6151245,.0000458286,.00466151] and total conditional estimated η8.53193e-5 degC. The contractor permits at most **1.8116184microV** of correlated dx under its other radii; if dx is enlarged to 2microV, its FIRST sufficient-radius failure is target index3168, η≈1.00031370e-4 degC (not a physical counterexample). A separate UNIFORM source node±1microV/body±1microA chart still passes η<9.326e-5degC, whereas 1.1microV first fails its radius at3307.

**Actual source falsifier of a stronger heat-sign claim.** Near target index811 the saved Q2 current sensor is +1.75462324e-7A. Independent y15/y20 nodal errors of opposite sign as small as **8.7731162pV** each can reverse its heat-sign, far below 1microV; thus we cannot replace the true ABS heat residual with a uniform differentiable/frozen-sign chart on the full target. The positive thermal subsolver survives this ambiguity by ABS-Lipschitz. An accepted all-50D future source-electric/body trajectory enclosure with its **very narrow differential contact** radius is OPEN; this D15 tube cannot be inherited from the distinct original .3V first PREP chart without full model/command/old-history compatibility. Claim only a true-source-real *conditional four-temperature* subroot chain, not a full Goal27 work/fiber bound.

## 2026-10-18 D16: exact positive two-package-coil Schur and H841 signed-goal adjoint

**Source-row derivation beyond D13's one external coil.** Use original `actual_law.py` rows 1/25 KCL, 34 Q2 Ls2 coil, 36 external sl coil, with `s=i36, j=-i34, R=.003322ohm, Rp=100ohm, L2=3.435nH`. The source identities are `r1=(sl-sa)/R+s`, `r25=(sa-sl)/R+(sa-sv)/Rp-j`, `r34=-(sa-sv)-L2*(j-jold)/h`, `r36=-sl+L*(s-sold)/h`, for original `sv=y22=Q2:sv`. Eliminating `sl,sa` yields exactly:
```math
A_{L,h}x_n=D_{L,h}x_{n-1}+e_1v_{22,n}+f_n,\qquad
x_n=(s_n,j_n)^T,
```
with `A=[[L/h+R+Rp,-Rp],[-Rp,L2/h+Rp]]`, `D=diag(L/h,L2/h)`, `f=[r36+(R+Rp)r1+Rp*r25,-r34-Rp*(r1+r25)]`. For every positive static L and h, A is a symmetric positive-definite M-matrix: `A^-1>=0`; `P=A^-1D>=0`, `P*ones<=ones`. There is no post-CAL inductance switch; distinct legitimate worlds use their own constant La/Lb and own prepared `s0,j0`. Exact finite-amplitude comparison at fixed Lb is `delta x_n = P_b delta xold + A_b^-1[e1 delta v22_n - e1 (Lb-La)*(s_a,n-s_a,old)/h + delta f_n]`. This is source algebra, NOT a two-state substitute for all 50D physics/thermal feedback.

**Goal-only backward recursion with complete H841 interpolation and bilinear term.** Set `M=P_H^T Omega_H P_H`, `v_a=vD_a-vsl_a`, `a=M*v_a`, `g=M*s_a`, and `z_N=(a_N,0), z_(n-1)=(a_(n-1),0)+P_b,n^T z_n`. Then exactly `delta W=g^T delta(vport)+z0^T delta x0+Σ_{n>=1} z_n^T A_b,n^-1[e1(delta v22-DeltaL*Delta s_a/h)+delta f]+delta(vport)^T M delta s`. Prepared flux `delta s0=(deltaPhi0-DeltaL*s_a,0)/Lb`, and separately prepared package current delta j0 appear explicitly. This signed work is NOT D13's frozen-sl causal derivative, nor Pro18D H561.

**Independent actual source-row and goal checks.** On original accepted full target6721 C saved source, PRIME recomputed max |r1/r25|=8.793e-13/1.0143e-12A, |r34/r36|=2.44249e-13/2.94875e-13V, 2x2 Schur identity max float closure1.615e-12V and f1/f2 max6.3291e-11/6.3369e-11V; frozen H841 true W=11161.291889185979nJ. Adjoints `z0_s=3.342437275298e-6 J/A, z0_j=2.753364757132e-6 J/A, Σ|z_n^T A_n^-1 e1|=1.63355693525e-5 J/V`. Under the explicitly *HYPOTHETICAL* same-static-L future source family with |delta prepared s0|,|delta prepared j0|≤1microA, all |delta v22|≤1microV, all |delta(vD-vsl)|≤2microV, alternate source Schur forcing residual=0, the positive two-state bound gives **|delta W_H|<=0.023062624 nJ**, including archived reference f and signed bilinear cross ≤1.987e-9nJ. This was independently recomputed by worker3 and PRIME's new minimal `goal_defect_transport.s150_package_two_coil_goal_bound`, which reports source row residuals, adjoints, radius and its claim ceiling; two new deterministic synthetic/invalid-input tests PASS in memory. Its `max |delta s|` conditional bound is ~11.8251microA. The *fixed-node-field* partial dW/dL at La4.16nH is -1469.487nJ/nH, versus D13 frozen grounded-sl -2682.275nJ/nH; neither is a full physical L derivative. Missing: all-legal future bounds on **internal** v22 and source full electrical/body path, common original CAL fiber and sensor errors. No certified Goal27 diameter contraction follows.

**Independent D15/D16 review (2026-10-18; conditional only).** The two-coil Schur reduction, positive M-matrix structure, prepared-flux/current terms, H841 adjoint recursion and bilinear interpolation bound are algebraically consistent for the stated fixed-L contract. The `0.023062624 nJ` radius remains conditional on same static L/grid, prepared `s,j` differences ≤1 µA, future `|δv22|≤1 µV`, `|δ(vD−vsl)|≤2 µV`, and zero alternate Schur-forcing residual; none of these input radii is yet jointly derived from a full 50D/CAL-compatible tube. For D15, the ABS-Lipschitz heat contractor is appropriate at sign crossings, but `1.8116184 µV`, the 2 µV first sufficient-inclusion failure at target index 3168, and the reported accumulated thermal radius have not been independently reproduced with a committed directed interval receipt. The pinned tree has no D15-specific calculator or regression test. A read-only local SHA256 check now finds `pro_runs/20261010_pro18_goal_adequacy_frontier/analysis/acceptance/pro18c_prediction_extension.npz` (3,928,589 bytes; SHA256 `af7299434d7dcde687da3bf56b5ce31babbc4e0c1c0e12b1a849b5f5530ae8fd`), matching the target-array identity cited above. Its bytes are still absent from the remote Math tree; no D15 numerical replay or stagewise interval receipt was produced. Smallest reusable regression: per-stage outward intervals for the correlated `dx`, electrical/body inputs, thermal residual, ETH/heat/diode guards and resulting `η_n`, plus an assertion that the first failing stage/radius matches the claimed threshold. No full-source Goal27 work-diameter shrink follows.

## 2026-10-18 D17: one pretarget grounded-sl voltage repair gate, and a two-load-sensor negative control

**One NEW source-coil necessary-information inequality.** On original accepted C CAL 4801x50 L4.16nH, the largest archived backward difference `|(s_n-sold)/h|=2.75482482754441e9 A/s` occurs at CAL index3221 / absolute time 6.9482625microseconds (old prepared state and same full digital command). With another *hypothetical* valid static-L world Lb4.50nH and IDENTICAL RAW s(t), source row36 forces grounded `sl` voltage change `|DeltaL*dot s|=0.936640441365V` at that ONE pretarget instant; source Q2 G2 is ON safely there (threshold margin4.736894V). If pairwise raw `|delta s_n|,|delta s_old|<=epsilonI`, candidate/source row36 residuals each ≤3e-8V and a NEW absolute noninvasive sl probe has per-world error≤etaV, the pair is strictly excluded by **`2*etaV +732.8(V/A)*epsilonI +6e-8V <0.936640441365V`**. Under pairwise epsilonI=0, etaV must be <.46832019V; at 1mA pairwise epsilonI, etaV<.10192019V; at epsilonI>=1.27816646mA this witness cannot separate even with perfect probe. This is a source-point *necessary* gate, not proof of a second same-CAL source world, sensor loading, raw-current recovery from RC-filtered CAL, or Goal27 source-wide information repair. All full-record ordinary competitors receive the same added sl readout. The Pro18F L4.50 saved RAW CAL source has DIFFERENT maximum slope2.776147588e9 A/s at index3223, so do not transplant it into the C witness.

**Strong noise-falsifier of a simpler D13 double-load-current sensor threshold.** An ideal exact-RAW terminal alias between L separated by ΔL=.34nH implies from the 100microH load/source coil rows a CAL load-current two-time gap max44.2973873microA at Pro18F L4.50 raw H index2923, so the older *zero external voltage difference* condition eta_j<11.07435microA is correct only WITH EXACT raw V/I equality. If each world instead has even a directly-calibrated favorable RAW port-V ambiguity ±.30558V (model-defined thought experiment; the actual P54 uncertainty is postfilter with unknown offsets/gains), the same coil identity allows pairwise voltage forcing uncertainty `(2*.30558V)*36.5375ns/(100microH)=223.302585microA`, over FIVE times the ideal L signal before current/noise errors. The archived maximal |I-I0|/(H-H0)=.358032135 A/ns, whereas a two-time voltage-noise-robust ΔL=.34nH separation would require >1.7975294 A/ns; NONE of original 4801 H supports it. Even with eta_j=0, the effective per-world RAW voltage error would have to be below ~60.86546mV, not .30558V. This does NOT disprove all load-current repairs under correlated offset/phase models or source physics; it specifically falsifies promoting the noiseless 11microA threshold to an instrument-qualified universal repair. The external CAL E and new sensor model must be jointly qualified.

## 2026-10-18 Independent frontier theorem-transfer audit (OpenAI Math)

**Evidence label: proof-design analogies only.** The following three repository manuscripts were checked against their original TeX sections pinned to `Gogoal-L/math@83324628a0495ea01dac9ec550befd946b079731`. None supplies a theorem directly applicable to the hybrid S150 source law, and none changes the current Goal27 direction or certifies any full-source work-diameter shrink. The value is in their proof architecture and in the falsifiable transfer tests below.

### 1. A sharp Fourier certificate for planar circle packing

- Original PDF: [paper.pdf](https://github.com/Gogoal-L/math/blob/83324628a0495ea01dac9ec550befd946b079731/preprints/A-sharp-Fourier-certificate-for-planar-circle-packing-September-23-2026/paper.pdf)
- Theorem text: [Theorem `intro:main`](https://github.com/Gogoal-L/math/blob/83324628a0495ea01dac9ec550befd946b079731/preprints/A-sharp-Fourier-certificate-for-planar-circle-packing-September-23-2026/build/sections/introduction.tex)
- Proof machinery: [Lemmas `interpolation:finite`, `interpolation:inverse`, Proposition `interpolation:solution`](https://github.com/Gogoal-L/math/blob/83324628a0495ea01dac9ec550befd946b079731/preprints/A-sharp-Fourier-certificate-for-planar-circle-packing-September-23-2026/build/sections/interpolation.tex); [Proposition `signs:global`](https://github.com/Gogoal-L/math/blob/83324628a0495ea01dac9ec550befd946b079731/preprints/A-sharp-Fourier-certificate-for-planar-circle-packing-September-23-2026/build/sections/signs.tex); [finite interval/quadrature certificates](https://github.com/Gogoal-L/math/blob/83324628a0495ea01dac9ec550befd946b079731/preprints/A-sharp-Fourier-certificate-for-planar-circle-packing-September-23-2026/build/sections/certificates.tex).

The theorem asserts a real radial Schwartz function with $\widehat f(0)=1$, $f(0)=2/\sqrt3$, $\widehat f\ge0$ globally and $f(x)\le0$ for $|x|\ge1$. The proof does not trust a finite table alone: it encloses a finite coefficient/interpolation problem, proves an inverse bound on the whole $\ell^1$ coefficient space, and separately controls infinite tails and global signs. The certificate appendix says terminating decimals are exact rationals and combines interval quadrature with an analytic moment remainder.

**S150 transfer test.** On one actual legal source box $X$, build a rational preconditioner $W$, compute an outward bound $q\ge\|I-WJ(X)\|$, and supply a source-residual plus nonlinear-remainder enclosure sufficient for a strict Krawczyk inclusion. The test passes only if $q<1$, every residual and remainder is source-derived, all 24 mixed-unit rows are consistently scaled, and every ETH/diode/thermal guard is covered. It fails if $q\ge1$, any tail/remainder is unbounded, or a branch/guard is omitted. **Boundary:** the manuscript's radial Fourier operator and infinite coefficient space do not map directly to the S150 Jacobian; only the finite-core-plus-rigorous-tail certificate architecture is transferable.

### 2. The Mahler Conjecture for General Convex Bodies

- Original PDF: [paper.pdf](https://github.com/Gogoal-L/math/blob/83324628a0495ea01dac9ec550befd946b079731/preprints/The-Mahler-Conjecture-for-General-Convex-Bodies-September-22-2026/paper.pdf)
- Main statement: [Theorem `thm:mahler`](https://github.com/Gogoal-L/math/blob/83324628a0495ea01dac9ec550befd946b079731/preprints/The-Mahler-Conjecture-for-General-Convex-Bodies-September-22-2026/build/sections/00-introduction.tex)
- Proof components: [Lemmas `lem:scalar-ranges`, `lem:scalar-certificates`, `lem:scalar-interpolation`, `lem:scalar-tail`](https://github.com/Gogoal-L/math/blob/83324628a0495ea01dac9ec550befd946b079731/preprints/The-Mahler-Conjecture-for-General-Convex-Bodies-September-22-2026/build/sections/07-scalar.tex); [Proposition `prop:segment-estimate`](https://github.com/Gogoal-L/math/blob/83324628a0495ea01dac9ec550befd946b079731/preprints/The-Mahler-Conjecture-for-General-Convex-Bodies-September-22-2026/build/sections/08-segments.tex).

The repository manuscript claims $P(K)\ge (n+1)^{n+1}/(n!)^2$ for every convex body, with equality exactly for simplices. Its relevant proof mechanism separates exact-rational finite-node bounds, interpolation from second differences, analytic tail bounds, and a strict segment inequality. The argument's force comes from uniform margins over the entire scalar domain, not from successful evaluation at sampled points.

**S150 transfer test.** Choose one legal parameter segment contained within a single smooth source branch. Enclose source residuals, one named guard, or the goal derivative at interval nodes; prove a uniform interpolation remainder and tail bound; then show the complete interval stays strictly on the required side of the decision margin. It fails if any remainder is unsupported, an interval crosses zero/goal threshold, or the segment crosses an ETH/clip seam without splitting and covering both branch images. **Boundary:** the scalar profiles in the manuscript have analytic regularity that is not automatically available across S150 hybrid seams; do not interpolate through a discontinuity.

### 3. Sharp One-Third Stability of Brenier Maps

- Original PDF: [article.pdf](https://github.com/Gogoal-L/math/blob/83324628a0495ea01dac9ec550befd946b079731/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/article.pdf)
- Main statement: [Theorem `main:stability`](https://github.com/Gogoal-L/math/blob/83324628a0495ea01dac9ec550befd946b079731/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/build/source/sections/introduction.tex)
- Proof components: [Lemma `moments:derivative`](https://github.com/Gogoal-L/math/blob/83324628a0495ea01dac9ec550befd946b079731/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/build/source/sections/moments.tex), [Lemma `gradient:interpolation`](https://github.com/Gogoal-L/math/blob/83324628a0495ea01dac9ec550befd946b079731/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/build/source/sections/gradient.tex), and [Proposition `finite:potentials`](https://github.com/Gogoal-L/math/blob/83324628a0495ea01dac9ec550befd946b079731/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/build/source/sections/finite_stability.tex).

For a compact convex source domain with uniform measure and compact target set, the manuscript states a uniform $L^2$ stability estimate $\|T_\mu-T_\nu\|_{L^2}\le C(K,Y)W_2(\mu,\nu)^{1/3}$, with the exponent sharp in general. Its proof combines a stationary-site moment estimate, convex-gradient interpolation and a finite-target potential bound. The exponent and constant depend on the stated geometric setting.

**S150 transfer test.** Try to establish a source-specific modulus for the H841 signed-work scorer as a function of a rigorously defined distance between complete-CAL/command/$\Delta L$ worlds, and challenge it with certified legal pairs near every ETH, diode and thermal seam. It fails if a pair violates the proposed modulus or if the constant cannot be bounded uniformly over the legal source family. **Boundary:** Wasserstein distance between target measures is not a metric on S150 source histories; neither the exponent $1/3$ nor its constant may be imported as a physical error bound.

**Research decision.** These papers suggest three useful proof-design patterns—finite exact core plus tail control; strict interpolation margins on a fully covered regular domain; and an explicitly falsifiable stability modulus. None presently provides the missing S150 source arrays, 24-row directed residual/Jacobian receipt, legal full-CAL second world, or 6720-stage D15 thermal interval recurrence. Therefore they do not change the evidence ceiling: S-L26 remains `REPORTED_NOT_RECOMPUTED`, D15 remains unreproduced from committed stagewise receipts, and certified Goal27 full-source signed-work diameter reduction remains **0 nJ**.
