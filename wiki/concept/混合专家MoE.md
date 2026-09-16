# 混合专家（MoE）

## 定义
Mixture-of-Experts 用多个专家替代单一前馈网络，由路由器为每个 token 选择少量专家；共享专家处理通用模式，路由专家提供条件容量。总参数与每 token 激活参数因此可以相差很大。依据：[[wiki/source/deepseek-v4-1-flash|报告]]第 7–8、22 页。

## 实例
V4.1-Flash 每层有 1 个共享专家与 384 个路由专家，每 token 选择 6 个路由专家；中间维 2304，使用[[wiki/concept/SwiGLU|SwiGLU]]及阈值 10 的 clamping（第 22 页）。

## 容量与负载
稀疏激活不自动保证设备均衡；若路由集中，部分设备过忙且其他专家训练不足。模型还结合[[wiki/concept/CED因果编码器解码器|CED]]，prefill/decode 的 8B/16B 激活差异不只由路由专家数决定。
