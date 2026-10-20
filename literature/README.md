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
