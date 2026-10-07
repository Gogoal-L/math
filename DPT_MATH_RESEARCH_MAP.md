# DPT-R1 × OpenAI Math 研究利用图谱

**用途**：这是一份长期维护的研究台账，用来记录 Gogoal-L/math 中哪些数学工作真正进入了 DPT-R1 / Pro17D，进入的位置是什么，契合度有多高，以及它们会怎样改变我们的科学对象、证明方式、实验设计和证据标准。

**基线版本**：adc7f1241b42e322a6451854ab7e4b4c146bf78a  
**首次系统整理**：2026-10-07

这份文件不把 OpenAI Math 当成可以直接搬结论的定理库。仓库中的论文更适合承担三类作用：

1. 给出已经成熟的数学对象和证明结构，帮助我们把 DPT 中模糊的直觉变成可定义、可证伪的问题；
2. 提供反例和适用边界，防止把 reduced-law 中成立的结果扩大到 native SPICE 或真实器件；
3. 提高 computation-backed result 的证据标准，让数值结果更接近一个可以审计的数学论证。

仓库原始入口仍保留在 [README](README.md)、[CONTENTS](CONTENTS.md)、[overview](overview.pdf) 和 [Lean formalization catalogue](lean/formalization.yaml)。

---

## 1. 这份图谱怎么判断契合度

这里的契合不看论文有多难，也不看结论有多漂亮。真正重要的是它能不能改变 DPT 当前已经存在的一个具体研究对象。

我用四个问题判断一篇工作的价值：

| 维度 | 判断问题 |
|---|---|
| 对象契合 | 它研究的数学对象，能否对应 DPT 中已经存在的 state、observation、goal、command、interaction 或 inverse problem？ |
| 证明契合 | 它的证明结构能否在 DPT 中重新推导，而不是只做类比？ |
| 证据契合 | 它要求的数据、measurement 或 computation，DPT 是否有机会在 S09/S10 或现有仿真框架内得到？ |
| 改变量 | 用了以后，能否改变 theorem、acquisition、certificate 或 claim ceiling，而不只是让文字更漂亮？ |

因此下面的等级表示“对 DPT 当前路线的贡献”，不是对数学工作的质量排名。

| 等级 | 含义 |
|---|---|
| **S+** | 已经可以改变 DPT 的数学对象或下一次关键 acquisition，值得优先继续推导 |
| **S** | 很强的直接迁移对象，需要一轮 DPT-specific derivation |
| **A** | 能明显提高证据标准或打开下一层问题，但暂时不是 S09 的主判据 |
| **B** | 主要用于 claim discipline、未来 native extension 或局部工具 |
| **C** | 有启发，但暂时不应占用当前有限的仿真和推导预算 |

### 阅读深度标记

| 标记 | 含义 |
|---|---|
| **D3** | 已读与 DPT 相关的正文 source、关键假设和 proof mechanism |
| **D2** | 已读 scope / introduction / 决定性章节，足以判断能不能迁移 |
| **D1** | 已完成 family-level 筛选，暂时保留在候选池 |

仓库中的 PDF 是正式渲染稿。本轮环境没有稳定完成所有 binary PDF 的逐页视觉检查，因此这份图谱主要依据论文对应的完整 TeX/source、Lean scope 和正文结构。涉及图形或版面本身的证据时，仍需单独补 visual PDF pass。

---

## 2. 目前最值得统一的 DPT 科学对象

Pro17D 现在已经出现了一个比“拟合 waveform”更清楚的方向：

> 给定未来 command 和预测目标，寻找 switching history 中最小、可更新、足以支持这些目标的有限 predictive representation。

记：

- H：允许的 preparation / history 集合；
- C：未来 command 集合；
- O: H -> Y：当前可获得的 observation；
- G_c: H -> R^p：施加未来 command c 后关心的 goal。

定义：

h1 ~_G h2，当且仅当对所有 c in C，都有 G_c(h1) = G_c(h2)。

这样以后讨论“需要多少 state”时，不再问完整内部状态能不能重建，而是问：

> 为了当前声明的 future goals，哪些 history 差异必须保留，哪些可以安全压掉？

这个对象已经和现有 reduced-law 结果发生了实际连接：

- 对 increment / zero-sum 类目标，当前一维 gate coordinate 已经表现出 exact sufficiency；
- 对 absolute drain 类目标，同一个 coordinate 不够，需要额外 drain / charge anchor；
- full-native vendor model 上是否仍存在类似有限 quotient，目前没有被证明。

这也是下面各个 OpenAI Math family 的统一入口。

---

## 3. 当前优先级总表

