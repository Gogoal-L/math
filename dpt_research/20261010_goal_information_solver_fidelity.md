# DPT-R1 frontier note: goal information x solver fidelity (2026-10-10)

**Status: independent mathematics + synthetic executable tests; NOT a newly accepted native SiC result.** This note extends the 2026-10-09 research map and leaves S09, the controller's scientific authority, and native budgets unchanged.

## Why this is a potentially stronger research object

The current DPT-R1 has (a) actual-law, prospective 150/600 V command predictions, including ordered commands, (b) an Eth local consistent chart/lift with qualified numerical derivatives, (c) a fixed two-row Q summary with radius/goal dependence, and (d) same-law one-Newton predictions that are often close to a fully solved finite law. These are different resources:

1. **Predictive information:** which initial physical directions are indispensable for a specified collection of future goals and command words?
2. **Numerical fidelity:** once the information and constitutive law are fixed, how accurately must an implicit step/trajectory be solved to meet the same goal tolerance?

The proposed next object is a **goal-, horizon-, radius-, and solver-conditional information/computation boundary**. This is a research hypothesis for *actual SiC*; its two calculable mathematical components below are well-known types of finite-dimensional results, not claims of newly invented universal theorems.

## I. All-word minimal goal quotient for a fixed linear switched model

Assume one fixed common state chart, finite alphabet `A`, and an exact linear homogeneous model

```math
x_{k+1}=A_a x_k,\qquad g_k=Cx_k,\qquad y_0=Ox_0.
```

Each `A_a` must be a specified matrix **valid after every reachable admissible prefix**. This strong condition is not established by one Jacobian of a nonlinear DPT. The current observation `O` is known at preparation; it is not automatically an autonomously updating state.

Define row spaces

```math
W_0=\mathop{\mathrm{row}}(C),\quad
 W_{h+1}= W_h + \sum_{a\in\mathcal A} W_h A_a.
```

**Proposition (standard switched-linear realization/observability argument; elementary proof here).** The sequence stabilizes after at most `n-rank(C)` strict rank increments. Write its least fixed space as `W_*`, of dimension `d_*`, and choose any full-row-rank matrix `B` with `row(B)=W_*`. Then:

- `z=Bx` contains every future goal `C A_{a_k}...A_{a_1}x` of this model, for *all finite words*, even though the word set is infinite;
- each command has a well-defined **exact autonomous** reduced update `z'=M_a z` because `BA_a=M_a B`, and `Cx=Dz` for some `D`;
- `d_*` is **minimal among autonomous linear goal-only state representations valid for all x in R^n**;
- given already available noiseless preparation rows `O`, the minimum count of additional **arbitrarily designed scalar linear measurements** needed to recover all-word goal data is

```math
k_{\mathrm{free}}=\mathop{\mathrm{rank}}\begin{bmatrix}O\\B\end{bmatrix}-\mathop{\mathrm{rank}}(O).
```

**Proof.** `W_h` is nested, so any genuine strict step raises rank by at least one and rank is at most `n`. Equality `W_{h+1}=W_h` makes `W_h A_a \subseteq W_h` for all `a`, so it contains all word rows by induction. Choosing `B` as a basis of `W_*` gives `BA_a=M_a B` and `C=DB`. Conversely, any valid linear state `Px`, updated by all commands with output `Cx`, must have row(P) containing `C` and be invariant under all `A_a`; hence it contains `W_*`. The measurement formula follows by completing row(O) to span row(O)+`W_*`. □

The new `dpt_tools/goal_word_quotient.py` computes the iterative row-space basis without enumerating exponentially many words and reports both `d_*` and `k_free` plus reduced matrices and closure residuals. Each numerical rank is tolerance-dependent: finite floating-point ranks are **diagnostics**, not an interval-certified exact rank theorem.

**Counterexample: primitive adequacy does not imply BA adequacy.** For

```math
A=\begin{pmatrix}1&0&0\\0&1&1\\0&0&1\end{pmatrix},\quad
 B=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix},\quad C=O=(1,0,0),
```

