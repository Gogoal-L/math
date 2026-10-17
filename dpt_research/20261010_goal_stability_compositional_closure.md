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

**Scope (independent DPT finite automaton theorem).** Fix a finite legal set of *complete information histories* $H$ after source identity, pretarget PREP/CAL digital command, external raw observation and joint noise contract are declared. Future update tokens $a$ include the legal commanded intervention and any new **pretarget** observation that can be used before the next prediction; write the deterministic realized history extension as $h\mapsto h a$ wherever legal. A future word $w$ induces a set $K(h,w)\subset\mathbb R$ of physically allowed signed terminal-work goals (J), including declared model/error uncertainty. Fix nonnegative tolerances $\tau_w$ and a desired memory alphabet with at most $2^M$ symbols. To avoid the classical loophole that one decoder can remember the entire preceding transcript outside the claimed $M$ bits, demand a **deterministic autonomous** representation $z=\pi(h)$, update $U(z,a)=\pi(ha)$ and a goal decoder $d(z,w)$, all using only legitimate new tokens and the same frozen future-word/scorer contract. This formal statement does not assign a physical measurement cost to an abstract token or claim that the controller's full recorded command is absent.

**(D1) A finite state is sufficient if and only if the legal histories admit a right-congruent $\tau$-compatible partition.** Such an $M$-bit autonomous predictor exists precisely when there is a partition $\{C_i\}_{i=1}^k$ with $k\le 2^M$ satisfying (a) every token allowed to all histories in $C_i$ has successors in one common class, with the legality/guard domain represented consistently; (b) for every future word $w$, the union $\bigcup_{h\in C_i}K(h,w)$ is nonempty and has diameter at most $2\tau_w$. **Proof (necessity):** fibers of any deterministic $\pi$ are stable under allowed common update tokens, and a shared scalar decoder within $\tau_w$ of all goal values forces their union diameter $\le2\tau_w$. **Proof (sufficiency):** label each partition cell, advance to its uniquely determined next class, and predict the midpoint of the class's goal union. The bound is elementary scalar interval geometry. If the future word changes a guard/legality domain, that domain must be included in the represented output or the partition must split accordingly. No finite-bank partition ensures correctness on the unseen continuous source domain without a qualified coverage/remainder argument; the single-transcript conflict-graph chromatic number in P19–P22 is only a one-time message minimum and need not be an autonomous-update minimum.

**Exact two-stage counterexample, status synthetic.** Let the hidden prepared bit be $h\in\{-1,+1\}$ and an internal flag $f\in\{0,1\}$ initially $0$. The lawful abstract command $A$ sets $f=1$ and reveals no $h$; command $B$ produces zero signed goal when $f=0$, but produces signed goal $h$ when $f=1$. All pretarget raw/digital observations are equal across the two hidden histories by construction, and an $A$-only or $B$-only goal test sees no difference; the ordered word $AB$ yields goals $-1,+1$ (dimensionless scaled J), so any shared predictor incurs error at least $1$ for $\tau<1$. A full-record ordinary that actually distinguishes $h$ is a strictly stronger information condition and predicts both; no source-law SiC two-world is asserted. More economical state messages need be compared at equal pretarget information and memory/replay cost. A physically legal update also needs branch/guard/moving-event time and *same* complete source continuation across stages, rather than a formal letter sequence.

**Original-paper boundaries.** F229, *Exact reconstruction threshold for the three-state symmetric channel*, Theorem 1.1 (original PDF p.3), Proposition 2.3 (p.8) and §6 (pp.27–33) assume an independent broadcast tree / channel eigenvalue threshold; its finite experiment is allowed to reveal hidden spin in a comparison, which is not a legal DPT sensor. F376-A, *Finite Instructions and Solenoidal Shear Flows*, Lemma 2.1 (p.3), Theorem 3.2 (p.6), and F376-B, *Incompressible Box Transport and Finite Computation*, Theorems 3.4 (p.10) and 4.1 (p.12), concern deterministic full-information incompressible flow constructions, not robust finite-bit DPT memory. F129's relation monoid/full alphabet state count is not a bound on our fixed few physical commands. We borrow the questions of whether information is recorded and can be autonomously updated; D1 is independently proved, not a corollary of those theorems. Candidate Main evidence: one **same S150 source**, qualified full pretarget recorded command/CAL and joint noise, a pair of source-reachable histories, a **predeclared ordered two-stage future command** and post-$A$ permissible observation, fixed work scoring. If the pair is still full-CAL compatible after $A$ but $AB$ goal gap exceeds $2\tau$, autonomous-state sufficiency fails; if post-$A$ observation separates the pair, that is a legal sensor repair candidate, subject to same-information full-record ordinary.

