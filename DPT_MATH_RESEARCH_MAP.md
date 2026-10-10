# DPT-R1 × OpenAI Math：研究利用与下一证据图谱

最后更新：**2026-10-10**（本轮新增独立数学研究与可执行工具）。本地主控**已同步并接受的 native 科学结果截至 2026-10-09**；原论文与 Lean scope 上游身份采用 `fd4aeeb2`，本轮只对具名来源新增定向原文核查，没有重新验证整个数学论文集。

这份 map 连接 **paper → mathematical object → DPT construction → accepted consequence → next evidence**。它保留原文定位和必要推导，帮助选择下一项研究；本地科学量值与冻结身份由 DPT-R1 原报告拥有，不在这里复制运行账本。

## 当前已取得什么

研究已从 measurement-defined effective commutation coordinate 的恢复，推进到：**在给定准备条件、command、观测与工程目标下，需要保留哪些信息、使用多复杂的本构更新，才能可靠预测有限响应？** 低维 predictive state 是其中一条候选路线；目标相关的模型充分性、直接 command-to-goal 结构和可测有效组合也共同参与竞争。

| 已吸收的数学动作 | 已接受的 DPT 成果（截至 2026-10-09） | 当前作用与下一缺口 |
|---|---|---|
| moment-conditioned exact recovery；attainable extremizer；restricted measurement repair | 固定 affine history functional 的 conditional minimax center/radius 与 top-k blockwise repair 已完成逐步证明和原数组复算；压缩误差远小于会改变当前 programme decision 的尺度 | **CONSTRUCTION + BOUND**。intermediate-object fit 已足够，不继续压历史 fit。极值在 moment 类中可达到；实际 DPT preparation image 的 sharp witness 尚缺 |
| finite command / ordered response；原表达路径 definedness（F116-A/B、F376 方法启发） | 已构造 actual-law command forward，并取得 600 V 两种 ordered commands 的 native 验证；E1 fine/half/quarter 保持 finite-storage waveform 优势，E2 fine/half 也支持该 family | **CONSTRUCTION + FALSIFIER**。command 顺序提供新判别信息；AB/BA 效应本身不证明非线性 memory 或低维更新闭合。没有宣称 vendor map 满足 universal rational hitting theorem |
| actual nonlinear storage + previous-state dependence；Schur / scalar positive-root update | actual coupled BE law、强 evolving-affine 与同 law one-Newton 可公平比较。多个 150/600 V 条件保留 finite-law positive；one-Newton 可廉价复现 full 的主要预测能力 | **CONSTRUCTION**。区分本构近似与求解近似；SCFI 数值形式的必要性未成立。full 不是独立器件真值 |
| goal-conditioned projection / signed residual / work product identity | full waveform 更准与 affine fixed VDS goal 更准可以同时成立；600 V、Rg 变化条件的 signed cumulative residual 定量显示相消机制。窗口 peak 与完整 event peak 已分开 | **CONSTRUCTION + FALSIFIER**。模型复杂度取决于 goal/H/command；继续寻找可从合法 pretarget 信息计算的 adequacy 条件，避免用局部本构余项替代输出分离 |
| goal-visible nullspace、source derivative factorization、finite-defect correction（F365/F372/F329 等 proof-pattern 与边界启发） | actual preparation 链形成 K=DG·DF·DP；source-only repair 与两 command 的固定 Q 摘要已有局部模型 positive。25 mV 保存点单行误差小；较大半径删除 Q 第二行后误差越过既定 0.01，保留两行改善 | **CONSTRUCTION + FALSIFIER**。信息需求随 radius/command/goal/tolerance 改变；固定 Q 删除不是 best-rank-one 下界，更不是全局最小状态证明。内部温度、prefix/model 与 recorded-command 成本单独核算 |
| tangent / implicit lift / event total derivative；certificate 分层（F266/F357/F365-B 方法启发） | Eth 已有 qualified local consistency continuation：27 storage 连续、23 algebraic coordinates 重建，Q2 junction coordinate 调整约 6.296 mV；moving-event 导数接入 lift。300/330 µV 两点联合数值预算支持响应符号 | **CONSTRUCTION + BOUND**。合法局部数值 chart 有用；diffusion underflow 下 active27 与 exact-real 状态分开。持续跨 stage 更新、连续半径与物理 preparation 可达性仍待建设 |
| observation identity、信息预算与 dominance（F140/F229/F372 启发） | 既有 RAW 的软件 H 压力测试、history acquisition 与 retained-summary 成本区分已落地；Atlas→BED 可消费 frozen forecasts 和 accepted outcomes，分别比较 waveform/fixed goal/cost | **CLAIM_GUARD + ACQUISITION**。不把确定性排序称为 Bayesian EIG；没有由同模型软件压力测试推导硬件噪声/精度结论 |

这些成果已经转成推导、唯一 replay、实际预测与反例，并非仅增加引用。**当前 S09 已检查的 OpenAI Math transfer 基本得到实质利用**；仍有来源只发挥边界或背景作用，不按“读过/上传过”宣布 exhausted。2026-10-08 的 bounded 未消费价值审查，在当时 fixed law / input / command / goal 范围内没有留下新的可执行 material delta；重开依据是新的 DPT 问题和可计算后果。

### 2026-10-10：信息维数 × 求解精度（独立数学研究，尚非 native 接受）

本轮在保持 2026-10-09 accepted science 不变的前提下，提出一个更强的、有两个独立证明义务的目标：**给定 preparation / command / goal / tolerance，同时确定未来预测需要多少状态信息，以及 one-Newton / affine 等廉价近似至少需要多少求解精度。** 详细推导与反例见 [goal information × solver fidelity frontier note](dpt_research/20261010_goal_information_solver_fidelity.md)。

