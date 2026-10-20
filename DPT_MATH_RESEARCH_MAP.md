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

## 4. 当前开放问题卡：Side自主选择的长期承重出口

这些问题承接Main短单元难以闭合的数学困难，不要求按顺序全做。Side可以发现更强对象；若改变问题，说明将改变Main哪项决定及为何更值得。

### Q1 — 合法CAL相容PREP像上的有限目标范围
- **P60原source七读数连续RC门（本轮新增）：** SHA锁定E/A原始保存数组，V3/I4零和双通道dual消共同offset，对共享b∈[90,110]MHz作80子带×4926阶严格有理数PL外包、150fs clock、同通道gain和逐读输出phase/noise共同排除。原始本地只读回放得正的**保存点条件**间隔；source-cell lift仅在额外认证全部4927阶50D根tube且其有向支持小于间隔时成立。见[mixed-nuisance P60](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md)、[执行器与测试](dpt_tools/s150_q2_six_row_certificate.py)；原始字节不在远端CI，全root/joint CAL E/H841仍OPEN。
- **S-L38已合并的首次原source六行存在唯一性：** Pro18E n3616固定完整旧50与Q2五节点±0.04V盒内，Q2 body/diode/4热方程在指定根盒唯一；Banach q<1.34e−5，原adapter kappa=1.007，predecessor旧T0盒内exclusion另有严格门。它不是剩余44行、全50D/连续PREP→CAL的证明。见[solver fidelity S-L38](dpt_research/20261010_goal_information_solver_fidelity.md)与[Fraction程序](dpt_tools/s150_q2_six_row_certificate.py)。
- **S-L37新source必需事实：** 原SHA实际ETH在有效T=260℃饱和后仍用RAW tj；raw T=260→261℃时相同有效T、g-s=−4/+14V，ETH分别改变−5.088/−270.956mV。只保留裁剪T的source-root contractor不可靠；该反证不证明raw T>260℃物理可达或50D根。见[solver fidelity S-L37](dpt_research/20261010_goal_information_solver_fidelity.md)和`goal_charge_checkpoint.py`，合法raw-state外包仍OPEN。

