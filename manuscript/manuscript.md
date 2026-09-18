# TCMedSeek: a data-quality-first approach to building and evaluating large language models for Traditional Chinese Medicine

[TODO: authors and affiliations]

## Abstract

**Background:** Large language models (LLMs) for Traditional Chinese Medicine (TCM) are typically developed by accumulating training stages and corpus scale. Two connected problems receive little attention. Training corpora and public benchmarks share an examination-system origin, which inflates scores through contamination. Scoring pipelines and faulty reference answers deflate scores, so benchmark errors operate in both directions. We hypothesized that data quality under measurement fidelity, rather than training-stage accumulation, is the binding constraint for TCM domain adaptation.

**Methods:** We built TCMedSeek by fine-tuning Qwen3.6-35B-A3B with a single-stage, one-epoch LoRA supervised fine-tuning on 135,797 samples. Of these, 87% derive from state-published textbooks, companion exercise sets, and the 2020 pharmacopoeia, with per-sample provenance traced to source volume and line (0.12% undetermined). Synthesis proceeds from fixed evidence tables before phrasing, with an 8.9% logged rejection rate. Six leakage channels, each introduced by a real contamination incident, are re-checked by an independent second implementation. Across 33 data-model iterations, closed-set errors were automatically attributed as knowledge gap, taught-but-misdiscriminated, or unmatched, and remediation was matched to error class. We evaluated 11 of 12 MTCMB sub-datasets (6,997 items) against 11 external baselines and the untrained base under one frozen protocol. Identical raw outputs were re-scored under three extraction protocols, from strictest (L0) to most lenient (L2), with an empirically calibrated ±1.0-point noise band and a constant-prescription degenerate baseline.

**Results:** TCMedSeek ranks first under all three protocols. Under the strictest L0 it averages 73.97 over 10 jointly scored subsets, exceeding the strongest external baseline by 9.09 points. Its protocol bandwidth is 0.57 points, versus up to 16.93 for baselines. Averaged over 11 subsets it gains 6.96 points over its untrained base, improving 10 subsets. Item-level flips are directional on all four closed subsets, for example 225 improved versus 121 worsened on the 4,800-item examination subset. Attribution of 744 errors yielded 61% taught-but-misdiscriminated, 9% knowledge gaps, and 30% unmatched. Contrastive remediation, not volume re-teaching, repaired the dominant class. The degenerate baseline outscores all systems on prescription recommendation, flagging a construct-validity failure in that subset.

**Conclusions:** A compact, authoritative, provenance-traced, and decontamination-gated corpus lets a single fine-tuning stage lead the current TCM LLM field. This holds when evaluation reports scoring sensitivity, calibrated noise, and degenerate baselines. The attribution-first refinement loop and the reporting practices proposed here generalize to other vertical domains where training and evaluation materials share origin.

**Keywords:** Traditional Chinese Medicine; large language models; supervised fine-tuning; data quality; benchmark contamination; evaluation reliability; LoRA

**Trial registration:** Not applicable.

## 1 Introduction

Traditional Chinese Medicine (TCM) is a core component of Chinese medical heritage. Its theoretical system has evolved over more than two millennia and remains active in contemporary healthcare, particularly across East Asia [R39]. Tremendous TCM knowledge is preserved in ancient books and embodied in accumulated clinical experience. This body of knowledge continues to serve as a foundation for modern TCM research and innovation [R39]. The central reasoning procedure of TCM, syndrome differentiation (bianzheng), requires multi-factor inference over symptoms, signs, and tongue and pulse manifestations to determine treatment principles and prescriptions [R40]. Artificial intelligence approaches have been applied to these tasks with growing intensity, from machine learning for tongue-image diagnosis to deep learning for herbal identification [R42].

In parallel, large language models (LLMs) [R34] such as GPT-4 [R35], Qwen3 [R36], and DeepSeek-V3 [R37] have advanced biomedicine considerably [R38]. They now support medical knowledge representation, diagnostic reasoning, and clinical decision support. A growing family of TCM-oriented LLMs has emerged. BianCang applies continued pre-training followed by supervised fine-tuning for syndrome differentiation and diagnosis [R01]. TCMChat and Lingdan target domain question answering, clinical reasoning, and prescription recommendation [R10, R11]. ShizhenGPT extends TCM modeling to a multimodal regime covering medicinal recognition and visual diagnosis [R02]. HuatuoGPT-o1 pursues verifier-based reinforcement learning for medical reasoning [R04]. ZhongYan integrates multi-source knowledge graphs with a three-stage training pipeline and retrieval augmentation [R12]. Complementary lines of work address the multimodal nature of TCM diagnostics, including tongue-image analysis [R15, R17, R20] and herbal image recognition [R16, R18, R19]. General Chinese medical models such as HuatuoGPT-II, DISC-MedLLM, PULSE, and Baichuan-M1 are frequently adopted as reference points in TCM evaluations [R03, R05, R06, R07].

Despite this rapid progress, development practice in the field is shaped by a scale race whose two blind spots are directly connected: data quality and measurement fidelity. First, TCM corpora are commonly assembled at large scale from web-scraped question banks, dialogue data, and model-generated instruction pairs. Few published reports detail their decontamination, deduplication, or source verification. Work in general NLP has shown that benchmark contamination systematically inflates reported performance [R25, R26] and that model families can overfit widely used benchmarks [R27]. The issue is acute in TCM. National licensing-examination questions serve simultaneously as training material and as evaluation material, so a model can score highly by memorizing examination items rather than mastering the discipline.

Second, measurement error also operates in the opposite direction. Exact-match and extraction-based scoring pipelines can mark substantively correct answers as wrong, and reference answers themselves may contain errors or ambiguities. ZhongYan's developers reported that iterative fine-tuning on incorrectly answered questions yielded limited gains and attributed this to ambiguous ground truth, leaving systematic treatment of the problem to future work [R12]. Taken together, benchmark scores in this domain are unreliable in both directions. A point lost is not necessarily a point wrong, and a point gained is not necessarily knowledge. Any claim about TCM LLM capability therefore requires both decontaminated training data and a multi-protocol evaluation design that quantifies how scores depend on the scoring pipeline itself.

This study presents TCMedSeek, a TCM LLM built on the premise that data quality, rather than the accumulation of training stages, is the binding constraint for domain adaptation. TCMedSeek is fine-tuned from Qwen3.6-35B-A3B, a 35-billion-parameter mixture-of-experts model, through a single-stage LoRA [R30] supervised fine-tuning of one epoch. It uses no continued pre-training, no reinforcement learning, and no retrieval augmentation. Its contributions are threefold.

First, an iterative, human-in-the-loop data refinement pipeline. Across 33 data-model co-iterations, every corpus revision was driven by full-coverage re-evaluation, automated attribution of closed-set errors, and classified remediation. Knowledge gaps were filled with new material. Discrimination failures were addressed with targeted contrastive cards. Suspected reference errors were escalated to authoritative arbitration rather than silently absorbed. Six independent leakage channels, each introduced after a real contamination incident, guard the corpus. Every zero-leak verdict is confirmed by a second, independently implemented checker.

Second, a full-spectrum, multi-protocol evaluation. We evaluate on MTCMB [R21], a public multi-task benchmark spanning five dimensions and 12 subsets, and report 11 subsets comprising 6,997 items. Thirteen models were compared under one frozen protocol on the same hardware. All scores were recomputed under three scoring protocols of increasing extraction leniency, so that each model's sensitivity to the scoring pipeline is exposed rather than hidden. Score differences are interpreted against an empirically calibrated noise band of ±1.0 percentage point, not against a statistical convenience threshold.

Third, an authoritative and lean training corpus with effective synthesis. The corpus contains 135,797 supervised samples. Of these, 87% originate from state-published planning textbooks, their companion exercise sets, and the Pharmacopoeia of the People's Republic of China (2020 edition). The correctness of most training facts is thus warranted by the publications themselves rather than by post-hoc filtering. Synthesis follows an evidence-table-first protocol in which verifiable facts and admissible entities are fixed before question phrasing is composed. Any sample failing a hard acceptance gate is discarded in full, yielding a logged rejection rate of 8.9%. Every sample is traced to its source volume and line, leaving only 0.12% of provenance undetermined.

