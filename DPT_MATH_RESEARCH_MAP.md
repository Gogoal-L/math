# DPT-R1 × Math Side：当前研究与吸收接口

更新：2026-10-20。用途是让 Main 与 Side 围绕能改变科学判断的问题工作，准确交付与吸收；本页不是证明正文、运行日志或自动派单器。

**当前结论：Pro19G已返回并完成Main限定吸收，92.5/100不是Original R1或hardware closure评分。** Main后继研究支持若干局部预测与ordinary简化，但合法CAL相容历史上的全非线性目标范围、实际误差合同与跨条件充分性仍未闭合。不要从旧版“准备发送”重新开始，也不要为补齐工具名单空跑。

## 1. 大方向、职责与默认读取

主目标：让Original R1更扎实，建立V4/V5 → S01–S09 → Pro17/18/19之间可检验的关系。优先回答四个问题：外部信息能恢复什么对象；恢复正确后未来目标为何仍失败；有限响应、准备历史或网络机制能否预测新条件；现有CAL支持什么、最少补什么才有用。

- **本MAP：** 当前科学问题、结果状态、吸收/使用入口、下一证据门。先读第2–4节，只有具名缺口才展开专题。
- **六份长期专题笔记：** 完整定义、合法域、推导、证明、反例和来源，定位见第6节；不按每轮任务新建平行报告。
- **dpt_tools与其README：** 实际维护的代码、输入/单位/误差几何合同、运行方式、控制与失败条件。
- **Main本地authorities：** ROADMAP负责阶段/路线，STATE负责科学综合，TASKS负责当前owner/执行，原family负责数据/score。它们不在这个Math仓库，不假定Side能访问。
- **Git与历史：** 改写本页的当前条目，旧版按第7节固定revision追溯；不在此持续追加回传流水。
- **文献：** 原始论文、阅读深度、可支持范围由[literature registry](literature/registry.json)拥有；新科学结论需要独立推导与验证，不把原论文定理或常数直接搬成SiC保证。

100 V Original R1、150 V source/CAL/history、600 V native是不同evidence charts。可以迁移方法和问题，不能把它们拼成一份硬件证明。Main没有授权Side自动读取protected truth、上传本地vendor/source/RAW或启动native。

## 2. 当前能力与吸收：三条状态轴

同一条结果分别记录下列状态，不能互相替换：

| 轴 | 状态及含义 |
| --- | --- |
| Side数学/实现 | `OPEN_RESEARCH`：正在构造或缺关键假设；`SIDE_VERIFIED`：声明数学域内有证明/具名测试；`AMENDED`或`WITHDRAWN`：修正或撤回了具体结论。代码测试不是全部数学命题的形式化证明。 |
| Main吸收 | `NOT_CONSUMED`、`READY_FOR_HANDOFF`、`MAIN_ACCEPTED_SCOPED`、`RETURN_FOR_REVISION`。只有Main具名裁决能改变这一轴；待输入、未提交与未实现须分开。 |
| 实际使用 | 数学条件关系、合成控制、保存数组回放、真实条件预测、既有工具消费者、可编辑推导/论文；注明实际达到哪一级，不能用“已吸收”掩盖尚未调用。 |

`READY_FOR_HANDOFF`须能给出最小输入与单位、唯一可执行工具、决定性检查、输出含义和最小缺件。源输入不在远端时，明确其缺失；不能把内部未来oracle伪装为预测前信息。

