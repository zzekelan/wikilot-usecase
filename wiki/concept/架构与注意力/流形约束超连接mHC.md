# 流形约束超连接（mHC）

## 定义与记号
mHC（Manifold-constrained Hyper-Connections）在相邻块间保留 n 条残差流。设 X_l∈R^(n×d)，A_l 将多流混合为块输入，B_l 混合残差，C_l 将块输出写回多流，则

X_(l+1)=B_lX_l+C_lF_l(A_lX_l)，(A_l,B_l,C_l)=H(X_l)。

依据：[[wiki/source/大模型报告/deepseek-v4-1-flash|报告]]第 12–13 页式 2–6。本页解释报告采用的多流框架，不据简式补全所有流形约束实现。

## 依赖与变体
系数从当前 X_l 预测时，计算输入混合可能等待跨隐藏维归约，造成重复读取。[[wiki/concept/架构与注意力/Single-Pass-mHC|Single-Pass-mHC]]改变的是这条依赖：当前输入使用上个块已经得到的系数，而不是把多残差流的基础框架全部替换。
