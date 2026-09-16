# SwiGLU

## 定义与结构
常见 SwiGLU 前馈结构可写为 [SiLU(xW_g)⊙(xW_v)]W_o。两个输入投影分别提供门控和特征，相乘后再输出投影；它使用[[wiki/concept/SiLU|SiLU]]，但不是 SiLU 本身。该式是对结构的补充解释。

## 报告实例
[[wiki/source/deepseek-v4-1-flash|报告]]第 22 页的 MoE 专家使用 SwiGLU，中间维 2304，并采用阈值为 10 的 clamping。clamping 是该实现控制幅度的配置，不是所有 SwiGLU 必须具备的定义部分。

门控改变特征如何组合，专家路由决定选哪些子网络；两者都可出现在 MoE，却处理不同问题。