| 能力/对象 | Main实际消费与当前状态 | 尚缺什么、下一用途 |
| --- | --- | --- |
| **D16 package两线圈/goal projection** | Main实际调用`goal_defect_transport.py`，原Pro18C H841同静态L条件半径0.02306262345 nJ；符号负控有效。后继两线圈有限比较已接受并进入本地02/05可编辑推导。 | 未来内部驱动/seed半径仍是条件输入；不是完整CAL推出的全源目标范围，也不是不同L直接改状态后的合法PREP。 |
| **S-L27 hybrid投影** | 原source保存状态局部复算支持ETH约−6.295 mV，而深反向body-current投影约4.379e−489 A；d=0标量反证约15.396 µA。Main限定接受并进入02推导。 | 大latent跳跃可有小目标投影，只对具名chart/held-state成立；不是外端口全误差界、可达第二世界或全域可平滑化。 |
| **椭球算子病态噪声修复** | 原rank阈值会将正奇异噪声误判成无噪声，合成同y双世界真实半径至少0.01却报0。现对rank模糊fail-closed返回decoder dual numeric upper和显式非sharp状态，精确负控进入回归。 | [goal_ellipsoid_recovery.py](dpt_tools/goal_ellipsoid_recovery.py)与[test_goal_ellipsoid_recovery.py](dpt_tools/test_goal_ellipsoid_recovery.py)；非有向源认证，尺度/物理E仍须资格化。 |
| **FullCAL/目标行与椭球API** | Main实际调用`goal_ellipsoid_recovery.py`并核盒/球、相关误差与dual支持。D3、eta=1e−6时，chi/psi盒半宽upper3.3813e−4 nJ，加既有CAL派生goal行可至1.1723e−5 nJ；正交行几乎无益。 | 固定centered tangent，不是全非线性域。派生行不算新增测量；绝对consumer与uniform remainder另有输入义务。 |
| **mixed-nuisance/contextual/measurement-factor接口** | 有Side条件数学与工具；不能把合成测试写成全部Main实际调用。 | Main真实transition/合法words、共同nuisance、joint error几何或统一非线性remainder尚缺；由具体decision触发最小消费，不逐模块空跑。 |
| **非线性fiber、goal-defect、动态closure** | 是可建设的条件数学对象；部分局部source关系和数值消费者已用。 | 连续合法CAL fiber的有用目标upper/lower、有限L own-PREP与多command更新仍开放，优先任务见第4节。 |
| **finite-bank repair、bits、shared-drift与sensor fusion** | Side有限域/指定概率模型中的定理与反例可供使用，完整范围在原专题/工具。 | 没有真实noise、相关性、成本与target tolerance合同就不能排名实际sensor或重复采集；finite bank不等于连续family。 |

**保留的修正与撤回。** S-L13原84 W椭球的Brouwer根存在性结论已撤回，不复活whole-fork PARK路线；S-L26定向中心残差/R/J/前驱链缺件不由收据算术测试补齐。D15和P54/P55原始stage/archive回执尚未被Main完整重放，不能称已认证原域反例。原Goal27合法full-source future-goal直径的已认证收缩仍未取得；“收缩为0”不代表真实直径为0。完整证明/反例保留在专题，不在MAP重新证明。

**本地caller修复不归咎上游定理。** Main已修复eta=0 profile误筛face点的本地消费者，保留最小反例、精确binary64有理线性支持及正eta原结果；冻结旧helper不改。600 V旧zero-prefix truth与full-parent-truth的work口径差−17.215333384 nJ已对账；新consumer保留实际前缀，不把同脚本自洽复放当作上游identity正确。

## 3. Main最新实证：哪些决定已经改变

这些是Main验收转述，Side没有因此独立获得或重演本地source archive。数值只属于各自reference、ports/operator、history、window与路径。