| 优先级 | Family | 契合度判断 | 最直接的 DPT 用法 | 如果做成，最可能带来的改变 |
|---|---|---|---|---|
| **S+** | **F140 Memory-sample lower bounds** | 很高 | 从 goal space 构造 information lower bound | 把“我们找到了一个小 state”推进到“任何更小 state 都不够” |
| **S+** | **F355 Tangent-flow uniqueness** | 很高 | 从 observation kernel 推导最少缺几维 measurement | 把 P2 从经验性 sensor proposal 变成最小测量定理 |
| **S** | **F116 Noncommutative identity testing** | 高 | 建立 ordered command / mixed interaction 的 word representation | 让 S09/S10 的 acquisition 对应“购买哪个缺失 functional” |
| **S** | **F365 + F372 inverse uniqueness** | 高 | 明确 model class、observation、goal、symmetry 下的 identifiability | 避免 reduced-law uniqueness 被误写成 full-native identifiability |
| **A** | **F266 certified computation** | 高 | 建立 algebraic / numerical / provenance / native 四层 certificate | 数值 coherence 可以升级成可审计 computation-backed claim |
| **A** | **F251 Strong Ulam stability** | 中高 | 定义 native command composition defect | 为“近似 command algebra 能否靠近 exact algebra”提供长期问题 |
| **B** | **F139 Query complexity** | 中 | 把一次 fresh simulation 当成有成本的 information query | 以后可以比较不同 characterization plan 的 query efficiency |
| **B** | **F289 Kadison-Kastler stability** | 中 | 约束“两个 representation 很接近”到底要用什么 metric | 避免用单侧 waveform fit 推 structural stability |
| **B** | **F325 Complete Crouzeix** | 中低 | 未来 nonnormal reduced propagator 的函数界 | 只有 representation 变复杂后才值得启用 |
| **C** | F357 / F374 / F098 / F119 / F229 | 低到中 | 边界、反例、稳定性和 reconstruction 类比 | 暂时用于审查，不进入主线证明 |

当前真正值得投入推导时间的是 **F140 + F355 + F116**。它们分别回答三个连续问题：

1. 至少需要多少 predictive information；
2. 当前 observation 到底缺了几维 goal-relevant information；
3. 下一次 command / mixed query 应该去测哪个尚未确定的 functional。

这三件事连起来后，DPT 的 S09/S10 就不再只是“多跑几个 case”，而会成为一个受数学结构约束的 bounded acquisition programme。

---

## 4. F140：Memory-sample lower bounds

### 已读材料

- [Lean scope](lean/docs/140.md)
- [Replacing Gaussian observations](preprints/Replacing-Gaussian-observations-in-memory-constrained-inference-September-27-2026/paper.pdf)
- [Introduction source](preprints/Replacing-Gaussian-observations-in-memory-constrained-inference-September-27-2026/build/sections/00-introduction.tex)
- [Finite Gaussian-fiber comparison](preprints/Replacing-Gaussian-observations-in-memory-constrained-inference-September-27-2026/build/sections/06-fiber.tex)

### 论文中真正可借用的部分

F140 研究的是 exact Gaussian observations 和 finite persistent state。它关心一个有限 memory learner 在保留有限信息以后，还剩多少与真实 signal 有关的信息，以及真实 observation rows 和 fresh rows 之间如何比较。

Gaussian regression 本身和 DPT 差得很远，不能直接套 theorem。真正契合 DPT 的地方是它把四件事明确分开：

- 原始 observation history；
- 被压缩后保留下来的 finite state；
- observation 之后仍然无法区分的 fiber；
- 为了完成目标任务，这个 fiber 上还必须保留多少信息。

这恰好对应我们现在的 predictive quotient。

### DPT 中可以怎么重写

定义 goal pseudometric：

d_G(h1,h2) = sup over c in C of ||G_c(h1)-G_c(h2)||。

如果一个 M bit representation 要对所有 future command 保证不超过 epsilon 的误差，那么任何在 d_G 下两两距离大于 2 epsilon 的 history 都必须被编码成不同状态。

因此自然得到一个候选 lower bound：

M >= log2 P(H, d_G, 2 epsilon)

其中 P 是对应 packing number。

这条式子本身是简单 counting argument，不是 F140 的 theorem。F140 的作用在于告诉我们：对有限 predictive state，真正该控制的是 observation 后的 goal-relevant information，而不是完整 physical state dimension。

### 契合度为什么高

DPT 当前已经有 representation 的上界结构：我们找到了一个很小的 coordinate，可以在某些 reduced-law goal class 中工作。

缺的正好是另一半：

> 有没有可能再压？如果不可能，最少为什么需要这么多信息？

F140 正好推动这个问题。

### 用了以后会具体改变什么

第一，论文中的“低维 representation”会从一个构造性结果升级成上下界问题。

目前最容易说的是：

> 这个一维 coordinate 足够。

如果 information lower bound 能建立，论述可以变成：

> 这个 coordinate 足够，而且在声明的误差和 command class 下，低于某个 information budget 的 representation 不可能统一完成目标。

第二，它会改变 S09/S10 的选点标准。一个 query 的价值不再只看 forecast spread，而可以问：

> 这个 query 能不能把当前同一 predictive code 里的 goal-distinct histories 分开？

第三，它可能给“minimum measurement”提供 information-theoretic 版本，与 F355 的 local dimension bound 形成互补。

