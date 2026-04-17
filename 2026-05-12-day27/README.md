# Day 27: AI 任务记录与异步化

今天重点：

- 长耗时任务设计
- 任务状态管理
- 后台异步执行思路

## 运行方式

```bash
cd 2026-05-12-day27
python3 -m uvicorn app:app --reload
```

## 测试示例

```bash
curl -X POST "http://127.0.0.1:8000/ai-tasks" -H "Content-Type: application/json" -d '{"task_type":"summary","content":"这是一段用于测试 AI 任务系统的文章内容。"}'
curl "http://127.0.0.1:8000/ai-tasks"
curl "http://127.0.0.1:8000/ai-tasks/1"
```

## 查漏补缺

1. AI 调用常常不是同步秒回的
2. 一旦耗时变长，就要有任务状态
3. 最少要记录输入、状态、输出、耗时