| 对象 | 新证据与实际决定 | 持久Main locator（仅本地可用） |
| --- | --- | --- |
| **Pro19G** | 三包764成员、本地43预测/13targets核验；CAL→memory→finite响应链可实际消费，最强同信息actual-law Full仍胜出。后继成果不追溯加G分。 | `pro_runs/20261014_pro19_physical_recovery_response_frontier/absorption.md`及同family `analysis/acceptance/pro19g_return_20261019/`。 |
| **N100恢复≠forward预测** | L=5.4375 nH的新离中点冻结quadratic work误差fine/H2=.070/.034 pJ，own chord20.481/19.147 pJ、旧A-response−27.114/−25.424 pJ；同训练信息scalar ordinary也强。停止相邻L小数位采购。 | `run/S03_heldout_recovery/development_scout/native_finite_L_mechanism/prep_response_transfer/offmidpoint_forecast/`。 |
| **S150 history repair** | 完整donor CAL拟合decoder在2/5/10 ns重构后继续source传播，future误差约.3 pJ。匹配同初态、两目标L、同34 ns命令时condensed−source功差−.00204583/+.0000255178 pJ。 | Pro19 family `analysis/pro19g_acceptance/physical/cal_memory_transfer/finite_L_failure_attribution/history_repair/stage_dependency/matched_propagator/`。这不是短CAL测量，不解释全部旧nJ失败。 |
| **600 V幅度与gate信息** | 两幅度CAL普通gain使exposed doublefall current RMSE .576648→.404464 A，work几乎不变。8CAL matched command→observed VGS仅使fit-grid current .920952→.883543 A，CV/LOAO不稳；实际future VGS输入是contemporaneous条件读出，不是command-only forecast。 | `run/S10_prediction_adequacy/development_scout/native_goal_transport/command_shape_response/causal_prefix_tail/amplitude_conditioned_current/achieved_gate_information/`。停止scalar/feature扫描，未证明序列CAL必要。 |
| **charge信息的ordinary正简化** | 内部7.035 µs测点、条件rho=.10 nC时，双向积分cone+finite-PL box在六model/port中已在saved DP内，DP额外收益0；相对无checkpoint history outer，combined平均再窄27.34%。 | S09 `command_gate_port/charge_history_goal_envelope/checkpoint_information/`。centers是exposed oracle，rho非仪器spec；停止DP加格。 |
| **有限轨迹与范数边界** | 完整历史L2/RMS可经Cauchy–Schwarz界定累计charge，不需零均值；endpoint-only charge不能控制内部历史。原共同gate半径1.219385 V略低于完整union最大1.219927 V。 | S09 `finite_charge_admission/`、`charge_history_goal_envelope/checkpoint_information/`。只承认原半径下的nodal-closure witness，不称原连续gate history合格；fixed map discrepancy仍未包。 |

局部正例、Full获胜、表示失效与ordinary简化都是成果。不能把fixed tangent、finite bank、内部oracle、同模型高精度或经验grid movement自动升级为外部恢复、TOTAL_ERROR或hardware metrology。

## 4. 四条研究前沿：只保留当前最高证据与下一个可失败任务

历史 S-L1–S-L40、P1–P60、Q2–Q4 中间尝试全部保留在既有六份专题笔记及 Git 历史；本索引不再逐条复述已被新约束增强的局部界。以下每项明确区分源实数数学、source-point replay、声明误差模型、原始 source IEEE 资格和 CAL/Goal27 全域闭合。

### Q1 — Original S150 合法 PREP/CAL 历史上的全根与 H841 goal outer

**当前最高原source结构：S-L43 的 14D package SPD、G11 Gauss32 guarded w-KCL、原 S-L41 G12 x-KCL。** 原 ZIP SHA250aa4ea...、actual_law SHA51b78f...、E NPZ SHAbaafdd8c... 严格冻结。S-L40 已可条件性消元24个线圈/器件/热变量，S-L41 再消去 x8/x20；新证明原14个 package P 节点只受正电阻、10线圈 BE 与固定源 forcing，exact Fraction 14×14 LDL全部枢轴正（最小约0.0192181S），从原单阶段 **50D↔10D 条件根对应**，且重构 g2/x 必须仍属于原±.04V十节点chart。另证明 Q1/Q2 原**有限 GL32** G11 w7/w19 行在原 solver |Δ(g−w)|≤1V guard 内均有唯一标量根，对所有固定 g,d±.04V成立；在此guard合格分支进一步条件性 **50D↔8D**。Q2 g−w 原源必要区间宽仅4.470192mV；两个与x无关的非零宽 G11 电压角子盒的全源数学根由 w-KCL 各自严格排除（r上界 Q1<−0.0213288A、Q2<−3.102596A），而PR29的两个x-KCL角子盒仍各自排除 >700A。**没有8D残差存在性、chart补集、原生IEEE GL32/SciPy外包、完整合法历史或Goal27证书**。见 [源结构与原论文迁移](dpt_research/20261010_goal_information_solver_fidelity.md)和 [fail-closed Fraction 代码与测试](dpt_tools/s150_q2_six_row_certificate.py)。

