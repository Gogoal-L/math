# OpenAI Math：完成原始论文深度精读的来源库

本目录按**论文阅读成熟度**组织，不再是“下一批重点论文”队列。收录标准：已直接读取原始 PDF 全文，按页核实承重定理/量词/假设及证明主链，记录必要的源版本和可检验 DPT 迁移边界。**深读完成并不表示独立重证作者整篇论文、运行 Lean/原计算归档，更不表示 DPT/Goal27 完整认证。**

| 论文 | 已核实的证明机制与严格使用边界 |
|---|---|
| [F116-A](F116-A_noncommutative_hitting_point.pdf) | 原文 13 页；统一有理矩阵 hitting point、迭代积分与消失阶。**不**覆盖物理 command。 |
| [F116-B](F116-B_rational_hitting_lists.pdf) | 原文 25 页；逆门 definedness、affine pencils 与 rational hitting lists。 |
| [F125](F125_metric_k_median_recovery.pdf) | 原文 53 页；k-median anchor/proxy、预算严格性。独立 fork SHA。 |
| [F229](F229_three_state_reconstruction.pdf) | 原文 60 页；三态重构、Blackwell experiment order、严格有限条件。 |
| [F266](F266_dimension_six_MUB_certificate.pdf) | 原文 76 页；连续 cell 排除与计算证书流程。全部计算归档**未独立重放**。 |
| [F329](F329_metric_entropy_duality_counterexample.pdf) | 原文 15 页；metric-entropy 极性对偶普适界反例，审查 Lemma 2.1/Props 3.2,4.2,4.3。 |
| [F357](F357_regular_RCD_bi_Lipschitz_coordinates.pdf) | 原文 43 页；RCD 多尺度方向控制和双 Lipschitz 图，不能移植 Bochner 假设。 |
| [F365-A](F365-A_metric_connection_partial_boundary.pdf) | 原文 50 页；metric+unitary connection 全连续边界算子、规范等价。 |
| [F365-B](F365-B_smooth_anisotropic_Calderon.pdf) | 原文 43 页；Calderón 全局部 DN 唯一性、finite probe 的强前提。 |
| [F365-C](F365-C_rough_scalar_conductivity_nonuniqueness.pdf) | 原文 33 页；有界可测标量电导率 full DN 非唯一性，正则性边界。 |
| [F372](F372_smooth_isotropic_elasticity_uniqueness.pdf) | 原文 24 页；静态各向同性弹性全边界算子与系数唯一性。 |
| [F374](F374_Brenier_one_third_stability.pdf) | 原文 18 页；Brenier 映射 1/3 稳定性与三原子 sharp 反例复算。 |
| [F376-A](F376-A_solenoidal_shear_instructions.pdf) | 原文 14 页；solenoidal shear 的连续时刻计算模拟与历史保持；**F376 Lean scope 不覆盖此 companion**。 |

