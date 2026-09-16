# DeepSeek-V4.1-Flash 技术报告

## 来源与阅读范围

- 原题：*DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression*；署名：DeepSeek-AI。研究工程、商务与合规作者名单见附录 A，第 46–47 页。
- 原文：[[raw/大模型技术报告/DeepSeek-V4.1-Flash/DeepSeek_V41_Tech_Report.pdf|本地 PDF]]，51 页。报告链接：[模型仓库](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)、[报告地址](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/DeepSeek_V41_Tech_Report.pdf)。
- 年份：2026；报告第 30 页记载生产部署于 2026 年 9 月上线。
- 阅读范围：全文 51 页，包括参考文献与附录；重点图文核对第 25、33、48、49 页。整理日期：2026-09-16。下文引用均为 **PDF 页码**，实验数值来自报告。
- [[raw/大模型技术报告/DeepSeek-V4.1-Flash/img_v3_0215e_1d574a93-1181-47ad-af6e-e46320b7f04g.png|后训练截图]]已核对为第 **6 页**“Building on this base model…”段落，不是第 25 页；内容概括了 SFT、RL、OPD 与数据管线的关系。

## 核心论点与章节地图

**作者论点：** 长时程智能体具有输入重、前缀复用多、上下文长的负载特征，瓶颈不只在注意力 FLOPs，也在 KV 的 HBM/SSD 容量和搬运。报告协同改变架构、缓存精度、状态恢复与训练数据，主张在能力提升时继续降成本。这套方案贯穿模型架构、训练和服务系统。出处：第 1、4–6、37 页。

| 范围 | 内容 |
| --- | --- |
| 1–7 | 摘要、目录、动机、能力主张、总架构图 |
| 7–16，§2 | 多模态主干、CED、CSA2、分层索引、mHC、Engram、DSpark、FP4、优化器与算法 1 |
| 16–20，§3 | 多模态分布式训练、共享注意力状态、Engram 分片、推理内核、持久缓存与重放 |
| 20–25，§4 | 文本/多模态数据、模型与训练超参数、基础模型表 1、研发 BPB 图 6 |
| 25–32，§5.1–5.2 | 合成任务、跨框架 RL、DSec、推理力度、异步调度与多教师 OPD |
| 32–36，§5.3 | 评测协议、表 3–4、力度控制、跨框架、多智能体 |
| 37 | 结论、极端输入与近似缓存的稳健性限制 |
| 38–45 | 相关架构、优化器、训练系统与评测基准的参考文献 |
| 46–51，附录 A–C | 作者名单、框架版本、力度细分曲线、指数 token 惩罚的局部推导 |

## 一、架构：降低不同环节的成本

| 项目 | 本报告配置与作用 | 页码 |
| --- | --- | --- |
| 参数口径 | 552B **主干**参数，另有 196B Engram；prefill 激活 8B/token，decode 激活 16B/token；不能把 552B 称含 Engram 的全部参数 | 7、13、22 |
| 主干 | 图像和文本输入，自回归文本输出；40 层、隐藏维 5120；20 层因果 encoder + 20 层 decoder | 7、21–22 |
| CED | decoder 的全局 KV 来自最后 encoder 隐状态的投影；长输入大部分不做完整 decoder 前向，局部 SWA 仍需重建 | 9 |
| CSA2 | 首两层仅 SWA；其余 encoder 18 层按 3×6 分组，每组 Full+5 Reuse，压缩比 2；decoder 20 层分 5×4，首组 Full+3 Reuse，其余 Reindex+3 Reuse，压缩比 1 | 10–12、22 |
| 注意力 | 64 个 query 头、头维 512、query 压缩维 1280；indexer 32 头、头维 128；Top-512；输出投影 8 组、中间维 1024；SWA 窗口 128 | 22 |
| 分层索引 | decoder 首个 Full 扫全范围，再按块最大分数选至多 2048×8=16384 个候选；后续 Reindex 在候选池内选 512。首轮扫描仍依赖上下文长度 | 11–12 |
| MoE | 每层 1 共享专家+384 路由专家，激活后者中的 6 个；专家中间维 2304；SwiGLU，clamp=10；图像和文本分别更新负载偏置 | 8、22 |
| Single-Pass mHC | 把输入混合系数错后一块使用，消除依赖；Mega-mHC 融合后激活流量从 (4n+4)d 降至 (2n+2)d；n=4、Sinkhorn-Knopp 20 次 | 12–13、22 |
| Engram | 条件记忆查表，196B 分两模块；2/3/4-gram、每阶 8 个 hash 头、总嵌入维 2048；每头约 16M 条目，互异素数表长；零基层号 1、14 | 13 |
| DSpark | 3 个 Transformer 块、窗口 128；一次并行草拟 5 个位置，用 Markov head 建模依赖，置信头结合吞吐曲线选择验证长度 | 13–14 |
| 精度 | 主 KV 用 E2M1、每 16 通道一个 E4M3 scale，省略二级 global scale；RoPE 后量化；indexer 采用 MXFP4；敏感的 SWA KV 保留 FP8 | 14 |

