# Chatbot Arena

## 平台身份

Chatbot Arena 是由 UC Berkeley 研究人员发起的开放大模型评测平台，自 2023 年 4 月收集匿名对战与人类偏好。用户自由提问，比较两个模型回答后投票；平台以统计方法汇总排名。研究发表于 [[wiki/source/chatbot-arena|ICML 2024 论文]]。

别名与沿革：Chatbot Arena→LMArena→Arena；论文平台、论文数据快照和后来公司的名称属于同一项目发展中的不同对象。

## 2024 论文的数据快照

截至 2024-01-21，表 1 报告 243,329 条对话/投票数据、50 个模型、90,051 用户、149 种语言，平均 1.3 轮，英语约 77%、中文约 5%。论文提出公开 100K+ 成对偏好数据集（第 2–4 页）。

LMSYS-Chat-1M 是更早的对话数据集，缺少直接用于排名的偏好标签；Arena Bench 则是从平台提示提炼出的固定自动评测集。

## 方法关系

- [[wiki/concept/成对比较|匿名成对比较]]提供反馈。
- [[wiki/concept/Bradley-Terry模型|BT 模型]]估计分数。
- [[wiki/concept/同时统计推断|同时区间]]描述名次不确定性。
- [[wiki/synthesis/主动分配评审预算与估计校正|主动采样与加权]]提高预算效率并校正模型对分配。
- [[wiki/concept/主题建模|主题分析]]与[[wiki/concept/异常投票检测|异常筛查]]检查数据结构和质量。

## 项目沿革

2024-09-20 的 LMSYS 公告宣布独立站 lmarena.ai；后续项目改名 Arena、使用 arena.ai。官方介绍记载 2025 年成立 Arena Intelligence Inc.，平台具有伯克利研究起源与后续公司化发展两层身份。链接：[独立站公告](https://www.lmsys.org/blog/2024-09-20-arena-new-site/)、[更名公告](https://arena.ai/blog/lmarena-is-now-arena)、[官方介绍](https://arena.ai/company/about)。来源页保留 2026-09-16 的核查记录。

## 关联条目（持续维护）

- [[wiki/entity/Arena-Bench|Arena Bench]]：Arena Bench 从平台提示中筛选构建。