### 目前不能从 F140 得到什么

- 不能从 Gaussian regression theorem 推出 DPT native lower bound；
- 不能由 memory bits 自动推出 sensor 个数；
- 不能跳过 DPT 自己的 history class 和 goal pseudometric 定义；
- 如果 native history space 没有明确的 admissible class，packing bound 也没有科学意义。

### 下一步

最小可做版本是先只处理 reduced law：

1. 固定当前真正声明的 future command set；
2. 固定一个 scalar terminal goal；
3. 构造一组 goal-separated histories；
4. 先给出 deterministic finite-code lower bound；
5. 再判断 noisy / randomized 版本是否值得进入论文。

**预期提升**：如果成功，这会是从“漂亮的 reduced representation”到“有 representation complexity 内容的研究对象”的实质提升。

---

## 5. F355：Tangent-flow uniqueness 与最小额外测量

### 已读材料

- [Tangent-flow manuscript](preprints/Tangent-flow-uniqueness-2026-09-24/paper.pdf)
- [Normalized family / compact observations](preprints/Tangent-flow-uniqueness-2026-09-24/build/sections/linear.tex)
- [Finite-jet obstruction](preprints/Tangent-flow-uniqueness-2026-09-24/build/sections/finite-jet.tex)

### 对 DPT 最有价值的证明结构

linear.tex 里的 Symmetric enlargement 从一个有 finite-dimensional kernel 的线性化 operator L 出发，选择有限 observation，使这些 observation 对 kernel 的作用足以消掉不可见方向。随后 augmented operator 变成可逆。

对 DPT 来说，最值得保留的是这个结构：

> 先找当前 measurement 看不见的方向，再判断其中哪些方向会影响目标，最后只补足那些 goal-visible 的不可见方向。

这和我们当前 drain-translation 现象非常接近。

### DPT 中的候选定义

在参考 history h* 处令：

K = ker(DO(h*))

即当前 observation 一阶看不见的方向。

再令：

N = K ∩ (intersection over c in C of ker(DG_c(h*)))

即 observation 看不见，同时对所有目标也无影响的方向。

于是定义：

r_G = dim(K/N)

这里的 r_G 可以叫 **goal-visible hidden dimension**。

它回答的是一个很具体的问题：

> 当前 measurement 丢掉的信息里，有多少维真的会影响我们声明的 future goals？

如果增加 k 个 scalar measurement P1,...,Pk，一阶 sufficiency 至少需要：

ker(DP restricted to K) ⊆ N

因此必然有：

k >= r_G

### 为什么它和现有 DPT 特别契合

现有 reduced-law 里已经出现一个几乎教科书式的例子。

drain translation 方向对 gate observation 是不可见的。

- 对 increment / zero-sum goal，这个方向同时也是 goal-null，因此它属于 N，无需额外测量；
- 对 absolute drain goal，这个方向会改变目标，因此它留在 K/N 中。此时 r_G = 1，一个独立 drain / charge anchor 正好补足这一维。

也就是说，我们现在的一维 repair 有机会从一个 isolated trick 变成一个 general theorem 的 worked example。

### 用了以后会具体改变什么

第一，P2 的问题会更清楚。

现在常见说法是：

> gate waveform 不够，所以再测 drain。

更强的版本是：

> gate observation 的 nullspace 中恰好有一维对 absolute goal 可见，因此任何 local sufficient repair 至少需要一个 independent scalar；某个 drain / charge anchor 达到了这个下界。

这两个说法的科学层级差很多。

第二，它可以成为 future sensor design 的统一标准。

以后不再按“哪个 sensor 看起来有信息”来挑，而是计算 candidate measurement 对 K/N 的 rank。

第三，它能和 F140 形成两个互补的 lower bound：

- F355 给 local geometric dimension；
- F140 给 global / finite-code information requirement。

### 风险和边界

这条路线依赖 local differentiability 和 rank 条件。native SPICE 的 effective history space 很可能比 reduced law 复杂，也可能存在 nonlinear folding，此时 tangent rank 只能证明局部结果。

所以它适合先在 reduced-law 上做严谨 theorem，再把 native 结果写成 numerical rank evidence，而不是直接宣布 global native sufficiency。

### 下一步

1. 把 K/N theorem 写成与 DPT 公式无关的有限维命题；
2. 在 reduced law 上完整证明；
3. 明确哪些 rank / regularity 条件让一阶 repair 升级成 local sufficiency；
4. native interface 可执行后，再计算实际 preparation family 的 DO 和 DG_c。

**预期提升**：这是目前最有希望把“需要什么 measurement”变成真正数学贡献的一条线。

---

## 6. F116：Noncommutative formula、ordered words 与 interaction acquisition

### 已读材料

- [Lean scope](lean/docs/116.md)
- [One Rational Matrix Hitting Point](preprints/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026.pdf)
- [Introduction / proof route](preprints/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026/build/introduction.tex)
- [Iterated-integral encoding](preprints/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026/build/iterated-integrals.tex)
- [Multiplicity estimate](preprints/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026/build/multiplicity.tex)

