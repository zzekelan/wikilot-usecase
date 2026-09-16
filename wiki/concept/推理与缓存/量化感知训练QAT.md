# 量化感知训练（QAT）

## 定义
QAT（Quantization-Aware Training）在训练过程中模拟或引入[[wiki/concept/推理与缓存/数值量化|数值量化]]的影响，让参数适应低精度使用；区别于训练结束后才单独转换格式。依据：[[wiki/source/大模型报告/deepseek-v4-1-flash|报告]]第 14 页。

## 实例
DeepSeek 全局 main KV 在后训练引入 QAT，RoPE 与非 RoPE 部分使用相同量化格式，并在 RoPE 后量化以减少解码开销。局部 SWA KV 对误差更敏感，保留 FP8。

## 边界
QAT 是适应精度的方法，不是某一种 FP4 格式的名称，也不保证任意缓存位宽都不损失质量。块大小、scale、截断位置和任务验证必须与实际部署相符；具体布局见[[wiki/concept/推理与缓存/FP4缓存量化|FP4缓存量化]]。