- **All-word linear goal quotient**：对同一精确线性 switched model，迭代 \(W_{h+1}=W_h+\sum_a W_h A_a\) 到行空间稳定，就得到**所有有限 command words**的最小 autonomous goal-only linear state；额外自由设计测量维数为 \(\operatorname{rank}[O;W_*]-\operatorname{rank}O\)。新增 [goal_word_quotient.py](dpt_tools/goal_word_quotient.py) 不指数枚举 command words，还输出 reduced updates 和 closure residual。它不能把 Eth 的非线性、分 chart、随 prefix 改变的 Jacobian 直接当作全局定常 \(A_a\)；DPT native 和连续半径 claim 仍待做。
- **Implicit goal-weighted residual**：对于固定 same-law 光滑隐式 residual \(F(y)=0\)，由 \(J=DF(\widehat y)\)、 \(J^T\lambda=Dg(\widehat y)^T\) 构造 pretarget correction \(-\lambda^T F(\widehat y)\)。若同一完整 smooth branch 上另行证明 Newton–Kantorovich 的 inverse/Lipschitz/domain bounds，才有二阶 goal remainder \(\tfrac12(\|\lambda\|L+H_g)\rho^2\)。新增 [implicit_goal_certificate.py](dpt_tools/implicit_goal_certificate.py) 会对不满足条件的案例返回 INCONCLUSIVE；它不负责证明输入 bounds 成立。可由单 BE stage 延至包含 Eth/event 的 **stacked full-trajectory**，但不能用单 stage 结果代替 whole-command 保证。
- **上限与 prior art**：这两套代数对象分别属于已有 switched-linear realization/observability 与 Newton–Kantorovich + goal-oriented residual analysis；潜在 *DPT 新贡献* 是对 actual law、合法 reachable preparation、finite command / goal、数值 guard 给出物理上可检验的适用边界。OpenAI Math [F149 invariant-region proof](preprints/Uniform-Permanence-in-Weakly-Reversible-Mass-Action-Systems-October-5-2026/build/sections/trapping.tex) 和 [F328 resolvent/anchor construction](preprints/Fixed-Points-of-Nonexpansive-Maps-in-Reflexive-Banach-Spaces-September-24-2026/build/sections/02-anchor.tex) 仅为可达域/迭代构造提供证明技巧，**不直接授权 SiC 定理**。

**下一份 zero-fresh 证据**：首先验证实际 Eth lift 能否组成同 chart、无 prefix 偷换的 commanded Jacobians；同时在冻结 one-Newton 预测上计算真正 full-law residual 与 goal adjoint，看 signed correction 是否预测 full-vs-cheap 的目标差。若条件不成立应报告失败，并保留 current accepted S09 positives。工具已经过 synthetic/解析测试，但未使用主控 private RAW 与真实 native solver；不晋升 scientific authority。

### 2026-10-10：ordered goal-defect transport——从单步信息/求解界到真实命令顺序的目标误差预算

在已有 all-word goal quotient、goal ambiguity 和 one-Newton goal-residual certificate 之间，新增**一个不要求各 stage 算子交换的有限命令误差传递对象**。详见 [本轮原文深读与完整证明](dpt_research/20261010_ordered_goal_defect_transport.md)、[Python auditor](dpt_tools/goal_defect_transport.py) 及 [11 项合成测试](dpt_tools/test_goal_defect_transport.py)。

若命令顺序对应同一合法线性状态 chart 的 \(x_{j+1}=A_jx_j+\xi_j\)，准备态隐藏误差满足 \(O\delta x_0=0,\ \|\delta x_0\|\le\rho\)，每阶段有独立 \(\|\xi_j\|\le\epsilon_j\)，目标 \(\delta g_k=c_k\delta x_k\)，则反向行向量 \(q_{k,k}=c_k,\ q_{k,j}=q_{k,j+1}A_j\) 给出

\[
\sup|\delta g_k|
=\underbrace{\rho\|q_{k,0}P_{\ker O}\|_2}_{\text{准备态信息缺口}}
+\underbrace{\sum_{j<k}\epsilon_j\|q_{k,j+1}\|_2}_{\text{各 stage 数值/本构误差}}
\]

在**声明的独立欧氏扰动球线性模型**中这是可达到的精确最坏值，并可输出构造见证；不把其精确性直接扩展到物理 reachable fiber 或真实非线性 DAE。工具可发现 stable eigenvalues 下的 nonnormal goal-visible transient，也保留 AB/BA literal order。它与上一轮「信息半径 vs 单次求解精度」形成一个更明确的 programme 问题：**哪个未知方向会在几次 command 后影响指定 goal？哪个 stage 的误差预算才值得压？**

本轮新增**深入原文** F251（October Strong Ulam）、F289（October near-inclusion/winding）、F325（direct complete Crouzeix）、F129（one-way liveness）、F363（local conservation nonuniqueness）和 F151（\(C^1\) entropy counterexample）。这些来源主要提供 correction obstruction、nonnormality、future-context state-cost 和物理平衡不足的边界；其直接数学定理并不推出上面的 DPT 公式。尤其 F325 的固定单算子函数演算不可用于 arbitrary mixed stage products，F251/F289 October companion 的 Lean selected scope 不覆盖其更强新结果。详细 source-claim/Lean 对照在新研究笔记中。

**下一份零新增仿真检验**：结合已资格化 Eth lift / event derivative 与同 law source Jacobian，验证同 chart 的 \(A_j\)、pretarget \(O\)、goal row \(c_k\) 和可信 \(\epsilon_j\)，用 archived S09 source/one-Newton/TT-source 结果检查谁真正主导 goal discrepancy。若只有点估计而无连续域 error envelope，标记 sensitivity-only；无权直接升级 native claim、改 S09 freeze 或新增 solver budget。

### 2026-10-10：非线性 observation-fiber 曲率与 finite-stage 可达域（独立数学结果）

本轮在 all-word linear quotient、one-Newton 误差和 ordered-stage transport 之上，新增两个不同于点上 Jacobian 与单一 trajectory 的**可证伪对象**。完整证明、OpenAI Math 六个 family 的原始定理/Lean-scope 审查及主控复算合同见 [nonlinear fiber & stage tube](dpt_research/20261010_nonlinear_fiber_and_stage_tube.md)。

