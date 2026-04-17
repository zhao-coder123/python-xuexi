# Day 22: 模型 API 基础接入

今天重点：

- 模型 API 请求结构
- Prompt 基础
- 超时与重试意识
- 成本意识

## 运行方式

```bash
cd 2026-05-07-day22
python3 -m uvicorn app:app --reload
```

## 本地安全配置

复制 `.env.example` 到 `.env.local`，再填你的真实 LLM Key。

`.env.local` 已经被 Git 忽略，不会提交。

## 测试示例

```bash
curl -X POST "http://127.0.0.1:8000/ai/summary" -H "Content-Type: application/json" -d '{"content":"FastAPI 是一个现代 Python Web 框架，支持异步编程和自动文档生成。"}'
```

## 查漏补缺

1. LLM 接口先封装成 service，不要直接散落在路由里
2. Prompt 也属于业务输入的一部分，需要可维护
3. 没有真实 API Key 时，mock 流程也很重要