**S-L44 真正更强的source补集：** 原x方程在 h>0.1108ps 时全局x*(d,s,dold,sold)严格呈(+,+,+,−)坐标单调，故合法闭盒两角即可有向包住x根，不需16角或独立划分x。在原n3616 Q2同一非零宽D×S×X source chart子盒，PR29笛卡尔残差含0（下界−1.56A），新联合单调两角严格证明原source r20≥0.51999999999886A，从UNRESOLVED升级为整盒无根；这是实际可复核的**全source单阶段子域排除**，不是全50历史或原生IEEE认证。见 [S-L44细节、精确负控](dpt_research/20261010_goal_information_solver_fidelity.md)及[同一工具](dpt_tools/s150_q2_six_row_certificate.py)。

**S-L40 执行域修正：** 先前 50D→26D 已消除12线圈与12双腿 D1/body/thermal 坐标，针对**固定 n3616 原始 h=0x1.b7cdfd9d80000p-37 秒、source十节点±.04V、旧两个vj∈(-1590,0]V**。理想实数全 raw-T 局部六行数学结论和目前可执行 native-boundary 证书不可混同；**已合并 PR #28 的源执行器仅接受旧8温度 [-60,260]°C**，超出一律 UNKNOWN；native SciPy/NumPy 误差未外包，源身份字符串并不证明原ZIP已在CI重演。即使有了S-L43的10D/guarded8D严格消元，剩余KCL存在/唯一性、guard外根与整个chart补集仍没有原source证书。见 [S-L40及纠错](dpt_research/20261010_goal_information_solver_fidelity.md)。

**S-L42 旧thermal历史必需性：** 在同固定节点chart下，两种条件独立旧四温度全−60/全260°C 的六行热平衡解，其新T0至少相隔 Q1 319.998950381836°C、Q2 319.999685114551°C；仅当前node的旧T盲估计条件minimax至少159.999475/159.999843°C。它们不被宣称是合法同PREP或同26D KCL的两条source历史。与Q2的28D状态下界相互支持，但不自动形成目标功双世界。

**P60b 七读数 PORT-V3/I4、连续80子带：** 原 E/A/ZIP SHA 锁定；4926阶段×80闭子带、共享b∈[90,110]MHz、零和offset、同通道gain/clock/phase/shared nuisance Fraction证书的**保存候选点**间隔已独立复核为 M=0.0344867139926634065 dimensionless；旧报告约0.0298276795443是待冻结旧code/clock/noise contract的历史对比值，不能据此宣称同条件改善；midpoint-to-edge RC漂移的独立算术变化可解释约0.0046590的差额，但旧源码/参数未被当前仓库完整对账。新M仍只是同一声明型误差模型的保存点证书，非新增物理信息。若另获连续全源历史50D tube，额外读数支持必须严格小于M；假设仅两端口V各同半径且I精确时 rV<4.960829mV，假设仅I tube时 rI<36.552385mA，**尚未获此tube**。共同实际E、cal-allroot和未来signed H841仍OPEN。见 [P60b](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md)和 [七读数执行器](dpt_tools/s150_q2_six_row_certificate.py)。

**新前沿论文迁移：** F090 的有限块/尾项 Schur 与signed Bernstein闭盒排除已由精确反例验证；新增完整审读 OpenAI *Atomic triangular-lattice* 31页原PDF+TeX，并真正运行原有限checker（20×20块及659项Bernstein均PASS，恶意枢轴阈值篡改使其FAIL）。独立移植共享nuisance精确消去、可计算几何尾项和De Casteljau闭盒分裂：合成三闭盒严格排除外两盒，保留含真root的中盒。只作为 **CONDITIONAL source-agnostic finite-cover算法**，原8D余式/GL32/guards/历史 E 仍缺原始解析包络。见 [完整证明及负控](dpt_research/20261010_goal_information_solver_fidelity.md)、[执行器](dpt_tools/s150_q2_six_row_certificate.py)、[原论文待读分类](literature_archive/README.md)。