- **二阶观测 fiber 信息下界。** 当合法 preparation chart 上的观测 O 为 C² submersion，且固定目标 G 的一阶梯度精确因子化 DG=b DO 时，隐藏方向 v∈ker(DO) 的 fiber 曲率为 Q(v)=vᵀ(D²G−ΣbᵢD²Oᵢ)v。若 Q(v)≠0，存在**相同 O 但未来 G 相差二阶量**的局部合法历史对，说明一阶 K/N 通过仍不足以保证有限半径充分性。新增 [fiber_curvature_audit.py](dpt_tools/fiber_curvature_audit.py) 可寻找最大曲率方向与二阶 level-set witness；C² 及可达历史 chart 必须另证，数值近零一阶因子化不视作 exact。
- **有限阶段连续域检查。** 对已验证 entire-stage box 内成立的仿射表示、偏置、逐坐标本构/求解 remainder bound，递推 interval hull；若每一步都落在下一 stage 有效 box 内，则给出**指定有限 command 序列**的条件 enclosure。新增 [stage_box_reachability.py](dpt_tools/stage_box_reachability.py)；保守 box 失败不等于物理状态越界，浮点计算不是 directed interval proof。
- **上游数学启发。** 深读 F049（稳定坐标与原坐标差异）、F149（有限仿射 trapping）、F360（局部横截曲率到凸域需强条件），并审查 F334/F093/F377 的适用前提。它们提供新反例和 proof architecture，**不直接证明 DPT 定理**。本轮 23 项解析/合成测试和 CLI 检查完成，但不增加 native outcome 或改变已有 authority。

**优先给主控的 zero-fresh 判别：** 固定同一 reachable history/command/goal，比较现有 fixed-Q 两行与一行在较大半径的差异，检查是否存在 Q(v) 的二阶信息泄漏；随后在 Eth-qualified chart 上尝试最小 stage-valid box 与 interval remainder。若缺 Hessian、物理可达性或持续 guard，应报告具体缺失的数据/方程，不强行把工具阴性结果当实际物理失败。
### 2026-10-10：F049/F149/F360 全文源码证明链与源图复核（更新 source-to-DPT 权重）

[逐篇完整正文/附录原文证据与源图复核](dpt_research/20261010_F049_F149_F360_fulltext_proof_audit.md)：已核对三篇各自 main.tex 包含的全部正文/附录与关键承重引理，重新用原始 TikZ 源码编译并目视检查 F049 的线丛/ideal 拉回交换图与 F149 的区间拼接图；**原始 GitHub PDF 二进制未能在本轮逐页截图审查，也没有独立形式化全部证明**。五条 F049 多项式身份已另行符号检验；图形只传达原文关系，不是 DPT 测量证据。

- **F049：WATCH / 概念边界**。stable polynomial coordinate 与原环境坐标不同，是严谨反例；不由此推出 Eth storage/lift 的不存在性。
- **F149：CONDITIONAL-MEDIUM**。真正承重的是 weak reversibility → 反应通量向内偏置 → min-affine plateau 的严格增加 → classwise absorbing set。DPT 最值得验证的替代命题是**具有真实 flow/guard/lift 条件的 hybrid invariant region**；现有 box auditor 没有证明无限时间吸收。
- **F360：WATCH / first-failure 证明架构**。主要定理依赖 weak MTW、Jacobi index form、非共轭性和覆盖论。DPT 应从受约束 implicit-branch continuation 和真实 Eth Jacobian / guard 开始，不调用 MTW 定理替代物理条件。

本轮是**文献来源深度和模型适用边界升级**，不改 S09 native evidence、代理分工、已冻结预测或 LTspice 预算。

### 证据范围与复查入口

上述 native positives 属于同 vendor、同本地电路的模型预测检验，覆盖声明的 150/600 V 条件与各自数值路径。低维充分性、全域 physical identifiability、hardware truth 和 TOTAL_ERROR 各有独立证据门。强 ordinary 胜出的 goal 与既有失败保留在比较中。

本次主控按已接受的原报告同步，local locators 如下（位于 DPT-R1 工作区，不是本 math 仓库的相对链接）：

- `run/S09_intervention_goal_transport/analysis/native_prediction.md`：E1/E2、ordered gaps、Rg 与 preparation native；goal reversal 与完整 event 支持。
- `run/S09_intervention_goal_transport/constructive_theory.md`：source K/Q、rho repair、finite curvature、Eth joint qualification。
- `docs/derivations/README.md`：2026-10-09 两轮承重链接受、公式到 thesis 的 maintext/appendix 映射和唯一 replay。
- `pro_runs/20261003_pro17_s09_constructive_frontier/absorption.md`：原构造及其接受边界；不把后续本地发现倒写成原报告已知。
- `run/goal_oriented_design_development/integrated_report.md` 与原 acquisition plan：Atlas→BED 比较、实际结果反馈及候选决策。

### 当前该买什么证据

1. **可持续更新与 reachable repair**：优先构造合法 preparation family 中的 goal-visible alias，再检查一个预先选定 repair 是否跨 command/目标有效。持续更新必须连过实际 guard/lift，不以增加 state 数量替代 closure。
2. **目标相关复杂度选择**：从合法 own-preparation 和实际本构推出 full/affine/one-Newton 的不同预测，分别冻结 waveform、work、peak/event goal，再购买有判别力的 native。新 current-parent single-wide 预测分离仅占 full increment RMS 的约 0.0116%/0.0359%，当前不为 finite-vs-affine 判别采购它。
3. **不同物理事件或工况**：Rg、负载/热准备与完整 turn-off 都可进入候选。Wu turn-off 预测需要完整 loop、动态 charge、diode/topology 和事件输入映射先闭合；随后补 actual turn-off RAW 才能检验独立 balance-based ordinary rival。现有 notch/recovery RAW 不覆盖 8.010 µs turn-off，不能代替该证据。

本 map 只保留能改变 prediction、information、repair、acquisition 或 claim boundary 的新动作。继续复述论文、重复微小数值 refinement 或补充无分歧 grid 不优先。

### 原文与工具导航

- [literature](literature/README.md)、[archive](literature_archive/README.md)：阅读优先级与备用全文，数量及文件身份以 registry 为准。
- [registry](literature/registry.json)：原文 acquisition、reading tier、Lean selected scope。**本次只更新 map**；registry 的历史 pending 身份尚未同步，不能据此覆盖上方本地主控接受。
- [dpt_tools](dpt_tools/README.md)：有限维/finite-bank auditors；数学工具自身通过不等于 native predictive claim。

以下逐篇分析保留来源定位与 proof-transfer 路径。原“POST-主动”表示形成候选分析，不是本次新增活动任务；当前执行优先级以上方已接受结果和下一证据为准。

