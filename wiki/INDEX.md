# Wiki 索引

原有三份资料已完成全文整理；补充的一手资料按专题阅读，范围见来源页。当前包含 **4 个来源、37 个概念、8 个实体、3 个综合条目**（不计兼容入口）。

## 阅读入口

- 先掌握全局：[[wiki/synthesis/从学习目标到智能体与人类偏好评测|从学习目标到智能体与人类偏好评测]]。
- 从基础进入模型：[[wiki/synthesis/深度学习基础与DeepSeek报告的共同概念|基础课件与 DeepSeek 的共同概念]]。
- 动手检验理解：[[wiki/synthesis/深度学习基础练习与推导|五组练习与推导]]。

## 来源笔记

- [[wiki/source/instructgpt|InstructGPT：用人类反馈训练指令遵循模型]] — SFT、奖励模型与 PPO 的方法分工；区分监督基线和 RL 初始化。

- [[wiki/source/深度学习基础-2026暑期学校|深度学习基础：2026 暑期学校]] — 96 页课件的五模块内容、公式、例子、教材章节与勘误。
- [[wiki/source/deepseek-v4-1-flash|DeepSeek-V4.1-Flash 技术报告]] — 51 页报告的架构、训练、系统、完整结果表与附录推导。
- [[wiki/source/chatbot-arena|Chatbot Arena 论文]] — 30 页论文的数据采集、排名统计、实验、派生基准与附录公式。

## 概念

### 学习目标、泛化与表示

- [[wiki/concept/经验风险与模型选择|经验风险与模型选择]] — 总体风险、最小二乘、岭回归和训练/验证/测试的分工。
- [[wiki/concept/泛化与数据质量|泛化与数据质量]] — 过拟合、多模态数据清洗与混合、任务合成和用户分布。
- [[wiki/concept/偏差方差与双下降|偏差、方差与双下降]] — 平方误差分解、随机标签记忆和插值阈值。
- [[wiki/concept/交叉熵-困惑度与BPB|交叉熵、困惑度与 BPB]] — 最大似然、分类梯度、语言建模指标与偏好拟合。
- [[wiki/concept/Softmax与温度采样|Softmax 与温度采样]] — logits 到概率、数值稳定性、温度与 top-p。
- [[wiki/concept/非线性表示与归一化|非线性表示与归一化]] — MLP、激活、通用近似与 BN/LN/RMSNorm。
- [[wiki/concept/反向传播与参数初始化|反向传播与参数初始化]] — 链式法则、梯度尺度及 Xavier/He 初始化。
- [[wiki/concept/正则化方法|正则化方法]] — L1/L2、权重衰减、早停、Dropout 与数据增强。
- [[wiki/concept/标签平滑与置信度校准|标签平滑与置信度校准]] — 软目标、过度自信及概率与经验正确率的关系。

### 优化与训练调度

- [[wiki/concept/损失曲面与SGD噪声|损失曲面与 SGD 噪声]] — 临界点、曲率、平坦性与小批量的隐式偏好。
- [[wiki/concept/动量-AdamW与权重衰减|动量、AdamW 与权重衰减]] — 一二阶矩、偏差修正、解耦衰减与混合优化配置。
- [[wiki/concept/学习率与批量调度|学习率与批量调度]] — 稳定步长、预热和衰减、批量噪声与长度扩展。
- [[wiki/concept/Muon与Sinkhorn矩阵优化|Muon 与 Sinkhorn 矩阵优化]] — 利用注意力头和矩阵行列结构预处理更新。

### 高效模型架构与推理系统

- [[wiki/concept/KV缓存与预填充解码|KV 缓存与预填充、解码]] — 区分 prefill/decode、全局/局部 KV 与持久缓存。
- [[wiki/concept/CED因果编码器解码器|CED 因果编码器–解码器]] — 从 encoder 状态生成 decoder 全局 KV，减少 prefill。
- [[wiki/concept/CSA2压缩稀疏注意力|CSA2 压缩稀疏注意力]] — Full、Reindex、Reuse 解耦 KV 共享与索引复用。
- [[wiki/concept/分层稀疏索引|分层稀疏索引]] — 从全局候选块到共享候选池，再做逐层 Top-K。
- [[wiki/concept/SWA有界重放|SWA 有界重放]] — 用固定窗口近似重算替代长期保存局部状态。
- [[wiki/concept/FP4缓存量化|FP4 缓存量化]] — 主 KV、索引器、局部缓存的精度选择与 QAT。
- [[wiki/concept/MoE与多模态负载均衡|MoE 与多模态负载均衡]] — 稀疏专家、激活参数与图文独立路由偏置。
- [[wiki/concept/Single-Pass-mHC|Single-Pass mHC]] — 改变混合系数依赖以实现单遍残差流融合。
- [[wiki/concept/推测解码与DSpark|推测解码与 DSpark]] — 多位置草拟、置信度预测和动态验证长度。
- [[wiki/concept/分布式训练与推理解耦|分布式训练与推理解耦]] — 视觉解耦、共享状态管理、通信重叠与 EPD。

