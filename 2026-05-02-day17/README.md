# Day 17: Redis 基础

今天重点：

- Redis 常见数据结构认知
- 缓存场景
- token / session 辅助场景
- 热点接口缓存

## 运行方式

```bash
cd 2026-05-02-day17
python3 -m uvicorn app:app --reload
```

## 说明

如果你本地没有 Redis，这个示例会自动退回到内存缓存，方便你先把流程跑通。

## 查漏补缺

1. Redis 不是只能当字典用
2. 缓存不是“加了就一定更快”，还要考虑失效策略
3. 热点列表最适合做缓存入门示例
