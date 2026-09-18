# TCMedSeek 参考文献库（v1，2026-09-16）

供 Introduction / Related Work 及后续全文使用。每条带核实状态：

- ✅ **已核实**：本次在 arXiv 官方 API / PubMed eutils / GitHub 仓库页逐条打开确认过题名、作者、年份、编号
- ✅(转) **经 JBHI 转引**：题录取自 ZhongYan (JBHI-00178-2026) 的参考文献表，该表经期刊出版流程，可信度高；投稿前建议再逐条过一眼 DOI
- ⚠️ **待办**：需要团队补充或最终核对

正文草稿（02/03 文件）中的引文标记 `[Rxx]` 与本表一一对应。投稿排版时再按 Chinese Medicine 的 BMC 编号风格重排顺序。

---

## A. 中医/医学大模型（对比模型与图谱）

| ID | 状态 | 条目 |
|---|---|---|
| R01 | ✅ | Wei S, Peng X, Wang Y-F, Shen T, Si J, Zhang W, et al. BianCang: A Traditional Chinese Medicine Large Language Model. IEEE Journal of Biomedical and Health Informatics (Early Access), 2025:1-12. arXiv:2411.11027. DOI: 10.1109/JBHI.2025.3612415. |
| R02 | ✅ | Chen J, Cai Z, Liu Z, Yang Y, Wang R, Xiao Q, et al. ShizhenGPT: Towards Multimodal LLMs for Traditional Chinese Medicine. arXiv:2508.14706, 2025. |
| R03 | ✅ | Chen J, Wang X, Ji K, Gao A, Jiang F, Chen S, et al. HuatuoGPT-II, One-stage Training for Medical Adaption of LLMs. arXiv:2311.09774, 2023 (v2 2024). |
| R04 | ✅ | Chen J, Cai Z, Ji K, Wang X, Liu W, Wang R, et al. HuatuoGPT-o1, Towards Medical Complex Reasoning with LLMs. arXiv:2412.18925, 2024. |
| R05 | ✅ | Wang B, Zhao H, Zhou H, Song L, Xu M, Cheng W, et al. Baichuan-M1: Pushing the Medical Capability of Large Language Models. arXiv:2502.12671, 2025. |
| R06 | ✅ | Bao Z, Chen W, Xiao S, Ren K, Wu J, Zhong C, et al. DISC-MedLLM: Bridging General Large Language Models and Real-World Medical Consultation. arXiv:2308.14346, 2023. |
| R07 | ✅ | Zhang X, Xue K, Zhang S. PULSE: Pretrained and Unified Language Service Engine. 2023. https://github.com/openmedlab/PULSE（官方 README 提供 bibtex；PULSE-7bv5 基于 bloomz-7b1-mt 微调） |
| R08 | ✅ | X-D-Lab. Sunsimiao: 中文医疗大模型（GitHub 仓库）. 2023. https://github.com/X-D-Lab/Sunsimiao（无正式论文，按软件仓库引用，注明访问日期） |
| R09 | ✅(转) | Yang S, Zhao H, Zhu S, Zhou G, Xu H, Jia Y, Zan H. Zhongjing: Enhancing the Chinese Medical Capabilities of Large Language Model through Expert Feedback and Real-World Multi-Turn Dialogue. AAAI 2024, 38:19368-19376. |
| R10 | ✅(转) | Dai Y, Shao X, Zhang J, Chen Y, Chen Q, Liao J, et al. TCMChat: A generative large language model for traditional Chinese medicine. Pharmacological Research, 2024, 210:107530. |
| R11 | ✅(转) | Hua R, Dong X, Wei Y, Shu Z, Yang P, Hu Y, et al. Lingdan: enhancing encoding of traditional Chinese medicine knowledge for clinical reasoning tasks with large language models. Journal of the American Medical Informatics Association, 2024, 31(9):2019-2029. |
| R12 | ⚠️ | Chai Z, Ma W, Xu D, Huang Y, Zhu W, Zhao J, et al. ZhongYan: A Knowledge-Integrated Large Language Model for Reasoning and Application in Traditional Chinese Medicine. IEEE Journal of Biomedical and Health Informatics, 2026 (in press). ⚠️ DOI 尚未见刊，见刊后补；这是我们的对标稿与引文锚（其 §V-C-4 承认 ambiguous ground truth 限制错题重训收益） |
| R13 | ⚠️ | Fu-TCM-27B（Qwen3.5-27B 底座）。⚠️ 未检索到正式论文；按模型仓库引用。**需团队提供其 HuggingFace/ModelScope 主页 URL**，引用格式：`Org. Fu-TCM-27B [model repository]. URL, accessed 2026-xx-xx.` |
| R14 | ⚠️ | Xinghe1.2-9B（星河）。⚠️ 同上，**需团队提供仓库 URL**。 |