---

## 1. 逐篇预期与实际利用：截至 2026-10-09

本表把原 map 的期待与本地实际成果对照。**兑现**指该预期已形成指定范围的结果；**部分兑现**指结构有用但较强目标仍缺证据；**边界作用**也可改变判断，但不算新增 predictor。数学来源、DPT 独立构造与 native outcome 分别记账，不将后续结果追溯归功于原论文。

| 论文 / 数学对象 | 原先希望它帮助什么 | 实际吸收、结论与后果 | 与预期比较 / 下一门槛 |
|---|---|---|---|
| **F116-A**：word→小 ODE→统一 vanishing order→finite detection | 有限历史/command 是否存在统一 detection order；构造可组合有限对象 | 原构造采用 finite lift / command object；随后 actual-law forward 与 ordered-command native 检验落地。精读把 multiplicity 条件和 exact hit/robust gap 区分补齐 | **部分兑现：构造方向已用。** 尚无实际 DPT bounded rational class 或统一 detection-order 定理；native positive 不由 universal hit theorem 保证 |
| **F116-B**：每个 inverse 的 definedness；独立 universal rank list | 固定 experiment family 同时检查 admissibility 与 rank/separation | 原表达树域原则、command/intermediate identity 已纳入工具与比较合同；明确 sampled cover 不保证全 reachable class。没有 native→affine-pencil 映射 | **域原则兑现，universal list 尚未兑现。** 只有合适类映射能带来新 command 预测时再开；不为利用该定理造大型 generator |
| **F229**：posterior sufficiency、garbling、finite dominating experiment | 判断摘要是否足够、新 readout 是否增加独立信息 | 已接受 strict topology 下 Ig/Q 可由既有 command/VGS/Rg 推出：改 coordinate 可以有用，但不是新增 acquisition；MODEL_PRIOR 与测量分开。K/Q digital compression、full-history acquisition 与保留成本也分开 | **信息身份判断兑现。** 尚无 DPT prior/noise 下的 posterior-sufficient causal coordinate 或 finite dominating experiment |
| **F266**：quotient→tangent proposal→normal remainder→atlas certificate | 将 fit/proposal 推为 whole-domain certificate，失败保留 unresolved | 原报告承重采用 proposal/certificate 架构；实际 Eth lift、event/flow/initial-state 联合数值预算及 source finite-defect/tube 分层已落地。有限两点符号与条件 tube 分开记录 | **部分兑现且实质有用。** sampled/domain-qualified certificates 已有；whole reachable domain、统一 remainder/branch containment 未成立 |
| **F365-A**：gauge/observation quotient；source separation | 先 quotient，再判断可辨识参数或可用组合 | 原文 full-source 与 finite construction 依赖已核；本地明确 projection、observed estimator、forward target 的不同身份；local functional annihilates observation nullspace 可支撑组合/goal 判断 | **局部判据兑现。** 一般物理唯一性或全族 recovery 未由 PDE theorem 迁移得到 |
| **F365-B**：jet surjectivity→finite frame→bootstrap | 从 tangent sufficiency 走向 finite-radius repair | local K/N/factor、actual source chain 和有限 defect correction 已构造；finite-input correction 对保存条件误差显著改善。条件 tube 的缺失余项被定位 | **部分兑现。** 连续邻域 sufficiency 与 actual guard/lift 的累计误差仍缺；本地优先 elementary finite-dimensional 方法 |
| **F365-C**：regularity/model class 改变 uniqueness | 避免将固定本构结果误当整个未知类可辨识 | smooth/rough 与 full operator/scalarization 的对照已精读接受；same-law、允许 nuisance/本构变化与不同 operator 的证据层分开 | **边界作用已兑现。** 尚未构造该 PDE 反例的 DPT 对应物，也不预设必须有 |
| **F372**：physical→auxiliary、combination→individual | internal fit 回到合法物理解；可预测组合先于完整参数唯一性 | 推动 actual command/own-preparation evaluator 与外部 goal 连接；full28/active27 只是声明 representation，不命名为最小 physical state。目标可预测与参数可唯一分解分别判断 | **连接要求已落实。** 更强 physical injectivity/minimal realization 仍需 reachable evidence |
| **F374**：sharpness lower construction＋uniform stability upper mechanism | 找出 DPT 的稳定性模量，不以 good fit 代替 stability | 三原子解析 sharpness/control 与唯一 replay 已接受；本地分别处理 point fit、gain、数值 movement、finite remainder。没有移植 1/3 指数 | **原文机制已理解并用于边界。** 未给 DPT 的 uniform stability exponent/modulus；本地 finite-radius 条件界不是该定理实例 |
| **F357**：跨尺度可求和 directional defect→all-pairs chart | tangent/implicit lift 升为有半径的稳定 prediction | 全文机制已精读；本地 finite-radius/curvature 分析与 Eth 联合误差沿该问题建设，明确多点验证、条件 tube 与连续球证书的区别 | **有限尺度建设部分兑现。** RCD/Bochner machinery 未移植；全邻域 uniform bound 尚缺 |
| **F376-A**：original domain、每步 update、intermediate readout | 找出 composition 在哪一段失去闭合，而非只看 endpoint | 已接受 BA command landmarks/阶段 readout 的回溯定位；之后 ordered native 与强 affine 比较增加预测证据。actual consistency lift 补 stage 接缝。二者是 DPT 自身计算 | **诊断与新检验已兑现。** 可持续低维 future-word congruence 尚未建立；AB/BA 不自动证明非线性 memory |
| **F140-A**：memory/precision/selection 信息预算 | 给低信息状态的真实成本或下界 | 定向阅读用于区分 acquired RAW、retained moments、数字 command summaries、internal model inputs；输入精度与 gain 的点上预算已可计算 | **预算澄清兑现。** 未得到该 Gaussian theorem 的 DPT sample/memory 下界；数字压缩不冒充减少 ADC 采样 |
| **F329**：entropy-duality 反例；直接 noise-fiber audit | 从 archive 找 goal-visible collision，决定修复信息 | finite-bank ambiguity 与 source-null direction/repair 的问题框架已有；合法小 preparation 的局部预测 repair 获得 positive。exact fiber、容差接近和 finite gap 分开 | **局部 repair 实质推进。** 全 reachable fiber diameter 上下界未闭合；有限 bank 无碰撞不证明充分 |
| **F355 方法启发＋独立 K/N lemma** | 最少额外 measurement、goal-visible hidden dimension | actual source K=DG·DF·DP 与两 command 固定 Q 构造、第三方向/半径/目标诊断已落实；固定 Q 第二行在较大半径保存点有效，局部 functional recovery 不要求全参数唯一 | **受限局部能力兑现。** best-rank-one 下界、最小部署 sensor 和持续 causal state 未证明；不把独立线性代数归为 F355 新定理 |

