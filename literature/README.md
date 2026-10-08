# DPT 当前核心文献

主控从 [MAP](../DPT_MATH_RESEARCH_MAP.md) 开始。这里放当前课题重要、尚需落实 DPT 推导/验证或确认主控理解的 **7 份 PDF**；每次只读当前问题对应的 2–4 份。已经形成方法分析的材料，也可以因 transfer 尚未落实而留在这里。

主控吸收状态尚未确认。论文位于核心区不表示“从未分析”，也不表示定理已能直接用于 native DPT。核心队列可按 evidence 调整；不会自动改变冻结证据、scientific claim 或仿真预算。

| 核心 PDF | 本次优先落实任务 |
|---|---|
| [F116-A_noncommutative_hitting_point.pdf](F116-A_noncommutative_hitting_point.pdf) | 把当前 command representation 与独立 finite lift / detection 条件对应；确认 theorem 条件是否真正满足。 |
| [F116-B_rational_hitting_lists.pdf](F116-B_rational_hitting_lists.pdf) | 落实每个 inverse occurrence 的 definedness；判断 hitting-list 类是否适用于当前 command，而非直接借用 headline。 |
| [F266_dimension_six_MUB_certificate.pdf](F266_dimension_six_MUB_certificate.pdf) | 把已有 numerical result 的 center/tangent/remainder/readout/provenance 收成可检查证书；确认资源失败仍为 unresolved。 |
| [F365-B_smooth_anisotropic_Calderon.pdf](F365-B_smooth_anisotropic_Calderon.pdf) | 判断简单 inverse/constant-rank theorem 是否已足够；若不足，再迁移 finite-probe / first-order cancellation 的 proof pattern。 |
| [F357_regular_RCD_bi_Lipschitz_coordinates.pdf](F357_regular_RCD_bi_Lipschitz_coordinates.pdf) | 把 rank persistence、gain 和 remainder 接到同一声明邻域；检查 tangent-to-finite-radius 升级是否成立。 |
| [F329_metric_entropy_duality_counterexample.pdf](F329_metric_entropy_duality_counterexample.pdf) | 在 matched history/command bank 上执行 noise-fiber goal-gap 检查；区分压缩 readout 与 archived raw feature。 |
| [F140-A_Gaussian_regression_memory_precision.pdf](F140-A_Gaussian_regression_memory_precision.pdf) | 先落实 elementary goal-packing 下界与信息预算；只在 Gaussian/memory 假设匹配时考虑 source-specific sharp bound。 |

## 对应与维护

- [literature_archive/](../literature_archive/README.md) 保存其余 26 份 PDF、原有方法分析的来源及完整论文对照表。归档材料按 reopen condition 调用。
- [registry.json](registry.json) 是两个目录共用的来源索引，记录 reading tier、pending task、未确认的主控吸收状态与精确 source commit/hash。
- 核心 Lean 阅读快照仅保留 F116 的两个 selected statement、F266 的 MUB statement、F329 的反例 statement，以及 F140 的 memory/precision statement和相关 scope。scope 中其他 companion 链接可指向归档。F365-B 无对应 selected coverage；F357 在 pinned commit 无 scope，不给它们借用 sibling 的形式化背书。
- Selected-statement `.lean` 是 Comparator 命题声明，不是独立证明包；完整 Lean proof、imports 和 comparator 配置继续位于原仓库 [lean/](../lean/)。
- [完整来源对照、手动增量检查和校验命令](../literature_archive/README.md#手动增量检查) 保留在归档说明。默认 `watch_paths` 只检查核心队列，重开归档时使用 `archive_watch_paths`。

快照源：OpenAI `openai/math` commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`。PDF 与 selected statement 的内容字节保持不变；scope 仅调整归档链接。[LICENSE](LICENSE) 保留原许可。
