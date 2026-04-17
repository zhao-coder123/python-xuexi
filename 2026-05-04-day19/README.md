# Day 19: 错误处理与代码规范

今天重点：

- 自定义异常
- 错误码设计
- 中间件
- `ruff` 和 `black`

## 运行方式

```bash
cd 2026-05-04-day19
python3 -m uvicorn app:app --reload
```

## 推荐测试

```bash
curl -i "http://127.0.0.1:8000/demo/ping"
curl -i "http://127.0.0.1:8000/demo/business-error"
curl -i "http://127.0.0.1:8000/demo/server-error"
```

## 代码规范命令

```bash
python3 -m black .
python3 -m ruff check .
```

## 查漏补缺

1. 错误码不是乱写数字
2. 中间件适合做横切能力，比如请求日志、耗时统计、trace id
3. 日志里不要打印密码、token 等敏感信息