DSpark 在主干预训练结束后单独训练（主干冻结），后训练中随主干更新但其目标梯度不传入主干；主 KV 的 QAT 与分层候选限制在后训练引入。不能说全部组件从预训练起就按最终部署方式运行。出处：第 8、12、14 页。

## 二、多模态与基础设施

DeepSeek-ViT 为 32 层、维度 1024、16 头、patch=14；用 2D-RoPE 支持变分辨率，线性 patch 投影适配 Muon，RMSNorm、SwiGLU；3×3 pixel-unshuffle 将视觉 token 数减为 1/9，再经两层 MLP 投影器接入主干（第 8、22 页）。视觉预训练先用约 **47B 图文对**做 SigLIP 对比学习（最高 224²），再接 4B MoE 语言模型，以 **236B token**做自回归微调（分辨率 544²–1344²），之后丢弃该临时语言模型。集成主干时视觉编码器先冻结，最终归一化和投影器可训练，学习率衰减阶段再解冻并用较小学习率（第 15、22–23 页）。这些计数不是把图文对与 token 当同一种单位相加。

训练系统要点（第 16–18 页）：

- 对比学习的两路 all-gather 与另一模态的前/反向重叠；视觉编码器独立部署为“视觉前向→LLM 前反向→视觉反向”。
- 超长图像密集序列按上下文并行 rank 均衡分片，每图只加载一次；RL 中增量传图并复用 CPU 预处理结果。
- CSA2 跨流水线 stage 共享由 shadow indexer、唯一参数 owner、梯度聚合、扩展通信载荷和 micro-batch 生命周期管理实现。
- Engram 按行分片，优化器状态再分片；确定性 token 索引允许提前取表，梯度延后回传。部署可从主机经 RDMA 预取；RL rollout 则使表常驻 GPU，二者不是矛盾。

推理系统（第 18–20 页）：融合 FlashMLA、DeepGEMM、TileKernels、DeepSelect 等内核；**Reuse 层**每次 prefill 15 个 kernel、decode 11 个，不是整模型总数。采用视觉 Encoder–Prefill–Decode 解耦（EPD）。全局 KV 为 **890 字节/token**，约前代 V4-Flash 的 1/4；持久 KV 约 1/8，来自全局 KV 压缩再叠加不持久保存 SWA。

全局 KV 保留至少 72 小时；encoder SWA 使用每机约 10% host DRAM 构成的短 TTL 池，decoder SWA 不做前缀缓存。缺失时只重放最后 128 token，而非精确恢复需要的层数×窗口。**有界重放是近似恢复**：后续状态会依赖缓存命中边界；作者称实验退化可忽略，不构成所有输入上的等价证明（第 19–20、37 页）。图 2 的 FLOPs 对 BF16/FP8/FP4 分别加权 1/0.5/0.25，4K→1M 上下文的单 token decode 加权 FLOPs 约增加 1/4；不是端到端时延实测（第 5 页）。

## 三、预训练数据与优化

