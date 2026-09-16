# FP4 缓存量化

## 定义与范围

本页讨论 DeepSeek 对 KV 与索引缓存使用低精度格式的具体方案，重点是 FP4 布局、scale 开销和量化位置。一般的[[wiki/concept/数值量化|数值量化]]原理与[[wiki/concept/量化感知训练QAT|QAT]]训练方法分别维护，不将部署格式等同于训练算法。来源：[[wiki/source/deepseek-v4-1-flash|报告]]第 14 页。

## 三种缓存分别处理

| 对象 | 报告精度/格式 | 目的 |
| --- | --- | --- |
| indexer Q/K | OCP MXFP4 | 加速索引计算并减小 indexer cache |
| 全局 main KV | E2M1，每 16 通道一个 E4M3 scale | 主要节省缓存，注意力前解量化 |
| 局部 SWA KV | FP8 | 对量化较敏感，保留更高精度 |

主 KV 方案类似 NVFP4，但省略二级 global scale；它不要求硬件原生支持该格式的矩阵乘，因为缓存读取后先解量化。包括 scale 元数据后，每 16 值约为 16×4+8=72 bit，即约 **4.5 bit/值**，这是存储布局的简单核算（第 14 页）。

## 为什么能省略全局 scale

报告的 512 维 latent 经 [[wiki/concept/RMSNorm|RMSNorm]] 后，在最大归一化权重约 1 的条件下，L2 范数约不超过 √512≈22.6；RoPE 保持范数，而该格式量级范围可到 448×6=2688。实际训练观测最大绝对值约 10，动态范围已有余量（第 14 页）。

主 KV 在后训练引入[[wiki/concept/量化感知训练QAT|量化感知训练]]，RoPE 与非 RoPE 部分采用同格式，并在 RoPE 后量化以降低解码开销。它与[[wiki/concept/CSA2压缩稀疏注意力|跨层共享]]从不同方向压缩[[wiki/concept/KV缓存|KV]]：一个减少每值字节，一个减少重复条目。