TCMedSeek ranks first among the 13 compared models under all three scoring protocols. Under the strictest protocol, which applies no answer extraction, TCMedSeek averages 73.97 over the 10 jointly scored subsets and leads the strongest external baseline by 9.09 points. The spread between its strictest and most lenient scores is 0.57 points. Several baselines gain more than 5 points from the scoring pipeline alone. Relative to its untrained base model, TCMedSeek improves by 6.96 points averaged over the 11 evaluated subsets, and item-level flip analysis confirms that the improvements are directional rather than retraining noise. These results support a concrete claim. With authoritative, verified, and compact data, a single fine-tuning stage suffices to reach the front of the current TCM LLM field. The claim is worth making because the evaluation protocols behind it are robust to scoring-pipeline choice.

The remainder of this study proceeds as follows. Section 2 reviews related work. Sections 3 and 4 present the data refinement pipeline, the training configuration, and the evaluation design. Section 5 reports the results. Sections 6 and 7 give the discussion with limitations and the conclusions.

## 2 Related Work

### 2.1 TCM-oriented large language models

Efforts to adapt LLMs to TCM can be organized along a capability-and-modality axis. The largest cluster consists of text-based dialogue and question-answering models. Sunsimiao and PULSE represent early lightweight fine-tuning efforts for Chinese medical dialogue [R07, R08]. Zhongjing couples domain pre-training with expert feedback over real-world multi-turn dialogues [R09]. TCMChat is tuned on curated TCM texts and QA pairs for herbal and diagnostic reasoning [R10]. Lingdan introduces specialized modules for TCM question answering and prescription recommendation [R11]. BianCang applies continued pre-training for knowledge injection followed by fine-tuning for knowledge activation, partly on a dataset derived from the national pharmacopoeia [R01]. Recent Qwen3.5-based systems such as Fu-TCM-27B [R13] and Xinghe1.2-9B [R14] continue this line on newer base models.

A second cluster pursues explicit reasoning. HuatuoGPT-o1 constructs verifiable medical problems with a medical verifier and applies verifier-guided search followed by reinforcement learning with verifier-based rewards [R04].

A third cluster is multimodal. TCM diagnosis rests on inspection, listening and smelling, inquiry, and pulse-taking, and much of this signal is not textual. Deep learning for tongue-image analysis has a long history [R17] and has reached prospective multicentre clinical deployment for disease screening [R20]. Recent work couples tongue images with multimodal LLMs and retrieval [R15, R16]. Image-based identification of Chinese materia medica likewise predates LLMs [R18, R19]. It has entered the multimodal-LLM era through ShizhenGPT, which pretrains on the largest TCM corpus to date and introduces a visual benchmark for medicinal recognition and visual diagnosis [R02].

A fourth cluster treats the LLM as a component of a knowledge system. ZhongYan builds multi-source parallel knowledge graphs and applies them in preference optimization and retrieval-augmented generation [R12].

Finally, general Chinese medical models, including HuatuoGPT-II [R03], DISC-MedLLM [R06], and Baichuan-M1 [R05], are trained on mixed corpora in which TCM is one constituent among many. They are frequently included in TCM evaluations, and we follow this convention. Their contrast helps separate pan-medical from TCM-specific competence.

TCMedSeek belongs to the text-based cluster. It differs from the models above in where the engineering effort is spent: construction concentrates on per-sample verification, decontamination, and provenance rather than on accumulating training stages.

### 2.2 Training-stage combinations

Vertical TCM models are conventionally described by their position on a stage ladder. The stages run from continued pre-training (CPT) for domain knowledge injection and supervised fine-tuning (SFT) for task alignment. Later stages add preference optimization such as direct preference optimization (DPO) [R31], reinforcement learning with verifiable rewards, and retrieval or knowledge-graph augmentation. BianCang traverses CPT and SFT [R01]. ZhongYan traverses all of the above, with 3.9 billion tokens of CPT corpus, more than 272,000 SFT samples, DPO with knowledge-graph-consistency rewards, and retrieval augmentation [R12]. HuatuoGPT-o1 applies reinforcement learning with verifier-based rewards on 40K verifiable problems [R04]. Group relative policy optimization (GRPO) [R32] offers an efficient policy-optimization variant that several medical reasoning efforts adopt. Closed-set TCM tasks are, in principle, programmatically verifiable and thus well suited to it. Examples include multiple-choice examination QA, multi-label syndrome classification, and set-matched prescription recommendation. Catastrophic forgetting is a recurring motivation for mixing general-domain data into CPT corpora [R33].

TCMedSeek occupies a minimal position on this ladder: a single LoRA [R30] SFT stage of one epoch, with no CPT, no preference optimization, no RL, and no retrieval component. This choice is a form of experimental control. The contribution we aim to isolate is the effect of data quality on a fixed, simple recipe, and each additional stage would confound that attribution. The ablation question of whether more stages would help is legitimately interesting but is not the question this study answers.

### 2.3 Data: scale, synthesis, and integrity

Published TCM training corpora draw on ancient texts, planning textbooks, examination question banks, electronic health records, and synthesized instructions. The prevailing direction is scale. ZhongYan's CPT corpus comprises roughly 3.9 billion tokens from 1,500+ ancient texts, 60+ textbooks and dictionaries, 32k herbal and formula records, and 45k clinical records, with a further 272,000+ SFT samples [R12]. ShizhenGPT curates over 100 GB of text and 200 GB of multimodal data [R02].

Descriptions of sample-level quality control are, by contrast, uncommon in this literature. The phrase "data contamination" rarely appears in TCM model reports, even though licensing-examination questions are both a standard training source and the substrate of most TCM benchmarks. In the general LLM literature, contamination is a recognized first-class threat to evaluation validity. Training-set overlap with benchmark test splits inflates scores [R25]. Contamination can be detected and quantified at instance and partition level [R26]. Commissioned replacement benchmarks such as GSM1k reveal systematic overfitting to established benchmarks in several model families [R27]. A parallel line of results supports the opposite lever, data quality. Carefully curated small instruction sets suffice for strong alignment [R28]. "Textbook-quality" data can substitute for orders of magnitude more web text [R29].

TCMedSeek is constructed in this second spirit, applied to a vertical domain where authority is verifiable. In total, 87% of its 135,797 samples derive from state-published textbooks, companion exercise sets, and the national pharmacopoeia, with per-sample provenance recorded to source volume and line. Synthesis proceeds from fixed evidence tables rather than free-form generation, with an 8.9% logged rejection rate. Six leakage channels screen the corpus, each retained after being introduced by a real contamination incident, and every zero-leak verdict is confirmed by an independent second implementation. No published TCM model we are aware of reports a comparable decontamination protocol. We state this as an observation about reporting practice, not as a claim about unpublished practice.

### 2.4 Benchmarks and measurement fidelity

Public TCM benchmarks have matured rapidly. TCMBench provides a broad multi-dimension evaluation [R22]. TCM-5CEval probes deep clinical-research competence [R23]. TCM-Eval contributes an expert-level dynamic and extensible design [R24]. MTCMB spans five dimensions across 12 sub-datasets, integrating licensing examinations, clinical case records, and classical texts, with frozen public data [R21]. Self-constructed, unpublished benchmarks also persist in this literature. ZhongYan evaluates on ZhongYiBench, whose items are not publicly released [R12], which places its headline numbers beyond third-party reproduction.

Two measurement problems receive less attention. First, scores can depend strongly on the scoring pipeline itself. An exact-match pipeline that receives an answer phrased as "the answer is B" may score it as wrong. Models also differ widely in how much apparent performance lenient extraction recovers. Second, benchmarks can exhibit construct-validity failures at the subset level. We show in Section 5 that a constant-prescription degenerate baseline outscores all compared models on the prescription-recommendation subset of MTCMB. Subset-level gains there must therefore be interpreted with care. Prior evidence already hints at reference-quality problems: ZhongYan attributes the limited benefit of error-driven fine-tuning to ambiguous ground truth [R12]. Our evaluation design responds to both problems. All 13 models are re-scored under three protocol levels on identical raw outputs. Per-model protocol bandwidth is reported alongside point estimates, and the noise band is calibrated empirically, in the spirit of contamination-aware re-evaluation in the general literature [R25, R27].

