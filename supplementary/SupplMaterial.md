# 12 · Supplementary Material（Additional files 1–4 整理稿）

> **为什么是 4 个**：正文引用只有 Additional file 1–4（Methods 3.1、3.3、4.1、4.2 与 Discussion 6.2）。原 09 文件的 8 个附项按主题归并为 4 个文件，正文编号不变、无需改动。
> 投稿版最终语言为英文；本文件为中文整理稿（材料不需要翻译，江老师指示）。
> 投稿纪律：全文无内部版本号；迭代以 M1…M10 表述。

---

## Additional file 1 — Iteration and remediation ledger（迭代与补救台账）

*正文引用处：Methods 3.1（iteration ledger）、Discussion 6.2（leak-cleanup ledger）*

### A. 迭代轨迹（33 轮协同迭代中的 10 个存档里程碑）

| 迭代节点 | 语料行数 | 节点说明 |
|---|---:|---|
| M1 | 131,753 | 27B 线早期 |
| M2 | 124,231 | 清洗定版 |
| M3 | 110,415 | 泄漏与重复大规模清除后的最低点 |
| M4 | 116,452 | 对外首版（27B，8 卡） |
| M5 | 133,849 | 换基座 35B-A3B 后重建 |
| M6 | 138,386 | 峰值 |
| M7 | 138,264 | 13 条题目质量判据整改 |
| M8 | 135,622 | 单模板密度包清理 |
| M9 | 135,864 | 596 道闭集错题逐题处置完毕 |
| **M10（交付）** | **135,797** | 交付版（train）/ val 3,288 |

> 每一次行数下降均为删除（去污/判废），非回滚。内部存档编号与全量版本文件备查，不随投稿发布。

### B. 泄漏清理台账（四波共 489 条）

| 波次 | 删除 | 触发通道 |
|---|---:|---|
| 第一波 | 251 | 归一后 3-gram Jaccard 题干闸（30 字片段闸对近变体全漏） |
| 第二波 | 167 | 长题干阈值降至 0.45 + 词袋闸（含被症状重排规避检测的 110 条） |
| 第三波 | 7 | 包含度阈值 40 字 → 12 字 |
| 第四波 | 64 | 新增 D/E/F 三通道 |
| **合计** | **489** | |

### C. 三次事故记录（对应正文 Methods 3.4）
1. 片段闸漏检 251 道原题（OCR/排版/题干微调致窗口失配）→ 改 3-gram 题干闸。
2. 症状重排 ≠ 去泄漏（早期脚本以重排规避 n-gram 判据）→ 加字符多重集 Jaccard（重排免疫）抓出 110 条；明令禁止以重排"修复"。
3. "零泄漏"认证下仍含 248 条逐字原题（三机制盲区）→ 催生 D/E/F 通道与双实现复核制度。

### D. 阈值定标记录
- 长题干（≥25 字）Jaccard 0.45：0.45–0.55 区间人工核对大量为同病例改写。
- 短题干（<25 字）0.75：句式相似度虚高（「降香…的功效是」vs「木香…的功效是」J=0.71 而为不同题）。
- D 通道题干相似度 0.5→0.8：0.5 时 B 型题共用选项池成片误判。

### E. 归因细则与补救记录
- 终轮归因：744 道闭集错题 = 68 真缺口 / 454 已教但错在辨析 / 222 未匹配。
- 收尾轮：596 道闭集错题逐题处置 → 396 张对比卡；已教主题一律不再补知识量。
- 防自欺判据：判"金标错/口径不符/指标伪影"必须举与分数无关的证据（权威文件、逐条内容核查、评分器源码），举不出即归为模型知识缺失。
- 盲重答复核：79 条金标存疑经"不看金标盲答"复核，推翻 29 条。
- 143 条金标存疑登记在案；5 条药典级 discrepancy（3 位执业医师确认前只写 discrepancy）。
- [TODO] 示例卡脱敏后补入 3–5 张。

---

## Additional file 2 — Data construction logs（数据构建日志）

*正文引用处：Methods 3.3（rejection logs）*

### A. 证据表合成判废明细（3,730 收 / 331 废 / 8.9%，废因逐条留档）

| 包 | 收 | 判废 | 主要废因 |
|---|---:|---:|---|
| P1 合方 | 722 | 78 | 文献口吻 32 / 该写全组成却漏药 26 / 问句重复 18 |
| P3 证素 | 483 | 110 | 问法骨架超密度封顶 75 / 未点出主体名 32 |
| P4 证候 | 700 | 94 | 未点出主体名 74 / 过短 17 |
| P6 药物 | 694 | 5 | 剂量不在药典原文里 3 |
| P7 安全 | 98 | 20 | 密度封顶 17 / 剂量 3 |
| 其余 | 702 | 24 | — |

问法骨架多样性实测（掩实体后，门槛 5%）：LLM 包 3,246 条 / 2,389 种骨架 / 最大占比 1.2%；手写包 1,564 条 / 1,038 种 / 1.2%；通用集 1,027 条 / 1,027 种 / 0.1%。