`C e3=CA e3=CB e3=0`, while `CBA e3=1`. For words of length at most `0,1,2`, ranks of goal information are `1,2,3`; missing free linear measurement counts beyond O are `0,1,2`. An extra hidden direction is exposed only by command A followed by B. The demonstration is exact algebra, not a DPT-native BA claim.

**DPT bridge and falsifier.** Construct *common-chart* transition Jacobians only after composing the qualified Eth lift, moving-event derivatives and all coordinate transforms. With the genuinely prefix-dependent nonlinear native map, do **not** pretend that one constant `A_a` works globally. If such a fixed-switching approximation fails an admissible two-command sensitivity replay, treat that as evidence for **mode-/prefix-indexed derivatives or nonlinear finite-radius analysis**, not an excuse to remove the counterexample. For actual archived ordered commands, the finite-word pathwise Jacobians are the correct initial evidence, and the all-word quotient is a strong **conditional comparator** to attempt only once its fixed-model contract is met.

## II. Conditional goal certificate from an implicit same-law residual

Suppose a previously frozen preparation and future command induce a *square smooth* implicit system `F(y)=0` on one qualified branch. Here `y` may contain one BE stage or the **entire stacked stage trajectory** after a legal consistency lift. Evaluate the full-law residual and Jacobian at a cheaper predicted state `yhat`:

```math
r=F(\widehat y),\quad J=DF(\widehat y),\quad q=Dg(\widehat y).
```

Assume, in a complete closed ball `B(yhat,R)` contained in the *same smooth physical/DAE branch*:

- `J` is invertible, with independently established `||J^{-1}||_2 <= beta`;
- `||J^{-1}r||_2 <= eta`;
- `||DF(u)-DF(v)||_2 <= L ||u-v||_2` for all points of the ball;
- for a **scalar smooth goal** `g`, `||D^2 g||_2 <= H_g` throughout the ball.

Let `h=beta*L*eta`. For `h<=1/2`, set

```math
\rho=\frac{2\eta}{1+\sqrt{1-2h}}\qquad (\rho=\eta\text{ when }L=0).
```

If `rho<=R`, the standard Newton--Kantorovich result supplies a nearby full-law root `y*` with `||y*-yhat||<=rho` (with the usual domain hypotheses). Solve one adjoint system `J^T lambda=q^T`. Then our elementary **goal-specific correction and remainder** is:

```math
\boxed{
 \left|\,[g(y^*)-g(\widehat y)]+\lambda^T r\,\right|
 \le \tfrac12(\|\lambda\|_2 L + H_g)\rho^2 .
 }
```

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

### Exact information lower bound before any solver choice

For a declared history/model class `H`, scalar future goal `G`, observation map `O` and deterministic norm-bounded noise `||e||<=sigma`, set

```text
H_y := {h in H : ||O(h)-y|| <= sigma}
Omega := sup over feasible y of [sup_{h in H_y} G(h) - inf_{h in H_y} G(h)].
```

If the scalar goal is bounded on each nonempty fiber, the deterministic *best possible* worst-case scalar prediction error from the noisy observation is **exactly `Omega/2`**. Proof: for any feasible `y`, the predictor cannot distinguish the extreme histories in `H_y`, hence suffers at least half their goal gap; the midpoint of the fiber goal interval attains that bound, even when extrema are not attained (use inf/sup). This is the scalar Chebyshev-center / radius-of-information argument from classical optimal recovery, not an OpenAI-specific theorem. If `Omega > 2 delta`, then **no solver precision, Newton iteration, or model refit can guarantee worst-case tolerance `delta` from those observations**. A close full-law root does not remove information ambiguity.

Conversely, even if `Omega/2 <= delta`, a computationally implemented predictor still needs a separate approximation/solver budget. For a method that actually approximates the ideal fiber midpoint with uniform scalar error `epsilon_comp`, its end-to-end model-class error is bounded by `Omega/2 + epsilon_comp`. The `implicit_goal_certificate.py` provides a per-history full-law goal correction for a smooth implicit solve; **it is not automatically a uniform certificate for the fiber midpoint**. Distinguish these two numerical objects before combining bounds.