In summary, existing work has explored an expanding space of TCM model architectures, training stages, and data sources. What has been missing is a model whose training data and evaluation protocol are jointly engineered for integrity. The corpus should make each sample's authority and provenance explicit and police contamination by construction. The evaluation should treat the scoring pipeline as a studied variable rather than a silent constant. TCMedSeek attempts to fill this gap. Its results suggest that, under such conditions, a single fine-tuning stage on a compact corpus suffices to lead the current field.

## 3 Data refinement pipeline and training configuration

### 3.1 Overview

TCMedSeek is produced by a closed-loop data refinement framework rather than by a stage-accumulating training recipe. Each iteration executes the cycle shown in Fig. 1. The system trains on the current corpus, re-evaluates the full benchmark slice, and extracts closed-set errors. Each error is attributed automatically to a knowledge skeleton, and suspected reference faults are arbitrated against authority. A remediation matched to the error class is then applied, folded back into the corpus, and followed by retraining. The framework ran 33 data-model co-iterations, each archived as a frozen corpus release. The complete iteration ledger, including the leak-cleanup history of every revision, is provided in Additional file 1. The main text reports the delivered configuration.

![**Fig. 1** The TCMedSeek construction loop. Each iteration performs single-stage LoRA SFT, evaluates the full frozen slice under three protocol levels, extracts closed-set errors, and attributes them automatically against the knowledge skeleton. Remediation is matched to the error class, and revisions re-enter the corpus only through the six-channel decontamination gate with an independent second implementation. The loop ran for 33 iterations.](figures/fig1_workflow.png){width=6.3in}


Three design principles govern the framework. First, measurement precedes optimization. No remediation is decided from training loss; all decisions come from full-coverage re-evaluation on a frozen slice. Second, every training sample must be verifiable. Its facts carry the authority of a published source, its provenance is recorded to source volume and line, and its admission is policed by hard gates. Third, a gate that reports zero may be blind rather than clean. Every zero verdict is confirmed by a second, independently implemented checker, and every escaped contaminant adds a new, permanent detection channel. All engineering complexity is located on the data side by design. The training side is held to a single supervised fine-tuning stage, so that the effect of data quality is not confounded by additional training stages.

### 3.2 Authoritative corpus construction

The final training corpus contains 135,797 supervised samples, with 3,288 reserved for validation, all carrying a system prompt. Sources are dominated by state-published, authoritative materials (Table 1). The 35 volumes of the 14th Five-Year Plan textbooks series for TCM contribute 75,600 samples (55.67%). Their 18 companion exercise volumes contribute 24,645 (18.15%). The Pharmacopoeia of the People's Republic of China, 2020 edition, Part I, contributes 17,684 (13.02%). Together these three classes account for 87% of the corpus, and the correctness of their facts is warranted by the publications themselves. The remainder comprises 10,764 public real-world case records (TCM-SD), 1,969 entries from the national standard clinical terminology for syndromes, and 911 samples from classical texts. A further 2,315 samples are hand-written or per-item rewrites, 1,027 are general-alignment samples, and 716 are constructed-format samples. The final 166 samples (0.12%) could not be provenance-determined. A corpus of digitized physician case records was evaluated and rejected entirely. Even samples passing all four screening gates retained OCR corruption in five of eight inspected cases.

Table 1. Composition of the training corpus.

| Source class | Samples | Share |
|---|---:|---:|
| 14th Five-Year Plan textbooks (35 volumes) | 75,600 | 55.67% |
| Companion exercise sets (18 volumes) | 24,645 | 18.15% |
| Pharmacopoeia of PRC (2020, Part I) | 17,684 | 13.02% |
| TCM-SD public case records | 10,764 | 7.93% |
| Hand-written / per-item rewrites | 2,315 | 1.70% |
| National standard syndrome terminology | 1,969 | 1.45% |
| General alignment / instruction following | 1,027 | 0.76% |
| Classical texts | 911 | 0.67% |
| Constructed-format samples | 716 | 0.53% |
| Undetermined | 166 | 0.12% |
| **Total (train / val)** | **135,797 / 3,288** | 100% |

![**Fig. 2** Corpus composition and provenance. (a) Source classes by share of the 135,797 training samples; the three state-published classes cover 87%. (b) Provenance adjudication routes (log scale); retroactive tracing reduced undetermined provenance from 29.7% to 0.12%.](figures/fig2_corpus.png){width=6.3in}


Per-sample provenance is established by an archival matching procedure that locates each sample in its source volume and line. The adjudication order is fixed: build-time source declarations take precedence as process truth, and retroactive matching serves as external evidence. In a single full-corpus pass, the procedure reduced undetermined provenance from 40,263 samples (29.7%) to 166 (0.12%). Agreement with build-time declarations reached 86.2% overall, with pharmacopoeia at 99%, national standard at 97%, case records at 96%, exercise sets at 87%, and textbooks at 71%. Calibration on a labeled subset exposed and fixed three defects. Template phrases shared across exercise sections were masked before matching. Twenty-seven same-title older textbook editions were separated as a distinct class. Pure match-length comparison was replaced by an origin-priority rule, since exercise texts quote textbook and pharmacopoeia wording verbatim; the priority order runs from pharmacopoeia and national standard, through textbooks and classics, to exercise sets, and raised overall agreement from 80.6% to 86.2%. Where multiple candidate sources are genuinely consistent with the content (6,860 samples), the corpus records the candidate list rather than forcing a single label.

### 3.3 Evidence-table-first synthesis

Synthetic instruction data are generated under an ordering constraint: verifiable facts first, phrasing second. For each generation batch, an evidence table fixes the admissible facts and an entity whitelist drawn from curated trusted tables. These tables cover 379 and 384 formula records, 2,097 pharmacopoeia entries, 2,012 national-standard syndrome entries, and 751 textbook syndrome-treatment entries. The last is used only as a pairing source, never as a sole basis for a question. The generation model, or a human writer, only composes the question phrasing. The system prompt forbids answers from exceeding the given material and forbids citation of the source medium. Each sample draws one of six to twelve question angles to prevent collapse onto a single template.

On collection, every sample passes a battery of hard gates, and failure of any single gate rejects the whole sample, with no touch-up. The gates cover length bounds and format checks; bans on examination-style phrasing and on referencing source media in answers; rejection of non-answers; a rule that the question must name its subject entity; composition completeness for combined-formula questions; presence of rule-witnessed terms in syndrome-element answers; a requirement that any stated dosage appear verbatim in the pharmacopoeia source; a toxicity-mention requirement for toxic herbs; and a cap of 12% on the per-batch frequency of any masked question skeleton. Across 3,730 collected samples, 331 (8.9%) were rejected, with every rejection reason logged (Additional file 2).

Remediation cards built from observed errors follow stricter witness discipline. A card may only be created if an independent textual witness, from the textbook corpus, the national standard, or the pharmacopoeia, is located for the target fact; no witness, no card. The card question must not reproduce the original item. A longest common substring of 10 or more characters with the original stem classifies the card as leakage and rejects it. The reference answer must literally contain the gold answer. An earlier check comparing only the first four characters was found to admit reverse-teaching cards and was replaced. Discrimination cards must mention the confusable option, since a card that does not name the distractor teaches no boundary. Hedging phrases that extrapolate beyond the witness, such as "although not directly mentioned" or "it can be inferred", are rejected. Answers sharing fewer than three 4-grams with the witness text are judged detached and rejected. Finally, suspected reference faults are re-examined by a blind re-answer protocol that scores without seeing the gold answer. Of 79 items flagged this way, 29 were overturned. Arbitration rather than assumption therefore governs the reference-fault class in Section 3.6.

### 3.4 Six-channel decontamination

