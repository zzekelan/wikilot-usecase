# 交叉熵、PPL 与 BPB 的换算

## 一个概率代价，三种表达

三个概念各自维护定义：[[wiki/concept/概率与采样/交叉熵|交叉熵]]、[[wiki/concept/概率与采样/困惑度PPL|困惑度（PPL）]]、[[wiki/concept/概率与采样/每字节比特数BPB|每字节比特数（BPB）]]。本页只说明换算条件及不同来源中的用途。

对同一段计分文本，计分 token 数为 T、对应字节数为 B，累计负对数概率为 N（自然对数），则：

| 指标 | 计算 | 单位/尺度 |
| --- | --- | --- |
| 平均 token 交叉熵 L | N/T | nat/token |
| PPL | exp(N/T) | 平均概率代价的指数尺度 |
| BPB | N/(B ln 2) | bit/byte |

由定义可得：

\[
\mathrm{BPB}=\frac{T}{B\ln2}L=\frac TB\log_2\mathrm{PPL}.
\]

公式是 wiki 的定义换算，不是 DeepSeek 报告给出的额外实验结果。只有文本、概率计分规则和分子一致时才可这样换算；不同 tokenizer 下不能只凭 PPL 数值对比。

例如 T=100、B=400、L=ln 2，则 PPL=2、BPB=0.25。单个正确 token 的概率为 0.5，只能确定其负对数代价为 1 bit，不能推断整段文本的 BPB。

## 三份原始资料分别在衡量什么

- [[wiki/source/深度学习基础/深度学习基础-2026暑期学校|基础课件]]第 31–38 页讲分类交叉熵、最大似然及输出层梯度，预测对象是标签。
- [[wiki/source/大模型报告/deepseek-v4-1-flash|DeepSeek 报告]]第 24–25 页评估文本概率，图 6 用 BPB 比较内部文档、代码和学术资料的预测代价；确切数据在 BPB 概念页与来源页。
- [[wiki/source/模型评测/chatbot-arena|Arena 论文]]第 4–5 页用加权二元交叉熵拟合偏好胜率。标签是人类比较结果，不是文本 token，不能把拟合值当成语言模型的 PPL。

共同数学形式有助于理解，却不能代替[[wiki/concept/评测方法/评测协议|评测对象与条件的对齐]]。
