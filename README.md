# TCMedSeek

**A data-quality-first large language model for Traditional Chinese Medicine.**

**面向传统中医药的、数据质量优先的大语言模型。**

---

## 中文简介

TCMedSeek 是一个中医垂域大语言模型，核心主张是：**制约领域适配效果的是"测量保真前提下的数据质量"，而非训练阶段的堆叠**。

- **极简训练配方**：Qwen3.6-35B-A3B（MoE）底座上仅做单段 LoRA 监督微调，1 个 epoch，无继续预训练、无强化学习、无检索增强；
- **权威精炼数据**：135,797 条监督样本，87% 来自国家规划教材、配套习题集与《中国药典》（2020 年版一部）；逐条溯源到"册 + 行号"（未定仅 0.12%）；证据表先行的合成协议，判废率 8.9% 且废因逐条留档；六通道去污闸 + 独立第二实现复核；
- **闭环精炼**：训练 → 全量实测 → 错题自动归因（缺口 / 已教但错在辨析 / 金标存疑）→ 分类补救 → 回灌重训，共 33 轮迭代；
- **全维度多口径评测**：公开基准 MTCMB（5 维 / 12 子集，本文报告 11 个子集、6,997 题），13 个模型同一冻结协议横评；全部分数在 L0/L1/L2 三档判分口径下从同一份原始输出离线重算，**口径带宽**作为报告量。TCMedSeek 在三档口径下均排名第一（最严苛的 L0 口径领先最强外部基线 9.09 分），自身口径带宽仅 0.57 分。

## English summary

TCMedSeek is a Traditional Chinese Medicine (TCM) domain LLM built on one premise: the binding constraint for domain adaptation is data quality under measurement fidelity, not the accumulation of training stages.

- **Minimal recipe**: single-stage LoRA supervised fine-tuning of one epoch on Qwen3.6-35B-A3B; no continued pre-training, no reinforcement learning, no retrieval.
- **Authoritative, lean corpus**: 135,797 supervised samples, 87% warranted by state-published textbooks, companion exercise sets, and the Pharmacopoeia of the PRC (2020, Part I); per-sample provenance traced to source volume and line (0.12% undetermined); evidence-table-first synthesis with a logged 8.9% rejection rate; six-channel decontamination gates re-checked by an independent second implementation.
- **Closed-loop refinement**: train → full-coverage evaluation → automated error attribution (gap / taught-but-misdiscriminated / suspected reference fault) → class-matched remediation → retrain, for 33 iterations.
- **Full-spectrum, multi-protocol evaluation**: on the public MTCMB benchmark (11 of 12 sub-datasets reported, 6,997 items), 13 systems under one frozen protocol; every score recomputed under three scoring protocols (L0, no extraction, to L2, full extractor) from identical raw outputs, with the protocol bandwidth reported per model. TCMedSeek ranks first under all three protocols (leading the strongest external baseline by 9.09 points at the strictest L0) with a bandwidth of only 0.57 points.

## Repository contents / 仓库内容

| Path | Description / 说明 |
|---|---|
| `manuscript/` | Manuscript draft (DOCX + Markdown), verified reference library, figure plan / 论文稿（Word + Markdown）、已核实参考文献库、图表方案 |
| `figures/` | Figures 1–4 (300 DPI PNG) and the scripts that generate and validate them / 图 1–4 及生成与校验脚本 |
| `supplementary/SupplMaterial.md` | Additional files 1–4 (iteration and remediation ledger; data construction logs; evaluation protocol deviations; baseline exclusions and training details) / 四个附文件整理稿 |
| `source_materials/` | Chinese working documents that the manuscript was written from / 论文写作所依据的中文原始材料 |
| `data_examples/` | Format documentation of the corpus and evaluation artifacts; real data are released with the paper / 数据格式说明（真实数据随论文发布） |

## Data and artifacts release plan / 数据与产物发布计划

The following artifacts are **not** in this repository because of size, and will be released upon publication (or on reasonable request):

- Provenance-annotated training corpus (JSONL with per-sample provenance fields, ~180 MB)
- Full evaluation artifacts: 13-model × 10-subset × 3-protocol matrices, per-item raw outputs and scores (~188 MB)
- LoRA adapters and merged model (~67 GB)
- Evaluation question lists with SHA-256 checksums, aggregation scripts

以下产物因体积原因不在本仓库，将在论文发表时（或按合理请求）发布：逐条溯源标注版训练语料（约 180 MB）、13 模型 × 10 子集 × 3 口径评测矩阵与逐题原始输出（约 188 MB）、LoRA 权重与合并模型（约 67 GB）、题单 SHA-256 与汇总脚本。

## Status / 状态

Manuscript in preparation; target journal: *Chinese Medicine* (BMC / Springer Nature).
论文撰写中；目标期刊 *Chinese Medicine*。

Citation / 引用：[TODO after publication]

Contact / 联系方式：[TODO]
