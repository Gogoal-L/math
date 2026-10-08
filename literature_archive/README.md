# DPT 文献归档与完整来源对照

主控从 [DPT_MATH_RESEARCH_MAP.md](../DPT_MATH_RESEARCH_MAP.md) 开始即可。当前落实队列在 [literature/](../literature/README.md)。本目录保存条件式、背景与长期边界材料；下面完整对照表仍列出全部 33 份 PDF，其中 7 份链接回核心区，26 份位于本归档区。归档表示当前优先级降低，不撤销已有分析或判定材料无价值。

快照来源：OpenAI 的 `openai/math`，commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`（2026-10-08 获取）。PDF 为原文件字节的重命名副本；首页核对了标题和身份，commit/hash 用于固定版本，不把目录日期当作最后修订日期。33 份 PDF、21 份 scope、47 份 selected-statement Lean 文件构成约 17.5 MB 的阅读包。

命名规则：`F365-A_metric_connection_partial_boundary.pdf` 中 `F365` 是上游 CONTENTS family；`A/B/C` 是本 MAP 对 companion 的本地标签，不是上游定理编号。新增版本保留旧快照与源 commit；需要并排阅读时加 `_vYYYYMMDD`，不覆盖旧文件后仍称其为旧版本。

[registry.json](../literature/registry.json) 是唯一来源索引：source commit、PDF/Lean 对应、SHA-256、按 scientific question 分组的独立 DPT 推导、代码/测试、claim ceiling 与 reopen condition。日常不必阅读 JSON。

## PDF 对照

所有原始 PDF 链接保留在这一表中。Lean 列链接到 family scope，后面的文字决定它是否覆盖当前 subpaper。点击 scope 后可读其 selected statement；family 相同不会自动获得相同形式化覆盖。

| 本地 PDF | 原始来源与版本说明 | Lean 对应 |
|---|---|---|
| [F116-A_noncommutative_hitting_point.pdf](../literature/F116-A_noncommutative_hitting_point.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/One-Rational-Matrix-Hitting-Point-for-Noncommutative-Formulas-September-24-2026/README.md) | [F116 scope](../literature/lean/F116_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F116-B_rational_hitting_lists.pdf](../literature/F116-B_rational_hitting_lists.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-Hitting-Lists-for-Noncommutative-Rational-Formulas-September-24-2026/Polynomial-Hitting-Lists-for-Noncommutative-Rational-Formulas-September-24-2026.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Polynomial-Hitting-Lists-for-Noncommutative-Rational-Formulas-September-24-2026/README.md) | [F116 scope](../literature/lean/F116_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F229_three_state_reconstruction.pdf](F229_three_state_reconstruction.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-exact-reconstruction-threshold-for-the-three-state-symmetric-channel-September-25-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-exact-reconstruction-threshold-for-the-three-state-symmetric-channel-September-25-2026/README.md) | [F229 scope](lean/F229_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F266_dimension_six_MUB_certificate.pdf](../literature/F266_dimension_six_MUB_certificate.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026/README.md) | [F266 scope](../literature/lean/F266_scope.md)；selected family bound 为 at most five；不证明 headline N(6)=3。 |
| [F365-A_metric_connection_partial_boundary.pdf](F365-A_metric_connection_partial_boundary.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Determination-of-a-metric-and-a-unitary-connection-from-one-boundary-patch-October-5-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Determination-of-a-metric-and-a-unitary-connection-from-one-boundary-patch-October-5-2026/README.md) | [F365 scope](lean/F365_scope.md)；未覆盖：365 scope 仅覆盖 F365-C。 |
| [F365-B_smooth_anisotropic_Calderon.pdf](../literature/F365-B_smooth_anisotropic_Calderon.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Smooth-Anisotropic-Uniqueness-in-the-Calderon-Problem-from-One-Boundary-Patch-September-24-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Smooth-Anisotropic-Uniqueness-in-the-Calderon-Problem-from-One-Boundary-Patch-September-24-2026/README.md) | [F365 scope](lean/F365_scope.md)；未覆盖：365 scope 仅覆盖 F365-C。 |
| [F365-C_rough_scalar_conductivity_nonuniqueness.pdf](F365-C_rough_scalar_conductivity_nonuniqueness.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Nonuniqueness-for-Bounded-Measurable-Scalar-Conductivities-in-Three-Dimensions-September-23-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Nonuniqueness-for-Bounded-Measurable-Scalar-Conductivities-in-Three-Dimensions-September-23-2026/README.md) | [F365 scope](lean/F365_scope.md)；覆盖 selected scalar-conductivity nonuniqueness statement。 |
| [F372_smooth_isotropic_elasticity_uniqueness.pdf](F372_smooth_isotropic_elasticity_uniqueness.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Global-Uniqueness-for-the-Smooth-Isotropic-Elasticity-Inverse-Problem-September-24-2026/article.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Global-Uniqueness-for-the-Smooth-Isotropic-Elasticity-Inverse-Problem-September-24-2026/README.md) | [F372 scope](lean/F372_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F374_Brenier_one_third_stability.pdf](F374_Brenier_one_third_stability.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/article.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/README.md) | [F374 scope](lean/F374_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F357_regular_RCD_bi_Lipschitz_coordinates.pdf](../literature/F357_regular_RCD_bi_Lipschitz_coordinates.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Bi-Lipschitz-Coordinates-at-Regular-Points-of-Noncollapsed-RCD-Spaces-September-25-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Bi-Lipschitz-Coordinates-at-Regular-Points-of-Noncollapsed-RCD-Spaces-September-25-2026/README.md) | 本版本无 357 scope。 |
| [F330_discrete_Lipschitz_free_bounded_approximation.pdf](F330_discrete_Lipschitz_free_bounded_approximation.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Failure-of-Bounded-Approximation-in-a-Lipschitz-Free-Space-over-a-Uniformly-Discrete-Metric-Space-September-26-2026/main.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Failure-of-Bounded-Approximation-in-a-Lipschitz-Free-Space-over-a-Uniformly-Discrete-Metric-Space-September-26-2026/README.md) | [F330 scope](lean/F330_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F094_Lp_subpolynomial_dimension_reduction.pdf](F094_Lp_subpolynomial_dimension_reduction.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Subpolynomial-dimension-reduction-in-Lp-September-23-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Subpolynomial-dimension-reduction-in-Lp-September-23-2026/README.md) | [F094 scope](lean/F094_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F098_doubling_Hilbert_embedding_obstruction.pdf](F098_doubling_Hilbert_embedding_obstruction.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-doubling-Hilbert-subset-with-no-finite-dimensional-bi-Lipschitz-embedding-September-25-2026/main.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-doubling-Hilbert-subset-with-no-finite-dimensional-bi-Lipschitz-embedding-September-25-2026/README.md) | [F098 scope](lean/F098_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F289-A_strong_Kadison_Kastler_stability.pdf](F289-A_strong_Kadison_Kastler_stability.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Universal-strong-Kadison-Kastler-stability-September-23-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Universal-strong-Kadison-Kastler-stability-September-23-2026/README.md) | [F289 scope](lean/F289_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F289-B_one_sided_near_inclusion_counterexample.pdf](F289-B_one_sided_near_inclusion_counterexample.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Near-Inclusions-of-von-Neumann-Algebras-Without-Small-Spatial-Embeddings-October-5-2026/near-inclusions.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Near-Inclusions-of-von-Neumann-Algebras-Without-Small-Spatial-Embeddings-October-5-2026/README.md) | [F289 scope](lean/F289_scope.md)；未覆盖本篇 one-sided companion。 |
| [F251_strong_Ulam_stability_amenability.pdf](F251_strong_Ulam_stability_amenability.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Strong-Ulam-Stability-Characterizes-Amenability-October-5-2026/strong-ulam-stability.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Strong-Ulam-Stability-Characterizes-Amenability-October-5-2026/README.md) | [F251 scope](lean/F251_scope.md)；未覆盖本篇：251 scope 覆盖 unitarizability 主结果。 |
| [F325-A_complete_Crouzeix_structural.pdf](F325-A_complete_Crouzeix_structural.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-complete-Crouzeix-theorem-September-23-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/The-complete-Crouzeix-theorem-September-23-2026/README.md) | [F325 scope](lean/F325_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F363_local_conservation_Boltzmann_nonuniqueness.pdf](F363_local_conservation_Boltzmann_nonuniqueness.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Nonuniqueness-with-local-conservation-for-the-hard-sphere-Boltzmann-equation-October-5-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Nonuniqueness-with-local-conservation-for-the-hard-sphere-Boltzmann-equation-October-5-2026/README.md) | [F363 scope](lean/F363_scope.md)；仅有较早 periodic theorem scope；不覆盖本篇全部 local-conservation refinement。 |
| [F129_one_way_liveness_state_lower_bound.pdf](F129_one_way_liveness_state_lower_bound.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/main.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/README.md) | [F129 scope](lean/F129_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F332_l1_Markov_cotype_extension.pdf](F332_l1_Markov_cotype_extension.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Metric-Markov-Cotype-Two-of-l1-October-5-2026/l1-markov-cotype.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Metric-Markov-Cotype-Two-of-l1-October-5-2026/README.md) | 本版本无 332 scope。 |
| [F324_metric_equivalent_nonisomorphic_Banach.pdf](F324_metric_equivalent_nonisomorphic_Banach.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Lipschitz-Equivalent-Separable-Banach-Spaces-Need-Not-Be-Linearly-Isomorphic-September-24-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Lipschitz-Equivalent-Separable-Banach-Spaces-Need-Not-Be-Linearly-Isomorphic-September-24-2026/README.md) | [F324 scope](lean/F324_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F329_metric_entropy_duality_counterexample.pdf](../literature/F329_metric_entropy_duality_counterexample.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Counterexamples-to-the-duality-conjecture-for-metric-entropy-September-24-2026/main.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Counterexamples-to-the-duality-conjecture-for-metric-entropy-September-24-2026/README.md) | [F329 scope](../literature/lean/F329_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F376-A_solenoidal_shear_instructions.pdf](F376-A_solenoidal_shear_instructions.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Finite-Instructions-and-Solenoidal-Shear-Flows-September-27-2026/manuscript.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Finite-Instructions-and-Solenoidal-Shear-Flows-September-27-2026/README.md) | [F376 scope](lean/F376_scope.md)；family scope 指向其他 sheet/detector papers；本 companion 的 exact statement 对应未独立核验。 |
| [F376-B_incompressible_box_computation.pdf](F376-B_incompressible_box_computation.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Incompressible-Box-Transport-and-Finite-Computation-October-6-2026/manuscript.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Incompressible-Box-Transport-and-Finite-Computation-October-6-2026/README.md) | [F376 scope](lean/F376_scope.md)；scope 链接 September 27 box edition；October 6 edition 与 October 7 repairs 不自动继承覆盖。 |
| [F132_sensitivity_block_sensitivity_separation.pdf](F132_sensitivity_block_sensitivity_separation.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/README.md) | [F132 scope](lean/F132_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F122-A_uniform_trace_reconstruction.pdf](F122-A_uniform_trace_reconstruction.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Uniform-quasipolynomial-time-trace-reconstruction-October-5-2026/uniform-trace-reconstruction.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Uniform-quasipolynomial-time-trace-reconstruction-October-5-2026/README.md) | [F122 scope](lean/F122_scope.md)；未覆盖本篇 uniform decoder；122 scope 为 lower bound。 |
| [F122-B_trace_reconstruction_lower_bound.pdf](F122-B_trace_reconstruction_lower_bound.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/quantitative-lower-bounds-for-trace-reconstruction-September-24-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/quantitative-lower-bounds-for-trace-reconstruction-September-24-2026/README.md) | [F122 scope](lean/F122_scope.md)；覆盖 selected deletion-trace lower bound。 |
| [F355_tangent_flow_uniqueness.pdf](F355_tangent_flow_uniqueness.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Tangent-flow-uniqueness-2026-09-24/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Tangent-flow-uniqueness-2026-09-24/README.md) | 本版本无 355 scope。 |
| [F140-A_Gaussian_regression_memory_precision.pdf](../literature/F140-A_Gaussian_regression_memory_precision.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Memory-and-precision-in-noiseless-Gaussian-regression-September-27-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Memory-and-precision-in-noiseless-Gaussian-regression-September-27-2026/README.md) | [F140 scope](../literature/lean/F140_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F140-B_posterior_replicas_information.pdf](F140-B_posterior_replicas_information.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Posterior-replicas-and-conditional-information-in-Gaussian-regression-September-27-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Posterior-replicas-and-conditional-information-in-Gaussian-regression-September-27-2026/README.md) | [F140 scope](../literature/lean/F140_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F140-C_exact_Gaussian_localization.pdf](F140-C_exact_Gaussian_localization.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Localization-costs-and-information-growth-for-exact-Gaussian-observations-September-27-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Localization-costs-and-information-growth-for-exact-Gaussian-observations-September-27-2026/README.md) | [F140 scope](../literature/lean/F140_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F119_binary_information_contraction.pdf](F119_binary_information_contraction.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/main.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/README.md) | [F119 scope](lean/F119_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |
| [F325-B_complete_Crouzeix_direct.pdf](F325-B_complete_Crouzeix_direct.pdf) | [原 PDF](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-direct-proof-of-the-complete-Crouzeix-inequality-September-26-2026/paper.pdf) · [版本说明](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-direct-proof-of-the-complete-Crouzeix-inequality-September-26-2026/README.md) | [F325 scope](lean/F325_scope.md)；有 family selected scope；对应原模型与 selected statement，DPT transfer 另行证明。 |

## Lean 阅读范围

核心区或归档区的 `lean/Fxxx_scope.md` 的 scope 正文保留上游原文，仅添加来源说明并调整链接。对应的 `lean/Fxxx_*.lean` 是 byte-identical **Comparator selected-statement** 快照：它们定义要验证的数学命题，可含 `axiom` 占位声明；这些声明本身不是 Lean 已经证明该命题的证据。

完整 solution module、imports、comparator 配置和工具链继续位于仓库原有 [lean/](../lean)。registry 的 `formalization.selected_statements` 给出 source path、comparator config、solution module 与 theorem names；source commit 固定其完整依赖版本。要核查证明，按照 [Comparator README](../lean/ComparatorChallenges/README.md) 在完整环境运行对应 comparator。本次没有运行 Lean 编译，也没有把这些阅读快照包装成独立可编译项目。

特别对应：F365-A/B 的 PDF 与 F365-C 的 scalar conductivity statement 分开；F266 的 selected 上界五与 headline 三分开；F122 的 lower bound 与 uniform decoder 分开；F376 的旧版本 scope 与新版本修订分开。来源是 Apache-2.0，保留 [LICENSE](LICENSE)；完整原始 attribution 在 canonical source 中继续保留。

## 手动增量检查

只在准备使用新数学结果、主控发现推导障碍，或上游发布相关更新时运行，不创建定期任务。下面步骤从仓库根目录运行，读取变更而不合并上游到当前分支。

```bash
git fetch https://github.com/openai/math.git main:refs/remotes/openai-math-review/main
git rev-parse refs/remotes/openai-math-review/main
git diff fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb refs/remotes/openai-math-review/main -- CONTENTS.md history.md lean/docs/
```

先看 `history.md` 的修订/撤稿、各论文 README 的 version note、CONTENTS 的新/移除/moved entries，以及对应 Lean scope 的精确 statement 变化。新版本可能仍使用同一目录名；F376 box 文件即在 October 7 修复 torus-projection / common-clock 估计，而其目录与首页仍写 October 6。

再只列出核心队列来源及依赖入口的变更。显式重开归档时，把下面的 `watch_paths` 换成 `archive_watch_paths`：

```bash
python - <<'PYCODE'
import json, subprocess
from pathlib import Path
r = json.loads(Path('literature/registry.json').read_text())
subprocess.run(['git', 'diff', '--name-status', r['source_commit'],
                'refs/remotes/openai-math-review/main', '--', *r['watch_paths']], check=True)
