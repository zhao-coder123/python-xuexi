# Day 23: 流式输出基础

今天重点：

- SSE / streaming 基础
- 前后端联调方式
- 流式输出的交互价值

## 运行方式

```bash
cd 2026-05-08-day23
python3 -m uvicorn app:app --reload
```

## 测试方式

```bash
curl -N "http://127.0.0.1:8000/stream/summary"
```

## 查漏补缺

1. 流式输出不是只能用于聊天
2. 核心价值是让用户尽快看到“正在处理”
3. SSE 比 WebSocket 更适合很多单向输出场景
