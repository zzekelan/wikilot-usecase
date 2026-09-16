# SearcherKit：搜索智能体框架调研

## 来源与核验范围

- 项目：SearcherKit，Python 包名 `searcherkit`，命令行入口 `searcher`。
- 团队：README 称由南方科技大学与香港中文大学（深圳）的[[wiki/entity/人物/魏鸿鑫|魏鸿鑫]]、荆炳义研究团队维护。
- 固定版本：[PyPI 0.1.1](https://pypi.org/project/searcherkit/0.1.1/)，源码包上传于 2026-07-20；Python ≥3.12，MIT 许可证。版本与许可由源码包 `pyproject.toml` 核对。
- 本地来源：[[raw/搜索智能体/SearcherKit/searcherkit-0.1.1.tar.gz|0.1.1 源码包]]与[[raw/搜索智能体/SearcherKit/pypi-0.1.1.json|PyPI 元数据快照]]，2026-09-16 下载；已核验源码包 SHA-256 与 PyPI 元数据一致。
- 文档：[入门](https://searcherkit.readthedocs.io/en/latest/docs/guide/index.html)、[架构](https://searcherkit.readthedocs.io/en/latest/docs/guide/customizing/project-architecture.html)、[训练](https://searcherkit.readthedocs.io/en/latest/docs/guide/training/training-overview.html)，读取于同日。`latest` 文档未固定构建提交，不能与 0.1.1 功能逐项视为完全相同。
- 阅读范围：README、包配置、SearchAgent 配置与循环说明、FileSource 全文、WebSource 初始化、Runner 的并发和检查点关键位置及训练适配器结构；不是全仓库审计。未安装运行、未调用模型、未做训练或性能实测。

## 定位：不是搜索引擎，也不是一个模型

**SearcherKit 是把大模型、搜索工具、数据源、运行记录和训练接口组织起来的搜索智能体运行框架。** 模型决定何时查资料、调用什么工具，再根据结果继续搜索或回答。它依赖外部模型与检索服务，不自行提供通用搜索索引，也不等于预训练好的搜索模型。（README；架构文档）

它是[[wiki/concept/后训练与智能体/智能体框架|智能体框架]]的一个具体实例。主要价值不在“多了一个搜索按钮”，而在于复用同一套智能体配置进行交互试用、批量采样、评测与后训练。

## 核心架构

```text
用户问题／批量数据集
        ↓
AgentRunner：并发、整任务重试、检查点、输出记录
        ↓
SearchAgent：一次任务中的模型—工具交互循环
        ├─ Parser ↔ LLM Client ↔ 模型服务
        └─ Tool → Source → 本地文件／网络／Elasticsearch
                 或 → MCP 服务
```

| 组件 | 负责什么 | 分离的意义 |
| --- | --- | --- |
| LLM Client | 模型服务 API 通信 | 更换端点不必重写检索 |
| Parser | 消息及工具调用格式转换 | 区分原生 tool calls 与文本编码工具调用 |
| Source | 检索或取回文档 | 数据源不直接决定智能体行为 |
| Tool | 暴露给模型的操作，如 search、visit | 多个工具可共享数据源 |
| SearchAgent | 单条轨迹的循环、工具分发和结束控制 | 将推理策略与批量调度分开 |
| AgentRunner | 并发、持久化、任务恢复 | 支撑批量研究与故障定位 |

YAML/Hydra 配置将这些组件组合起来。`upstream` parser 适用于供应商返回结构化工具调用的情况；工具调用写在文本中的模型可能需要专用 parser。（架构及入门文档）

源码 `src/searcherkit/agent/search_agent.py` 的 `SearchAgentConfig` 提供 `max_turn`、上下文 token 预算、时间预算和重试配置。特别注意：其中 `max_tokens` 文档解释为上下文预算检查，不宜直接当成单次生成上限；时间预算可以触发收尾提示，硬超时仍可能要由调用方执行。

## 实际能搜什么？

### 本地文件

0.1.1 的 `FileSource` 调用 `ripgrep`，参数含 `--fixed-strings` 与 `--smart-case`，因此这里是**字面文本匹配**，不是默认向量语义检索。`top_k` 控制保留的命中文件数，结果 score 固定为 1.0，不应把返回顺序当成训练过的相关性排序。（源码 `sources/file.py`）

它适合 Markdown、代码、配置等可读文本；官方入门明确不提供 PDF、图像等二进制内容解析。路径解析会检查实际路径仍处于 `root_path` 内，但这只是文件访问边界，不等同于完整的进程沙箱、网络隔离或权限系统。

### 网络

0.1.1 的 `WebSource` 默认使用 **Google Serper 搜索 + Jina Reader 取回网页**，要求 Serper API key，提供超时、并发和重试配置。框架可以扩展，不代表现有实现已原生支持所有搜索服务。（源码 `sources/web.py`）

### Elasticsearch 与 MCP

源码包含 Elasticsearch source；官方文档另列 MCP-backed tools。两者分别解决检索后端与外部工具接入问题。具体索引、鉴权、服务部署和插件行为仍需按自己的环境配置。（架构文档；源码目录）

## 与普通搜索、RAG 有什么区别？

以下是按交互机制做的对照，不是论文性能比较。

| 方式 | 典型流程 | 谁决定下一步 |
| --- | --- | --- |
| 普通搜索 API | 输入查询 → 返回结果 | 调用者 |
| 固定单轮 RAG | 检索 → 拼接上下文 → 生成答案 | 预设流程 |
| SearcherKit 搜索智能体 | 提问 → 搜索 → 阅读 → 改写查询／补查 → 回答 | 模型在框架约束下决策 |

SearcherKit 与 RAG 并不互斥：它可以承载多轮、工具驱动的检索增强流程；“智能体式 RAG”也可以采用类似机制。关键差异是控制流程，而不是是否使用向量库。

多轮搜索能处理证据不足、查询需要修正的问题，但也增加模型 token、工具费用和延迟；应按[[wiki/synthesis/后训练与智能体/模型-框架与评测协议的比较边界|模型、框架与评测协议的比较边界]]控制相同模型、检索后端和预算，再比较结果。

## 为什么强调训练？

官方架构将普通推理与训练 rollout 连接起来：模型在相同工具环境中执行搜索，保存轨迹，再将记录送到训练流程。

- **[[wiki/concept/后训练与智能体/监督微调SFT|SFT]]**：轨迹转换为目标训练格式，再通过 MS-Swift 启动训练。文档列出转换脚本与 dry-run 检查，不是仅执行一次 `pip install` 就自动完成训练。
- **[[wiki/concept/后训练与智能体/强化学习RL|RL]]**：对接 AReaL、slime，由训练框架拥有 rollout worker 与训练调度，SearcherKit 提供智能体、工具及适配逻辑。源码中能找到两套适配目录及奖励逻辑。
- **检查点评测**：训练出的模型部署到兼容端点后，复用原有工具、parser、数据集和配置进行评测。（训练文档）

这里的优势是减少训练与推理之间的工具行为差异，不等于保证二者完全一致。README 称用该管线训练过有竞争力的 8B 模型，但本次来源中未核实配套实验表、训练成本、具体权重与可复现结果，不能据此宣称优于其他框架。

## 最小试用与本 wiki 的适配

官方入门示例（来自 `latest` 文档，本次未执行）：

```bash
# 在 Python 3.12+ 虚拟环境中
pip install searcherkit==0.1.1
rg --version
export LLM_MODEL="你的模型"
export LLM_API_KEY="你的密钥"
export LLM_BASE_URL="https://你的兼容端点/v1"
export FILE_SEARCH_ROOT="./wiki"
searcher --help
```

随后按所用版本准备包含 `file` source、`search`／`visit` tools 与 parser 的 YAML，再启动交互界面。`latest` 文档给出的快捷命令为 `searcher tui --config-path file_search`；本次未验证此配置别名在 0.1.1 分发包中可用，不能保证照抄即可运行。

**对本工作区最直接的用途是搜索 `wiki/` 中的 Markdown，而不是直接检索 `raw/` 中的 PDF。** 原始 PDF 若要进入该文件搜索路径，应先在另处提取文本，不修改原件。SearcherKit 也没有因此自动获得本项目的引用规范、日志维护、跨页更新与 Git 工作流；这些需要额外的系统提示和执行工具。

## 采用前应检查什么？

1. **证据质量**：核查回答引用是否真的支持结论，搜索片段是否被过度解释；多轮检索本身不保证事实正确。
2. **安全与隐私**：检索到的网页应当视为数据而不是指令；控制 MCP 权限、文件根目录及敏感资料外发。使用远程模型时，“本地文件搜索”不意味着文本不会发送到外部端点。
3. **预算与稳定性**：记录工具调用次数、token、耗时、失败与重试；分别配置批量并发和单条任务预算。
4. **可复现性**：固定包版本、模型、配置与语料快照。检查点用于恢复任务，不意味着冻结网络搜索结果或恢复任意中途模型状态。
5. **依赖与成熟度**：0.1.1 为早期版本号，但不能仅凭版本号判定质量；目前可确认包中有测试目录和训练适配代码，不能把“存在测试”当成“全部通过”或生产稳定性证明。

## 结论与待补问题

**适合需要多轮检索、批量轨迹记录，以及搜索智能体 SFT／RL 实验的研究工作；单次查询接口或固定 RAG 则未必需要这套复杂度。**

本次确认了发布包、架构与部分具体实现。仍待核实：官方 GitHub 规范仓库地址及对应发布提交、独立技术论文、8B 模型实验结果、BCP-Link 与该版本的确切关系，以及端到端安装与运行情况。不把名称相近的 SearchKit 项目自动并入本条目。