### 未作承重迁移的储备

F330/F094/F098 用于 approximation、stability 与 finite/global dimension 的分离；F332/F324 用于 extension/metric representation 与 physical/linear identity 的边界；F251/F289 用于 approximate algebra 与 exact correction 的区别。F325、F363、F129、F132、F122、F119 及 companions 保留各自触发条件，具体原文与推导在下文。

这些材料有既有分析或工具控制，但本次没有接受一个分别由它们新增的 DPT native predictor/theorem。它们与上表的实际利用程度不同；没有新 material consequence 时不强行列成成果。Pro17B 的 exact conditional minimax 本身是重要项目结果，一般 recovery 原理来自既有理论，不能为增加 OpenAI Math 使用数量将其改记为某一 family 的贡献。

### 本次对照得到的判断

**超过早期预期的是落地深度**：现在已有 actual-law generator、ordered native evidence、廉价 one-Newton、目标反转解释、source repair 与合法局部 lift；此前 map 仍主要列候选动作。**尚未达到最强预期的是理论范围**：没有统一 low-dimensional causal state、continuous reachable sufficiency 或全域稳定界。

下一轮不再按论文数量扩线。优先把已有这些对象连接成可更新或更经济的工程预测；某篇储备原文只有带来新的可计算后果才重新进入承重任务。

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
- F325：此前 scope 核查涵盖 polynomial/holomorphic/rational 指定端点。本地已有 conditional stage Jacobian/propagator，但尚未将 F325 的 envelope 绑定并验证为当前实际预测界。
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

- [F229 PDF](literature_archive/F229_three_state_reconstruction.pdf)
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

## 4. F266：proposal、certificate 与 unresolved 的分层

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

此 proof architecture 已进入原构造；当前同名 E1/E2 的 native 验证状态见开头接受表，不能混用不同报告时点。

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

- [F365-A PDF](literature_archive/F365-A_metric_connection_partial_boundary.pdf)
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

- [F365-C PDF](literature_archive/F365-C_rough_scalar_conductivity_nonuniqueness.pdf)
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

- [F372 PDF](literature_archive/F372_smooth_isotropic_elasticity_uniqueness.pdf)
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

- [F374 PDF](literature_archive/F374_Brenier_one_third_stability.pdf)
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

- [F330 PDF](literature_archive/F330_discrete_Lipschitz_free_bounded_approximation.pdf)
- [F094 PDF](literature_archive/F094_Lp_subpolynomial_dimension_reduction.pdf)
- [F098 PDF](literature_archive/F098_doubling_Hilbert_embedding_obstruction.pdf)

F330 区分 approximation property 与 bounded approximation property：每个 finite/compact test 上都能找到 finite-rank approximant，不代表这些 approximants 可以共享一个 finite operator-norm bound。对 DPT 的翻译是：

> 每个有限 command bank 都能 fit 一个低维 state，不代表存在一个 uniformly stable、可部署的低维 predictor。

F094 又说明 exact 与 approximate complexity 可以数量级完全不同；F098 则说明即使 geometry 很“低复杂度”（doubling），整个 infinite/continuous class 仍可能没有任何 fixed finite-dimensional bi-Lipschitz representation。

因此 DPT 建议把“minimum state dimension”升级成至少带四个参数的对象：

`d_G(epsilon, kappa; H, C)`

其中 `epsilon` 是允许的 future-goal error，`kappa` 是 measurement/state 到 goal 的允许 gain/condition budget，`H` 是 admissible history class，`C` 是 future command family。任何低维 claim 都应同时声明自己覆盖 finite bank、finite neighborhood，还是 continuous operational class。

### F289 + F251：trajectory fit 与 structural equivalence 分开

- [F289 strong stability](literature_archive/F289-A_strong_Kadison_Kastler_stability.pdf)
- [F289 one-sided boundary](literature_archive/F289-B_one_sided_near_inclusion_counterexample.pdf)
- [F251 Strong Ulam companion](literature_archive/F251_strong_Ulam_stability_amenability.pdf)

F289 的正向 strong Kadison-Kastler theorem 与 October one-sided counterexample 合起来给 DPT 一个直接 guard：

> “native 中每条 trajectory 都能在 surrogate 里找到近邻”是 directed approximation，不是 structural equivalence。

如果要声称两套 reduced/native dynamics 在结构上等价，至少需要 reciprocal/two-sided closeness，或者一个 explicit near-identity transformation/correction theorem。

F251 的 Strong Ulam companion 从 algebra 侧给同样警告：small composition defect 不能在没有额外结构时自动升级成“附近存在 exact command algebra”。因此以后若 `AB`、`BA`、fusion 等 composition residual 很小，主控只能先记为 **approximate algebra evidence**；是否能 correction 成 exact representation 是第二个 theorem。

### F325：fixed nonnormal propagator 出现时立即打开

- [F325 PDF](literature_archive/F325-A_complete_Crouzeix_structural.pdf)

若后续 frozen stage 真能写成一个 fixed nonnormal operator `A` 的 polynomial / rational readout，F325 的 complete Crouzeix control 可以把 matrix functional 的 operator norm 压到 numerical range 上的二维 envelope：

`||R(A)|| <= 2 sup_{z in W(A)} ||R(z)||`

这里不把它扩展到不同矩阵的 arbitrary noncommutative product。触发条件很明确：**只有 fixed propagator / fixed generator 真正成为 load-bearing object 时才启用。**

### F363 + F129：两个长期 claim guard

- [F363 PDF](literature_archive/F363_local_conservation_Boltzmann_nonuniqueness.pdf)
- [F129 PDF](literature_archive/F129_one_way_liveness_state_lower_bound.pdf)