Training sources (national examination exercise banks) and benchmark sources (national licensing examinations) share origin, so contamination policing is structural. The corpus is screened by six leakage channels, each introduced in response to a specific contamination incident and retained permanently. Channel A checks verbatim normalized stem matches, and channel B checks containment of a gold stem within a training stem. Channel C combines option fingerprints with stem containment. Channel D, the short-stem channel, combines option fingerprint, selected-answer text, and stem similarity at a 0.8 threshold; it was added after a legacy gate was found to skip all 1,834 short-stem items wholesale. Channel E combines option fingerprint, selected-answer text, and stem similarity at 0.6; it was added after option dictionaries rendered the legacy option parser ineffective. Channel F applies a 40-character sliding-window index over the entire benchmark text, including answer fields; it was added after leaks were discovered in answer text rather than question text.

Cumulative cleanup removed 489 samples across four waves. The first wave removed 251 items, detected by a normalized 3-gram stem gate after the initial 30-character fragment gate missed near-verbatim examination variants. The second wave removed 167, including 110 items whose leakage had been disguised by reordering symptom phrases; these were caught by a character-multiset Jaccard check that is invariant to reordering. A threshold-tightening wave removed 7 after the containment threshold tightened from 40 to 12 characters. The final wave removed 64 via the new D, E, and F channels.

Two aspects of this protocol are, to our knowledge, unreported in existing TCM LLM work, and we state them as observations about reporting practice. First, thresholds are calibrated, not assumed. The stem gate operates at 3-gram Jaccard 0.45 for long stems of 25 or more characters, where manual verification found paraphrases of the same case. For short stems it operates at 0.75, because structural similarity inflates Jaccard there: "the effect of Xiangjiang is" versus "the effect of Muxiang" scores 0.71 while being a different question. Second, deletion is bounded by a same-item rule. Identical or paraphrased examination items are deleted; overlapping knowledge points are not, since deleting every knowledge point touched by an examination would amount to deleting the curriculum itself. A coverage recheck after the final cleanup confirmed retention of, for example, 1,978 occurrences of the concept "jinye" (body fluids) and 387 occurrences of the formula Linggui Zhugan Decoction. Every zero-leak verdict from the primary implementation is reconfirmed by a second, independently written checker before any release.

### 3.5 Model and training configuration

TCMedSeek is fine-tuned from Qwen3.6-35B-A3B [R36], a 40-layer sparse mixture-of-experts model, with LoRA [R30] for one epoch and nothing further. There is no continued pre-training, no preference optimization, no reinforcement learning, and no retrieval component. LoRA (rank 64, alpha 128, dropout 0.05) targets 220 modules covering all 40 layers via a regular expression over module names. This is an implementation point worth recording. The architecture mixes self-attention and linear-attention layers, and the conventional q/k/v/o target list would cover only one quarter of layers. Routed experts and routers are untouched by design. Training uses an effective batch of 28 (7 GPUs × 4) at a learning rate of 1.18 × 10^-4, scaled from a batch-20 baseline by the square root of the batch ratio. The length cutoff is 1,536 tokens, under which zero of 135,797 samples are truncated; the longest sample spans 1,444 tokens. Training completes 4,850 steps in 9,856 s at a peak memory of 82.04 of 97.9 GB, with a final training loss of 0.8694.

Adapter integration is verified bitwise. All 220 targeted modules are confirmed merged, with 1,045 of 1,045 indices accounted for. Merged modules differ from the base, with relative changes of 9.9% and 9.3% for two audited module types. Untouched modules, including all routed experts and routers, are bit-identical to the base. This excludes both failure modes of an accidental no-op and an accidental out-of-scope merge. Validation loss is tracked per capability dimension but is not used to judge progress, for a documented reason. Prescription-dimension loss ranks among the lowest of all dimensions (0.2373), while measured prescription-recommendation performance is the only declining subset in the final comparison. All progression decisions in the loop are made from full-coverage re-evaluation on the frozen slice, never from loss.

### 3.6 Attribution taxonomy and classified remediation

At each iteration, every closed-set error, from multiple-choice and multi-label items, is extracted and attributed automatically against a knowledge skeleton index of the corpus. The procedure yields one of three classes: knowledge gap, meaning the topic is not covered by any training sample; taught-but-misdiscriminated, meaning the topic is covered and the error matches a confusable neighboring concept; or unmatched. The final attribution wave covered 744 errors: 68 knowledge gaps, 454 taught-but-misdiscriminated, and 222 unmatched.

Remediation is matched to the class (Algorithm 1). Gaps receive new corpus material. Discrimination failures receive contrastive cards that name the confusable option. Adding further knowledge volume is not applied for this class: the missing competence is the boundary, not the fact, and our data show that re-teaching covered knowledge does not repair such errors. Suspected reference faults are escalated to authority arbitration. A fault may be classified as a gold-answer or scoring artifact only with evidence independent of model scores, namely the authoritative document itself, item-level content inspection, or the official scorer's source code. Absent such evidence, the item remains attributed to model deficiency. Under this discipline, 143 items are registered as suspected reference faults and five pharmacopoeia-level discrepancies are recorded. Pending independent confirmation by licensed physicians, they are reported as discrepancies, not corrections.

**Algorithm 1** Iteration of the refinement loop (one pass).
```
Input: corpus D_t, frozen evaluation slice S, trained model M_t
1  M_t ← SFT(base, D_t)                        # single-stage LoRA
2  R ← M_t evaluated on S (frozen protocol)
3  E ← extract closed-set errors from R
4  for e in E:
5     a(e) ← attribute(e | knowledge skeleton of D_t)
6        # ∈ {gap, misdiscrimination, unmatched}
7     if a(e) = gap:            queue new corpus material with provenance
8     if a(e) = misdiscrimination: queue contrastive card (witness required,
9                                  distractor must be named, LCS<10 vs stem)
10    if suspected reference fault:
11       require score-independent evidence, else reclassify as model deficiency
12 D_{t+1} ← D_t + accepted queue − contamination deletions
13 (six-channel gate + independent re-implementation must both report zero)
14 goto 1 until delivery criteria met
```

Gain detection across retrainings must respect the retraining perturbation tax. Retraining on near-identical data produces approximately 4.3% undirected answer flips, concentrated on a stable band of roughly 665 swing items and independent of corpus changes. Mean-score movement within this tax is therefore uninformative. Gains are claimed only when flips are directional, that is, when items changed from wrong to right outnumber the reverse beyond the tax. The directed-flip statistics of the final model are reported in Section 5.5.

## 4 Evaluation design

### 4.1 Benchmark and protocol

Evaluation uses MTCMB [R21], a public multi-task benchmark of five dimensions and 12 sub-datasets (7,100 items). The dimensions are knowledge QA (TCM-ED-A, TCM-ED-B, TCM-FT), language understanding (TCMeEE, TCM-CHGD, TCM-LitData), diagnostic reasoning (TCM-MSDD, TCM-Diagnosis), prescription recommendation (TCM-PR, TCM-FRD), and safety (TCM-SE-A, TCM-SE-B). We run 11 of 12 sub-datasets, totaling 6,997 items. TCM-FT is omitted because its prompt configuration is absent from the official release, which aborts the evaluation chain. The official few-shot prompt strategy is used throughout, with frozen decoding: greedy search, repetition penalty 1.05, and a maximum of 1,024 new tokens. Models are admitted through the extension point designated by the official framework. Four deviations from the official protocol are disclosed in full in Additional file 3. They are an answer-extraction bridge required for the comparison of Section 4.3, a thinking-mode implementation difference, the omitted sub-dataset, and our frozen decoding parameters. The bridge is quantified in Section 4.3 rather than ignored.

### 4.2 Comparative panel

Thirteen systems are compared under one frozen protocol on one machine: TCMedSeek, its untrained base, and 11 external baselines. The baselines were selected to cover the field structurally. TCM vertical models include BianCang-7B/14B [R01], ShizhenGPT-7B/32B [R02], Xinghe1.2-9B [R14], Sunsimiao-7B [R08], and Fu-TCM-27B [R13], which shares the Qwen3.5-27B base family at comparable scale to ours. Pan-medical and Chinese medical coverage is provided by Baichuan-M1-14B [R05] and HuatuoGPT2-7B/34B [R03]. HuatuoGPT-o1-8B [R04] represents medical reasoning with long chains of thought. Six candidate baselines were excluded before any score was seen, for structural reasons recorded in Additional file 4. Examples include a BLOOM-family model without fused-attention kernels, a base model whose 2,048-token context cannot hold the few-shot prompt, and a model whose published weights are quantization-only. Batch sizes are determined per model, with automatic re-splitting on out-of-memory events.

