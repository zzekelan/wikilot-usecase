# CSA2 压缩稀疏注意力

## 方法概览

CSA2（Compressed Sparse Attention 2）同时利用序列压缩、跨层 KV 共享和稀疏索引复用。每个 query 读取选出的全局 main KV，并结合当前层局部 SWA KV 计算注意力。来源：[[wiki/source/deepseek-v4-1-flash|报告]]第 9–12 页、图 4。

| 模式 | main KV / indexer K | Top-K 位置 | 当前层保留的计算 |
| --- | --- | --- | --- |
| Full | 当前层生成 | 当前层选取 | main Q、indexer Q、SWA KV、注意力 |
| Reindex | 复用前面 Full 层 | 用自己的 indexer Q 重新选 | main Q、重新打分、SWA KV、注意力 |
| Reuse | 复用前面 Full 层 | 复用最近 Full/Reindex 的选择 | main Q、SWA KV、注意力 |

**KV 共享节省存储，索引共享节省选取计算。** Reindex 在两者之间折中：保持相同缓存，但允许不同层关注不同位置。Reuse 也会产生新的注意力输出，并非跳过该层（第 10–11 页）。

## 相比 CSA 的简化

压缩比 m 表示把一组 m 个原位置压成条目；CSA2 去掉原 CSA 的相邻压缩窗口重叠和压缩时的绝对位置嵌入。indexer K 直接由 main KV 投影，不再从隐藏状态单走一条压缩路径。m=1 时不压缩序列，但仍可做跨层共享和稀疏选择（第 10 页）。

## 在 V4.1-Flash 中的布局

前两层只有 SWA。encoder 其余 18 层按三组 Full+5 Reuse 排列，m=2；decoder 20 层为五组四层，第一组 Full+3 Reuse，其余 Reindex+3 Reuse，m=1。每个 query 选 Top-512，SWA 窗口 128（第 22 页）。

结合[[wiki/concept/CED因果编码器解码器|CED]]时，decoder 的 Full 层从最终 encoder 状态投影全局 KV。共享减少重复保存，层间重选保留部分表达灵活性；稀疏选择的主要风险是漏掉任务所需位置（第 11、37 页）。

## 关联条目（持续维护）

- [[wiki/concept/分层稀疏索引|分层稀疏索引]]：减少 Reindex 层的全上下文扫描。

- [[wiki/concept/跨层共享状态管理|跨层共享状态管理]]：说明跨流水线阶段的共享实现。