**S-L46 更新（源原始持续子域）：** 原 n3616、原 saved old50 及 12 个 old coil 电流各 ±1mA 的明确条件 predecessor slab 内，Q1 gate6 与 G11w7 联合消元，经 P16 原电阻/全部 12 BE 线圈仿射 lift，证明六电压当前闭子盒（Q1 gate 保存+10..12mV，其余五节点保存±0.1mV）整个原 source exact-real r6>1.0997A，故无根；既有单独 G11/G12 不可得此结论。原 source ZIP/law/adapter/NPZ SHA、公式、negative controls 与执行器见 [S-L46](dpt_research/20261010_goal_information_solver_fidelity.md)、[code](dpt_tools/s150_q2_six_row_certificate.py)。最高证据仍是 **合法源表达式、固定阶段及条件 predecessor 子域整盒排除**；原全 PREP/CAL 外补集、GL32/SciPy outward 与 Goal27 未闭合。

**S-L47 更强条件性原源证明：** 在同 n3616 已保存 predecessor 旧电压和 12 旧线圈各 ±1mA、其他五 current(d,g,s) ±0.1mV 的严格盒上，源 P16 gate g2 仿射灵敏度 a_g≈0.9553822356；G11 finite Gauss 单调使原 Q1 r6 随 g 以 >111.0449577A/V 单调。保存 Q1 gate±125µV 端面残差严格反号（左上界 −1.050867mA，右下界 +1.022349mA），从而每条 fiber 内唯一 guarded Q1 gate 根，原电路结构在其 preimage 上条件性 **50D↔5D**。绝非其余五 KCL、所有 source/predecessor/guard 历史或 Goal27 已闭合。见 [证明与 F122 正定松弛严格不适用](dpt_research/20261010_goal_information_solver_fidelity.md)、[Fraction 执行器](dpt_tools/s150_q2_six_row_certificate.py)。

**下一唯一承重OPEN：** 从已唯一重构的P14/G12x2/guard内G11w2继续证明剩余原 **8D KCL** 全闭盒根/补集（并另行处理G11 guard外分支），外包Q1/Q2 ETH/diode/thermal/clip/ABS seam及原生求积误差；再建立每个合法 predecessor 50D 与PREP126→CAL4800全过程封闭reachability、共同 4801×2 sensor E 和H841 signed-work有向传播。输入仍只有 source-saved n3616 chart，不能称 Goal27有全域upper/lower。

### Q2 — 合法命令 alphabet 的 history/right-congruence 与必需记忆维数

**原source BE 28D predecessor key已升级为局部最小。** exact-real source residual对旧态的依赖因子化为 pi28=(W^T v_old 6, coil old12, vj old2, T old8)。选择原 source S/W charge 6×6 minor，detS=detW=1，附12 coil/2 diode/8 thermal非零旧导数证明在源smooth实数chart上 rank D_old F_BE=28。因此**任何 C1、要保持全部一步 residual 的state摘要维数 m≥28**，原pi28达到下界；若保留old port voltage还需≥29。这个下界不约束goal-only memory、root-set quotient或CAL可恢复维数。在保存n3615的Q1 vj≈−134.885V处 NumPy exp(−972)下溢零：另一个不同旧vj可使全50D浮点残差逐位相同，严禁把实数28秩写成原IEEE rank。见 [Q2局部秩证据与反证](dpt_research/20261010_goal_stability_compositional_closure.md)及 [goal_word_quotient.py](dpt_tools/goal_word_quotient.py)。

**长期OPEN：** 原真实source old_command/reset/TRAP的合法future alphabet、guards、全root历史集合能否右同余，以及一组具有同全CAL但不同future goal的**可达**两世界。合成{A,Blow,Bhigh}右同余而加B0失败仍是命令域反例，不是原S150合法轨迹证明。

### Q3 — pretarget PORT charge / shared prepared current / sharp primal-dual

