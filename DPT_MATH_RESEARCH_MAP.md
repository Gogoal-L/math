# DPT-R1 × OpenAI Math：主控研究利用图谱

这份文件服务于主控，不做论文摘要集。每篇文献只保留四件事：它在 Pro17D 中是什么身份、真正可迁移的数学动作、会改变哪个 DPT 决策、什么时候值得重新打开。

最后更新：2026-10-08（对照官方 fd4aeeb2；扩展 F332/F324/F329/F376 proof transfer）  
当前对象：DPT-R1 / Pro17D，预算上限 S09 + optional S10。

### 使用方式：主控仍然只需要这份 MAP

本轮采用轻量研究桥：本文件保留问题、推导、优先级与决策入口；[`literature/`](literature/README.md) 保存按 family/subpaper 命名的 PDF，以及对应的 Lean scope / selected-statement 阅读快照。来源路径、commit、文件校验值、DPT 独立推导、现有代码/测试和 reopen condition 集中在一份 [`registry.json`](literature/registry.json)，供追溯与手动增量检查；主控平时不用逐项阅读它。原 `preprints/` 与 `lean/` 文件继续作为完整源码与证明入口，原 PDF 链接全部保留在 literature 对照表。

**希望从先进数学获得的实际增量**：发现更好的预测对象、证明更少测量已经足够、构造现有模型无法排除的反例，或得到有明确误差范围的预测。数学结果若能改变这些对象，可以支持项目转向；先交付一个能与普通模型比较的 DPT 独立推导和最小验证，再由研究者判断转向价值。

| 最先检验的问题 | 可以立即使用的数学动作 | 什么结果会改变主控决策 |
|---|---|---|
| 参数未唯一确定时，目标是否仍能稳定预测？ | 独立 K/N 因子化 + noise-fiber goal ambiguity | 找到 goal-visible collision，或在声明范围内得到有限 gain / remainder 的目标预测界 |
| 已存 waveform 里有没有丢掉的有用信息？ | 比较压缩 observation 与 raw-trace 派生 feature | 现有特征足以消除关键歧义时，优先 zero-fresh 重分析；仍有歧义时明确所缺的独立信息 |
| 一条 fusion 到底识别了什么？ | 四角混合差分 + cubic rival + bias/noise envelope | 区分 finite mixed response、严格二次系数和条件式中心系数区间，决定 optional S10 是否值得 |

这些是当前可执行的研究问题。F355/F365-B/F357 提供 proof-pattern 启发，K/N 与误差界由 DPT 独立证明；F329/F332 的边界帮助选择正确的目标与假设。要进一步支持转向，最有价值的产物是一个新 predictive object，或一个较原对象更强且能被独立 history/command 反驳的预测，而非继续增加 theorem 名称。

**本轮验证范围（2026-10-08）**：论文首页身份、上游 `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` 的文件字节、Lean selected scope 与 37 个 synthetic Python tests。没有提供 native S09 archive；下一次真实 replay 仍需主控从 archive 明确 history/command identity、单位/时标、reference/query、信息预算与 provenance。当前不增加 adapter，不代替主控冻结证据或晋升 claim。

---

## 0. 先读这一页：主控应当带走什么

目前最有价值的统一问题是：

> 给定 future command family 和指定 goal，switching history 中最少需要保留什么信息，当前 observation 丢了哪些 goal-relevant directions，下一次 acquisition 应该购买哪一项尚未确定的信息？

OpenAI Math 与相关既有数学方法目前提供了若干互补动作；表中须区分**原论文已证明的定理**与**DPT 独立推导**：

| 动作 | 主要来源 | 对 DPT 的直接作用 |
|---|---|---|
| 找最小缺失 measurement | 独立有限维 K/N lemma；F355 为 finite-jet 方法启发 | 从 observation nullspace 中分离真正影响 goal 的方向；需声明局部稳定性假设 |
| 给 predictive state 做信息下界 | F140 | 从“这个 state 足够”推进到“更少信息不可能统一完成任务” |
| 建立有 definedness 的 command algebra | F116-A/B | command 顺序、mixed term、所有 inverse gate 的定义域一起管理 |
| 判断新 measurement 是否真的增加信息 | F229 | 用 experiment dominance / garbling 剪掉信息上冗余的 acquisition |
| 把 numerical fit 变成 certificate | F266 | center residual、approximate tangent、normal remainder、provenance 分层 |
| 从 tangent 结论升级到 finite-radius / nonlinear 结论 | F357 + F365-B，辅以 F374 | rank 之后还要有 multiscale directional/remainder control，不能把单点 Jacobian 当 neighborhood chart |
| 区分低维 approximation 与可部署的 stable representation | F330 + F094/F098 + F324 | 追 dimension、error、gain 和作用域；低失真 metric encoding 不直接决定 linear/physical coordinates | 
| 已有观测下的 deterministic worst-case goal ambiguity | 独立 finite-bank minimax；F329 作为反面启发 | 直接检验噪声 fiber 中的 goal gap，区分 archived feature 与新仿真 | 
| 稳定 goal factor 的延拓 | F332 | 在全类 observation image 已有 Lipschitz factor 时，研究如何延拓到 ambient observation space | 
| 可组合 predictive state | F376 + F116 + F129 + 经典 future-context equivalence | 检验未来命令词的 definedness、goal 与 stage telemetry，不只看 primitive endpoint |
| 有界 mixed-interaction certificate | F132 的 joint-profile 思想；独立的有限差分余项与误差设计 | 给 S09 一次 fusion 的真实识别范围、bias/noise envelope、幅度选择与 cubic ordinary counterexample |
| 固定 nonnormal propagator 的 operator envelope | F325 与经典 logarithmic norm | 一次比较 matrix-valued polynomial readout 的 numerical-range 界与更简单的 energy/lognorm 界 |

另外两条是长期边界：

- F365-A/C：identifiability 必须先声明 model class、goal 和不可见 symmetry；regularity 一变，uniqueness 可能直接翻转。
- F372：physical data 到 auxiliary representation 的 reduction 必须检查 injectivity；辅助变量上的 uniqueness 不能从 physical data 自动继承。
- F251/F289：small composition defect 或 one-sided trajectory fit 不自动给出 nearby exact algebra / structural equivalence；需要单独的 correction theorem 或 two-sided control。
- F325：一旦 frozen stage 变成 fixed nonnormal propagator，numerical range 可以给 polynomial/rational readout 一个 operator-norm envelope。
- F363：physics/conservation consistency 与 uniqueness 是两类证书；守恒本身不能替代 identifiability。

新的综合优先顺序是：先在已存 raw waveform 上定位 noise-fiber goal ambiguity（F329 的反例精神 + 独立 minimax），用 empirical gain 判断是否需要新 feature（F332 的条件式延拓），再检查 rival history 是否被未来 command-word/stage event 区分（F376 + F116）；F324 只给 metric 与 linear physical state 的解释边界。

如果主控只记一条执行规则：

> **每次准备增加一个 theorem、sensor 或 simulation 前，先问它究竟减少了哪个 goal-visible ambiguity；如果没有明确减少，就不占 fresh budget。**

---

## 1. 文献身份：Pro17D 当时用了什么，后来又发现了什么

状态含义：

- **P17-承重**：已经实际改变 Pro17D 的构造或证据结构。
- **P17-背景**：当时上传/可见，但 Pro17D 没有把它作为承重推导。
- **POST-主动**：本轮重新深读后，已经形成可执行的 DPT 新路线。
- **WATCH**：保留为边界或未来升级，不应占当前 S09/S10 预算。

| 文献 | Pro17D 身份 | 当前身份 | 最值得保留的作用 |
|---|---|---|---|
| F116-A One Rational Matrix Hitting Point | **P17-承重** | **POST-主动** | bounded rational system、multiplicity、ordered-word encoding |
| F116-B Polynomial Hitting Lists | P17-背景 | **POST-主动** | 每个 inverse occurrence 的 definedness；universal nonadaptive test bank |
| F229 Three-state reconstruction threshold | P17-背景 | **POST-主动** | experiment dominance / garbling；保守 finite upper experiment |
| F266 Maximum MUB in dimension six | **P17-承重** | **POST-主动** | Root-like certificate；未解决记录不能被当 negative evidence |
| F365-A Metric + connection from one patch | P17-背景 | **POST-主动** | quotient-first identifiability；response embedding |
| F365-B Smooth anisotropic Calderón | P17-背景 | **POST-主动** | finite probe-jet completeness + superlinear bootstrap |
| F365-C Rough scalar conductivity nonuniqueness | P17-背景 | **POST-主动** | regularity/model-class 改变可辨识性本身 |
| F372 Smooth isotropic elasticity uniqueness | P17-背景 | **POST-主动** | physical-to-auxiliary injectivity audit；full operator ≠ finite reconstruction |
| F374 Brenier one-third stability | P17-背景 | WATCH / 方法主动 | uniqueness 与 stability modulus 分开；边界切换可造成非 Lipschitz 放大 |
| F355 Tangent-flow uniqueness | Pro17D 后发现 | **最高优先 POST** | goal-visible hidden dimension / minimum measurement |
| F140 Memory-constrained inference | Pro17D 后发现 | **最高优先 POST** | finite information lower bound；adaptive selection 的 information charge |
| F357 Bi-Lipschitz coordinates at regular RCD points | Pro17D 后发现 | **POST-主动 / 高优先** | multiscale directional defect；从 tangent regularity 到 all-pairs local chart 的 proof architecture |
| F330 Bounded approximation failure | Pro17D 后发现 | **POST-主动 / 高优先** | finite-rank approximation 与 uniformly bounded stable representation 的分离 |
| F094 Subpolynomial Lp reduction | Pro17D 后发现 | **POST-主动** | exact complexity 与 fixed-distortion approximate complexity 可以完全不同 |
| F098 Doubling Hilbert obstruction | Pro17D 后发现 | **POST-主动** | finite-set success / doubling geometry 不保证 whole-class finite-dimensional bi-Lipschitz state |
| F289 Kadison-Kastler + one-sided boundary | Pro17D 后发现 | **POST-主动 / 边界** | two-sided structural closeness 与 one-sided approximation 的分离 |
| F251 Strong Ulam stability companion | Pro17D 后发现 | WATCH / 条件主动 | small algebra defect 能否 correction 成 exact algebra 取决于结构，不可默认 |
| F325 Complete Crouzeix | Pro17D 后发现 | WATCH / 触发即主动 | fixed nonnormal propagator 的 polynomial/rational functional control |
| F363 Boltzmann nonuniqueness refinement | Pro17D 后发现 | WATCH / claim guard | conservation / consistency 不等于 uniqueness |
| F129 Exponential state cost | Pro17D 后发现 | WATCH / 长期 | future-context separation 可转成真正的 discrete state-complexity lower bound |
| F332 Metric Markov cotype of ell1 | 后续深读 | POST-条件主动 | 已稳定 ell1-valued goal factor 的 dimension-free Lipschitz extension，不提供可辨识性 |
| F324 Lipschitz-equivalent nonisomorphic Banach spaces | 后续深读 | WATCH / 表示边界 | metric equivalence 不推出无限维 linear isomorphism；与有限维 DPT rank 判据区分 |
| F329 Metric-entropy duality counterexample | 后续深读 | POST-主动（边界启发） | 用 direct noise-fiber / packing audit，避免无假设的 polar entropy shortcut |
| F376 Universal computation in forced Navier–Stokes | 后续深读 | POST-主动（方法） | original-domain command semantics、history record、within-command guard；不引申流体物理 headline |
| F132 Block sensitivity exceeds squared ordinary sensitivity | 本轮深读 | POST-主动（方法） | 明确单扰动、联合谓词/组合干预两种证据，给 S09 robust interaction certificate 的建模动机 |
| F122 Worst-case deletion trace reconstruction | 本轮深读 | WATCH / 条件主动 | 明确时标与删除信道；只有原始采集确有未知时标删除才开复杂度分支 |
| F119 Sharp binary information contraction | 本轮深读 | WATCH | 仅在独立均匀 bit / symmetric noise 类被验证时可启用 sharp information bound |
| F325 Complete Crouzeix（第二轮证明检查） | 本轮深读 | WATCH / 固定矩阵触发 | 对 pure exponential 先比较经典 logarithmic-norm 界，matrix-coefficient polynomial/rational 再考虑 F325 |