**数量与来源身份：**上表共 13 篇，其中 12 篇来自固定 OpenAI `openai/math` snapshot commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`；F125 来自独立 fork `Gogoal-L/math` commit `014f3ab440592123fafa5c6b67b5e3105587f0f8`、原文件 SHA256 `823fdb284a7d3c0e3089869ba2da3d394db4f19b1c2ab56477ce6ae1b232614b`，不可把它算入固定 snapshot 的 33 篇。全部源身份与 SHA 对照以 [registry.json](registry.json) 为准，所涉 PDF 原字节未修改。

**阅读证据：**F116-A/B、F125、F229、F266、F357、F365-A/B/C、F372、F374、F376-A 具有项目只读研究库中的 `DEEP_READ_V1` 逐页、证明链和适用条件笔记。本次还直接检查 F329 的完整 15 页原始 PDF（Theorem 1.1、Lemma 2.1、Propositions 3.2/4.2/4.3 及 §5 依赖顺序）。未把本地原始 archive/vendor 或私有研究笔记上传 GitHub。

**Lean 范围：**[lean/](lean/) 的 `Fxxx_scope.md` 和 `Fxxx_*.lean` 是**原文选定 statement 的阅读快照**，不等于本目录里的 PDF 已有完整可复验 Lean 证明。F266 的 selected at-most-five **不能**支持论文 headline at-most-three；F365 scope 仅覆盖 C 的 nonuniqueness（不覆盖 A/B）；F376-A 对应的家族 companion Lean scope 仍留 archive。

**DPT 使用：**文献机制只能在额外证明原问题的 model class、guard/branch、连续参数域、误差 enclosure 和合法 PREP→CAL history 后迁移。F266 的穷尽证书思想与 Q1 source-root/interval cover 最相关，但其论文原计算归档缺件仍不构成本项目所有 50D roots 的证书。新的读论文工作从 [literature_archive/](../literature_archive/README.md) 进入，只有补齐全文及证明审读证据才转入本目录。完整 pinned source、书目和手动更新流程保留在归档 README。

来源许可原样保留：[LICENSE](LICENSE)。


## 逐篇证据路径：源定理、关键证明与迁移边界

以下是阅读成熟度索引，不是形式化验证完成清单。每个原始 PDF 的准确 title、canonical preprints source path、版本、SHA256、DPT transfer 等级和 open obligation 均可在 [registry.json](registry.json) 的对应 paper/asset 条目中查到。原始 2026 OpenAI Math 预印本未被本仓库独立确认是已同行评审期刊论文。

| Paper | 已核实的承重原文定位 | 核心量词 / 严格边界 / DPT 实际迁移 |
| --- | --- | --- |
| F116-A | Thm 1.1、Lemma 2.1、Thm 4.2、式(13)–(15)；PDF pp.2,4–11 | 无逆门、非交换、有界公式树与特征零；统一有理矩阵命中在数学类上精确，不给合法 DPT command、鲁棒间隔或 source-root cover。 |
| F116-B | Thm 1.1、Prop 4.2、有限网格与复杂度；PDF pp.1–2,12–21 | 每一个逆门按原语法树定义，不能化简后丢 domain；与 DPT guard/domain 类比仅是方法。 |
| F125 | Thms 1.1/3.3、预算严格性 Lemma 8.1；PDF pp.1–53 | k-median anchor/proxy 与例外簇条件；不能迁入 DPT 的近似系数。原 [OpenAI F125 selected Lean scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/125.md) **存在**，但未在此镜像或执行；本 PDF 独立 fork 原 SHA 已登记。 |
| F229 | Thm 1.1、Cor 1.2、posterior experiment order；PDF pp.1–60 | 三态 tree broadcasting 条件；input-independent kernel 可证明后处理 CAL feature 不添信息，未证明合法 DPT 随机 channel equivalence。 |
| F266 | Props 3.11/4.5、completion/rounding 数值证书；PDF pp.1–76 | 必须覆盖所有闭 cell，failed/unresolved 均为零；论文标题 at-most-three 的全部数值 execution archive **未独立复现**；selected Lean 仅证明 at-most-five 等片段。对应 [Q1 S-L41 与 F090](../dpt_research/20261010_goal_information_solver_fidelity.md) 是独立条件迁移，不是论文直接证明 DPT。 |
| F329 | Thm 1.1、Lemma 2.1、Props 3.2/4.2/4.3、最终参数顺序；PDF pp.1–15 | metric entropy 极性对偶的任意维全局常数反例，不给固定 DPT 残差上界；有完整 15 页原文直接审读记录，但**暂未建立独立本地 DEEP_READ_V1 笔记**，此项以 registry 的 page-grounded locator 单独审计。 |
| F357 | Thm 1.1、Bochner/Gram Lemmas 2.2–2.5、Props 4.10/5.6；PDF pp.1–43 | 非塌缩 RCD 空间、所有欧氏 tangents；多尺度 secant 结构启发 DPT remainder 证明，不能假定源具有 RCD 几何。 |
| F365-A | Thm 1.1、共同 cap/connection-Laplacian 论证；PDF pp.1–50 | smooth metric+unitary connection 完整局部边界能量双线性算子，不是有限 DPT 端口采样。 |
| F365-B | Thm 1.1、Thm 3.1、Green/Hessian 逻辑；PDF pp.1–43 | smooth n>=3、全局部 DN 算子与已知 cap/metric 前提；有限 harmonic tests 无法单独推出有限CAL唯一性。 |
| F365-C | Thm 1.1、weak DN 对称二电导率反例；PDF pp.1–33 | 3D 有界可测均匀椭圆标量电导率可同全 DN 而物理内部不同；说明对象类与正则性是识别必要前提。F365 Lean只对 **C** 的选定结果，不对 A/B。 |
| F372 | Thm 1.1、leading transport/full displacement-to-traction；PDF pp.1–24 | 3D smooth Lamé 强正性和完整静态边界算子；不自动解决 DPT 低维 finite input uniqueness。 |
| F374 | Thm 1.1、Prop 2.2、三原子 sharp 例子；PDF pp.1–18 | Brenier map 目标分布 W2 距离的 1/3 Hölder 稳定性与不可改善反例；不借用指数到 H841 无条件源误差。 |
| F376-A | Lemma 2.1、Thm 1.1、连续 shear-flow 模拟；PDF pp.1–14 | 全阶段时间与 transition inverse 域不可只在 endpoint 检查；F376 家族 selected Lean scope 是**其他 companion**，不是该篇完整流体定理证明。 |

**证据异质性：**12 篇可在只读 DPT 项目研究库找到对应 DEEP_READ_V1 逐页原文笔记；F329 为直接原文审读、现仅 registry/README 的可复核页码链，不能声称有第13份本地标准笔记。F266 笔记的 frontmatter 旧字段需在项目本地单独修正；不能通过本 GitHub PR 写本地任何文件。Lean ComparatorChallenges 的选定声明/桥接桩不能代表作者论文全部证明。Rump、Jaulin、Chen、Petreczky 等外部来源在专题中另行标注作者与定理，绝不归为 OpenAI 原创。下一原文精读候选在 [literature_archive](../literature_archive/README.md)，其中 F090 已完成 49 页主方法与源 checker 审查，但未持久化标准 DEEP_READ_V1 或独立执行 Arb，不在本完成表内。