### 4.3 Three scoring protocol levels and bandwidth

Generation-task scoring pipelines differ in how much they extract from raw model output, and this difference is itself model-dependent. All 13 systems are therefore scored three times from the same raw outputs, recomputed offline at zero additional inference cost. L0 applies no extraction and feeds raw output to the official verbatim comparator. L1 applies first-option-letter extraction only, approximating the original official regular expression. L2 applies our full extractor, which strips thinking traces and markup, extracts option letters and lists, and falls back to content-based comparison. For each model we report the protocol bandwidth, L2 minus L0, as a first-class quantity. It measures how much of a model's apparent performance is contributed by the scoring pipeline rather than the model. Because our L2 pipeline is not the official one, our scores are never placed in the same table as official leaderboard values. Where the official leaderboard is discussed, it is quoted separately with the pipeline difference stated.

### 4.4 Noise band and directionality

Score differences are interpreted against an empirically calibrated noise band of ±1.0 percentage point. The band is estimated from within-group contrasts over duplicate and near-duplicate items, with an observed range of 0.3 to 1.4%, rather than from a sample-size formula. The latter yields roughly 4 points here and would bury real effects in both directions. For comparisons of our model against its own base, the directed-flip criterion of Section 3.6 applies in addition.

### 4.5 Degenerate baseline and judge-stability disclosures

For the prescription-recommendation subset, we evaluate a degenerate baseline that outputs one constant prescription regardless of input. It scores 0.4341, above every compared model. Subset-level gains on this subset are therefore reported only alongside this baseline, and claims of patient-specific improvement there would require a permutation test over case-specific gains. TCM-SE-A requires an external LLM judge, and the official judge model is unavailable to us. This subset is accordingly scored by a fixed alternative judge under the same rubric and the same gold answers, for the untrained base and TCMedSeek only. Consequently SE-A appears only in the base-versus-TCMedSeek comparison as a within-judge difference (63.90 to 72.50 under the same judge, rubric, and gold answers), never in the 13-model horizontal table.

### 4.6 Aggregation discipline

Two aggregation schemes are used and never mixed in one table. The horizontal 13-model comparison uses summarize3, under which generation tasks contribute ROUGE-1 only. The longitudinal base-versus-TCMedSeek comparison uses a four-metric average of ROUGE-1, ROUGE-L, BERTScore, and BLEU. The two schemes produce different numbers from identical raw scores, for example 72.63 versus 67.11 on the same subset. This is expected and is footnoted wherever both appear.

## 5 Results

### 5.1 Main comparison under three scoring protocols

Table 2 reports the 10-subset simple average for all 13 systems under the three scoring protocols of Section 4.3, computed from identical raw outputs. TCMedSeek ranks first under all three levels. Under L0, the strictest level, which applies no answer extraction and is therefore maximally unfavorable to our pipeline, TCMedSeek scores 73.97 and leads the strongest external baseline, BianCang-14B at 64.88, by 9.09 points. Under L2 it scores 74.54. Its closed-set average over examination and multi-label subsets is 82.46 and is unchanged across all three protocols. For the subsets where extraction cannot contribute, the bandwidth is exactly zero.

Table 2. 10-subset average under three scoring protocols (L0, no extraction; L1, first-letter extraction; L2, full extractor). Bandwidth is L2 minus L0.

| # | Model | Base / scale | L0 | L1 | L2 | Bandwidth |
|---:|---|---|---:|---:|---:|---:|
| 1 | **TCMedSeek** | Qwen3.6-35B-A3B + LoRA | **73.97** | **73.97** | **74.54** | +0.57 |
| 2 | Untrained base (35B-A3B) | Qwen3.6-35B-A3B | 62.91 | 67.85 | 68.53 | +5.62 |
| 3 | ShizhenGPT-32B-LLM | Qwen2 dense 32B | 64.80 | 64.80 | 66.04 | +1.24 |
| 4 | BianCang-14B | Qwen2.5-14B | 64.88 | 64.88 | 65.05 | +0.17 |
| 5 | Xinghe1.2-9B | 9B | 62.21 | 62.50 | 63.38 | +1.17 |
| 6 | Baichuan-M1-14B | 14B | 51.18 | 53.57 | 60.42 | +9.24 |
| 7 | BianCang-7B | Qwen2.5-7B | 54.34 | 59.44 | 60.24 | +5.91 |
| 8 | Fu-TCM-27B | Qwen3.5-27B | 60.07 | 60.07 | 60.21 | +0.14 |
| 9 | ShizhenGPT-7B-LLM | 7B | 56.18 | 56.18 | 57.29 | +1.11 |
| 10 | Sunsimiao-7B | 7B | 52.08 | 55.62 | 55.68 | +3.60 |
| 11 | HuatuoGPT2-34B | Yi-34B | 27.22 | 29.39 | 33.48 | +6.26 |
| 12 | HuatuoGPT-o1-8B | 8B | 9.73 | 17.66 | 26.67 | +16.93 |
| 13 | HuatuoGPT2-7B | 7B | 12.94 | 19.08 | 19.87 | +6.93 |

Aggregation: generation tasks contribute ROUGE-1 only (Section 4.6); SE-A is not included (Section 4.5).

### 5.2 Protocol bandwidth as a measured property

The bandwidth column of Table 2 is the empirical core of our evaluation argument. TCMedSeek's bandwidth is +0.57. BianCang-14B (+0.17) and Fu-TCM-27B (+0.14) are comparably small. A small bandwidth is therefore a shared property of format-compliant models rather than an artifact constructed to favor our pipeline. By contrast, HuatuoGPT-o1-8B gains +16.93 points from L0 to L2, and Baichuan-M1-14B gains +9.24. For such models, a substantial share of apparent performance under lenient scoring is contributed by the extraction pipeline.

![**Fig. 3** Scores of all 13 systems under the three scoring protocols, computed from identical raw outputs. The vertical span of each line is the protocol bandwidth (L2 minus L0), printed at right. TCMedSeek ranks first under all three protocols with a bandwidth of 0.57 points, while several baselines gain more than 5 points from the scorer alone.](figures/fig3_bandwidth.png){width=5.4in}


Our own untrained base shows the cost of the strictest protocol from the opposite direction. Its bandwidth is +5.62, and its L0 score of 62.91 falls below BianCang-14B (64.88) and ShizhenGPT-32B (64.80). The fine-tuned model stays first even at L0.

Two further readings of Table 2 close alternative explanations of our lead. Base advantage: Fu-TCM-27B, built on the same-generation, same-family Qwen3.5-27B base, scores 60.21 at L2, eight points below our untrained base (68.53). The lead is therefore not explained by base recency or family. Scale advantage: Xinghe1.2-9B (63.38) outranks Fu-TCM-27B at one third of the size, so scale does not order this field either.

### 5.3 Per-subset structure of the win

Table 3 details the 10 jointly scored subsets under L2. TCMedSeek is numerically first on 8 of the 10. Interpreted against the ±1.0 noise band, this is six wins beyond noise, two ties within it (ED-B +0.46 over BianCang-14B; TCMeEE +0.78 over BianCang-14B), and two losses. The losses are reported as such. On literature extraction (LitData), Fu-TCM-27B leads by 5.40, with higher ROUGE-1, ROUGE-L, and BLEU individually. This is a genuine gap rather than a length artifact. On prescription recommendation (PR), ShizhenGPT-32B leads by 1.23, within noise. We do not contest this subset, because the constant-prescription degenerate baseline of Section 5.6 scores above every model on it.

Table 3. Per-subset scores under L2: TCMedSeek versus the strongest external model on each subset. Verdicts apply the ±1.0-point noise band.

