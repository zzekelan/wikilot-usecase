# Arena Bench

## 与 Chatbot Arena 的区别

Arena Bench 是 ICML 2024 [[wiki/source/chatbot-arena|Arena 论文]]中从众包提示筛出的 **350 个固定问题**组成的派生基准。[[wiki/entity/Chatbot-Arena|Chatbot Arena]]实时收集真人票；Arena Bench 使用 GPT-4-Turbo 评审，是静态问题与自动偏好评价的组合（第 6–7、26–27 页）。

## 评测流程

1. 按主题覆盖筛选复杂问题，如 Flutter 跨平台习惯追踪应用、太阳能 Raspberry Pi 系统设计。
2. 将 GPT-4-Turbo、GPT-4-0314、Claude-1 的回答交给 GPT-4-Turbo，生成参考答案。
3. 将待测回答与统一基线 GPT-3.5-Turbo-0301 比较。
4. 每题交换 A/B 位置评两次，每模型共 700 次比较。
5. 胜/平/负记 10/5/0；显著胜负按三次胜负加权，其余权重 1，取加权平均。

因此最终分数不仅取决于胜负比例，还取决于“显著胜负”的出现频率。来源：论文附录 D.2–D.3，第 26–27 页。

## 评价什么

rubric 要求先识别事实错误，再比较有用性、相关性、简洁性，必要时考虑创造性与遗漏信息。图 4 用这一派生基准与 MT-Bench 对照，展示所选问题上的区分力（第 7、27 页）。

参考答案、裁判和筛题过程共同影响分数。理解结果时，应连同[[wiki/concept/主题建模与LLM评审|LLM 评审协议]]一起阅读，而非把 0–10 分等同真人平台的 BT 分数。
