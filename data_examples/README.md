# Data formats (documentation only)

This folder documents the formats of the artifacts to be released with the paper.
**No real data are included in this repository yet.** All numeric values below are
format illustrations, not samples from the corpus.

## Training corpus (JSONL, one sample per line)

Each of the 135,797 training samples carries the following fields:

| Field | Description |
|---|---|
| `system` | System prompt (present on 100% of samples) |
| `instruction` / `input` | Question text |
| `output` | Reference answer |
| `meta.source` | Build-time source declaration (e.g., textbook volume, pharmacopoeia) |
| `meta.trust_src` | Witness statement: how the facts are warranted (e.g., "textbook syndrome-treatment entry; drug names follow ChP dispensing names") |
| `meta.prov.corpus` | Provenance adjudication result: source corpus, volume, and line |
| `meta.prov.route` | Adjudication route: declared / retro-traced / by-construction / trust_src / undetermined |
| `meta.confidence` | Confidence tier (high / medium / low / unlabelled) |

Validation split: 3,288 samples, same schema. Both files ship with SHA-256 checksums.

## Evaluation matrices

- `matrix_long.csv` — long format, one row per (model, sub-dataset, protocol level):
  `model, dataset, n, level, score` where `level ∈ {L0, L1, L2}`.
- `matrix.json` — the same data with sub-dataset item counts and metric names.
- Protocol bandwidth per model is `score(L2) − score(L0)` over the 10 jointly scored sub-datasets.

## Per-item outputs

For each model and sub-dataset:

- `mid.jsonl` — per-item model output, with the raw generation preserved in the `raw` field.
- `score.json` — per-item score under the official scorer, plus the recomputed L0/L1/L2 levels.

## Reproduction scripts

- Figure generation: `figures/make_figures.py` (matplotlib); geometric validation: `figures/check_figures.py`.
- Leakage gates, provenance tracing, and aggregation scripts are listed in `supplementary/SupplMaterial.md` (Additional files 1–2) and will be released with the paper.

## Provenance summary (already published in the paper)

Undetermined provenance was reduced from 29.7% to 0.12% by retroactive tracing at 86.2%
agreement with build-time declarations (pharmacopoeia 99%, national standard 97%,
case records 96%, exercise sets 87%, textbooks 71%).