文本侧强调信息增益、scaling ladder、领域专家质量评估，以及较新的仓库、提交、依赖和框架；过滤弱模型生成和低质量机器翻译等“隐式重复”。多模态侧以原生网页/PDF 为主，包含图文对、交错图文和领域数据；从 Common Crawl 重新构建覆盖，先廉价过滤再下载图像，再做图像感知去重和 SmolVLM 评分，部分淘汰文档回收为图文对，补充 OCR、grounding、pointing、图像代码及 computer-use 轨迹。纯文本与多模态重叠样本优先保留后者，最终 token 比 **7:1**，packing padding≤10⁻⁴。出处：第 20–21 页。

总训练 **45T token**；固定 batch **100.6M token**；从 64K 稀疏注意力起训、无 dense warmup，在 34T 扩至 1M。前 2000 步线性预热，至 28T 保持 2.6×10⁻⁴，28T–40T 余弦降到 2.6×10⁻⁵，40T–45T 保持；28T 开始解冻视觉编码器（第 15、22 页）。详见[[wiki/concept/学习率与批量调度|训练调度]]。

| 参数组 | 优化与关键参数（第 15–16、22 页） |
| --- | --- |
| RMSNorm 等非矩阵 | AdamW，β₁=.9、β₂=.95、ε=10⁻²⁰、weight decay=.1；bias/scaling 不衰减 |
| 线性矩阵/投影器 | Muon；Q/K 按 head 分块；Nesterov momentum=.95、decay=.1；更新 RMS=.18 |
| Engram、token embedding、预测头 | 动量后做 Sinkhorn 行列归一化，K=11、τ=10⁻³、ε=10⁻²⁰、学习率修正 .18；无 weight decay；Engram 学习率再×5 |

多模态路由 bias 更新速率均 .001，同时仍保留权重 .0001 的序列级平衡损失；“auxiliary-loss-free”不能理解为整个训练完全无平衡辅助项。使用 sample-level attention mask（第 22 页）。基础解释见[[wiki/concept/动量-AdamW与权重衰减|优化器]]、[[wiki/concept/泛化与数据质量|数据与泛化]]。

## 四、基础模型完整结果：表 1 与图 6

表 1 在内部统一评测框架下比较 **Base**；表中分差≤0.3 被作者视作同水平，但不是统计显著性检验。除注明外，分数越高越好；“—”表示未报告（第 24 页）。

| 基准（指标） | shots | V4-Flash | V4-Pro | V4.1-Flash |
| --- | --- | ---: | ---: | ---: |
| AGIEval（EM） | 3–5 | 83.9 | 84.4 | 83.4 |
| MMLU-Pro（EM） | 5 | 68.3 | 73.5 | 74.1 |
| C-Eval（EM） | 5 | 92.1 | 93.1 | 92.1 |
| MultiLoKo（LLM-Judge） | 5 | 42.6 | 50.9 | 45.5 |
| SimpleQA-Verified（EM） | 25 | 30.1 | 55.2 | 42.3 |
| SuperGPQA（EM） | 5 | 46.5 | 53.9 | 53.1 |
| BBH（EM） | 3 | 86.9 | 87.5 | 86.1 |
| BBEH（EM） | 1 | 25.4 | 29.8 | 27.2 |
| DROP（F1） | 1 | 88.6 | 88.7 | 87.9 |
| HellaSwag（EM） | 0 | 85.7 | 88.0 | 87.2 |
| BigCodeBench（Pass@1） | 3 | 56.8 | 59.2 | 60.6 |
| HumanEval（Pass@1） | 0 | 69.5 | 76.8 | 79.4 |
| GSM8K（EM） | 8 | 90.8 | 92.6 | 93.0 |
| MATH（EM） | 4 | 57.4 | 64.5 | 61.1 |
| MGSM（EM） | 8 | 85.7 | 84.4 | 80.2 |
| LongBench-V2（EM） | 1 | 44.7 | 51.5 | 45.2 |
| MMMU-Pro（EM） | 4 | — | — | 56.5 |
| CVBench（EM） | 4 | — | — | 77.9 |
| DocVQA（LLM-Judge） | 4 | — | — | 95.6 |
| RefCOCO-avg（Acc@0.5） | 0 | — | — | 86.0 |