### 论文里和 DPT 最契合的部分

这个 family 的主结果是 noncommutative formula identity testing。对 DPT 来说，真正新鲜的部分是 ordered words 的 faithful encoding。

论文用 iterated integrals 把 word order 保留下来。即使两个表达式使用相同字母，AB 和 BA 仍然可以被区分。commutator 的非零性也说明了 cancellation 可能把第一次可见差异推迟到更高阶，但 order information 没有消失。

这和 DPT 的一个实际难点非常接近：

> aggregate pulse area 一样，并不保证 terminal response 一样；顺序、同时作用和 history 都可能产生不同 response。

### 对 DPT 更合适的表示

可以把 command response 按 word degree 分层：

- degree 0：prepared baseline；
- degree 1：primitive command A、B；
- degree 2：AA、BB、AB、BA；
- 更高阶：更长的 ordered words。

同时要把两类 interaction 分开：

1. simultaneous mixed functional，例如 quadratic response 里的 alpha beta C_AB；
2. sequential ordered interaction，例如 AB 与 BA 的差。

这两类现象都可以放进一个 command-word hierarchy，但数学上不能混为一谈。

### S09 为什么因此更有意义

现在 S09 fusion 可以写得更准确。

假设 declared quadratic class 是：

F(alpha,beta) = F0 + alpha L_A + beta L_B + alpha^2 D_A + beta^2 D_B + alpha beta C_AB

只测 primitive axes 时，C_AB 完全没有被确定。

因此 mixed query 的价值很明确：

> 它第一次直接测量 axis information 无法推出的 mixed functional。

这比“再加一个中间 amplitude 看看”更有 acquisition 意义。

### 用了以后会具体改变什么

第一，S09 和 optional S10 可以承担不同的数学角色。

- S09：测 simultaneous mixed interaction；
- S10：如果仍有预算，可以专门测 ordered AB vs BA，或者另一个未被 S09 消掉的 timing cross。

第二，现有 A3 / N4 / phase / fusion 结果可以放到一个分层表示里。这样不同发现不再像独立的小规律，而是 command expansion 的不同 coefficient。

第三，如果未来能证明某个有限 word truncation 对目标足够，就有机会得到一个真正 finite command representation。

### 需要特别防止的过度解释

ordered-word / iterated-integral 表示本身并不是 DPT 新发明。Chen-Fliess、nonlinear realization 等已有大量相关文献。

所以未来真正可能形成贡献的是：

- 这个表示在 power-semiconductor switching 的具体 scientific object；
- goal-dependent truncation / sufficiency；
- bounded acquisition；
- prospective falsification；
- 与 physical charge / parasitic state 的可解释连接。

不能把“用了 noncommutative words”本身写成 novelty。

### 下一步

1. 为 DPT 固定 primitive command alphabet；
2. 明确 simultaneous mixed 与 sequential ordered 两套 coefficient；
3. 把 S09 对应到一个明确缺失 coefficient；
4. 在 S09 后根据剩余 nullspace 决定 S10，而不是按最大 forecast spread 机械选点。

**预期提升**：它能把 experiment design 从“选有差异的 case”推进到“有目的地识别 representation 中还未知的 coefficient”。

---

## 7. F365 + F372：inverse problem 给 identifiability 的边界

### 已读材料

- [F365 Lean scope](lean/docs/365.md)
- [Joint metric/connection recovery](preprints/Determination-of-a-metric-and-a-unitary-connection-from-one-boundary-patch-October-5-2026/paper.pdf)
- [Joint recovery introduction](preprints/Determination-of-a-metric-and-a-unitary-connection-from-one-boundary-patch-October-5-2026/build/sections/01-introduction.tex)
- [F372 Lean scope](lean/docs/372.md)
- [Smooth isotropic elasticity](preprints/Global-Uniqueness-for-the-Smooth-Isotropic-Elasticity-Inverse-Problem-September-24-2026/article.pdf)
- [Coefficient recovery](preprints/Global-Uniqueness-for-the-Smooth-Isotropic-Elasticity-Inverse-Problem-September-24-2026/build/sections/coefficient-recovery.tex)

### 为什么这组论文和 DPT 有用

这组 inverse-problem 工作最值得学习的是 claim discipline。

同样是 inverse problem：

- 在足够光滑、结构明确的 class 中，可以有很强的 uniqueness；
- class 一放宽，nonuniqueness 可能立刻出现；
- 某些 uniqueness 只在 gauge / diffeomorphism equivalence 下成立；
- F372 使用的是 full boundary operator，结论也不是一个有限测量 reconstruction algorithm。

这对 DPT 非常直接。

以后讨论 identifiability 时，至少要同时写出：

identifiability = (model class, observation operator, goal, allowed symmetry)

### 对当前项目的具体改变

我们应该长期保留这三个区分：

uniqueness != finite sufficiency != stable reconstruction

