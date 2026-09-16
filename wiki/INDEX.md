# Wiki 索引

## 来源笔记

- [[wiki/source/chatbot-arena|Chatbot Arena：基于人类偏好的大模型评测平台]] — 30 页全文：数据、BT 排名、主动采样、专家复标、全部附录及统计/公式疑点。

- [[wiki/source/深度学习基础-2026暑期学校|深度学习基础：2026 暑期学校]] — 96 页完整五模块笔记：公式、例子、工程细节、书目、练习入口与勘误。
- [[wiki/source/deepseek-v4-1-flash|DeepSeek-V4.1-Flash 技术报告]] — 51 页全文整理：架构、训练、系统、全部结果表、附录、图 6 数值及证据限制。

## 概念

- [[wiki/concept/交叉熵-困惑度与BPB|交叉熵、困惑度与 BPB]] — 概率预测指标的定义、换算关系、token 示例与评估边界。
- [[wiki/concept/泛化与数据质量|泛化与数据质量]] — 过拟合、数据覆盖与去重、训练/验证/测试的分工。
- [[wiki/concept/动量-AdamW与权重衰减|动量、AdamW 与权重衰减]] — 参数更新机制、L2 与衰减的区别，以及报告的混合优化方案。
- [[wiki/concept/学习率与批量调度|学习率与批量调度]] — 步长、预热、余弦衰减及报告的实际训练日程。
- [[wiki/concept/非线性表示与归一化|非线性表示与归一化]] — MLP、激活函数以及 BN/LN/RMSNorm 的作用与区别。
- [[wiki/concept/Softmax与温度采样|Softmax 与温度采样]] — logits 到概率、温度示例及其与 top-p 的区别。

## 跨来源对照

- [[wiki/synthesis/深度学习基础与DeepSeek报告的共同概念|深度学习基础与 DeepSeek 报告的共同概念]] — 对照概率预测与 BPB、泛化与数据、优化器、学习率、非线性表示及温度采样，注明对应页码与区别。

## 原始资料目录

### 深度学习基础

- [[raw/深度学习基础/深度学习基础_2026暑期学校.pdf|深度学习基础课件 PDF]] — 魏鸿鑫主讲，2026 暑期学校，96 页；已完成全文文本导读。

### 大模型技术报告 / DeepSeek-V4.1-Flash

- [[raw/大模型技术报告/DeepSeek-V4.1-Flash/DeepSeek_V41_Tech_Report.pdf|DeepSeek 技术报告 PDF]] — 51 页，当前仅局部阅读。
- [[raw/大模型技术报告/DeepSeek-V4.1-Flash/img_v3_0215e_1d574a93-1181-47ad-af6e-e46320b7f04g.png|DeepSeek 后训练段落截图]] — 涉及 SFT、RL、OPD 与数据管线；原文页码待核对。

### 大模型评测 / Chatbot Arena

- [[raw/大模型评测/Chatbot-Arena/Chatbot_Arena_ICML_2024.pdf|Chatbot Arena 论文 PDF]] — ICML 2024 正式版，研究众包成对比较与人类偏好排名。

## 维护记录

- [[wiki/LOG|变更日志]] — 记录资料入库、阅读笔记和维护变更。
