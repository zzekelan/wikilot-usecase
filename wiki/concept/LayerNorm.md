# LayerNorm

## 定义
Layer Normalization（LN）对指定特征集合计算均值 μ 和方差 σ²，再输出 yᵢ=γᵢ(xᵢ−μ)/√(σ²+ε)+βᵢ。依据：[[wiki/source/深度学习基础-2026暑期学校|课件]]第 88–89 页。

## 与 BatchNorm 的区别
LN 不依赖同一批次其他样本，通常训练和推理使用同样的样本内统计方式。[[wiki/concept/BatchNorm|BatchNorm]]则通常跨批量等轴统计。要核对实现的 normalized shape，不能笼统说“整层的所有数”都共享统计。

这使 LN 适合变长序列等场景，但它同样只是控制统计尺度，不意味着激活服从正态分布，也不单独保证训练稳定。