V4-Flash/V4-Pro 的主干参数分别 284B/1.6T，激活 13B/49B；本代 552B、8B/16B。结果体现取舍，不能概括为每项都超过 V4-Pro（第 24 页）。

**R&D** 指 Research and Development（研发）。第 24 页以日常研发单独收集的内部文档、非公开代码和学术资料评估概率建模。图 6（第 25 页，已视觉核对）的完整数值如下，**BPB 越低越好**：

| 留出语料 | V4-Flash-Base | V4-Pro-Base | V4.1-Flash-Base |
| --- | ---: | ---: | ---: |
| 内部文档 | .617 | .590 | .564 |
| 内部代码仓库 | .1562 | .1494 | .1443 |
| 学术资料 | .4929 | .4677 | .4305 |

以 (旧−新)/旧计算，相对 V4-Flash 下降约 **8.6%/7.6%/12.7%**，相对 V4-Pro 约 **4.4%/3.4%/8.0%**（wiki 按图值计算）。第 6 页的“5%–10%”概括不是每类、每个对照均成立的精确区间。全文未找到这些内部集的样本量、逐项训练隔离/去重审计、误差条或公开下载地址；“held-out”不足以补全这些信息。

BPB 与 PPL 同源于负对数概率但归一化不同；例如单 token 概率 .5 对应单步 PPL=2，**不是 BPB=2**。完整定义见[[wiki/concept/交叉熵-困惑度与BPB|概率预测指标]]。作者说 API 无法进行此类测试，应读作其所用 API 的限制；支持充分 logprob 的其他接口未必如此。更低 BPB 不等于已验证能独立完成研发。

## 五、后训练与智能体环境

作者明确沿用 **SFT→RL→OPD**，不主张新后训练算法，主要归因于数据/环境工程；其“几乎全部提升来自数据”的归因属于作者结论，报告未提供足够隔离消融让本 wiki 独立确认（第 6、25 页）。

1. **任务三元组**＝问题、环境、验证系统；以难度和正确性训练构题能力，轨迹在后续 RL 中持续复审质量。
2. **通用智能体**：员工/合作方自愿反馈的工作流、接口和失败案例，生成 mocked 工具、单多轮环境，不应理解为公开用户生产数据均可随意使用。
3. **代码智能体**：高难/失败会话及达到 star 门槛的 GitHub 项目；构题 agent→隔离容器搭建→多 agent 解题→独立质检→修复再验。保留 fail-to-pass 与 pass-to-pass 测试，清除答案痕迹，检查可投机性（第 25–26 页）。
4. **跨框架 RL**：sandbox 执行工具，worker 统一轨迹与训练控制；模型合并后重新初始化后续 RL run，图 7–8 的断段不是同一 run 的连续优化（第 26–28 页）。
5. **DSec**：百万级并发 sandbox 的作者部署主张；分片、自定义最终一致 placement+节点硬准入、sub-NUMA worker VM。相似负载下单机密度约 1000→2500+；LS 类、SCHED_IDLE/core scheduling 降低干扰；AppArmor/eBPF 隔离，破坏环境计失败并回传惩罚信号（第 27–29 页）。
6. **推理力度**：b∈1…100，训练在相同问题与 b 的子组内计算优势，长度惩罚系数 k(b) 指数下降。2026-09 报告 API low/high/max→50/75/100；不是硬 token 上限（第 29–30 页）。
7. **异步训练**：rollout/train 同设备分时；sample-level 完成计数触发新 prompt，避免 batch 粒度震荡和 group 内长尾。限制数据集并发、丢弃早返短样本缓解长度偏差；限制离策略比例、屏蔽过旧 token；token 级暂停、保存 KV/专家路由、拼接 routing replay、样本完成即回收（第 30–31 页）。
8. **OPD**：最终全词表蒸馏覆盖全领域，使用 **40 多个教师**，可来自不同训练阶段/架构；异步处理中保持配比、教师和并发配置切换一致。正文没有给出可直接复现的完整 OPD loss 或全部教师清单（第 31–32 页）。