PYCODE
```

`watch_paths` 包含论文目录（PDF、README、TeX 与 bibliography）、相关 Lean scope（含当前不存在的 scope）、selected declarations / comparator configs / solution 入口和工具链。完整 Lean import library 不复制进这个目录；证明层的复用需沿 solution imports 在 pinned commit 检查。只变化 import library 时，先问其是否影响正在依赖的 source statement；DPT 独立引理不会因此自动重开。

对相关变化采用三种人工判定：

| 变化 | 处理 |
|---|---|
| 新论文 / 标题或引用调整，未改变当前 DPT 对象和条件 | 记录候选或不处理，现有推导继续使用 pinned source |
| 依赖 theorem 的假设、结论、证明关键步改变，或该 source 被撤稿 | 定位 MAP 的 question / transfer，检查独立 DPT 推导是否仍成立；只重开受影响部分 |
| Lean scope 增加/收窄/换版本 | 更新 statement-level 对应；DPT 推导与 native claim 单独裁决 |

手动检查输出是 **review candidate**。只有变化影响 MAP 的假设、目标、上下界、measurement、反例或 certificate 时，才修改对应推导/优先级。撤稿会改变对原 theorem 的依赖身份；若 DPT 只借方法且已有独立证明，保留该证明并说明来源状态。变更确认前，保留当前 source commit；不要只把 hash 更新成 latest。

本次对照的 history 已列出 October 7 的三篇撤稿，它们不在当前 DPT bundle。对相关 F376 修订，本轮仅核对版本身份并保留方法层使用，没有宣称独立复证流体 theorem。

## 本轮审计与验证

1. **组织批次**：保留 MAP 全文和所有旧来源入口；建立短名 PDF、scope 与 statement 的精确对应。用途是让主控快速调取正确版本，尤其防止 companion/Lean scope 错配。
2. **数学工具批次**：统一 `predictive_state_audit.py` 与 `measurement_factor_audit.py` 的秩/伪逆截止值为 `s > max(atol, rtol*s_max)`。保留既有 CLI、输入和结论范围；数值舍弃的方向继续计入误差残差。
3. **验证批次**：33 个原测试加 4 个解析回归，合计 37 个 synthetic tests。新增例子是 `O=0, P=eps*y, G=y` 的绝对截止反例、弱方向的 `sigma/eps` 噪声放大、相对截止变化和 tangent factor 一致性。两个绝对截止用例先在旧代码失败，再由局部修正通过。

数学上，给定分解 `DG=B DO+A DP+E` 与同一状态球 `||delta h||<=r` 的独立 remainder bounds，误差界仍为

`||E|| r + (C_G+||B|| C_O+||A|| C_P) r² + ||B|| sigma_O + ||A|| sigma_P`。

截断伪逆改变 `A/B/E`，不改变这个三角不等式推导。舍弃方向时不能令它的误差凭空消失；保留弱方向时不能省略 noise gain。这里的 envelope 是输入假设，浮点 SVD 与文件哈希不提供经过 interval 验证的数值证书。

从根目录运行全部 Python 测试：

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s dpt_tools -p 'test_*.py' -v
```

校验阅读快照字节（不是验证定理）：

```bash
python - <<'PYCODE'
import hashlib, json
from pathlib import Path
r = json.loads(Path('literature/registry.json').read_text())
bad = [a['snapshot_path'] for a in r['assets']
       if not Path(a['snapshot_path']).is_file()
       or hashlib.sha256(Path(a['snapshot_path']).read_bytes()).hexdigest() != a['sha256']]
print('Snapshot integrity:', 'OK' if not bad else bad)
raise SystemExit(bool(bad))
PYCODE
```

本轮未收到 native S09 archive，所有代码结果保持 synthetic/conditional 身份。真实 replay 前由主控提供同一 history/query 的对应关系、单位/时标、reference、信息预算、噪声约定与 provenance。当前不实现未定义的 adapter、不合并不同 command 的语义，也不更新 Power Semiconductor 主控的 scientific authority 或仿真预算。