- **决定：** 哪些外部CAL信息已经足以预测具名未来goal，哪些合法历史仍会使预测失败？
- **对象：** 同一law/family下的合法own-PREP history集合，完整recorded-command、观察算子和joint error E；直接研究相关goal像或残差`R=G−p(O)`，不先把每个内部状态独立建盒。
- **最强ordinary：** 获相同CAL/public law/seed/family权限的Full与简单goal/readout模型。Full已准确时，贡献可为更少必要信息、明确误差/失效边界，不强求beat Full。
- **有用出口：** 一个非零有限域内可复算的条件upper/lower与关键常数资格，或合法同信息双世界的goal gap及最小repair。tangent/finite bank最大差不代替连续域。
- **P59更强原始3点CAL证书：** SHA钉住的E/A真实保存数组给出精确|w·y|=0.383515988924V，源6个时钟邻接段斜率<7e9V/s；在150fs、≤.02V phase、|gain|≤1.1条件下，epsV+1.1rho_source<0.362360988924V可排除该L4.55保存点（eps=.30558时需rho_source<.0516191V）。严格保留source-cell全根/实际joint E/H841 OPEN；见[mixed-nuisance P59](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md)及`test_paper_transfer_falsifiers.py`。此门强于P58但非全域排除。
- **P58首次原始CAL点排除门：** 同原digital PREP/CAL的Pro18E L4.30观测与Pro19A L4.55 source候选五时刻，exact Fraction共同25MHz相位/增益dual给出|w·y|=0.1233289070766861V；在具名150fs clock/phase/gain及source误差假设下仅当epsV+1.1rho_source<0.122979989584V才能排除该存点。此为真实source数组的候选**必要**排除，不是所有合法L4.55根或Goal27工作直径证书。见[mixed-nuisance P58](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md)和Fraction回归；全root/cell、joint E、未来H841仍OPEN。
- **2026-10-20 P57条件推进：** 同一完整CAL记录的box条件化joint-error支持可比原E−E界严格更紧；固定clock/RC与7维凸共享nuisance模型下，单一候选全CAL不相容具有≤8读数Helly见证。一个4801点合成双root的精确误差门为3/20 V，future-work直径从0跃至1 nJ；真实50D source roots、guard和joint E仍OPEN。见[mixed-nuisance P57](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md)和`test_paper_transfer_falsifiers.py`。
- **长期难点：** PREP126/CAL4800/target6720、guard/diode与相关remainder；允许先攻短片段或直接goal证书。缺source输入可做独立条件数学，不反复生成合成收据冒充source包含。
- **S-L32/D19证据门：** 原S150 body row在ETH跨guard下需要非零状态补偿，已以原source十进制多项式全温度带Fraction/单调性程序证实而非输入假设，不能在保持全50连续的假设下两侧同时零残差；固定H841 work不能被BE-right work替代（原coil-row构造差0.100nJ）。见[solver fidelity S-L32](dpt_research/20261010_goal_information_solver_fidelity.md)、[stability D19](dpt_research/20261010_goal_stability_compositional_closure.md)和回归。full50 root/guard及joint E仍OPEN。
- **S-L36连续guard子域已闭合（source表达式级）：** 对原SHA绑定ETH多项式，精确有理数单调性与二分闭矩形cover使整个(T,g-s)子域可判严格LOW/HIGH或保留所有触界UNDECIDED。25.0084–25.0087℃时g-s=[2.70,2.71]V严格LOW、[2.711,2.72]V严格HIGH；只覆盖2D guard，不认证50D源根/补集/Goal27。见[solver fidelity S-L36](dpt_research/20261010_goal_information_solver_fidelity.md)与`s150_original_guard_replay.py`，下一OPEN为源root/history图的穷尽lift及joint CAL E。
- **S-L33原始E状态可复算：** SHA-pinned Pro18E保存4927x50的Q2 ETH guard在n1707为-1.748918775mV、n1708翻正；±.8mV g/s及±.001C的假设tube只保保存点guard符号，±1mV即跨guard。新[s150 original guard replay](dpt_tools/s150_original_guard_replay.py)严格核原ZIP/actual_law/E NPZ身份且拒绝ALL_ROOT声明；远端原始字节仍缺，完整50D/联合E/H841证书OPEN。
- **S-L31真实source-law硬界：** 按SHA钉住的S150原始actual_law.py在25℃、ETH阈值2.710238125V存在6.459102210mV跳跃；跨阈值连续替代一致误差≥3.229551105mV，必需分guard并保留两分支，不能用盒径趋零代替。证据[solver fidelity S-L31](dpt_research/20261010_goal_information_solver_fidelity.md)及Fraction回归；实际全50D根/联合CAL E/H841目标仍OPEN。
- **S-L30跨guard条件传播：** 同一共同光滑扩展chart中，把跨分支残差J显式计入(q,A,B,J)根差界；小投影电流差仍可触发150 nJ未来guard反例。完整source-real q/J与未来H841外包OPEN，见[solver fidelity S-L30](dpt_research/20261010_goal_information_solver_fidelity.md)。
- **S-L29全root闭合反证：** 同一完整4801×2合成CAL记录下，4926个合法局部阶段及严格guard仍可漏掉另一个全历史根，未来功相差150 nJ（minimax75 nJ）；all-root需要全域补集覆盖。见[solver fidelity S-L29](dpt_research/20261010_goal_information_solver_fidelity.md)和Fraction回归，真实source OPEN。
- **S-L28论文迁移负控：** index-1 DAE 的各根光滑、每根唯一不推出全根覆盖；同完整零观察的双代数根合成未来signed work相差2 nJ。见[solver fidelity S-L28](dpt_research/20261010_goal_information_solver_fidelity.md)与独立Fraction回归；原S150 full50 root/guard仍OPEN。
- **现有笔记：** [mixed-nuisance/fiber](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md)、[solver fidelity](dpt_research/20261010_goal_information_solver_fidelity.md)、[goal defect](dpt_research/20261010_goal_stability_compositional_closure.md)。