| Subset | n | TCMedSeek | Best external | Model | Margin | Verdict |
|---|---:|---:|---:|---|---:|---|
| ED-A | 1,197 | 89.31 | 86.97 | Fu-TCM-27B | +2.34 | Win |
| ED-B | 4,800 | 90.27 | 89.81 | BianCang-14B | +0.46 | Tie |
| SE-B | 50 | 88.00 | 84.00 | Fu-TCM-27B | +4.00 | Win |
| MSDD | 100 | 62.25 | 47.75 | Baichuan-M1-14B | +14.50 | Win |
| CHGD | 100 | 63.50 | 55.70 | Fu-TCM-27B | +7.79 | Win |
| Diagnosis | 200 | 82.02 | 75.74 | Baichuan-M1-14B | +6.27 | Win |
| FRD | 200 | 78.64 | 72.43 | ShizhenGPT-32B | +6.21 | Win |
| TCMeEE | 100 | 80.67 | 79.89 | BianCang-14B | +0.78 | Tie |
| LitData | 100 | 72.63 | 78.03 | Fu-TCM-27B | −5.40 | Loss |
| PR | 100 | 38.12 | 39.35 | ShizhenGPT-32B | −1.23 | Loss (within noise) |

![**Fig. 4** Per-subset margins of TCMedSeek over the strongest external model under L2, against the empirically calibrated ±1.0-point noise band (shaded). Six wins exceed the band, two ties fall within it, and two losses are reported as such.](figures/fig4_margins.png){width=5.4in}


Under L0 the win/tie/loss structure is identical. The strongest external model on Diagnosis and FRD changes to Xinghe1.2-9B, with margins widening to +5.65 and +9.69. Without our extractor, these two subsets are won by more.

### 5.4 Gains over the untrained base

Table 4 reports the longitudinal comparison under the four-metric aggregation scheme (Section 4.6). These numbers are not comparable to Table 2 and are footnoted accordingly. Averaged simply over the 11 evaluated subsets, the untrained base scores 67.58 and TCMedSeek 74.53, a gain of 6.96 points. Weighted by item count over the 6,997 evaluated items, the gain is +2.96, from 84.62 to 87.58. The difference between the two averages reflects the dominance of examination subsets by item count. A total of 10 of the 11 subsets improve; the only decline is PR (−1.67). The largest gains are multi-label syndrome classification (MSDD +20.00), dialogue-to-record structuring (CHGD +14.45), diagnosis with syndrome elements (+10.96), LLM-judged safety fill-in (SE-A +8.60, within-judge difference only, Section 4.5), literature extraction (+8.11), and safety multiple choice (SE-B +8.00).

Table 4. Longitudinal comparison over 11 subsets (four-metric aggregation for generation tasks; accuracy for closed sets).

| Dataset | n | Base | TCMedSeek | Δ |
|---|---:|---:|---:|---:|
| TCM-MSDD | 100 | 42.25 | 62.25 | +20.00 |
| TCM-CHGD | 100 | 48.97 | 63.42 | +14.45 |
| TCM-Diagnosis | 200 | 74.76 | 85.72 | +10.96 |
| TCM-SE-A* | 50 | 63.90 | 72.50 | +8.60 |
| TCM-LitData | 100 | 59.00 | 67.11 | +8.11 |
| TCM-SE-B | 50 | 80.00 | 88.00 | +8.00 |
| TCM-FRD | 200 | 77.02 | 79.90 | +2.88 |
| TCM-ED-B | 4,800 | 88.10 | 90.27 | +2.17 |
| TCM-ED-A | 1,197 | 87.22 | 89.31 | +2.09 |
| TCMeEE | 100 | 82.35 | 83.28 | +0.93 |
| TCM-PR | 100 | 39.79 | 38.12 | −1.67 |

*SE-A scored by a single fixed alternative judge for both columns; only the difference is interpretable (Section 4.5).

### 5.5 Directed flips

Table 5 applies the directionality criterion of Section 3.6 to the four closed subsets. On every one of them, items changed from wrong to right outnumber the reverse, well beyond the retraining perturbation tax established during the loop. That tax is approximately 4.3% undirected flips, concentrated on roughly 665 swing items. On ED-B, the net balance of +104 items should be read against the fact that a 1% score change corresponds to roughly 48 items at this subset size. On MSDD, the 43-to-8 ratio is decisive.

Table 5. Directed flips between the untrained base and TCMedSeek on closed subsets.

| Dataset | n | Wrong→right | Right→wrong | Net |
|---|---:|---:|---:|---:|
| TCM-ED-B | 4,800 | 225 | 121 | +104 |
| TCM-MSDD | 100 | 43 | 8 | +35 |
| TCM-ED-A | 1,197 | 51 | 26 | +25 |
| TCM-SE-B | 50 | 4 | 0 | +4 |

### 5.6 Degenerate baseline and construct validity

The constant-prescription baseline (Section 4.5) scores 0.4341 on PR, above all 13 systems in Table 2, including models whose training emphasizes prescription generation. We therefore treat PR as a construct-validity case study for the benchmark rather than as a performance axis. The subset's instance score averages Jaccard, F1, and a size-agreement term. A fixed prescription can satisfy size agreement while overlapping a limited herb vocabulary shared by many case records. Claims of case-specific prescription improvement would require a permutation test over per-case gains, which none of the compared systems' margins here support.

### 5.7 Outcomes of attribution-driven remediation

The final attribution wave (744 closed-set errors) yielded 68 knowledge gaps, 454 taught-but-misdiscriminated errors, and 222 unmatched items (Section 3.6). The discrimination class dominated the remediation effort and validated the taxonomy empirically. In the closing iterations, 596 closed-set errors were individually dispositioned and 396 contrastive cards were produced, with re-teaching volume withheld for covered topics by design.

Two negative observations are reported because they bound the method. First, structural alignment is not equivalent to semantic gain. A targeted remediation raised the structural completeness of the pathogenesis segment in CHGD outputs from 19% to 67%, matching the gold format, while F1 improved by only 0.012. That remediation direction was closed. Second, the registered 143 suspected reference faults and five pharmacopoeia-level discrepancies remain pending independent confirmation by licensed physicians and are reported as discrepancies only. Among them is one safety item whose gold answer states a stricter contraindication category than the pharmacopoeia itself. Training toward the gold answer would raise the benchmark score while worsening fidelity to the authoritative source.

## 6 Discussion

This study started from a measurement argument. In a domain where training material and evaluation material share origin, benchmark scores are unreliable in both directions: contamination inflates them [R25, R26, R27], while extraction-strict scorers and faulty references deflate them. The TCMedSeek results support the argument and its constructive converse. When contamination is policed by construction, scoring sensitivity is reported instead of hidden, and remediation is matched to error class, a single one-epoch LoRA fine-tuning suffices. On a compact corpus of 135,797 samples, it leads a 13-model field under all three scoring protocols. The lead survives the strictest protocol, which cannot benefit from our own extraction pipeline.

### 6.1 Complexity belongs on the data side

The most direct comparison is ZhongYan [R12], which trains a 14B model through continued pre-training on 3.9 billion tokens, supervised fine-tuning on over 272,000 samples, DPO with knowledge-graph rewards, and retrieval augmentation. TCMedSeek uses approximately half the supervised corpus, no continued pre-training, no preference stage, and no retrieval, yet ranks first on a public multi-dimension benchmark. We attribute this to where the engineering effort was spent rather than to the training recipe, which is minimal by design. In total, 87% of the corpus carries the authority of state publications. Provenance is recorded per sample to source volume and line, with 0.12% undetermined. Synthesis proceeds from fixed evidence tables with an 8.9% logged rejection rate, and every zero-leak verdict is confirmed by an independent second implementation. Published TCM model reports we are aware of do not describe a comparable sample-level protocol. We state this as an observation about reporting practice, not as a claim about unpublished practice. The finding aligns with the quality-first line in general LLM research. There, small curated instruction sets rival larger ones for alignment [R28], and textbook-quality data substitutes for orders of magnitude more web text [R29]. It extends that line to a vertical domain in which authority is externally verifiable rather than judgment-based.

### 6.2 A point lost is not a point wrong

