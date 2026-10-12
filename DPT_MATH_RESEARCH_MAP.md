# DPT-R1 × OpenAI Math：成果利用与下一数学问题

更新：2026-10-12。覆盖本地已接受的 Pro18A/B/C 及其后续定向复算；尚在建设的证书只记为未决对象。

OpenAI Math 对 DPT 的主要贡献，已经从“提示如何检查信息不足”发展到三个可计算对象：**同一可达类上的信息下界与观测修复上界、主动多阶段命令中的历史反例、主动校准后的目标预测**。下一步最值得攻的是把这些对象接成有限域、多阶段的可靠预测结构，同时回接原始有效换流电感问题。

本页服务 Math side 的选题和复用。DPT 科学 authority 仍由本地 accepted evidence 拥有；这里记录使用后果，不替代冻结评分。原来的长篇阅读展开可从 [Git 历史](https://github.com/Gogoal-L/math/commits/main/DPT_MATH_RESEARCH_MAP.md) 找回，专题推导继续保留在 [dpt_research](dpt_research/)。

## 0. 承重数学主线：从论文公式到 DPT 可验证命题（2026-10-12）

本节直接给定义、推导、适用前提、反例和具名物理接口。专题笔记提供证明原文 locator；这里不再把“看过某篇论文”当作数学成果。**上游 F119/F129/F132 的定理**与**以下独立构造的 DPT 线性/非线性引理**始终分开。共同前提：reference、source law、preparation、外部 observation、端口/符号、合法 command word、目标窗口和 nuisance 域必须固定；100 V 原始 R1、150 V active history/CAL 与 600 V native 是不同 evidence chart。

### 0.1 科学目标不是恢复 θ，而是恢复规定命令下的 G

令 $`h\in\mathcal H_{\mathcal R}`$ 是由合法 preparation 在参考系统 $`\mathcal R`$ 中生成的 source-reachable 历史；$`O(h)`$ 是**目标计算之前允许取得的外部观测**；$`T_w(h)`$ 是按实际顺序执行合法有限命令字 $`w`$ 后的 source state；$`G_j(T_w(h))`$ 是具名 work/peak/event-time。参数 $`\theta=(L_g,L_s,L_d,L_{\rm loop},R_g,\ldots)`$ 及未测电荷/热态并不默认可由 $`O`$ 唯一恢复。正确的决策对象是：

**(M1)**

```math
\boxed{
\mathcal R_{j,w}(O,\mathcal H_{\mathcal R})=
\inf_{\widehat G:\,O\mapsto\mathbb R}\ 
\sup_{h\in\mathcal H_{\mathcal R},\ \text{合法误差}}
|\widehat G(O(h))-G_j(T_w(h))|.
}
```

若两个合法 $`h_+,h_-`$ 在误差合同下可生成同一观测 $`y`$，则任何观测型预测器在 $`y`$ 只能输出同一个数，三角不等式立即给

**(M2)**

```math
\mathcal R_{j,w}\ge\tfrac12|G_j(T_w(h_+))-G_j(T_w(h_-))|.
```

这解释 18B 的未来 peak 差是**不可避免误差的下界见证**，不是整个可达类的上界；18C 的 L 不唯一与目标 work 稳定可同时成立。有限 bank 的小 goal spread **不是**全域小 $`\mathcal R`$ 的证明。该统一对象既可作用于工程目标，也容纳 18A 的严格噪声/证书结果。

### 0.2 F132：从嵌套敏感度证明提炼“联合干预”的可证伪方程

原文：[F132 construction](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/01-construction.tex)、[recurrences](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/02-recurrences.tex)、[separation](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/03-separation.tex)。

对 total Boolean $`f`$，$`s(f,x)`$ 统计单 bit 翻转的变化数，$`\operatorname{bs}(f,x)`$ 是可同时选出的**互不相交敏感输入块**数。F132 构造深度 $`d`$、目标数 $`M`$、门控数 $`k=2M^2+1`$、$`r=\lceil\sqrt M\rceil`$ 的嵌套 predicate。其承重处是必须同时维护普通敏感度 $`S_{\ell,b}`$ 与共同翻转两种 predicate 的 $`J_{\ell,b}`$，其典型递推为

**(M3)**

```math
\begin{aligned}
 S_{\ell,1}&\le M^2S_{\ell-1,0}+rS_{\ell-1,1},&
 J_{\ell,1}&\le M^2J_{\ell-1,0}+rS_{\ell-1,1},\\
 S_{\ell,0}&\le16S_{\ell-1,0}+S_{\ell-1,1}+3J_{\ell-1,1},&
 J_{\ell,0}&\le16S_{\ell-1,0}+3J_{\ell-1,1}.
\end{aligned}
```

其中常数 16 来自标签控制的 near-accepting targets，3 来自 tournament gate-only 候选；省去 $`J`$ 会漏掉“一次 bit 翻转同时修复多个 gate”的路径。最终 Boolean 构造有

**(M4)**

```math
\begin{aligned}
s(f)&\le 2(d+2)M^{d+1},\\
\operatorname{bs}(f,0)&\ge M^2(2M^2+1)^d,\\
\frac{\operatorname{bs}(f)}{s(f)^2}
&\ge \frac{2^d}{4(d+2)^2}.
\end{aligned}
```

**独立 DPT 迁移引理：** 对两个**同时可合法操控**的物理/命令参数 $`a,b`$，固定同 reference 的四角目标值 $`G_{00},G_{10},G_{01},G_{11}`$。定义交互对比

**(M5)**

```math
\Delta_{ab}G=G_{11}-G_{10}-G_{01}+G_{00}
=\int_{a_0}^{a_1}\!\!\int_{b_0}^{b_1}
\frac{\partial^2G}{\partial a\,\partial b}\,db\,da
```

（积分式需要整块合法域内 $`C^2`$ 正则）。**任何**加性 ordinary $`Q(a,b)=q_1(a)+q_2(b)`$ 均有 $`\Delta_{ab}Q=0`$。若四角的 absolute forecast error 都不超过 $`\epsilon`$，则 $` |\Delta_{ab}G|\le4\epsilon`$；因此

**(M6)**

```math
\boxed{\max_{\text{四角}}|G-Q|\ge|\Delta_{ab}G|/4.}
```

若四次 source goal 求值分别仅知误差界 $`\eta_{00},\eta_{10},\eta_{01},\eta_{11}`$，能核验的下界为 $`(|\Delta_{\rm observed}|-\sum\eta)_+/4`$。此界对 $`G(a,b)=ab`$ 的四个 $`0/1`$ 角点可达到（最佳加性拟合误差 $`1/4`$）。因此它是**针对加性模型类的锋利 falsifier**，不是“所有普通 nonlinear 模型不可能”的定理，也不继承 F132 的 superquadratic exponent。对于 Rg×L、历史×CAL、stage×command 等，只在四角 preparation/branch/端口一致且合法时应用。比较现有 [mixed_interaction_audit](dpt_tools/mixed_interaction_audit.py) 的 source-level four-corner 对比；普通二阶耦合模型仍是强 rival。

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
\mathcal V_0&=\operatorname{row}(C),\\
\mathcal V_{k+1}
&=\mathcal V_k+\sum_{u\in\mathcal A}\mathcal V_kA_u,\\
\mathcal V_\infty
&=\operatorname{span}_{w\in\mathcal A^*}\operatorname{row}(CA_w).
\end{aligned}
```

若 $`\dim x=n`$，该升链最多发生 $`n-\dim\mathcal V_0`$ 次严格增维；稳定后 $`\mathcal V_\infty A_u\subseteq\mathcal V_\infty`$，所以以此 row basis $`T`$ 定义 $`z=Tx`$，存在准确 reduced update $`T A_u=\bar A_u T`$。任何线性**自主演化且覆盖所有词目标**的商状态，其 row space 必须含 $`\mathcal V_\infty`$；最小维数为 $`\dim\mathcal V_\infty`$。[goal_word_quotient](dpt_tools/goal_word_quotient.py) 计算这一命题。**有限指定** $`\mathcal W`$ 则只要求 $`\operatorname{row}(CA_w:w\in\mathcal W)`$，不是 all-word autonomous closure。

另一个可以直接测试的结果是**顺序交换缺陷**：

**(M9)**

```math
G_{A\to B}(x)-G_{B\to A}(x)
=C(BA-AB)x=C[B,A]x.
```

若两个短命令是连续 vector fields $`f_A,f_B`$ 的小 $`\Delta t`$ 演化且流光滑，状态交换缺陷的一阶非零项为 $`\Delta t^2(Df_B f_A-Df_A f_B)+O(\Delta t^3)`$；stage 输出/事件守卫仍可能额外产生差异。既有 18B 的 ordered-command 结果与此**问题形式**相符，但 actual switched/guarded law 并非一个全局线性交换子，因此必须用 native legal $`A\to B,B\to A`$ 两次实际执行来判定。

### 0.4 F119：从信息产生率看清“相关噪声”的定理边界

原文：[F119 main theorem](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/main.tex)、[canonical three-point optimizer](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/sections/canonical.tex)、[thinning](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/sections/thinning.tex)、[flow](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/sections/flow.tex)。

在**均匀独立输入 + 各坐标独立 binary-symmetric noise** 的原定理中，令

**(M10)**

```math
\begin{aligned}
\psi(r)&=\tfrac12\bigl[(1+r)\ln(1+r)+(1-r)\ln(1-r)\bigr],\\
I(u)&=H(\mathbb E u)-\mathbb E H(u),\\
F(\psi(r))&=r\,\operatorname{atanh}r.
\end{aligned}
```

噪声半群 $`P_t=T_{e^{-t}}`$、$`N_0=\frac12\sum_i(\mathrm{Id}-\mathrm{flip}_i)`$ 满足精确导数

**(M11)**

```math
\frac{dI(P_tu)}{dt}
=-\mathbb E[\operatorname{atanh}(P_tu)\,N_0P_tu]
=-D(P_tu).
```

论文经 three-point entropy-budget optimizer、convex-perspective reserve、common-output thinning 和维数归纳证明 $`D(g)\ge F(I(g))`$。置 $`r_t=\psi^{-1}(I(P_tu))`$，由 $`\psi'(r)=\operatorname{atanh}r`$ 得 $`r_t'\le-r_t`$，积分即

**(M12)**

```math
\boxed{I(T_\rho u)\le\psi(|\rho|\psi^{-1}(I(u)))}.
```

**必须区别两个独立性假设：** 中间 joining cost 优化允许两个 child fields 耦合，但输入 $`X_i`$ 与噪声 $`Z_i`$ 的独立性在原定理中不可取消。显式反例：$`X_1,X_2`$ 独立公平 signs，$`Y_i=X_i Z_i`$。独立 $`Z_i`$ 时，coordinate/parity 的互信息为 $`\psi(\rho),\psi(\rho^2)`$；若噪声完全共享 $`Z_1=Z_2=Z`$，则 $`Y_1Y_2=X_1X_2`$，**parity 恰好无损**。这只推翻“F119 coordinate optimum 也适用于相关噪声”的迁移，未推翻 F119 本身。DPT 的工程启发是检查**共享 offset/gain/skew 是否真的构成可消去的 nuisance 方向**，不是把二元互信息 bits 当作 volt/nJ deterministic error guarantee。

### 0.5 三篇真正联合的严格结果：future-goal minimax radius with mixed nuisance

这是本 Math 仓库的新**独立线性模型推导与实现**，不是宣称 F119/F129/F132 直接推出 SiC 定理。假设有限 source chart 由

**(M13)**

```math
\begin{aligned}
x&=x_0+Bz,\qquad \|z\|_2\le1,\\
y-y_0&=HBz+N\eta+Ee,\\
&\|e\|_2\le1,\qquad \eta\in\mathbb R^p.
\end{aligned}
```

这里 $`N\eta`$ 是**可任意大的同一个未知线性 nuisance**，$`Ee`$ 是**联合、可相关、确定性有界**的传感器误差；$`z,e`$ 是**彼此独立的两个单位球预算**，不能由普通样本 covariance 自动获得。命令 $`w=(u_1,\ldots,u_\ell)`$ 的 linear update 为 $`F_w=A_{u_\ell}\cdots A_{u_1}`$，第 $`j`$ 个未来目标的线性部分是 $`c_{w,j}^\top z`$，其中 $`c_{w,j}=B^\top F_w^\top C_j^\top`$。令 $`A=HB`$。

**定理（标量、有限维、整个声明线性 chart 的 minimax radius）：**

**(M14)**

```math
\begin{aligned}
R(c;A,N,E)
&=\inf_{\widehat g}\sup_{\|z\|,\|e\|\le1,\eta}
 |c^\top z-\widehat g(Az+N\eta+Ee)|\\
&=\max_{\substack{\|z\|\le1,\ \|e\|\le1\\Az+Ee\in\operatorname{im}N}}
 |c^\top z|\\
&=\min_{\substack{a\in\mathbb R^m\\N^\top a=0}}
 \left(\|c-A^\top a\|_2+\|E^\top a\|_2\right).
\end{aligned}
```

证明的三步：① 对可由反号 $`(z,e,\eta)`$ 形成同一 $`y=0`$ 的两条历史，所有 decoder 至少承担 $`|c^\top z|`$；② 对任意 $`N^\top a=0`$，线性预测器 $`a^\top(y-y_0)`$ 的误差由两个单位球的 support function 上界给出式 (M14) 最后一行；③ 将 $`(z,e)`$ 的紧凸对称积球与观测线性等式作 Lagrange/Fenchel dual（原点满足严格球内点），上下界相合。因此**存在最优线性外部 readout**，不需要先估计全部 $`x,\theta,\eta`$。该结论属于已有 optimal-recovery 范畴，相关标准来源：[Foucart–Liao, Journal of Complexity 83 (2024), 101841](https://doi.org/10.1016/j.jco.2024.101841)；这里只作具名 mixed-nuisance 归约与 DPT 使用合同。

**把无界 nuisance 与零噪声 contrast 分两次剔除：** 取 $`U_0`$ 张成 $`\ker N^\top`$，设 $`A_0=U_0^\top A,E_0=U_0^\top E`$。$`E_0`$ 的 compact/full-left SVD 写成 $`E_0=U_r\Sigma_rV_r^\top`$，其正交余方向为 $`U_\perp`$。由于 $`U_\perp^\top E_0=0`$，任何兼容状态差 $`z`$ 必须满足

**(M15)**

```math
Kz=0,\quad K=U_\perp^\top A_0;
\qquad z=Zv,\quad Z^\top Z=I,\quad\operatorname{im}Z=\ker K.
```

再定义 $`M=\Sigma_r^{-1}U_r^\top A_0Z`$、$`c_r=Z^\top c`$，则

**(M16)**

```math
\boxed{
R=\max_{\|v\|\le1,\ \|Mv\|\le1}|c_r^\top v|,
\qquad
R^2=\min_{0\le q\le1}
 c_r^\top\big[(1-q)I+qM^\top M\big]^{-1}c_r.
}
```

端点奇异时沿 $`q\to0^+,1^-`$ 取兼容极限，不以盲目 Moore–Penrose 代替无穷方向。**推导而非仅引用优化器：** 对 $`D_q=(1-q)I+qM^\top M`$，Cauchy–Schwarz 给
$`(c_r^\top v)^2\le(c_r^\top D_q^{-1}c_r)(v^\top D_qv)\le c_r^\top D_q^{-1}c_r`$；在最小化的内点 $`q^\star`$，令 $`v_\star=D_{q^\star}^{-1}c_r`$，一阶导数为 $`\|v_\star\|^2-\|Mv_\star\|^2=0`$，规范化即可同时触及两个约束并达到上界。端点最优时对应单个活跃约束；若有奇异方向先依 (M15) 消去。故式 (M16) 是全局可计算结果，而不仅是局部 SVD heuristic。实际代码仍有 floating-rank 门槛，其“半径 0”只有在物理证明 exact common mode 时才可以作为物理零误差。

多个未来词、多个工程目标各有容许误差 $`\tau_j>0`$。对所有目标使用同一预测前观测、分别构造最优线性 decoder，**归一化 worst-case 最大误差**准确等于

**(M17)**

```math
R_{\infty,\mathcal W}=
\max_{w\in\mathcal W,\ j}\frac{R(c_{w,j};A,N,E)}{\tau_j}.
```

因此 $`R_{\infty,\mathcal W}\le1`$ 是声明模型/传感器/有限 word 下的**达到工程容差的充分且必要条件**；不是全 command language 或 nonlinear source 的证书。[contextual_goal_recovery.py](dpt_tools/contextual_goal_recovery.py) 实际计算此式，调用 [goal_ellipsoid_recovery.py](dpt_tools/goal_ellipsoid_recovery.py) 的一维 $`q`$ 求解器；[8 项解析＋CLI 测试](dpt_tools/test_contextual_goal_recovery.py) 覆盖命令先后、rank-one shared noise、independent noise、预测前 CAL 和非法输入。

**由 (M16) 退化出的无噪声 rank 定理：** 当 $`E=0`$，$`R(c)=0`$ 当且仅当 $`c\in\operatorname{row}(U_0^\top HB)`$。若一组未来目标在 $`z`$ 坐标堆为 $`\Gamma_{\mathcal W}`$，允许免费设计任意理想、无新增 nuisance 的标量测量，则最少还缺的独立读数为

**(M18)**

```math
k_{\rm ideal}=
\operatorname{rank}\begin{pmatrix}U_0^\top HB\\\Gamma_{\mathcal W}\end{pmatrix}
-\operatorname{rank}(U_0^\top HB).
```

这与已有 [contextual_goal_quotient.py](dpt_tools/contextual_goal_quotient.py) 一致；$`B`$ 非满秩时必须先写在可达 $`z`$ chart 中，不能把整个 ambient parameter space 当作真实 reachable space。真实 CAL/传感器只能从**有限合法候选库**购买，所需 channel 数可能大于理想 $`k_{\rm ideal}`$。

**精确小例子：** $`B=H=I_2,\ N=(1,1)^\top,\ E=0,\ C=(1,-1),\ A_{\rm future}=\mathrm{diag}(1,-1)`$。当前 goal 为 $`x_1-x_2`$，可用 $`y_1-y_2`$ 精确计算，$`R_{\rm now}=0`$；未来 goal 变成 $`x_1+x_2`$，却与无界共同 offset 混淆，$`R_{\rm future}=\sqrt2`$（状态先验是 $`\|z\|_2\le1`$，不是两个独立区间）。若合法预测前 CAL 另读 $`y_3=\eta`$，则 $`y_1+y_2-2y_3=x_1+x_2`$，future 半径归零。若原两通道分别有联合球 $`\|e\|\le1`$ 的 **0.1 倍独立误差**，CAL 后 $`R_{\rm future}=0.1\sqrt2`$；共享的 0.2 倍噪声 $`E=0.2(1,1)^\top`$ 则在差分方向仍完全消去。**这个小例子的单位是归一化状态/目标，不是 V、nH 或 nJ。**

### 0.6 非线性 DPT 恰好还缺的东西：余项、work 事件、peak 守卫

源器件电荷本构、Coss/Crss、body diode 与模式/事件切换一般使 (M13) 只是局部近似。在同一**具名合法非零域**，若观测与某个 future scalar goal 有

**(M19)**

```math
\begin{aligned}
O(z)&=y_0+Az+N\eta+Ee+r_O(z),\\
G_w(z)&=G_{w,0}+c_w^\top z+r_{G,w}(z),\\
\|r_O\|&\le\beta_O,\qquad |r_{G,w}|\le\beta_{G,w}.
\end{aligned}
```

则对任何 $`N^\top a=0`$，有可复算的**非线性条件上界**

**(M20)**

```math
\begin{aligned}
\sup|\widehat G_a-G_w|
&\le\|c_w-A^\top a\|+\|E^\top a\|\\
&\quad+\beta_{G,w}+\|a\|\beta_O,\\
\widehat G_a&=G_{w,0}+a^\top(y-y_0).
\end{aligned}
```

证明是展开残差、消去 $`N\eta`$、逐项取范数。最小化右侧时**应当把 $`\|a\|\beta_O`$ 一起计入**；先以 (M14) 选出放大系数很高的 decoder 再忽略 remainder，会虚报修复。关键不足是从 actual coupled source 给出 $`\beta_O,\beta_G`$ 在准备/未来共同合法域的统一上界，而不是把 finite-bank 最大残差称为证书。式 (M14) 的精确 minimax 下界不能在非线性 remainder 未控制时照搬。

对于真正的 DPT signed stage work（需固定端口、电流方向与窗口），设

```math
W(z)=\int_{t_a(z)}^{t_b(z)} V_{DS}(t,z)I_D(t,z)\,dt.
```

Leibniz rule 给出真实目标导数：

**(M21)**

```math
\begin{aligned}
DW[\delta z]
&=\int_{t_a}^{t_b}
\bigl(I_D\,DV_{DS}[\delta z]+V_{DS}\,DI_D[\delta z]\bigr)\,dt\\
&\quad+[V_{DS}I_D]_{t_b}Dt_b[\delta z]\\
&\quad-[V_{DS}I_D]_{t_a}Dt_a[\delta z].
\end{aligned}
```

若事件由 $`\phi(t,z)=0`$ 定义且 **transversal**，$`|\partial_t\phi|\ge\gamma>0`$，隐函数定理给

**(M22)**

```math
Dt_\ast[\delta z]=-\frac{D_z\phi[\delta z]}{\partial_t\phi}.
```

当 crossing 斜率接近 0、峰值多重或 guard 换支时，$`DG`$ 及 $`\beta_G`$ 可能剧增甚至失去该光滑表示。对于唯一内部光滑非退化 peak，包络定理的一阶 peak-value 导数是 $`D_z V_{DS}(t_\ast,z)`$，但 **peak time** 仍需另行求导；有多个几乎相等的 ringing peaks 时不能随意选择其中一个导数。

18B 的配对实值例子表明目标种类本身很重要：

**(M23)**

```math
\begin{aligned}
\Delta W_1&\approx+1.628664~\mu{\rm J},\\
\Delta W_2&\approx-1.686273~\mu{\rm J},\\
\Delta W_{\rm total}&\approx-57.609755~{\rm nJ},\\
1-\frac{|\Delta W_{\rm total}|}{|\Delta W_1|+|\Delta W_2|}
&\approx 98.26\%.
\end{aligned}
```

这解释了为什么单个 total-work goal 可以比两阶段 work、peak/event 更稳定。它**不是** total Eon/Eoff 的全局稳定定理；目标必须与正式窗口、积分符号及 source 端口一致。

### 0.7 回接原始 R1 的可辨识方向，而非把数学停在抽象 chart

在**声明 KVL 符号、实际 source 电流导数与明确 discrepancy**的低阶 turn-off 诊断中，可将外部 overshoot 近似写作

**(M24)**

```math
u(t):=V_{DS}(t)-V_{\rm DC}
\approx L_{\rm eff}s(t)+R_{\rm loop}I_D(t)+b(t),
\qquad s(t)=-\frac{dI_D}{dt}.
```

若将允许的 offset/电阻/传感器偏差基函数离散堆成 $`N_s`$，令 $`P_\perp`$ 是加权 $`W`$-内积对 $`\operatorname{col}N_s`$ 的正交投影，则在线性、已知 $`s`$ 情形

**(M25)**

```math
\widehat L_{\rm eff}
=\frac{\langle P_\perp s,P_\perp u\rangle_W}{\|P_\perp s\|_W^2},
\qquad
|\widehat L_{\rm eff}-L_{\rm eff}|
\le\frac{\|\epsilon\|_W}{\|P_\perp s\|_W}.
```

若 $`P_\perp s=0`$，该实验无法区分有效 L 和允许 nuisance；若它很小，即使 waveform 拟合完美，参数也会不稳定。注意 **s 的数值微分误差、gate-charge/Coss 非线性、internal Kelvin source 与 external cut port 不一致**均可破坏 (M24) 的条件；它不是 LTspice/硬件的已核验器件方程。更重要的是，某个未来 overshoot/work 的导数 $`DG`$ 可能在这个不可辨识方向上很小，于是 (M1)/(M14) 允许目标稳定而 L 不唯一。下一步该拿真实 R1 reference 的同源 $`O,DO,DG,s,N_s`$ 与设备外部 cut record 来检验，而不是借用 150 V CAL 的 chart 替 100 V R1 作证。

#### 传感器关联误差真正进入 stage-work：common time shift 与 relative deskew 的定量分解

这是一条来自 DPT 积分定义、独立于 F119 随机通道定理的**物理测量方程**。在固定窗口 $`[t_a,t_b]`$ 上，若探头读到 $`V_m(t)=V(t+\delta_v)`$、$`I_m(t)=I(t+\delta_i)`$，且两波形在声明窗口中 $`C^2`$、偏移足够小，Taylor 展开给

**(M26)**

```math
W_m-W
=\delta_v\!\int_{t_a}^{t_b}\dot V I\,dt
+\delta_i\!\int_{t_a}^{t_b}V\dot I\,dt+O(\|\delta\|^2).
```

设共同偏移 $`\delta_c=(\delta_v+\delta_i)/2`$、相对偏移 $`\delta_r=(\delta_v-\delta_i)/2`$，由分部积分 $`\int(\dot VI+V\dot I)=[VI]_{t_a}^{t_b}`$ 可得

**(M27)**

```math
\begin{aligned}
W_m-W
&=\delta_c[VI]_{t_a}^{t_b}\\
&\quad+\delta_r\int_{t_a}^{t_b}
(\dot V I-V\dot I)\,dt\\
&\quad+O(\|\delta\|^2).
\end{aligned}
```

**可检查的解析负控：** $`V(t)=2+3t,\ I(t)=5-2t,\ [t_a,t_b]=[0,1]`$，符号积分精确给 $`W=13.5`$，并且 $`W_m-W=5\delta_c+19\delta_r-6\delta_c^2+6\delta_r^2`$。两项的系数 5、19 与 (M27) 严格一致。若积分窗口也随两条波形**共同平移**而移动，完整时间平移可由换元消去；(M27) 的共同边界项是针对**固定物理积分窗口**，不可混到自动事件窗口中。若两探头带宽/滤波不同，其误差不等价于单一 timing skew，还必须纳入频率响应 discrepancy。DPT 原始测量指导：[Wolfspeed Dynamic Characterization](https://www.wolfspeed.com/knowledge-center/article/dynamic-characterization-and-measurement-methods/)；[Hardware Testing Methodologies for Wide Bandgap High-Power Converters, Electronics 13 (2024), 3918](https://www.mdpi.com/2079-9292/13/19/3918)。这才是 F119“信息依赖噪声相关结构”的**可执行物理启发**：实际 source 需要同一波形时标、校准手段和误差相关性证据才能兑现；公式本身不测量任何探头偏差。

### 0.8 真正的 acquisition 判别：CAL 是干预，不只是增加一行 sensor

对于允许购买的预测前观测集合 $`\mathcal S\subseteq\mathcal M_{\rm legal}`$，每一个 candidate 都要有实物端口、获取时间、共同 nuisance/误差关联列和成本 $`c_s`$。在**同一个 source reference 与未来目标**上，有限预算下的目标相关设计问题为

**(M28)**

```math
\boxed{
\min_{\mathcal S\subseteq\mathcal M_{\rm legal}}
\sum_{s\in\mathcal S}c_s
\quad\mathrm{s.t.}\quad
\max_{w,j}R_{w,j}(\mathcal S)/\tau_j\le1.
}
```

这里 $`R_{w,j}(\mathcal S)`$ 来自具名 observation/N/E/goal chart 的 (M14–M17)；并非以单个参数 Jacobian condition number 或“测量越多越好”来替代目标误差。**若增加一个纯观测而不改变 preparation/物理状态，且旧误差合同仍作为新合同的正确 marginal**，最优 minimax radius 不会变大：新预测器可以忽略新读数，直接复用旧预测器。若 CAL 同时改变了物理状态，单纯套这个单调性是错误的实验比较。

尤其对于 18C 的**主动** CAL，设 $`K:\mathcal H\to\mathcal H`$ 是实际 CAL 操作，$`O_K`$ 是 CAL 后得到的外部读数。CAL 后未来目标是 $`G_w^K(h)=G(T_wK(h))`$，而非原来的 $`G(T_wh)`$。要只估计 **CAL 带来的信息价值**，需要同样执行 $`K`$、同样的后续未来，但在 predictor 输入中分别**隐藏或开放 CAL 数据**：

**(M29)**

```math
\begin{aligned}
R_{\rm withheld}^{K}
&=\inf_\delta\sup_h
 |\delta(O_{\rm pre}(h))-G(T_wK(h))|,\\
R_{\rm measured}^{K}
&=\inf_\delta\sup_h
 |\delta(O_{\rm pre}(h),O_K(K(h)))-G(T_wK(h))|.
\end{aligned}
```

这两个对象固定 **同一 CAL-induced physical history**，所以 $`R_{\rm measured}^K\le R_{\rm withheld}^K`$；若把 $`R_{\rm measured}^K`$ 与 no-CAL future $`G(T_wh)`$ 直接比较，观测的信息增益和操作 $`K`$ 的物理效应已混在一起。必须单列 CAL-versus-NO-CAL **干预/状态转移效应**，才能科学地解释 Pro18C 结果。

**最低成本可取得信息**还必须打败强 ordinary：完整记录 command、固定波形/斜率估计、合格 deskew、已知 CAL 执行日志、基于原 source 的低阶近似。优先的下一项证据是 150 V 同 reference 的 CAL-executed-and-withheld 对照或真实 B/history pair 的 source chart，冻结未来 word 和目标后再算 (M28)；不是扩大 PDF 数目或把理想 rank 直接命名为真实 sensor minimum。

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
\|I-HJ_F(x)\|_{\rho,\infty}\le\kappa<1
\quad(x\in B_\rho(c)),
\qquad
\|HF(c)\|_{\rho,\infty}\le(1-\kappa)\,;
```

最后一个条件这里的规范化盒半径定义为 $`\|x-c\|_{\rho,\infty}\le1`$。则 $`T(x)=x-HF(x)`$ 把该盒映入自身且收缩，有唯一合法 root $`x^\star`$，并且

**(M39)**

```math
\|x^\star-c\|_{\rho,\infty}
\le\frac{\|HF(c)\|_{\rho,\infty}}{1-\kappa},
\qquad
|G(x^\star)-G(c)|
\le L_G\frac{\|HF(c)\|_{\rho,\infty}}{1-\kappa}.
```

第二式假设在同盒内 $`G`$ 对相同加权范数有统一 Lipschitz 常数 $`L_G`$，其 guard、事件与积分窗口都已合格。**证明结构**是 Banach 自映射与收缩，加上 $`G`$ 的统一一阶增益；不是当前 600-V vendor 源已通过该完整 box 的宣告。把 (M37) 传入 $`\|HF(c)\|`$ 时还需其余 nodal/charge/network/thermal residual rows、共享 previous-state 相关性与完整伴随/goal 传播，不能只对一个 diode scalar 宣称全波形误差。

这条 (M34–M39) 是对**已提供实际耦合 BE 本构**的条件余项建设：F132 提醒不可漏组合项；F119 提醒不能用不合格噪声独立性；F129 提醒 previous-step charge 及合法命令历史影响后继响应。**数学计算来自指数电荷方程自身**；不是将任何 F119/F129/F132 的原定理直接移植到 SiC。该结果对应 V6 **600 V coupled BE branch**，与先前 150-V reference-completed trapezoidal descriptor 分开，不共享求解/物理资格。


### 0.11 深挖：真正的二阶可辨识对象是 observation fiber 的相对 Hessian

进一步核对 [Neuberger–Alexanderian–van Bloemen Waanders 2024 原文 §3](https://arxiv.org/html/2411.07532) 后，需要与其 **Bayesian-Gaussian quadratic-goal OED** 区分：它使用二次目标展开和后验方差进行传感器设计；我们这里独立推导的是**确定性、固定观测相容类上的最坏 scalar-goal 半径**。[Zhong et al. 2026 SIAM/ASA](https://doi.org/10.1137/24M1649344) 进一步处理非线性观察和未来 QoI 的 Bayesian information gain，但不提供以下硬误差界。完整证明、强反例、来源与物理接口见 [二阶 goal fiber 专题笔记](dpt_research/20261012_second_order_goal_fiber.md)。

**合法前提：** 在一份固定 source reference 的 pretarget preparation 点 $`h_0`$，外部观测 $`O(h)`$ 和冻结合法未来命令后的标量目标 $`G_w(h)`$ 是 $`C^3`$；$`DO(h_0)`$ 对观测空间满行秩。取 $`Z`$ 的列为 $`\ker DO(h_0)`$ 正交基，且最有趣的一阶“看似足够”情形满足

**(M40)**

```math
DO(h_0)Z=0,\qquad
DG_w(h_0)Z=0
\iff DG_w(h_0)=\lambda^\top DO(h_0).
```

根据正则水平集隐函数定理，若一整个**明确的、source-合法的 chart-ball** 都可达，则存在真正保持同一观测的曲线族 $`h(v)`$：

**(M41)**

```math
O(h(v))=O(h_0),\quad
h(0)=h_0,\quad Dh(0)=Z,\quad \|v\|_2\le r.
```

对观测约束二次微分并消去曲线弯曲的法向加速度，得到真正的目标二阶矩阵：

**(M42)**

```math
\boxed{
Q_w=Z^\top\left[
D^2G_w(h_0)-\sum_j\lambda_jD^2O_j(h_0)
\right]Z.
}
```

**推导：** $`DO\,h''(0)[v,v]+D^2O[Zv,Zv]=0`$，且 $`DG_w=\lambda^\top DO`$，所以 $`D^2(G_w\circ h)(0)=Z^\top(D^2G_w-\lambda^\top D^2O)Z`$。因此**只看 $`D^2G`$ 自身是错的**：非线性 observation 的曲率可以制造、也可以完全抵消未来目标的二阶歧义。

若确有整个合法 chart-ball 上的统一三阶上界 $`M_w`$（它是**真正复合函数 $`G_w\circ h`$** 的三阶导数界，不是单独 goal 的 ambient 三阶导数），Taylor 定理给

**(M43)**

```math
G_w(h(v))=G_w(h_0)+\tfrac12v^\top Q_wv+R_3(v),
\qquad |R_3(v)|\le M_wr^3/6.
```

定义 $`s_+=\max(0,\lambda_{\max}(Q_w))`$、$`s_-=\min(0,\lambda_{\min}(Q_w))`$。球内包括中心 $`v=0`$，二次型的精确最大最小分别是 $`r^2s_+/2,r^2s_-/2`$。固定外部观测时，一个 scalar decoder 必须输出同一数，其 minimax 最优输出是目标范围中点，故

**(M44)**

```math
\boxed{R_2(r)=\frac{r^2}{4}(s_+-s_-).}
```

对每个状态的目标统一扰动不超过 $`M_wr^3/6`$ 时，max 和 min 各移动至多该值。因此可得到**真正双侧的局部目标半径资格**：

**(M45)**

```math
\boxed{
\bigl[R_2(r)-M_wr^3/6\bigr]_+
\le R_{\rm fiber}(r)
\le R_2(r)+M_wr^3/6.
}
```

这里正号 $`[x]_+=\max(x,0)`$。若整个 global observation fiber 比这个 chart-ball 大，(M45) **仅有下界**可直接传递到全域，不能把局部上界命名为全域预测充分性。若 third-derivative 常数尚无严格来源，数值 Hessian 只能提供 $`R_2`$ 的主项诊断。

**两个物理直觉相反、但一阶完全相同的精确反例。** 在二维合法局部 chart $`|y|\le r`$，取 $`O=x+y^2`$。若目标 $`G=x`$，虽然 $`DG=DO`$ 于中心，其精确 observation fiber 为 $`x=-y^2`$，故 $`Q=-2`$ 且

**(M46)**

```math
R_{\rm fiber}(O=x+y^2,G=x)=r^2/2;
\quad R_{\rm fiber}(O,G=O)=0.
```

第二个目标 $`G=O`$ 的 ambient Hessian 并非零，但观测本身已经充分，所以相对 Hessian 正确地抵消了它。

**新增信息甚至可能一阶 Jacobian 为零。** 若旧观测为 $`O=x`$、未来目标为 $`G=y^2`$，一个**假设在 future 之前合法取得的非线性 CAL proxy** $`P=y^2+e,\ |e|\le\epsilon`$，在中心有 $`DP=0`$，却给出准确 deterministic minimax 半径

**(M47)**

```math
\boxed{R_{\rm with\ P}=\min(\epsilon,r^2/2).}
```

证明是：给定读数 $`p`$，相容目标值落在 $`[0,r^2]\cap[p-\epsilon,p+\epsilon]`$，最大区间长度为 $`\min(r^2,2\epsilon)`$。此 toy 不能被误说成工程上能在开关前直接测量未来 work；需要真实合法 CAL 的对应 proxy 与误差资格。它证明 first-order **rank 不是 nonlinear candidate 的完整 acquisition 价值标准**。

**未来命令的二阶曲率如何向 preparation 传播？** 设一步合法光滑更新 $`x_+=f_u(x)`$，后续 goal 为 $`g_+(x_+)`$，$`J_u=Df_u`$，则（所有量在对应实际 stage point 求值）

**(M48)**

```math
\begin{aligned}
D(g_+\circ f_u)&=J_u^\top Dg_+,\\
D^2(g_+\circ f_u)
&=J_u^\top D^2g_+J_u\\
&\quad+\sum_j(Dg_+)_jD^2(f_u)_j.
\end{aligned}
```

即使最后一阶段工程目标 $`g_+`$ 是线性的，**非线性 source command 的第二项仍可制造目标曲率**。这提供一种比把所有历史压成 28-state 直接构造更经济的必要信息审计：沿冻结命令词回传 goal gradient/Hessian，再在**同一 pretarget observation fiber** 上计算 $`Q_w`$。在共同合法 chart-ball、所有目标共同的 pretarget observation 和具名工程容差 $`\tau_j`$ 下，任意预测器至少要承担

**(M49)**

```math
R_{\infty,\mathcal W}\ge
\max_{w,j}
\frac{\bigl[\frac{r^2}{4}(s_{+,w,j}-s_{-,w,j})
-M_{w,j}r^3/6\bigr]_+}{\tau_j}.
```

**可验证代码**：[regular fiber curvature](dpt_tools/fiber_goal_curvature.py) 的 source Hessian/grad 输入及 backward command pullback；[12 项独立测试](dpt_tools/test_fiber_goal_curvature.py) 包括 120 个 cubic exact-fiber 场景和真实多项式两阶段命令的解析 oracle。它们验证数学实现，不代表自动提取了 LTspice/BE/trapezoidal source 的导数或完成了本构全域余项证书。

**对 18B/C 的可证伪选择：** (i) 150-V 同 reference/source 的完整 recorded-command ordinary 是否已经充分；(ii) 若不足，未见 pair 的未来 work/peak 歧义是否能由 $`Q_w`$ 特征方向定量预测；(iii) 合法 CAL 在不混入自身状态干预效应的条件下能否缩小真实 goal fiber，而不只是提高参数 Hessian 的秩；(iv) peak/event guard 换支导致光滑 chart 失效时，退回前面的 sup-norm peak 和分段 work 界。最强科学出口是**源码同域的条件下界 + 非线性有界上界 + 未参与拟合的未来预测**，而不是将这套微分几何称为已有 SiC 全局证书。

### 0.12 直接回接实际隐式 source 残差：不必显式构造整套 nonlinear update

上一段 (M48) 需要每个未来命令的状态更新 Hessian，但真实 DPT source evaluator 通常只提供离散隐式节点残差，例如 coupled backward Euler、梯形积分或带 charge/thermal 的求解器。正确的接口不必先全局求出状态转移 $`f_u`$。固定一个**合法命令** $`u`$，令前态 $`x`$、后态 $`z=f_u(x)`$ 满足整套离散 source 方程 $`F(z,x;u)=0`$，并假设真实点处 $`A=F_z`$ 可逆。于是由隐函数定理：

**(M50)**

```math
\begin{aligned}
F(z,x;u)&=0,\qquad A=F_z,\quad B=F_x,\\
J_u:=Df_u&=-A^{-1}B,\qquad A J_u+B=0.
\end{aligned}
```

目标 $`g(z)`$ 若只通过 postcommand 状态计算，则定义当前态 future goal $`G(x)=g(f_u(x))`$，求解 $`A^\top\lambda=\nabla g(z)`$ 得到 adjoint $`\lambda`$。任何前态方向 $`a,b`$ 诱导扩展 source 方向 $`p_a=(J_u a,a)`$、$`p_b=(J_u b,b)`$。连续对源残差**二次微分**并消去 $`D^2f_u`$，给出下式精确 Hessian-vector pairing：

**(M51)**

```math
\boxed{
\begin{aligned}
DG(x)&=J_u^\top\nabla g(z),\\
D^2G(x)[a,b]
&=(J_ua)^\top D^2g(z)(J_ub)\\
&\quad-\lambda^\top D^2F(z,x;u)[p_a,p_b].
\end{aligned}
}
```

**推导：** $`D^2F[(J_ua,a),(J_ub,b)]+A D^2 f_u[a,b]=0`$；代入 $`D^2(g\circ f_u)[a,b]=(J_ua)^\top D^2g(J_ub)+(\nabla g)^\top D^2 f_u[a,b]`$，再用 $`A^\top\lambda=\nabla g`$ 即得第二项的**负号**。实际实现须保留 $`F_{zz},F_{zx},F_{xz},F_{xx}`$ 全部块，尤其**同一步 current/previous charge 的相关性**，不能只对目标和当前态求 Hessian。该式可用求解当前 node Jacobian 与其转置来构造目标二阶方向导数；大规模 source 可采用 Hessian-vector products，而不必显式形成完整三阶存储张量。

**把式子作用到已提供的 V6 二极管 BE 子本构。** 若固定 $`a,I_s,\tau`$，并暂只检查 §4.7 的二极管 charge/conduction 对残差的贡献

**(M52)**

```math
F_{D,n}=i_{b,n}-I_s(e^{v_n/a}-1)
-\frac{\tau I_s(e^{v_n/a}-e^{v_{n-1}/a})}{h_n},
```

则控制电压块的**精确二阶残差导数**为

**(M53)**

```math
\begin{aligned}
\frac{\partial^2 F_{D,n}}{\partial v_n^2}
&=-\frac{I_s e^{v_n/a}}{a^2}
\left(1+\frac{\tau}{h_n}\right),\\
\frac{\partial^2 F_{D,n}}{\partial v_{n-1}^2}
&=+\frac{\tau I_s e^{v_{n-1}/a}}{h_n a^2}.
\end{aligned}
```

这两个项符号相反，且 previous charge 通过 $`1/h_n`$ 放大；**这是跨步 charge history 必须进入目标 Hessian 的精确 source 原因之一**。本式对该 scalar BE diode contribution 的交叉 $`v_n,v_{n-1}`$ 导数为零；但整套网络/器件/热残差的 mixed Hessian、隐式状态求解耦合与 guard 并不必为零。若 $`a=a(T)`$、$`I_s=I_s(T)`$，还要加入温度方向和其交叉偏导。本节不是把 diode branch 当作整个 vendor model。

对于一个合法相容 source 状态邻域，定义 $`\|D^2F\|`$ 为从两项归一化 source 方向到残差向量的双线性算子范数。由 (M51) 和 $`\|[J_u;I]\|_2^2=1+\|J_u\|_2^2`$（此处 $`\|[J_u;I]\|_2^2`$ **实际上等于** $`1+\|J_u\|_2^2`$），得条件目标曲率上界：

**(M54)**

```math
\boxed{
\|D^2G\|
\le \|J_u\|^2\|D^2g\|
+\|\lambda\|\,\|D^2F\|
  \bigl(1+\|J_u\|^2\bigr).
}
```

这帮助确定哪个 source 区域更值得重做有限域证书：$`F_z`$ 接近奇异、$`\|J_u\|`$ 大、指数电荷曲率大时，简单 constant/affine ordinary 的余项可能迅速上升；若 adjoint $`\lambda`$ 与曲率 source rows 正交，**某个工程目标**仍可稳定。这是**带目标投影的物理计算压力测试**，不是绝对的 source 器件精度定理。完整多步 work/peak 还需 stage goal/window boundary 与 guard。V6 的 150-V trapezoidal 与 600-V BE 残差不可混接。

[可执行隐式 source Hessian 工具](dpt_tools/implicit_goal_hessian.py) 实现式 (M50–M51)，输入同点完整 $`F_z,F_x,D^2F,\nabla g,D^2g`$；[独立解析测试](dpt_tools/test_implicit_goal_hessian.py) 包括精确含 $`F_{zx}`$ 交叉项的 rational source、含 $`F_{zz},F_{xx}`$ 的 implicit source，以及 200 个随机解析显式律与隐式残差一致性比较。需要在实际 DPT source 中冻结 reference、nodal 变量单位、求解分支和正确的上一时步 state，才可将输出放进 (M42–M49) 的真实 observation-fiber 计算。

**验证账本：** F119/F129/F132 的上述定理式从钉住的 [openai/math source](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb) 抽出；(M5–M6),(M8–M9),(M13–M22),(M24–M25) 是在具名假设下的独立有限维/分析推导。F119 相关噪声反例有精确有限枚举，F129 二状态 relation context 有全枚举，F132 小局部 grouped witness 有合成审计；[proof-level 细节](dpt_research/20261011_F119_F129_F132_proof_level_DPT_bridge.md)。联合半径工具另经独立的 70 组随机受约束 primal/dual 数值交叉检查（最坏绝对差约 $`9.14\cdot10^{-12}`$，其中 6 个严格容差下的 SciPy line-search status 未成功但最终可行迭代满足 $`10^{-8}`$ 约束容差；非形式证书），以及 analytic/CLI regressions。**没有真实 SiC source replay、没有物理参数/测量噪声资格、没有全部非线性 remainder 的统一证书。**

---

## 1. 从原预期到实际成果

Pro17C/D/E 提供了 actual coupled law、ordered-command forecast、有限更新与 source-derived 信息修复的执行基础。S09 随后建立同模型 native 对照、goal-dependent model reversal，以及强 affine / one-Newton 的竞争条件。18A/B/C 分别推进证明、动态反例和主动辨识；原始 R1 的观测受限恢复仍有独立证据义务。

| 单元 | 原来希望解决什么 | 已获得的实际增量 | 当前证据域与剩余问题 |
| --- | --- | --- | --- |
| **18A：可达信息与修复** | 将近匹配历史推进到合法 Q-fiber；补齐 preparation 误差传播 | 同一个 actual50 离散系统中，126 步 preparation＋128 步后续 hold 的 **254 步联合证书**；精确有理 Q-fiber 与合法域包含；预测前外部 VDS 读出提供更小的统一目标误差上界 | 声明初态、参数族、hold 分支和离散 law 内的条件结论。完整数字 command 三幅值可恢复该历史方向，是必须保留的强 ordinary；电压修复并非对所有输入预算都必要 |
| **18B：目标相关动态闭合** | 静态摘要是否能在后续 command 中继续支持目标预测 | 150 V 主动两阶段 actual-law 历史对产生 work、peak、事件差；有限 F4 类内构造 memory 修复。未见成员与细化 preparation 后重新 shooting **实际击穿原预测律的推广** | 有限 source 见证与已兑现 falsifier。当前坐标更新缺陷、目标差异和最小可取得 repair 尚未统一闭合；28-state 实现不是最小状态定理 |
| **18C：主动 CAL→未来目标** | 观测不到的本构方向是否妨碍未来预测；主动测量能否修复 | 150 V 同一 reference 中，关断不可见的 κ 方向在主动未来产生 work 差异；最终五点非线性 CAL chart 支持 12-member bank 预测；L 不唯一而特定未来目标相对稳定 | 有限 bank、局部证书与条件测量结论。完整 active preparation→CAL / future 的关联余项界仍未知；100、150、600 V 尚无同一物理验证链 |

### 18A：已兑现的严格信息改善

在声明的离散可达族和目标中，本地重放得到：

```math
\begin{aligned}
R_{Q\text{-only}}&\ge 2.2864273\ \mu\mathrm V,\\
R_{Q+V}&\le0.68783535
+1.06041884\,\varepsilon_V\quad(\mu\mathrm V).
\end{aligned}
```

这里 $`\varepsilon_V`$ 的数值以 µV 表示。若 $`\varepsilon_V<1.50750997\ \mu\mathrm V`$，增加预测前电压读出后的统一上界严格小于 Q-only 的不可避免误差下界。

这实现了“信息不足的合法见证＋有限信息修复”。输入合同同时改变修复的必要性：若完整 preparation command 已记录，Q 加第三幅值即可反演相关方向，无需新增传感器。µV 门槛是这个任务的条件数学预算，实际仪器可实现性尚未资格化。

### 18B：动态反例更扎实，修复推广受到实际攻击

- 原有限 F4 类：C2 peak 的 current-only 误差下界约 **1.300865 V**；memory quadratic 的条件上界为 **0.031606 V＋324.628·εm**，εm 以 V 表示。有限类上界与声明噪声合同绑定。
- 已冻结的第二未见成员 $`s=-12/7`$：quadratic 扩展 **5/9 项未过**。这是已评分的 source falsifier，不能用重新拟合抹去。
- preparation 细化后重新 shooting 达到冻结的 **5 nV / 0.1 nA** 近等观测合同；同一 future 下 C2 peak 差仍为 **2.586995 V**。分段 work 差约 **+1.628664 / −1.686273 µJ**，总差 **−57.609755 nJ**，相消约 **98.26%**；事件时间差约 **−1.624 / +1.391 ns**。
- 旧 memory/direct quadratic/cubic 在这个新匹配对上 **7/9 项未过**。已加强的是有限动态 obstruction；新网格近匹配尚不是 exact real fiber 或连续域证书。
- 总 work 可以比阶段目标更稳定；有限 F4 类内 constant ordinary 的总 work 半径约 **28.785842 nJ**。这是正面结果：目标集合决定所需信息，历史不同不意味着每个工程目标都需要复杂修复。

### 18C：非唯一参数恢复与稳定目标预测开始分离

- 关断 branch 上 channel 为零，κ∈[0.98,1.02] 在该观测中不可见；已有计算未来 signed-work 直径 **122.479683 nJ**。严格实数目标下界还需扣除两条 active 目标求值误差。
- 最终五点 chart 的 12-member source bank 最大误差：**Full 0.875243 nJ、N2 0.891739 nJ、Direct/Linear 5.875723 nJ**。N2 与 Full 的最大差仅 **0.017177 nJ**；有限 bank 内提高非线性求解精度的收益已很小。
- 七个非线性近等观测成员的 L 范围 **4.278748–4.321331 nH**，未来 work 直径仅 **0.335303 nJ**。这支持具名有限族内“参数仍不唯一、目标相对稳定”；七点直径不是整个 fiber 的上界。
- ±1 mA 声明样本扰动下，一个实际测试的 Full 误差为 **3.534100 nJ**；替换 16 ns anchor 后仍为 **3.525150 nJ**。额外锚点没有形成有意义的修复。
- 126-step preparation 的 L-direction 区间重放通过；**joint remainder 的已曝光最大值 6.086919 nJ 只是统一 β 的下侧诊断**，不是 β 上界。共同仿射测量链的 shape ratio 不覆盖独立样本误差、skew、滤波变化或 native discrepancy。

这里 work 均按各自声明窗口、端口和符号定义，不能直接命名为完整 Eon/Eoff；peak 与 overshoot increment 也分开。source 正例、数值路径变化和物理用途量级分别判断。

## 2. 哪些 OpenAI Math 真正反哺了研究？

“用于构造”指具体进入本地证明、算法或反例；“边界作用”指实际排除了不合法路线；“候选”尚未形成 DPT 后果。采用证明结构不等于继承原定理的常数、物理假设或形式化证明。

| 来源与最小 locator | 实际使用与新理解 | 利用状态 / 下一价值 |
| --- | --- | --- |
| [F266：MUB certificate](literature/F266_dimension_six_MUB_certificate.pdf)，pp.17–23，square inverse、center/tangent/remainder/readout | 18A 将 proposal＋certificate 组织方式用于实际 254-step 联合系统；18B 将误差与读出资格接到有限 F4 修复。关键进步是保留跨步相关性，而非每步独立放大误差盒 | **用于构造、已复算。** MUB 原全局证明未迁移；Banach 自映射与 verified inverse 的 DPT 推导及 Rump 等标准方法单独归源。下一攻 active joint certificate |
| [F229：three-state reconstruction](literature_archive/F229_three_state_reconstruction.pdf)，pp.6–9，§2 | 18A 区分 deterministic bounded-error 与 posterior/channel 语义；18B 区分 static goal sufficiency、recursive update 和跨阶段目标充分性 | **构造＋边界作用。** 不借用随机重构阈值。关键后果：低维读出成功不自动支持持续更新；完整 recorded-command ordinary 需公平保留 |
| [F376-A：solenoidal shear instructions](literature_archive/F376-A_solenoidal_shear_instructions.pdf)，Lem.2.1、§5.1 Eq.(14)；[F376-B 修订](literature_archive/F376-B_incompressible_box_computation.pdf) | 18B 实际按 partial update domain、命令前缀和 stage/edge outputs 定义动态任务；18A/C 检查后停在不适用处 | **B 用于构造；A/C 未迁移流体定理。** 新理解：endpoint summary 会遗漏后续仍影响目标的阶段信息；DPT 无需继承可逆流体或停机结构 |
| [F357：RCD coordinates](literature/F357_regular_RCD_bi_Lipschitz_coordinates.pdf)，Prop.5.4，pp.37–39 | C 借用方向相关组合与误差传播的证明思路，寻找关联而非独立盒的 bound；A/B 未使用 RCD 几何保证 | **C 证明结构启发。** DPT 半径、Jacobian/inverse、合法分支及常数仍须独立验证；不继承维数独立或点依赖常数 |
| [F374：Brenier stability](literature_archive/F374_Brenier_one_third_stability.pdf)，Prop.5.1，Eqs.(5.5–5.6) | C 追求直接约束目标 functional，避免先恢复全部不适定参数；A/B 未建立 OT 假设 | **C 证明结构启发。** 不迁移 $`1/3`$ 指数或 Wasserstein 常数。下一价值是 goal-sensitive compatible set，不是完整状态距离 |
| [F125：metric k-median recovery](literature/F125_metric_k_median_recovery.pdf)，Thm.1.1 | B 实际拒绝用曝光后的赢家划分构造“少量例外＋廉价主体”选择器；C 保持 PARK | **边界作用；DPT 正向 mapping 尚未完成。** 只有预测前特征能识别例外域，才值得发展廉价 ordinary＋少量补信息路线 |
| [F116-A](literature/F116-A_noncommutative_hitting_point.pdf) / [F116-B](literature/F116-B_rational_hitting_lists.pdf)，定义域与 hitting assumptions | Pro17/S09 对 ordered command、表达式 definedness、原 law 与替代实现的身份检查；A 检查实际 exp/clip 系统后拒绝 rational universal-hitting 迁移 | **前期构造＋边界作用。** 新 native ordered positives 属于 DPT 自身；不宣称 vendor map 满足自由矩阵定理 |
| F365-A/B/C、F372：观测 quotient、nonlinear lift 与物理辅助对象 | source derivative、合法观测、局部 lift、有限半径证明义务进入 S09 的 K/Q 信息修复；后续由 A 的 exact fiber、B 的动态反例、C 的非线性 chart 推进 | **方法已吸收。** PDE/gauge/elasticity 原定理不直接证明 DPT identifiability；继续用实际 reachable chart 与观测合同 |
| F329、F355：直接 ambiguity 与有限阶 obstruction | 形成有限 bank/fiber 下界和 $`K=DG\,DF\,DP`$ 的信息分解；A/C 将部分问题推进到实际构造 | **独立 DPT 引理与构造。** scalar fiber 的半直径下界、K/N 线性代数不是原论文的新定理；不能由一个 scalar 失败推出所有一维表示失败 |
| F140：memory/precision 信息预算 | 区分 acquired waveform、retained summary、完整数字 command、内部 oracle 与新传感器；A 的 recorded-command rival 明确改变“最低新增信息”的判断 | **预算与边界作用已兑现。** 无 DPT Gaussian sample/bit 下界；数字压缩不自动减少 ADC 采样 |
| F332、F324、F094、F098 及 F049/F149/F360 | 强化坐标、延拓、维数、正则性和可达域的适用条件检查 | **保留专题阅读，暂非 ABC 承重计算。** 没有新的实际输入或可计算后果时 PARK；[F049/F149/F360 原文审计](dpt_research/20261010_F049_F149_F360_fulltext_proof_audit.md) |
| F175/F139 等 cover/query 方向 | 对最小额外信息、误差容限和查询代价提供候选结构 | **候选。** 原概率/oracle 前提不直接给出 DPT sensor-optimality 或 solver-budget 结论；见 [repair-cover 笔记](dpt_research/20261010_goal_tolerance_repair_cover.md) |

上述 ABC locator 对应各自 source ledger 中实际使用的 supplied version；不自动代表最新上游修订。每篇的 acquisition、版本与具体阅读深度继续归 [literature registry](literature/registry.json)。本次是实际用途同步，没有将全部旧文献标成二次全文精读；外部论文的撤回、修订和 selected Lean scope 仍需按实际承重版本核对。

## 3. Math 代码：已用的对象与尚未接通的实现

[工具入口与输入合同](dpt_tools/README.md) 给出完整 API。本次核对 A/B/C source ledger、吸收记录和本地接口，**未确认以下 Math 仓库模块被直接 import 并在真实 DPT 输入上完成 replay**。已确认的是本地等价对象的使用；两者分开记录。

| Math 实现 | 本地已经用了什么、效果如何 | 代码利用状态与最小下一输入 |
| --- | --- | --- |
| [predictive_state_audit](dpt_tools/predictive_state_audit.py)、[measurement_factor_audit](dpt_tools/measurement_factor_audit.py) | source-derived K/Q、$`DG=B\,DO+A\,DQ+E`$ 与信息余项；S09 局部修复、A 的 exact fiber、C 的非线性 chart 均有实际后果 | **本地构造已用；仓库模块直接重放未确认。** 可用同域 DO/DQ/DG、单位缩放及可信二阶常数对照；旧 bound 修订已要求保留 O 的余项 |
| [goal_ambiguity_audit](dpt_tools/goal_ambiguity_audit.py)、[goal_repair_cover](dpt_tools/goal_repair_cover.py) | A 实际信息下界；B 有限 F4 下界；Cal 已检查 C 合法测量子盒相交 | **独立实际实现已用；cover 的 DPT 最优采集结论未形成。** 输入应为合法 nuisance 集合，带单位、共同误差相关性、goal 求值误差及采集成本 |
| [goal_lipschitz_stability](dpt_tools/goal_lipschitz_stability.py) | B 已有重新 shooting 的 current/next 与 future-goal 见证；C 有有限近等观测成员 | **可直接接入的候选，尚无实际 replay。** 计算有限 bank 的 gain–error 曲线及 transition-pair 必要误差下界；有限类成功不能晋升连续动态闭合 |
| [implicit_goal_certificate](dpt_tools/implicit_goal_certificate.py)、[goal_defect_transport](dpt_tools/goal_defect_transport.py) | A/S10 的 actual-law residual、Jacobian/adjoint 与 signed goal correction；同网格 Full/N2 比较区分内部求解差与 native discrepancy | **本地 source 功能已用；仓库模块直接重放未确认。** 需要实际 inverse/remainder 常数，或声明的线性 chart；修正内部 source 误差不保证改善 native 目标 |
| [fiber_curvature_audit](dpt_tools/fiber_curvature_audit.py)、[stage_box_reachability](dpt_tools/stage_box_reachability.py) | A 用联合平方系统证书；B 实际重新 shooting；C 当前攻相关 active fork/tube | **实际问题已落地；工具需要真实连续域 bound。** 独立盒过松时应保留跨步相关性；INCONCLUSIVE 不等于 law 失败 |
| [goal_word_quotient](dpt_tools/goal_word_quotient.py)、[command_word_audit](dpt_tools/command_word_audit.py) | B 已按合法 BE update、阶段输出与目标定义动态反例；Pro17/S09 已运行 ordered commands | **语义已用；linear all-word theorem 尚未绑定 nonlinear actual law。** 先交付同 reference 的 goal-relevant transition/future pairs，不把坐标失败直接当目标失败 |
| [mixed_interaction_audit](dpt_tools/mixed_interaction_audit.py)、domain/definedness 工具 | B+C 联合 history/L/κ/sensor 正在建设；真实 law 的 branch/guard 在本地检查 | **定向候选。** joint interaction 需合法参数矩形及实际统一余项；expression inventory 只检查表达式身份，不证明物理可达性 |

本地可复用实现归 canonical source evaluator、已有 acceptance consumer 与 derivations，不复制一整套 Math engine。仓库 synthetic tests 只证明工具自己的合同；本次没有将它们计作 DPT 实验或重新运行全部工具测试。

### 三条共用计算关系

1. **合法观测相容对给下界。** 在声明误差集合内，两条可达历史允许同一观测，则仅使用该信息的 scalar-goal 预测器最坏误差至少为目标间隔的一半。source 目标存在求值误差时，要先扣除两端的误差上界。有限 bank 见证给整个类的下界，不给整个类的上界。
2. **有限域修复给上界。** 固定中心和系数，令 $`f=g-BO-AQ`$。若合法半径内确有 $`\|D^2f\|\le M`$，则
```math
\begin{aligned}
|\Delta g-B\Delta O-A\Delta Q|
&\le\|E\|r+\tfrac12Mr^2\\
&\quad+\|B\|\varepsilon_{\Delta O}
+\|A\|\varepsilon_{\Delta Q}\\
&\quad+\eta_{\rm evaluation}.
\end{aligned}
```
   关键建设对象是合法域、统一 M、初态/事件传播和摘要取得方式，不是 Taylor 公式本身。
3. **目标投影决定求解精度的价值。** 同一离散 law、正号伴随约定下，
```math
G(X^\star)-G(\widehat X)\approx-\sum_n\lambda_n^\top R_n(\widehat X).
```
   要形成保证，还需非线性余项与可解性界；moving peak/event 要有相应 guard/readout 资格。solver/grid/source-native 的 signed chain 是计算路径分解，不能自动解释成独立物理原因。

## 4. 下一轮 side 最值得攻什么？

### A. Active 联合有限域目标证书

**已有输入：** A 的联合相关证书、C 的 actual residual/Jacobian、126-step preparation、同初态 CAL / target 两分支，以及真实 remainder 见证。

**要建设的对象：** 在一个非零合法 preparation/parameter/sensor 邻域中，把 initial-state propagation、active branch、隐式可解性、关联 remainder 和目标投影接到统一 bound。允许更小作用域、分阶段证书或新的 block/functional 表示；优先避免独立误差盒抹掉共同初态与测量锚点的相关性。

**合格出口：** 可复算的合法域与统一常数，得到某个具名目标的修复后上界，或一个明确反例和低复杂度合法修复。当前浮点场计算、有限样本最大余项或 q 诊断不足以完成连续证书。F266 的证书组织、F357 的方向组合、F374 的目标 functional 是最直接的已有入口。

### B. Goal-relevant dynamic closure 与最小修复

**已有输入：** B 的主动两阶段历史对、未见成员评分、细化后重新 shooting、阶段 work 相消和 peak/event 差；C 的 CAL 与不可见 κ 方向。

**要建设的对象：** 在同一 reference 中同时比较 coordinate-update defect 和 future-goal defect，测试 recorded-command、past voltage、主动 CAL、有限 memory 与 observation-updated state。history 信息是否能替代 CAL、本构校准是否能弥补 history 缺口，均允许被普通方案或反例推翻。

**合格出口：** 一条完整的合法 obstruction→最小可取得 repair→目标误差资格→冻结 holdout/falsifier 链，或有界域内的 positive sufficiency。不能把尚未评分的预测称为成功，也不能由重拟合生成“新预测”。F229/F376 提供信息与更新语义；gain/transition 工具应优先消费已有实际 pair。

### C. 原始 R1 与外部测量桥：数学和物理接口分工

100 V R1 的外切口、L/Rser/gain 相容集合，150 V 的 history/κ 主动 chart，600 V 的 native work/peak，是三套具名系统。它们可以共享方法，尚不能拼接成同一个严格物理结论。

Math side 可帮助求出观测 fiber 上的可恢复组合、未来目标范围、最小新增测量和带 nuisance 的界。真正缺失的同步 cut voltage、传感器资格、合法 own-preparation 或独立 model discrepancy，需要 DPT 数据/物理证据；滤波算法不能生成旧观测没有的信息。

优先成果是一个可复算的 compatible-set / goal-range 改善，而非默认恢复五个寄生参数。实际用途容差未知时，保留数学正例，并输出随容差的条件范围。

## 5. 专题推导与接手定位

这些笔记保留完整理论展开；本页只同步已经发生的用途和下一决定性缺口：

- [信息 × 求解精度](dpt_research/20261010_goal_information_solver_fidelity.md)：goal quotient、隐式目标误差与强固定策略。
- [ordered goal-defect transport](dpt_research/20261010_ordered_goal_defect_transport.md)：阶段顺序、backward goal rows 与误差支持。
- [nonlinear fiber / stage tube](dpt_research/20261010_nonlinear_fiber_and_stage_tube.md)：二阶 fiber 与条件可达域。
- [repair-cover 与目标容差](dpt_research/20261010_goal_tolerance_repair_cover.md)：信息代价、有限覆盖与源定理前提。
- [goal stability / compositional closure](dpt_research/20261010_goal_stability_compositional_closure.md)：有限 gain 曲线、更新闭合与目标稳定性的区别。

DPT 本地复算 locator（以下路径属于 DPT 工作区，不是本 Math 仓库文件）：

| 内容 | 实际入口 |
| --- | --- |
| ABC 科学接受与范围 | pro_runs/20261010_pro18_goal_adequacy_frontier/absorption.md |
| A/B 论文使用与 source 身份 | artifacts/run_A/pro18a_source_ledger.csv、artifacts/run_B/pro18b_source_ledger.csv（上述 family 内） |
| C 精简 reader、ledger 与原始字节 | artifacts/run_C/README.md、artifacts/run_C/pro18c_submission/、artifacts/run_C/original_submission.zip |
| C 实际 acceptance consumer | analysis/acceptance/pro18c_review.py 及配套结果（上述 family 内）；完整 replay 的 archive 适配沿既有入口 |
| 逐步推导 / 实际 law | docs/derivations/README.md、canonical TeX、已有 commutation_balance.py |
| Cal 科学判读 | simulation/source_evaluator.py、simulation/README.md；comparison identity、bounded nuisance、signed-error chain、filtered flux 与用途区间 |

维护时只更新有材料性改变的行：新定理/反例、实际输入上的工具 replay、被兑现的 falsifier、修复后的误差范围，或决定下一项证据的卡点。读过、用于构造、通过复算、进入 native 判别分别登记；不以 PDF 数量、代码量或思考时长衡量吸收程度。


## 6. 2026-10-11：F119/F129/F132 原始证明深读与反例（持续更新）

**证据身份：** 下面是固定 OpenAI Math 版本 `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` 的原始 LaTeX 定理、核心引理、证明结构和原稿 TikZ 图审阅，加上独立合成有限枚举；不代表 Lean 全文验证、真实 DPT 输入重放或硬件测量。此条记录与尚未合并的 [连续 goal-information PR #4](https://github.com/Gogoal-L/math/pull/4) 分开维护。

**F132 的真正承重结构。** [nested predicates 与 tournament labels](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/01-construction.tex) 给出合法组合敏感块；[Prop. recurrences](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/02-recurrences.tex) 同时递推单 predicate 的正/负敏感度 S 与两个嵌套 predicate 同时翻转的 J。随机 edge labels 限制一次修复一个 target 的候选行少于 t=16，tournament 内 gate-only 候选至多 3，不能省略 J；[final counting](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/03-separation.tex) 将块增长 M²(2M²+1)^d 与 s(f)≤2(d+2)M^(d+1) 相比，d=9 可用 composition 放大。**DPT 增量不是 Boolean 指数，而是定向检验成组 intervention 与 stage/goal guard 的联合敏感性。** 合成 d=1,M=3 witness 在零输入 342 个 bit 的所有 one-bit flips 均无效，57 个互不相交的 6-bit 组各能触发响应；这个小 M 并未验证论文全局 label/sensitivity upper bound。论文 d=9 且 M≥9^10 的明确种子规模至少有 **238 位十进制位**，不能声称可直接部署为 DPT 测量方案。

**F129 的真正承重结构。** [context-separation lemma](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/build/sections/separation.tex) 用左右合法的 singleton identity relation 把矩阵任意一个 (i,j) entry 变成可测 nonzero-product 判据；[matching-corner lemma](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/build/sections/matching.tex) 保持 rank/support 并以 minimal-rank idempotent 提升 permutation lifts；[rank-loss proof/figure](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/build/sections/rank.tex) 以 32 conjugates 制造 256 additions，单一 common support budget 64c，缩减关系点数 31，再递推指数 bound。**必须有完整 relation alphabet、任意上下文与该精确 matching monoid 表示**；无法从 DPT 有限合法 command 直接推出指数状态下界。对全部 16 个两状态 relation 的 256 对，合成程序验证了论文使用的双侧 singleton 上下文可分离性。DPT 可迁移任务是只在合法 preparation/command library 内验证 near-aliased histories 的未来区分 word；已有 command_word_audit 是第一优先实现，不应复制通用 automata engine。

**F119 的真正承重结构及改变结论的反例。** [main theorem](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/main.tex) 设均匀独立输入与 **independent binary symmetric noise**，将信息损失写作 entropy semigroup 产生率；[three-point optimizer](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/sections/canonical.tex) 包含内部核心 (x,y) 与至多两共同角点；[reserve](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/sections/reserve.tex) 将 total entropy 预算作为 convex perspective 来分配；[thinning](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/sections/thinning.tex) 控制共同输出混合并接上正的 curvature margin；[upgrade/flow](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/sections/upgrade.tex) 用 max profile 与维数归纳，再积分得到 sharp contraction。注意其成本优化允许**中间随机对之间的相关性**；不可混淆为通道噪声不必独立。

自建的精确两比特负控：X1,X2 为独立公平 signs，Y_i=X_i Z_i。**独立** Z_i 且 E Z_i=ρ 时，coordinate 的 retained MI 为 ψ(ρ)，parity 为 ψ(ρ²)；**完全共享** Z1=Z2=Z 时，Y1Y2=X1X2，parity 信息保持 **1 bit**。ρ=0.3 的枚举结果为独立：0.0659319446 vs 0.0058508285 bits，共享：0.0659319446 vs 1 bit。此结论直接击穿“F119 的 coordinate optimality 不依赖噪声相关结构”的过强迁移，**不反驳 F119 原定理**。DPT 应优先测试可测的 nuisance-invariant paired contrast 与共同误差合法域；不是宣称 parity 对模拟波形最优，也不是混用 MI bits 与 goal nJ 的评价。

**GitHub Actions 最新实测（2026-10-12）。** 已采用 `python -m unittest discover -v -p 'test_*.py'` 执行完整自动发现的回归套件；本轮主分支 [run 38180573299](https://github.com/Gogoal-L/math/actions/runs/38180573299) 实际报告 **153 tests / OK**，涵盖 F119/F129/F132 有限反例、连续目标信息半径、rank-deficient sensor noise、finite future words 和 mixed-nuisance prediction；新增加的极小噪声数值稳定性和严格容差测试均在其中。这里的通过只意味着声明的合成工具合同，不能替代 native DPT/实验硬件验证。

**F119 引发的程序修复（已在 main）。** [goal_ellipsoid_recovery](dpt_tools/goal_ellipsoid_recovery.py) 现接受 E∈R^{m×p} 任意 rank；[推导](dpt_research/20261011_continuous_goal_information_bridge.md) 区分无噪声 readout、相关 bounded noise、证据边界。主分支另有 [contextual_goal_recovery](dpt_tools/contextual_goal_recovery.py) 将无限共享 nuisance 与有限指令集目标半径统一到式 (M13–M17)。极小 E 的 SVD 浮点泄漏曾令最优 decoder 上界虚增，现增加独立最小二乘/零基线候选、可行 witness 检查，并移除了随意的 1e-9 全局容差宽限。**数学零半径只有在 physical noise rank、误差地板、端口及时间关联都已证实时才是物理结论。** 原 draft [PR #4](https://github.com/Gogoal-L/math/pull/4) 的已验证实现按文件纳入 main 后已关闭，所属临时分支已清理；无需保留长期 feature branch。

**OpenAI Math 自身 Lean 定理层的进一步核对（2026-10-11）。** 三篇均有官方 [F119](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/119.md)、[F129](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/129.md)、[F132](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/132.md) formalized-scope 页面和真正的证明源码，而不仅有论文声称。[F119 SoftChannel.Main](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/InformationTheory/SoftChannel/Main.lean) 从 SoftInformation 及 CourtadeKumar 的底层证明推出 contraction、attainment、偏置 refinement 与 selected production；[F129 Automata.Main](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Combinatorics/Automata/Main.lean) 拼接 small_nfa 与 deterministic_lower_bound；[F132 Sensitivity.Separation](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Combinatorics/Sensitivity/Separation.lean) 给出 quantitative、unbounded quadratic、fixed-power 三个结论。**关键版本/检查边界：** `lean/ComparatorChallenges/*.lean` 的相应题目含有 `sorry`，它们是 comparator statement placeholders；不能误读为实际 proof 文件的缺口。已实读上述 *证明主入口* 与官方 statement scope，但**尚未重新以 Lean/lake 完整构建整个依赖闭包**，也未完成 source Lean→纸本全部技术引理的一一审计，因此只登记“上游有对应形式化源码和声明”，不是本地新通过的机器证明。即便原 theorem 经 Lean 正式核证，也不保证其不同模型前提的 DPT transfer。



**新的三篇交叉联合结果：future-word goal / shared-nuisance quotient（2026-10-11）。** [代码](dpt_tools/contextual_goal_quotient.py)、[单测](dpt_tools/test_contextual_goal_quotient.py)已进入 main，[CI run 38178960392](https://github.com/Gogoal-L/math/actions/runs/38178960392) 实测 **129 tests / OK**（上面 124 加 5 项有限 word/观测/校准 rank tests）。声明共同的**线性初态 chart**和有限命令集 $`\mathcal W`$：按物理顺序定义 $`F_w=A_{w_\ell}\cdots A_{w_1}`$，允许预测前观测 $`y=Hx+N\eta`$，其中 $`\eta`$ 是**不受界限制的共享 nuisance**。令 $`U_0`$ 张成 $`\ker N^\top`$，现有不受 nuisance 影响的观测行空间 $`R=\operatorname{row}(U_0^\top H)`$；将具名未来目标 $`C F_w`$ 的行按 $`\mathcal W`$ 堆成 $`G_{\mathcal W}`$。在可任意增加**理想无 nuisance 的线性状态标量观测**的特殊信息库中，恰好需要
```math
k_{\min}^{\rm ideal}=\operatorname{rank}\begin{pmatrix}R\\G_{\mathcal W}\end{pmatrix}-\operatorname{rank}(R)
```
个额外独立行，才能一次覆盖所有**指定**未来命令的线性目标。证明由 nuisance 可抵消的观测相容方向 $`\{\delta x:H\delta x\in\mathrm{im}N\}=\ker(U_0^\top H)`$ 与 row/null 正交补及 quotient dimension 直接给出。**这是有限线性代数结论，不是 F119/F129 原定理或 nonlinear SiC 最小状态/传感器数定理。** 两态例：$`H=I_2,N=(1,1)^\top,C=(1,-1),A=\mathrm{diag}(1,-1)`$。当前目标完全可恢复，但未来命令 A 后目标成为 (1,1)，出现一个维度的信息缺口；合法预测前 CAL 额外测量 $`\eta`$ 则填补缺口。在额外理想噪声自由源状态观测的抽象库下 $`k_{\min}=1`$，但实际 CAL 可以改变 nuisance knowledge，二者信息成本不同。160 组独立 integer-rational SymPy oracle 与 SVD 诊断吻合；物理状态合法域、有限 noisy sensor、nonlinear remainder 与 held-out scoring **仍待本地主控消费实际 18B/C 数据**。见 [F119/F129/F132 原文 proof-level 研究](dpt_research/20261011_F119_F129_F132_proof_level_DPT_bridge.md)。

这一新增通道让 F132（合法联合干预）、F129（future context distinguishability）、F119（共享误差结构）首次落实为可执行的同一个**目标相关信息缺口测试**；已有的 [goal_word_quotient](dpt_tools/goal_word_quotient.py) 计算的是给定线性更新与 goal 下的自主状态维数，本工具仅计算给定有限 word 与 shared nuisance 的**预测前目标测量充分性**；二者不可混淆。工况完全未知时，不应用 k_min 推断 physical hardware minimum。