F363 的意义是把 **conservation certificate** 与 **uniqueness certificate** 分开。DPT 的 charge balance、energy balance、KCL/KVL 检查属于物理一致性证据，不替代 identifiability。

F129 则提供另一种 state lower-bound 语言：如果两个 histories 不同，总能找到一个 future context 把它们区分，那么任何正确 predictor 都不能把这两类 history 合并。若未来 DPT command family 被诚实离散成 finite semigroup / monoid，这条 context-separation 路线可能比 packing bound 更直接地给 deterministic state-complexity lower bound。

F136 与 F139 留在 WATCH：前者是 PPAD local-check robustness，后者在明确 well-conditioned logconcave potential 下给 sampling oracle complexity，都不构成 DPT mixed-query 直接下界。F119 在下面新增的原文小节单独审查；仍不占 S09/S10 预算。



### F332：已存在的稳定预测因子如何延拓为部署映射

**证据 locator**：[PDF](literature_archive/F332_l1_Markov_cotype_extension.pdf)；[完整主证明及第 6 节 extension corollary](preprints/Metric-Markov-Cotype-Two-of-l1-October-5-2026/build/main.tex)；[Mendel–Naor 2013 先验](https://arxiv.org/abs/1301.3963)。目前未发现 lean/docs/332.md。本项目核对了主证明的 cut representation、cubic remainder、martingale telescoping 以及 corollary 的前提；**没有独立证明整篇预印本的全部细节**。

这篇论文的有用性必须从证明链理解。有限 \(\ell_1\) 点集可编码为 weighted binary cuts，使 \(\|x_i-x_j\|_1=\|z_i-z_j\|_H^2\)。作者取 cubic \(\phi(t)=3t^2-2t^3\)；其导数在 binary vertices 处消失，因此两点的平方 \(\ell_1\) 距离增量被 Hilbert 四次方势的 Bregman remainder 控制。条件于 martingale 旧状态时，Bregman 的一次项均值为零，累计损失 telescopes。论文给出 \(N_2(\ell_1)\le12\sqrt{21}\)，然后使用 Hilbert source 的 Markov type 2、\(\ell_1=c_0^*\) 和 Mendel–Naor extension theorem，得到 universal \(K\) 使任意已有的 Lipschitz \(f:S\subset H\to\ell_1\) 可以延拓到整个 Hilbert space，\(\operatorname{Lip}F\le K\operatorname{Lip}f\)。**\(K\) 并未被证明等于 \(12\sqrt{21}\)**。

**与 DPT 真正兼容的条件命题：** 令 \(\mathcal H\) 为已经声明的 switching-history class，\(Y=(O,P):\mathcal H\to\mathbb R^m\) 为单位白化的观测，\(G:\mathcal H\to\ell_1\) 为未来 goal readout。如果：(i) \(Y(h_1)=Y(h_2)\Rightarrow G(h_1)=G(h_2)\)；(ii) 对不同观测 pair 存在统一有限的
\[
L=\sup_{Y(h)\ne Y(h')}\frac{\|G(h)-G(h')\|_1}{\|Y(h)-Y(h')\|_2}<\infty,
\]
则 \(G\) 在 image \(Y(\mathcal H)\) 上才构成 Lipschitz map；**在接受 F332 所述 theorem 的前提下**，可将它延拓到全部 Euclidean observation space，放大至多 \(K\) 倍。extension 不是 identifiability theorem、不是 simulator validation、也不自动给 predictor 算法。若只关心单个 scalar readout，可直接考虑更简单的 McShane extension；F332 的特有价值是多通道 \(\ell_1\) goal 在目标维度增长时仍有 dimension-free existence framing。

**最小测试**：先在已有波形的 finite history bank 报 \(L_{\rm bank}\)。若存在相同 \(Y\) 但不同 \(G\)，有限 gain 不存在，必须找新 measurement 或收窄目标；若 \(L_{\rm bank}\) 过大，先比较从 raw waveform 提取新 feature 与真正新增 sensing 哪个能改善 condition。finite bank 上的低 gain 只是一项观察，无法给出 continuous-class 的 uniform upper bound。工具中新增的 scalar gain 是这一步的局部 indicator，不应标成部署 certificate。**S09 新仿真并非由 F332 自动触发。**

### F324：低失真 metric state 与 linear/physical state 的层级差别

**证据 locator**：[PDF](literature_archive/F324_metric_equivalent_nonisomorphic_Banach.pdf)；[Hilbert slots 及图示](preprints/Lipschitz-Equivalent-Separable-Banach-Spaces-Need-Not-Be-Linearly-Isomorphic-September-24-2026/build/sections/05-hilbert.tex)；[localized linearization](preprints/Lipschitz-Equivalent-Separable-Banach-Spaces-Need-Not-Be-Linearly-Isomorphic-September-24-2026/build/sections/04-localization.tex)；[最终证明](preprints/Lipschitz-Equivalent-Separable-Banach-Spaces-Need-Not-Be-Linearly-Isomorphic-September-24-2026/build/sections/06-assembly.tex)；[Lean selected scope](literature_archive/lean/F324_scope.md)。

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

**证据 locator**：[shear-flow companion PDF](literature_archive/F376-A_solenoidal_shear_instructions.pdf)；[七阶段 shear、recording 和 observer proof](preprints/Finite-Instructions-and-Solenoidal-Shear-Flows-September-27-2026/build/main.tex)；[October 6 box revision PDF](literature_archive/F376-B_incompressible_box_computation.pdf)；[guarded-history proof](preprints/Incompressible-Box-Transport-and-Finite-Computation-October-6-2026/build/guarded-history.tex)；[torus scaling / physical-viscosity proof](preprints/Incompressible-Box-Transport-and-Finite-Computation-October-6-2026/build/torus-routing.tex)；[Lean 376 的 selected scope](literature_archive/lean/F376_scope.md)。

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

**亲读锚点**：[原始论文](literature_archive/F132_sensitivity_block_sensitivity_separation.pdf)；[00 定义与策略](preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/00-introduction.tex)；[01 tournament gate 与 target-row 示意](preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/01-construction.tex)；[02 四组耦合递推](preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/02-recurrences.tex)；[03 量化分离与 composition](preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/03-separation.tex)；[Lean selected scope](literature_archive/lean/F132_scope.md)。

论文对象严格是 total Boolean functions 的**全局** sensitivity \(s(f)=\max_x s(f,x)\) 和 disjoint block sensitivity \(\mathrm{bs}(f)=\max_x\mathrm{bs}(f,x)\)。其 construction 在 \(d\) 层的嵌套 predicates 上分别控制从零变一、从一变零的 single-bit sensitivity \(S_{\ell,0},S_{\ell,1}\)，还增加同一 bit 同时改变**两个不同 child predicates** 的 joint profiles \(J_{\ell,0},J_{\ell,1}\)。这是最该学的技术点：只递推单变量 sensitivity，无法闭合 recursive gate 的界；必须把 pair-change events 作为独立数学对象。论文用 tournament edge labels 限制一次 bit flip 能修复多少候选 clause；下界则构造大量 disjoint blocks 同时使目标行满足。得到 \(s(f)\le2(d+2)M^{d+1}\) 与 \(\mathrm{bs}(f,0)\ge M^2(2M^2+1)^d\)，从而 \(\mathrm{bs}/s^2\ge2^d/[4(d+2)^2]\)，最后经 disjoint composition 得固定指数 \(\alpha>2\)。

**转成 DPT 的正向动作**：同时审计（a）primitive/单参数扰动；（b）两项或多项干预共同出现时的 signed mixed contrast；（c）多个 readouts/stage predicates 是否在同一 waveform 上共同变化。尤其对 threshold 目标，例如 \(1\{\max_t V_{DS}(t)>V_{\rm lim}\}\)，局部连续灵敏度很小也可能存在边界跨越。**但 F132 的超二次指数依赖特定高维 Boolean tournament 递归，绝不构成 SiC 连续参数模型中的 sensor 数或 query 数下界**。真正适合低预算的替代是我们下面的 bounded mixed-contrast lemma，而不是迁移其指数。

最小 ordinary counterexample：\(F(\alpha,\beta)=\alpha\beta\) 在两条坐标轴上恒零，组合干预才出现响应；再考虑 \(F_2(\alpha,\beta)=\alpha\beta(\alpha-a_*)v(t)\)，即使 primitive 和既定一次 fusion \((a_*,b_*)\) 的**完整时间波形**都相同，别的 mixed command 仍能区分。由此一条 mixed query 的“极强反证”只在明确冻结的 quadratic/rational/regularity 类中成立。

### F122：trace alignment / erasure model 先于全波形 reconstruction 的复杂度

**亲读锚点**：[uniform reconstruction PDF](literature_archive/F122-A_uniform_trace_reconstruction.pdf)、[main theorem 与假设](preprints/Uniform-quasipolynomial-time-trace-reconstruction-October-5-2026/build/manuscript/main.tex)、[positive moment arrays 与错误前缀 separation](preprints/Uniform-quasipolynomial-time-trace-reconstruction-October-5-2026/build/manuscript/setup.tex)、[analytical signal / exact generating identity](preprints/Uniform-quasipolynomial-time-trace-reconstruction-October-5-2026/build/manuscript/separation.tex)、[lower-bound companion](literature_archive/F122-B_trace_reconstruction_lower_bound.pdf)、[Lean selected scope](literature_archive/lean/F122_scope.md)。

这里的 input 是任意未知 length-\(n\) binary string，每个位独立以已知 retention probability \(p\) 保留；收到的 trace **没有原始 position labels**。uniform decoder 不是靠简单的 pairwise separation 直接恢复：先构造每个候选 prefix 的正半定 moment relaxation，把“任何错误前缀”变成可观测 trace statistics 上的 separation，再用高阶位置/间距 moments 与多尺度解析 continuation 限制最坏样本数。固定 \(p\) 的 upper bound 为 quasipolynomial；另一个 companion 给 exact worst-case full-string reconstruction 的 superpolynomial lower bound。**本次核对的 lean/docs/122.md 主要 formalize 下界，不能借它证明 October 5 uniform decoder 的每一行细节。**

**DPT 适用判断**：普通 LTspice 自适应时间步/插值属于带 timestamps 的数值重采样，和 unknown-location independent deletion channel 不同；不能从 F122 直接搬出 quasipolynomial sample cost。真正的可迁移动作是先区分已观察 waveform 的原始 time axis、clock jitter、事件区间、丢点/删点 mechanism，再问是否需要完整 trace recovery。若唯一目标是 \(V_{DS,\max}\) 或某个 timing threshold，可以先证直接的 goal-bound：在一个已完全覆盖、最大网格间隔 \(\Delta\) 的 C² 时间区间里，且 \(\|V''\|_\infty\le M_t\)，线性插值误差给
\[
0\le \max_t V(t)-\max_i V(t_i)\le M_t\Delta^2/8.
\]
这是 elementary interpolation theorem，**不是 F122 的定理**；若 event/discontinuity、stage crossing 或 curvature envelope 未被覆盖，这个证书立即失效。保留为“采样模型核验”触发项，zero-fresh 优先，不为 F122 单独占 S09/S10。

### F119：sharpen information loss, but only under its genuine binary-channel model

**来源**：[main theorem / soft-channel proof](preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/main.tex)、[Lean scope](literature_archive/lean/F119_scope.md)。

F119 使用**独立均匀输入 bits**、独立同分布 binary-symmetric noise、预先指定且可随机化的 one-bit summary。主定理先固定 summary 原始 mutual information，再证明独立噪声后的保留信息不能超过一个合适幅度的单坐标软通道；Boolean 推论给经典形式 \(I(f(X);Y)\le1-h_2(\varepsilon)\) bits，输出 bias 时有更强上界。条件中 uniform cube、binary output、symmetric channel 缺一不可。

DPT switching latent 通常连续、有物理相关性，simulator discrepancy 未被标定为 independent BSC。这里可用的是 **channel-specific data-processing / information-retention gate**：若把 stage event 离散成 bits 并另外确证其 noise channel，才讨论此类 sharp rate。暂列 WATCH；不把 \(1-h_2(\varepsilon)\) 作为未标定 DPT 的信息预算。

### F325：fixed nonnormal stage 的 numerical-range upper envelope，及其更简单的强竞争者

**亲读锚点**：[direct proof](preprints/A-direct-proof-of-the-complete-Crouzeix-inequality-September-26-2026/build/main.tex)、[structural companion](preprints/The-complete-Crouzeix-theorem-September-23-2026/build/main.tex)、[Lean selected scope](literature_archive/lean/F325_scope.md)。

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

## 11. 统一数学连接：对象、信息与更新

当前承重链可以写成：

`legal preparation → actual dynamics → observation / retained coordinate → finite command update → engineering goal`。

其中有三种不同的充分性：固定 goal 的恢复、跨 command 的预测、以及可持续 stage transition。前两种 positive 已有局部结果；第三种仍是高价值上限。判断维数时同时声明 tolerance、gain、preparation radius、command/goal family 和实际输入成本。

K/N 与 factorization 是局部信息工具；moment-conditioned minimax 给声明类的完整上下界；reachable witness 才能把 obstruction 落到 DPT 合法 history。F357/F365-B 提醒如何补 finite-radius remainder，F266 提供 proposal/certificate/unresolved 的分层；各迁移结果仍由 DPT 推导与实际验证承担。


## 12. S09 与后续 evidence：从计划到已执行

原 fusion-only 采购阶段已经推进到多种 finite / ordered commands、150/600 V 与非电压工况的实际比较，不能继续把 fusion 写成尚未发生的“第一次”S09 query。一次 mixed contrast 能支持 finite interaction；中心 Taylor coefficient 还需要相应 class/remainder 条件。AB/BA 的区别在线性记忆系统中也可出现，必须结合强 ordinary 的冻结预测定位新增后果。

下一 evidence 由尚未解决的 consequential uncertainty 决定：同信息预算的模型分歧、reachable information repair、完整物理目标或跨工况迁移。optional S10 是否提升 evidence family，应与独立 vendor/measurement 或有机制意义的 domain stress 比较；不因已有 600 V 数据自动宣布 S10 或 high-voltage 全域闭合。

所有后续 adaptive candidate 保留真实选择时点；已曝光数据可以支持机制诊断和更强 ordinary 构造，fresh promotion 另冻结。


## 13. 决策时检查的五件事

1. **目标与信息**：哪个 goal、command、operating domain？输入来自 pretarget、内部状态、recorded command 还是 scoring outcome？
2. **新后果**：能否算出新预测、有限界、合法反例或最小 repair？最强 ordinary 是否已经解释 positive？
3. **域与数值**：原表达路径、guard/lift、完整 observation support 是否有效？数值分辨、cross-path 与用途材料性分别怎样？
4. **充分性层级**：当前证据是 tangent、有限点、bank、连续邻域还是实际 reachable class？误差与 gain 是否随目标/半径改变？
5. **下一选择**：什么结果会换模型、换表示或新增信息？若没有判别价值，先换 intervention/readout 而非追加同类 native。


## 14. 最小原文 bundle：只按具名缺口重开

| 具名缺口 | 定向原文 / 原对象 | 必须产出的终态 |
|---|---|---|
| reachable goal-visible repair | F365/F372、实际 preparation map、K/Q 和匹配 histories | same-law witness 或可计算 repair；明确 full-command ordinary |
| finite-radius / stage update | F357、F365-B、F266；actual guard、lift、flow | 有半径/余项的 prediction 或具名 failed transition |
| ordered command / definedness | F116-A/B、F376；actual command 和内部逆路径 | 未见 word 的不同预测或明确域失败 |
| information cost / sufficiency | F140、F229、F329；真实 acquisition/retention contract | 信息增量、ambiguity、gain 或成本决策 |
| goal-conditioned adequacy | actual full/affine/one-Newton、signed residual、工程目标 | pretarget adequacy 条件或新 falsifier |

原文定理、proof-pattern 和 DPT 独立结果分别标识。已有源不能给出新后果时，不继续扩大阅读 bundle。


## 15. 何时暂停与重开

没有合法 preparation map 时，不将 numerical rank 作为 physical reachable theorem；没有 uniform remainder 时，保留 tangent/有限点 positive 并具名缺口。没有真实 probabilistic experiment、deletion channel 或指定 Gaussian/bit 假设时，不迁移相关数值信息界。

若 elementary factorization、inverse-function 或能量关系已能解决问题，优先使用它；大型 PDE、operator algebra 或 universal hitting machinery 只在实际 DPT 对象满足其结构并产生新后果时进入。

暂停一个迁移不等于数学源已永久 exhausted。重开必须说明：**现有对象 → 新数学操作 → 可计算 DPT 后果 → strong rival / falsifier**。


## 16. 当前 priority：建设而不是重复审计

最值得推进的是合法可更新 prediction 与真实工程目标。把已有 consistency lift、source repair 和 finite-law forward 连成跨 stage/command 的对象；同时允许更经济的直接 goal operator 或 flux/work 关系胜出。

已有 150/600 V finite positives、one-Newton 简化与 ordinary goal victories 构成建设起点。最多保留两个能产生材料性差异的未消费数学对象；没有新差异时明确收口，把注意力转回 DPT 物理输入、observation 和新预测。


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

这些是本 math 仓库的 **synthetic / finite-bank auditable statements**。工具本身尚未逐项绑定实际 DPT 输入；本地主控已有 native 预测与 source-repair 结果，不能把此工具接口缺口误写成 S09 没有 native evidence。参见 [详细使用说明](dpt_tools/README.md)。

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

## 18. 维护方式

按当前成果替换过时计划，合并重复规则，保留原文 locator 和 decisive evidence。每次更新只记录改变 scientific object、prediction、bound、measurement、falsifier、acquisition 或 claim ceiling 的内容。日期是吸收/接受日期，不伪装为每篇原文的首次深读日期。

本次更新记录：2026-10-09，同步已接受的 actual finite-law / ordered-native、goal reversal、source information repair、Eth lift 与两轮公式复核；替换 D-only 对象及待执行 fusion 叙述，合并重复 priorities/bundles。当前实现以本地唯一 evaluator/replay 为准；未上传 vendor payload、RAW、版权全文或私有 source。

下次更新优先回答：新增的哪项可计算结构改变了预测能力、信息需求或工程使用，而不是又读了多少论文。

