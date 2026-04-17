# Day 15: 内容管理模块

今天开始不只是练技术点，而是开始练“业务模块”。

这次你要补上的关键认知：

- 用户模块只是开始
- 一个后台系统通常至少还有内容模块
- 业务字段设计和技术字段设计要分开看

## 运行方式

```bash
cd 2026-04-30-day15
python3 -m uvicorn app:app --reload
```

## 测试示例

```bash
curl "http://127.0.0.1:8000/articles"
curl -X POST "http://127.0.0.1:8000/articles" -H "Content-Type: application/json" -d '{"title":"FastAPI 入门","summary":"示例摘要","content":"这里是一段足够长的文章内容示例。","status":"draft"}'
```

## 查漏补缺

1. 业务模块不是把 users 改名成 articles 就结束了
2. 文章模块要开始考虑状态字段、作者字段、摘要字段
3. 内容模块以后会成为 AI 摘要、改写、标题优化的承载点
