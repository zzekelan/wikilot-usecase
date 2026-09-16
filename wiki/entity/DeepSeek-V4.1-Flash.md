# DeepSeek-V4.1-Flash

## 模型概览

DeepSeek-AI 的多模态 MoE 模型，接收图像和文本，自回归输出文本，支持最高百万 token 上下文。训练与评测细节见[[wiki/source/deepseek-v4-1-flash|技术报告]]第 1、7、21–24、33 页。

| 规格 | 配置 |
| --- | --- |
| 主干 | 40 层，隐藏维 5120，552B 参数 |
| 条件记忆 | 另有 196B [[wiki/entity/Engram|Engram]] 参数 |
| 每 token 激活量 | prefill 8B，decode 16B |
| 视觉输入 | [[wiki/entity/DeepSeek-ViT|DeepSeek-ViT]] + 两层 MLP 投影 |
| 预训练 | 45T token，文本:多模态 token=7:1 |
| 全局 KV | 890 字节/token |

“Flash”是模型名称，不表示其总参数只有 8B/16B；这两个数字描述计算时的激活量。

## 关键组件如何协同

- [[wiki/concept/CED因果编码器解码器|CED]]减少长输入的 decoder prefill。
- [[wiki/concept/CSA2压缩稀疏注意力|CSA2]]共享 KV/索引，[[wiki/concept/分层稀疏索引|分层索引]]减少后续全范围打分。
- [[wiki/concept/FP4缓存量化|FP4]]压缩每条缓存；[[wiki/concept/SWA有界重放|SWA 有界重放]]减少持久局部缓存。
- [[wiki/concept/混合专家MoE|MoE]]与 Engram 分别提供稀疏计算容量和查表记忆。
- [[wiki/concept/Single-Pass-mHC|Single-Pass mHC]]优化残差流搬运，[[wiki/entity/DSpark|DSpark]]加速输出生成。

## 基础模型与后训练模型

Base 用于概率预测和 few-shot 能力评估；后训练模型通过 SFT、RL、OPD 强化推理、工具使用与多模态智能体行为。来源页保留全部结果表。

能力例子：Base 的 HumanEval=79.4、LongBench-V2=45.2；后训练 Max 的 GPQA Diamond=90.9、DeepSWE v1.1=74.2、Terminal-Bench 2.1=90.6。它们对应不同模型阶段、任务和评测设置，应按各自协议比较（第 24、32–35 页）。

报告的重点是常用任务能力与成本的组合；较难科学任务、多模态边界、长上下文稀疏检索与近似状态恢复仍是进一步优化方向（第 37 页）。

相关资源：[模型仓库](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)。

## 关联条目（持续维护）

- [[wiki/synthesis/SFT-RL与OPD的分工|SFT、RL 与 OPD 的分工]]：说明基础模型到推理/智能体模型的训练阶段。
