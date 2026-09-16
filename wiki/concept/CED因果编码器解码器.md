# CED 因果编码器–解码器

## 架构与动机

CED（Causal Encoder–Decoder）把因果 Transformer 的前半层视为 encoder，后半层视为 decoder。与经典双向编码器的序列到序列模型不同，这里的 encoder 也是因果的，整个模型仍自回归生成文本。目标是降低输入占比很高的智能体工作流中的[[wiki/concept/KV缓存与预填充解码|prefill 成本]]。来源：[[wiki/source/deepseek-v4-1-flash|报告]]第 7–9 页。

## 核心：decoder KV 从哪里来

常规逐层注意力从当前层状态 H_l 生成 KV。CED 对后半层的全局分支改为：

\[
C_l=H_{L/2}W_l^{KV},\qquad Z_l=H_{L/2}W_l^Z,\quad l>L/2.
\]

C 是 KV 条目，Z 是相应压缩权重。只要完整运行 encoder，就能由其最后状态投影出 decoder 所需的全局 KV，无需为大部分输入 token 执行完整 decoder。来源：报告第 9 页式 1。

## 为什么还要运行一小段 decoder

局部滑窗注意力（SWA）保留逐层 KV 生成，需要当前层隐藏状态。报告只对 prompt 最后 n_win 个 token 执行 decoder 有界重放，补足开始解码所需的局部状态。若 N≫n_win，计算规模从 O(NL) 变为 O(NL/2+n_win L/2)，长输入时近似减半（第 9、20 页）。

实际模型为 40 层、20+20，窗口 128；prefill 激活 8B 参数/token、decode 激活 16B。生成阶段的新 token 仍需通过整个网络。CED 节省的是大部分输入的后半层计算，并非将所有操作一律减半（第 7、22 页）。

CED 决定 KV 的**生成来源**；跨层 KV 共享决定**哪些层复用它**，两者可以叠加。

## 关联条目（持续维护）

- [[wiki/concept/CSA2压缩稀疏注意力|CSA2 压缩稀疏注意力]]：在 CED 的 KV 生成机制上叠加跨层共享。

- [[wiki/concept/SWA有界重放|SWA 有界重放]]：提供 decoder 局部 KV 的低成本恢复路径。