## B. 多模态舌诊 / 中药图像识别（江老师点名补齐的两类）

| ID | 状态 | 条目 |
|---|---|---|
| R15 | ✅ | Luo L, Chae J, Chen Z, Liu Y, Cheng S, Gao W, et al. MMIR-TCM: Memory-Integrated Multimodal Inference and Retrieval for TCM Clinical Decision Support. arXiv:2607.01814, 2026.（舌诊 MLLM + RAG，含 MedTCM 多模态数据集） |
| R16 | ✅ | Xie J, Yu Y, Chen Y, Zhang H, Zhao L, He J, et al. BenCao: An Instruction-Tuned Large Language Model for Traditional Chinese Medicine. arXiv:2510.17415, 2025.（指令调优多模态助手，含舌象分类 API 与草药识别） |
| R17 | ✅ | Liu Q, Li Y, Yang P, Liu Q, Wang C, Chen K, Wu Z. A survey of artificial intelligence in tongue image for disease diagnosis and syndrome differentiation. Digital Health, 2023, 9:20552076231191044. DOI: 10.1177/20552076231191044.（舌诊 AI 综述锚点） |
| R18 | ✅ | Miao J, Huang Y, Wang Z, Wu Z, Lv J. Image recognition of traditional Chinese medicine based on deep learning. Frontiers in Bioengineering and Biotechnology, 2023, 11:1199803. DOI: 10.3389/fbioe.2023.1199803.（中药图像识别直接对应文献） |
| R19 | ✅ | Mulugeta AK, Sharma DP, Mesfin AH. Deep learning for medicinal plant species classification and recognition: a systematic review. Frontiers in Plant Science, 2023, 14:1286088. DOI: 10.3389/fpls.2023.1286088. |
| R20 | ✅ | Yuan L, Yang L, Zhang S, et al. Development of a tongue image-based machine learning tool for the diagnosis of gastric cancer: a prospective multicentre clinical cohort study. eClinicalMedicine, 2023, 57:101834. DOI: 10.1016/j.eclinm.2023.101834.（舌诊 AI 临床落地证据） |

> 注：ShizhenGPT [R02] 本身即是"草药识别 + 视觉诊断"的 LLM 时代代表作（其论文含 Medicinal Recognition 视觉基准），B 类与 A 类在 R02 上交汇。

## C. 评测基准

| ID | 状态 | 条目 |
|---|---|---|
| R21 | ✅ | Kong S, Yang X, Wei Y, Wang Z, Tang H, Qin J, et al. MTCMB: A Multi-Task Benchmark Framework for Evaluating LLMs on Knowledge, Reasoning, and Safety in Traditional Chinese Medicine. arXiv:2506.01252, 2025. 数据归档：Zenodo DOI 10.5281/zenodo.20465629（CC-BY 4.0）。仓库：https://github.com/Wayyuanyuan/MTCMB |
| R22 | ✅(转) | Yue W, Wang X, Zhu W, Guan M, Zheng H, Wang P, et al. TCMBench: A comprehensive benchmark for evaluating large language models in traditional Chinese medicine. arXiv:2406.01126, 2024. |
| R23 | ✅(转) | Huang T, Chen J, Lu L, Chen P, Li T, Han B, et al. TCM-5CEval: Extended deep evaluation benchmark for LLM's comprehensive clinical research competence in traditional chinese medicine. arXiv:2511.13169, 2025. |
| R24 | ✅(转) | Cheng Z, Lu Y, Ye H, Liu Z, Wang M, Liu J, et al. TCM-Eval: An expert-level dynamic and extensible benchmark for traditional chinese medicine. arXiv:2511.07148, 2025. |

## D. 数据污染 / 评测完整性（立论支撑）

| ID | 状态 | 条目 |
|---|---|---|
| R25 | ✅ | Sainz O, Campos JA, García-Ferrero I, Etxaniz J, Lopez de Lacalle O, Agirre E. NLP Evaluation in trouble: On the Need to Measure LLM Data Contamination for each Benchmark. Findings of EMNLP 2024. arXiv:2310.18018. |
| R26 | ✅ | Golchin S, Surdeanu M. Time Travel in LLMs: Tracing Data Contamination in Large Language Models. ICLR 2024 (Spotlight). arXiv:2308.08493. |
| R27 | ✅ | Zhang H, Da D, Lee D, Robinson V, Wu C, Song W, et al. A Careful Examination of Large Language Model Performance on Grade School Arithmetic (GSM1k). NeurIPS 2024 (Datasets and Benchmarks). arXiv:2405.00332. |

## E. 数据质量 / "少而精"路线