例如：

- reduced law 中一个 coordinate 足够，并不推出 native SPICE 也有同一个 quotient；
- full waveform operator 可以唯一决定某个 parameter，也不代表有限几个 DPT case 足够；
- 局部 injective 也不代表 reconstruction condition number 好。

### 契合度

它对 S09 的直接选点帮助不如 F140/F355/F116，但对论文 claim ceiling 非常重要，所以仍然是 S 级。

它主要改变“我们允许自己说到哪里”。

### 用了以后会具体改变什么

以后每个 identifiability claim 都应该带 class qualifier。

例如不再写：

> drain state is identifiable from gate response.

而应写成类似：

> 在声明的 reduced law、command family 和 goal class 内，某 coordinate 对指定 goal 是 sufficient；扩大到 nonlinear charge surface、thermal state、diode state 或额外 parasitic mode 后需要重新判断。

这种写法不会削弱结果，反而能把结果的数学对象说清楚。

**预期提升**：减少 claim drift，也方便把“为什么 native 还需要一层验证”写成科学结构，而不是防御性 disclaimer。

---

## 8. F266：把数值结果升级成 certificate

### 已读材料

- [Lean scope](lean/docs/266.md)
- [Exact Fourier certificates](preprints/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026.pdf)
- [Exact verification section](preprints/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026/build/sections/05-verification.tex)
- [Maximum MUB execution contract](preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/build/sections/execution.tex)

### 最值得移植的是证据结构

F266 对 DPT 很契合，因为我们大量依赖 LTspice、root solving、numerical scoring 和有限 simulation budget。

这类工作最容易出现的问题是：

> 数值上非常漂亮，但无法回答“它到底证明了哪一层东西”。

F266 把几个证据层拆得很清楚：

- candidate generation 可以用数值或 modular elimination；
- 真正 certificate 需要单独 exact check；
- execution provenance 要记录 source、binary、hash、platform、arithmetic assumptions；
- 资源上限不能被偷偷当成 negative certificate；
- computation 执行正确和数学 lemma 正确是两件不同的事。

### DPT 可以直接采用的四层 certificate

#### C1：exact algebraic certificate

适合：

- rank / determinant；
- command composition identity；
- finite elimination；
- symbolic coefficient relation。

#### C2：one-sided numerical certificate

适合：

- root enclosure；
- domain / saturation margin；
- monotonicity；
- denominator separation；
- 可证明的 remainder envelope。

#### C3：simulator provenance

至少记录：

- vendor model/library hash；
- LTspice version；
- netlist/configuration hash；
- run command；
- waveform / CSV hash；
- scorer version；
- outcome 后没有修改 parameter。

#### C4：native / empirical validation

包括：

- fresh prospective outcome；
- convergence / refinement；
- 后续若有 hardware，再作为单独证据层。

### 用了以后会具体改变什么

最直接的变化是，我们以后不再把 machine precision match 当成自动等价于 scientific proof，而是可以明确写：

> 哪个部分是 exact identity，哪个部分是 numerical enclosure，哪个部分只是一次 simulator observation。

这对 S03-S09 这种越来越数学化的项目很重要。

另一个实际变化是，当 Pro run 找到很强的新 algebraic relation 时，后续 Codex 任务应该优先问：

> 能不能把它变成独立 certificate？

而不只是继续画更多 residual plots。

### 契合度

方法契合非常高，但它主要提高已有 claim 的可信度，不直接创造新的 physical law，所以放 A 级更合适。

**预期提升**：让 DPT 的强数值结果具备更清楚的可复核性，也降低 reviewer 把它当成 simulator-specific coincidence 的空间。

---

## 9. F251：Strong Ulam stability 与 approximate command algebra

### 已读材料

- [Strong Ulam Stability](preprints/Strong-Ulam-Stability-Characterizes-Amenability-October-5-2026/strong-ulam-stability.pdf)
- [Source](preprints/Strong-Ulam-Stability-Characterizes-Amenability-October-5-2026/build/strong-ulam-stability.tex)

论文研究 unitary almost representation：

def(mu) = sup ||mu(gh) - mu(g)mu(h)||

并讨论什么时候 small defect 意味着它靠近真正 representation。

### 和 DPT 的契合点

DPT reduced law 中可能存在 exact command composition，但 native SPICE / hardware 上更现实的情况是近似 closure。

因此可以定义 native composition defect：

delta_comp = sup ||R_hat(c2 o c1) - R_hat(c2) R_hat(c1)||

然后问：

> 如果 delta_comp 很小，什么时候能推出存在一个真正 finite reusable command representation，且它与 native response 足够接近？

这个问题很有价值，因为它连接 exact reduced mathematics 和 native deployment。

### 为什么现在还不能作为主线

F251 的 theorem 是 group + unitary representation。DPT command 通常：

- 不可逆；
- 非 unitary；
- 更接近 semigroup；
- 可能有 saturation / dissipation；
- metric 也未定义。