### Q2 — 跨command序列的goal-relevant history closure

- **决定：** 单次CAL上足够的摘要，何时可作为后续序列中递推更新的预测状态？
- **对象：** 保留合法PREP、command顺序、future word与goal的memory quotient/finite response；pointwise gate范围或短history特征支持不能直接证明whole-sequence支持。
- **强对手/挑战：** 完整数字命令、同CAL、简单history ordinary；构造单段成功但组合失败的可检验反例，再尝试合法repair。不能只增加feature并报告exposed fit。
- **有用出口：** 新序列上的不同可计算预测、受范围限制的closure关系，或严格限定的最少history信息。原doublefall中候选失败不证明同外部信息普遍不可能。
- **Q2新条件判据：** 同两hidden历史对受限{A,Blow,Bhigh}所有future word目标等价，加入B0即产生150nJ差异；右同余与guard closure必须绑定允许的future command alphabet。见[stability Q2](dpt_research/20261010_goal_stability_compositional_closure.md)，不代表原50D历史合法。
- **工具/笔记：** [goal word](dpt_tools/goal_word_quotient.py)、[predictive-state audit](dpt_tools/predictive_state_audit.py)、[dynamic closure](dpt_research/20261010_goal_stability_compositional_closure.md)。

- **2026-10-20 Side条件负控：** 两个线性command更新各自严格收缩仍可能出现单段不可观测、双段goal gap；已复用原有限word工具，详见[dynamic closure](dpt_research/20261010_goal_stability_compositional_closure.md)。该合成负控不认证原source连续合法历史。

### Q3 — 可取得charge误差信息与reference discrepancy的联合传播
- **Q3新source coil-row条件sharp界：** Pro18C原H841目标核与Ls=4.16nH BE约束、未来|δvD|≤1µV盒模型，未测半径.029982652636nJ；完美未来PORT charge第一半窗降至.001330657989nJ，两半窗降至.001300015555nJ（仅多0.0306424pJ）。同bias三读误差下双row固定dual噪声支撑284.0036705V·rho[nC]，严格收益需rho<.1009939pC。LOCAL source-array Fraction重放，CI仅通用模型回归；非pretarget/全50D Goal27证书。见[mixed-nuisance Q3](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md)与`goal_charge_checkpoint.py`；关键OPEN为合法可取得的PRETARGET charge-to-future transfer与全root joint E。

- **决定：** 哪一项实际可取得的历史/测点信息，能把目标范围缩到有用水平？
- **对象：** gate积分、少数charge checkpoint、origin/first-reversal与reference support；同时保留reference-map discrepancy，区分连续轨迹与采样closure。
- **强ordinary：** checkpoint双向Lipschitz cones+finite-PL box，必须得到同一信息。先解释它做不到什么，再用DP/更深数学。
- **有用出口：** 条件精度要求、误差—goal tradeoff、合法可行见证和outer之间的gap，或证明endpoint/窗口摘要不足。没有真实sensor误差分布就用确定性条件，不制造noise prior。
- **Q3源目标信息反例：** 原C保存H841固定外端口目标核在6720 fine电流坐标中842非零/5878零，独立盒±1uA半径约0.00621835nJ；未来完美两半窗PORT charge checkpoint仍可无收益。属source-point+未认证独立future盒，不是S09 gate charge或全root Goal27证书。见[mixed-nuisance Q3](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md)。
- **停止重复：** 不继续仅为tight数字加密现有DP；不把query实际残差、内部假设µV/µA或假想rho倒称部署前界。
- **笔记：** [goal/fiber recovery](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md)、[finite goal propagation](dpt_research/20261010_goal_stability_compositional_closure.md)。

