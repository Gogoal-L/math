# DPT-R1 × OpenAI Math：Research Transfer Map

**更新：2026-10-12。** 本页是 DPT 主控和 Math Side 的双向科研接口。它回答：**Main 已吸收什么，Side 又推进了什么新的可吸收结果，下一项实际证据怎样改变判断。** 完整证明在 [dpt_research](dpt_research/)，代码/输入合同在 [dpt_tools](dpt_tools/README.md)，此处保留科研决策必需的结果、状态、界限与可执行接入路径。

**当前判断。** Main 已记录 Pro18A 的可达信息证书与观测修复、Pro18B 的主动两阶段历史反例及外推失败、Pro18C 的 active CAL 与目标预测。Side 进一步形成目标相关 minimax recovery、shared-nuisance quotient、有限历史消息比特预算、重复采集的共享漂移信息下界、跨传感器未知相关性的可辨识界、二次目标 Gq/相关模型误差下的 acquisition 排序、非线性 observation-fiber Hessian、source-law Hessian/charge bounds 的独立数学结构。**这批 Math 仓库模块在真实 DPT 输入上直接 replay 尚未确认；不能凭 synthetic tests 把它们自动标为 Main 已接受。**

## 0. 两条证据账本与更新规则

| 证据身份 | 判据 | 不能替代什么 |
| --- | --- | --- |
| **MAIN_ACCEPTED** | 本地 DPT 主控具有具名 accepted/absorption 记录、模型参考、实际输出和 claim boundary；本页据现有记录同步 | Side 在本仓库自行作出的状态改变 |
| **SIDE_VERIFIED** | 数学命题证明、反例或合成验证在明确的数学输入域内成立 | 真实 SiC source、sensor qualification、native experiment |
| **READY_FOR_HANDOFF** | 所需实际输入、可运行工具、冻结 scorer、决定性验收结果均能指给主控 | 主控已经运行工具或接受结论 |
| **OPEN_RESEARCH** | 缺合法物理状态域、关联 remainder、一致误差界、下一预测或反例 | 因无法形成证明就否认已经得到的有限正例 |

**一个结果允许同时有 SIDE_VERIFIED 和 READY_FOR_HANDOFF；MAIN_ACCEPTED 属于不同轴。** 每条新成果必须给出 object / theorem / adversary / source identity / test / smallest main input / expected verdict delta。Main 消费后只登记新实际 evidence 与 acceptance locator，不能把“Side 已读论文”“代码通过 CI”直接升级为 source-law 定理。失败、强 ordinary 获胜、INCONCLUSIVE 和尚无 replay 同样保留。

## 1. Main 已吸收或记录的 DPT 结果（Main → Side）

以下来源于本地 DPT acceptance/closure 与已有 MAP 的同步结果；Math 仓库未独立重放这些本地 source archive。所有数值只属于各自声明 reference、preparation、operator、window、command、numerical path 和 goal。

| 已有对象 | 主控已取得的决策性证据 | 交给 Math Side 的实际问题 |
| --- | --- | --- |
| **原始 R1 / S01–S06** | C3M0075120K 有审计的 ports、one-dimensional effective loop target、局部 response/profile、已知 ΔL 与 path/common-mode validity 压力；完整 scalar composite gate 仍需独立证据 | 100 V 的 L/Rser/gain 相容集合哪些方向支持 external goal prediction？不能把拟合量直接命名为 PCB/package 几何参数 |
| **S09 / Pro17 预测链** | 同 native family 出现 goal-dependent full/affine 排序反转；有限 nonlinear law、one-Newton 与 ordered command 有各自 positive 和强 ordinary rival | 先冻结预测前可见信息和目标；分清 waveform、fixed projection、stage work、full-event peak、solver 与 native discrepancy |
| **Pro18A — MAIN_ACCEPTED（按本地吸收记录）** | 126-step preparation＋128-step hold，合计 **254-step** actual50 joint certificate；Q-only minimax lower **2.2864273 µV**，Q＋预测前 VDS readout upper **0.68783535＋1.06041884 εV µV**（εV 用 µV），故当 εV < **1.50750997 µV** 时有严格信息改善 | 加入 sensor 前先测试 full recorded-command ordinary：完整数字命令附带第三幅值可反演相关历史方向；所需物理测量误差预算尚未资格化 |
| **Pro18B — MAIN_ACCEPTED（按本地吸收记录）** | 150 V actual-law 主动历史对，经 refinement/re-shoot 达到 near-alias；未来 C2 peak 差 **2.586995 V**；旧 memory/direct quadratic/cubic 在新增匹配对上 **7/9** 项未过；阶段 work 约 **＋1.628664/−1.686273 µJ**，总差 **−57.609755 nJ** | current summary、recursive update 和 future goal 必须分开检验；finite F4 上 total-work constant ordinary 可有约 **28.785842 nJ** 半径，历史不同不意味着每个目标都需复杂 memory |
| **Pro18C — MAIN_ACCEPTED（按本地吸收记录）** | 150 V κ 在 off observation 不可见而未来 work 有差；5-point nonlinear CAL chart 的 12-member bank：Full/N2/Direct 最大误差 **0.875243/0.891739/5.875723 nJ**；7 个近等观测成员 L 为 **4.278748–4.321331 nH**，work spread 仅 **0.335303 nJ** | 参数无法唯一恢复而给定 goal 可以稳定；0.335303 nJ 不是连续 fiber 上界，6.086919 nJ 已见 joint remainder 最大值也不是 uniform β |

