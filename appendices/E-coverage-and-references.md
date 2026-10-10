# 附录 E｜覆盖范围、可信边界与公开参考

## 内容标签

本书中的“参考模式”表示编写时核对过相应实现路径或测试表达的工程做法；“推荐设计/教学示例”表示为便于理解而重新设计的通用方案；“扩展知识”不代表任何系统已具备该功能。

字段、SQL、接口、状态图与实验代码均为教学表达，不是可直接部署的完整生产系统。不能将它们作为某个线上产品的准确API说明或性能承诺。

## 覆盖矩阵

| 问题域 | 主章节 | 实践方式 |
|---|---|---|
| Agent与Workflow、框架选型 | 01、02、20 | 对比固定链路与反馈循环 |
| 请求、角色、item、协议 | 03、05、12 | 逐条配对调用/结果 |
| loop、状态机、停止与重试 | 04、09 | 注入空输出/截断/503 |
| 意图、Skill、工具目录 | 10、23 | 路由与误触发任务集 |
| 短期记忆、token预算 | 06 | 对比实际模型输入 |
| 压缩与状态保留 | 07 | 边界切分、恢复测试 |
| 长期记忆、RAG | 08 | 污染/冲突/权限/删除测试 |
| 沙箱、凭据、MCP | 11、17 | 最小权限与外发对抗 |
| 数据库、幂等、并发 | 12、13 | 并发屏障、迟到提交 |
| SSE、取消、恢复 | 14 | 半包、断流、快照与终态 |
| 调度、队列、回调 | 15 | 重复触发/重复投递 |
| 视觉、文件、产物 | 16、23 | 缓存过期/追问/文件验证 |
| 成本、预留、结算 | 18 | 定点计费和重复结算 |
| trace、eval、CI | 19 | 假模型链路与真实模型分开 |
| 多Agent与规划 | 20 | 独立子任务对照实验 |
| 性能、部署与演进 | 21 | 容量模型与故障演练 |
| 完整应用设计 | 22 | 五阶段验收 |
| 故障诊断 | 24、附录C | 按时间线找到首个偏离 |
| 面试复盘 | 附录A、D | 60问与证据故事 |
| 检索算法进阶 | 附录F | 候选、过滤和重排实验 |

## 本次没有替你验证的事

没有启动完整生产依赖、没有调用付费模型做任务成功率基准、没有压测多节点、没有验证所有外部平台的实时权限或价格、没有证明所有安全防线不可绕过。不能从局部代码或测试文件的存在推导线上配置和生产指标。

仓库实验只验证四类小模型行为；文档构建检查只验证可生成与链接等格式条件，不证明每条工程建议在你的环境都适用。将来采用时还要补应用级测试。

## 公开一手参考

以下用于进一步核对概念和协议，不是正文全部内容的复制来源。访问核对日期：2026-10-10。current链接可能更新，接入时固定版本并复测。

- [Agent与工作流模式](https://www.anthropic.com/engineering/building-effective-agents)：理解动态决策与预定义流程的区别。
- [ReAct研究入口](https://react-lm.github.io/)：理解行动反馈参与下一步决策。
- [RAG原始论文](https://arxiv.org/abs/2005.11401)：检索与生成组合的研究起点，不等于生产知识库全设计。
- [MCP官方架构](https://modelcontextprotocol.io/docs/learn/architecture)：Host/Client/Server、能力与传输；不同协议版本不要混用。
- [SSE标准](https://html.spec.whatwg.org/multipage/server-sent-events.html)：事件字段、解析与连接行为。
- [Tokio教程](https://tokio.rs/tokio/tutorial)：Rust异步任务与运行时。
- [PostgreSQL锁机制](https://www.postgresql.org/docs/current/explicit-locking.html)：事务锁的范围和冲突。
- [pgvector官方仓库](https://github.com/pgvector/pgvector)：向量搜索、索引与过滤的实现资料。
- [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/)：链路与span概念。
- [OWASP提示注入防护](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)：威胁模型和分层防护参考。

不要背某个型号当前价格/窗口作为长期知识。应记住如何查能力、如何写兼容测试、如何存费率版本与如何证明自己的运行结果。