- **2026-10-20 Side精确条件界：** 端点charge共同bias与独立有界误差下，带符号积分目标有可计算sharp minimax半径；中点checkpoint可有零最坏情形收益。见[mixed-nuisance Q3证明](dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md)与`test_goal_ceiling_tools.py`；未给出物理D、joint E、reference discrepancy资格。

### Q4 — 100 V原R1的可恢复对象与新条件后果
- **E150已保存路径Hessian方法级反证（本轮新增）：** B100/E100/B150原始三曲线的中点缺陷迫使任意逐路径ABSOLUTE Hessian上界三项之和（在每路径eps=六ordinary最小gap/2的条件下）至少3.044/2.894 nJ/nH²，超过最近六候选区分门0.15796/0.14237达19.27/20.33倍；三项各自绝对界再triangle不能认证所需交互曲率，必须转向直接SIGNED C''与相关误差外包。见[second-order Q4](dpt_research/20261012_second_order_goal_fiber.md)及[严格算术负控](dpt_tools/goal_defect_transport.py)。E150真值和TOTAL_ERROR仍缺。
- **Q4六ordinary新判别：** 同保存三历史输入的scalar/full-profile六预测最小间距仅fine9.872633pJ、H2 8.898416pJ；预目标比较候选需各自真实TOTAL_ERROR严格小于半间距4.936/4.449pJ。第四角点E150目标、ownPREP/clock/window和误差仍缺，不排序胜者。见[second-order fiber Q4](dpt_research/20261012_second_order_goal_fiber.md)与`audit_e150_waveform_ordinary_coefficients`。

- **决定：** 有限CAL支持的是哪个measurement-defined对象，以及它对新history/condition的未来goal是否足够？
- **构造/挑战：** 保留L/Rser/gain/clock相容关系和实际观测预算；与同信息frequency/whole-wave/scalar-work ordinary正面比较，不能把有效对象命名为独立PCB/package参数。
- **有用出口：** 前置可算有限系数/余项、一个新的独立条件预测、可取得的最小信息repair。解释已接受N100曲率关系后要给新后果，不重买相邻L点。
- **Q4最新信息门：** B100/E100/B150三角实际存档值无法唯一识别E150：任意history×load交互均匹配三角。若另有合法全域混合导数上界M，E150严格位于additive±M；r/q所需交互fine约−2.406/−3.994 nJ，source未证明M。精确算子及负控见[Q4 interaction](dpt_research/20261012_second_order_goal_fiber.md)和goal_defect_transport；新条件端点/clock/TOTAL_ERROR仍OPEN。
- **Q4定量未冻结候选：** B100/E100/B150已有历史work给出E150三个候选预目标值（fine 35.285/32.879/31.291 nJ），尚无E150合法端点、blackout与TOTAL_ERROR。不得当作前瞻source胜出。见[second-order fiber Q4](dpt_research/20261012_second_order_goal_fiber.md)。
- **2026-10-20 N100新判别：** 已冻结100V B-history实际保存fine/H2数据呈现全H与leading子窗shared/current-scaled profile排名反转；只在现有条件属于retrospective，不能宣称window-uniform充分或L_eff恢复。下个新条件为100V E-history×150uH×L_ext5.25nH，须先具备E-history 150uH source-valid 5.0/5.5nH端点、冻结scorer和joint TOTAL_ERROR。详见[second-order fiber Q4](dpt_research/20261012_second_order_goal_fiber.md)。
- **缺件：** reference/端口/单位/同步与合法PREP input contract由Main提供；没有这些时保留条件关系。
- **笔记：** [second-order fiber](dpt_research/20261012_second_order_goal_fiber.md)、[measurement factor](dpt_tools/measurement_factor_audit.py)。

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
