# 滑动窗口注意力（SWA）

## 定义
Sliding-Window Attention（SWA）对位置 i 只读取最近 W 个因果位置，例如 [max(0,i−W+1),i]。局部缓存因而随窗口宽度而非全部历史长度增长。依据：[[wiki/source/deepseek-v4-1-flash|报告]]第 9–12、19–20 页。

## 多层依赖
单层只看 W 个位置，不意味着 L 层状态只依赖同样 W 个原始 token；层间依赖会扩展感受范围。精确恢复局部 KV 可能需要重放约 L×W 的输入范围。

[[wiki/concept/SWA有界重放|SWA有界重放]]只恢复有限尾段，是近似方案；[[wiki/concept/CSA2压缩稀疏注意力|CSA2]]把局部窗口与稀疏全局读取结合，避免将 SWA 当成完整长距离检索能力。报告实际窗口为 128（第 22 页）。
