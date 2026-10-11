# DPT-R1 × OpenAI Math：成果利用与下一数学问题

更新：2026-10-11。覆盖本地已接受的 Pro18A/B/C 及其后续定向复算；尚在建设的证书只记为未决对象。

OpenAI Math 对 DPT 的主要贡献，已经从“提示如何检查信息不足”发展到三个可计算对象：**同一可达类上的信息下界与观测修复上界、主动多阶段命令中的历史反例、主动校准后的目标预测**。下一步最值得攻的是把这些对象接成有限域、多阶段的可靠预测结构，同时回接原始有效换流电感问题。

本页服务 Math side 的选题和复用。DPT 科学 authority 仍由本地 accepted evidence 拥有；这里记录使用后果，不替代冻结评分。原来的长篇阅读展开可从 [Git 历史](https://github.com/Gogoal-L/math/commits/main/DPT_MATH_RESEARCH_MAP.md) 找回，专题推导继续保留在 [dpt_research](dpt_research/)。

## 1. 从原预期到实际成果

Pro17C/D/E 提供了 actual coupled law、ordered-command forecast、有限更新与 source-derived 信息修复的执行基础。S09 随后建立同模型 native 对照、goal-dependent model reversal，以及强 affine / one-Newton 的竞争条件。18A/B/C 分别推进证明、动态反例和主动辨识；原始 R1 的观测受限恢复仍有独立证据义务。

| 单元 | 原来希望解决什么 | 已获得的实际增量 | 当前证据域与剩余问题 |
| --- | --- | --- | --- |
| **18A：可达信息与修复** | 将近匹配历史推进到合法 Q-fiber；补齐 preparation 误差传播 | 同一个 actual50 离散系统中，126 步 preparation＋128 步后续 hold 的 **254 步联合证书**；精确有理 Q-fiber 与合法域包含；预测前外部 VDS 读出提供更小的统一目标误差上界 | 声明初态、参数族、hold 分支和离散 law 内的条件结论。完整数字 command 三幅值可恢复该历史方向，是必须保留的强 ordinary；电压修复并非对所有输入预算都必要 |
| **18B：目标相关动态闭合** | 静态摘要是否能在后续 command 中继续支持目标预测 | 150 V 主动两阶段 actual-law 历史对产生 work、peak、事件差；有限 F4 类内构造 memory 修复。未见成员与细化 preparation 后重新 shooting **实际击穿原预测律的推广** | 有限 source 见证与已兑现 falsifier。当前坐标更新缺陷、目标差异和最小可取得 repair 尚未统一闭合；28-state 实现不是最小状态定理 |
| **18C：主动 CAL→未来目标** | 观测不到的本构方向是否妨碍未来预测；主动测量能否修复 | 150 V 同一 reference 中，关断不可见的 κ 方向在主动未来产生 work 差异；最终五点非线性 CAL chart 支持 12-member bank 预测；L 不唯一而特定未来目标相对稳定 | 有限 bank、局部证书与条件测量结论。完整 active preparation→CAL / future 的关联余项界仍未知；100、150、600 V 尚无同一物理验证链 |

### 18A：已兑现的严格信息改善

在声明的离散可达族和目标中，本地重放得到：

$$
R_{Q\text{-only}}\ge 2.2864273\ \mu\mathrm V,\qquad
R_{Q+V}\le 0.68783535+1.06041884\,\varepsilon_V\quad(\mu\mathrm V).
$$

这里 $\varepsilon_V$ 的数值以 µV 表示。若 $\varepsilon_V<1.50750997\ \mu\mathrm V$，增加预测前电压读出后的统一上界严格小于 Q-only 的不可避免误差下界。

这实现了“信息不足的合法见证＋有限信息修复”。输入合同同时改变修复的必要性：若完整 preparation command 已记录，Q 加第三幅值即可反演相关方向，无需新增传感器。µV 门槛是这个任务的条件数学预算，实际仪器可实现性尚未资格化。

### 18B：动态反例更扎实，修复推广受到实际攻击

- 原有限 F4 类：C2 peak 的 current-only 误差下界约 **1.300865 V**；memory quadratic 的条件上界为 **0.031606 V＋324.628·εm**，εm 以 V 表示。有限类上界与声明噪声合同绑定。
- 已冻结的第二未见成员 $s=-12/7$：quadratic 扩展 **5/9 项未过**。这是已评分的 source falsifier，不能用重新拟合抹去。
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
| [F374：Brenier stability](literature_archive/F374_Brenier_one_third_stability.pdf)，Prop.5.1，Eqs.(5.5–5.6) | C 追求直接约束目标 functional，避免先恢复全部不适定参数；A/B 未建立 OT 假设 | **C 证明结构启发。** 不迁移 $1/3$ 指数或 Wasserstein 常数。下一价值是 goal-sensitive compatible set，不是完整状态距离 |
| [F125：metric k-median recovery](literature/F125_metric_k_median_recovery.pdf)，Thm.1.1 | B 实际拒绝用曝光后的赢家划分构造“少量例外＋廉价主体”选择器；C 保持 PARK | **边界作用；DPT 正向 mapping 尚未完成。** 只有预测前特征能识别例外域，才值得发展廉价 ordinary＋少量补信息路线 |
| [F116-A](literature/F116-A_noncommutative_hitting_point.pdf) / [F116-B](literature/F116-B_rational_hitting_lists.pdf)，定义域与 hitting assumptions | Pro17/S09 对 ordered command、表达式 definedness、原 law 与替代实现的身份检查；A 检查实际 exp/clip 系统后拒绝 rational universal-hitting 迁移 | **前期构造＋边界作用。** 新 native ordered positives 属于 DPT 自身；不宣称 vendor map 满足自由矩阵定理 |
| F365-A/B/C、F372：观测 quotient、nonlinear lift 与物理辅助对象 | source derivative、合法观测、局部 lift、有限半径证明义务进入 S09 的 K/Q 信息修复；后续由 A 的 exact fiber、B 的动态反例、C 的非线性 chart 推进 | **方法已吸收。** PDE/gauge/elasticity 原定理不直接证明 DPT identifiability；继续用实际 reachable chart 与观测合同 |
| F329、F355：直接 ambiguity 与有限阶 obstruction | 形成有限 bank/fiber 下界和 $K=DG\,DF\,DP$ 的信息分解；A/C 将部分问题推进到实际构造 | **独立 DPT 引理与构造。** scalar fiber 的半直径下界、K/N 线性代数不是原论文的新定理；不能由一个 scalar 失败推出所有一维表示失败 |
| F140：memory/precision 信息预算 | 区分 acquired waveform、retained summary、完整数字 command、内部 oracle 与新传感器；A 的 recorded-command rival 明确改变“最低新增信息”的判断 | **预算与边界作用已兑现。** 无 DPT Gaussian sample/bit 下界；数字压缩不自动减少 ADC 采样 |
| F332、F324、F094、F098 及 F049/F149/F360 | 强化坐标、延拓、维数、正则性和可达域的适用条件检查 | **保留专题阅读，暂非 ABC 承重计算。** 没有新的实际输入或可计算后果时 PARK；[F049/F149/F360 原文审计](dpt_research/20261010_F049_F149_F360_fulltext_proof_audit.md) |
| F175/F139 等 cover/query 方向 | 对最小额外信息、误差容限和查询代价提供候选结构 | **候选。** 原概率/oracle 前提不直接给出 DPT sensor-optimality 或 solver-budget 结论；见 [repair-cover 笔记](dpt_research/20261010_goal_tolerance_repair_cover.md) |

上述 ABC locator 对应各自 source ledger 中实际使用的 supplied version；不自动代表最新上游修订。每篇的 acquisition、版本与具体阅读深度继续归 [literature registry](literature/registry.json)。本次是实际用途同步，没有将全部旧文献标成二次全文精读；外部论文的撤回、修订和 selected Lean scope 仍需按实际承重版本核对。

## 3. Math 代码：已用的对象与尚未接通的实现

[工具入口与输入合同](dpt_tools/README.md) 给出完整 API。本次核对 A/B/C source ledger、吸收记录和本地接口，**未确认以下 Math 仓库模块被直接 import 并在真实 DPT 输入上完成 replay**。已确认的是本地等价对象的使用；两者分开记录。

| Math 实现 | 本地已经用了什么、效果如何 | 代码利用状态与最小下一输入 |
| --- | --- | --- |
| [predictive_state_audit](dpt_tools/predictive_state_audit.py)、[measurement_factor_audit](dpt_tools/measurement_factor_audit.py) | source-derived K/Q、$DG=B\,DO+A\,DQ+E$ 与信息余项；S09 局部修复、A 的 exact fiber、C 的非线性 chart 均有实际后果 | **本地构造已用；仓库模块直接重放未确认。** 可用同域 DO/DQ/DG、单位缩放及可信二阶常数对照；旧 bound 修订已要求保留 O 的余项 |
| [goal_ambiguity_audit](dpt_tools/goal_ambiguity_audit.py)、[goal_repair_cover](dpt_tools/goal_repair_cover.py) | A 实际信息下界；B 有限 F4 下界；Cal 已检查 C 合法测量子盒相交 | **独立实际实现已用；cover 的 DPT 最优采集结论未形成。** 输入应为合法 nuisance 集合，带单位、共同误差相关性、goal 求值误差及采集成本 |
| [goal_lipschitz_stability](dpt_tools/goal_lipschitz_stability.py) | B 已有重新 shooting 的 current/next 与 future-goal 见证；C 有有限近等观测成员 | **可直接接入的候选，尚无实际 replay。** 计算有限 bank 的 gain–error 曲线及 transition-pair 必要误差下界；有限类成功不能晋升连续动态闭合 |
| [implicit_goal_certificate](dpt_tools/implicit_goal_certificate.py)、[goal_defect_transport](dpt_tools/goal_defect_transport.py) | A/S10 的 actual-law residual、Jacobian/adjoint 与 signed goal correction；同网格 Full/N2 比较区分内部求解差与 native discrepancy | **本地 source 功能已用；仓库模块直接重放未确认。** 需要实际 inverse/remainder 常数，或声明的线性 chart；修正内部 source 误差不保证改善 native 目标 |
| [fiber_curvature_audit](dpt_tools/fiber_curvature_audit.py)、[stage_box_reachability](dpt_tools/stage_box_reachability.py) | A 用联合平方系统证书；B 实际重新 shooting；C 当前攻相关 active fork/tube | **实际问题已落地；工具需要真实连续域 bound。** 独立盒过松时应保留跨步相关性；INCONCLUSIVE 不等于 law 失败 |
| [goal_word_quotient](dpt_tools/goal_word_quotient.py)、[command_word_audit](dpt_tools/command_word_audit.py) | B 已按合法 BE update、阶段输出与目标定义动态反例；Pro17/S09 已运行 ordered commands | **语义已用；linear all-word theorem 尚未绑定 nonlinear actual law。** 先交付同 reference 的 goal-relevant transition/future pairs，不把坐标失败直接当目标失败 |
| [mixed_interaction_audit](dpt_tools/mixed_interaction_audit.py)、domain/definedness 工具 | B+C 联合 history/L/κ/sensor 正在建设；真实 law 的 branch/guard 在本地检查 | **定向候选。** joint interaction 需合法参数矩形及实际统一余项；expression inventory 只检查表达式身份，不证明物理可达性 |

本地可复用实现归 canonical source evaluator、已有 acceptance consumer 与 derivations，不复制一整套 Math engine。仓库 synthetic tests 只证明工具自己的合同；本次没有将它们计作 DPT 实验或重新运行全部工具测试。

### 三条共用计算关系

1. **合法观测相容对给下界。** 在声明误差集合内，两条可达历史允许同一观测，则仅使用该信息的 scalar-goal 预测器最坏误差至少为目标间隔的一半。source 目标存在求值误差时，要先扣除两端的误差上界。有限 bank 见证给整个类的下界，不给整个类的上界。
2. **有限域修复给上界。** 固定中心和系数，令 $f=g-BO-AQ$。若合法半径内确有 $\|D^2f\|\le M$，则
   $$
   |\Delta g-B\Delta O-A\Delta Q|
   \le \|E\|r+\tfrac12Mr^2+\|B\|\varepsilon_{\Delta O}
        +\|A\|\varepsilon_{\Delta Q}+\eta_{\rm evaluation}.
   $$
   关键建设对象是合法域、统一 M、初态/事件传播和摘要取得方式，不是 Taylor 公式本身。
3. **目标投影决定求解精度的价值。** 同一离散 law、正号伴随约定下，
   $$
   G(X^\star)-G(\widehat X)\approx-\sum_n\lambda_n^\top R_n(\widehat X).
   $$
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


## 6. 2026-10-11：连续域目标信息半径（新 Math-only 桥梁）

**增量：** [完整推导、反例和新增论文审计](dpt_research/20261011_continuous_goal_information_bridge.md)；[连续信息半径 NumPy 计算器](dpt_tools/goal_ellipsoid_recovery.py)；[解析/CLI 测试](dpt_tools/test_goal_ellipsoid_recovery.py)。这是对已有 finite-bank fiber / repair-cover 的补充：在**整个中心椭球合法**、具有**确定性联合相关测量误差**的同一线性 chart 上，给定未来 scalar engineering goal，直接计算其 global minimax 风险和达到该风险的外部读数线性解码器。

设 \(x=x_0+Bz,\|z\|\le1;\ y=Hx+Ee,\|e\|\le1;\ G=G_0+g^\top Bz\)。当 \(E\) 非奇异且全部信息来自同一合法模型/准备域时，令 \(A=E^{-1}HB,c=B^\top g\)，则
\[
R=\max_{\|z\|\le1,\|Az\|\le1}|c^\top z|
=\min_w(\|c-A^\top w\|+\|w\|)
=\sqrt{\min_{q\in[0,1]}c^\top[(1-q)I+qA^\top A]^{-1}c}.
\]
**此数学定理属于 prior art**：Foucart–Liao, *Journal of Complexity* 83 (2024), 101841，[DOI](https://doi.org/10.1016/j.jco.2024.101841)。本仓库成果是可执行的 DPT 信息/goal 接口，不是新的最优恢复定理或物理精度证明。合成例中，使用同一单通道观测，可观测目标半径 0.2，未观测目标半径 1；parameter nonuniqueness 与 goal predictability 可分开检验。工具的 witness/dual gap 是浮点诊断，不替代 verified interval 或 source-native validation。

**新增 OpenAI Math 原文阅读（限定范围）：** [F132](https://github.com/openai/math/blob/main/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/02-recurrences.tex) individual/block sensitivity 可启发合法成组干预（DPT 已有 mixed_interaction_audit；其 Boolean exponent 不可迁移）；[F129](https://github.com/openai/math/blob/main/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/build/sections/rank.tex) full relation-monoid / future-context lower bound 不构成 SiC nonlinear memory dimension 定理；[F119](https://github.com/openai/math/blob/main/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/main.tex) 的独立 Boolean-noise mutual information 也不能当作 correlated deterministic DPT sensor information budget。三者分别为 TEST-DESIGN ANALOGY、PARK、REJECT FOR CURRENT GATE。

**最小接入/证伪：** 本地主控提供一个**150-V Pro18C 同 reference** 的真实 source-legal state/parameter 域、预目标观测导数 H、完整确定性误差 E、未来 work 导数 g、非线性 remainder、冻结 ordinary 对手与一个 prospective CAL。计算保留原信息预算时 NO_CAL 与 CAL 的 target 半径，并用实际合法近匹配历史检验上下界。100-V scalar R1、150-V active CAL 和 600-V native 各有自己的 reference，不拼成一个物理保证；18B 的跨阶段历史更新另需 dynamic closure。**目前只有 synthetic testing，没有仓库模块对真实 DPT 输入的 native replay，也没有科学晋升。**