## 六、后训练完整基准表与比较条件

表 3（第 33 页）汇总后训练模型的评测结果。 以下列顺序与原表一致；K3 为正文所称 Kimi-K3；横线不表示零。HLE 的 † 是 text-only 子集，不能与完整 HLE 混比。除 Codeforces rating 外下列为百分制/报告评分。

| 基准（指标） | Opus-5 Max | GPT-5.6 Sol Max | K3 Max | GLM-5.3 | V4-Pro Max | V4-Flash Max | V4.1-Flash Max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| GPQA Diamond（Pass@1） | 93.4 | 94.1 | 92.9 | 88.1 | 92.4 | 89.9 | 90.9 |
| HLE（Pass@1） | 56.3 | 44.5 | 43.5 | 42.0† | 42.7† | 37.8† | 36.8（39.1†） |
| Codeforces（Rating） | — | — | — | — | 3348 | 3289 | 3471 |
| MathArena Apex（Pass@1） | — | — | 65.6 | — | 65.3 | 58.6 | 65.6 |
| Terminal-Bench 2.1（Pass@1） | 89.1 | 88.8 | 88.3 | 88.2 | 87.9 | 82.7 | 90.6 |
| Terminal-Bench 3.0（Pass@1） | 43.3 | 34.4 | 17.7 | 28.3 | 11.8 | 7.6 | 30.0 |
| Terminal-Bench 4.0（Pass@1） | 51.8 | 39.9 | 12.6 | 37.9 | 12.4 | 7.0 | 31.2 |
| DeepSWE v1.1（Resolved） | 74.0 | 73.0 | 67.5 | 66.9 | 62.7 | 54.4 | 74.2 |
| ProgramBench（Almost@1） | 37.0 | 23.0 | 17.5 | 19.0 | 15.5 | — | 20.3 |
| NL2Repo-Bench（Score） | 75.3 | 56.8 | 58.0 | 58.0 | 61.5 | 54.2 | 65.4 |
| CyberGym（Pass@1） | — | 84.5 | 80.0 | 84.5 | 83.3 | 76.7 | 88.1 |
| SEC-Bench Pro（Pass@1） | — | 74.3 | — | — | 56.4 | 30.9 | 62.8 |
| ExploitGym（Pass@1） | 22.1 | 33.7 | — | 15.0 | 5.4 | 1.8 | 15.3 |
| HLE with tools（Pass@1） | 63.6 | — | 59.8 | 62.5 | 60.0 | 51.5 | 63.9 |
| AutomationBench（Pass@1） | 50.3 | 45.8 | 46.7 | 48.8 | 43.2 | 37.7 | 54.8 |
| Agents’ Last Exam（Pass@1） | 28.6 | 26.7 | 27.6 | 28.5 | 25.7 | 25.2 | 31.8 |
| Chartography with tools（Pass@1） | 84.0 | 79.9 | 68.1 | — | — | — | 78.9 |
| BabyVision with tools（Pass@1） | 94.1 | 88.9 | 85.7 | — | — | — | 89.6 |
| ZeroBench-main with tools（Pass@5） | 52.0 | 53.0 | 41.0 | — | — | — | 49.0 |

协议（第 32、35、47–48 页）：推理温度/top-p=1/1；代码智能体通常 DSH Minimal、1M context、1/.95，DeepSWE 改用 mini-SWE，SEC-Bench Pro（260505）用 Claude Code；视觉 agent 用 Claude Code、512K；AutomationBench v1.0.6 公开集与 ALE-CLI 用官方 scaffold。评测限制网络、移除 Git 历史和临时 build/package cache，仍观察到投机行为。不能把工具辅助结果当成纯模型闭卷分数。采样概念见[[wiki/concept/Softmax与温度采样|Softmax 与温度采样]]。

表 4（第 35 页）的 **同一 checkpoint** 跨框架结果：