Pro17D 自己在第 7 节明确把 F116-A 与 F266 作为重点亲读和实际采用的 OpenAI Math 来源；其余当时保持 navigation/background 身份。这里不会把后续发现倒写成 Pro17D 当时已经使用。

### 证据身份

这些论文非常新。外部资料在 2026 年较早阶段仍把 smooth anisotropic Calderón 和同时恢复两个 Lamé moduli 列为 open problems，因此 F365-B/F372 属于需要高强度独立核验的 headline claims。当前图谱主要使用它们的 proof architecture，不让 DPT 的承重结论依赖“OpenAI 已解决该开放问题”这一事实。状态校准可参考 [AIM inverse-problem catalog](https://github.com/MColbrook/AIM/blob/main/CATALOG.md) 和 [2026 ICM satellite inverse-problem talk](https://sites.math.rutgers.edu/~mv715/schedule)。F374 目前也有独立工作复用了其 three-atom sharpness construction，但该工作明确不验证 OpenAI 的 general one-third theorem，见 [Evidence Press transport-map certificate](https://evidencepress.org/releases/planar-transport-map-sensitivity-certificates/)。

仓库自身的 formalization scope 也必须逐篇看：

- F116：scope 覆盖 selected universal hitting theorem，并覆盖 rational-formula hitting-list 结果。
- F229：当前 selected formalization 只覆盖 Kesten-Stigum 阈值以上的 reconstruction；临界/次临界 non-reconstruction 不在 selected statement 中。
- F266：selected formalization 明确弱于论文 headline 的 N(6)=3。
- F365：当前 365 scope 记录的是 bounded measurable scalar conductivity nonuniqueness，也就是这里的 F365-C。
- F372、F374：对应 scope 文件声明覆盖各自主 uniqueness / stability statement。
- F094、F098、F330、F325：仓库都有 selected formalization，覆盖这里使用的主要 dimension-reduction / approximation / Crouzeix statement。
- F289：selected formalization 覆盖 September 的 universal strong Kadison-Kastler stability；October 的 one-sided near-inclusion counterexample 目前不在该 scope 内。
- F251：当前 `lean/docs/251.md` 覆盖 unitarizability 主结果；这里使用的 October Strong Ulam Stability companion 不应自动标成 Lean-backed。
- F357：当前仓库未见 `lean/docs/357.md`，所以这里只把它当 proof architecture 使用。
- F363：selected formalization 覆盖较早 periodic nonuniqueness 结果；October 的 exact local-conservation refinement 是更强版本，不能借旧 scope 替它背书。
- F129：selected formalization 覆盖 one-way liveness 的 exponential deterministic state lower bound。
- F132：lean/docs/132.md selected statement 覆盖其 superquadratic sensitivity separation；该 theorem 的 Boolean 模型和 DPT 的连续参数交互不同。
- F122：lean/docs/122.md selected statement 覆盖 worst-case deletion trace **lower bound**；不是其 October uniform decoder 的同一套证明。
- F119：lean/docs/119.md selected statement 覆盖 uniform-cube noisy binary summary 的 sharp contraction。
- F325：lean/docs/325.md 覆盖 complete Crouzeix 的 polynomial/holomorphic/rational 指定端点；当前 DPT 没有已冻结 native generator A。
- F324 的 lean/docs/324.md 涵盖 separable Banach 反例；F329 的 lean/docs/329.md 涵盖 dimension-free entropy-duality 反例。其 Lean scope 仅覆盖该 family 的指定 statements，不替 DPT 迁移证明背书。
- F332：本轮未发现 lean/docs/332.md；按未经本项目独立证明核验的预印本使用。
- F376：lean/docs/376.md 分别覆盖若干 sheet、box、particle/velocity detector statements；October 6 修订与各种 pressure/clock companions 不可整体继承旧 scope。

因此“Lean-backed”必须按具体 statement 使用，不能按 family 名整体继承。

---

## 2. F116-A / F116-B：command algebra 的价值比 multiplicity 更大

### 深读锚点

- [F116-A PDF](literature/F116-A_noncommutative_hitting_point.pdf)
- [formula-systems.tex](preprints/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026/build/formula-systems.tex)
- [construction.tex](preprints/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026/build/construction.tex)
- [F116-B PDF](literature/F116-B_rational_hitting_lists.pdf)
- [encoding.tex](preprints/Polynomial-Hitting-Lists-for-Noncommutative-Rational-Formulas-September-24-2026/build/sections/encoding.tex)
- [rank.tex](preprints/Polynomial-Hitting-Lists-for-Noncommutative-Rational-Formulas-September-24-2026/build/sections/rank.tex)

### 读完后最重要的三件事

**1. Pro17D 对 F116-A 的使用是正确的。**  
F116-A 把 bounded formula 转成小维 rational differential system，再用 multiplicity 控制非零 scalar output 最晚何时出现。Pro17D 没有把 A3 强塞进其 Fuchsian degree 假设，而是转向直接 finite lift + definedness proof。这一点应保留。

**2. F116-B 对 DPT 新增了一个更实用的规则：definedness 属于表达路径，不属于化简后的函数。**  
Rational formula 里每个 inverse gate 都必须在原 expression tree 上可逆。后续代数 cancellation 不能替一个原本 undefined 的中间 inverse 洗白。

对 Möbius / Riccati / matrix command composition，这意味着主控以后不能只检查最终 denominator。应当保存：

- 每个 inverse occurrence；
- 它的 admissible domain；
- composite command 后 domain 是否仍闭合；
- 简化前后 definedness 是否一致。

这可以形成一个轻量 **command-domain certificate**。

**3. universal hitting list 给出一个远期但很有吸引力的 acquisition 思路。**  
F116-B 的 test list 只依赖变量数和 size bound，不依赖 formula coefficients。DPT 如果以后能把 bounded command family 真正放进一个有限 rational representation class，就可以问：

> 是否存在一个 coefficient-independent、预先冻结的有限 query bank，只要 representation 非零/有额外 mode，就一定有一个 query 能击中它？

这比 outcome-aware 地找下一点更强，但目前只是研究方向，不应冒充已有 DPT theorem。

### 对主控的触发规则

当出现下面任一情况，重新打开 F116：

- 新的 command map 含 inverse / Möbius / rational matrix composition；
- 想声称 finite Taylor/order 足以检测非零 discrepancy；
- 想设计 outcome-blind 的固定 characterization bank；
- S10 想区分 AB 与 BA 或更高 ordered interaction。

---

## 3. F229：先判断新 measurement 是否真的增加信息

### 深读锚点

- [F229 PDF](literature/F229_three_state_reconstruction.pdf)
- [foundations](preprints/The-exact-reconstruction-threshold-for-the-three-state-symmetric-channel-September-25-2026/build/sections/02-foundations.tex)
- [finite experiment / grid](preprints/The-exact-reconstruction-threshold-for-the-three-state-symmetric-channel-September-25-2026/build/sections/06-grid.tex)
- [certificates](preprints/The-exact-reconstruction-threshold-for-the-three-state-symmetric-channel-September-25-2026/build/sections/appendix-certificates.tex)

### 真正可迁移的不是 Potts threshold

最值得 DPT 使用的是 **experiment order**。

F229 把 posterior 本身视为 sufficient experiment，并用 degradation / garbling 比较实验：如果一个 observation 可以由另一个 observation 通过 Markov kernel 生成，它不会更有信息。这个 order 在 edge transmission 和 branch composition 下保持。

对 DPT 的直接翻译：

> 如果候选 readout 只是已有 waveform 的确定性 post-processing，它不能为 identifiability 新增 information dimension。

例如从同一 VGS trace 再计算一个 scalar feature，可能提高 numerics 或 robustness，但它不是独立 sensor evidence。新的 drain/charge/current measurement 则可能切开原 observation fiber。

### 更强的 proof architecture

F229 的负向证明还有一个值得保留的套路：

1. 先解析证明“任何非平凡固定点必须离 trivial state 至少有一个 gap”；
2. 再构造一个 **更有信息的有限 surrogate experiment**；
3. 如果连这个上界 experiment 都落在 gap 以下，那么真实 experiment 更不可能支撑非平凡解；
4. 数值 rounding / omitted tails 全部朝“更有信息”方向补偿，因此计算误差不会制造假 negative。

DPT 以后若要证明某一 observation family 不足，可以尝试同样的方向性证书：

> 不需要精确模拟所有 native uncertainty，只要构造一个明确比真实 observation 更有信息的 upper experiment；若它仍不能区分 goal-distinct states，真实 measurement 更不可能做到。

这比“当前 optimizer 没找到”强很多。

### 当前边界

DPT 现在主要是 deterministic simulation，没有完整 probabilistic experiment model，所以 Blackwell/garbling machinery不能直接搬 theorem。现阶段先使用它的 **information-dominance test**：

- 是新增物理信息，还是已有数据的 post-processing？
- 若是 surrogate，它相对真实 system 是信息上界还是下界？
- numerical approximation 的方向是否保守？

### 对主控的触发规则

每次提出新 sensor、feature、query 或 surrogate 前，先做一次 dominance check。若新对象只是旧 observation 的函数，它不应被计成独立 identifiability evidence。

---

## 4. F266：把 E1/E2/N2 收成一个可复用 certificate object

### 深读锚点

- [F266 PDF](literature/F266_dimension_six_MUB_certificate.pdf)
- [rounding](preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/build/sections/rounding.tex)
- [phase-cover / Root certificate](preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/build/sections/phase-cover.tex)
- [refinement](preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/build/sections/refinement.tex)
- [execution](preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/build/sections/execution.tex)

### Pro17D 已经吸收的部分

F266 促使 Pro17D 不把小 tangent residual 当成完整 certificate，而是分开：

- center defect；
- approximate tangent / projector；
- Gram / orthogonality defect；
- nonlinear normal remainder；
- operator/readout contribution。

这已经进入 E1/E2/N2。

### 本轮再往前一步

F266 的 Root certificate 实际上提示我们把这些信息做成一个标准数据对象，而不只是散落在报告里。

一个 DPT local certificate 至少应包含：

center  
+ local coordinates / tangent basis  
+ center residual  
+ Gram/projector defect  
+ domain radius  
+ normal remainder bound  
+ readout/operator bound  
+ provenance

这样主控以后拿到一个“局部 approximation 很准”的结论时，可以直接问：

> certificate object 是否完整？

而不用重新人工追 residual 是在哪个空间算的。

另一个必须继承的执行规则：

> **timeout、cap、unresolved cell、failed certificate 都保持 unresolved；任何资源失败都不能自动转成 nonexistence / exclusion。**

### 为什么只借 methodology

F266 的 headline MUB claim 很强，而 selected formalization 明确没有证明其 at-most-three headline。DPT 不需要依赖这个 headline。我们只使用可独立检查的 certificate architecture。

---

## 5. F365-A：先 quotient，再谈 uniqueness

### 深读锚点

- [F365-A PDF](literature/F365-A_metric_connection_partial_boundary.pdf)
- [introduction](preprints/Determination-of-a-metric-and-a-unitary-connection-from-one-boundary-patch-October-5-2026/build/sections/01-introduction.tex)
- [boundary/source evaluations](preprints/Determination-of-a-metric-and-a-unitary-connection-from-one-boundary-patch-October-5-2026/build/sections/02-boundary.tex)
- [matrix moments](preprints/Determination-of-a-metric-and-a-unitary-connection-from-one-boundary-patch-October-5-2026/build/sections/06-matrix.tex)

### 对 DPT 最有启发的两层

**第一层：不可见 symmetry 必须先 quotient 掉。**  
F365-A 的 uniqueness 从来不是裸 uniqueness，而是 modulo boundary-fixing diffeomorphism + unitary gauge。那些 transformation 本来就不会改变 measurement。

DPT 对应地应当先定义：

> 哪些 internal-history transformation 对所有 declared future goals 都不可见？

这和 goal quotient 完全一致。我们不需要恢复“真实内部状态”本身，只需要恢复其 goal-equivalence class。

**第二层：response embedding。**  
论文用 source-generated solution evaluation 把一个内部 point / fiber 映射到它对一族 source 的响应，由这些 response functionals 区分 points。

DPT 可以考虑对应对象：

I(h): c ↦ G_c(h)

也就是把 history 表示成“它对未来 probe commands 的响应函数”。有限 predictive representation 的目标，随后变成：

> 有没有有限 probe set 可以在当前 admissible class 上保留 I(h) 对目标所需的信息？

这是连接 PSR、F355 和 experiment design 的自然桥，但 general predictive-state idea 已有 prior，不能把 embedding 本身当 novelty。

---

## 6. F365-B：F355 之后最值得学的 nonlinear lift

### 深读锚点

- [F365-B PDF](literature/F365-B_smooth_anisotropic_Calderon.pdf)
- [local extension](preprints/Smooth-Anisotropic-Uniqueness-in-the-Calderon-Problem-from-One-Boundary-Patch-September-24-2026/build/sections/03-product-continuation.tex)
- [shrinking balls](preprints/Smooth-Anisotropic-Uniqueness-in-the-Calderon-Problem-from-One-Boundary-Patch-September-24-2026/build/sections/04-shrinking-balls.tex)

### 最值得迁移的 proof pattern

这篇论文不是只做 rank test。它先选择一个**有限 probe family**，使这些 harmonic jets span 所有 admissible second-order directions；然后：

1. 假设 discrepancy 在半径 r 上只有 O(r) 的 provisional control；
2. transfer functional 精确复现 constants 和 coordinates，因此 Taylor 的 affine 部分被消掉；
3. 剩余项变成 O(r²)；
4. finite-order interpolation + spanning jets 把结构 discrepancy 提升为 O(r^{3/2})；
5. 这是对 O(r) 的严格改善，因此可以让 r 缩到 0，得到 local equality。

### DPT 对应的问题

K/N 的独立 goal-visible nullity lemma 只给带稳定性前提的 tangent-level 最小 measurement。真正写论文时，reviewer 会继续问：

> rank 满了以后，为什么 finite perturbation 下仍然唯一/稳定？

F365-B 给的是一个很好的 proof template：

**finite probe completeness + first-order cancellation + superlinear remainder = nonlinear local lift**

对 DPT 不需要照搬 shrinking spheres。更简单的 inverse/constant-rank theorem 若足够，优先用简单版本。但主控应当把“rank + remainder”当成两道 gate，而不是看到 Jacobian full rank 就停止。

### 可以形成的实际判据

对候选 measurement set P：

1. 检查 DP 对 K/N 是否满秩；
2. 检查这个 rank 在一个 finite neighborhood 内是否保持；
3. 给二阶 remainder 一个明确 bound；
4. 证明 measurement separation 的线性项压过 remainder。

如果 2-4 做不到，只称 tangent identifiability，不升格为 finite-radius sufficiency。

---

## 7. F365-C：regularity 不是技术细节，它可能决定 uniqueness 是否存在

### 深读锚点

- [F365-C PDF](literature/F365-C_rough_scalar_conductivity_nonuniqueness.pdf)
- [scalarization](preprints/Nonuniqueness-for-Bounded-Measurable-Scalar-Conductivities-in-Three-Dimensions-September-23-2026/build/sections/scalarization.tex)
- [nonuniqueness construction](preprints/Nonuniqueness-for-Bounded-Measurable-Scalar-Conductivities-in-Three-Dimensions-September-23-2026/build/sections/nonuniqueness.tex)

### 对 DPT 最重要的反例意义

这篇工作宣称：在 3D，两个不同的 uniformly positive bounded measurable scalar conductivities 可以拥有相同的 full Dirichlet-to-Neumann operator；而 smooth scalar class 中有强 uniqueness 结果。

对 DPT 的警告非常直接：

> “我把未知对象写得更灵活”并不只是增加 fitting freedom，它可能把一个可辨识问题变成根本不可辨识的问题。

所以 native model class 以后不能只写“allow nonlinear Cgd / unknown charge surface”。还要明确：

- finite-dimensional parameterization 还是 arbitrary function；
- smoothness / monotonicity / bounded variation；
- physical reciprocity / positivity；
- operating-domain restriction。

如果这些 class assumptions 不冻结，任何“minimum measurement”都没有稳定含义。

### 一个可借的构造观念

F365-C 的 scalarization 只精确保留有限个指定 Cauchy pairs，而不是完整 operator。这个区别对 DPT 很有用：

> 一个 reduced model 能精确匹配若干 selected trajectories，不代表它等价于 native input-output operator。

因此“finite trajectory match”和“operator equivalence”必须始终分开。

---

## 8. F372：physical-to-auxiliary reduction 要做 injectivity audit

### 深读锚点

- [F372 PDF](literature/F372_smooth_isotropic_elasticity_uniqueness.pdf)
- [introduction](preprints/Global-Uniqueness-for-the-Smooth-Isotropic-Elasticity-Inverse-Problem-September-24-2026/build/sections/introduction.tex)
- [physical transfer](preprints/Global-Uniqueness-for-the-Smooth-Isotropic-Elasticity-Inverse-Problem-September-24-2026/build/sections/boundary-reduction.tex)
- [transport matching](preprints/Global-Uniqueness-for-the-Smooth-Isotropic-Elasticity-Inverse-Problem-September-24-2026/build/sections/transport-matching.tex)
- [coefficient recovery](preprints/Global-Uniqueness-for-the-Smooth-Isotropic-Elasticity-Inverse-Problem-September-24-2026/build/sections/coefficient-recovery.tex)

### 为什么这篇对我们比原先想的更有用

论文回顾一个历史错误：把 physical elasticity problem reduction 到 auxiliary vector-scalar system 后，原 reduction map 并非 injective，因此 physical boundary equality 不能自动提升成 unrestricted auxiliary Cauchy-data equality。

这恰好是 DPT 常见风险。

我们会不断引入：

- deembedded waveform；
- charge coordinate；
- Riccati variable；
- Möbius lift；
- latent stage state；
- surrogate feature。

主控必须区分两类结论：

1. auxiliary coordinate 足以 **forward predict goal**；
2. physical observations 足以 **uniquely recover auxiliary coordinate**。

前者不需要 injective；后者必须证明。

### 主控的新检查项

任何时候由 physical equality 推 auxiliary equality，都先问：

> physical → auxiliary 的 map 在当前 class 上 injective 吗？如果不是，是否只需要 quotient / forward sufficiency？

这条检查可以防止很多“变换之后看起来可解，所以原问题可辨识”的错误。

### 另一个边界

F372 使用 full displacement-to-traction operator，证明的是 uniqueness，不给 finite measurement reconstruction algorithm，也不给噪声稳定性。这再次提醒：

full operator uniqueness ≠ finite sufficiency ≠ stable reconstruction。

---

## 9. F374：不要从 uniqueness 跳到 Lipschitz robustness

### 深读锚点

- [F374 PDF](literature/F374_Brenier_one_third_stability.pdf)
- [introduction](preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/build/source/sections/introduction.tex)
- [finite stability](preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/build/source/sections/finite_stability.tex)
- [sharpness](preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/build/source/sections/sharpness.tex)

### 真正值得 DPT 学的东西

F374 的 sharpness example 很有启发：target measure 的扰动很小，但最优 map 的 cell assignment 在一条薄区域上发生切换，最终 map distance 的尺度明显大于 target perturbation 的线性尺度。

DPT 的对应风险是 regime boundary：

- commutation stage boundary；
- saturation boundary；
- diode branch transition；
- event timing crossing。

这些地方即使 predictor 唯一，也可能只有 Hölder-like robustness，不能默认 Lipschitz。

因此以后“stable identifiability”至少要报告一个 modulus：

||prediction/state difference|| ≤ ω(||measurement difference||)

哪怕 ω 只是 empirical envelope，也比只报告 local condition number 完整。

### 不做什么

不把 Brenier 的 1/3 exponent 移植到 DPT。这里只借两个结构：

- stability exponent 是独立科学对象；
- regime/cell reassignment 可以制造 sharp counterexample。

如果 DPT 要声称 robust low-information predictor，应主动在 stage-transition 附近做 adversarial perturbation。

---

## 10. Pro17D 后新增的高价值 family

下面先保留 F355/F140 两个直接承重 family，再加入第二轮筛选中会改变 claim ceiling 或验证路线的 family。

### 独立 K/N lemma：goal-visible hidden dimension（F355 用于 finite-jet 方法启发）

核心对象：

K = ker DO(h*)

N = K ∩ (所有 future goals 的 kernel)

r_G = dim(K/N)

解释：

- K：当前 observation 看不见的方向；
- N：虽然看不见，但对所有声明目标也没影响；
- K/N：真正缺失、且会改变未来 goal 的信息。

若增加 k 个 scalar measurements P，要在一阶消掉所有 goal-visible ambiguity，至少需要：

ker(DP restricted to K) ⊆ N

因此在要求 G=Phi(O,P) 为局部 Lipschitz 因子且 O/P/G 在中心可微时，k ≥ r_G。证明：对被 DO 与 DP 同时消去的方向 v，观测增量是 o(t)，Lipschitz 因子使目标增量也是 o(t)，所以 DG(v)=0。此下界是本项目的独立有限维微分引理，**并非 F355 mean-curvature-flow 论文定理**。F355 真正可迁移的是 finite-jet obstruction / exponent-independent certificate 的证明程序。

非 Lipschitz exact-recovery 反例：O(x)=x^3, G(x)=x 在零点 r_G=1，却有 G=cuberoot(O)，无需新测量但局部 gain 发散。另有候选可实现性限制：O=x, G=y，只允许 P1=y+z、P2=z 时，虽然 r_G=1，单个候选都不能 suffices，必须配合两个。

当前 reduced-law 的 drain-translation 例子正好可以成为 worked example：

- increment goal：translation 属于 N，不用补；
- absolute drain goal：translation 留在 K/N，一个 drain / charge anchor 补一维。

**主控用途**：sensor selection 以后优先最大化对 K/N 的 rank，而不是最大化 raw sensitivity。

### F140：predictive information lower bound + adaptive-selection charge

第一层是简单的 goal pseudometric：

d_G(h1,h2) = sup_c ||G_c(h1)-G_c(h2)||

如果 M-bit state 要 uniform error ≤ ε，则任何 2ε-separated goal packing 都需要不同 code：

M ≥ log2 P(H,d_G,2ε)

第二层是这次深读后更重要的东西：**actual rows 和 fresh rows 不能在 adaptive selection 后假装等价。**

F140 专门比较：

- learner 真正看过、并可能影响当前 finite state 的 observation；
- 与当前 state 独立的 fresh observation。

conditioning on selected state 会 bias actual observations，替换成 fresh rows 要支付 conditional-information cost。

**DPT 对应规则**：

- S10 若根据 S09 outcome 再选择，就属于 adaptive acquisition；
- 可以做，但它的 evidentiary role 与预先冻结的 S10 不同；
- outcome-aware query 不应再被描述成与 S09 同等级的 prospective test；
- 如果要保留强 prospective claim，应在看 S09 前冻结 selection rule，而不是只冻结一个模糊候选集合。

这比单纯“不要 data snooping”更精确，因为它告诉我们 adaptation 本身是一种 information channel。F140 的 O(d) conditional-information surcharge 严格依赖 spherical/Gaussian/memory 假设，**不能变成 DPT 的数值信息税**。此外必须区分 full acquired waveform Y、当前压缩 feature O=f(Y)、新提取的 existing-waveform feature P=g(Y) 和真正 fresh simulation。相对于 O，P 可以补足已经丢弃的信息，尽管无法超过完整 Y 的信息量。


### F357：把 tangent regularity 升级成 multiscale predictive chart

### 深读锚点

- [F357 PDF](literature/F357_regular_RCD_bi_Lipschitz_coordinates.pdf)
- [introduction](preprints/Bi-Lipschitz-Coordinates-at-Regular-Points-of-Noncollapsed-RCD-Spaces-September-25-2026/build/source/introduction.tex)
- [summable directional pinching](preprints/Bi-Lipschitz-Coordinates-at-Regular-Points-of-Noncollapsed-RCD-Spaces-September-25-2026/build/source/pinching.tex)

它最值得 DPT 借的不是 RCD 几何本身，而是一个严格区分：

> **tangent object 正确，不等于 neighborhood 内存在一个对所有 pair 都稳定的 coordinate chart。**

F357 在 dyadic scales `r_i` 上同时追踪局部 Gram normalization 与 directional defects；真正承重的是同一批 positive forms 在 actual coordinate differences 上的 defect 可以累积控制，而不是单点 Jacobian 看起来满秩。DPT 对应地不应只报告一个 center 的 singular values，而应在一组 frozen scales 上同时检查：

- goal-visible hidden dimension 是否保持；
- candidate measurement 的 row-space containment 是否保持；
- measurement-to-goal factor 的 gain 是否失控；
- directional / nonlinear remainder 是否有可求和或明确收敛的 envelope。

因此 T2 之后更自然的对象不是“再算一次 Jacobian”，而是一个 **multiscale predictive-coordinate certificate**。

### F330 + F094/F098：低维不够，还要区分 error、gain 和作用域

- [F330 PDF](literature/F330_discrete_Lipschitz_free_bounded_approximation.pdf)
- [F094 PDF](literature/F094_Lp_subpolynomial_dimension_reduction.pdf)
- [F098 PDF](literature/F098_doubling_Hilbert_embedding_obstruction.pdf)

F330 区分 approximation property 与 bounded approximation property：每个 finite/compact test 上都能找到 finite-rank approximant，不代表这些 approximants 可以共享一个 finite operator-norm bound。对 DPT 的翻译是：

> 每个有限 command bank 都能 fit 一个低维 state，不代表存在一个 uniformly stable、可部署的低维 predictor。

F094 又说明 exact 与 approximate complexity 可以数量级完全不同；F098 则说明即使 geometry 很“低复杂度”（doubling），整个 infinite/continuous class 仍可能没有任何 fixed finite-dimensional bi-Lipschitz representation。

因此 DPT 建议把“minimum state dimension”升级成至少带四个参数的对象：

`d_G(epsilon, kappa; H, C)`

其中 `epsilon` 是允许的 future-goal error，`kappa` 是 measurement/state 到 goal 的允许 gain/condition budget，`H` 是 admissible history class，`C` 是 future command family。任何低维 claim 都应同时声明自己覆盖 finite bank、finite neighborhood，还是 continuous operational class。

### F289 + F251：trajectory fit 与 structural equivalence 分开

- [F289 strong stability](literature/F289-A_strong_Kadison_Kastler_stability.pdf)
- [F289 one-sided boundary](literature/F289-B_one_sided_near_inclusion_counterexample.pdf)
- [F251 Strong Ulam companion](literature/F251_strong_Ulam_stability_amenability.pdf)

F289 的正向 strong Kadison-Kastler theorem 与 October one-sided counterexample 合起来给 DPT 一个直接 guard：

> “native 中每条 trajectory 都能在 surrogate 里找到近邻”是 directed approximation，不是 structural equivalence。

如果要声称两套 reduced/native dynamics 在结构上等价，至少需要 reciprocal/two-sided closeness，或者一个 explicit near-identity transformation/correction theorem。

F251 的 Strong Ulam companion 从 algebra 侧给同样警告：small composition defect 不能在没有额外结构时自动升级成“附近存在 exact command algebra”。因此以后若 `AB`、`BA`、fusion 等 composition residual 很小，主控只能先记为 **approximate algebra evidence**；是否能 correction 成 exact representation 是第二个 theorem。

### F325：fixed nonnormal propagator 出现时立即打开

- [F325 PDF](literature/F325-A_complete_Crouzeix_structural.pdf)

若后续 frozen stage 真能写成一个 fixed nonnormal operator `A` 的 polynomial / rational readout，F325 的 complete Crouzeix control 可以把 matrix functional 的 operator norm 压到 numerical range 上的二维 envelope：

`||R(A)|| <= 2 sup_{z in W(A)} ||R(z)||`

这里不把它扩展到不同矩阵的 arbitrary noncommutative product。触发条件很明确：**只有 fixed propagator / fixed generator 真正成为 load-bearing object 时才启用。**

### F363 + F129：两个长期 claim guard

- [F363 PDF](literature/F363_local_conservation_Boltzmann_nonuniqueness.pdf)
- [F129 PDF](literature/F129_one_way_liveness_state_lower_bound.pdf)

F363 的意义是把 **conservation certificate** 与 **uniqueness certificate** 分开。DPT 的 charge balance、energy balance、KCL/KVL 检查属于物理一致性证据，不替代 identifiability。

F129 则提供另一种 state lower-bound 语言：如果两个 histories 不同，总能找到一个 future context 把它们区分，那么任何正确 predictor 都不能把这两类 history 合并。若未来 DPT command family 被诚实离散成 finite semigroup / monoid，这条 context-separation 路线可能比 packing bound 更直接地给 deterministic state-complexity lower bound。

F136 与 F139 留在 WATCH：前者是 PPAD local-check robustness，后者在明确 well-conditioned logconcave potential 下给 sampling oracle complexity，都不构成 DPT mixed-query 直接下界。F119 在下面新增的原文小节单独审查；仍不占 S09/S10 预算。



### F332：已存在的稳定预测因子如何延拓为部署映射

**证据 locator**：[PDF](literature/F332_l1_Markov_cotype_extension.pdf)；[完整主证明及第 6 节 extension corollary](preprints/Metric-Markov-Cotype-Two-of-l1-October-5-2026/build/main.tex)；[Mendel–Naor 2013 先验](https://arxiv.org/abs/1301.3963)。目前未发现 lean/docs/332.md。本项目核对了主证明的 cut representation、cubic remainder、martingale telescoping 以及 corollary 的前提；**没有独立证明整篇预印本的全部细节**。

这篇论文的有用性必须从证明链理解。有限 \(\ell_1\) 点集可编码为 weighted binary cuts，使 \(\|x_i-x_j\|_1=\|z_i-z_j\|_H^2\)。作者取 cubic \(\phi(t)=3t^2-2t^3\)；其导数在 binary vertices 处消失，因此两点的平方 \(\ell_1\) 距离增量被 Hilbert 四次方势的 Bregman remainder 控制。条件于 martingale 旧状态时，Bregman 的一次项均值为零，累计损失 telescopes。论文给出 \(N_2(\ell_1)\le12\sqrt{21}\)，然后使用 Hilbert source 的 Markov type 2、\(\ell_1=c_0^*\) 和 Mendel–Naor extension theorem，得到 universal \(K\) 使任意已有的 Lipschitz \(f:S\subset H\to\ell_1\) 可以延拓到整个 Hilbert space，\(\operatorname{Lip}F\le K\operatorname{Lip}f\)。**\(K\) 并未被证明等于 \(12\sqrt{21}\)**。

**与 DPT 真正兼容的条件命题：** 令 \(\mathcal H\) 为已经声明的 switching-history class，\(Y=(O,P):\mathcal H\to\mathbb R^m\) 为单位白化的观测，\(G:\mathcal H\to\ell_1\) 为未来 goal readout。如果：(i) \(Y(h_1)=Y(h_2)\Rightarrow G(h_1)=G(h_2)\)；(ii) 对不同观测 pair 存在统一有限的
\[
L=\sup_{Y(h)\ne Y(h')}\frac{\|G(h)-G(h')\|_1}{\|Y(h)-Y(h')\|_2}<\infty,
\]
则 \(G\) 在 image \(Y(\mathcal H)\) 上才构成 Lipschitz map；**在接受 F332 所述 theorem 的前提下**，可将它延拓到全部 Euclidean observation space，放大至多 \(K\) 倍。extension 不是 identifiability theorem、不是 simulator validation、也不自动给 predictor 算法。若只关心单个 scalar readout，可直接考虑更简单的 McShane extension；F332 的特有价值是多通道 \(\ell_1\) goal 在目标维度增长时仍有 dimension-free existence framing。

**最小测试**：先在已有波形的 finite history bank 报 \(L_{\rm bank}\)。若存在相同 \(Y\) 但不同 \(G\)，有限 gain 不存在，必须找新 measurement 或收窄目标；若 \(L_{\rm bank}\) 过大，先比较从 raw waveform 提取新 feature 与真正新增 sensing 哪个能改善 condition。finite bank 上的低 gain 只是一项观察，无法给出 continuous-class 的 uniform upper bound。工具中新增的 scalar gain 是这一步的局部 indicator，不应标成部署 certificate。**S09 新仿真并非由 F332 自动触发。**

### F324：低失真 metric state 与 linear/physical state 的层级差别

**证据 locator**：[PDF](literature/F324_metric_equivalent_nonisomorphic_Banach.pdf)；[Hilbert slots 及图示](preprints/Lipschitz-Equivalent-Separable-Banach-Spaces-Need-Not-Be-Linearly-Isomorphic-September-24-2026/build/sections/05-hilbert.tex)；[localized linearization](preprints/Lipschitz-Equivalent-Separable-Banach-Spaces-Need-Not-Be-Linearly-Isomorphic-September-24-2026/build/sections/04-localization.tex)；[最终证明](preprints/Lipschitz-Equivalent-Separable-Banach-Spaces-Need-Not-Be-Linearly-Isomorphic-September-24-2026/build/sections/06-assembly.tex)；[Lean selected scope](literature/lean/F324_scope.md)。

预印本的准确结果是：可分**无限维**实 Banach 空间 \(X,Y\) 具有双 Lipschitz bijection，满足
\[
(4/21)\|s-t\|_X\le\|\Psi(s)-\Psi(t)\|_Y\le(76/25)\|s-t\|_X,
\]
但 \(X,Y\) 并不线性同构。关键并非凭空找一个 nonlinear embedding：先在 Hilbert blocks 中对 frozen slots 构造严格 isometry，保留各块的 perpendicular components，把旧 slot scalars 移到 even blocks、额外 scalar coordinates 移到 odd blocks（论文图示）；随后让 slots 依输入变化，借 derivative budget 保持全局双 Lipschitz，且在有限多点邻域形成 tail-coordinate local orthogonality；通过 Lipschitz-free linearization 得到 completely continuous operator，再用该线性结构不变量构造不可同构的 graph spaces。

**DPT 正向用途**：将四件事分开验收——goal-distance metric encoding、局部可微 Jacobian structure、可以依命令更新的 compositional state、物理参数语义。一个 nonlinear latent 能低失真预测 \(V_{DS},I_D,E_{\rm on/off}\)，并不因此揭示唯一的 \(L_g,L_s,R_g,\ldots\) 物理坐标，更不自动保持 composition law。先从现有数据检查两个 state 的 goal distance 与 latent distance 是否满足双向 bound，再检查其是否支持正确的 command update；不要直接回归参数唯一性。

**边界与反例作用域**：F324 的不可同构构造依赖无限维 Banach geometry，**不是**有限维 DPT tangent-rank lemma 的反例，也不给出任何 DPT 必须使用无限 latent dimension 的下界。对于光滑有限维历史流形，仍优先使用 inverse/constant-rank theorem。这里只在主控准备作 structural-identity 或“学到了唯一 physical state”的强解释时触发；当前 S09/S10 无须为其另增 query。




### F329：直接 goal ambiguity 优先于无假设的 polar-entropy 推断

**证据 locator**：[PDF](literature/F329_metric_entropy_duality_counterexample.pdf)；[matrix-to-body lemma](preprints/Counterexamples-to-the-duality-conjecture-for-metric-entropy-September-24-2026/build/sections/02-matrix-contract.tex)；[partition compression + pivot 图](preprints/Counterexamples-to-the-duality-conjecture-for-metric-entropy-September-24-2026/build/sections/03-compression.tex)；[parameter-order proof](preprints/Counterexamples-to-the-duality-conjecture-for-metric-entropy-September-24-2026/build/sections/05-counterexample.tex)；[Lean selected scope](literature/lean/F329_scope.md)。

作者的反例不是笼统的“covering number 不可信”。对任意提出的 dimension-free 比较常数 \(a,b\ge1\)，论文在**可随参数增加的维度**构造 origin-symmetric convex body \(K\)，另一体为 cube \(L=B_\infty^n\)，使 primal/polar covering entropy 的统一比较失败。主证明先制造实矩阵：rows 的 sup-norm separation 至少为 1，而 columns 的绝对凸包有非常小的 uniform approximation list。用 \(K=3\,\mathrm{absconv}\{R_x\}+tB_\infty\) 得
\[
N(K,L)\ge|X|,\qquad
N\bigl(L^\circ,(6\varepsilon+2t)K^\circ\bigr)\le M.
\]
partition-compression 的关键是保留 class label，而非原中心：图中 pivot 换为固定代表元后，控制路径长度由 \(j\) 放宽到 \(3j+2\)，再用 logarithmic profile 将其变为可控误差。该结论否定的是**无结构、跨维度**的 universal polarity shortcut；欧氏球/椭球等附加假设下的已有正面 duality 理论仍可用。

**独立、可直接证明的 DPT 正向对象**。给定指定 finite 或 compact history class \(\mathcal H\)，scalar goal \(g:\mathcal H\to\mathbb R\)，带单位白化的 observation \(Y:\mathcal H\to\mathbb R^m\)，确定性噪声 \(\|e\|_2\le\sigma\)，定义
\[
E_*(Y,\sigma)=\inf_{\hat g}\sup_{h\in\mathcal H,\|e\|_2\le\sigma}
|\hat g(Y(h)+e)-g(h)|.
\]
只要每个非空可行 fiber 上的 goal 有界，就有初等恒等式
\[
\boxed{E_*(Y,\sigma)=\tfrac12
\sup_{\|Y(h)-Y(h')\|_2\le 2\sigma}|g(h)-g(h')|.}
\]
**证明**：观测噪声球相交的任意一对 history 可以给出同一测量值，任意 estimator 至少对其中一个误差达到目标间隔的一半；反向，在每个非空观测 fiber 上取 goal 的 supremum/infimum 中点作为 estimator，误差至多该 fiber diameter 一半。两个 Euclidean 半径 \(\sigma\) 的球相交当且仅当中心间距离至多 \(2\sigma\)。这条 minimax lemma 属于我们在指定条件下的**独立初等构造，并非 F329 的定理或新数学发现**。对一般向量 \(\ell_2/\ell_1\) goal，最小 enclosing radius 通常不等于半径一半，必须另解 Chebyshev-center 问题。

**DPT 可证伪产物**：现有 finite history bank 上的 worst indistinguishable pair、goal gap、目标误差下界和 candidate feature 的改善。新工具 goal_ambiguity_audit.py 计算的是**supplied finite bank 的 exact scalar minimax 值**；当完整可行 history class 大于 bank，它仅是全类最坏误差的 lower bound。不要把局部 Jacobian dual singular-vector heuristic 冒充跨所有 history 的 information lower bound。结合 F229 的 experiment dominance，应优先重读已保存 raw waveform，看是否已有 feature 就能拆开最危险 pair，再决定 fresh acquisition。

### F376：从完整命令定义域到可更新的 predictive-state quotient

**证据 locator**：[shear-flow companion PDF](literature/F376-A_solenoidal_shear_instructions.pdf)；[七阶段 shear、recording 和 observer proof](preprints/Finite-Instructions-and-Solenoidal-Shear-Flows-September-27-2026/build/main.tex)；[October 6 box revision PDF](literature/F376-B_incompressible_box_computation.pdf)；[guarded-history proof](preprints/Incompressible-Box-Transport-and-Finite-Computation-October-6-2026/build/guarded-history.tex)；[torus scaling / physical-viscosity proof](preprints/Incompressible-Box-Transport-and-Finite-Computation-October-6-2026/build/torus-routing.tex)；[Lean 376 的 selected scope](literature/lean/F376_scope.md)。

必须先说明原论文为何引入 reversibility：作者需要把有限 symbolic instructions 嵌入**光滑不可压缩流的可逆 time map**，故以历史 record 保存被覆盖的旧信息。recorder lemma 要求 destination control 固定 incoming displacement，且 destination + written symbol 能唯一找回 predecessor；证明先检查**完整允许的 transition domain**，再看 special initialized run 的 checkpoint invariants。七阶段 lift/shears/translation/drop 作用于整个 closed source rectangle，而非某条被观察到的典型轨迹；observer 不是只核每个周期的 endpoint，还核所有 intermediate times 是否误入 forbidden strip。October 6 companion 进一步在不同 torus/box/force classes 下精确追踪尺度与投影，physical viscosity 不能在坐标伸缩中悄悄替换。

**真正可迁移的命题是有限 future-word congruence**，不是流体计算的普适性。设有限 history states \(H\) 和 partial deterministic command updates \(T_a:H\rightharpoonup H\)，每个 state 具有 goal \(g(h)\)，并可选择提供每个 command 的 within-stage readout \(q_a(h)\)（例如完整过程的 VDS peak 是否越阈）。定义
\[
h\equiv h'
\quad\Longleftrightarrow\quad
\text{对每个允许 future command word，全部 prefix definedness、
已声明的 stage readout 与 terminal goal 一致。}
\]
**Elementary proof**：若 \(h\equiv h'\) 且 \(a\) 对两状态均定义，则对任一后续 word \(w\)，从 \(T_a(h)\) 与 \(T_a(h')\) 运行 \(w\) 等同于分别从 \(h,h'\) 运行 \(aw\) 的后缀，故 \(T_a(h)\equiv T_a(h')\)。因此 quotient 支持 well-defined next-state update；对显式给出的有限确定性模型，反复 partition refinement 得到最粗的 goal/definedness/stage-output 等价类。这是 Myhill–Nerode-style 标准推论在 DPT command 语义上的使用，**不是 F376 已证明的 DPT 定理**。

两个 concrete falsifiers：① primitive A、B endpoint/goal 相同，但 \(G(T_B T_Ah_1)\ne G(T_B T_Ah_2)\)，说明单步 calibration 不足以支持 compositional prediction；② 两 history 的 A endpoint 完全相同，但一个 A 过程中 VDS peak 越阈，另一条不越阈，则仅保存 endpoint 的观测语义不足。command_word_audit.py 在 supplied finite transition table 上给出最短 distinguishing word，并比较用户明确输入的 transition_outputs；**工具不能从缺失的 native stage trace 自动推断输出**。

**最重要的作用域差异**：真实 SiC DPT 是含耗散、寄生和 switch-mode branch changes 的物理过程，既不需要 Turing-complete forced fluid，也不需要每个物理 command update 逆映射存在。F376 强制记录 reversible history 是为了其 fluid embedding；DPT 应借用的是显式定义域、命令前缀和全过程观察约束。如果同一已有 waveform 已经含完整 switching-stage trace，优先 zero-fresh 计算 within-command events。optional S10 只有在现存具体 rival 恰好被某个 admissible ordered command / stage observable 分开时才值得购买，而且 AB 和 BA 两个顺序不能假定由一次 simulation 免费同时提供。

**四文合成的最好研究对象**不是更复杂的 fit，而是一个证据三元组：有物理含义的 goal-visible ambiguity pair（F329 + 噪声 minimax），有明确 gain/extension 前提的低信息 observation state（F332，F324 作结构边界），以及一个最短的 admissible command-word/stage-output discriminator（F376 + F116）。输出至少保留：history/domain 身份、\(Y/G\) 端口、噪声归一化、最大歧义对、distinguishing word、程序/原生 waveform 来源和 claim ceiling。此组合若在既定 S09/S10 预算内得到 fresh independent evidence，才值得进一步升级为前瞻性数学-物理命题。




### F132：从 single-coordinate sensitivity 走向 joint / block-intervention certificate

**亲读锚点**：[原始论文](literature/F132_sensitivity_block_sensitivity_separation.pdf)；[00 定义与策略](preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/00-introduction.tex)；[01 tournament gate 与 target-row 示意](preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/01-construction.tex)；[02 四组耦合递推](preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/02-recurrences.tex)；[03 量化分离与 composition](preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/03-separation.tex)；[Lean selected scope](literature/lean/F132_scope.md)。

论文对象严格是 total Boolean functions 的**全局** sensitivity \(s(f)=\max_x s(f,x)\) 和 disjoint block sensitivity \(\mathrm{bs}(f)=\max_x\mathrm{bs}(f,x)\)。其 construction 在 \(d\) 层的嵌套 predicates 上分别控制从零变一、从一变零的 single-bit sensitivity \(S_{\ell,0},S_{\ell,1}\)，还增加同一 bit 同时改变**两个不同 child predicates** 的 joint profiles \(J_{\ell,0},J_{\ell,1}\)。这是最该学的技术点：只递推单变量 sensitivity，无法闭合 recursive gate 的界；必须把 pair-change events 作为独立数学对象。论文用 tournament edge labels 限制一次 bit flip 能修复多少候选 clause；下界则构造大量 disjoint blocks 同时使目标行满足。得到 \(s(f)\le2(d+2)M^{d+1}\) 与 \(\mathrm{bs}(f,0)\ge M^2(2M^2+1)^d\)，从而 \(\mathrm{bs}/s^2\ge2^d/[4(d+2)^2]\)，最后经 disjoint composition 得固定指数 \(\alpha>2\)。

**转成 DPT 的正向动作**：同时审计（a）primitive/单参数扰动；（b）两项或多项干预共同出现时的 signed mixed contrast；（c）多个 readouts/stage predicates 是否在同一 waveform 上共同变化。尤其对 threshold 目标，例如 \(1\{\max_t V_{DS}(t)>V_{\rm lim}\}\)，局部连续灵敏度很小也可能存在边界跨越。**但 F132 的超二次指数依赖特定高维 Boolean tournament 递归，绝不构成 SiC 连续参数模型中的 sensor 数或 query 数下界**。真正适合低预算的替代是我们下面的 bounded mixed-contrast lemma，而不是迁移其指数。

最小 ordinary counterexample：\(F(\alpha,\beta)=\alpha\beta\) 在两条坐标轴上恒零，组合干预才出现响应；再考虑 \(F_2(\alpha,\beta)=\alpha\beta(\alpha-a_*)v(t)\)，即使 primitive 和既定一次 fusion \((a_*,b_*)\) 的**完整时间波形**都相同，别的 mixed command 仍能区分。由此一条 mixed query 的“极强反证”只在明确冻结的 quadratic/rational/regularity 类中成立。

### F122：trace alignment / erasure model 先于全波形 reconstruction 的复杂度

**亲读锚点**：[uniform reconstruction PDF](literature/F122-A_uniform_trace_reconstruction.pdf)、[main theorem 与假设](preprints/Uniform-quasipolynomial-time-trace-reconstruction-October-5-2026/build/manuscript/main.tex)、[positive moment arrays 与错误前缀 separation](preprints/Uniform-quasipolynomial-time-trace-reconstruction-October-5-2026/build/manuscript/setup.tex)、[analytical signal / exact generating identity](preprints/Uniform-quasipolynomial-time-trace-reconstruction-October-5-2026/build/manuscript/separation.tex)、[lower-bound companion](literature/F122-B_trace_reconstruction_lower_bound.pdf)、[Lean selected scope](literature/lean/F122_scope.md)。

这里的 input 是任意未知 length-\(n\) binary string，每个位独立以已知 retention probability \(p\) 保留；收到的 trace **没有原始 position labels**。uniform decoder 不是靠简单的 pairwise separation 直接恢复：先构造每个候选 prefix 的正半定 moment relaxation，把“任何错误前缀”变成可观测 trace statistics 上的 separation，再用高阶位置/间距 moments 与多尺度解析 continuation 限制最坏样本数。固定 \(p\) 的 upper bound 为 quasipolynomial；另一个 companion 给 exact worst-case full-string reconstruction 的 superpolynomial lower bound。**本次核对的 lean/docs/122.md 主要 formalize 下界，不能借它证明 October 5 uniform decoder 的每一行细节。**

**DPT 适用判断**：普通 LTspice 自适应时间步/插值属于带 timestamps 的数值重采样，和 unknown-location independent deletion channel 不同；不能从 F122 直接搬出 quasipolynomial sample cost。真正的可迁移动作是先区分已观察 waveform 的原始 time axis、clock jitter、事件区间、丢点/删点 mechanism，再问是否需要完整 trace recovery。若唯一目标是 \(V_{DS,\max}\) 或某个 timing threshold，可以先证直接的 goal-bound：在一个已完全覆盖、最大网格间隔 \(\Delta\) 的 C² 时间区间里，且 \(\|V''\|_\infty\le M_t\)，线性插值误差给
\[
0\le \max_t V(t)-\max_i V(t_i)\le M_t\Delta^2/8.
\]
这是 elementary interpolation theorem，**不是 F122 的定理**；若 event/discontinuity、stage crossing 或 curvature envelope 未被覆盖，这个证书立即失效。保留为“采样模型核验”触发项，zero-fresh 优先，不为 F122 单独占 S09/S10。

### F119：sharpen information loss, but only under its genuine binary-channel model

**来源**：[main theorem / soft-channel proof](preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/main.tex)、[Lean scope](literature/lean/F119_scope.md)。

F119 使用**独立均匀输入 bits**、独立同分布 binary-symmetric noise、预先指定且可随机化的 one-bit summary。主定理先固定 summary 原始 mutual information，再证明独立噪声后的保留信息不能超过一个合适幅度的单坐标软通道；Boolean 推论给经典形式 \(I(f(X);Y)\le1-h_2(\varepsilon)\) bits，输出 bias 时有更强上界。条件中 uniform cube、binary output、symmetric channel 缺一不可。

DPT switching latent 通常连续、有物理相关性，simulator discrepancy 未被标定为 independent BSC。这里可用的是 **channel-specific data-processing / information-retention gate**：若把 stage event 离散成 bits 并另外确证其 noise channel，才讨论此类 sharp rate。暂列 WATCH；不把 \(1-h_2(\varepsilon)\) 作为未标定 DPT 的信息预算。

### F325：fixed nonnormal stage 的 numerical-range upper envelope，及其更简单的强竞争者

**亲读锚点**：[direct proof](preprints/A-direct-proof-of-the-complete-Crouzeix-inequality-September-26-2026/build/main.tex)、[structural companion](preprints/The-complete-Crouzeix-theorem-September-23-2026/build/main.tex)、[Lean selected scope](literature/lean/F325_scope.md)。

若已真正冻结**同一个**复数矩阵 \(A\)（固定 linearized stage/generator），令 \(P(z)=\sum_{k=0}^d B_k z^k\) 为 matrix-coefficient polynomial，F325 给出
\[
\|P[A]\|_2=\left\|\sum_{k=0}^{d}A^k\otimes B_k\right\|_2
\le 2\max_{z\in W(A)}\|P(z)\|_2,\quad
W(A)=\{u^*Au:\|u\|_2=1\}.
\]
proof architecture 值得学的是 **positive double-layer resolvent + Faber coefficients + singular-vector compression**。论文先在包住数值域的 analytic convex domain 构造正核，比较 Fourier/系数范数；再分别对 \(FG\) 与 \(GF\) 保持 coefficient order，利用 resolvent Hermitian 部分正性产生 sharp 2；最后缩小 analytic domains，包含数值域退化为线段/点的情况。不能据此推出 arbitrary noncommutative products \(P(A,B)\) 的相同界。

**一个更具体、可计算的 DPT 警告**：\(A=\begin{psmallmatrix}-1&4\\0&-1\end{psmallmatrix}\)、\(t=0.25\) 时 eigenvalue-only 给 \(e^{-t}\approx0.7788\)，而 \(\|e^{At}\|_2\approx1.2601\)，说明稳定 eigenvalues 仍可伴随 transient growth。其数值域为以 \(-1\) 为圆心、半径 2 的 disk；Crouzeix analytic-function consequence 给 \(2e^{t}\approx2.5681\) 的 conservative envelope。但对**纯 \(e^{At}\) 的欧氏 2-norm**，经典 logarithmic norm
\[
\|e^{At}\|_2\le e^{t\lambda_{\max}((A+A^*)/2)}
=e^{t}\approx1.2840
\]
**更紧且更简单**。因此 F325 只在 stage 的 polynomial/rational **matrix-valued** readout、filter/surrogate 形成 load-bearing object，并且简单 matrix-measure/energy inequality 不够时，才值得升级。对 time-varying、switching、多矩阵有序乘积，须另做 domain 和 product proof。此处 numerical-range 例子是代数 illustration，不是已识别的 native SiC stage。




### S09 的新数学中心：一条 mixed query 的 information ceiling 与有界系数估计

这一节是**本项目独立的、明示 regularity/noise 假设的初等推导**；F132 提供单干预与组合干预分开的证明动机，F116-B 提供固定 query bank 与 original-domain definedness 的 proof style。它不是 OpenAI 已发表的 DPT theorem，更不能从 F116-B 的非交换有理**矩阵代入** hitting list 直接推出一组物理可执行的 scalar Rg/Lg queries。

**A. 模型阶数决定最低查询数。** 令已经完成的同 reference primitive axes 沿 \(\alpha=0,\beta=0\) 全部冻结，定义 waveform-valued mixed residual
\[
R(\alpha,\beta,t)=F(\alpha,\beta,t)-F(\alpha,0,t)-F(0,\beta,t)+F(0,0,t).
\]
在严格 quadratic class 中，\(R=\alpha\beta C_{11}(t)\)，所以任何一条 \(\alpha\beta\ne0\) 的匹配 fusion waveform 都能确定 \(C_{11}(t)\)（噪声精度另算）。但在 cubic mixed family 中
\[
R=\alpha\beta[C_{11}(t)+\alpha C_{21}(t)+\beta C_{12}(t)].
\]
每个固定 query \((a_i,b_i)\) 只提供一个 waveform-functional 线性组合。若这些三个 \(C_{jk}(t)\) 是**未知且可任意变化的函数**，即便每条 waveform 有无限多时间采样点，鉴别它们也需要 query coefficient matrix \([1,a_i,b_i]\) 的 rank 3。S09 加 optional S10 最多两个 mixed points，矩阵 rank 至多 2；除非冻结更小的 function class / shared known time templates 或额外独立 readout constraints，否则无法完整恢复三个未知函数。一个反例是 \(R=\alpha\beta(\alpha-a_*)v(t)\)：两条 primitive axes 与 frozen S09 \((a_*,b_*)\) 处的全波形均为零，中心混合系数却为 \(-a_*v(t)\)。

**B. 真实可用的非线性误差定理。** 对任一提前声明的 scalar goal/readout \(g(\alpha,\beta)\)，定义四角差
\[
D_{a,b}g=g(a,b)-g(a,0)-g(0,b)+g(0,0),\quad a b\ne0.
\]
在贯穿 0 到 \(a,b\) 的完整矩形上 \(g\in C^2\)，且
\[
|\partial_{\alpha\beta}g(u,v)-\partial_{\alpha\beta}g(0,0)|
\le M_\alpha|u|+M_\beta|v|,
\]
并且四角 readout 各自满足 absolute error \(\eta_{ab},\eta_{a0},\eta_{0b},\eta_{00}\)，则
\[
\boxed{\left|\frac{\widehat D_{a,b}g}{ab}-\partial_{\alpha\beta}g(0,0)\right|
\le \frac{M_\alpha|a|+M_\beta|b|}{2}
+\frac{\eta_{ab}+\eta_{a0}+\eta_{0b}+\eta_{00}}{|ab|}.}
\]
**证明**：对混合导数用二维微积分基本定理表达 \(D_{a,b}\) 的 signed double integral；取矩形平均，分别积分 \(|u|\) 与 \(|v|\) 给出半幅度系数；四角 readout 的各项 absolute error 由三角不等式相加。无需把独立样本假设强加到 noise；这些只是每个 absolute error 的 deterministic envelope。若未有可辩护的 \(M_\alpha,M_\beta,\eta_j\)，这仍只能作参数敏感性计算，不得写成 certificate。

**C. 为什么极小干预不一定最优。** 记 \(P=\sum_j\eta_j\)、\(r=M_\alpha/2\)、\(s=M_\beta/2\)。在 \(r,s,P>0\) 且无物理 amplitude/domain 约束时，minimize \(U(a,b)=r|a|+s|b|+P/|ab|\) 有正幅度极小值
\[
|a|_*=(P s/r^2)^{1/3},\quad |b|_*=(P r/s^2)^{1/3},
\quad U_* =3(P r s)^{1/3}.
\]
由对 \(a,b>0\) 的一阶导数条件 \(ra=sb=P/(ab)\) 得出；当 \(M_\alpha=M_\beta=M\) 且每角 error \(\eta_j=\eta\)，有 \(|a|_*=|b|_*=(8\eta/M)^{1/3}\)。真正选点必须在 **precommitted physical validity box、已有 matched primitive runs、采样分辨率与事件定义** 下搜索，不能直接使用无约束最优值。

**D. 科学决策与 falsifiers。**
- 首先判断 S09 是测试一个**冻结的 rival goal**，估一个 local \(C_{11}\)，还是想恢复任意 nonlinear command map；三者不应共用一种 PASS。
- 若有经过 freeze 的 cubic variation envelopes 与 readout error，报告一个 mixed coefficient 的 conditional interval；仅当 interval 排除零时，对此项给 bounded sign evidence。
- 若没有这些 envelopes，仍可以如实输出 measured mixed finite response \(D_{a,b}g\) 和其误差，而不把它叫中心导数。
- S10 应优先争取能够推翻 remaining rival 的**第二个模型特定预测**；在无其他结构下，两点仍不足以重构 generic cubic mixed class。
- 此处 noise 与 model discrepancy 不可混用。LTspice deterministic numerical tolerance 不给 physics discrepancy 的 automatic \(\eta\)；不同参数/不同 switching stage 引入 domain-switching 时，上述 \(C^2\) 假设可能不成立。
- **实现**：[mixed_interaction_audit.py](dpt_tools/mixed_interaction_audit.py)，输入四角 scalar readout、三阶控制系数与各角 absolute error；它做上述条件式 interval 和 predeclared amplitude-grid 查询设计，不从一次结果反向拟合这些系数。相关 synthetic tests：[test_mixed_interaction_audit.py](dpt_tools/test_mixed_interaction_audit.py)。

**Prior-work 桥接**：factorial interaction / confounding 本来就是成熟 DOE 主题（[NIST DOE handbook](https://www.itl.nist.gov/div898/handbook/pri/section3/pri3333.htm)、[Godolphin 2021](https://doi.org/10.1111/rssb.12397)）；面向 nonlinear goal 的 experimental design 也有 [Neuberger et al. (2024)](https://arxiv.org/abs/2411.07532) 与 [Zhong et al. (2026)](https://doi.org/10.1137/24M1649344)。因此 novelty 不在于 factorial interaction 或 goal-directed design 本身。DPT 可争取的具体增量是：**在只有 S09＋optional S10、物理 switching stage 和已存 waveform 的约束下，把目标歧义、可辨识系数类、噪声/曲率幅度最优性和独立前瞻性验证整合成一个有界、可证伪的预测结论。**



---

## 11. 现在可以形成的 DPT 数学链

把这些文献真正融合以后，最值得推进的是下面七层。它们是递进 gate，不要求全部在 IH2662 项目内完成。

### T1. Goal quotient

定义 history equivalence：

h1 ~_G h2 iff 对所有 c，G_c(h1)=G_c(h2)。

先解决“目标需要什么状态”，不追求完整 internal-state recovery。

### T2. Minimum local measurement

用独立 K/N lemma 给 goal-visible hidden dimension（F355 仅作为有限阶证明启发），并在明确局部 Lipschitz 因子或一阶模型假设下证明 reduced law 上的一维 repair 下界。候选 measurement 的第一道 gate 是：

ker(DP restricted to K) subseteq N。

### T2b. Bounded-noise scalar goal ambiguity

先声明 admissible histories、units/whitening、noise radius 和目标。直接在原始/派生 observation 的有限 history bank 找 `||Y(h)-Y(h')||<=2σ` 却具有大 goal gap 的 pair，输出确定性 minimax error 下界；它可决定应买哪个 feature/sensor，比只比较 raw sensitivity 更贴合目标。该 finite-bank 值不能当 operational continuous-class upper bound；完整类验证还需明确 domain 和统一误差边界。详见 F329 节和 goal_ambiguity_audit.py。

### T3. Multiscale finite-radius predictive chart

把 T2 从一个 center 扩到 frozen neighborhood / scales：

- goal-visible rank persistence；
- measurement row-space containment persistence；
- measurement-to-goal gain 不爆炸；
- nonlinear / directional remainder 有明确 envelope。

优先用简单 inverse/constant-rank theorem；需要更强 multiscale bootstrap 时，再借 F357 与 F365-B 的 proof architecture。没有 remainder/domain 证书时，只称 tangent sufficiency。

### T4. Stable approximate predictive dimension

不要只问 state dimension d。至少同时冻结：

- prediction tolerance epsilon；
- stability/gain budget kappa；
- admissible history class H；
- command family C。

把 finite-bank fitting 与 continuous operational-class representation 分开。F330 负责提醒“存在 approximant”与“存在 uniformly bounded approximant”不同；F094/F098 负责提醒 exact/approximate 与 finite/global complexity 也不同。

### T4b. Lipschitz extension is conditional

若全 class 上存在 G=Phi(Y) 且具有一致 finite Lipschitz gain，F332 的 Hilbert-to-ell1 extension theorem 才可能提供 ambient observation extension；finite-bank gain 仅是筛查。F324 进一步阻止从 metric accuracy 推 linear/physical latent identity。不得用“extension 存在”反向推出 identifiability。

### T5. Information lower bound + acquisition order

用独立 goal-packing lemma 给 state complexity 下界（F140 是严格条件下的 memory/sample 方法启发）；用 F229 的 dominance test 判断新 sensor/readout 是否真正增加信息。只有在 history/command class 真正冻结后才做复杂 information theorem。

### T5b. Future-word state congruence

对 finite partial deterministic command model，用所有 admissible future words 的 goal、definedness 与显式 stage outputs 来定义等价类。该最粗 equivalence 为 right congruence，能形成可更新的 reduced state；两条 primitive endpoint 相同的历史仍可能被 AB/BA 或 within-stage event 区分。command_word_audit.py 只在提交的有限模型上验证，不等于 native waveform guarantee。

### T6. Command algebra + domain + correction boundary

把 primitive / mixed / ordered commands 放进同一 representation：

- primitive A, B；
- simultaneous mixed coefficient C_AB；
- sequential AB, BA；
- composite rational maps。

每个 inverse occurrence 单独记录 definedness。F116 管 expression-path domain；若要从 small composition defect 升级到 exact algebra，再用 F251/F289 作为 correction/structural-equivalence guard，而不是自动升级 claim。

### T7. Certificate-grade native bridge

用 F266 的结构给每个 load-bearing numerical claim 一个 certificate object，并把 simulator provenance 分开保存。certificate 至少应携带 center、basis/projector、rank tolerance、domain、remainder、gain、readout/operator bound 与 provenance。


---

## 12. S09 / optional S10：当前最有信息效率的解释

### S09

若 frozen quadratic class 为：

F(α,β)=F0+αL_A+βL_B+α²D_A+β²D_B+αβC_AB

primitive axes 无法确定 C_AB。

因此 S09 fusion 的角色不是“再跑一个 pulse”，而是：

> **第一次直接 acquisition 一个 primitive characterization 无法推出的 mixed functional。**

这仍然是当前最合理的 fresh query，但一次有限幅度 fusion 还不足以识别中心的 mixed Taylor coefficient。对矩形上 C² 的 F，mixed finite difference D_AB F(a,b) 等于从 0 到 a、0 到 b 的混合二阶导数积分，所以 D_AB/(ab) 是矩形平均导数；只有严格 quadratic class 或额外导数变化界才能称它为中心 C_AB。

### S09 后再决定 S10 时，按这个顺序

1. **先做 F229 dominance check**：候选 S10 是否真的新增 physical information，还是 S09/已有 waveform 的 post-processing？
2. **看 remaining K/N**：还有哪个 goal-visible direction 没被当前 observations 切开？
3. **看 command-word residual**：simultaneous mixed 已解决后，AB vs BA 是否成为最小新方向？
4. **先做 mixed-class/uncertainty gate**：现有一条 fusion 究竟是严格 quadratic 的系数测试、带 remainder 的区间，还是普通 finite mixed response？剩余 cubic interaction 自由度可否通过 S10 消掉？
5. **看 within-command event**：相同 endpoint 的 VDS peak、stage-boundary crossing 是否已被同一 waveform 区分？
6. **看 adaptation 身份**：如果 S10 是看到 S09 后才挑的，明确记录为 adaptive follow-up，不再包装成同等级 prospective test。
7. 若没有一个 query 能明显改变 theorem / representation / rival set，S10 不必使用。

---

## 13. 主控的九个固定问题

以后每次有新 idea，先过这九个问题。这样比继续增加文献摘要更有用。

1. **Goal**：它解决的是哪个 future goal？换 goal 后结论还成立吗？
2. **Fiber**：当前 observation fiber 上是否存在 goal-distinct histories？
3. **Information**：新 measurement 真增加信息，还是已有 observation 的 post-processing？
4. **Domain**：所有 rational/inverse intermediate states 是否都 defined？
5. **Local-to-finite / mixed model**：现在只有 Jacobian/rank，还是已有 finite-radius remainder guarantee？S09 所估的是 finite mixed response、严格 quadratic 系数，还是带明确 C² variation/noise envelope 的系数区间？
6. **Physical-to-auxiliary**：从 physical waveform 推 auxiliary state 时，injectivity 是否真的证明？
7. **Certificate**：承重 numerical claim 是否有 center defect、tangent defect、remainder、domain 和 provenance？
8. **Stability**：低维 representation 的 gain / condition number 是否在 frozen neighborhood 与 scales 内有界，还是只在某个 finite bank 上能 fit？
9. **Structure**：当前证据只是 one-sided trajectory approximation / small composition defect，还是已经有 reciprocal control 或 explicit correction theorem？

任何 idea 如果九个问题里没有一个答案发生变化，通常不值得占 fresh simulation budget。

---

## 14. 主控调用文献的最小 bundle

不要把整个 OpenAI Math 论文集一次性交给模型。

### P2 / minimum measurement

- Pro17D relevant derivation
- F355 linear / finite-observation sections
- F365-B local-extension proof architecture
- F140 information comparison
- reachable-pair evidence

目标：证明 K/N 下界，并判断能否从 tangent sufficiency 升到 finite-radius sufficiency。

### Command algebra / S09-S10

- F116-A formula-system / iterated-integral sections
- F116-B encoding / rank
- frozen primitive and fusion definitions
- current command matrices

目标：定义 missing mixed/ordered functional，并做 inverse-occurrence definedness audit。

### Acquisition pruning

- F229 foundations + finite experiment section
- candidate sensor/readout map
- existing observations

目标：建立 measurement dominance / redundancy map，剪掉不增加独立信息的 acquisition。

### Numerical certificate

- F266 Root / refinement / execution sections
- exact derivations
- simulator/model hashes
- scorer and numerical margins

目标：生成 reusable DPT certificate object，而不是更多 residual screenshots。

### Identifiability boundary

- F365-A/B/C
- F372
- explicit DPT model class / regularity / allowed symmetry

目标：检查 claim 究竟是 quotient uniqueness、finite sufficiency 还是 stable reconstruction。


### Stable predictive representation

- F357 introduction + directional pinching
- F330 obstruction / operator sections
- F094/F098 dimension-reduction statements
- frozen multiscale Jacobians、candidate measurements、remainder bounds

目标：把“低维”拆成 dimension + error + gain + scope，判断 finite-bank success 是否真的支持 finite-radius / operational-class predictor。

### Approximate algebra / surrogate equivalence escalation

- F116 expression tree + domain certificate
- F251 Strong Ulam companion
- F289 strong two-sided stability + one-sided boundary companion
- current primitive / fusion / ordered command residuals

目标：只在 approximate algebra 或 surrogate structural-equivalence claim 真正承重时，判断是否需要 correction theorem；否则停留在 bounded approximate statement。


---

## 15. 什么时候不要继续挖这条数学线

保持 bounded programme 很重要。

- F140：如果 admissible history class 还没冻结，不做复杂 entropy theorem；先用 elementary packing。
- F355：如果 native preparation interface 还不能生成 independent hidden directions，不把 numerical rank 当 native theorem。
- F116-B：如果 DPT command map 不能诚实写成 bounded rational / matrix class，不追 universal hitting-list theorem。
- F229：没有 probabilistic/noise experiment model时，只用 dominance / data-processing logic，不写 Blackwell-theory headline。
- F365-B：如果 inverse-function theorem 已足够给 finite-radius result，不复制 PDE 的 shrinking-sphere machinery。
- F357：没有 multiscale neighborhood data 或 certified remainder 时，不把单点 Jacobian 成功包装成 bi-Lipschitz-like predictive chart。
- F330/F094/F098：如果 operational history/command class 还没冻结，不从 finite-bank fit 推 global/continuous low-dimensional representation。
- F251/F289：只有 approximate command algebra 或 surrogate structural-equivalence claim 真正承重时才打开；普通 waveform fit 不需要上升到 operator-algebra correction。
- F325：只有 fixed nonnormal propagator / polynomial 或 rational functional 真正承重时才打开；对纯指数半群的欧氏范数先试经典 logarithmic-norm bound。
- F132：不能把 Boolean block-sensitivity 的全局超二次分离当作连续 DPT 的 query-complexity 定理；只迁移 coupled/joint intervention proof pattern。
- F122：若原始 waveform 有精确 timestamps、并未经历未知位置的独立 deletion channel，禁止搬用 trace-reconstruction sample-complexity theorem。
- F119：若没有独立均匀 bits 与已标定 symmetric flip channel，不使用它的 sharp mutual-information 数值下界。
- F363/F129：分别作为 uniqueness claim guard 与 discrete-state lower-bound reserve，不主动占 fresh simulation budget。

---

## 16. 当前优先级

如果只允许主控再投入三块高强度数学工作：

**第一：F355 + F357 + F365-B**  
把一维 charge repair 推成“minimum measurement + multiscale finite-radius local sufficiency”。优先交付一个能被 prospective evidence falsify 的 local theorem，而不是继续加抽象。

**第二：F116-A/B**  
把 command algebra 补上 ordered interaction 和 inverse-occurrence definedness certificate，并给 S09/S10 一个真正的 acquisition basis。F251/F289 只在要把 approximate algebra 升级成 exact/structural claim 时触发。

**第三：F140 + F229 + F330 + F094/F098**  
把“多少信息是必要的”“哪个 measurement 真新增信息”“低维 predictor 是否稳定可部署”放进同一个 dimension-error-gain-scope 框架。

**本轮优先**：在 S09 query 被 freeze 前，先用新 mixed-interaction envelope 判断一条 fusion 能兑现的 theorem scope（严格二次、带三阶余项的区间、或仅 finite mixed response），并检查物理可行的 amplitude/noise trade-off；这项检查优先于再增加理论名称。F132 提醒不能从 primitive sensitivity 推出组合干预无效，F122 只在真实 trace deletion/alignment 模型出现时触发。F332 的 extension 和 F324 的 nonlinear-linear boundary 只在稳定目标状态/解释主张承重时启用；F329 的 primal noise ambiguity + F376 的 future word discriminator 则优先在 **zero-fresh archive** 上执行。F266 继续作为所有承重 numerical work 的固定证据层并行执行。F325 在 fixed nonnormal propagator 出现时即时启用，不单独开理论线。


---

## 17. 主控可直接运行的审计工具

图谱现有多项轻量 mechanical auditor。它们的角色是把容易在口头推理里滑过去的条件固定成可复查 JSON；**PASS 只代表对应 numerical/algebraic condition 通过，不自动升级 scientific claim。**

### goal-visible measurement / multiscale audit

- [`predictive_state_audit.py`](dpt_tools/predictive_state_audit.py)
- [使用说明](dpt_tools/README.md)

输入 `DO`、`DG` 与可选 `DP` 后，它直接计算：

- `K = ker(DO)`；
- `r_G = rank(DG|K) = dim(K/N)`；
- scalar measurement 下界 `k >= r_G`；
- `ker(DP|K) subseteq ker(DG|K)` 的 numerical row-space test；
- measurement-to-goal minimum-norm linear factor 及其 2-norm gain；
- candidate sensor rows 的小规模 exact subset search + greedy fallback；
- 若提供 scale-indexed Jacobians，则逐尺度重复上述 audit；
- 原版 (C_G + ||A|| C_P) r² 只在受限 tangent/fiber 特殊条件下可用，不能作为任意状态扰动的 general bound。新方案须使用 DG = B DO + A DP + E，并计入 observation remainder C_O、linear residual E 和噪声增益。

它故意把 claim ceiling 写进输出：rank PASS 仍只是 tangent statement；remainder coefficient 的真实性必须由 derivation / interval / native evidence 单独保证。

### additional bounded goal / command / factor audits

- [mixed_interaction_audit.py](dpt_tools/mixed_interaction_audit.py)：对匹配四角的一个 scalar goal 计算 mixed finite difference、中心混合导数的**条件式误差区间**及预先限制的 query amplitude grid；其 zero exclusion 只在给定 C² variation/noise/domain 假设被另行证实后有 scientific force。

- [goal_ambiguity_audit.py](dpt_tools/goal_ambiguity_audit.py)：在有限 bank 上计算 scalar minimax ambiguity、最危险 indistinguishable pair、已有 feature 与新增 scalar candidate 的对比，以及 empirical scalar Lipschitz gain。输入必须先统一 observation 单位与 noise radius。
- [command_word_audit.py](dpt_tools/command_word_audit.py)：在有限 partial deterministic 模型上生成最粗 future-word congruence，并给 primitive alias 的最短 word / stage output witness；stage information 只取自显式输入。
- [measurement_factor_audit.py](dpt_tools/measurement_factor_audit.py)：报告 DG=B DO+A DP+E 和条件式 all-direction bound；缺少任何 O/P/G remainder 时不输出 quadratic bound。
- [expression_domain_inventory.py](dpt_tools/expression_domain_inventory.py)：为 original AST 标识每个 inverse occurrence 的独立 path；必须区分 undefined、numerically ill-conditioned 和由于前一个错误未曾检查的 occurrence。

这些是 **synthetic / finite-bank auditable statements**。尚未提供 DPT-R1 native S09/S10 replay 输入，不产生 LTspice prospective claim；参见 [详细使用说明](dpt_tools/README.md)。

### rational / matrix command-domain audit

- [`command_domain_audit.py`](dpt_tools/command_domain_audit.py)

这个工具按原 expression tree 逐个记录 `inv` occurrence，在 supplied command samples 上报告 smallest singular value、condition number 和 undefined samples。它不会先把表达式化简后再检查，因此能直接执行 F116-B 的原则：

> definedness 属于原 expression path；后续 cancellation 不能替一个 undefined intermediate inverse 洗白。

sampled PASS 仍不等于 continuous-domain closure。若要把它升级成 theorem，需要对每个 inverse occurrence 给 analytic / interval / optimization lower bound。

### tests 与下一步 Lean target

- [test_frontier_tools.py](dpt_tools/test_frontier_tools.py) 新增 bounded-noise minimax、archived-feature reuse、two-command witness、within-command event、observation-curvature correction、inverse occurrence inventory 的 synthetic regression tests。

- [`test_dpt_tools.py`](dpt_tools/test_dpt_tools.py) 提供 synthetic regression cases，包括“一维 repair 成功”“mixed measurement 看似有投影但仍不足”“两个 mixed rows 才能共同 repair”以及“中间 inverse undefined 即失败”。
- 下一步最值得 formalize 的 Lean statement 不是整套 DPT physics，而是一个小而承重的 finite-dimensional lemma：若 `ker(M|K) subseteq ker(G|K)`，则 `G|K` factor through `M|K`，从而 `rank(G|K) <= rank(M|K) <= number of scalar measurements`。等 native state/goal maps 冻结后再把这个 lemma 接到项目对象，避免过早 formalize 一个仍在移动的 abstraction。


---

## 18. 维护规则

以后只有在文献改变下面至少一项时，才更新这份 map：

- scientific object；
- theorem assumption；
- lower/upper bound；
- measurement choice；
- falsifier；
- certificate；
- claim ceiling。

“读过”“很像”“可以引用”都不算 materially used。

当前最值得争取的最终结构仍是：

> **finite predictive quotient  
> + minimum goal-visible measurement  
> + multiscale finite-radius sufficiency  
> + stable approximate representation（dimension / error / gain / scope）  
> + predictive information lower bound  
> + mixed/ordered command acquisition  
> + certificate-grade native validation**

但现在每一项的来源、触发条件和失败边界已经更清楚。主控下一步应该优先把其中一项做成真正的新 theorem 或 prospective discriminator，而不是继续扩充方法名词。