**Main 接受的含义。** 上述 MAIN_ACCEPTED 是现有本地 absorption 记录的状态转述，不表示本次 GitHub Math 重演了原始 DPT 仿真；来源、时间、owner 都在第 5 节。18A 的完整 recorded-command 替代方案、18B 未见成员失败、18C 非唯一 L 是 Side 后续研究必须正面接受的证据。**100 V R1、150 V CAL/history、600 V native 是三套不同 evidence chart，不能拼接成一条硬件测量证明。**

### 2026-10-17 本地主控只读回填：新证据如何改变 Side 问题

以下是 Math Side 对 `Power Semiconductor/docs/derivations/README.md`（2026-10-17 阅读版）与 `pro_runs/20261014_pro19_physical_recovery_response_frontier/absorption.md` 的**只读记录**；精确公式另见本地 `docs/derivations/dpt_r1_02_switching_physics.tex`、`dpt_r1_04_objective_recoverability.tex` 的 INV-FRB01–10、`dpt_r1_05_differential_transport.tex`。这些是本地主控的 scoped acceptance / source-replay 记录，**本 GitHub Math 本轮并未读取 protected truth、独立运行其 native/flow，也不改变其 owner 决定**。本地文件可能存在未提交版本，Math 只登记读取时的科学状态，不提供镜像原始 source 的权威副本。

| 新来源与本地报告身份 | 改变的科学判断 | 仍需 Math Side 闭合的条件 |
| --- | --- | --- |
| **Pro19D（2026-10-17 本地主控限定接受；有限 flow witness 尚未独立全量重放）** | 同 S150 own-PREP、完整 raw CAL 下，压缩 χ+ψ 的合法近等观测见证距离 `9.4980621e-7≤1e-6`，但 full CAL 距离 `2.7589800e-5`，对应 doublet signed-work 差 `0.000321128494 nJ`；只证明该**压缩摘要**丢失了完整记录可辨别的方向。stored linear full-CAL tangent 的 `ker A⊆ker g` 可读出目标，27 支持中 18 项为盒内 sharp、9 项为 unboxed outer；实际连续非线性 `C_eta` 范围仍 OPEN | 与 Full 同信息对照，取得完整合法 source/guard/联合 noise 下的 `G-p(O)` uniform remainder，或具名且 **Full 同样相容** 的 future-work 双世界反例；不能把 compressed alias 外推为 Full 也失败 |
| **Pro19B（本地主控已接受 fixed-law source algebra）** | 当前同 law 有每步 **10 nonlinear solved variables / 28 sufficient carry-history coordinates** 的可执行消元构造；这不是 10-state 模型、最小动态状态，也没有证明 28-history 能由原 I2 外部记录初始化。保留 gate/charge/diode/load/thermal feedback | 检查低维表示在合法 PREP、guard、future command 作用下的 update consistency、external initialization 与 goal invariance；先比同信息 Full50 |
| **Goal27 / 150 V Pro18C（2026-10-12 controller-accepted conditional proxy，旧 whole-fork beta PARK）** | normalized five-current 分式**代理**的 fixed affine-q 全 bank noise-free error upper `0.876578434279 nJ`，中心之外有 exact 同-q 双点 lower `0.343587503255 nJ`；calibrated-D 与 known-absolute raw5 的相应同角色 proxy minimax 半径约 `0.0115878648465 / 0.003780563 nJ`。这些来自不同测量信息与标定合同，不能互报赢家 | 给 actual nonlinear coupled source、full pretarget CAL、真实 joint sensor error 和同一 frozen work 取得有效 `G-p(O)` 上界；不能把 proxy certificate 或 77 点最大值称 continuous source guarantee |
| **INV-FRB / N100、S02（2026-10-17 推导阅读版；作用域限定已接纳记录）** | 固定有限弦投影读数与真实 signed work 是不同泛函；**`W_H(a)-W_H(b)≠W_H(a-b)`** 因 `VI` 双线性。S02 匹配 PREP 的一组 Rg 变化 fine/coarse work 差约 `+13.611560/+13.593594 nJ`，错误的差波形自乘只约 `+0.722291/+0.713992 nJ`。N100 新 PREP 的 time-shape 在同一 tail-work 评分比 Full/profile 好，且两者的 ΔL 恢复排序不能直接移植到未来 work；R1 联合 L/Rg 新命令亦出现 recovered L 准但 work 不够准 | 冻结 goal scorer 的端口、电流身份、时间窗口与两条路径；始终与 full-record/time-shape/ordinary 同信息竞争，给正确的波形**差后积分**规则与余项，避免读出投影好被提升为 signed-work 保证 |
| **S02 参数曲率（2026-10-16 本地主控接受 scoped）** | 状态线性 RLC descriptor 仍可有非零参数二阶曲率，有限弦 Taylor remainder 与 fixed readout bias 有各自预算 | S02 上的已验数学不能作为 S150/600 V 的 uniform curvature 常数；只有匹配 source path、合法 PREP 和观测定义才可迁移证明结构 |