| 框架 | DeepSWE v1.1（Resolved） | Terminal-Bench v2.1（Pass@1） |
| --- | ---: | ---: |
| Claude Code v2.1.251 | 69.8 | 88.0 |
| Codex v0.147.0 | 65.6 | 84.1 |
| OpenCode v1.18.15 | 65.5 | 85.0 |
| Pi v0.84.2 | 66.2 | 86.1 |
| mini-SWE，commit 04d809ceab9d | 74.2 | 90.3 |
| DSH Minimal | 72.6 | 90.6 |
| DSH Standard | 70.5 | 85.8 |
| DSH PTC | 67.6 | 85.8 |

共同条件：Linux、effort=100、1M context、temperature=1、top-p=.95、max_steps=500；两任务每题分别 N=8/N=3，**多次采样用于估计单次表现，不等于 Pass@8/Pass@3**；Terminal-Bench 禁网。无额外实验 system prompt，但保留各框架原生 prompt/tool schema。DSH Standard/PTC 版本 v0.1.1+custom.202609011522，分别 26 个初始函数工具、通过 TypeScript run_code 调用 24 个底层工具。附录表 5 的 Claude Code 版本 2.1.105/.238/.251/.259：DeepSWE=68.4/68.7/69.8/68.6（未舍入平均 68.9），Terminal=87.3/88.4/88.0/87.6（均 87.8）。

## 七、力度曲线、多智能体与附录推导

图 9：effort 25→100，八项推理均值 67.1→76.3、DeepSWE 66.0→74.2、Terminal 82.4→90.6，输出约×2.5（第 34–35 页）。**但不能推广为逐点单调提升**：附录 B.2/图 11（第 48–49 页）明确存在跨框架平台与下跌，长度也有局部波动。正文关于 60–80 力度可用不到一半 token 接近最高分是作者概括，不保证所有框架/预算点成立。

图 12 的八项为 AIME 2026、Apex 2025 Shortlist、GPQA Diamond、HLE-Text、IMO-AnswerBench、LiveCodeBench、MathArena Apex、SimpleQA-Verified；正文举例 MathArena 25.3→65.6（+40.3 点），AIME 最高 100%，AIME 长度 4.6k→11.4k、MathArena 29.1k→86.1k（第 48–50 页）。曲线未提供逐点机器可读数据，未从像素推造精确数值。

**Agent Team** 用 lead 分派 fresh/fork teammate、共享仓库、持久 mailbox 与带 revision 检查的任务板；write scope 是 advisory，不等同强制文件锁。奖励＝任务表现+协作奖励−derived latency；后者按 token 固定速率和工具实测耗时构造事件 DAG，取关键路径，弱化服务排队影响（第 35–36 页）。

初步实验（图 10，第 36 页）仅比较“观察到最强”的配置：ProgramBench 过滤为参考解≥95% 的 **172 个 golden 任务**，每配置计划 516 rollouts（每题至多 3），Almost@1 指每次 rollout 得分≥.95；1–12h 截止时读取已有输出。multi 从 1h 的 13.59% 到 8h 峰值 30.04%，single 对应 12.79%/20.39%。FrontierSWE v2 是公开 no-GPU 子集、Mean@5，1–20h：multi 13.50→32.90，single 10.50→28.20。不是同算力预算的因果消融，也不是表 3 原始 ProgramBench 集的直接替代。

附录 C（第 49–51 页）在未触及惩罚 cap 的内部最优点假设 p′(ℓ)≈a·exp(−ℓ/s)，与 k(b)=k₀exp(−(b−b_min)/τ) 联立得到最优长度关于 b 近似仿射。作者明确说这是局部奖励模型，不保证观测长度线性或逐点单调；达到 cap 后边际惩罚归零需另论。

## 八、结果解读与原文疑点

