# Day 18: 操作日志与审计

今天重点：

- 后台为什么要审计
- 新增、更新、删除为什么要留痕
- 操作日志最少应该记录什么

## 运行方式

```bash
cd 2026-05-03-day18
python3 -m uvicorn app:app --reload
```

## 测试示例

```bash
curl -X PATCH "http://127.0.0.1:8000/users/1" -H "Content-Type: application/json" -d '{"nickname":"Minda Zhang"}'
curl -X DELETE "http://127.0.0.1:8000/users/2"
curl "http://127.0.0.1:8000/operation-logs"
```

## 查漏补缺

1. 审计日志不是普通调试日志
2. 最少要能回答：谁、在什么时候、对什么、做了什么
3. 生产环境里通常还会记录 IP、请求路径、结果状态
