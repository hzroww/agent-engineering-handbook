# Agent 工程学习手册

从概念到实现，从正常链路到故障边界：一套可连续阅读、可面试复习、可用于设计新系统的中文资料。

## 从哪里开始

- [单文件总册 BOOK.md](BOOK.md)：连续阅读全部正文、附录与实验说明。
- [学习路线与自测](appendices/D-learning-route.md)：按基础、实践和面试三个目标安排阅读。
- [60 个递进面试追问](appendices/A-interview-drills.md)：各章还附有专题问答和练习。
- [故障排查速查表](appendices/C-troubleshooting.md)：遇到问题按现象定位链路。
- [无密钥教学实验](labs/README.md)：只用 Python 标准库，验证四类关键不变量。
- [范围、限制与公开参考](appendices/E-coverage-and-references.md)：先理解材料能证明什么、不能证明什么。

初学者建议先读第01—04章，再沿第22章做垂直切片。不要一开始就把所有架构组件全部搭出来。

## 24 章目录

1. [从零建立 Agent 的正确认识](chapters/01-foundations.md)
2. [整体架构、模块边界与技术选型](chapters/02-architecture.md)
3. [完整请求链路与调试 JSON](chapters/03-request-lifecycle.md)
4. [Agent Loop、状态机与停止条件](chapters/04-agent-loop.md)
5. [模型协议、提示词与供应商兼容](chapters/05-model-protocol-and-prompts.md)
6. [上下文工程与短期记忆](chapters/06-context-and-short-memory.md)
7. [上下文压缩与恢复](chapters/07-compaction.md)
8. [长期记忆、RAG 与知识库](chapters/08-long-memory-and-rag.md)
9. [工具调用与失败兜底](chapters/09-tools-and-failure-recovery.md)
10. [Skill 设计与用户意图](chapters/10-skills-and-intent-routing.md)
11. [沙箱、MCP 与凭据](chapters/11-sandbox-mcp-and-credentials.md)
12. [数据库与 JSON 字段映射](chapters/12-storage-and-data-model.md)
13. [多用户、并发、幂等与租约](chapters/13-multiuser-concurrency-and-idempotency.md)
14. [流式、取消、重连与恢复](chapters/14-streaming-cancellation-and-resume.md)
15. [后台任务、定时调度与回调](chapters/15-background-jobs-and-scheduling.md)
16. [多模态、视觉证据与产物](chapters/16-multimodal-and-artifacts.md)
17. [安全、提示注入与人工确认](chapters/17-security-and-human-approval.md)
18. [Token、成本与账单](chapters/18-token-cost-and-billing.md)
19. [Trace、Eval 与 CI](chapters/19-tracing-evals-and-ci.md)
20. [规划、自检与多 Agent](chapters/20-planning-and-multiagent.md)
21. [部署、性能与长期演进](chapters/21-production-and-evolution.md)
22. [从零设计完整应用](chapters/22-end-to-end-design-workshop.md)
23. [能力地图与前端证据展示](chapters/23-capability-map-and-interfaces.md)
24. [故障复盘案例](chapters/24-incident-casebook.md)

## 附录

- [A｜60 个递进面试追问](appendices/A-interview-drills.md)
- [B｜术语对照与易混概念](appendices/B-glossary.md)
- [C｜故障排查速查表](appendices/C-troubleshooting.md)
- [D｜学习路线与设计评审清单](appendices/D-learning-route.md)
- [E｜覆盖范围、可信边界与公开参考](appendices/E-coverage-and-references.md)
- [F｜检索与评测进阶](appendices/F-retrieval-and-evaluation-deep-dive.md)

## 怎么使用这份资料

每个主题尽量按“问题→机制→数据/流程→取舍→失败→测试→追问”展开。先用人话讲清责任，再保留正式术语，便于继续查官方文档。

正文的“参考模式”与“推荐设计”不是同一标签。示例接口、SQL和代码是教学表达，不是完整生产系统。模型价格使用明确虚构的计算示例；供应商窗口、协议版本、平台权限需要接入时重新核验。

本书没有声称“读完就自动成为资深工程师”。真正的掌握需要实现、故障注入、压测与复盘。也不要将学习内容直接包装成自己已经做过的工作或编造效果数据。

## 本地运行与维护

要求 Python 3.10+，无需安装依赖或配置 API Key。

```bash
python3 -m unittest discover -s labs -v
python3 -m unittest discover -s tests -v
python3 scripts/book.py
python3 scripts/book.py --check
```

第一组验证教学模型，第二组验证文档构建工具。总册由分章机械合并；编辑原章节后重新生成，避免两份内容漂移。文档检查验证本地链接、代码围栏与总册同步，不替代内容正确性审查。

版本：2026-10-10 学习版。外部链接可能更新；将方案用于真实系统前，请补充环境对应的验证。
