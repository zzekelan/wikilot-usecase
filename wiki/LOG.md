# Wiki 变更日志

## [2026-09-14] 阅读问答入库 | DeepSeek-V4.1-Flash 的研发场景评估

- 按用户要求，将“real-world R&D scenarios”的解释写入[[wiki/source/deepseek-v4-1-flash|报告来源笔记]]，注明[[raw/DeepSeek_V41_Tech_Report.pdf|原文]]第 24 页出处。
- 记录内部评估语料的组成、困惑度与 BPB 的含义，区分作者的评估说明和阅读解读。
- 更新[[wiki/INDEX|Wiki 索引]]。原始 PDF 和截图未修改。
- 待办：核读图 6 与评估集细节；当前来源笔记不是全文总结。工作区用途与阅读偏好的 schema 记录仍待用户确认，本次未修改 AGENTS.md。

## [2026-09-14] 入库与分类 | 深度学习基础课件及 raw 整理

- 读取课件全部 96 页的可提取文本，视觉核对第 70、87 页；新增[[wiki/source/深度学习基础-2026暑期学校|五模块导读与勘误]]，记录阅读范围与页码。
- 将三份原始资料按主题移动，保留文件名，逐一核验移动前后 SHA-256 一致。
- 路径迁移记录（旧路径仅为历史记录）：
  - `raw/深度学习基础_2026暑期学校.pdf` → [[raw/深度学习基础/深度学习基础_2026暑期学校.pdf|深度学习基础课件]]。
  - `raw/DeepSeek_V41_Tech_Report.pdf` → [[raw/大模型技术报告/DeepSeek-V4.1-Flash/DeepSeek_V41_Tech_Report.pdf|DeepSeek 报告]]。
  - `raw/img_v3_0215e_1d574a93-1181-47ad-af6e-e46320b7f04g.png` → [[raw/大模型技术报告/DeepSeek-V4.1-Flash/img_v3_0215e_1d574a93-1181-47ad-af6e-e46320b7f04g.png|后训练截图]]。
- 更新[[wiki/INDEX|索引]]及[[wiki/source/deepseek-v4-1-flash|DeepSeek 笔记]]中的原文路径，补充截图与基础课件的关联。历史日志保留不改，旧链接由本条迁移记录追溯。
- 未完成事项：未运行课件实验或逐图复核全部图表，未对引用论文做外部核查；DeepSeek 报告仍为局部精读，截图页码待核对。
- 自动审批拒绝额外写入 AGENTS.md，原因是超出本次任务范围的持久配置变更；已放弃该修改，AGENTS.md 保持原状。

## [2026-09-14] 阅读问答入库 | 困惑度的含义

- 在[[wiki/source/deepseek-v4-1-flash|DeepSeek 来源笔记]]补充困惑度的直观示例、通用定义、比较前提及与 BPB 的区别，明确概念补充与报告原文的边界。
- 更新[[wiki/INDEX|索引]]描述；未新增原文阅读范围，图 6 和评估集细节仍待核读。


## [2026-09-14] 问答综合 | 深度学习基础与 DeepSeek 的共同概念

- 补读报告第 7、14–15、20–22、24–25、31–32 页，建立[[wiki/synthesis/深度学习基础与DeepSeek报告的共同概念|共同概念对照]]，连接概率预测与 BPB、泛化、优化、调度、网络表示和温度采样。
- 更新[[wiki/source/deepseek-v4-1-flash|报告笔记]]阅读范围，以及[[wiki/source/深度学习基础-2026暑期学校|课件笔记]]与[[wiki/INDEX|索引]]的链接。
- 区分报告直接陈述与数学解释，明确混合优化器、RMSNorm 与 LN、OPD 与标签平滑的区别。图 6 仅核读图注，数值仍待核验；未外部核查实验。

## [2026-09-14] 概念整理 | 深度学习基础与 DeepSeek 共用概念

- 按用户要求建立六个概念页：[[wiki/concept/交叉熵-困惑度与BPB|概率预测指标]]、[[wiki/concept/泛化与数据质量|泛化与数据]]、[[wiki/concept/动量-AdamW与权重衰减|优化机制]]、[[wiki/concept/学习率与批量调度|学习率调度]]、[[wiki/concept/非线性表示与归一化|网络组件]]及[[wiki/concept/Softmax与温度采样|概率与采样]]。
- 各页记录定义、适用范围、例子、两份来源的对应页码和相关概念；区分原文与补充解释。
- 更新[[wiki/INDEX|索引]]及[[wiki/synthesis/深度学习基础与DeepSeek报告的共同概念|跨来源对照]]的概念导航，保留已有来源笔记和综合解释。
- 本次基于已核读资料整理，未新增外部研究或实验；报告图 6 的数值及评估数据隔离细节仍待核查。

## [2026-09-16] 入库与分类 | Chatbot Arena 论文

- 从 PMLR 官方论文页定位并下载 ICML 2024 正式版，归档至 [[raw/大模型评测/Chatbot-Arena/Chatbot_Arena_ICML_2024.pdf|大模型评测 / Chatbot Arena]]，已验证为 PDF 文件。
- 新增[[wiki/source/chatbot-arena|论文来源笔记]]，记录作者、发表信息、下载来源与摘要要点；更新[[wiki/INDEX|索引]]。
- 本次完成查找与归档，未全文精读；未修改已有原始资料。

## [2026-09-16] 身份核查 | Chatbot Arena 与 Arena.ai

- 根据 LMSYS 与 Arena 官方页面，确认 Chatbot Arena → LMArena → Arena 的沿革及 UC Berkeley 研究项目起源，补入[[wiki/source/chatbot-arena|来源笔记]]。
- 区分伯克利学术起源与现今公司主体；2024 年论文不代表当前平台全部功能。

## [2026-09-16] 条目整理 | DeepSeek-V4.1-Flash 技术报告

- 完成[[wiki/source/deepseek-v4-1-flash|DeepSeek-V4.1-Flash 技术报告]]：51 页全文整理：架构、训练、系统、全部结果表、附录、图 6 数值及证据限制。
- 同步[[wiki/INDEX|索引]]；本条目独立提交，原始资料未修改。
- 证据以条目所注页码与版本为准；限制、疑点或未公开信息在正文保留。

## [2026-09-16] 条目整理 | Chatbot Arena：基于人类偏好的大模型评测平台

- 完成[[wiki/source/chatbot-arena|Chatbot Arena：基于人类偏好的大模型评测平台]]：30 页全文：数据、BT 排名、主动采样、专家复标、全部附录及统计/公式疑点。
- 同步[[wiki/INDEX|索引]]；本条目独立提交，原始资料未修改。
- 证据以条目所注页码与版本为准；限制、疑点或未公开信息在正文保留。
