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