This gives an explicit **necessary information gate** preceding a separate **sufficient solver gate**. It improves the scientific decision: a goal-fiber collision calls for a new legitimate observation/repair, while a small information radius but large implicit solver residual calls for a better numerical method. The existing `goal_ambiguity_audit.py` computes the exact scalar finite-bank version and remains the right zero-fresh first tool.

Closest prior: [optimal recovery with inaccurate observations](https://doi.org/10.1016/j.jco.2024.101841) and [Chebyshev-center optimal learning](https://doi.org/10.1016/j.sysconle.2023.105648). For DPT, `H` must be a valid reachable preparation family, not an arbitrary box of internal parameters.

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

---

## Legacy MAP derivations: goal peak and actual BE charge/solver bounds (M30–M39)

These numbered derivations are source-conditional; they do not constitute a complete vendor-law SiC certificate. The formula IDs are preserved from the immutable [historical MAP](https://github.com/Gogoal-L/math/blob/15b3fde162b2f7cb729ec106b847be1ad046d222/DPT_MATH_RESEARCH_MAP.md).

### 0.9 用不光滑工程目标反向检验：peak 值可稳定，但 peak 时间不一定稳定

**新的正向救援：** 18B 已揭示 peak/event 对历史很敏感；但这并不要求每一种 peak-value 预测都满足唯一、非退化峰的条件。对共享同一个合法物理时间窗口 $`[a,b]`$ 的两条连续电压波形 $`V_1,V_2`$，仅从 max 的基本定义就有

**(M30)**

```math
\boxed{\left|\max_{t\in[a,b]}V_1(t)-\max_{t\in[a,b]}V_2(t)\right|
\le \|V_1-V_2\|_{L^\infty[a,b]}.}
```

**推导：** 对任意 $`t`$，$`V_1(t)\le V_2(t)+\|V_1-V_2\|_\infty`$；取两端的 supremum 得到一侧不等式，交换 1/2 得另一侧。无论 ringing 在两处几乎等高、argmax 因微小扰动从第一个峰跳到第二个峰，**peak 值**仍然 1-Lipschitz 于完整波形 sup norm；**峰出现时间**则完全可能跳变，必须另给事件分支选择与横截条件。若工程目标是 overshoot $`V_{\rm peak}-V_{\rm DC}`$，还要对 bus voltage 基准差另加 $`|\Delta V_{\rm DC}|`$。这为 Pro18B 提供一个比强行拟合稳定 peak-event time 更经济的潜在证明路线：先证准许历史域内的完整波形 sup norm 界，再直接给 peak-value 上界。

同一固定窗口的 stage work 也具有无需微分求峰时刻的通用目标上界。利用 $`V_1I_1-V_2I_2=I_1(V_1-V_2)+V_2(I_1-I_2)`$，积分与 Hölder 给

**(M31)**

```math
\boxed{|W_1-W_2|
\le (b-a)\left[
\|I_1\|_\infty\|V_1-V_2\|_\infty+
\|V_2\|_\infty\|I_1-I_2\|_\infty
\right].}
```

这两式提供可复用、目标相关的**充分上界**，但可能比伴随积分的 signed cancellation 松很多；已观察到 18B 两个阶段 work 几乎相消时，应同时报告 stage-wise bound 与直接 signed total-work estimator，不能把逐阶段绝对盒和当成必要误差下界。若窗口随 guard/events 移动，仍需式 (M21–M22) 的边界项与 guard 资格。

**反例：只做一阶 rank/quotient 测试可能把二阶 goal ambiguity 漏成零。** 考虑严格合法的数学状态圆盘 $`\mathcal H_r=\{(x,y):x^2+y^2\le r^2\}`$，现有观测 $`O(x,y)=x`$，未来目标 $`G(x,y)=y^2`$。在中心 $`DG(0,0)=(0,0)`$，且 $`DO(0,0)=(1,0)`$，**一阶 goal-row 缺口为零**；但固定观测 $`O=x`$ 时，$`0\le G\le r^2-x^2`$，所以条件最坏误差精确是 $`(r^2-x^2)/2`$，全域最优 minimax 半径为

**(M32)**

```math
\boxed{R_{\mathcal H_r}(O,G)=\frac{r^2}{2}>0,\qquad
DG(0,0)|_{\ker DO(0,0)}=0.}
```

实现该半径的解码器可取 $`\widehat G(x)=(r^2-x^2)/2`$。这是一个**明确可计算的二阶漏信息反例**，展示“局部一阶 target 不可见方向的 DG=0”不等于有限半径 goal recovery。对于沿精确 observation fiber 的光滑曲线 $`h(t)`$，记 $`h_0=h(0)`$、$`v=h'(0)`$、$`a=h''(0)`$。若 $`DG(h_0)[v]=0`$，则二阶 goal 变化一般仍为

**(M33)**

```math
\begin{aligned}
\left.\frac{\mathrm d^2}{\mathrm dt^2}G(h(t))\right|_{t=0}
&=D^2G(h_0)\bigl[v,v\bigr]\\
&\quad+DG(h_0)\bigl[a\bigr].
\end{aligned}
```

因此要从 18C 的 source Jacobian 读出有限 CAL chart 的可靠预测，需要**连同 observation-fiber 曲率/合法域与 goal 余项**一并约束；某一中心的 rank=0 不自动升级为非零域 sufficient information。反过来，如果直接的 $`L^\infty`$ 波形包络已经足够小，式 (M30–M31) 可能不用支付高阶参数重构的代价。这是两个真正可判别的研究分支，而不是再列一批候选文献。

---

### 0.10 从 IH2662 V6 实际耦合 BE 本构导出 charge surrogate 的严格余项（600-V source model）

前面 (M13–M20) 将非线性实际 law 的余项留作 $`\beta`$；下面不再停留于抽象 $`D^2G`$。用户提供的《IH2662 DPT Research Design V6》§4.7 明确给出了**后续 600-V coupled backward-Euler evaluator** 的 body-diode conduction/storage 支路（位于指数、charge 和 breakdown guards 内）：

**(M34)**

```math
\begin{aligned}
i_{\rm cond}(v_j)&=I_s\bigl(e^{v_j/a}-1\bigr),\\
q_D(v_j)&=\tau I_s e^{v_j/a},\\
R^{\rm full}_{D,n}
&=i_{b,n}-i_{\rm cond}(v_{j,n})\\
&\quad-\frac{q_D(v_{j,n})-q_D(v_{j,n-1})}{h_n}.
\end{aligned}
```

此处 $`\tau=2\,\mathrm{ns}`$、$`a>0`$ 是相关固定温度 branch 的 emission-factor thermal voltage；V6 中强 evolving-affine 对手在合法 BASE 电压 $`\bar v_n`$ 取 $`q_D^{\rm aff}(v)=q_D(\bar v)+q'_D(\bar v)(v-\bar v)`$。令 $`\delta v=v-\bar v`$，直接代入指数原函数得到**恒等式**：

**(M35)**

```math
\boxed{
q_D(v)-q_D^{\rm aff}(v)
=q_D(\bar v)\!\left(e^{\delta v/a}-1-\frac{\delta v}{a}\right).
}
```

没有从 Boolean F132 借用任何曲率常数。由于 $`e^s\ge1+s`$ 且 $`|\delta v|\le d`$ 时指数 Taylor 余项的最大值在 $`\delta v=+d`$ 端点，得到该**固定 BASE、固定 $`a,I_s,\tau`$ 的 sharp uniform bound**：

**(M36)**

```math
0\le q_D(v)-q_D^{\rm aff}(v)
\le \underbrace{q_D(\bar v)\bigl(e^{d/a}-1-d/a\bigr)}_{\epsilon_q(d;\bar v)}
\le\frac{q_D(\bar v)}2e^{d/a}(d/a)^2.
```

第二个不等式由积分余项 $`e^s-1-s=s^2\int_0^1(1-t)e^{ts}\,dt`$ 给出。数值量纲核查：$`d/a=0.2`$ 时 sharp charge remainder 为 $`0.02140275816\,q_D(\bar v)`$；若 $`d/a=1`$，则为 $`0.71828182846\,q_D(\bar v)`$。因此不能因为某段 gate 电压变化“看起来较小”就默认 affine-storage 精度足够；真正支配量是控制电压位移相对于本构热尺度 $`a`$ 的比值。这里没有将这些无量纲示例误写为 V6 已实测的实验误差。

若 BE 残差中当前与前一步 charge 均以各自 evolving-affine law 代替，从 (M34–M35) 逐项相减，有

**(M37)**

```math
R^{\rm full}_{D,n}-R^{\rm aff}_{D,n}
=-\frac{\delta q_n-\delta q_{n-1}}{h_n},
\qquad
|R^{\rm full}_{D,n}-R^{\rm aff}_{D,n}|
\le\frac{\epsilon_{q,n}+\epsilon_{q,n-1}}{h_n}.
```

若前一步 storage 值保留 actual full-law charge，只需 $`\epsilon_{q,n}/h_n`$；电流误差的单位由 $`\mathrm C/\mathrm s=\mathrm A`$ 检查。若 thermal $`a`$ 随模拟状态变化、BASE 未预先冻结或跨越 branch/guard，该单一 $`\epsilon_q`$ 不能当作全 coupled residual 的一致上界，必须重新覆盖这些真实状态维度。

**从 local storage defect 真正传到工程目标还需要哪条桥？** 对完整**同一**离散 source residual $`F(x)=0`$，在某个具名全状态合法凸盒 $`B_\rho(c)`$ 中寻找可验证近逆 $`H`$，满足

**(M38)**

```math
\begin{aligned}
\|I-HJ_F(x)\|_{\rho,\infty}
&\le\kappa<1\quad(x\in B_\rho(c)),\\
\|HF(c)\|_{\rho,\infty}&\le1-\kappa.
\end{aligned}
```

最后一个条件这里的规范化盒半径定义为 $`\|x-c\|_{\rho,\infty}\le1`$。则 $`T(x)=x-HF(x)`$ 把该盒映入自身且收缩，有唯一合法 root $`x^\star`$，并且

**(M39)**

```math
\begin{aligned}
\|x^\star-c\|_{\rho,\infty}
&\le\frac{\|HF(c)\|_{\rho,\infty}}{1-\kappa},\\
|G(x^\star)-G(c)|
&\le L_G\frac{\|HF(c)\|_{\rho,\infty}}{1-\kappa}.
\end{aligned}
```

第二式假设在同盒内 $`G`$ 对相同加权范数有统一 Lipschitz 常数 $`L_G`$，其 guard、事件与积分窗口都已合格。**证明结构**是 Banach 自映射与收缩，加上 $`G`$ 的统一一阶增益；不是当前 600-V vendor 源已通过该完整 box 的宣告。把 (M37) 传入 $`\|HF(c)\|`$ 时还需其余 nodal/charge/network/thermal residual rows、共享 previous-state 相关性与完整伴随/goal 传播，不能只对一个 diode scalar 宣称全波形误差。

这条 (M34–M39) 是对**已提供实际耦合 BE 本构**的条件余项建设：F132 提醒不可漏组合项；F119 提醒不能用不合格噪声独立性；F129 提醒 previous-step charge 及合法命令历史影响后继响应。**数学计算来自指数电荷方程自身**；不是将任何 F119/F129/F132 的原定理直接移植到 SiC。该结果对应 V6 **600 V coupled BE branch**，与先前 150-V reference-completed trapezoidal descriptor 分开，不共享求解/物理资格。