所以当前只能借问题形式和 stability philosophy，不能借 theorem。

### 用了以后可能带来的提升

如果未来真的建立 DPT-specific stability theorem，项目会从：

> reduced model 有一个 exact algebra

推进到：

> native dynamics 虽然不 exact，但在一个可量化 defect 下靠近某个 finite algebra。

这会明显提高 representation 的工程和科学意义。

当前阶段先记录，不占用 S09/S10 预算。

---

## 10. F139：query complexity 与 characterization budget

### 已读材料

- [PDF](preprints/Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026/article.pdf)
- [Main source](preprints/Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026/build/main.tex)
- [Introduction](preprints/Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026/build/sections/introduction.tex)
- [Lower bound](preprints/Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026/build/sections/lower.tex)

这篇工作的核心方法论是把 information acquisition 明确定义成 oracle query，同时允许 query 之间做任意 computation。

### DPT 的对应物

可以把：

- fresh LTspice run；
- hardware measurement；
- 新 operating point；
- 新 command sequence；

统一看作有成本的 characterization query。

离线 algebra、symbolic derivation、Pro run reasoning 可以看作不增加 physical acquisition budget 的 computation。

### 可能带来的改变

以后我们可以更严谨地比较：

- 一个方案需要 4 个 fresh runs 才能识别；
- 另一个方案需要 8 个；
- 哪些 query 是 adaptive；
- 哪些只是在重复已有 axis information。

这能给 bounded project 一个很合适的评价标准：

> 用多少真正新的 acquisition，换来了多少独立 predictive information。

当前还没有必要追求完整 query-complexity theorem，所以保持 B 级。

---

## 11. F289：structural closeness 需要先定义 metric

### 已读材料

- [PDF](preprints/Universal-strong-Kadison-Kastler-stability-September-23-2026/paper.pdf)
- [Introduction](preprints/Universal-strong-Kadison-Kastler-stability-September-23-2026/build/sections/01-introduction.tex)

Kadison-Kastler 的距离是对称的。论文也明确区分 ordinary gap、matrix-level control、spatial implementation 和 one-sided near inclusion。

### 对 DPT 的主要价值

它提醒我们：

> 几个 waveform fit 得很近，与两个 command representation 在结构上很近，不是同一件事。

以后如果要说 native system 接近 reduced algebra，需要明确：

- 比较的是哪些 attainable responses；
- metric 是否对称；
- command composition 是否也接近；
- 是否存在一个 nearby exact object。

目前它主要是 claim discipline。

---

## 12. F325：Complete Crouzeix，暂时保留

### 已读材料

- [Lean scope](lean/docs/325.md)
- [Direct proof](preprints/A-direct-proof-of-the-complete-Crouzeix-inequality-September-26-2026/paper.pdf)
- [Source](preprints/A-direct-proof-of-the-complete-Crouzeix-inequality-September-26-2026/build/main.tex)

它控制 nonnormal operator 的 polynomial / rational functional calculus。

如果 DPT 后续 representation 真的发展成较高维 nonnormal propagator，并需要对多步 command 的 polynomial function 做 norm bound，这个 family 会有价值。

当前 representation 还没有复杂到需要它。现在引入会增加数学负担，却不改变 S09 或当前 theorem，所以先放 B 级。

---

## 13. 二级候选：目前不进入主线

对全部 372 family 做过 DPT-oriented screening 后，下面这些工作值得保留，但暂时不应占用主要预算。

### F357：Bi-Lipschitz coordinates

它提醒我们：一个 coordinate 能区分，与稳定地能区分不同。真正 stable coordinate theorem 要有明确 regularity 条件。

### F374：Brenier map stability

它说明 uniqueness 和 quantitative stability exponent 是两层问题。以后 DPT 即使证明 unique representation，也还要问噪声放大率。

### F098：finite-dimensional embedding counterexample

它是一个反例提醒：看起来 low-complexity、compact 或 doubling，不自动意味着存在稳定 finite-dimensional embedding。

### F119：information contraction

可能为后续 information bottleneck 提供工具，但当前 DPT observation geometry 还没有需要它。

### F229：reconstruction threshold

可以帮助思考什么时候 information 足够恢复，但目前与 DPT 的直接数学接口还弱。

这些 family 目前只承担边界审查，不作为论文主证明的依据。

---

## 14. 把这些工作组合起来后，DPT 可以形成什么 theorem stack

单独引用很多高级数学并不会自动提高项目。真正有价值的是把它们组织成一条连续论证。

### T1：exact goal quotient

在声明的 reduced law 和 command class 内证明：

- 某个 finite coordinate 对目标足够；
- 它在 command 下可以闭合更新；
- 因而不需要完整内部 physical state。

这是现有工作基础最好的一层。

### T2：goal-visible hidden dimension

定义：

K = ker(DO)

N = K ∩ goal-null directions

r_G = dim(K/N)

然后证明：

- 当前 measurement 至少缺多少维 goal-relevant information；
- 至少需要几个 scalar repair；
- 某个实际 measurement 达到了这个下界。