The attribution taxonomy operationalizes the deflation direction. Of 744 closed-set errors in the final wave, 454 (61%) were taught-but-misdiscriminated: the corpus covered the topic, and the model failed on the boundary against a confusable neighbor. For this class, our data show that adding knowledge volume does not repair the error, while contrastive cards that name the distractor do. This result explains, in mechanistic terms, why error-driven fine-tuning that does not classify its errors can yield little. ZhongYan reported limited gains from iteratively fine-tuning on wrong answers and attributed this to ambiguous ground truth [R12]. Our taxonomy separates that explanation into at least three distinct failure modes. Only one, verified reference faults, of which five pharmacopoeia-level cases await confirmation, is the benchmark's fault. Only one other, true gaps at 9%, is repaired by teaching more. The remaining 61% require discrimination, not repetition.

The inflation direction is documented with equal specificity. The leak-cleanup ledger, 489 deletions across four waves (Additional file 1), records three mechanism failures that a "zero leaks" certificate had masked. One is a fragment gate blind to near-verbatim examination variants. Another is a repair practice that reordered symptom phrases and thereby evaded order-sensitive detectors without removing the exposure. The third is structural blind spots in option parsing. These incidents motivate two protocol rules that we propose for adoption beyond this study. Deletion criteria must be re-derived whenever a gate reports zero on data known to be at risk. And any zero verdict requires an independent second implementation before it is believed.

### 6.3 Evaluation practice implications

Three evaluation findings generalize. First, protocol bandwidth should be a reported quantity. Recomputing all 13 systems under three extraction levels from the same raw outputs costs no additional inference. It reveals that apparent performance differs by up to 16.93 points as a function of the scorer alone. Second, noise bands should be calibrated empirically. Our duplicate-item contrasts yield 0.3 to 1.4%, whereas a naive sample-size formula would have returned roughly 4 points, large enough to mask real effects in both directions. Third, degenerate baselines belong in the main table. A constant-prescription baseline that outscores every model on a prescription subset is direct evidence of construct-validity failure that per-model margins cannot supply.

### 6.4 Limitations

The study has boundaries that we state explicitly. (1) Provenance is not fully closed. 166 samples (0.12%) remain undetermined, and 7,369 samples are attributed to the textbook class without a resolved volume. Retroactive matching agrees with build-time declarations at 86.2% overall but 71% for textbooks, partly because several volumes entered through image-based transcription. (2) Approximately two thirds of source material is scanned and passed through OCR. An analysis of dropped characters found an 8.8% error rate for items containing an affected drug name, versus 9.8% for controls. Residual corruption, rather than character loss, is therefore the operative risk. (3) One known capability gap is left open. The western-disease-name field in entity extraction (TCMeEE) is answered as absent in all 658 related training samples, while 69 of 100 gold items expect a value; closing it would have required inventing clinical detail absent from the case records. (4) Several capability classes depend heavily on single sources, with medication safety at 91.1% from the pharmacopoeia and syndrome classification at 67.0% from one public case corpus. Pharmacopoeia OCR digit errors propagate directly into safety-adjacent content, and one observed error mode was a toxic-herb dosage stated too high. (5) The benchmark and the training exercise banks share an examination system of origin. We delete same items and retain shared knowledge points, which bounds but does not eliminate distributional affinity. (6) The internal validation split has grouping leakage across questions about the same formula or source, which affects internal val scores only; no progression decision used internal val loss. (7) TCM-FT (100 items) could not be run for infrastructure reasons, so coverage is 11 of 12 sub-datasets. (8) SE-A is not in the 13-model table because baseline-side LLM judging was not run; its base-versus-TCMedSeek difference is within one fixed judge. (9) The five pharmacopoeia-level discrepancies await confirmation by three licensed physicians, and until then are reported as discrepancies rather than corrections. (10) The pipeline's attribution and gating are automated, but arbitration and card authoring are human-in-the-loop. The loop is evidenced by incident-driven ledgers rather than by factorial ablation of its components. (11) A corpus of physician case records was evaluated and rejected for OCR-related quality reasons; not all available corpora should be used. (12) Results are demonstrated on a single base model family, and transferring the recipe across families is untested.

## 7 Conclusions

TCMedSeek indicates that the binding constraint in building TCM LLMs is data quality under measurement fidelity, not training-stage accumulation. A single-stage LoRA supervised fine-tuning of one epoch on 135,797 samples ranks first among 13 systems across all three scoring protocols on a public five-dimension benchmark. Of these samples, 87% are warranted by state publications, and all are provenance-traced and decontamination-gated. The protocol bandwidth of the model is 0.57 points, against gains of up to 16.93 for baselines. The methodology generalizes beyond this model. Attribute before remediating, because most closed-set errors in a well-covered corpus are discrimination failures rather than knowledge gaps. Report scoring-protocol sensitivity, because apparent performance can move by double digits with the extractor alone. And require independent re-implementation before believing any zero-contamination verdict. Future work includes verifier-based reinforcement learning on the programmatically checkable subsets this evaluation identified, extension to multimodal TCM diagnostics, and confirmation of the registered reference discrepancies by independent clinical review.

## Declarations

**Ethics approval and consent to participate**
Not applicable. This study involved no human subjects and no hospital records. The training corpus derives from published books and publicly released datasets, with no personally identifiable information. [TODO: confirm the TCM-SD license terms before submission.]

**Consent for publication**
Not applicable.

**Availability of data and materials**
The MTCMB benchmark is publicly available (Zenodo, DOI 10.5281/zenodo.20465629). The provenance-annotated training corpus, raw evaluation outputs with preserved raw fields, item-list SHA-256 checksums, and aggregation scripts are planned for release with the paper. [TODO: repository URL; decide whether LoRA weights (67 GB) are included.]

**Competing interests**
[TODO]

**Funding**
[TODO: funding grant numbers]

**Authors' contributions**
[TODO: CRediT roles for each author]

**Acknowledgements**
[TODO: compute resources acknowledgement]

**AI usage disclosure**
During preparation of this work the authors used large language models to assist with corpus generation under fixed evidence tables (as described in Methods), automated error attribution, and manuscript language editing. All synthetic training samples passed the hard acceptance gates described in Methods. All model-assisted attributions were arbitrated under the score-independent evidence rule. All AI-assisted text was reviewed and revised by the authors, who take full responsibility for the content.

**Abbreviations**
TCM: Traditional Chinese Medicine; LLM: large language model; SFT: supervised fine-tuning; LoRA: low-rank adaptation; CPT: continued pre-training; DPO: direct preference optimization; GRPO: group relative policy optimization; MTCMB: Multi-task Traditional Chinese Medicine Benchmark; ROUGE/BLEU/BERTScore: overlap- and embedding-based generation metrics; PR: prescription recommendation; SE: safety evaluation; OCR: optical character recognition.

## References (working library, to be renumbered in BMC style at submission)

