# PPO：近端策略优化原始论文

## 来源与阅读范围

- 原题：Proximal Policy Optimization Algorithms。
- 作者：John Schulman、Filip Wolski、Prafulla Dhariwal、Alec Radford、Oleg Klimov，OpenAI。
- 版本：arXiv:1707.06347v2，2017-08-28；下载日期：2026-09-16。
- 一手入口：[作者论文](https://arxiv.org/abs/1707.06347v2)；[[raw/强化学习/PPO/1707.06347.pdf|原文 PDF]]，12 页。
- 本次专题阅读：第 1–5 页，§1–5 和 §6.1 开头；聚焦策略梯度与 PPO 方法，后续实验和附录未整理。

## 问题与基本思路

策略梯度交替执行环境采样和参数更新。直接对同一批轨迹反复优化普通策略梯度目标，可能让策略变化过大。PPO 使用便于一阶优化的替代目标，在采样成本与更新稳定性之间折中（§1–2，第 1–2 页）。

论文 §2.1 式 1 的梯度估计为：

\[
\hat g=\hat{\mathbb E}_t[\nabla_\theta\log\pi_\theta(a_t\mid s_t)\hat A_t].
\]

其中策略 π 给出行动概率，优势估计 Â 衡量该行动相对基准的好坏。它不是要求给出每一步的标准答案。

## 裁剪目标

令概率比率 \(\rho_t=\pi_\theta(a_t|s_t)/\pi_{\rm old}(a_t|s_t)\)，PPO-Clip 最大化：

\[
L^{\rm clip}=\hat{\mathbb E}_t[\min(\rho_t\hat A_t,\operatorname{clip}(\rho_t,1-\epsilon,1+\epsilon)\hat A_t)].
\]

这在有利方向上移除过度改变比率的激励；它不是对参数或全部概率比率施加硬约束，也不是裁剪梯度（§3，式 7，第 3 页）。论文另给出自适应 KL 惩罚版本（§4，第 4 页）。

## 训练循环与适用边界

算法 1：旧策略并行采样 → 估计优势 → 多轮小批量更新 → 将更新后的策略用于下一轮采样。Actor-Critic 实现还包括价值函数误差和可选熵奖励（§5，第 4–5 页）。

原论文场景是连续控制与 Atari，不是语言模型。[[wiki/source/后训练与强化学习/instructgpt|InstructGPT]] 将 PPO 用于语言模型回答策略；其相对 SFT 参考策略的 KL 惩罚，和 PPO 相对一轮旧策略的更新控制不是同一件事。PPO 是[[wiki/concept/后训练与智能体/强化学习RL|强化学习]]算法之一，不能用 PPO 定义整个 RL。