- 第 6 页“能完成超过 95% 现实任务”未定义目标任务总体、抽样和区间，**不可作为普遍成功率入库**。第 37 页也承认最高难任务与大模型仍有差距。
- 第 37 页对比名称出现 Fable-5、GPT-6 Astra，与表 3 的 Opus-5、GPT-5.6 Sol 不一致；保留原文差异，未知是否编辑遗留，不能擅自认定为同一模型。
- 890 B/token 只指全局 KV，不含权重、所有局部缓存、激活、Engram 和系统开销；1/4、1/8 不等于整体成本同比下降。未提供统一硬件下完整美元成本、时延、置信区间和每组件消融矩阵。
- 稀疏选择可能漏检；重放非精确；未测极端上下文不能按无损处理。安全任务高分不等于模型安全；作者提醒双重用途，报告非完整安全评估。

与[[wiki/source/深度学习基础-2026暑期学校|基础课件]]的数学联系见[[wiki/synthesis/深度学习基础与DeepSeek报告的共同概念|共同概念对照]]；与[[wiki/source/chatbot-arena|Arena 论文]]共同关注评测的人群、任务、采样与统计不确定性。

## 关联条目（持续维护）

- [[wiki/concept/Muon与Sinkhorn矩阵优化|Muon 与 Sinkhorn 矩阵优化]]：展开混合优化器方案及算法 1。

- [[wiki/concept/KV缓存与预填充解码|KV 缓存与预填充、解码]]：解释报告降低部署成本时使用的缓存与推理阶段口径。

- [[wiki/concept/CED因果编码器解码器|CED 因果编码器–解码器]]：展开降低 prefill 计算的因果编码器–解码器。

- [[wiki/concept/CSA2压缩稀疏注意力|CSA2 压缩稀疏注意力]]：解释架构图中的 Full、Reindex 与 Reuse。

- [[wiki/concept/分层稀疏索引|分层稀疏索引]]：展开分层候选池的选择与复杂度。

- [[wiki/concept/SWA有界重放|SWA 有界重放]]：展开运行时与持久缓存之间的存储–重算权衡。

- [[wiki/concept/FP4缓存量化|FP4 缓存量化]]：说明主 KV 低精度布局与 QAT。

- [[wiki/concept/MoE与多模态负载均衡|MoE 与多模态负载均衡]]：展开 DeepSeekMoE 的专家配置与图文分模态路由。

- [[wiki/concept/Single-Pass-mHC|Single-Pass mHC]]：解释 Mega-mHC 内核融合所依赖的结构改变。

- [[wiki/entity/Engram|Engram]]：记录条件记忆模块的配置与训练/部署关系。

- [[wiki/concept/推测解码与DSpark|推测解码与 DSpark]]：解释 DSpark 的草拟、验证与训练阶段。

- [[wiki/entity/DeepSeek-ViT|DeepSeek-ViT]]：集中说明视觉编码器及其两阶段训练。

- [[wiki/entity/DeepSeek-V4.1-Flash|DeepSeek-V4.1-Flash]]：作为模型实体总览，连接架构组件与完整结果。

- [[wiki/concept/分布式训练与推理解耦|分布式训练与推理解耦]]：串联多模态训练、共享状态、Engram 分片和 EPD 部署。

- [[wiki/concept/SFT-RL与OPD|SFT、RL 与 OPD]]：整理后训练流程与多教师蒸馏。

- [[wiki/concept/智能体任务合成与验证|智能体任务合成与验证]]：展开自动任务生产、质检和修复循环。

- [[wiki/entity/DSec|DSec]]：记录智能体沙箱平台的身份、调度和隔离设计。

- [[wiki/concept/异步RL与离策略样本|异步 RL 与离策略样本]]：解释异步后训练调度和两类偏差修正。

- [[wiki/concept/推理力度与测试时计算|推理力度与测试时计算]]：展开力度条件、长度奖励、预算曲线和附录推导。

- [[wiki/concept/智能体框架与评测协议|智能体框架与评测协议]]：解释跨框架成绩差异与复现配置。

- [[wiki/entity/DeepSeek-Harness|DeepSeek Harness]]：集中记录框架模式与协作接口。

- [[wiki/concept/多智能体协作与关键路径|多智能体协作与关键路径]]：解释多智能体协作奖励与初步实验。
