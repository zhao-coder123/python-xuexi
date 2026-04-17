# Day 24: Dify 基础认知与接入

今天重点：

- Dify 应用模式
- Chatflow / Workflow / Agent 基本概念
- Dify API 调用方式
- 为什么当前主线优先 Dify

## 运行方式

```bash
cd 2026-05-09-day24
python3 -m uvicorn app:app --reload
```

## 本地安全配置

把 `.env.example` 复制成 `.env.local`，填入你的 Dify Key。

## 查漏补缺

1. Dify 适合快速把 AI 能力接进业务
2. Dify 和 LangChain 不是互斥关系，而是层级不同
3. 先把 API 调通，再考虑复杂工作流