### B. 逐条溯源方法与校准
- 判定顺序：建库声明优先于回溯（声明=过程真值，回溯=外部证据）。
- 六路判定计数：声明 71,520 / 回溯 59,616 / 声明·无上游 3,342 / 按构造 716 / trust_src 437 / 未定 166。
- 分来源一致率：药典 99% / 国标 97% / TCM-SD 96% / 习题集 87% / 教材 71%（总 86.2%）。
- 三个判据缺陷修复：① ≥300 条共现的 12-gram 判为模板并遮蔽；② 27 本旧版次单列；③ 原产地优先规则（药典/国标 > 教材 > 古籍 > 习题集），一致率 80.6%→86.2%。
- 6,860 条 ambiguous 只给候选册清单，不硬判。
- 工具：prov_{engine,run,retrieve,calib,write,summary} 六脚本；标注版数据随论文发布。

---

## Additional file 3 — Evaluation protocol deviations（评测协议偏离）

*正文引用处：Methods 4.1（four deviations）*

1. **抽取桥接**：`_postprocess_bridge.py` 接入 7 个子集读答案路径；系统性抬分 → 正文 4.3 以三档口径（L0/L1/L2）量化该偏差，且我方分数不与官方排行榜并列。
2. **think/nothink 定义**：官方 `--prompt-type 2` 为提示层 CoT；我方 `TCM_THINKING` 为 chat template 开关，官方无此概念。
3. **子集**：官方 12 集，我方生成 11（TCM-FT 缺官方 prompt yaml，会中断评测链）、打分 10 + SE-A 自有裁判；题量 6,997。
4. **解码参数固定**（官方未规定）：贪婪 / repetition_penalty 1.05 / max_new_tokens 1024 / sdpa。

---

## Additional file 4 — Baseline exclusions and training details（基线排除与训练细节）

*正文引用处：Methods 4.2（excluded baselines）*

### A. 基线排除清单（看分前、结构性理由）
| 模型 | 排除理由 |
|---|---|
| PULSE-7bv5 | BLOOM 底座无 sdpa 实现，仅 eager，外推约 2 小时且加批更慢 |
| Zhongjing-LLaMA | Ziya 底座上下文 2048，装不下 few-shot 提示 |
| TaiYi-LLM | 外推 4–5 小时 |
| WiNGPT2 | 下载残缺，仅 1/4 分片 |
| Lingdan-13B-PR | 无 chat_template、输出退化重复、128 题 673 s（注：其 tokenizer bug 已修复，排除理由不是装不上） |
| BigDataTCM-34B | org 无公开权重（401）；仅 4bit 量化版，不能与 bf16 同表 |

### B. 训练与合并验收细节
- 分维度 val loss（epoch 1）：总体 0.9442 / 诊断 0.6994 / 知识问答 1.2306 / 安全 0.5162 / 处方 0.2373 / 文献抽取 0.0516 / 语言理解 0.0945 / 诊断 CoT 0.3505 / 自由问答 1.1257 / 通用对齐 1.2521；loss_history 485 点。
- 训练：7×RTX PRO 6000，LoRA r=64 / α=128 / dropout 0.05，有效 batch 28，lr 1.18×10^-4，cutoff 1536（截断 0/135,797），4,850 步 / 9,856 s，峰值显存 82.04/97.9 GB，final train loss 0.8694。
- 合并验收：命中 220/220；索引 1,045/1,045 缺 0 多 0；已合并模块（q_proj / in_proj_qkv）相对改动 9.9% / 9.3%；未合并模块（layernorm / routed experts / router）与基座逐位相同。
- LoRA 目标正则（全文）：`^model\.layers\.[0-9]+\.(self_attn\.(q|k|v|o)_proj|linear_attn\.(in_proj_qkv|out_proj)|mlp\.shared_expert\.(gate|up|down)_proj)$`

### C. SE-A 裁判说明
- 官方裁判 GLM-4-Air-250414 不可用（无 key）；自有固定裁判、同 rubric、同金标，仅对 untrained base 与 TCMedSeek 两列打分。
- 因此 SE-A 绝对分不与任何排行榜并列，只有两列之间的差可用（63.90 → 72.50）。

---

## 正文引用核对表

| 正文位置 | 引用 | 对应本文件 |
|---|---|---|
| Methods 3.1（iteration ledger）| Additional file 1 | AF1 |
| Discussion 6.2（leak-cleanup ledger）| Additional file 1 | AF1 |
| Methods 3.3（rejection logs）| Additional file 2 | AF2 |
| Methods 4.1（four deviations）| Additional file 3 | AF3 |
| Methods 4.2（excluded baselines）| Additional file 4 | AF4 |

> 原尺寸较大而不随投稿发布的材料（13 模型逐题 raw/score、训练日志全文、标注版全量语料）在 Data availability 声明中说明获取方式。
