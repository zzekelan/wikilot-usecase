# Single-Pass mHC

## 从单残差流到多残差流

mHC（Manifold-constrained Hyper-Connections）在相邻 Transformer 块之间保留 n 条残差流。设 X_l∈R^(n×d)，A_l 将多流混合为块输入，B_l 混合残差，C_l 将块输出写回多流：

\[
X_{l+1}=B_lX_l+C_lF_l(A_lX_l),\qquad (A_l,B_l,C_l)=H(X_l).
\]

来源：[[wiki/source/deepseek-v4-1-flash|报告]]第 12–13 页，式 2–6。

## 依赖为什么妨碍融合

先生成 X_l，再从它归一化、投影出 A_l，最后再读取 X_l 做输入混合；A_l 要等跨隐藏维归约完成，迫使再次遍历激活。加入 pre-norm 后，原实现的激活读写量为 (4n+4)d。

Single-Pass 把块输入改为 **A_(l−1)X_l**，使用前一块已经产生的混合系数。这样每个 X_l tile 可以同时用于当前输入混合和下一块系数预测，消除等待 A_l 的依赖。

## 效率来自数据流改变

部署内核 Mega-mHC 融合残差更新、输入混合、系数预测、pre-norm 和 FP8 转换，达到 (2n+2)d 激活读写量，约为原实现一半。报告 n=4，对应从 20d 到 10d。预训练仍可用多内核实现，结构改变与部署融合是两层工作（第 13、22 页）。

这里的收益主要是内存流量，不等于 Transformer 整层 FLOPs 减半。它与[[wiki/concept/CSA2压缩稀疏注意力|CSA2]]互补：前者优化残差数据流，后者优化注意力缓存和索引。
