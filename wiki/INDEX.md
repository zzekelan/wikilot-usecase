# Wiki 索引

## 来源笔记

- [[wiki/source/chatbot-arena|Chatbot Arena：基于人类偏好的大模型评测平台]] — 数据采集、BT 排名、主动采样、专家复标、异常检测与附录公式。

- [[wiki/source/深度学习基础-2026暑期学校|深度学习基础：2026 暑期学校]] — 五模块的概念、公式、例子、工程细节、教材章节与勘误。
- [[wiki/source/deepseek-v4-1-flash|DeepSeek-V4.1-Flash 技术报告]] — 架构、预训练、后训练、服务系统、完整结果表和附录推导。

## 概念

- [[wiki/concept/交叉熵-困惑度与BPB|交叉熵、困惑度与 BPB]] — 统一解释最大似然、交叉熵梯度、PPL、BPB 以及 Arena 的偏好概率建模。
- [[wiki/concept/泛化与数据质量|泛化与数据质量]] — 过拟合、数据覆盖与去重、训练/验证/测试的分工。
- [[wiki/concept/动量-AdamW与权重衰减|动量、AdamW 与权重衰减]] — 参数更新机制、L2 与衰减的区别，以及报告的混合优化方案。
- [[wiki/concept/学习率与批量调度|学习率与批量调度]] — 步长、预热、余弦衰减及报告的实际训练日程。
- [[wiki/concept/非线性表示与归一化|非线性表示与归一化]] — MLP、激活函数以及 BN/LN/RMSNorm 的作用与区别。
- [[wiki/concept/Softmax与温度采样|Softmax 与温度采样]] — logits 到概率、温度示例及其与 top-p 的区别。
- [[wiki/concept/经验风险与模型选择|经验风险与模型选择]] — 从总体风险、最小二乘到岭回归，解释验证集选择与测试集评估。
- [[wiki/concept/偏差方差与双下降|偏差、方差与双下降]] — 解释平方误差分解、随机标签记忆及插值阈值附近的双下降。
- [[wiki/concept/反向传播与参数初始化|反向传播与参数初始化]] — 链式法则、梯度消失与爆炸，以及 Xavier、He 初始化的尺度推导。
- [[wiki/concept/正则化方法|正则化方法]] — 按作用位置比较 L1/L2、早停、Dropout 和数据增强。
- [[wiki/concept/标签平滑与置信度校准|标签平滑与置信度校准]] — 解释软目标、过度自信，以及预测概率与实际正确率的对应关系。
- [[wiki/concept/Muon与Sinkhorn矩阵优化|Muon 与 Sinkhorn 矩阵优化]] — 解释按矩阵结构预处理更新、按头 Muon 和嵌入表的行列平衡。
- [[wiki/concept/KV缓存与预填充解码|KV 缓存与预填充、解码]] — 解释 prefill、decode、全局/局部 KV 与持久前缀缓存的成本。
- [[wiki/concept/CED因果编码器解码器|CED 因果编码器–解码器]] — 通过 encoder 输出生成 decoder 全局 KV，减少长输入预填充计算。
- [[wiki/concept/CSA2压缩稀疏注意力|CSA2 压缩稀疏注意力]] — 用 Full、Reindex、Reuse 三种模式解耦 KV 共享和稀疏索引复用。
- [[wiki/concept/分层稀疏索引|分层稀疏索引]] — 先全局选择候选块，再在共享候选池中进行各层 Top-K 重选。
- [[wiki/concept/SWA有界重放|SWA 有界重放]] — 以最近一个窗口的近似重算替代长期保存局部 KV，并支持 CED 预填充。
- [[wiki/concept/FP4缓存量化|FP4 缓存量化]] — 区分主 KV、索引器与局部缓存的精度选择，以及 QAT 的作用。
- [[wiki/concept/MoE与多模态负载均衡|MoE 与多模态负载均衡]] — 解释共享/路由专家、总参数与激活参数，以及分模态路由偏置。
- [[wiki/concept/Single-Pass-mHC|Single-Pass mHC]] — 通过错位使用混合系数消除依赖，使多残差流处理可融合为单遍。
- [[wiki/concept/推测解码与DSpark|推测解码与 DSpark]] — 草拟多个 token，再由主模型验证；DSpark 用置信度和负载选择验证长度。
- [[wiki/concept/分布式训练与推理解耦|分布式训练与推理解耦]] — 把视觉、语言、共享状态与推理阶段分开调度，并通过重叠和融合减少开销。
- [[wiki/concept/SFT-RL与OPD|SFT、RL 与 OPD]] — 比较示范学习、奖励优化与在策略蒸馏，解释后训练各阶段的分工。
- [[wiki/concept/智能体任务合成与验证|智能体任务合成与验证]] — 将问题、环境、验证器共同构造成可训练任务，并持续审计难度与正确性。
- [[wiki/concept/异步RL与离策略样本|异步 RL 与离策略样本]] — 解释 rollout 长尾、样本级调度、长度偏差与策略陈旧性的处理。
- [[wiki/concept/推理力度与测试时计算|推理力度与测试时计算]] — 用条件化长度奖励学习成本–质量控制，并解释指数惩罚的局部推导。
- [[wiki/concept/智能体框架与评测协议|智能体框架与评测协议]] — 把模型、工具、提示、上下文管理和预算视为联合评测对象。
- [[wiki/concept/多智能体协作与关键路径|多智能体协作与关键路径]] — 解释共享任务、消息协调、派生延迟奖励和多智能体计算预算。
- [[wiki/concept/人类偏好与成对比较|人类偏好与成对比较]] — 用匿名相对选择评价开放式回答，并区分偏好、正确性和评审一致性。
- [[wiki/concept/Bradley-Terry模型与Elo|Bradley–Terry 模型与 Elo]] — 由成对胜负拟合潜在分数，解释逻辑胜率、平移不识别与 Elo 的关系。

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

- [[AGENTS.md|整理与维护约定]] — 写作风格、条目分工、引用关系与逐条提交流程。
- [[wiki/LOG|变更日志]] — 记录资料入库、阅读笔记和维护变更。

## 实体

- [[wiki/entity/Engram|Engram]] — DeepSeek 的条件记忆模块：ngram 哈希查表、上下文门控与确定性预取。
- [[wiki/entity/DeepSeek-ViT|DeepSeek-ViT]] — 视觉编码器的结构、图文对比预训练、自回归微调及语言主干接入。
- [[wiki/entity/DeepSeek-V4.1-Flash|DeepSeek-V4.1-Flash]] — 多模态 MoE 模型的身份、核心规格、组件关系和能力轮廓。
- [[wiki/entity/DSec|DSec]] — DeepSeek Elastic Compute：支持大规模智能体训练与评测的沙箱平台。
- [[wiki/entity/DeepSeek-Harness|DeepSeek Harness]] — DeepSeek 智能体框架的 Minimal、Standard、PTC 与 Agent Team 模式。
