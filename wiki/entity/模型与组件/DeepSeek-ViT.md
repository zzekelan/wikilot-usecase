# DeepSeek-ViT

## 身份与结构

DeepSeek-ViT 是 V4.1-Flash 使用的视觉编码器，将图像转换为语言主干能处理的视觉表示。它在 Vision Transformer 基础上采用 2D-RoPE、线性 patch 投影、RMSNorm 和 SwiGLU，支持变分辨率输入。来源：[[wiki/source/大模型报告/deepseek-v4-1-flash|报告]]第 8、22 页。

配置为 32 层、隐藏维 1024、16 个注意力头、patch size=14。空间特征经 **3×3 pixel-unshuffle** 将每个邻域移入通道维，token 数减少为 1/9，再经两层、隐藏维 5120 的 MLP 投影器接入语言主干。pixel-unshuffle 是重排而非简单丢弃九分之八的输入值。

## 两阶段视觉训练

| 阶段 | 数据与目标 | 分辨率与目的 |
| --- | --- | --- |
| 对比预训练 | 约 47B 图文对，SigLIP sigmoid 对比损失 | 最高约 224×224，学习大规模图文关联 |
| 自回归微调 | 连接临时 4B MoE，236B token，下一 token 预测 | 约 544²–1344²，强化 OCR、图表等细粒度能力 |

微调结束后丢弃临时语言模型，只保留视觉编码器。接入主干预训练后先冻结编码器，最终归一化与投影器可训练；学习率衰减阶段解冻视觉编码器，并用较小步长联合优化。来源：报告第 15、22–23 页。

## 与其他组件的联系

[[wiki/synthesis/学习与表示/非线性表示与归一化组件对照|MLP、SwiGLU 与 RMSNorm]]构成视觉到语言的表示桥梁；[[wiki/concept/优化与调度/Muon|Muon]]影响线性 patch 投影的设计；图像与文本进入同一主干后由[[wiki/concept/架构与注意力/多模态专家负载均衡|分模态 MoE 负载均衡]]协调专家使用。

## 关联条目（持续维护）

- [[wiki/entity/模型与组件/DeepSeek-V4.1-Flash|DeepSeek-V4.1-Flash]]：V4.1-Flash 使用该视觉编码器接收图像。

- [[wiki/concept/分布式系统/多模态训练解耦|多模态训练解耦]]：视觉编码器以独立阶段参与多模态训练。
