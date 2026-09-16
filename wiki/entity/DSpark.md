# DSpark

## 身份与结构
DSpark 全称 Confidence-scheduled Speculative Decoding with Semi-autoregressive Generation，是 DeepSeek 报告中的[[wiki/concept/推测解码|推测解码]]模块。三个 Transformer 块配合 128 token 滑窗，一次前向为五个草拟位置产生基础 logits。依据：[[wiki/source/deepseek-v4-1-flash|报告]]第 13–14 页。

轻量 Markov head 建模草拟位置间依赖；confidence head 预测条件接受概率并组合成前缀存活概率。调度器结合实测 engine 吞吐曲线，动态选择每请求验证长度，优化当前负载下 token 吞吐。

## 如何跟随主模型
主干预训练不使用 MTP；结束后冻结主干单训 DSpark。后训练时两者一起更新，但 DSpark 目标梯度不传回主干，使草拟器追踪变化的策略。它用于线上服务，也用于 RL/OPD rollout 加速（第 8、14 页）。

与 CED 的侧重点比较见[[wiki/synthesis/输入与输出阶段的推理加速|输入与输出阶段的推理加速]]。它是执行加速模块，不是新的后训练学习目标；[[wiki/concept/监督微调SFT|SFT]]、[[wiki/concept/强化学习RL|RL]]和[[wiki/concept/在策略蒸馏OPD|OPD]]的信号分工不因此改变。