这是 F355 最可能带来的新数学内容。

### T3：predictive information lower bound

对 d_G 构造 packing，证明：

- 任何 uniform predictor 至少需要多少 finite states / bits；
- 当前 representation 的复杂度离这个 lower bound 有多远。

这是 F140 的主要价值。

### T4：ordered command signature

把 primitive、mixed、ordered response 统一到 finite word hierarchy，明确：

- 现有 axes 决定了哪些 coefficient；
- S09 新增了哪个 mixed functional；
- optional S10 还要买哪一项信息。

这是 F116 和 acquisition design 的连接。

### T5：approximate native algebra

定义 composition defect，并研究 small defect 是否意味着靠近 exact finite representation。

这属于后续升级，不要求在 S09 前完成。

### T6：certificate-grade numerical layer

对真正 load-bearing 的 computation，明确分别给出：

- exact identity；
- numerical bound；
- provenance；
- prospective native outcome。

这一层由 F266 支撑。

---

## 15. 这些 family 组合后会带来什么实质变化

### 15.1 数学对象会更集中

如果不引入这些结构，项目容易不断积累：

- 一个 phase law；
- 一个 charge observation；
- 一个 fusion effect；
- 一个 timing effect；
- 一个新的 residual pattern。

每个结果都可能是对的，但彼此比较散。

把 F140、F355、F116 连起来以后，可以把这些结果重新解释成一个统一问题：

> 一个 switching history 需要保留哪些 goal-relevant information，future commands 如何作用在这份 information 上，新的 measurement 如何补足当前 representation 看不见的部分。

这样各个发现开始服务同一个 scientific object。

### 15.2 为什么做 S09 会更强

以前 S09 可以解释为模型之间 spread 大，因此值得测。

现在还能加一层：

> primitive axes 没有识别 mixed functional，S09 是第一次直接 acquisition 这个缺失项。

如果 S09 成功，它增加的不只是一个 datapoint，而是一类新的 independent information。

### 15.3 optional S10 会更容易裁决

S10 不应自动选择 forecast disagreement 最大的点。

更合适的规则是：

> S09 之后还剩哪个 goal-visible direction 或 interaction coefficient 未被识别？

如果 simultaneous interaction 已解决，但 order dependence 仍未解决，那么 AB vs BA 可能比再做一个 fusion amplitude 更值。

### 15.4 P2 可以从 sensor suggestion 升级为 measurement theorem

这可能是整个 map 中最明确的提升。

从：

> 我们建议加一个 drain observation。

提升到：

> 当前 observation 的 goal-visible hidden dimension 是 1，因此任何 local sufficient repair 至少需要一个 independent scalar，某个 drain / charge anchor 达到该下界。

这会让 sensor choice 和数学贡献连起来。

### 15.5 数值结果的证据层次会更清楚

F266 可以让项目里的 proof、verification、simulation 不再混用。

一个结果可以明确标注：

- algebra exact；
- numerical certified；
- simulator observed；
- native/hardware untested。

这样既不需要为了谨慎写成满页“不能说明”，也不会把 simulator coincidence 写成 theorem。

### 15.6 论文的 contribution 结构会更独立

如果 T1-T4 能形成闭环，论文贡献不再主要依赖某个 SiC MOSFET 的几条仿真曲线拟合得很好。

更可能形成这样的结构：

1. 定义 goal-dependent predictive representation；
2. 构造一个 exact low-information quotient；
3. 给出 measurement / information lower bound；
4. 用 prospective mixed acquisition 检验 representation 的下一项未知 interaction；
5. 用 certificate-grade computation 支撑关键数学和数值接口。

这类结构即使后续某个具体 physical mechanism 被否掉，研究对象本身仍然可以保留。

---

## 16. S09 与 optional S10 的当前解释

现阶段仍建议保留 S09 fusion 作为主要 fresh acquisition，前提是它的 freshness contract 没有被破坏。

### S09

在 declared quadratic response class：

F(alpha,beta) = F0 + alpha L_A + beta L_B + alpha^2 D_A + beta^2 D_B + alpha beta C_AB

primitive axes 无法确定 C_AB。

因此 S09 最清楚的科学角色是：

> **第一次直接测量 primitive axes 之外的 mixed functional。**

评分后：

- interaction 接近零：保留该 primitive pair 上的 affine / linear-memory null；
- 落在冻结的 Q / phase cluster：说明该 predictor 有 prospective usefulness，但不能单凭这一点认定唯一 charge mechanism；
- 落在所有冻结 candidate 之外：直接否掉这些 finite interaction rules，不在 outcome 后重新调 gain / phase；
- post-score charge diagnostics 只用于定位 failure 是 charge additivity 还是 transverse interaction。

### optional S10

S10 应该服从 S09 后的 remaining nullspace。

高价值候选包括：

- AB vs BA，检验 order-sensitive memory；
- 一个能够区分两个仍然 observationally equivalent history 的 query；
- 一个专门测试 measurement-repair sufficiency 的 case。

