# DeepSeek Harness

## 身份

DeepSeek Harness（DSH）是 DeepSeek 的智能体执行框架，为模型提供工具、任务循环和协作机制。它是[[wiki/concept/智能体框架|智能体框架（harness）]]，与语言模型本身分工不同。[项目地址](https://github.com/deepseek-ai/deepseek-harness)。来源：[[wiki/source/deepseek-v4-1-flash|报告]]第 34–36、39、48 页。

## 三种单智能体模式

| 模式 | 工具接口 | 报告中的配置 |
| --- | --- | --- |
| Minimal | 单一 bash 工具 | 代码 agent 的主要评测模式 |
| Standard | 直接函数工具 | full SDK profile，26 个初始工具，包含 web search/fetch |
| PTC | 通过程序组合工具 | TypeScript run_code，24 个底层工具 |

Standard/PTC 使用 v0.1.1+custom.202609011522。模式改变的是模型与外部环境的接口，工具数量不是能力分数（第 48 页）。

## Agent Team 模式

主 agent 可创建具名、持久 teammate：fresh 不带主线程历史，fork 带已完成轮次的一次性快照。所有 agent 共享仓库 checkout；持久 mailbox 支持消息与唤醒，共享任务板记录所有权、依赖和建议写入范围，并用 revision 检查更新。lead 负责最终检查、测试和回应（第 35–36 页）。

[[wiki/entity/DeepSeek-V4.1-Flash|V4.1-Flash]]在多种 DSH 模式和其他框架中训练、评测，目标是提高跨工具协议的适应性，而非只记住一种工具格式。

## 关联条目（持续维护）

- [[wiki/synthesis/多智能体协作的时间与计算成本|多智能体协作与关键路径]]：展开 Agent Team 的协调机制与关键路径。
