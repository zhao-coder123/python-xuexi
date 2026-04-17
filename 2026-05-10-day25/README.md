# Day 25: 把 Dify 接到业务模块里

今天重点：

- 平台能力和业务接口结合
- 结果保存与追踪
- 错误回退

## 运行方式

```bash
cd 2026-05-10-day25
python3 -m uvicorn app:app --reload
```

## 测试示例

```bash
curl -X POST "http://127.0.0.1:8000/articles/1/summary"
curl -X POST "http://127.0.0.1:8000/articles/1/rewrite"
curl -X POST "http://127.0.0.1:8000/articles/1/title-optimize"
```

## 查漏补缺

1. AI 能力最好挂到已有业务资源下，而不是散着放
2. 文章模块是最适合接 AI 摘要、改写、标题优化的入口
3. 真正项目里通常还要把 AI 结果存数据库