原source-coil future oracle 与真实 PRETARGET 必须分离。旧冻结 gamma=0 的两future-charge条件最小半径1.300015555pJ（相对R0=.029982652636nJ缩小95.6641%）。**本轮新增sharp物理记忆负控：**在相同原Pro18C source row36 Ls4.16nH与原H841电压核下，若未来驱动盒再容许 ONE SHARED PREP 线圈旧电流偏差 |gamma|≤5µA，则两42ns未来 PORT charge 即使均完美零观测，source系数线性盒的原始Fraction primal/dual仍有非零sharp R=1.617350388645pJ，明确±两世界 charge全同而signed-work差3.234700777289pJ。新先验的无charge半径也须重新算为R0new=.060732996605nJ，不能沿用旧95.6641%百分比；当前先验中的有条件收缩97.33695%，但gamma可取得性、真实共同CAL E及剩余49源残差无证书。原 source SHA/未来 PORT charge/可执行 [Q3证明](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md)、[原code LP证书](dpt_tools/goal_charge_checkpoint.py)；CAL12ns与TARGET18ns既有20.136246938nC差距仍反证直接CAL当oracle。下一OPEN为合法own-PREP跨command K、未来线圈与端口电压物理耦合及joint E/H841全源界。

### Q4 — Original R1 100V E150 合法新条件及 TOTAL_ERROR

已存B100/E100/B150三角三条source truth**不决定缺失E150第四角点**，不能以 additive interaction假设出胜负。六ordinary同存档三角输入的fine/H2预测最小差分别9.872633pJ/8.898416pJ；若要预测新角点，两个待比较模型各自源合法 TOTAL_ERROR 必须严格小于4.936pJ/4.449pJ才能取得该gap的判别资格。已有逐路径 absolute Hessian 上界三角式松度对关键比较达约19–20倍，下一高值检验应是SIGNED mixed curvature的source有向包络、E150 own-PREP/command/event times/窗口冻结和独立第四角点新证据。无E150真值不得宣称 prospective win。见 [Q4源三角边界](dpt_research/20261012_second_order_goal_fiber.md)、[defect工具](dpt_tools/goal_defect_transport.py)。

## 5. 一个完整Side研究单元的可复用模板

复制到**既有专题笔记中的一个节**，不要为模板本身新增报告、JSON或任务系统。没有实际新内容的字段用具名缺件说明，不填装饰性文字。

### 模板：对象ID — 一句话可失败问题

1. **问题与决定：** 解决Main哪个具体困难、谁使用结果；成功/失败后改变什么选择。
2. **合法合同与信息身份：** reference/family、PREP/command、ports/windows/operator、单位/符号、参数域/branch、允许的CAL/recorded-command/prior、joint error；construction/selection/deployment/scoring信息分别标出，曝光历史不重置。
3. **正向构造与证明：** 明确数学对象、假设、边界项/导数/矩阵空间和有限余项；引用原定理时说明真正继承的部分。
4. **最强同信息ordinary：** 相同输入、成本和先验权限下实际比较；不通过削弱Full或多给新模型信息制造优势。
5. **计算与资格：** 固定工具/输入版本、可执行命令、已执行known-answer/反号/边界控制、输出单位、失败与未执行项；昂贵计算先保存唯一checkpoint再做后处理。
6. **重要依赖挑战：** 主动攻击首个成功结果；需要时修表示、信息条件或实验，保留原freeze身份。模型/调用错误、定理错误与DPT迁移错误分开。
7. **状态与用途：** 分别填写Side状态、Main吸收状态、实际使用级别；数学证明/合成验证/真实source回放/前瞻预测不能混写。
8. **Main最小下一消费：** 唯一tool/专题locator、最小输入与确切缺件、期望的不同输出和decision delta；只有模型真有可用分离时建议新数据，成本未知就写UNKNOWN。
9. **STOP/reopen与回填：** 完整单元交付后更新MAP对应条目，结果正文留专题，API留工具README；Main返回accepted locator/范围/决定后替换当前状态，不再追加重复历史。

可先推进完整条件理论或局部建设，不因全域认证/TOTAL_ERROR尚缺而停止；也不能把条件结论写成已经满足物理假设。

## 6. 唯一的证明与工具入口