R01. Wei S, Peng X, Wang Y-F, Shen T, Si J, Zhang W, et al. BianCang: A Traditional Chinese Medicine Large Language Model. IEEE Journal of Biomedical and Health Informatics (Early Access), 2025:1-12. arXiv:2411.11027. DOI: 10.1109/JBHI.2025.3612415.
R02. Chen J, Cai Z, Liu Z, Yang Y, Wang R, Xiao Q, et al. ShizhenGPT: Towards Multimodal LLMs for Traditional Chinese Medicine. arXiv:2508.14706, 2025.
R03. Chen J, Wang X, Ji K, Gao A, Jiang F, Chen S, et al. HuatuoGPT-II, One-stage Training for Medical Adaption of LLMs. arXiv:2311.09774, 2023 (v2 2024).
R04. Chen J, Cai Z, Ji K, Wang X, Liu W, Wang R, et al. HuatuoGPT-o1, Towards Medical Complex Reasoning with LLMs. arXiv:2412.18925, 2024.
R05. Wang B, Zhao H, Zhou H, Song L, Xu M, Cheng W, et al. Baichuan-M1: Pushing the Medical Capability of Large Language Models. arXiv:2502.12671, 2025.
R06. Bao Z, Chen W, Xiao S, Ren K, Wu J, Zhong C, et al. DISC-MedLLM: Bridging General Large Language Models and Real-World Medical Consultation. arXiv:2308.14346, 2023.
R07. Zhang X, Xue K, Zhang S. PULSE: Pretrained and Unified Language Service Engine. 2023. https://github.com/openmedlab/PULSE.
R08. X-D-Lab. Sunsimiao: a Chinese medical large language model (GitHub repository) . 2023. https://github.com/X-D-Lab/Sunsimiao.
R09. Yang S, Zhao H, Zhu S, Zhou G, Xu H, Jia Y, Zan H. Zhongjing: Enhancing the Chinese Medical Capabilities of Large Language Model through Expert Feedback and Real-World Multi-Turn Dialogue. AAAI 2024, 38:19368-19376.
R10. Dai Y, Shao X, Zhang J, Chen Y, Chen Q, Liao J, et al. TCMChat: A generative large language model for traditional Chinese medicine. Pharmacological Research, 2024, 210:107530.
R11. Hua R, Dong X, Wei Y, Shu Z, Yang P, Hu Y, et al. Lingdan: enhancing encoding of traditional Chinese medicine knowledge for clinical reasoning tasks with large language models. Journal of the American Medical Informatics Association, 2024, 31(9):2019-2029.
R12. Chai Z, Ma W, Xu D, Huang Y, Zhu W, Zhao J, et al. ZhongYan: A Knowledge-Integrated Large Language Model for Reasoning and Application in Traditional Chinese Medicine. IEEE Journal of Biomedical and Health Informatics, 2026 (in press).. [TODO: DOI upon publication].
R13. Fu-TCM-27B. [TODO: model repository URL and access date].
R14. Xinghe1.2-9B. [TODO: model repository URL and access date].
R15. Luo L, Chae J, Chen Z, Liu Y, Cheng S, Gao W, et al. MMIR-TCM: Memory-Integrated Multimodal Inference and Retrieval for TCM Clinical Decision Support. arXiv:2607.01814, 2026.
R16. Xie J, Yu Y, Chen Y, Zhang H, Zhao L, He J, et al. BenCao: An Instruction-Tuned Large Language Model for Traditional Chinese Medicine. arXiv:2510.17415, 2025.
R17. Liu Q, Li Y, Yang P, Liu Q, Wang C, Chen K, Wu Z. A survey of artificial intelligence in tongue image for disease diagnosis and syndrome differentiation. Digital Health, 2023, 9:20552076231191044. DOI: 10.1177/20552076231191044.
R18. Miao J, Huang Y, Wang Z, Wu Z, Lv J. Image recognition of traditional Chinese medicine based on deep learning. Frontiers in Bioengineering and Biotechnology, 2023, 11:1199803. DOI: 10.3389/fbioe.2023.1199803.
R19. Mulugeta AK, Sharma DP, Mesfin AH. Deep learning for medicinal plant species classification and recognition: a systematic review. Frontiers in Plant Science, 2023, 14:1286088. DOI: 10.3389/fpls.2023.1286088.
R20. Yuan L, Yang L, Zhang S, et al. Development of a tongue image-based machine learning tool for the diagnosis of gastric cancer: a prospective multicentre clinical cohort study. eClinicalMedicine, 2023, 57:101834. DOI: 10.1016/j.eclinm.2023.101834.
R21. Kong S, Yang X, Wei Y, Wang Z, Tang H, Qin J, et al. MTCMB: A Multi-Task Benchmark Framework for Evaluating LLMs on Knowledge, Reasoning, and Safety in Traditional Chinese Medicine. arXiv:2506.01252, 2025. Data archived at: Zenodo DOI 10.5281/zenodo.20465629 (CC-BY 4.0) 。 Repository: https://github.com/Wayyuanyuan/MTCMB.
R22. Yue W, Wang X, Zhu W, Guan M, Zheng H, Wang P, et al. TCMBench: A comprehensive benchmark for evaluating large language models in traditional Chinese medicine. arXiv:2406.01126, 2024.
R23. Huang T, Chen J, Lu L, Chen P, Li T, Han B, et al. TCM-5CEval: Extended deep evaluation benchmark for LLM's comprehensive clinical research competence in traditional chinese medicine. arXiv:2511.13169, 2025.
R24. Cheng Z, Lu Y, Ye H, Liu Z, Wang M, Liu J, et al. TCM-Eval: An expert-level dynamic and extensible benchmark for traditional chinese medicine. arXiv:2511.07148, 2025.
R25. Sainz O, Campos JA, García-Ferrero I, Etxaniz J, Lopez de Lacalle O, Agirre E. NLP Evaluation in trouble: On the Need to Measure LLM Data Contamination for each Benchmark. Findings of EMNLP 2024. arXiv:2310.18018.
R26. Golchin S, Surdeanu M. Time Travel in LLMs: Tracing Data Contamination in Large Language Models. ICLR 2024 (Spotlight). arXiv:2308.08493.
R27. Zhang H, Da D, Lee D, Robinson V, Wu C, Song W, et al. A Careful Examination of Large Language Model Performance on Grade School Arithmetic (GSM1k). NeurIPS 2024 (Datasets and Benchmarks). arXiv:2405.00332.
R28. Zhou C, Liu P, Xu P, Iyer S, Sun J, Mao Y, et al. LIMA: Less Is More for Alignment. NeurIPS 2023. arXiv:2305.11206.
R29. Gunasekar S, Zhang Y, Aneja J, Mendes CCT, Del Giorno A, Gopi S, et al. Textbooks Are All You Need. arXiv:2306.11644, 2023.
R30. Hu EJ, Shen Y, Wallis P, Allen-Zhu Z, Li Y, Wang S, et al. LoRA: Low-Rank Adaptation of Large Language Models. ICLR 2022.
R31. Rafailov R, Sharma A, Mitchell E, Manning CD, Ermon S, Finn C. Direct Preference Optimization: Your Language Model is Secretly a Reward Model. NeurIPS 2023.
R32. Shao Z, Wang P, Zhu Q, Xu R, Song J, Bi X, et al. DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models . arXiv:2402.03300, 2024.
R33. Kirkpatrick J, Pascanu R, Rabinowitz N, et al. Overcoming catastrophic forgetting in neural networks. PNAS, 2017, 114(13):3521-3526.
R34. Zhao WX, Zhou K, Li J, Tang T, Wang X, Hou Y, et al. A survey of large language models. arXiv:2303.18223, 2023.
R35. Achiam J, Adler S, Agarwal S, et al. GPT-4 Technical Report. arXiv:2303.08774, 2023.
R36. Yang A, Li A, Yang B, Zhang B, Hui B, Zheng B, et al. Qwen3 Technical Report. arXiv:2505.09388, 2025.. [TODO: replace if a Qwen3.5/3.6 technical report is released].
R37. Liu A, Feng B, Xue B, et al. DeepSeek-V3 Technical Report. arXiv:2412.19437, 2024.
R38. Qiu J, Li L, Sun J, Peng J, Shi P, Zhang R, et al. Large AI models in health informatics: Applications, challenges, and the future. IEEE Journal of Biomedical and Health Informatics, 2023, 27(12):6074-6087.
R39. Singh K, Gupta JK, Jain D, Kumar T, Singh T, Saha S. Exploring the ancient wisdom and modern relevance of chinese medicine: A comprehensive review. Pharmacological Research - Modern Chinese Medicine, 2024.
R40. Jiang M, Lu C, Zhang C, Yang J, Tan Y, Lu A, Chan K. Syndrome differentiation in modern research of traditional chinese medicine. Journal of Ethnopharmacology, 2012, 140(3):634-642.
R41. Yip HF, Li Z, Zhang L, Lyu A. Large language models in integrative medicine: Progress, challenges, and opportunities. Journal of Evidence-Based Medicine, 2025, 18(2):e70031.
R42. Pan D, Guo Y, Fan Y, Wan H. Development and Application of Traditional Chinese Medicine Using AI Machine Learning and Deep Learning Strategies. The American Journal of Chinese Medicine, 2024, 52(3):605-623. DOI: 10.1142/S0192415X24500265.