**Side 的实际选择变化：** 先处理 S150 actual full-CAL 上 `G-p(O)` 的相关 source remainder / continuous compatible-goal 范围，再考虑有限 ΔL 的联合 work–slope enclosure 与最小 pretarget 修复。若已存完整 CAL ordinary 足够，增加摘要或新传感器没有独立信息收益；若只因已有 Banach self-map 的 q>1 而失败，则仅说明该充分性检验未通过，不能断言源模型无根或所有证书路线无望。上述记录不标记为本轮 MAIN_ACCEPTED，也不授权新 native。

## 2. Math Side 又推进了什么（Side → Main 的可吸收增量）

| 新对象 / 状态 | 新的可检验能力及不能外推的部分 | 主控最小下一消费 |
| --- | --- | --- |
| **Mixed-nuisance future-goal radius** — SIDE_VERIFIED＋READY_FOR_HANDOFF | 固定线性可达 state chart，联合有界 correlated error 与任意共享 nuisance 下，goal minimax primal/dual radius 精确相等；存在最优线性 pretarget decoder，无须先恢复全部参数。真实非线性 remainder 与 noise budget 必须另证 | 同 reference 的 HB、N、joint error factor E、legal finite words、future goal rows/tolerances → [contextual_goal_recovery](dpt_tools/contextual_goal_recovery.py) → 与真实 source goal 残差对照；[P 系列完整证明](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md) |
| **Goal-relevant future-word / dynamic closure** — SIDE_VERIFIED（线性/有限域）；READY_FOR_HANDOFF | common linear chart 的最小 all-word row quotient 与 finite-word goal deficiency；ordered stage defect 的精确线性 support bound、transition-pair obstruction。不能把一个 Jacobian 的 rank 推广为 switched/guarded native 最小状态 | 已合法生成的 current/next near-alias、完整 command order、分阶段与总 goal、ordinary rival → [goal stability](dpt_tools/goal_lipschitz_stability.py)、[goal word](dpt_tools/goal_word_quotient.py)、[defect](dpt_tools/goal_defect_transport.py)；[完整证明](dpt_research/20261010_goal_stability_compositional_closure.md) |
| **Nonlinear observation-fiber recovery** — SIDE_VERIFIED（局部条件定理）；OPEN_RESEARCH（native） | 同观测 fiber 的二阶目标漂移由 **goal Hessian − observation Hessian multiplier** 决定；局部 minimax 半径须加受控三阶 remainder，零一阶信息缺口不足以证明目标充分 | 同一 pretarget legal chart、DO/DG/D²O/D²G、branch guards、third-order bound 和 future goal → [fiber curvature](dpt_tools/fiber_goal_curvature.py)、[implicit source Hessian](dpt_tools/implicit_goal_hessian.py)；[C 系列证明](dpt_research/20261012_second_order_goal_fiber.md) |
| **Grouping, information contraction and correlated noise** — SIDE_VERIFIED（数学/合成） | 从 F132 提炼合法四角 mixed contrast 及加性 ordinary 的 sharp lower bound；F129 的 future context 概念与 F119 的 iid noise 定理只在明确转换后适用。**没有**向 SiC 迁移 Boolean exponent、二元 MI 或独立噪声假设 | 构造 Rg×L / history×CAL 的**同一合法 preparation**四角，冻结端口与 goal；同强二阶 ordinary 比较；[proof-critical audit](dpt_research/20261011_F119_F129_F132_proof_level_DPT_bridge.md)、[mixed contrast](dpt_tools/mixed_interaction_audit.py) |
| **Actual-law source residual / goal projection** — SIDE_VERIFIED（条件本构推导）；OPEN_RESEARCH（统一域） | V6 600 V coupled BE 二极管 exponential charge 的 sharp affine remainder、previous-step residual 与隐式 Jacobian/Hessian/adjoint 组合；可解释 full、affine 与便宜 Newton 为何按 goal 改变排序。单支路误差不是全 source 上界 | 一份全耦合 source/branch 的同域 residual、current/previous derivatives、uniform inverse/remainder 常数、peak/event guard → [implicit certificate](dpt_tools/implicit_goal_certificate.py)；[solver fidelity 证明](dpt_research/20261010_goal_information_solver_fidelity.md) |
| **Goal-oriented Hessian + correlated model-discrepancy OED（2025–26 外部论文增量）** — SIDE_VERIFIED（联合 Gaussian 公式、独立 Monte Carlo/反例）；READY_FOR_HANDOFF（限定概率模型）／OPEN_RESEARCH（实际 SiC） | 精读 [Neuberger et al. 2025](https://doi.org/10.1007/s10915-025-03073-y) 的二次 goal posterior-variance 定理、[Koval–Nicholson 2025](https://doi.org/10.1007/s10915-025-03008-7) 的 *parameter*-A-opt BAE 交叉协方差处理，并以 [Zhong et al. 2026](https://arxiv.org/abs/2403.18072) 的 nonlinear observation GO-EIG 为强对照。构造状态–模型误差保留 C=Cov(x,d) 的条件 Gaussian Gq 对比：两参数合成例中，参数 A/MI 偏好传感器 A，而未来二次目标 Gq 偏好 B（风险 **2→1.5**）；Gl 两者都为 0。忽略 C、单点 H 失效或错误参数单位可逆转判断；未证真实器件传感器收益 | 主控按 **同一 reference、合法 pretarget** 的 CAL 候选给 prior/obs Jacobian、future goal Hessian、measurement 与 paired-model discrepancy (包括 C)、units、完整 recorded-command ordinary 和 holdout；先跑 [quadratic-design](dpt_tools/goal_ellipsoid_recovery.py) 诊断并与强普通/非线性 observation 比较，只有 source-native 新证据才能进入 Main；[Q1–Q2 推导及反例](dpt_research/20261012_second_order_goal_fiber.md) |
| **有限历史信息比特预算（F140-A 触发的 Side 增量）** — SIDE_VERIFIED（finite-bank 定理＋代码）；READY_FOR_HANDOFF（具名输入） | 对合法有限 history bank，精确 archived transcript 类在未来目标前被压缩、decoder 再收到带误差盒的 pretarget 外部观测；所需最少定长消息数等于 transcript 冲突图染色数 χ，bits=⌈log₂χ⌉（经典 Witsenhausen zero-error side-information 定理的 DPT 目标容差版本）。五成员 C₅ 反例：最大冲突 clique=2，但 χ=3，至少 **2 bits**；若同一 transcript 内存在冲突，额外编码该 transcript **无法修复**。F140-A 的高斯 streaming 下界、F365-B PDE 唯一性均没有直接迁移 | 主控提供同 reference 的 legal history+真实可提前获取的完整数字 command/transcript、后续 pretarget 观测与误差盒、每个 future command 的 goal/error/tolerance；运行 [retained-goal-bits](dpt_tools/goal_repair_cover.py) 与 **完整 recorded-command ordinary** 比较，独立 holdout 后才讨论吸收；[P19–P22 严格证明](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md) |
| **F122 → 两历史重复采集/共享漂移信息下界** — SIDE_VERIFIED（P23–P26 条件证明、Gaussian 精确计算、Monte Carlo/CLI）；READY_FOR_HANDOFF（具名输入）／OPEN_RESEARCH（真实噪声合同） | 从 OpenAI F122 的 testing/TV tensorization 机制（非其 deletion-trace superpolynomial 结论）建立：未来目标 gap>2τ 时，预测前可见观测律须满足 TV≥1−2α；对同参考下能合法重复的两条历史，传感器高斯误差=每次独立项＋跨次共享校准项时，有精确的最少重复次数和不可消除的错误率下限。三组**单次噪声分布完全相同**的解析例分别需 **12/20/无限次**；仅知道每次 readout 方差不足以决定 acquisition。F115 的 uniform integer-table coupling 与 F373 的 Coulomb multi-marginal 非 Monge 结论也不能直接给 DPT 噪声先验 | Main 提供同一合法 reference、完整 recorded-command ordinary、可复现 preparation 对、真实**预测前 sensor mean gap**、跨次/次内噪声分解及未来目标容差；运行 [gaussian-repeat-goal](dpt_tools/goal_ambiguity_audit.py)，先判定重复同一传感器是否有上限，再与增加不同 sensor/完整记录比较；[P23–P26 原文审计及证明](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md)，未完成 native replay 不晋升 Main |
| **跨传感器 Fréchet 信息下界＋Hall 支持集修复（F115/F373 深挖）** — SIDE_VERIFIED（有限分类定理 P27–P30＋达界联合分布＋独立数值/CLI）；READY_FOR_HANDOFF（需可取得的 hist/联合端口）／OPEN_RESEARCH（真实 coupling） | 若仅有两条历史各传感器的独立**边缘分布**，跨 sensor 相关性完全未知，则合法联合观测律的**最小 TV 恰为最大单传感器 TV**；未来目标区间分离且两历史等先验时，最佳可保证**平均**预测失败率为 (1−max TV)/2，并能给出达界 adversarial coupling 和实际可执行的最佳单传感器 likelihood rule。已知联合依赖时可出现巨大正向 synergy：两个各自都无信息的 binary sensor 联合能完美辨别；3 个独立 Bernoulli sensor 的 TV 0.6→0.792。**平均失败率不是每条历史的 minimax 错误率**。再利用 F115 的 bounded-flow/structural-zero 提示获得**两传感器加权 Hall 最小支持泄漏量**：若两历史各自高概率联合支持不相交、外泄率经 source 资格化为 ε0/ε1，则存在每历史误判率分别不超过 ε0/ε1 的判别器；实际支持不被软件自动认证。F373 Coulomb 非 Monge 不迁移为 SiC coupling 定理；F139 的全局 strong-convex oracle 在非线性观测下可失效 | Main 冻结同 reference 两个 legal preparation、**完整命令 ordinary**、同一 future word/goal/tolerance，给真实可提前取得 sensor 的 per-history categorical marginals、bin、联合同 shot readout、nuisance/calibration/时序；先跑 [marginal-only-fusion](dpt_tools/goal_ambiguity_audit.py) 得保守基线，再用具名**同 shot 联合分布或合法支持集/噪声 tail 界**评估 synergy，并在 holdout 用 per-history 成功率复核；[原文证据审阅、P27–P32 证明](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md) |
| **Finite-bank minimum-cost feature repair** — SIDE_VERIFIED（finite bank、finite candidate library） | 有目标误差区间和 coordinatewise sensor noise 的有限相容对，得到 optimal finite-bank interval radius、hitting-set/cover 与 Lipschitz-gain acquisition；不能宣称物理 continuous-domain sensor optimality | 固定 legal candidate library、每个预目标可取得 feature、correlated/noise model、per-goal tolerance 和成本 → [cover](dpt_tools/goal_repair_cover.py)；[proof annex](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md) |

**上游论文如何真正作用于 DPT。** F266 的 center/tangent/remainder 证书组织实际帮助 18A 的联合链；F229/F376 区分静态目标摘要、动态更新及历史控制；F357/F374 提示方向相关界和 goal-functional 直接约束，但其 RCD/OT 定理未迁移为 SiC 保证；F125 的异常例外选择必须有预测前识别能力；F116 的 universal hitting 前提不适用于含 exp/clip 的 actual source。F122 的 deletion-channel sample exponent 不直接适用 DPT，但其总变差测试思想支持 P23；F115/F373 已在 [P27–P30](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md) 发展为**独立证明**的 finite-category Fréchet coupling 决策器，保留它们原论文的整数 margins / Coulomb support 作用域；F139 因全局强凸 oracle 要求仍只作条件参考。F119/F129/F132 的严谨证明与不适用条件在 [专门 proof audit](dpt_research/20261011_F119_F129_F132_proof_level_DPT_bridge.md)；F049/F149/F360 仍主要是 [来源与边界审阅](dpt_research/20261010_F049_F149_F360_fulltext_proof_audit.md)。文献状态以 [registry](literature/registry.json) 为准。

## 3. 下一轮 Side 研究：三个有决定性增量的接口

### A. 150 V active preparation → CAL / future 的统一有限域预测上界

**已有基础：** 18A 联合 certificate，18C 实际残差/Jacobian、126-step preparation、同初态 CAL/target fork。**需要建设：** 在同一个 source-合法非零域中保留初态传播、active branch、sensor/nuisance correlation、隐式可解性、目标投影和统一 remainder。**Main 最小输入：** F、完整 current/previous derivatives、合法控制盒、joint nuisance、goal 和相应标定量；在真实复算前可先以合法 CAL candidates、goal Hessian、联合模型误差协方差执行 [Gq/BAE 排序压力测试](dpt_tools/goal_ellipsoid_recovery.py)，若传感器选择随 discrepancy 或 nonlinear observation 假设翻转则优先补充源证据。**合格交付：** 可复算上界＋范围＋反例/ordinary 比较，或明确 obstruction 和最小合法修复。Sampled maximum 和局部浮点 Jacobian 均不能单独形成物理全域证书。

### B. 150 V future-goal dynamic closure / 最小可取得的历史修复

**已有基础：** 18B near-alias pair、re-shooting、stage/peak/event/total-work 差及新的 7/9 falsifier；C 的 κ 与 active CAL。**Main 最小输入：** 同 reference 的 measured pretarget history/recorded-command（注明哪些 digital transcript 已存且何时可用）、后续 pretarget sensor/noise（区分跨次共享偏差、逐次独立噪声与**跨传感器联合分布**）、合法 finite word、future scoring、units 和冻结 holdout。可先用 [有限历史信息比特工具](dpt_tools/goal_repair_cover.py) 给出目标容差下可存消息上/下界，与 full-record ordinary 对照。**合格交付：** 信息不够的目标下界 → 真正可取得的 repair → 同预算强 ordinary → 目标上界或 fresh falsifier；不能把重新拟合生成的预测称为 out-of-sample 成功。

### C. 100 V 原 R1 的外部端口相容集合与目标可恢复性

**已有基础：** L/Rser/gain 相容方向、original sensor/path definition 与 observed profile movement。**Main 最小输入：** external cut-voltage/current、端口/方向、sensor correlation、model discrepancy、同一 bounded nuisance family 以及目标容差。**合格交付：** 一项可复算的 compatible-set/goal-range 缩减和最小合法干预，而非先验强求 Lg/Ls/Ld/Lloop/Rg 全部唯一恢复。100/150/600 V 的方法可迁移，实际量和证明不能混接。

### D. 2026-10-17 source-to-goal conditional mathematics and controller bridge

**多步 PREP 及有限 L 的承重建设（Side conditional, actual-source OPEN_RESEARCH）。** 对同一合法 PREP/source/guard/固定命令及 signed work，若 P(z,L)=0、F(X,z,L)=0、W=G(X,z,L) 在共同分支可微，P_z、F_X 可逆，F_X^T λ=G_X^T，则
$
W_L=(G_L-\lambda^TF_L)-(G_z-\lambda^TF_z)P_z^{-1}P_L.
$
这是包含入口状态传导的**条件精确恒等式**，不自动给 preparation/window 因果比例。二步 BE 合法 PREP 解析 oracle 的 W=(5L²+6L+2)/(L+1)³，在 L=1→2 的窗口和 PREP 积分贡献分别为 −137/648、−25/162，总和 −79/216；中心曲率值不能替代完整有限 L 的余项常数。 [完整 S-L1–S-L6 推导与独立负控](dpt_research/20261010_goal_information_solver_fidelity.md) 以 F266 center–tangent–remainder 为证书组织借鉴，原 MUB theorem、root existence、Lean 结论均不自动迁移。

**新的 goal-relevant 预测对象。** 对同完整 pretarget CAL/recorded-command 相容的历史集合 H_y，联合保留 w_h=W_h(L0) 与 s_h=W_h'(L0)，在全部合法有限 ΔL 路径上独立证明 M≥sup |W_h''|。令 a(δ)=inf_(h∈H_y)(w_h+δs_h), b(δ)=sup_(h∈H_y)(w_h+δs_h)。则冻结未来 signed work 处于 [a(δ)−Mδ²/2,b(δ)+Mδ²/2]；若半宽 (b−a)/2+Mδ²/2≤τ，中点是条件式 τ-adequate decoder。存在合法同信息双世界且未来差>2τ 则任何点预测均不能达到 τ。务必保留 (w,s) **联合支持**，不能以分别建盒声称最优。L、W、s、M 的单位分别为 H、J、J/H、J/H²；source-wide M、guard、previous/current Jacobian、合法 prep 与 frozen goal 缺失时只报告 OPEN_RESEARCH。F266 的原论文证明模式不提供这些 source constants。

**Goal27 直接目标残差的两条条件证书（新 S-L5–S-L6）。** 将实际 S150 whole PREP+CAL/target source 写为 F(Z,θ)=0，冻结未见 signed work G、原完整预目标观察 O 及已训练的 p，直接研究 R=G−p(O)，其 source adjoint 解 F_Z^Tλ=(G−p(O))_Z^T。S-L5 用真实 root/guard 和统一 R'' 的**参数单元 Taylor 余项**证明误差界，保留 G 与 O 的共享状态抵消；S-L6 在经过独立资格化、确实包含全部合法 source roots 的外包集合 B 上验证 sup_B |R−λ^TF|≤ε，则因为 root 上 F=0，无须统一逆范数/收缩即可取得目标误差≤ε。两者都需要实际 source 全域证据；S-L6 **没有证明根存在或物理 law 有效**。对现有 projective proxy 的 ε_proxy=0.876578434279 nJ，只能在另外证明同源联合差额 δ 后写 actual bound≤ε_proxy+δ；未资格化 δ 时保持 OPEN。证明、解析负控及单位见 [S-L5–S-L6](dpt_research/20261010_goal_information_solver_fidelity.md) 和 [同源负控](dpt_tools/test_paper_transfer_falsifiers.py)。

**F329 启发的独立连续 fiber 正向界（P33）。** 同实际 source-legal compact Θ 上若已认证覆盖半径 ρ 的网格、完整预目标观测 O 和未来目标 G 的 uniform Lipschitz L_O/L_G，以及同一 joint error 集 E，定义 B(y)={i:dist(y−O_i,E)≤L_Oρ}。所有连续合法相容世界的 future goal 都落于 [min_B G_i−L_Gρ,max_B G_i+L_Gρ]；半宽≤τ 才预测，否则 ABSTAIN。证明和 Θ=[0,1], O=0, G=4θ(1−θ) 端点 bank 假稳定反例见 [P33](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md)。F329 polar metric entropy counterexample 和 F140-A Gaussian streaming bit bound 均不直接成为 DPT lower bound；history compression 还需完整 digital transcript、joint noise 与合法 future 更新相容。finite bank 最大差只能构成必要 lower witness，未认证 ρ/Lipschitz 不能宣称连续充分。

**F357/F325 条件阅读。** F357 的 RCD bi-Lipschitz 构造无法为既有 N100 I2/I3 sensor 自动证明逆稳定。独立局部引理：合法凸域半径 r 内去 nuisance 的 f=PO 若 m=σ_min Df(q0)>0、sup||Df−Df(q0)||≤Hr<m，则 ||f(q)−f(q')||≥(m−Hr)||q−q'||；仍需要 qualified joint sensor noise、goal gain 和 actual chart。仅逐点 rank>0 不够，(cos t,sin t) 首尾可以同观测。F325 的 fixed-operator Crouzeix 可形式应用于冻结多步 DAE block-shift 算子，但已有 exact ordered adjoint/triangular inverse 是更强 ordinary；二步非正规 toy 的 Crouzeix bound 约 50.005，而实际乘积为 1，没有理由据此提升 archive。原 I2 两通道和新增 I3 的 sl 电压必须分开信息成本，KVL 邻接电压恒等式不能直接推物理 branch current 或 signed work 因果份额。

**Main closure 接口与决定性比较。** 本地主控 [docs/derivations/README.md]（只读检查 2026-10-17）已记录 S02 有接受的参数曲率有限弦数学；Goal27 的五电流 fractional-linear **代理域**全 bank 有条件 uniform goal 上界、raw5/calibrated-D ordinary，而 actual S150 全非线性 G−p(O) source-wide 认证仍 OPEN，原 whole-fork root/bank-beta 充分证书路线 PARK。这两种 reference 和证据身份均不得混接。优先接入同一 150 V source 的真实合法 PREP、完整预目标数字命令与 CAL、source current/previous derivatives、原 H/scorer、joint nuisance、source/guard tube、冻结 unseen finite ΔL signed work，比较最强同信息 full-record ordinary；先尝试 G−p(O) source-qualified uniform upper 或合法同 full-CAL 双世界分离>2τ。q>1 的已有 Banach 充分检验失败不是物理解不存在证明。不得读取 protected truth、自动启动 native 或自行晋级 MAIN_ACCEPTED。现有六份证明笔记、7 core / 26 archive 文献与 dpt_tools 入口继续复用。

## 4. 完整数学知识位置与工具

目前维持 **6 份长期更新的证明笔记**，每份应自含 definition、legal domain、theorem、proof、strong ordinary/counterexample、executable test、actual DPT interface 与未闭合处。旧版相似笔记以全文 provenance annex 并入，保留有价值的失败与来源，不再根据 Pro 运行日期无限创建新文件。

| 当前证明笔记 | 主要内容；对应 Python 入口 |
| --- | --- |
| [Mixed nuisance / goal radius](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md) | P1–P33、joint-noise radius、CAL、finite-bank repair；[recovery tool](dpt_tools/contextual_goal_recovery.py)、[cover](dpt_tools/goal_repair_cover.py) |
| [Goal stability / dynamic closure](dpt_research/20261010_goal_stability_compositional_closure.md) | finite gain、recursive consistency、ordered goal-defect；[stability](dpt_tools/goal_lipschitz_stability.py)、[defect](dpt_tools/goal_defect_transport.py) |
| [Second-order goal fiber / source Hessian](dpt_research/20261012_second_order_goal_fiber.md) | C1–C23 的 relative Hessian、Q1–Q2 的 Gaussian-Gq/BAE acquisition、stage tube 与 native qualifications；[fiber](dpt_tools/fiber_goal_curvature.py)、[implicit Hessian](dpt_tools/implicit_goal_hessian.py) |
| [Information × solver fidelity](dpt_research/20261010_goal_information_solver_fidelity.md) | goal sensitivity、source BE storage defect、work/peak、contraction、solver error；[certificate](dpt_tools/implicit_goal_certificate.py) |
| [F119/F129/F132 proof-level bridge](dpt_research/20261011_F119_F129_F132_proof_level_DPT_bridge.md) | actual-paper assumptions、counterexamples、Boolean/context/noise transfer |
| [F049/F149/F360 original-proof audit](dpt_research/20261010_F049_F149_F360_fulltext_proof_audit.md) | 源论文证明、失败迁移与条件界，独立于 DPT accepted evidence |

**公式身份保留：** 原 MAP 的 M1–M54 现在分别在下列专题证明中保留同一编号及上下文；原始逐字版本由 [固定 Git 历史快照](https://github.com/Gogoal-L/math/blob/15b3fde162b2f7cb729ec106b847be1ad046d222/DPT_MATH_RESEARCH_MAP.md) 提供。旧 ID 不再在本导航页重复展开；新增证明使用所在专题的局部编号。

| Legacy equations | Living proof |
| --- | --- |
| **M1–M2，M13–M29** | [mixed-nuisance / original-R1/CAL](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md) |
| **M3–M6，M10–M12** | [F119/F129/F132 source audit and transfer](dpt_research/20261011_F119_F129_F132_proof_level_DPT_bridge.md) |
| **M7–M9** | [future-word dynamic closure](dpt_research/20261010_goal_stability_compositional_closure.md) |
| **M30–M39** | [goal/charge/solver fidelity](dpt_research/20261010_goal_information_solver_fidelity.md) |
| **M40–M54** | [nonlinear goal fiber / implicit Hessian](dpt_research/20261012_second_order_goal_fiber.md) |

Tool API、命令和单位合同见 [dpt_tools/README](dpt_tools/README.md)；现有 [Actions](.github/workflows/dpt-math-auditors.yml) 做 Python regressions、MathJax/GFM 兼容和公式结构检查。**CI PASS = 数学实现/渲染的既定测试通过，不等于所有数学命题形式化证明，更不代表 SiC native/hardware validation。**

## 5. 主控回传入口与下一次更新条件

以下是**本地 DPT 工作区**内的相应材料路径，不是本 GitHub Math 仓库可以直接访问的文件：

- **Pro18 programme absorption:** pro_runs/20261010_pro18_goal_adequacy_frontier/absorption.md；其后若有新一版 Main 裁决，以新 acceptance 和 source ledger 为准。
- **A/B source ledger:** artifacts/run_A/pro18a_source_ledger.csv、artifacts/run_B/pro18b_source_ledger.csv（位于同一 family）。
- **C reader/提交数据:** artifacts/run_C/README.md、artifacts/run_C/pro18c_submission/、artifacts/run_C/original_submission.zip。
- **Actual-law 与复算消费者:** simulation/source_evaluator.py、analysis/acceptance/pro18c_review.py、docs/derivations/README.md。
- **论文来源:** [literature registry](literature/registry.json)、[承重 literature](literature/)、[非承重 archive](literature_archive/)。

**Side → Main** 提交新 proof/test、合法输入、工具结果及最强对手；**Main → Side** 回填新 source replay、冻结评分、失败/接纳及具体修改后的 scientific claim。只因一次新 Pro run、阅读文献或 CI test count 增加，不在 MAP 增添长篇研究日志。只有命题、反例、真实吸收、有效误差界、可部署测量或下一个科学决定出现材料性改变，才更新此页。
