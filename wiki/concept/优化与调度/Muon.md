# Muon

## 机制
Muon 对[[wiki/concept/优化与调度/动量|动量]]形成的矩阵更新做近似正交化，再按约定缩放。[[wiki/source/大模型报告/deepseek-v4-1-flash|报告]]第 14–15 页以 Newton–Schulz 正交化与 Sinkhorn 平衡比较；这里预处理的是更新，不是要求参数矩阵本身始终正交。

## 按头处理
Q/K 权重采用 head-wise Muon：先按注意力头分块，各块独立预处理，而非对整个权重矩阵施加一个变换。头结构因此影响更新几何。

## 具体配置
报告用于主干线性矩阵、Engram 投影及视觉语言投影器；Nesterov momentum=.95，解耦 weight decay=.1，更新 RMS 调至 .18，以复用学习率尺度（第 15、22 页）。这些是该报告配置，不是 Muon 唯一合法参数；非矩阵仍可用[[wiki/concept/优化与调度/AdamW|AdamW]]。
