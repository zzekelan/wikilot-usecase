# 动量、AdamW 与权重衰减

## 定义与范围

本页解释梯度优化中的三个相关机制：动量（Momentum）积累历史梯度；Adam 结合梯度一阶矩与二阶矩估计调整更新；AdamW 将权重衰减（Weight Decay）从自适应梯度更新中解耦。这里的优化指训练参数更新，不包含报告中推理服务的性能优化。

动量的直觉是保留持续一致的更新方向，同时缓和来回震荡。Adam 的二阶矩用于调整不同参数的更新尺度。AdamW 则在梯度更新之外对参数施加收缩。出处：[[wiki/source/深度学习基础-2026暑期学校|课件]]第 68–71、84 页。

## 从动量到 Adam

动量的一种约定为 vₜ=βvₜ₋₁+gₜ，θₜ₊₁=θₜ−ηvₜ；另一种用 (1−β)gₜ 做指数平均，两者的尺度可由学习率对应调整。Nesterov 提前考虑沿历史方向移动后的位置，形成前瞻修正。来源：课件第 68 页。

Adam 以零初始化的一、二阶矩估计组合方向和尺度：

\[
m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,\qquad
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2,
\]
\[
\hat m_t=m_t/(1-\beta_1^t),\quad \hat v_t=v_t/(1-\beta_2^t),\qquad
\theta_{t+1}=\theta_t-\eta_t\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}.
\]

这里的平方、平方根和除法逐元素进行。AdaGrad 累计全部梯度平方，RMSProp 用指数平均减少历史累积导致的持续步长缩小，Adam 再加入一阶矩和偏差修正。来源：课件第 67–71 页。

例如 β₁=.9、β₂=.999、首步非零梯度 g，忽略 ε：不修正时 m₁/√v₁≈3.16·sign(g)，修正后为 sign(g)。课件第 70 页“分母小 1000 倍”混淆了 v 与 √v，分母实际相差约 31.6 倍。

## L2 与权重衰减的区别

若目标增加 λ‖θ‖²/2，在朴素 SGD 下有 θ←(1−ηλ)θ−ηg，因此与相同系数约定的权重衰减等价。Adam 会对包含 L2 项的梯度整体进行自适应处理，所以通常不等价于独立收缩参数。AdamW 明确将两者分开。出处：课件第 84 页。

这是[[wiki/concept/泛化与数据质量|泛化控制]]的一种手段；衰减越大并不必然越好，仍需验证集选择。

## DeepSeek 的实际配置

[[wiki/source/deepseek-v4-1-flash|报告]]第 15、22 页按参数类型分配优化方法：

| 参数类型 | 更新方法 |
| --- | --- |
| RMSNorm 权重等非矩阵参数 | AdamW |
| 主干线性变换等矩阵参数 | Muon；Query/Key 权重使用按头处理的 Muon |
| Engram 嵌入、token 嵌入与预测头 | 带动量的 Sinkhorn 平衡更新 |

报告对 Muon 使用 Nesterov 动量和解耦权重衰减；Sinkhorn 更新也使用 Nesterov 动量，但不施加权重衰减。因此不能把报告概括为“整个模型都使用 AdamW”。

矩阵结构如何影响更新见[[wiki/concept/Muon与Sinkhorn矩阵优化|Muon 与 Sinkhorn]]。报告的 AdamW 使用 β₁=.9、β₂=.95、ε=10⁻²⁰；RMSNorm 权重衰减 .1，bias 和 scaling 不衰减（第 15、22 页）。实际更新幅度还受[[wiki/concept/学习率与批量调度|学习率调度]]影响。跨来源解释见[[wiki/synthesis/深度学习基础与DeepSeek报告的共同概念|共同概念对照]]。

## 关联条目（持续维护）

- [[wiki/concept/Muon与Sinkhorn矩阵优化|Muon 与 Sinkhorn 矩阵优化]]：补充报告中矩阵参数的两类优化方法。