| ID | 状态 | 条目 |
|---|---|---|
| R28 | ✅ | Zhou C, Liu P, Xu P, Iyer S, Sun J, Mao Y, et al. LIMA: Less Is More for Alignment. NeurIPS 2023. arXiv:2305.11206. |
| R29 | ✅ | Gunasekar S, Zhang Y, Aneja J, Mendes CCT, Del Giorno A, Gopi S, et al. Textbooks Are All You Need. arXiv:2306.11644, 2023. |

## F. 训练方法

| ID | 状态 | 条目 |
|---|---|---|
| R30 | ✅(转) | Hu EJ, Shen Y, Wallis P, Allen-Zhu Z, Li Y, Wang S, et al. LoRA: Low-Rank Adaptation of Large Language Models. ICLR 2022. |
| R31 | ✅(转) | Rafailov R, Sharma A, Mitchell E, Manning CD, Ermon S, Finn C. Direct Preference Optimization: Your Language Model is Secretly a Reward Model. NeurIPS 2023. |
| R32 | ✅ | Shao Z, Wang P, Zhu Q, Xu R, Song J, Bi X, et al. DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models（提出 GRPO）. arXiv:2402.03300, 2024. |
| R33 | ✅(转) | Kirkpatrick J, Pascanu R, Rabinowitz N, et al. Overcoming catastrophic forgetting in neural networks. PNAS, 2017, 114(13):3521-3526. |

## G. 通用/医学大模型背景（Introduction 借 JBHI 引用）

| ID | 状态 | 条目 |
|---|---|---|
| R34 | ✅(转) | Zhao WX, Zhou K, Li J, Tang T, Wang X, Hou Y, et al. A survey of large language models. arXiv:2303.18223, 2023. |
| R35 | ✅(转) | Achiam J, Adler S, Agarwal S, et al. GPT-4 Technical Report. arXiv:2303.08774, 2023. |
| R36 | ✅(转) | Yang A, Li A, Yang B, Zhang B, Hui B, Zheng B, et al. Qwen3 Technical Report. arXiv:2505.09388, 2025. ⚠️ 我们底座为 Qwen3.6-35B-A3B；经查 arXiv 无 "Qwen3.5/3.6 Technical Report"（仅 Qwen3.5-Omni, arXiv:2604.15804）。**若阿里后续发布 3.5/3.6 技术报告，请替换本条**；在此之前正文写法见 02 文件注 4。 |
| R37 | ✅(转) | Liu A, Feng B, Xue B, et al. DeepSeek-V3 Technical Report. arXiv:2412.19437, 2024. |
| R38 | ✅(转) | Qiu J, Li L, Sun J, Peng J, Shi P, Zhang R, et al. Large AI models in health informatics: Applications, challenges, and the future. IEEE Journal of Biomedical and Health Informatics, 2023, 27(12):6074-6087. |
| R39 | ✅(转) | Singh K, Gupta JK, Jain D, Kumar T, Singh T, Saha S. Exploring the ancient wisdom and modern relevance of chinese medicine: A comprehensive review. Pharmacological Research - Modern Chinese Medicine, 2024. |
| R40 | ✅(转) | Jiang M, Lu C, Zhang C, Yang J, Tan Y, Lu A, Chan K. Syndrome differentiation in modern research of traditional chinese medicine. Journal of Ethnopharmacology, 2012, 140(3):634-642. |
| R41 | ✅(转) | Yip HF, Li Z, Zhang L, Lyu A. Large language models in integrative medicine: Progress, challenges, and opportunities. Journal of Evidence-Based Medicine, 2025, 18(2):e70031. |
| R42 | ✅ | Pan D, Guo Y, Fan Y, Wan H. Development and Application of Traditional Chinese Medicine Using AI Machine Learning and Deep Learning Strategies. The American Journal of Chinese Medicine, 2024, 52(3):605-623. DOI: 10.1142/S0192415X24500265. |

---

## 检索过程记录（供复核）

- arXiv 官方 API（export.arxiv.org）逐条确认：R01-R06, R15, R16, R21, R25-R29, R32；并证伪三个错误记忆号（2312.13925 不是 HuatuoGPT-II，2412.18926 不是 HuatuoGPT-o1，2310.20230 不是 PULSE）
- PubMed eutils 确认：R17-R20, R42
- GitHub 仓库页确认：R07（官方 bibtex）、R08（X-D-Lab org）
- 检索不到正式论文、按仓库引用处理：R08、R13、R14
- 江老师点名的"多模态舌诊 / 草药饮片识别"两类：LLM 时代用 R02/R15/R16，深度学习时代用 R17-R19，临床落地用 R20 —— 已够 Related Work 使用
- HuatuoGPT-o1 的 RL 算法（03 文件待核项）：论文摘要确认为 **verifier 引导搜索 + verifier-based reward RL** 两阶段，未限定 PPO/GRPO —— 正文措辞用 "verifier-based reinforcement learning" [R04] 即可，不会写错
