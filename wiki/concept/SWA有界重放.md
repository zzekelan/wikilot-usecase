# SWA 有界重放

## 局部缓存为什么难恢复

SWA（Sliding-Window Attention）每层只看最近 W 个位置，但层间依赖累积：L 层局部 KV 的精确恢复可能需要重放约 L×W 个 token。若只为一次缓存缺失就重算很长前缀，节省存储会变成计算负担。来源：[[wiki/source/deepseek-v4-1-flash|报告]]第 19–20 页。

有界重放（Bounded Replay）只处理最近 W 个 token，并将局部注意力截断到重放段内。重放始于 s 时，位置 i 的 SWA 范围为 [max(s,i−W+1),i]。以窗口 128 为例，重放长度控制在 128，而非层数乘 128。

## Encoder 与 decoder 两条路径

| 路径 | 何时使用 | 计算与复用 |
| --- | --- | --- |
| Encoder 重放 | 命中全局 KV、未命中局部 SWA | 重算前缀末尾 SWA，保留原全局 KV；新后缀生成两类 KV |
| Decoder 重放 | 每次 CED prefill | 最后一个窗口的 encoder 输出通过 decoder，生成本次解码使用的局部 KV |

两条路径分别解决持久缓存容量与[[wiki/concept/CED因果编码器解码器|CED]]的 decoder 局部状态需求。decoder SWA 不做前缀持久缓存（第 20 页）。

## 生命周期决定缓存策略

全局 KV 有长尾复用，报告保留至少 72 小时；encoder SWA 多在活跃会话内复用，使用每机约 10% host DRAM 组成的短 TTL 池，过期后用重放补齐。结合[[wiki/concept/CSA2压缩稀疏注意力|CSA2]]和低精度，全局 KV 约为前代 1/4，移除持久 SWA 后持久 KV 约为 1/8（第 19 页）。

这是以小段重算换容量的**近似状态恢复**。截断会让新后缀状态依赖缓存命中边界；报告通过实验和后训练中的重放适配控制影响，极端边界仍需压力测试（第 20、37 页）。