## 2026-10-17 D2: continuous-command goal pseudometric, guarded finite-memory tubes and passive two-branch counterexample

**Independent strengthening of finite-alphabet D1.** Fix a single complete source-law/PREP reference, a finite future horizon \(T\), all admissible continuous (or piecewise-continuous) future digital/analogue commands, full recorded pretarget external CAL, a **joint persistent** nuisance/error trajectory, and the terminal current/voltage identity. A source-history state \(x\) is augmented with all live preparation/DAE/filter/guard memory required to define future continuous signed terminal power \(p_x^w(t)=V_{\rm term}^w(t)I_{\rm term,x}^w(t)\). For histories sharing the same legal future word set and compatible event labels/guard timing, define
\[
d_T(x,x')=\sup_{\substack{w\text{ legal for both}\\|w|\le T}}
\int_0^{|w|}|p_x^w(t)-p_{x'}^w(t)|\,dt\quad[\mathrm J].
\tag{D2-a}
\]
If branch legality/event identity differs in a way the scorer cannot align, report \(+\infty\) / ABSTAIN rather than force a false quotient. On one legal domain \(d_T\) is a **pseudometric** (zero can identify physically distinct states) and dominates \(|W_w(x)-W_w(x')|\) for each future word. For every common legal command prefix \(a\) of duration \(h\) and compatible disturbance continuation,
\[
d_{T-h}(\Phi_a x,\Phi_a x')\le d_T(x,x').
\]
**Proof:** triangle inequality holds after taking each signed-power absolute value and supremum. Each suffix \(w\) of the updated states corresponds to the original concatenated word \(aw\); the integral of *absolute* power mismatch along the suffix is at most its value over the full prefix-plus-suffix because the prefix contribution is nonnegative. Supremize over suffixes. The absolute signed-work *difference alone*, without absolute power *inside the time integral*, can have cancellation between prefix and suffix and need not satisfy this right-congruence inequality. This exact behavioral distance is not automatically computable or bounded by finitely many source simulations; a DAE guard mismatch destroys the certified domain.

**(D2-b) A conditional constructive finite-bit streaming tube.** For a compact actual-source and joint-nuisance augmented history set, suppose a finite cover of at most \(N\) cells \(C_i\) of diameter \(\rho\) in a stated dimensionless state metric, every legal hybrid transition has **qualified complete** guard/consistency propagation, and the source-validated same-input transition map is \(\kappa\)-incrementally contractive \(\|\Phi_a x-\Phi_a x'\|\le\kappa\|x-x'\|\) for each allowed segment, \(\kappa\le1\). Let a sound directed OUTER reachability operator \(\widehat\Phi_a(B)\) contain **all** legal true successors of \(B\), with extra overhang from its exact image at most \(\beta\) in the same norm. Represent the compatible histories as a length-\(N\) cell mask (cost \(N\) bits plus clock/mode/command metadata), propagate **all** possible successor cells, and intersect only with the *same* temporally joint nuisance-feasible new pretarget observation. If \(D_k\) denotes diameter of the selected union, the conservative recurrence is
\[
D_{k+1}\le\kappa D_k+2(\rho+\beta).
\]
Proof: each survivor lies within \(\rho+\beta\) of a truly reachable predecessor state; insert two such nearby witnesses and use the incremental gain. Joint measurement intersection can only reduce diameter if the augmented latent error state is carried consistently. Iteration gives \(D_k\le\kappa^kD_0+2(\rho+\beta)(1-\kappa^k)/(1-\kappa)\) for \(\kappa<1\), otherwise \(D_k\le D_0+2k(\rho+\beta)\). If every frozen source-legal future signed goal obeys a **validated** \(L_G\)-Lipschitz bound with a separate solver/scorer remainder \(\epsilon_G\) J, the midpoint error is bounded by \(L_GD_k/2+\epsilon_G\), enabling a conditional \(\tau\)-adequate decision or ABSTAIN. This is a sufficient **all-source** contract, not a claim that \(N\) is economical or that S150 has a certified \(\kappa\), invariant augmented set or global DAE branch.

**A physically interpretable exact positive and stronger failure than the D1 flag toy.** Take an ideal port capacitor \(C_0>0\) in parallel with two passive identical R–L branches, driven by the same terminal voltage \(u(t)\), with \(R,L>0\). Let \(s=i_1+i_2\), hidden differential \(d=i_1-i_2\). The full port measurement is \(I=C_0\dot u+s\). For **all continuous legal common voltage words** with unchanged symmetric branches,
\[
\dot s=(2u-Rs)/L,\qquad \dot d=-Rd/L.
\]
Thus \(s\) alone is an exact autonomous goal state for every future external signed work \(\int u(C_0\dot u+s)dt\) in this *symmetry-preserving* command class; nonzero hidden \(d\) is behaviorally irrelevant even if it has not been recovered. Moreover \(|s_u(t)-s'_v(t)|\le e^{-Rt/L}|\Delta s_0|+(2/R)(1-e^{-Rt/L})\|u-v\|_\infty\). On equal voltage samples a scalar quantizer mesh \(\rho\) updates with contraction \(e^{-Rh/L}\) and quantization recurrence \(r_{k+1}\le e^{-Rh/L}r_k+\rho/2\), conditional on a source-certified initialization from the **full** joint-CAL record.

If the **future legal action alphabet is enlarged** to a branch-1-only finite inductance intervention \(L\mapsto L+\delta\) with \(\delta>0\), and the initial hidden splits \(i_1=(s\pm a)/2,\ i_2=(s\mp a)/2\) are both source-legal under identical complete recorded PREP and full port CAL, the quotient breaks. Assume flux continuity at the change, \((L+\delta)i_1(0+)=Li_1(0-)\) (account for external actuator energy separately); drive with common constant \(u=U\) for time \(T\). Direct linear solution yields a **signed external work gap**
\[
|\Delta W|=\frac{|Ua|L}{R}
\left[e^{-RT/(L+\delta)}-e^{-RT/L}\right]>0.
\]
Hence any same full-port record-only scalar decoder for this *new* action class has minimax error at least \(|\Delta W|/2\); a full true-state oracle knows \(d\) but purchases extra hidden information and is not an ordinary at equal budget. Synthetic values \(L=5\)nH, \(\delta=0.2\)nH, \(R=0.1\Omega\), \(U=150\)V, \(a=1\)A, \(T=10\)ns give approximately \(47.416604269\) nJ difference (never an actual S150 number). If documented PREP forces \(d=0\), the branch-specific \(\delta\) is not a legal DPT intervention, or guard/flux-reset physics is different, the counterexample is **inapplicable**, not evidence for actual hidden memory. A legal zero-input dwell before the intervention shrinks \(|d|\) by \(e^{-Rt_p/L}\); with no other errors a \(\tau\)-goal requirement can be repaired without new sensor only when
\[
t_p\ge(L/R)\max\{0,\log(|\Delta W_0|/(2\tau))\},
\]
provided the changed preparation remains legal and its time cost is included. Any independent residual work bound must reduce the remaining \(\tau\) budget first. Alternative genuine branch current/flux measurement costs are separate; an N100 third observed voltage is not silently such a sensor.

**Primary literature, correctly limited.** Willems, “Dissipative Dynamical Systems Part I” (1972), §2 pp.323–327, motivates equivalence by **all future behavior**; van der Schaft, “Bisimulation of Dynamical Systems,” HSCC (2004), Definition 1 p.4 and Definition 4 p.12 require matching inputs/outputs and hybrid event occurrence, not merely a common point Jacobian. Pola, Girard & Tabuada, “Approximately Bisimilar Symbolic Models for Nonlinear Control Systems,” [arXiv:0706.0246](https://arxiv.org/abs/0706.0246), Theorems 4.1 (PDF p.6) and 5.1 (p.9), assume smooth δ-GAS/δ-ISS systems with explicit incremental bounds and quantized inputs; they do not establish switched electrothermal DAE root/guard or persistent-noise qualification. Hermann–Krener (1977) Theorem 3.1 is a local smooth observability-rank result, not global external-inverse sufficiency; F229/F376 finite-tree/real-flow construction assumptions are different. D2 is a **project-owned** sufficient construction plus passive-law comparator, not a literature theorem transplanted to SiC. The smallest Main decision-changing observation remains source-qualified **same digital PREP + full raw CAL/joint noise** hidden pair or certified same-source goal tube under a frozen lawful finite \(\Delta L\) word, alongside the strongest full-record ordinary. **Status SIDE_VERIFIED mathematics / actual physical new-word closure OPEN.**