| Living proof | 职责 / API入口 |
| --- | --- |
| [Mixed nuisance / goal radius](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md) | joint nuisance/error、finite-bank repair、信息下界；[contextual recovery](dpt_tools/contextual_goal_recovery.py)、[repair cover](dpt_tools/goal_repair_cover.py)。 |
| [Goal stability / dynamic closure](dpt_research/20261010_goal_stability_compositional_closure.md) | finite response、更新一致性、ordered goal defect；[stability](dpt_tools/goal_lipschitz_stability.py)、[defect](dpt_tools/goal_defect_transport.py)。 |
| [Second-order goal fiber](dpt_research/20261012_second_order_goal_fiber.md) | nonlinear fiber/Hessian、Gq/BAE；[fiber](dpt_tools/fiber_goal_curvature.py)、[implicit Hessian](dpt_tools/implicit_goal_hessian.py)。 |
| [Information × solver fidelity](dpt_research/20261010_goal_information_solver_fidelity.md) | source/guard/finite remainder与solver误差；[certificate](dpt_tools/implicit_goal_certificate.py)。 |
| [F119/F129/F132 proof audit](dpt_research/20261011_F119_F129_F132_proof_level_DPT_bridge.md) | 原论文假设、反例与DPT迁移边界。 |
| [F049/F149/F360 original audit](dpt_research/20261010_F049_F149_F360_fulltext_proof_audit.md) | 承重原证明与失败迁移，独立于Main实证。 |

工具合同、单位和实际调用命令见[dpt_tools/README.md](dpt_tools/README.md)。不要复制第二份live实现；具名caller错误先最小反例，再修维护路径，旧frozen source保持。原M1–M54及其专题编号的历史映射见[原MAP固定快照](https://github.com/Gogoal-L/math/blob/2d5ef8cf0a813b42a48f821049866df804535a9c/DPT_MATH_RESEARCH_MAP.md#4-完整数学知识位置与工具)，新证明沿专题编号，不在MAP重编全部公式。

## 7. 维护、历史与恢复：避免再次打乱

**更新触发：** 只有新命题/反例、材料性假设修正、实际Main消费或下一科学决定改变才更新MAP；阅读数量、测试数量、运行时长和一次新Pro字母不是触发条件。

**一次闭环：** Side在原笔记/工具完成一个完整单元 → 更新本页对应当前能力或问题卡 → Main按最小输入实际消费 → 回填实际接受范围、locator和下一决定。Main未消费就保留未消费，不凭“已发送/CI绿灯”改状态；Main接受不等于已经写进TeX/论文。

**放在哪里：** 完整证明/反例在六份living notes；API/consumer与资格在工具README；Main运行事实在本地family；错误原因与更正在原对象旁。不要把每次回传复制进MAP，不逐轮新建证明笔记，不重复搬迁历史artifact。旧细节按需从[改版前完整MAP](https://github.com/Gogoal-L/math/blob/2d5ef8cf0a813b42a48f821049866df804535a9c/DPT_MATH_RESEARCH_MAP.md)查询，旧源码/输入/结果身份不改，不另复制一份大型archive。

**并行与冲突：** 独立子问题可并行，专题/工具写域分开，由一个owner消化完整单元；同一MAP更新先读最新blob再提交，发生并发变化先合并，禁止覆盖其他贡献。Side无须向别的聊天发消息；MAP是可拉取接口，不自动授权外部发布、源数据上传或Main执行。

**缺输入时：** 精确列最小缺件及为何阻断actual-source结论；继续独立数学/合成反证或可算局部关系，不能重造hash、归档、合法状态与执行回执，也不反复请求同一缺件。长期根/余项证明可以留OPEN，保留已成立部分和reopen条件。

**CI：** 复用[现有auditors](.github/workflows/dpt-math-auditors.yml)的Python回归、MathJax/GFM与公式检查，不重建、不减负控。CI PASS只是这些检查通过，不是所有命题形式化证明、source输入资格或native/hardware有效性。只在实际测出瓶颈后做最小性能优化，不按测试数量或绿色速度评价科研。

**与后续Pro/S10：** 同19G source/CAL合同的相关合法PREP→goal范围问题可作为19H候选；若换native新序列、信息合同或evidence family，先定义新问题再考虑Pro20。S10“给定可取得信息下何时预测、何时修复/拒判”目前是研究者讨论候选，尚未冻结最终命题/目标容限或授权新native。项目科学边界由Main/研究者拥有，本MAP不自动激活阶段。