如果 S09 已经把 interaction 问题解决，再做一个相似 fusion amplitude 的边际价值可能很低。

---

## 17. 对 Pro run / Codex 的实际使用方式

不应该每次把 722 篇 manuscript 全塞进去。按问题选择最相关的数学 bundle 更有效。

### 做 P2 / minimum measurement

给：

- 当前 Pro17D scientific report；
- F355 linear.tex；
- F140 06-fiber.tex；
- reduced-law derivation；
- reachable-pair / goal evidence。

任务重点：

> 推出 goal-visible hidden dimension、最少 measurement 数和 local sufficiency 条件。

### 做 command algebra / interaction

给：

- A3 / N4；
- F116 iterated-integrals.tex、multiplicity.tex；
- primitive axes；
- S09 frozen forecast；
- exact command definitions。

任务重点：

> 建立 primitive / mixed / ordered coefficient hierarchy，并判断下一项最值得 acquisition 的 coefficient。

### 做 numerical certificate

给：

- F266 verification / execution；
- LTspice manifest；
- model hashes；
- scorer；
- exact derivation；
- numerical margins。

任务重点：

> 区分 candidate generation 与 verification，把 load-bearing numerical claims 变成 exact 或 one-sided certificate。

### 做 identifiability review

给：

- F365 positive + negative pair；
- F372；
- 当前 DPT model class；
- observation / goal / symmetry 声明。

任务重点：

> 检查 claim 是否只在 reduced class 成立，哪些 extension 会破坏 uniqueness。

### 做 approximate native algebra

给：

- F251；
- F289；
- native composition residual；
- reduced exact maps。

任务重点：

> 定义合适 defect 和 metric，先判断是否存在可证明的 stability question。

---

## 18. 下一轮阅读和推导优先级

### 第一优先：F355

继续读 finite-dimensional reduction 和相关 normalized-coordinate construction。

目标不是多摘几个 lemma，而是写出一个 DPT 自己的：

> minimum goal-relevant measurement theorem。

### 第二优先：F140

继续读 Posterior replicas、conditional information、subsphere / fiber 方法。

目标是判断 simple packing lower bound 能否进一步加强，或者能否处理 noisy / randomized finite state。

### 第三优先：F116

只有当 command-word hierarchy 已经进入实际 DPT derivation 后，再深入 formula-systems.tex 和 construction.tex。

### 第四优先：F266

当某个 Pro17D numerical claim 真正准备进入论文时，再针对该 claim 阅读 rounding / verifier code，并制作同等级别的 DPT certificate。

### 第五优先：外部 prior subtraction

T2-T5 如果准备写 novelty，需要补：

- Hermann-Krener nonlinear observability；
- Chen-Fliess series / nonlinear realization；
- predictive-state representation；
- goal-oriented model reduction；
- optimal experiment design。

这一步决定我们到底是在重新表达已有理论，还是确实形成了 power-semiconductor 中新的 bounded object。

---

## 19. 如何长期维护这份文件

以后每读一篇对 DPT 有实际影响的 manuscript，只记录真正发生了改变的内容：

1. family / manuscript 和具体路径；
2. 阅读深度；
3. 原论文实际证明的 theorem；
4. 和 DPT 哪个 object 对应；
5. 哪些 assumptions 可以保留；
6. 哪些 assumptions 在 DPT 中失效；
7. 它改变了哪个 theorem、acquisition、certificate 或 claim；
8. 使用后预计能提高哪一层科学内容；
9. 下一条 falsifier 或未解决依赖。

仅仅读过或引用过不算 materially used。

一篇文献真正进入这个项目，至少要改变下面之一：

- definition；
- derivation；
- experiment selection；
- lower / upper bound；
- certificate；
- claim boundary。

---

## 20. 当前结论

截至这一轮，OpenAI Math 对 DPT 最有价值的作用已经比较清楚。

**F355** 最可能产生新的 DPT theorem，因为它直接对应当前 measurement 究竟少几维的问题。

**F140** 最可能提高 representation 的数学上限，因为它把 sufficiency 推向 lower bound。

**F116** 最直接改变 S09/S10 的 acquisition logic，因为它提供了 organized command / interaction hierarchy。

**F266** 不一定创造新 physical law，但它能显著提高强数值结果的证据质量。

**F365/F372** 负责把 identifiability 的边界说清楚。

**F251/F289** 更适合下一阶段，把 exact reduced algebra 推向 approximate native algebra。

如果这几条线能在剩余预算内形成闭环，DPT-R1 最有希望获得的升级是形成一个更完整的研究对象：

有限 predictive quotient + 最小 goal-visible measurement + predictive information lower bound + 有目的的 mixed/ordered acquisition + certificate-grade validation

这五部分彼此有依赖，也彼此能被反证。它们比单独继续增加 waveform fit、parameter inversion 或 post-hoc mechanism explanation 更有机会形成一个可以独立站住的数学与器件物理结合框架。
