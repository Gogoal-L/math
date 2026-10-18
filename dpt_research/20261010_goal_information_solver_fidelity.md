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

## 2026-10-17 addendum: full-PREP work/slope certificate (S-L1–S-L4)

**Scope and units.** The following is independent DPT calculus, inspired by F266's certificate *architecture*; it is not the MUB theorem or a source-verified SiC result. Fix one source reference, the complete **pretarget** digital command, a legal preparation protocol, a frozen future command, terminal port orientation, fixed-grid/window signed-work rule and one smooth guard/DAE branch. All derivatives are taken in stated, physically scaled coordinates. Here $`L`$ has units H, $`W`$ has units J, $`W_L`$ has J/H and $`W_{LL}`$ has J/H$`^2`$.

**S-L1 (the prepared-state contribution is exact under regularity).** Let $P(z,L)=0$ describe the complete legal preparation, $F(X,z,L)=0$ the stacked future residual and $W=G(X,z,L)$ the frozen signed terminal work. If $P_z,F_X$ are invertible along a smooth, source-consistent continuation, solve $F_X^\top\lambda=G_X^\top$. Then
```math
\frac{dW}{dL}=
\underbrace{G_L-\lambda^\top F_L}_{\text{fixed-entrance future response}}
-\underbrace{(G_z-\lambda^\top F_z)P_z^{-1}P_L}_{\text{legal PREP transport}}.
```
Indeed $z_L=-P_z^{-1}P_L$ and $X_L=-F_X^{-1}(F_L+F_z z_L)$; substitute in $dG/dL$. If $z=S(H,L)$ is a readout of prepared history $P(H,L)=0$, include the **explicit** $S_L$ term. The decomposition is parametrization- and preparation-protocol-dependent, not an intrinsic physical or causal allocation. A post hoc initial-condition splice, changing active set, moving guard/event, solver grid or inconsistent DAE algebraic initial state is outside these assumptions.

