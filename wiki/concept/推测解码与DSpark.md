# 推测解码与 DSpark

## 基本思路

推测解码（Speculative Decoding）先由轻量草拟器提出多个候选 token，再交给主模型批量验证，减少逐 token 运行昂贵模型的次数。系统收益取决于草拟成本、候选被接受的长度及批量执行效率；具体输出分布由验证规则决定。

[[wiki/source/deepseek-v4-1-flash|报告]]第 13–14 页采用 DSpark（Confidence-scheduled Speculative Decoding with Semi-autoregressive Generation），将半自回归草拟与置信度调度结合。

## DSpark 怎样工作

1. 三个 Transformer 块、128 token 滑窗，一次前向并行生成五个草拟位置的基础 logits。
2. 轻量 Markov head 建模草拟 token 之间的依赖。
3. confidence head 预测逐位置条件接受概率，组合成前缀存活概率。
4. 调度器结合这些概率和实测 engine 吞吐曲线，为每请求动态选择验证长度，优化当前负载下的系统 token 吞吐。

草拟越长不一定越快：低接受率会浪费计算，高并发下最优长度也可能变化（第 14 页）。

## 怎样跟随主模型训练

主干预训练期间不使用 MTP；结束后冻结主干，单独训练 DSpark。后训练中两者一起更新，但 DSpark 目标梯度不传回主干，从而追踪不断变化的策略。它同时用于线上服务，以及 RL/OPD 的 rollout 加速（第 8、14 页）。

与[[wiki/concept/CED因果编码器解码器|CED]]侧重点不同：CED 主要减少输入 prefill，DSpark 主要减少输出解码的串行开销；[[wiki/concept/KV缓存与预填充解码|KV 缓存]]则支持两阶段的状态复用。