### 后训练与智能体

- [[wiki/concept/SFT-RL与OPD|SFT、RL 与 OPD]] — 示范学习、奖励优化及学生轨迹上的多教师蒸馏。
- [[wiki/concept/智能体任务合成与验证|智能体任务合成与验证]] — 问题、环境、验证器的构建、质检与修复循环。
- [[wiki/concept/异步RL与离策略样本|异步 RL 与离策略样本]] — 长尾调度、长度偏差、陈旧 token 与恢复机制。
- [[wiki/concept/推理力度与测试时计算|推理力度与测试时计算]] — 条件化长度奖励、指数惩罚与质量–成本曲线。
- [[wiki/concept/智能体框架与评测协议|智能体框架与评测协议]] — 模型、工具、提示、上下文和预算的联合评测。
- [[wiki/concept/多智能体协作与关键路径|多智能体协作与关键路径]] — 任务分工、消息、派生延迟奖励与并行预算。

### 人类偏好、排名与评测

- [[wiki/concept/人类偏好与成对比较|人类偏好与成对比较]] — 匿名相对选择、专家一致性与用户分布。
- [[wiki/concept/Bradley-Terry模型与Elo|Bradley–Terry 模型与 Elo]] — 潜在分数、逻辑胜率、加权拟合与非参数推广。
- [[wiki/concept/置信区间与近似排名|置信区间与近似排名]] — bootstrap、sandwich、同时推断和名次范围。
- [[wiki/concept/主动采样与逆概率加权|主动采样与逆概率加权]] — 按不确定性分配评审预算并校正模型对抽样。
- [[wiki/concept/异常投票检测|异常投票检测]] — 秩 p 值、有限次数检查与混淆矩阵。
- [[wiki/concept/主题建模与LLM评审|主题建模与 LLM 评审]] — 提示聚类、问题区分力和自动裁判协议。
- [[wiki/concept/评测指标与可比性|评测指标与可比性]] — 概率建模、Pass@k、Mean@k、任务成绩和偏好分数。
- [[wiki/concept/评测污染与奖励投机|评测污染与奖励投机]] — 区分训练泄漏、选择过拟合与环境投机。

## 实体

### 模型、模块与系统

- [[wiki/entity/DeepSeek-V4.1-Flash|DeepSeek-V4.1-Flash]] — 多模态 MoE 模型总览及架构、训练和评测入口。
- [[wiki/entity/DeepSeek-ViT|DeepSeek-ViT]] — 视觉编码器、两阶段训练及语言主干接入。
- [[wiki/entity/Engram|Engram]] — ngram 哈希查表、上下文门控与条件记忆预取。
- [[wiki/entity/DSec|DSec]] — 大规模智能体训练与评测的弹性沙箱平台。
- [[wiki/entity/DeepSeek-Harness|DeepSeek Harness]] — Minimal、Standard、PTC 与 Agent Team 模式。

### 评测平台与基准

- [[wiki/entity/Chatbot-Arena|Chatbot Arena]] — 众包匿名成对评测平台、数据和项目沿革。
- [[wiki/entity/Arena-Bench|Arena Bench]] — 从 Arena 提示筛出的 350 题固定自动评测集。

### 人物

- [[wiki/entity/魏鸿鑫|魏鸿鑫]] — 暑期学校讲者，研究可靠学习、自动化评估与搜索智能体。

## 跨来源对照

- [[wiki/synthesis/从学习目标到智能体与人类偏好评测|从学习目标到智能体与人类偏好评测]] — 串联三份资料的目标、数据、系统和评测，并提出研究问题。
- [[wiki/synthesis/深度学习基础与DeepSeek报告的共同概念|深度学习基础与 DeepSeek 报告的共同概念]] — 从概率目标和优化基础进入稀疏架构、后训练与推理。
- [[wiki/synthesis/深度学习基础练习与推导|深度学习基础：练习与推导]] — 五组课堂练习的解题思路、公式核算和实验设计。

## 原始资料

- [[raw/深度学习基础/深度学习基础_2026暑期学校.pdf|深度学习基础课件 PDF]] — 96 页，已完成全文整理。
- [[raw/大模型技术报告/DeepSeek-V4.1-Flash/DeepSeek_V41_Tech_Report.pdf|DeepSeek 技术报告 PDF]] — 51 页，已完成正文与附录整理。
- [[raw/大模型技术报告/DeepSeek-V4.1-Flash/img_v3_0215e_1d574a93-1181-47ad-af6e-e46320b7f04g.png|DeepSeek 后训练截图]] — 对应报告第 6 页，概述 SFT、RL、OPD 和数据管线。
- [[raw/大模型评测/Chatbot-Arena/Chatbot_Arena_ICML_2024.pdf|Chatbot Arena 论文 PDF]] — 30 页，已完成正文、附录与示例整理。

## 维护

- [[AGENTS.md|整理与维护约定]] — 写作风格、条目分工、引用关系与逐条提交流程。
- [[wiki/LOG|变更日志]] — 资料整理、条目更新和维护检查记录。