**S-L2 (joint work–slope envelope and sharp two-world obstruction).** For a nonempty set $`\mathcal H_y`$ of source-legal worlds compatible with the **same complete pretarget** command/CAL observation $`y`$, let $`w_h=W_h(L_0)`$, $`s_h=W'_h(L_0)`$ and let one independently source-certified $`M\ge\sup_{h\in\mathcal H_y,\,|\ell-L_0|\le r}|W_h''(\ell)|`$ hold along each legal future continuation. Define the *joint* feasible pair set $`\mathcal Z_y=\{(w_h,s_h):h\in\mathcal H_y\}`$ and its support endpoints $`a(\delta)=\inf_{\mathcal Z_y}(w+\delta s)`$, $`b(\delta)=\sup_{\mathcal Z_y}(w+\delta s)`$. For $`|\delta|\le r`$,
```math
\begin{gathered}W_h(L_0+\delta)\in\\\left[a(\delta)-\frac12M\delta^2,b(\delta)+\frac12M\delta^2\right],\\R_y(\delta)\le\frac{b(\delta)-a(\delta)}2+\frac12M\delta^2\end{gathered}
```
This follows by Taylor's theorem **for every eligible history** followed by infimum/supremum; the interval midpoint is a pretarget predictor with the displayed worst-case upper bound. A guaranteed $\tau$-adequate prediction needs the right-hand side $\le\tau$. Pairwise lower witnesses remain valid: any two eligible histories with $|(w_h-w_{h'})+\delta(s_h-s_{h'})|>2\tau+M\delta^2$ refute $\tau$-adequacy. Keeping $(w,s)$ **joint** can be much sharper than combining separate $w$ and $s$ boxes; for pairs $(1,-1),(-1,1)$ at $\delta=1$, the joint linear goal is identically $0$, while the independent box gives $[-2,2]$.

To compute $s_h$ without a new solver, stack **all PREP + switching** residual rows as $\mathcal F(X,L;h)=0$ with $A=\mathcal F_X$ and solve $A^\top\lambda=G_X^\top$: $s_h=G_L-\lambda^\top\mathcal F_L$. Every backward-Euler mass/stamp term, previous-state derivative, prepared history and readout window belongs to this full derivative. With $J=-A^{-1}\mathcal F_L$, the conditional curvature is
```math
\begin{gathered}W''=G_{LL}+2G_{XL}J+G_{XX}[J,J]\\-\lambda^\top(\mathcal F_{LL}+2\mathcal F_{XL}J\\+\mathcal F_{XX}[J,J])\end{gathered}
```
A pointwise floating Hessian or a finite collection of observed worlds does not supply the uniform $M$, the continuous set $\mathcal Z_y$, root existence or guard coverage. Compare on the **same information, source tube and goal** against full-source forward/adjoint and calibrated full-record ordinary predictors.

**S-L3 (F266-inspired centered normal-error bound; conditional independent lemma).** Let $z=(X,L)\in\mathbb R^{n+1}$ and $\mathcal F:\mathbb R^{n+1}\to\mathbb R^n$, with a dimensionless scaled norm specified for unlike physical units. At a center $c$ choose a unit approximate tangent $t$ with $t_L\ne0$ and a preconditioner $M_0\in\mathbb R^{(n+1)\times n}$. Put $J_c=D\mathcal F(c)$,
```math
\begin{gathered}\alpha=\|I-tt^\top-M_0J_c\|,\quad n_0=\|M_0\mathcal F(c)\|,\\s=DG(c)t/t_L,\quad b=\|DG(c)-s e_L^\top\|\end{gathered}
```
Assume every eligible exact root $c+d$ lies in one source-certified smooth, guard-consistent ball $\|d\|\le R$, that $\|M_0(\mathcal F(c+d)-\mathcal F(c)-J_c d)\|\le C\|d\|^2$ there and $\|D^2G\|\le H_G$. Then
```math
|G(c+d)-G(c)-s\,d_L|
\le b(n_0+\alpha R+CR^2)+\tfrac12H_GR^2.
```
**Proof:** $e=(I-tt^\top)d=(I-tt^\top-M_0J_c)d-M_0\mathcal F(c)-M_0R_F(d)$ at any root, so $\|e\|\le n_0+\alpha R+CR^2$; $DG(c)-s e_L^\top$ annihilates $t$. Apply Taylor to $G$. Neither this lemma nor F266 **establishes root existence**; a verified covering of the legal continuation and source/guard remainder are separate obligations. F266 Definition 4.1, Lemmas 4.3–4.4, Propositions 4.5–4.6 and Theorem 7.1 provide the original certificate pattern with separate global/computational obligations; its MUB and selected Lean scopes do not transfer to DPT.

**S-L4 (exact analytic checks and falsifiers, all synthetic).** For unit-step BE $Li'+i=1$, legal one-step PREP $(L+1)i_0=1$, two future steps $(L+1)i_k-Li_{k-1}=1$ and $W=i_1+i_2$, exact substitution gives $W=(5L^2+6L+2)/(L+1)^3$. The fixed-entrance and PREP derivatives are respectively $-L(3L+1)/(L+1)^4$ and $-L(2L+1)/(L+1)^4$. On $L:1\to2$ their integrals are $-137/648$ and $-25/162$, summing to $\Delta W=-79/216$. The first-order remainder about $L=1$ equals $31/432$: using only the point curvature $|W''(1)|=1/8$ falsely promises $1/16$, while a **validated interval** curvature cap $M=1/6$ promises $1/12$ and covers it. Independently, $\mathcal F_a(X,L)=X-a(L-L_0)^2$, $G=X$ has the *same center residual and tangent* for every $a$ but arbitrary finite $\Delta W=a\delta^2$; source curvature enclosure is indispensable. For slope information, worlds $h=\pm1$ with $\mathcal F_h=X-h(L-L_0)$, $G=X$ and equal pretarget observation share $w_h=0$ and $M=0$ yet produce future goals $\pm\delta$; every scalar decoder has radius at least $|\delta|$.

**Controller interface and current status.** Supply actual source/model+reference, legal PREP and complete pretarget command, qualified stacked current/previous derivatives, signed terminal-work scorer with physical units and ports, branch/guard/timebase, the entire compatible-history $(w_h,s_h)$ support or certified enclosure, uniformly verified $M$, sensor joint nuisance and a same-information full-record ordinary comparator. Local DPT derivations already include S02 parameter-curvature mathematics and scoped two-step actual-source results; do not relabel those as this **whole source/fiber** certificate. A failure of a particular full-fork Banach sufficient test does not prove the physical DAE has no solution. **Mathematical theorem/analytic fixture: SIDE_VERIFIED; actual whole-source/future command guarantee: OPEN_RESEARCH.** See [existing implicit certificate](../dpt_tools/implicit_goal_certificate.py), [ordered goal transport](../dpt_tools/goal_defect_transport.py) and [transfer falsifier tests](../dpt_tools/test_paper_transfer_falsifiers.py).

## 2026-10-17 goal-corrected residual cell certificate (S-L5): an alternative to separate state/observation bounds

**The target is the *actual same-law prediction error*, not parameter recovery.** Freeze one source family, the original sensor operator/time stamps and full **pretarget** recorded CAL command, a predictor $p$ fitted without the future target, and an unseen-command scalar **signed external terminal work** $G$. Include complete legal PREP, charge/storage, future source steps and the fixed goal readout in a stacked residual $F(X,\xi)=0$. Use dimensionless scaled coordinates $\xi$ for any physical parameter (e.g. $\xi=(L-L_0)/L_{\rm scale}$); $X$ is the jointly prepared state/trajectory and $O(X,\xi)$ is the original pretarget external CAL observation. On a connected **source-validated** smooth guard/DAE branch with $A=F_X$ invertible and exact root $X(\xi)$, define
```math
Q(X,\xi)=G(X,\xi)-p(O(X,\xi)),\qquad R_p(\xi)=Q(X(\xi),\xi).
```
The associated adjoint uses the **corrected-goal covector** $Q_X=G_X-Dp(O)O_X$, not $G_X$ alone. Solving $A^\top\lambda=Q_X^\top$ and $X'=-A^{-1}F_\xi$ gives the following independently proved **conditional exact identities**:
```math
\begin{gathered}R_p'=Q_\xi-\lambda^\top F_\xi,\\R_p''=D^2Q[(X',1),(X',1)]\\-\lambda^\top D^2F[(X',1),(X',1)]\end{gathered}
```
Proof: differentiate $F(X(\xi),\xi)=0$ once and twice, substitute in the chain rule for $Q$. Every mixed current/previous Hessian and PREP derivative remains in the full stacked $D^2F$, while $D^2Q$ includes the nonlinear projective readout curvature $D^2p(O)$. These formulae establish **point derivatives only** until actual source-legal intervals have verified root existence, identical goal/port/timebase, invertible $F_X$, guard coverage and *uniform* remainder bounds.

**A useful scalar certificate without an independently huge $\|X-X_0\|$ multiplier.** Cover the claimed legal $\xi$ interval with finitely many certified intervals $I_j$ centered at $\xi_j$ and halfwidth $h_j$; certify $X(\xi)$ on **every point** of each $I_j$, $M_j\ge\sup_{I_j}|R_p''(\xi)|$, and the center error $|R_p(\xi_j)|\le e_j$ using an exact source goal or independently verified a posteriori root/goal enclosure. Then
```math
\boxed{\ \sup_{\xi\in\bigcup I_j}|G-p(O)|
\le \max_j \left(e_j+|R_p'(\xi_j)|h_j+\frac{M_j}{2}h_j^2\right).\ }
```
Unlike separately bounding $G$ and $O$ before subtracting, this uses their **shared source and correlated first-/second-order variation**. If the raw pretarget observation is $y=O+e$ with the *qualified joint* sensor-error set $E$, add the separately pretarget-computable support $\sup_{e\in E}|p(O+e)-p(O)|$ uniformly in the actual admissible $O$; for a frozen affine $p(O)=c+\ell^\top O$ this is the exact symmetric support $\sup_{e\in E}|\ell^\top e|$. Existing full-record/source-law ordinary and physical acquisition costs remain the comparison. This is a covering method, not a claim that a cheap source-wide root cover exists; a one-dimensional $L$ interval does **not** certify the controller's multivariate S150 D3 bank.

**Exact synthetic cancellation oracle and failure gate.** On $\xi\in[0,1]$, let $F(x,\xi)=x-1000\xi-\xi^2$, $G=x+\xi^2$, $O=(999/1000)x$ and frozen $p(y)=y$. The exact source root gives
```math
\begin{gathered}R_p(\xi)=\xi+\frac{1001}{1000}\xi^2,\quad\lambda=\frac1{1000},\\R_p'(\xi)=1+\frac{2002}{1000}\xi,\\R_p''=\frac{2002}{1000}\end{gathered}
```
One certified cell centered at $\xi=1/2$, $h=1/2$ yields a **sharp** upper $R_p(1)=2001/1000$ despite individually order-1000 changes in $G$ and $O$. A separate naive triangle for these two readings loses the cancellation. The example is pure dimensionless algebra, **not** S150 volt/current scaling or evidence of qualified DPT coverage. If source-root/guard enclosure fails, $M_j$ is just a point Hessian, $p$ was fitted to the heldout work, or sensor gain/noise is omitted, return INCONCLUSIVE rather than a bound. [Three independent exact analytic checks](../dpt_tools/test_paper_transfer_falsifiers.py) establish this fixture.

**Named controller consumer.** The local 2026-10-17 derivation ledger's 150-V Goal27 already has a certified *fractional-linear proxy-bank* error upper but lacks uniform **actual nonlinear** $G-p(O)$ coverage. The smallest potentially decision-changing handoff is its existing saved same-source PREP/CAL/target checkpoints and frozen $p$, plus qualified actual $F_X,F_\xi,D^2F$, the complete $O/G$ readout and joint noise, cell root/guard certifiers, and exact/interval center defects. A verified $R_p$ envelope may permit a bounded, *goal-specific* source claim even if an earlier global all-state self-map sufficient test remained inconclusive. It cannot bypass source reachability, physical source-vs-native discrepancy, or Main authorization. Existing [implicit goal certificate](../dpt_tools/implicit_goal_certificate.py), [implicit Hessian audit](../dpt_tools/implicit_goal_hessian.py), and [goal-fiber recovery](../dpt_tools/fiber_goal_curvature.py) should be reused; a new runtime tool is unwarranted until actual inputs and a stringent ordinary test show benefit. **Status: independent conditional algebra SIDE_VERIFIED, three synthetic tests; actual source-uniform bound OPEN_RESEARCH.**

## 2026-10-17 goal-Lagrangian source-root enclosure (S-L6): a functional certificate without global inverse bounds

**Independent conditional DPT lemma (not actual SiC validation).** Fix source reference and law, legal full PREP+CAL and future command, recorded pretarget data, frozen scalar signed-work goal $G$ (J), actual pretarget observation $O$, and predictor $p$ fitted without the withheld target. Let $F(Z,\theta)=0$ stack the **entire** prepared source, charge/thermal, algebraic and previous-state residuals on the correct guard/readout path, and define $R=G-p(O)$ (J). The residual rows carry different physical units, so multiplier component $\lambda_j$ has units J/(unit of $F_j$).

For each legal parameter/history cell $C$, suppose an **independently validated** outer set $B_C$ contains every physically admissible *exact* root $(Z,\theta)$ under the declared source law, command and guard. No uniqueness or regular inverse bound is assumed. If a fixed, pretarget-computed multiplier $\lambda_C$ and verified exact/interval evaluation establish
```math
\sup_{(Z,\theta)\in B_C}|R(Z,\theta)-\lambda_C^\top F(Z,\theta)|\le\epsilon_C,
```
then all compatible legal exact roots obey $|G-p(O)|\le\epsilon_C$. A finite verified cover over the full stated domain yields the upper $\max_C\epsilon_C$. **Proof:** at each true root $F=0$, substitute into the inequality. The outer cover can be much larger than the set of roots and may be established by valid physical/source enclosures, but must include **every** eligible source root. This lemma neither proves existence, correct branch selection nor the validity of the source relative to native/hardware. Unlike a standard whole-state Kantorovich certificate, it does not require uniqueness, a uniform $F_Z^{-1}$, or a Banach self-map $q<1$; an arbitrary guessed box is no valid substitute for independently justified root inclusion.

**Existing Goal27 proxy to actual-source gap.** Preserve the controller's accepted fractional-linear normalized five-current proxy on the declared S150 bank. It has a scoped uniform noise-free fixed-predictor bound $\epsilon_{\rm aff}=0.876578434279\,{\rm nJ}$ *in the proxy*, not in the actual nonlinear source. Define the joint model-error functional
```math
\Phi(Z,\theta)=\big[G_{\rm actual}(Z,\theta)-p(q_{\rm actual}(Z,\theta))\big]
-\big[G_{\rm aff}(\theta)-p(q_{\rm aff}(\theta))\big].
```
If all actual source roots are in certified $B_C$ and one verifies $\sup_{B_C}|\Phi-\lambda_C^\top F_{\rm actual}|\le\delta_C$ across the claimed bank, then at each root the **actual same-source** prediction error satisfies
```math
|G_{\rm actual}-p(q_{\rm actual})|\le\epsilon_{\rm aff}+\max_C\delta_C .
```
This preserves correlation between future signed work and the original pretarget observation, potentially reducing the inflation of separate model-output and observation bounds. Adjoint covectors $\lambda$ from the corrected goal derivative $\Phi_Z$ and full PREP source $F_Z$ are candidates, but only uniform verified interval residuals make the claim. **P0 denominator and root-cover prerequisite.** The actual normalized sensor is rational: $q_{\rm actual}$ requires the true full-source $D_{\rm actual}=I_{60}-I_{12}$ to remain nonzero, with its sign and 100-MHz filter/PREP initial state qualified **across the entire actual root cover**. The accepted proxy interval $D_{\rm aff}\in[5.3726858484,5.5505454704]$ A proves neither actual positivity nor avoidance of the real pole. The original six-parameter S150 bank is $(a_1,a_2,a_3,L,\kappa,b)$ with radii $(.14,.14,.14\,\mathrm V,.28\,\mathrm{nH},.018,10\,\mathrm{MHz})$ and both CAL/target branches share the lawful prepared endpoint. A valid outer cover must include the *full 126-step PREP, 4800-step CAL and 6720-step target*, all 50 source equations, previous/current charge, GL32 corrections, thermal/heat, guard and scored output. Certified local active-step boxes/finite samples are not a global cover; subdivide by source/denominator branch before interval evaluation. If numerical residuals are approximate rather than exact, bound the additional $|\lambda^\top r_{\rm numerical}|$ with correct physical units and outward rounding; do not hide that error inside an exact-root identity.

Real sensor readings require an additional **joint** gain/offset/filter/noise support $\sup|p(q_{\rm obs})-p(q_{\rm actual})|$; nominal synthetic sensor budgets cannot be promoted to instrument error.

**Exact synthetic adversary to the old sufficient test.** Let $F=(x+y^2-1,10^{-3}y)$, $G=x+y^2$, $p\equiv1$, and let a certified source outer box include the root $(1,0)$ and $y\in[-1,1]$. With $\lambda=(1,0)$, $G-p-\lambda^\top F\equiv0$ throughout the box: the goal is exactly 1 for every true source root. Yet a natural center inverse has norm $\ge10^3$ and $\|I-J_0^{-1}DF(x,y)\|_\infty=2|y|$, whose supremum is 2, so its sufficient contraction gate fails. This proves one conditional goal bound can succeed where that **particular** full-state sufficient test fails; it says nothing about how tight an actual Goal27 multiplier can be. [Exact independent tests](../dpt_tools/test_paper_transfer_falsifiers.py) check the algebra and root-cover caveat.

**Original-literature comparison and remaining source inputs.** This is an elementary source-residual duality statement, not a universal new a-posteriori theory. [Chaudhry–Lewis–Molla (2025)](https://arxiv.org/abs/2507.03712) derives adjoint QoI representations for semi-explicit index-1 / Hessenberg index-2 DAEs; [Sharma–Bartel–Schaller (2026)](https://arxiv.org/abs/2605.14082) addresses energy-balance DWR for **linear index-1 port-Hamiltonian** DAEs with consistent initial data, assumptions unverified for nonlinear clipped/switched SiC. **Primary-source inconsistency requiring clarification:** in [arXiv v1 Assumption 2.1(a)–(b)](https://arxiv.org/html/2605.14082v1#S2), $E$ is declared singular with $\mathrm{rank}(E)=r<n$, while $E^\top Q$ is simultaneously asserted to be symmetric **positive definite on all $\mathbb R^n$**, $Q$ nonsingular. This literal combination is algebraically impossible since $\mathrm{rank}(E^\top Q)\le r<n$. A PSD full descriptor with an SPD reduced differential block might be intended, but must not be silently substituted for the printed assumption; until corrected, no theorem is imported as an S150 certificate. To pursue actual source coverage, Main need only supply existing lawful full PREP+CAL/target checkpoints, original F/G/q/p and joint sensor contract, plus a justified full-domain outer source cover and interval evaluator for the correlated functional. Compare the resulting signed bound against the strongest same-information full-record ordinary and the cost of whole-fork root certification. Until then mathematical SIDE_VERIFIED / actual-source OPEN_RESEARCH; no automatic MAIN_ACCEPTED.

## 2026-10-17 S-L7: homogeneous root-only certificate for a rational observation (separate from S-L6)

**New proof obligation, not an actual-source certificate.** Retain the exact same legally prepared source-root equation $F(Z,\theta)=0$, original five sampled CAL currents, frozen source signed external goal $G$ (J) and affine projective readout $p(q)=g_0+\ell^\top(q-q_0)$, $\ell$ in J per dimensionless ratio. Define $D=m_{60}-m_{12}$ (A), $B=(m_{31}-m_{12},m_{42}-m_{12},m_{46}-m_{12})$ (A), and the **denominator-cleared joint goal numerator**
```math
N=D\,[G-g_0+\ell^\top q_0]-\ell^\top B \qquad [N]=\mathrm{J\,A}.
```
The identity $G-p(B/D)=N/D$ is exact only where $D\ne0$. To avoid demanding that $B/D$ be even *defined* on a loose off-source interval box, select a physical/source-qualified set $K$ containing **every** admissible exact joint PREP+CAL+target root and all legal parameters/modes. Suppose outward interval arithmetic or exact symbolic identities certify on **all of $K$** a positive scalar $d_0$ (A), error $\epsilon$ (J), and residual multipliers $\mu,\nu_+,\nu_-$ with the three signed inequalities
```math
\begin{gathered}D-d_0-\mu^\top F\ge0,\\\epsilon D+N-\nu_+^\top F\ge0,\\\epsilon D-N-\nu_-^\top F\ge0\end{gathered}
```
Each multiplier has the row-specific units required to make its product with the full source residual respectively A or J·A. At every exact root $F=0$, the inequalities give $D\ge d_0>0$ and $-\epsilon D\le N\le\epsilon D$. Hence
```math
\boxed{\quad |G-p(q)|=|N/D|\le\epsilon\quad\text{for ALL legal source roots}.}
```
This is an **independent elementary root-relative positivity lemma** in the lineage of equality-constraint multipliers/real-algebraic positivity, rather than a new general semialgebraic completeness theorem. It strengthens the **applicability** of S-L6 to rational outputs: the off-shell set $K$ may contain $D=0$ and sign changes, so $\sup_K|G-p(q)-\lambda^\top F|$ is undefined, but all three polynomialized inequalities can remain perfectly valid. It does not relax exhaustive real-root coverage or infer that any root exists; a numerically guessed corrected-center tube is inadmissible. If approximations have nonzero source residual, carry the rowwise scaled $\mu^\top r,\nu^\top r$ uncertainty and directed arithmetic explicitly rather than substitute $F=0$.

**Exact two-root, off-shell-pole oracle.** On the certified toy outer interval $K=[-1,3]$, choose $F(x)=x(x-2)$, $D(x)=1-F(x)$, $m_{12}=0,m_{31}=F,m_{42}=m_{46}=0,m_{60}=D$, $G=0$, $p(q)=q_1$. Legal real roots $x=0,2$ both have $D=1,q=0,G=0$. Off the roots $D(2)=1>0,D(5/2)<0$, so $D$ has a zero within $K$ by continuity, where the S-L6 rational expression is undefined. Yet $N=-F$, and exact choices $\mu=-1,\nu_+=-1,\nu_-=+1,d_0=1,\epsilon=0$ make all three certificate expressions identically zero over $K$. Thus a **nonunique all-root** system has a sharp zero-width goal certificate without a defined off-shell ratio or an invertible source Jacobian everywhere. Conversely, for the **same** roots and CAL currents but goal $G(x)=x$, the goals are 0 and 2 (in arbitrary chosen work units), so any same-observation scalar predictor has radius at least 1. This information obstruction cannot be removed by multipliers. The exact nonnegative polynomial identities $x+\tfrac12F(x)=\tfrac12x^2$ and $2-x+\tfrac12F(x)=\tfrac12(x-2)^2$ also verify the sharp two-root goal interval [0,2], showing source equalities can sharpen a loose ambient box [−1,3]. [Synthetic regression](../dpt_tools/test_paper_transfer_falsifiers.py) is not evidence of a SiC source root.

**Research prior and actual next computation.** Exact rational SOS certificates (e.g. Kaltofen, Li, Yang & Zhi, *J. Symbolic Comput.* 47 (2012), 1–15, DOI [10.1016/j.jsc.2011.08.002](https://doi.org/10.1016/j.jsc.2011.08.002)) motivate checking signed positivity with equality constraints. The real DPT BE charge/thermal exponential, piecewise clip and GL32 law are not automatically polynomials or amenable to a low-degree SOS certificate. An alternative interval arithmetic implementation must bound the **whole signed expression** before splitting absolute terms, retain branch/pole orientation, and use the original archived source/guard/measurement law. For 150-V Goal27 the smallest new legitimate input is (i) a source-justified **root-exhaustive all-branch outer $K$** over the common 126-step PREP, CAL4800 and target6720, all 50 law variables and the recorded command, (ii) the actual $D,B,G,F$ and frozen predictor, (iii) a prefix-first signed positivity test for actual $D-d_0-\mu^\top F$ on $K$, then (iv) verified positive upper margins for the two numerator signs and a same-information full-CAL ordinary. Mere proxy $D_{\rm aff}>0$ is insufficient; a point Hessian, coarse sample or PARKed full-state contraction failure neither proves nor refutes S-L7 feasibility. **S-L7 mathematical SIDE_VERIFIED / actual S150 all-root denominator and goal still OPEN_RESEARCH.**

**Interaction with command-aware P36.** In the stored *affine proxy*, the recorded digital PREP amplitudes can be used to replace the original command-blind fixed $p(q)$ with the projective inverse $\widehat G(a,q)$; the proxy no-noise residual then vanishes (P36). A physical S-L7 consumer could apply the same homogenization to a suitably derived rational command-aware decoder, but its denominator and the source-root cover must be established anew. The old 0.3435875 nJ q-only lower witness uses different recorded PREP amplitudes; it does not refute P36 or prove real full-CAL ambiguity.

## 2026-10-17 S-L8: exhaustive discrete-prefix root outer and denominator-first continuation

**Purpose: supply the missing outer B of S-L6/S-L7 without asserting a full-state contraction.** Let the genuine source parameter bank be $\theta_s=(a_1,a_2,a_3,L,\kappa)$; the remaining Goal27 $b$ (90–110 MHz readout bandwidth) enters the common observation RC filter, **not** an extra 50-state network residual parameter. Let the full source-legal backward-Euler or other *qualified* stage equations be
```math
F_{n,m}(x_n,x_{n-1},\theta_s)=0,\quad
(x_n,x_{n-1},\theta_s)\in{\cal G}_{n,m},
```
where $m$ ranges over **all legally reachable** conduction/clip/guard modes, and $x_n$ includes electrical and algebraic states, old/new charge, GL32, thermal and source-consistency conditions. The joint PREP endpoint is propagated into **both** saved CAL and target command forks; do not independently reinitialize a fork. To avoid a circular guessed small tube, require a source-proved globally exhaustive ambient family $K_n(E)$ (compact in all 50 coordinates, not just dynamic voltages/current).

**(S-L8) Conditional discrete-prefix all-root covering lemma.** Suppose for *every* legal stage root, not just a selected solver root, a nonnegative proper source-verified storage/estimate $V_n(x_n)$ satisfies
```math
V_n(x_n)-V_{n-1}(x_{n-1})
\le h_n\big(\alpha_n V_n(x_n)+c_n\big),
\qquad h_n\alpha_n<1,
```
with source-qualified constants $\alpha_n,c_n$, and source KCL/algebraic coercivity/thermal bounds plus legal guards prove **all** state components in a compact envelope $K_n(E_n)$ whenever $V_n\le E_n$. Starting from the certified *entire* legal preparation set $K_0(E_0)$, take
```math
E_n=\frac{E_{n-1}+h_nc_n}{1-h_n\alpha_n}.
```
At each stage, exhaustively tile the ambient set $K_{n-1}(E_{n-1})\times K_n(E_n)\times\Theta_s$, splitting modes at every unresolved switching/clip/initialization seam. Discard a cell only when a **sound directed interval** evaluator proves $0\notin F_{n,m}(\text{cell})$ in some row, or a guard/recorded command is rigorously impossible; retain all remaining cells, including uncertain and seam-touching cells, and project survivors into the next reachable outer. Then **every** source-legal exact stage-root sequence remains in the retained prefix set, by induction on n. It does not follow that any root exists, branches are unique, or that surviving cells are reasonably narrow. Parameter sharing, one prepared endpoint for both forks, full controller timebase, and filter memory must be preserved in a global parameter/path dependency representation; dropping correlations preserves only a looser valid outer. If any source-variable lacks global algebraic/thermal/coercive compactness, S-L8 CANNOT claim the full-root outer.

**Prefix first: certify actual rational readout, then goal.** At the completed pretarget CAL prefix, attach the original filter recurrence with $b\in[90,110]$ MHz, its lawful initial state and full gain/offset/clock nuisance; the 5 selected filtered currents must share the same recorded PREP/CAL path. Evaluate $D_{\rm actual}=I_{60}-I_{12}$ on the exhaustive retained CAL prefixes, ideally using source-residual multipliers of S-L7, and require a **strict** true-root lower $D_{\rm actual}\ge d_*>0$ A. The old proxy's $D_{\rm aff}$ bound is irrelevant to this actual-gate assertion. Then retain actual source signed goal $G_{\rm actual}$, the fixed proxy decoder $p$ (or P36's recorded-command decoder if its new homogeneous denominators are separately qualified), and the fraction-free
```math
N=D_{\rm actual}[G_{\rm actual}-G_0+\ell^\top q_0]-\ell^\top B_{\rm actual}\quad[\mathrm{J\,A}].
```
If the accepted *proxy* full-bank bound $|R_{\rm aff}(\theta)|\le\epsilon_{\rm aff}=0.876578434279$ nJ and a **rigorously directed, same-parameter, same-command** residual certificate
```math
\sup_{B_{\rm all}}|N-D_{\rm actual}R_{\rm aff}(\theta)-\mu^\top F_{\rm whole}|
\le\delta_N\quad[\mathrm{J\,A}]
```
hold, then every eligible root obeys $|G_{\rm actual}-p(q_{\rm actual})|\le\epsilon_{\rm aff}+\delta_N/d_*$. The correlation between actual CAL and target signed work remains inside **one** numerator. Solver/GL32/rounding residue, gain/offset joint noise and unknown physical model discrepancy must be qualified independently, with row units in $\mu$. The certificate is *conditional*, does not assume the existing PARKed Kantorovich q becomes small, and may be computationally uneconomic because prefix boxes can explode.

**Two exact sanity examples expose the necessary distinctions.** (Positive) A single passive RL load with $R=1\Omega$, $u=1\mathrm V$, $h=1\mathrm s$, $L\in[1,2]\mathrm H$, initial $i_0=0$, and two BE steps has
```math
\begin{gathered}i_1=\frac1{L+1}\in[1/3,1/2]\mathrm A,\\i_2=\frac{2L+1}{(L+1)^2}\in[5/9,3/4]\mathrm A,\\D=i_2-i_1=\frac{L}{(L+1)^2}\in[2/9,1/4]\mathrm A\end{gathered}
```
Its **discrete** physical energy identity
```math
\tfrac L2(i_n^2-i_{n-1}^2)+\tfrac L2(i_n-i_{n-1})^2
+hRi_n^2=hu i_n
```
establishes a whole-root storage inequality, before simple residual algebra narrows the actual current and D ranges. The two-step terminal work $W=hu(i_1+i_2)\in[8/9,5/4]\mathrm J$ is NOT a SiC/150-V claim. (Negative) For a *continuous dissipative* gradient flow $\dot x=x-x^3=-V'(x)$, $V=(x^2-1)^2/4$, $V'\dot x=-(V')^2\le0$, $x_0=1$, the BE stage $h=5$ has **three** real roots
```math
5x_1^3-4x_1-1=(x_1-1)(5x_1^2+5x_1+1)=0.
```
Besides $x_1=1$, the two regular roots $x_1=(-5\pm\sqrt5)/10$ **increase** $V$ above zero. A second BE stage $h=1$ satisfies $x_2^3=x_1$, so each branch has a real two-step continuation. Thus *continuous-time* barrier/passivity does not prove a BE all-root energy bound: a source-specific discrete inequality, selected branch rule or conservative all-branch ambient is indispensable. Separately, a passive RL at DC equilibrium $i_0=u/R$ has a unique constant trajectory but two equal CAL samples $D=0$. Root/energy coverage never by itself proves projective denominator positivity. [Analytic unit tests](../dpt_tools/test_paper_transfer_falsifiers.py) preserve both controls.

**Original literature and transfer distance.** Rauh, Brill & Günther, “A Novel Interval Arithmetic Approach for Solving Differential-Algebraic Equations with VALENCIA-IVP,” *Int. J. Appl. Math. Comput. Sci.* 19 (2009), 381–397, DOI [10.2478/v10006-009-0032-4](https://doi.org/10.2478/v10006-009-0032-4), §§2.2,4.2,6,8.1 (paper pp.383–394), derives validated DAE state enclosures/constraint pruning under interval algebraic solvability; it does **not** prove DPT whole electrothermal root existence. Prajna & Rantzer, “Convex Programs for Temporal Verification of Nonlinear Dynamical Systems,” *SIAM JCO* 46 (2007), 999–1021, DOI [10.1137/050645178](https://doi.org/10.1137/050645178), §1 equations (1.1–1.3), treats **continuous** vector fields/barrier trajectories; the discrete BE negative control is therefore material. Other related interval-DAE references whose full theorem proofs were not verified must not be elevated to authority. **Scientific decision:** do not pay for new native or restart PARKed full-fork beta until real source discrete coercive/global ambient plus CAL positive denominator can be certified; if no such physical all-branch outer emerges from stored law, the proof route is INCONCLUSIVE, while actual full-CAL fiber remains a separate competing information strategy.

## 2026-10-17 S-L9: moving-event index-one DAE goal residual — essential boundary term, not extra information

**Event-specific necessary repair to S-L5/S-L6.** Suppose a source-legal piecewise smooth index-one DAE has complete consistent initial algebraic state, guarded switching at $\tau$, and source-verified transversal event $h(x(\tau^-),\tau)=0$ with $|d h/dt|\ge\alpha>0$. When future terminal work is genuinely piecewise integrated from power $P^-,P^+$ and the event time varies, the derivative includes
```math
\delta G_{\rm moving\ boundary}=\big[P^-(\tau^-)-P^+(\tau^+)\big]\delta\tau\quad [\mathrm J].
```
A full stacked source Jacobian/goal adjoint must include event residual, reset/jump and source-consistency derivatives, not just chronological differential/charge rows. Without validated transversality, event identity may fail and this derivative need not be bounded. The sign of external work cannot be inferred from positive dissipation alone. The same full recorded PREP/CAL and frozen goal window must be used for every compared prospective source world.

**Independent exact 2D hybrid oracle.** Use a single algebraic port variable $u$ and event time $\tau$, with consistently scaled dimensionless $F(u,\tau)=(u-1,u\tau-0.6)=0$. Define a synthetic switched external-work goal
```math
G(u,\tau)=u(1+\tfrac12u)\tau+2u(1-\tau)\quad\mathrm J .
```
Its qualified root is $`u=1,\tau=0.6`$, yielding $`G_\ast=1.700`$ J. At approximate $`\widehat Y=(0.9,0.6)`$, $`G(\widehat Y)=1.503`$ J, source residual $`(-0.1,-0.06)`$, Jacobian $`\bigl[\begin{smallmatrix}1&0\\0.6&0.9\end{smallmatrix}\bigr]`$, gradient $`DG=(1.94,-0.495)`$ J in scaled units, and exact adjoint $`\lambda=(2.27,-0.55)`$ J. Thus $`L(\widehat Y)=G(\widehat Y)-\lambda^\top F(\widehat Y)=1.697`$ J, a joint goal correction requiring the event equation; the remaining finite nonlinear correction is +0.003 J. A source approximation with $`u=1,\tau=0.5`$ obeys the **flow/algebraic** equation $`u-1=0`$, yet yields $`G=1.750`$ J: omitting the guard changes the signed goal by 0.050 J even when the retained flow residual is exactly zero. This is an analytic negative control, NOT a measurement or SiC work estimate.

With a verified root ball $B_r$, a qualified matrix preconditioner $K$ and $q=\sup_{B_r}\|I-KDF\|<1$, $\eta=\|KF(\widehat Y)\|$, $\eta+q r\le r$, the usual contraction yields a root distance $\rho\le\eta/(1-q)$ on this one qualified branch. Taking $Q=G-p(O)$, $\lambda$ from the **complete** event-aware ordered adjoint, $L=Q-\lambda^\top F$, $\sup_{B_r}\|D^2L\|\le M$, gives the already-known conditional goal interval $|Q(Y_\ast)-L(\widehat Y)|\le\|DL(\widehat Y)\|\,\rho+M\rho^2/2$. This is **subsumed by S-L6**, and does NOT beat the exact same-information ordered adjoint or permit a global S150 source certificate. It is useful only as a concrete **missing-guard negative test** before deploying a residual certificate across event switches.

**Primary-source assumptions.** Serban & Recuero (2019) source event sensitivity identities (original §§2–3, event Eq.4/6/8 and jump Eq.12–13, pp.6–9) require consistent DAE branches and transversal event. Chen & Trenn (2023) switched DAE common-Lyapunov/dwell results require authorized jump/consistency maps, not simply adjacent continuous-flow matrices. Chaudhry, Lewis & Molla (2025), [arXiv:2507.03712](https://arxiv.org/abs/2507.03712), Theorems 3.2–3.4 use semi-explicit index-one/Hessenberg-index-two regularity and **linear QoI** for the original averaged-J residual representation; an independent nonlinear signed $VI$ Hessian/guard remainder must still be proved for DPT. Use [analytic no-guard regression](../dpt_tools/test_paper_transfer_falsifiers.py) as a falsifier; this is not another completion claim. Status SIDE_VERIFIED on synthetic DAE, actual S150/N100 source guard and root cover OPEN.

## 2026-10-18 S-L10: two ACTUAL 150V source-specific one-step dissipativity identities, not a whole-root energy certificate

**Why this materially narrows the S-L8 missing proof.** A read-only 2026-10-18 audit of the *nonprotected accepted* Rev6 source in original_submission.zip::analysis/actual_law.py (original controller acceptance locator: pro_runs/20261010_pro18_goal_adequacy_frontier/artifacts/run_C), not a simulated source run, checks two real physical subblocks and their stage signs. Unlike generic passivity or the older fixed-forcing diode monotonicity, these identities use the true G12 charge-row orientation, x–d shunt and the actual diffusion-current/body residual. They are **rowwise** algebraic gates only: global 50D thermal/algebraic coercivity, modes and all roots remain OPEN.

**(S-L10a) Source G12-GL32 stepwise shunt allocation, exact completion of square.** The source nodal residual includes the genuine G12 branch of *quadrature-computed charge* $Q_{12}(u)$, $u=v_d-v_s$, sampled at each implicit step with $\Delta Q=Q_{12}(u_n)-Q_{12}(u_{n-1})$. The associated incidence vector is the x–s edge, so pairing all nodal rows with the potentials leaves a cross term $(u+a)\Delta Q/h$, where $a=v_x-v_d$. The source x–d shunt has $R_{xd}=10^{-4}\Omega$; allocate a **nonnegative fraction** $0<\alpha\le1$ of its conductance dissipation $\alpha a^2/R_{xd}$ to this one charge branch, leaving $1-\alpha$ for other residual contributions. Where actual source charge is increasing, its **real secant** $c=\Delta Q/(u_n-u_{n-1})$ has units F and is nonnegative. The following identity is exact for every BE step $h>0$ and every $u_n,u_{n-1},a$, without a root unique inverse:
```math
\begin{gathered}\Delta u=u_n-u_{n-1},\\\frac{\alpha a^2}{R_{xd}}+(u_n+a)\frac{\Delta Q}{h}\\=\frac{c}{2h}(u_n^2-u_{n-1}^2)\\+\left[\frac{c}{2h}-\frac{R_{xd}c^2}{4\alpha h^2}\right](\Delta u)^2\\+\frac{\alpha}{R_{xd}}\left[a+\frac{R_{xd}c\Delta u}{2\alpha h}\right]^2\end{gathered}
```
**Proof:** expand both squares, use $u_n^2-u_{n-1}^2=2u_n\Delta u-(\Delta u)^2$, and cancel the $a\,c\Delta u/h$ cross term. If the **literal** source GL32 integrated charge is monotone and $0\le c\le C_{\max}$ on the entire declared guard and parameter interval, a sufficient **sharp for this allocated square** timestep condition is
```math
h\ge \frac{R_{xd}C_{\max}}{2\alpha}.
```
The nonnegative charge-remnant and square then cannot by themselves destroy the stage energy inequality. The controller's actual G12 clipped branch has archived $C_{\max}=1.0156922324976233\times10^{-9}\mathrm F$ (source low-voltage $C(0.1\,\mathrm V)$ maximum); with $\alpha=1/2$, the allocation threshold is **$h_\ast=0.1015692232497623$ ps**. The saved legitimate grids have min PREP step about 63.492ps and CAL/target step 12.5ps, so **this one G12 subblock passes its exact source-specific timestep gate at every original stage**. This is a scoped source-row sign check, NOT a whole-fork root certification; α must be shared consistently with all other rows. Critically $c$ depends on endpoints, so $c(u_n^2-u_{n-1}^2)/(2h)$ does **not automatically telescope** across stages, and quadrature weights stored as binary64 must be interpreted and enclosed as the actual implemented 32-point rule, not as an ideal primitive to silently assert an exact global energy.

**(S-L10b) Source diode diffusion/body positive-storage inequality with a mandatory signed term.** The actual saved-law diffusion/body residuals use $`z=I_s\exp(v_j/a_V)>0,\ \tau=2`$ns, $`i_b=(z-I_s)+(\tau/h)(z-z_{\rm old})`$ and $`d=-v_j-E_{\rm th}-r_{\rm eff}i_b`$, with $`r_{\rm eff}>0`$ in the qualified source guard. **Do not assume $`i_b\ge0`$**: a charge decay may make it negative. The exact body power identity is
```math
-d\,i_b=v_j i_b+E_{\rm th}i_b+r_{\rm eff} i_b^2.
```
Define $\Psi(z)=a_V[z\log(z/I_s)-z+I_s]$, whose physical units are $\mathrm{V\,A}=\mathrm W$; the actual diffusion *stored energy* is $\tau\Psi(z)$ in J, so $(\tau/h)\Delta\Psi$ is W. Since $\Psi'(z)=v_j$, $\Psi''(z)=a_V/z>0$, and $v_j(z-I_s)\ge0$, the convex supporting-hyperplane inequality yields
```math
v_j i_b\ge(\tau/h)[\Psi(z)-\Psi(z_{\rm old})].
```
For an independently verified $|E_{\rm th}|\le E_{\max}$ and $r_{\rm eff}\ge r_{\min}>0$, Young's inequality proves the exact **rowwise** lower bound
```math
-d\,i_b\ge\frac{\tau}{h}\Delta\Psi+
\frac{r_{\min}}2 i_b^2-\frac{E_{\max}^2}{2r_{\min}}.
```
This retention of the signed $E_{\rm th}i_b$ is essential; setting $v_j i_b\ge0$ without the diffusion term is generally false. The original source clips some channel/thermal-dependent terms but does NOT globally clip the thermal **state** $T$, and the heat row includes a *different* $|d\,i_{\rm sense}|$ term; therefore these inequalities neither prove thermal boundedness nor permit double counting the diode resistor as heat. They do, however, give concrete source-row constraints for a future validated all-root interval pruning and show why a generic continuous pH storage cannot substitute for the discrete BE law.

**Minimal exact two-step controls (no source flow).** On the source clipped constant-slope G12 branch take $`u_0=0,\ u_1=0.02,\ u_2=0.04`$ V, $`h=12.5`$ps, $`c=C(0.1\mathrm V)`$, $`\alpha=1/2`$, and $`a_n=-R_{xd}c\Delta u/(2\alpha h)`$: for both steps the completed square vanishes and the remaining coefficient is strictly positive; analytic rational substitution verifies the source row orientation, half-charge term, physical units and timestep gate. Separately choose positive diode $`z_0=I_s,z_1=2I_s,z_2=3I_s,\ h=\tau`$, $`v_{j,n}=a_V\log(z_n/I_s)`$, $`E_{\rm th}=0,r_{\rm eff}=1\Omega`$, $`d_n=-v_{j,n}-r_{\rm eff}i_{b,n}`$; both diode and body BE residuals vanish exactly and satisfy the convex $`\Psi`$ inequality. These controls are physically patterned test equations, not proof that an S150 legitimate full prepared history realizes them. [Explicit regression](../dpt_tools/test_paper_transfer_falsifiers.py).

**Exact remaining root obstruction.** Even if S-L10a and S-L10b hold for every source step, one must prove the other actual KCL/network, threshold/clipped channel, thermal absolute-value and guard rows can jointly absorb these signed sources, and provide a uniform bound for all algebraic/thermal 50D states before S-L8's exhaustive interval root outer exists. Neither the accepted recenter center nor the seven exposed nonlinear source points proves those quantified bounds. Local historical partial F derivative used FD and source GL32 charge derivative differs from ideal primitive: only the literal value/derivative and directed interval forcing may enter any strict actual goal-adjoint remainder. Evidence level **SIDE_VERIFIED true-source one-step algebra**, actual source-wide root/goal denominator / future signed work **OPEN_RESEARCH**, whole-fork bank beta **PARK**.

## 2026-10-18 S-L11: actual fixed-window work makes the P36 homogeneous source-goal Hessian partially low rank

**Source-specific structure, beyond merely naming an adjoint.** Let $X$ stack every lawful original common 126-step PREP, 4800-step filtered CAL and 6720-step target state plus actual index-one algebraic/thermal/guard variables and source Jacobian rows. Fix the recorded command and the original target H scorer *before* source forecast. On the original stored fixed 841-point target-output time grid the signed external terminal work
```math
G_H(X)=\frac12\sum_k\Delta t_k
[V_k I_k+V_{k+1}I_{k+1}]\quad[\mathrm J]
```
is a **quadratic function of the exposed physical port V/I state components** (with independently fixed interpolation/trapezoidal weights and no moving guard); it is NOT the unrelated $W(\Delta V,\Delta I)$ nor a non-quadratic continuous native integral. Augment the original sampled 100MHz RC filtering recurrence and calibrated five readout states into the source vector, so five sampled CAL currents are *linear coordinate readouts of X* on one fixed mode/clock, despite the nonlinear physical DAE forcing. With a fixed P36 recorded-PREP $a$, let $s(X),v(X)$ be the four homogeneous projective coordinates $H(a)^{-1}t(m(X))=(s,v)$; these are **linear in those readout coordinates**, but the constraint law $F(X)=0$ remains nonlinear. Set $C(a)=G_0+c_a^\top a$ and the denominator-cleared actual goal numerator
```math
N(X)=s(X)[G_H(X)-C(a)]-c_u^\top v(X)\quad[\mathrm J].
```
At eligible true roots $s>0$, the frozen decoder error is exactly $N(X)/s(X)$. Because $s,v$ are linear and $G_H$ is quadratic, their exact source-coordinate Hessian is
```math
D^2N(X)=s(X)D^2G_H+
Ds\otimes DG_H(X)+DG_H(X)\otimes Ds.
```
The *mixed correction* has rank at most **two** at any point; the first $sD^2G_H$ term and the full $-\lambda^\top D^2F$ Hessian may be high rank over 11546 stages. **Claiming the entire 50-state/global Hessian is rank two would be false.** The actual G11 GL32 charge, diode diffusion/thermal source rows and RC coefficient variation must be differentiated as implemented; in the nonprotected archived source, some local Jacobians were obtained by finite differences and the ideal charge primitive derivative is not identical to the literal GL32 endpoint derivative. A point FD tangent is not a rigorous outward Hessian envelope.

**(S-L11) Conditional goal-only projected factor certificate.** For any source/root/guard-qualified ball $\|X_\ast-\widehat X\|\le R$ (dimensionless physical variable scaling required), choose a frozen physical row-scaled multiplier $\lambda$ and $\mathcal L(X)=N(X)-\lambda^\top F(X)$ [J]. Suppose on the entire convex source-valid segment all true-root Hessians admit a **verified** decomposition
```math
\begin{gathered}D^2\mathcal L(X)=\sum_j U_jK_j(X)U_j^\top+E(X),\\\|K_j(X)\|\le M_j,\ \|E(X)\|\le\eta\end{gathered}
```
where each $U_j$ is a fixed low-column projection and source rows $P_j$ satisfy uniformly $\|U_j^\top-P_j DF(X)\|\le\delta_j$ on that ball, in the same declared row/state norms. Since $F(X_\ast)=0$, source integration gives
```math
\|U_j^\top (X_\ast-\widehat X)\|
\le b_j:=\|P_jF(\widehat X)\|+\delta_j R.
```
Second-order Taylor, **without forming a global state inverse**, now yields the rigorously *conditional* signed goal-only bound
```math
\begin{gathered}|G_H(X_\ast)-\widehat G|\\\le\frac{|\mathcal L(\widehat X)|+\|D\mathcal L(\widehat X)\|R}{s_\ast}\\+\frac{\frac12\sum_j M_j b_j^2+\frac12\eta R^2}{s_\ast},\\s(X_\ast)\ge s_\ast>0\end{gathered}
```
**Proof:** $N(X_\ast)=\mathcal L(X_\ast)$. Integrate $P_j DF(X)$ along the segment to replace the true $U_j^\top e$ with $-P_jF(\widehat X)$ plus at most $\delta_jR$, then apply the Hessian factor bound in the integral Taylor remainder. This is a source-specific *factorization/computation strategy for the existing S-L6 goal Lagrangian*, not a generally sharper theorem than an exact full ordered adjoint and not a replacement for a root-containing source outer.

**Exact distinct oracle.** Let $F(x,y)=(x-1,\varepsilon(y-1))$ with $\varepsilon>0$ arbitrarily small, $s=1,N=(x+y)^2$, center $\widehat X=(0,0)$ and true root $(1,1)$. Choose $U=(1,1)^\top$, $K_1=2$, $P=(1,\varepsilon^{-1})$, $\lambda=0$ and $E=0$. Then $U^\top=PDF$, $\delta=0$, $b=|PF(\widehat X)|=2$, $\mathcal L(\widehat X)=D\mathcal L(\widehat X)=0$ and the bound is *exact*: $|N(X_\ast)|\le(2)(2^2)/2=4$. The full inverse Jacobian norm diverges as $\varepsilon\to0$, while the factorization's target bound stays finite. The **ordinary** full-source solver also knows the exact goal 4, so this does not imply scientific improvement over a same-information full-record ordinary; the toy only falsifies the premise that every goal bound must pay the smallest state singular value. [Exact negative-control regression](../dpt_tools/test_paper_transfer_falsifiers.py).

**Primary reference and true data gap.** Endtmayer, Langer & Wick, “Two-Side a Posteriori Error Estimates for the Dual-Weighted Residual Method,” *SIAM J. Sci. Comput.* 42(1) A371–A394 (2020), DOI [10.1137/18M1227275](https://doi.org/10.1137/18M1227275), original [author report](https://www.ricam.oeaw.ac.at/files/reports/18/rep18-32.pdf) Theorem 2.1 PDF p4 retains a nonlinear functional remainder; Lemma 3.6 p7 and Theorem 3.9 p8 use additional approximation/saturation assumptions, Remark 3.13 excludes unbudgeted data/quadrature errors. It is stationary nonlinear FE a posteriori theory, **not** a guarantee for switched DAE/GL32/physical SiC. The smallest actual zero-native check is to qualify **one source-legal saved segment** containing the CAL/target active thermal row9/row41, the exact original 841-point VI scorer, genuine GL32 derivative/guard and shared filter state, then produce outward full-field $P_jDF,U_j$ and low-dimensional Hessian factors. If source-wide root containment or $s_\ast>0$ fails, ABSTAIN. Recenter point shifts $\Delta G\approx-2.581761188\times10^{-13}$ J and observed joint $-1.393544835528\times10^{-13}$ J have their own certified-offset ledger and cannot be silently swallowed into this nonlinear remainder. **Status mathematical SIDE_VERIFIED / actual all-root S150 source-G bound OPEN.**

## 2026-10-18 S-L12: literal source thermal-ray root exclusion and GL32 endpoint-jet correction

**Source-specific all-root thermal necessary gate.** Original nonprotected \`pro_runs/20261010_pro18_goal_adequacy_frontier/analysis/actual_law.py\` L20–21 and L116–129 gives the accepted 4-node-per-leg Rev6 $R_{\rm th}=(.06378,.1553,.09942,.1417)$ C/W and $C_{\rm th}=(.00131,.006698,.01941,.07301)$ J/C. Source L255–259 and L289–297 uses the literal BE thermal residual and $H=|d\,i_{\rm sense}|+(v_g-v_{g2})^2/9\ge0$ W; thermal **state** itself is not globally clipped. Set
```math
M_h=C_{\rm th}/h+K_{\rm th}.
```
Because this grounded thermal Stieltjes matrix is a nonsingular M-matrix, $z_h=M_h^{-1}e_1>0$. With previous legally reached temperature $T_{\rm old}$, every exact source root in a leg **must** satisfy
```math
\begin{gathered}
T=T^0+z_hH,\\
T^0=25{\bf1}+M_h^{-1}(C_{\rm th}/h)(T_{\rm old}-25{\bf1}).
\end{gathered}
```
Consequently any proposed all-root state box $B$ is **impossible** if the independently outward-enclosed sets $H_{\rm electric}(B)$ and $(T_1-T_1^0)/(z_h)_1$ have empty intersection, or if the other three temperatures cannot share that same ray. This rejects **all** roots in the cell, not merely a chosen Newton iteration; it makes no claim of existence in accepted cells. For fixed electric forcing and smooth fixed guard/clip branch, $(z_h)_1\,\sup|dH/dT_1|<1$ is a separate *conditional* scalar uniqueness gate; variable electric/diode forcing requires full Schur/guard analysis.

**Independent exact source-coefficient control.** Fraction Gaussian elimination of those four literal $`R/C`$ values gives $`(z_h)_1=9.5419833052694515\times10^{-9}`$ C/W at $`h=12.5`$ ps and $`4.8467187209060625\times10^{-8}`$ C/W at $`h=63.49206349224305`$ ps. All 4 source thermal rows have exactly zero rational residual for one-W ray forcing. With $`T_{\rm old}=25^\circ\mathrm C`$, a 3 V voltage across the 9 ohm gate resistor already supplies at least 1 W in the source heat; an unheated $`T=25^\circ\mathrm C`$ candidate therefore fails, without solving the full 50-state system. The heat values, source guards, full digital PREP old state and electric box must be separately qualified for actual CAL/target decisions. This is a **rigorous source subblock exclusion**, NOT a tight all-source work bound or an S150 whole-domain positive certificate. A separate archived first-PREP coarse uncentered energy attempt returned a huge ~250 kV bounding scale because of the 150 V/87.416 micro-ohm Norton injection; that float diagnostic is not evidence that source roots reach this magnitude. A useful next energy enclosure must first complete the signed bus/source work around its driven center.

**Literal G11 GL32 differentiation (distinct from ideal capacitance).** Actual source L207–224 evaluates a fixed split-panel 32-node charge quadrature, while L261–265 uses point finite differences and L293 idealized charge_tangent. For one legitimate smooth quadrature panel from $c$ to $b$, with length $\ell=b-c$, positive weights $p_j=w_j/2$, nodes $\xi_j=(1+x_j)/2$, $C_j=C(c+\xi_j\ell)$, the *exact derivative of the finite quadrature itself* is
```math
\begin{gathered}
Q_{32}=\ell\sum_j p_j C(c+\xi_j\ell),\\
\partial_bQ_{32}=\sum_jp_j[C_j+\ell\xi_j C'_j].
\end{gathered}
```
It generally differs from ideal $`C(b)`$, even before floating-point/directed-rounding budgets. Its nodal BE Jacobian update is per-leg incidence-outer-product times $`\Delta(\partial Q_{32})/h`$ [S], a sparse rank-one contribution per signed branch. At split knots/thermal abs/clip guards, qualify one-sided derivatives or interval slopes, not an unbroken smooth Hessian. The independent Fraction polynomial-quadrature oracle falsifies replacing this finite-panel derivative with ideal endpoint capacitance. Actual CAL4926 row9 q~8.592 and target6846 row41 q~4.991 are **preconditioned output rows**, not themselves thermal residual rows; before asserting any rescue of the PARKed self-map, a source-validated directed correction would need to cut the earlier failing q+eta-1 by at least 7.686 and 4.085 respectively (fixed old preconditioner/weights). No lawful saved per-step inverse-row fields sufficient for this numerical correction were obtained without visiting forbidden tmp. Regression: [existing source proof tests](../dpt_tools/test_paper_transfer_falsifiers.py). Status **SIDE_VERIFIED source-row algebra; actual full-root/goal outer OPEN**.



## 2026-10-18 S-L13: S150 source-centered first-PREP OFF/cool existence and GL32 value falsifiers

**Scope and original source.** Nonprotected original Pro18C ZIP, analysis/actual_law.py L165–224,225–259,276–301, defines 26 KCL nodes, 12 BE coils, old/current charges, body-diode and 4-node thermal. Its supply coil has +150 V forcing and the 87.416-microohm Norton resistor: the uncentered scalar all-root Young bound was vacuous (~250 kV). At the ACTUAL saved first-PREP old state, algebraically eliminate coils, shift electrical nodes e=v-v_old, and reference diode current to i_b,old=z_old-I_s with z_old=I_s exp(vj_old/aV). Source charge is old/new difference, not an absolute-charge forcing. The centered KCL residual rho retains exact signed source-port cancellation.

**Conditional positive first-PREP OFF/cool root chart, a genuinely new scoped result.** At h=63.492063492 ps and legal first command, a1 in [.16,.44] V and L_ext in [4.02,4.58] nH, suppose the working chart has both gates below the true 1.7 V threshold and all 8 thermal states in [25,26] C. Original source OFF channel is zero; positive literal segmented GL32 secants, clipped GS/G12 charges, and half the x-d resistive shunt give a grounded incremental SPD 26-node graph A. The exact body sign and monotone positive diode charge imply the all-root radial necessity:
```math
\begin{gathered}
e^\top A e+r_{\min}\|\Delta i_b\|^2\\
\le-\rho^\top e-\sum_k b_{\mathrm{ref},k}\Delta i_{b,k},
\end{gathered}
```
where delta i_b=(1+tau/h)(z-z_old) and b_ref=d_old+vj_old+Eth(g,T)+r_eff(z_old-I_s). The actual G12 signed timestep gate is h>=0.05078461 ps here. An archived-coefficient tree-flow Fraction corner bound gives Qrho<=0.001412441911 W; source Bernstein Eth in [-1.700613,.949824] V and r_eff in [.0699,.0701] ohm give Qbody<=83.664783888 W. **Both together are strictly less than E=84 W**. The GS graph edge gives |delta GS|<1.960220 V, so both new GS remain below -2.0345 V; the 4-node thermal M-matrix ray stays below 25.062 C (and all eight T below 26 C). These are self-closing OFF/cool branch conditions, not assertions about other branches.

**2026-10-18 independent correction of the earlier Brouwer existence claim (S-L13).** The first-step centered radial **necessary** estimate and numerical E=84 W OFF/cool shell are retained, but the preceding claim that projection on the whole ellipse yields a fully source-qualified accepted 50D root is **withdrawn**. Original actual_law.py L445–455 imposes the *solver* |delta(g-w)|<=1 V G11 trial guard, whereas the shell bounds only delta(g-s). With ONLY Q1:w increment +2 V, delta GS=0, delta GD=-2 V, and even the generous source Cgd<=555 pF bound gives shell cost <= 4 W + 4e-7 W + (4 V²)(555 pF)/(63.492 ps) <38.966 W <84 W. This explicit shell member violates the 1 V guard. Monotone eliminated diode z>0 also does not imply source evaluator -1590 V < vj <= 500 aV, and a variable secant A(e) does not define a convex constant-metric projection ellipse without a fixed SPD lower A*. Therefore the energy bound can serve as a **conditional candidate-root enclosure and OFF/thermal self-closure**, or support a hypothetical globally extended algebraic root argument, but **cannot** certify existence of an *accepted/guard-legal* source step by itself. A repaired Brouwer certificate needs one fixed convex A*-ellipse, G11 guard-face pointing/invariance or a smaller validated box, diode endpoint brackets on every face, and the actual thermal/charge law throughout; no such repaired positive legal-root theorem has yet been verified. This correction supersedes the earlier unsupported promotion; main status remains OPEN.

**S-L14: literal split-GL32 VALUE bound and actual checkpoint row exclusion (not S-L12 endpoint derivative).** For each smooth sorted quadrature panel [l,r], length a=r-l, nodes xi_j and weights p_j, moment sums m0=sum p_j and m1=sum p_j xi_j, the exact Peano kernel K2(t)=(1-t)^2/2 - sum_(xi_j>=t) p_j(xi_j-t) yields:
```math
\begin{gathered}
|Q_{32}-\int_l^r C(v)\,dv|\\
\le a\bigl(|m_0-1|C_{\max}
+a|m_1-\tfrac12|C'_{\max}\\
+a^2\Lambda_2 C''_{\max}\bigr),\quad
\Lambda_2=\int_0^1|K_2(t)|dt .
\end{gathered}
```
Source actual_law.py L207–224 splits across -600,-20,-0.1 V; source tanh uses unclipped voltage so derivatives require qualified one-sided panels. The archival source array analysis/acceptance/pro18c_prediction_extension.npz has actual PREP127/CAL4801/target6721 state50 for one **distinct** physical query (a=.23,.37,.23 V,L=4.16nH,kappa=1.009,b=95MHz), not the earlier failed nominal center. At saved PREP n64 Q1:g-w, +0.454389413 ->+0.454379306 V, h=63.492063491396 ps, true delta Q~-5.31546947904e-15 C. Replacing only its charge-row h by CAL 12.5 ps creates -341.518914 microA extra Q1:g raw KCL row (Q1:w opposite), versus 3-microA archived node tolerance. This strictly rejects that **frozen-other-rows wrong-timebase consumer**, not a changed whole BE step. At saved target n3592 Q2:g-w crossing -0.1 V, true split-minus-unsplit adds +0.196371166 microA at raw row18 and negative at row19; at CAL n3331 the correction is -0.061612379 microA, falsifying a universal signed GL32 correction. At saved final CAL n4800 and target n6720 no G11 knot is crossed, hence split-vs-unsplit contribution is exactly ZERO there. Those are **different parameter records** from historic preconditioned row9/row41 q defects. Neither point test certifies a full source goal remainder; float rounding and whole-source guard/root proof remain OPEN. Regression: [existing source tests](../dpt_tools/test_paper_transfer_falsifiers.py).



## 2026-10-18 S-L15: cross-step microbank bounds and literal ETH switch discontinuity

**New step-2/3 anchored S150 necessary gate, not full PREP126.** The original nonprotected original_submission.zip::geometry.npz has t(127), y(127x50), exactly agreeing with source_crosscommand.npz::prep_time and pro18c_prefix_interval_arrays.npz::centers. The saved pro18c_prefix_interval_certificate.json qualifies predecessor component intervals ONLY for a_i=0.3 +/- 1e-6 V and L=4.3 +/- 0.0001 nH (not the original +/-0.14 V and +/-0.28 nH Goal27 bank). Re-center actual KCL around each qualified old state and its old diode positive charge, with the signed 150 V bus forcing and exact GL32/GS/G12 increments as S-L13. Fraction 16-corner rooted-tree and body bounds yield at step2 Qrho<=0.001061884904 W, Qbody<=83.664852566 W, and step3 Qrho<=0.001041144424 W, Qbody<=83.664910339 W: both sums strictly <84 W. On any ALREADY LEGAL exact root in the OFF/T in [25,26] C cell, the actual GS edge gives |delta GS|<1.960220 V and new gates < -2.0345 V; M-matrix thermal rays keep Tj below 25.061 C (others <25.07 C). Archived centers pass the G11 1 V trial gate retrospectively (max delta G11 steps2/3 7.35e-5/1.1223e-4 V); that is NOT a prospective guard-face certificate for all candidates. Every parameter outside the tiny original interval, accepted numerical fixed-point existence, competing ON/HOT roots, directed rounding and future work remain OPEN. Original actual_law.py L165-259,276-301,445-455 fixes units and guards.

**New actual-source discontinuity, not a smooth Jacobian defect.** Literal eth_literal in actual_law.py L134–152 branches at gate g*=clip(8.381e-6*T^2 - .004696*T + 2.8224,1.7,3.2) V. The two branch polynomials are NOT matched at equality. At T=80 C, exact literal-decimal rational g*=2.5003584 V and the one-sided jump of ETH is the positive rational 10730773761148205545757 / 11920928955078125000000 V =0.9001625461895794 V. At T25 the jump is -0.00645910221 V. Source row r_ib=vj+ETH(g,T)+r_eff(T) ib+d retains this finite jump in the BE algebraic row (L249–251,276–301), invalidating intermediate value and a single locally Lipschitz/Clarke or Jacobian secant across the seam. On the explicit T=80 C two-branch neighborhood g_minus in [g*-.01,g*], g_plus in (g*,g*+.01], source |dETH/dg|<=0.888254 V/V on either side and r_eff=.0696002254 ohm imply this NECESSARY two-root inequality:
```math
\begin{gathered}
|\Delta v_j|+|\Delta d|
+0.0696002254\,\Omega\,|\Delta i_b|\\
+0.888254(|g_--g_*|+|g_+-g_*|)
\ge 0.90016254618\;\mathrm V.
\end{gathered}
```
Thus a source-qualified cell with both gates within 0.01 V of the seam and pairwise |delta vj|,|delta d|<=0.1 V and |delta ib|<=1 A cannot contain exact roots on BOTH ETH sides: the left side is <0.288 V. This is a rigorous conditional **branch-separation necessary gate**, not a finding that the actual archived 150 V trajectory reaches the seam or that another root exists. Temperature-varying cells require their own intervalized jump and branch slopes. The practical first falsifier is whether a proposed complete source/guard outer intersects g-net3(T)=0; otherwise a smooth separate chart remains legitimate. Original Abdelfattah–Eisa–Stechlinski IEEE Control Systems Letters 9 (2025) pp2507–2512 DOI 10.1109/LCSYS.2025.3630241, arXiv 2508.18476v2 Thm III.3 preprint PDF p2, requires locally Lipschitz regular index-one hypotheses and gives LOCAL observability, not a global source-root certificate.

## 2026-10-18 S-L16: guarded scalar KCL elimination across actual PREP/CAL/target

**New source-positive partial implicit solve after S-L13.** In original 50D actual_law.py SHA256 51b78f729393d29745f59ca150adfef69e1847bf26a8853c6cef3d6be9e2083d, lines 184–220,445–455, each transistor w node has w-d=1 Ohm, g-w=1e7 Ohm and the signed literal split-GL32 charge. Fix ALL OTHER new-stage coordinates, the OLD control u0=g_old-w_old and step h>0, put u=g_new-w_new. Its exact w KCL is:
```math
\begin{gathered}
F_w(u)=\frac{g_{\rm new}-u-d_{\rm new}}{1\,\Omega}
-\frac{u}{10^7\,\Omega}-\frac{Q_{32}(u,u_0)}h,\\
u\in[u_0-1\ {\rm V},u_0+1\ {\rm V}] .
\end{gathered}
```
This explicitly honors the actual 1V G11 final-state guard; the 84W whole-source ellipse alone did not. If F_w(u0-1V)>0>F_w(u0+1V), IVT gives one inside-guard scalar real root. It is UNIQUE: source Cgd(u) positive, nondecreasing and has logarithmic slope <=.818 /V on all literal smooth panels (the tanh argument remains UNCLIPPED where the prefactor clips). The lower-moving source GL32 32-node positive-weight panel derivative therefore remains positive even for 1V changes; the upper-moving derivative is positive. Continuous split integration across -600,-20,-.1 V preserves monotonicity. Consequently F_w strictly decreases with u throughout the guard. This is an exact elimination of TWO scalar KCL coordinates CONDITIONAL on the remaining 48 source state coordinates and old shared state, not a 50D legal root.

**All-source-step arithmetic qualification from one archived source path.** Nonprotected acceptance/pro18c_prediction_extension.npz SHA256 af7299434d7dcde687da3bf56b5ce31babbc4e0c12b1a849b5f5530ae8fd holds separate PREP127/CAL4801/target6721 state50/time arrays, with identical legal prepared terminal state, query a=(.23,.37,.23)V,Ls4.16nH,kappa1.009,b95MHz. Each of 126+4800+6720 source steps gets a rectangle allowing INDEPENDENT |delta g_new|,|delta d_new|,|delta old control u0|<=.01V around SAVED centers, not arbitrary coupled 50D state changes. Source charge uses positive GL32 weights and actual G11 Cgd. Without floating tanh or power, for ANY panel:
```math
C_{gd}(u)\ge
\frac{555\,{\rm pF}}
{[1+46\mathrm{clip}(-u,.1,600)]^{3/5}}.
```
Let c_low denote the lower right side. A bound on signed charge for shifted old u0 is |Q32(u0±1,u0)| >=(1-1e-12) c_low(min relevant shifted u)(1V). This includes the translated OLD charge; simply subtracting .03A from the NOMINAL signed face without rebounding charge is false (a −.01V old-control shift can change charge current >.068A). Saved binary64 values are lifted exactly to Fractions, c_low uses rational clip and a verified INTEGER q with q^5>=d^3 for d=1+46clip so 555pF/q is rigorously lower, and source Gauss-weight sum/2 is bounded below by (1-1e−12). The ohmic r0 variation is <=(3+1e−7)*.01A. This gives 23292 scalar w equations, 46584 guard-face signs, and exact-rational strictly positive min left/right margins, safely rounded DOWN in A:

| fork | Q1 (left/right) | Q2 (left/right) |
|---|---:|---:|
| PREP126 | >2.0625 / >3.8837 | >1.0116 / >1.0111 |
| CAL4800 | >0.3091 / >0.7619 | >1.1824 / >0.2253 |
| target6720 | >0.3099 / >0.7619 | >1.1824 / >0.2239 |

Thus for EVERY fixed remaining-48-coordinate input respecting these three-coordinate tubes, each of the two original G11 w KCL equations admits EXACTLY ONE |delta(g-w)|<1V real solution. This is a *source-row guarded Schur elimination with a reproducible numerical necessary domain*, not a coupled 48D existence/unique/all-root source certificate, native Newton-iterates guarantee, full Goal27 history propagation or future work enclosure. Archive producer/model numerical uncertainty is not included by lifting its saved binary64 values. An all-world extension needs a true guard-stable 48D full root outer, denominator and predecessor-history inclusion. Reusable [stage audit API](../dpt_tools/stage_box_reachability.py), [independent archived source-row tests](../dpt_tools/test_stage_box_reachability.py).


**S-L17 prospective 48D/50D sparse verification route, original theorem checked.** Rump, *Verified Error Bounds for Sparse Systems Part II* (2026 author manuscript, **not** yet independently assigned a journal DOI), Section 8 **Theorem 8.2 and Eq.(8.7), printed p.21/PDF page index20**, https://www.tuhh.de/ti3/paper/rump/sparselss_II_final.pdf, explicitly reprises Rump's earlier *Acta Numerica* 19 (2010) Theorem 13.3, DOI 10.1017/S096249291000005X; the new useful method is a sparse verified **POINT matrix with one interval right-hand side**, not a new root theorem. For a source-consistent C1 branch F on xhat+X, and a fully outward interval Jacobian J subset of M+[-Delta,Delta], rigorously enclose **all** solutions of My=-F(xhat)-E x, |E|<=Delta, x in X in an interval Y; Y subset int(X) proves existence and uniqueness **within X** and avoids forming a dense inverse. The branch/diode/GL32/heat guards, full old-state/parameter forcing, and the union over competing S150 roots remain mandatory independent proofs. Counterexample falsifying the old criterion "q_infty >1 implies impossibility": f(x1,x2)=(x1+1.1 sin x2,x2+.1 sin x1), centered at0, X=[-2,2]x[-1,1], M=I and Delta_12=1.1,Delta_21=.1 give unweighted q_infty=1.1>1 but sparse Y=[-1.1,1.1]x[-.2,.2] strictly inside X. A weighted infinity norm on these radii has defect .55<1. In S150 the frozen center CAL/target ETH branch margins (reported separately as 1.748919/1.013285 mV) exceed node ±.0001V plus thermal ±.001C seam shift .205702 mV, giving conditional local clearances 1.543217/.807583 mV; this ONLY removes that ETH seam from such ALREADY qualified local boxes. To apply the sparse theorem source-wide still requires jointly directed interval Jacobians/charge split, diode, G11, thermal, predecessor and source error on all legal branches; a failed unweighted q-infinity test proves nothing about physical nonexistence. Source archive and published-original theorem page identities were independently checked; this is a next executable certificate *design*, not a produced verified 50D Krawczyk enclosure.


**S-L18 independent first-PREP diode-history mismatch falsifier of an attempted FULL50 root repair.** Original source actual_law.py L241–242,276–288 uses D1 diffusion storage in the BE stage, not an assumption that the public initial state lies exactly on the static diode equilibrium manifold. Let z=Is exp(vj/aV), tau=2 ns and define
```math
\begin{gathered}
\eta_0=z_{\rm old}-I_s-i_{b,\rm old},\\
\Delta i_b=(1+\tau/h)(z-z_{\rm old})+\eta_0,\\
\Delta v_j(\Delta i_b-\eta_0)\ge0,
\end{gathered}
```
for the source-compatible monotone exponential. A proposed Schur/Brouwer proof that substitutes Delta ib=(1+tau/h)(z-z_old) and declares Delta vj Delta ib>=0 for EVERY first-PREP state is therefore **incorrect unless eta0=0 has been independently qualified**. Fresh read-only first archived Pro18E source seed x[38:40]=(5.193079316339365,1.727274097021394e-08) A, x[40:42]=(4.087729751223548,-154.4820273950659)V, original law Is≈8.312221736852897e-13A, aV≈.13873992725386358V yields eta0≈(+2.499602568218e-4,-1.727357219239e-8)A, NOT zero. Q2's exp has near-underflow scale in binary64, but its mismatch sign/magnitude is robust. Actual first-seed admissible scalar diode perturbation delta vj_Q1=-1e-7 V yields delta ib_Q1≈+0.000128305918 A and delta vj*delta ib≈-1.28305918e-11 W <0, an explicit signed counterexample to the previously assumed product nonnegativity on the actual source history. Thus the root-level Schur body relation acquires an actual signed eta0 correction and the radial lower bound must retain Delta vj eta0, with diode-domain nonzero storage and bracket qualification. **Critical scope correction:** a consistently reference-centered Schur construction may instead define beta=i_b,new−(z_old−I_s), in which case Delta v_j * beta>=0 and a KCL residual centered at i_b,ref=z_old−I_s cancels the eta0 correction exactly. The true-source negative product refutes using the *physical old-state increment* as the sign-monotone coordinate, but does NOT by itself refute a correctly beta-referenced Schur identity. A full first-PREP 50D guarded-root existence upgrade remains **not independently accepted this round** because its rational 32×8 coefficient extrema, fixed convex source-wide map and diode/thermal selfmap have not been fully reproduced by the independent counterauditor; no all-equation source-root/solver result is claimed merely from the successful G11 scalar faces. This is a new SOURCE-SPECIFIC falsifier, not a synthetic toy or an assertion that physical roots do not exist. To repair: recompute bordered transfers, signed radial/diode endpoint bounds and Brouwer thermal/electrical selfmap with this measured eta0, then independently direct-evaluate all original coefficients before upgrading.


**S-L19 new actual-first-PREP root-CONDITIONAL Schur G11 gate, not accepted root existence.** Independently reconstructed original 26-node G,B,GS,GD,DS,XO stamps (actual_law.py L184–203) and all 32 coefficient corners for L_s∈[4.02,4.58]nH, literal segmented cG11∈[1.7,527]pF, noncollocated G12 cG12∈[56.8,1016]pF; independent floating sanity confirmed Sii>=.0592349115ohm, |Soff|<=.0075537492ohm, |Poff|<=.0073550911ohm, Sii−|Pii|>=.0016973449ohm. The separate worker used rational-residual corner correction and conservative stated bounds Sii>.059234910, |Soff|<.007553750, |Poff|<.007355092, Sii−|Pii|>.001697343; *independent re-execution of all directed certificates is not supplied*. Let beta_i=i_b,new−(z_old−Is), NOT the physical Delta i_b; this reference ensures Delta vj_i * beta_i>=0 despite S-L18's nonzero eta0. For any ACTUAL exact real root satisfying the declared OFF/T25–25.07 branch/tube and charge coefficient ranges, elimination gives (S+diag(r+k))beta=t−b, k>=0, S=DS^T A^-1DS, P=GD^T A^-1DS, t=DS^T A^-1rho_ref, q=GD^T A^-1rho_ref and Delta GD=−q+P beta. If independently justified |b|<.57V, |t|<.028508396V, |q|<.027735716V, and r>=.0699ohm, then
```math
\begin{gathered}
\|\beta\|_\infty<
\frac{.57+.028508396}
{.0699+.059234910-.007553750}
<4.923\ {\rm A},\\
\|\Delta GD\|_\infty<
.027735716+.598508396\\
+(.007553750+.007355092)\,4.923
<.700\ {\rm V}<1\ {\rm V}.
\end{gathered}
```
The inequality proves that **IF** the proposed real-lifted 50D OFF/cool first-step root exists inside that source-centered branch and all listed source coefficient/transfer bounds are valid, its FINAL G11 control satisfies the accepted 1V ROOT guard; it does **not** show the entire 84W ellipse lies inside guard or that the actual source Newton TRIALS converge legally. Verifying continuous fixed-SPD Brouwer selfmap, thermal/diode evaluator brackets, source input exactness, initial diode-reference beta and all legal root branches is a logically separate existence obligation. Thus the withdrawn S-L13 unconditional accepted-root existence wording is NOT restored here. An inconsistent replacement of beta with physical Delta ib is explicitly falsified by S-L18. This is a materially stronger prospective root-only GUARD exclusion, not proof of an accepted 50D source run.
