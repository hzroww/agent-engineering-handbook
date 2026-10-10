# 附录 B｜术语对照与易混概念

| 术语 | 人话解释 |
|---|---|
| Agent | 围绕目标根据证据选择行动并持续执行的系统 |
| Agent loop | 请求模型、执行工具、观察结果和决定停止的循环 |
| Workflow | 程序预先规定主要执行路径 |
| ReAct | 决策与行动反馈交替的组织方式 |
| Plan-and-execute | 先形成计划，再执行与必要重规划 |
| Orchestrator | 协调推理、工具、状态与收尾的模块 |
| Harness | 包装运行入口/生命周期的外壳，具体职责因系统而异 |
| Port | 核心需要的能力接口 |
| Adapter | 把具体服务接到能力接口的实现 |
| DTO | 某个边界上的数据传输结构 |
| Principal | 经过验证的当前操作主体 |
| Tenant/workspace | 数据与权限隔离范围，例如组织空间 |
| Conversation | 可持续追问的会话容器 |
| Turn | 一次用户输入引发的一轮工作 |
| Run/response | 一次执行的生命周期记录 |
| Iteration | 主循环的一次模型决策及处理 |
| Attempt | 某次调用的重试尝试 |
| Item | 有类型、有顺序的历史记录单元 |
| Delta | 增量变化，不保证是一个token |
| Token | 模型内容计量单位，不等于字或词 |
| Context window | 一次模型调用可使用的信息容量约束 |
| Canonical history | 真实历史的权威记录 |
| Model projection | 为当前模型构造的历史/证据视图 |
| Compaction | 用摘要和状态替代较早上下文 |
| Frontier | 已被摘要覆盖的历史边界 |
| Overlay | 恢复模型视图时应用的覆盖层 |
| Preserved state | 不依赖摘要模型猜测、确定性保留的工具状态 |
| Long-term memory | 跨会话可检索、更新和遗忘的协作信息 |
| RAG | 检索材料后再基于材料生成答案 |
| Chunk | 被独立索引的文档或内容片段 |
| Embedding | 表示语义特征的向量 |
| BM25 | 常见关键词相关性排序方法，并非所有全文索引都采用它 |
| RRF | 将多路检索排名合并的一种方法 |
| Reranker | 对召回候选再排序的模块/模型 |
| Grounding | 让结论建立在具体可核验证据上 |
| Provenance | 内容来自哪里、何时、谁或哪个工具产生 |
| Tool schema | 工具参数的结构约束 |
| Skill | 完成特定任务的一组说明与资源 |
| MCP | AI应用接入工具与上下文的协议 |
| Sandbox | 限制代码运行环境和可用资源的隔离机制 |
| OAuth scope | 授权允许的能力范围，不等于全部业务权限 |
| Approval | 用户对某次具体动作的确认 |
| Prompt injection | 外部数据伪装成指令影响模型行为 |
| SSRF | 服务被诱导访问不应访问的内部/受限网络资源 |
| TOCTOU | 检查时与执行时状态已改变的竞态 |
| Idempotency | 同一业务请求重复送达不产生额外效果 |
| Fingerprint | 对规范化请求计算的稳定指纹 |
| Lease | 有时限的执行所有权 |
| Fencing | 拒绝旧执行者继续提交或产生受保护效果 |
| Backpressure | 消费者跟不上时对生产速度/缓冲施加限制 |
| Backoff/jitter | 失败后退避等待与随机抖动 |
| Circuit breaker | 依赖持续失败时暂时阻断请求 |
| Outbox | 业务事务内记录待发送事件，后台可靠投递 |
| At-least-once | 至少送达一次，可能重复 |
| Exactly-once | 精确一次效果；必须明确保证范围，不能随意承诺 |
| SSE | HTTP响应上的服务器到客户端文本事件流 |
| Snapshot | 某时刻完整状态投影 |
| Attach | 连接仍在运行的执行者，接收快照及后续变化 |
| Resume | 从已保存边界继续工作，不等于恢复内存future |
| Artifact | 可交付、可引用的生成产物 |
| Dossier | 某对象的结构化证据档案 |
| Object storage | 保存文件对象的服务 |
| Presigned URL | 带时限访问权限的链接，不是永久文件身份 |
| Trace/span | 一次任务的链路及其中的阶段 |
| Metric | 可聚合的计量，如延迟、失败率 |
| Eval | 评估任务效果、风险和效率的方法 |
| Mock/fake | 可预测的测试替身，不是真模型能力证明 |
| Rubric | 评审维度与分级标准 |
| SLO | 服务希望达到的用户体验/可靠性目标 |
| P95 | 95%的观测值不超过的分位点 |
| Shadow evaluation | 不产生真实副作用的旁路比较 |
| Canary rollout | 小范围灰度发布 |
| Price version | 用于历史计费的固定费率版本 |

## 五组必须能区分的词

1. 保存历史 ≠ 本次发给模型 ≠ 模型正确使用。
2. 生成调用 ≠ 执行成功 ≠ 业务目标完成。
3. 请求失败 ≠ 外部操作未发生 ≠ 费用为零。
4. 幂等 ≠ 去重文本 ≠ 会话互斥。
5. 浏览器断线 ≠ 用户取消 ≠ 服务崩溃。

