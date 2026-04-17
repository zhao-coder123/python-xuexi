# Day 14: 分页、过滤、排序

今天重点是把列表接口写得更像后台接口。

你要补上的核心意识：

- 列表接口不能只会“查全部”
- 分页是后台基础能力
- 过滤和搜索会直接影响接口可用性
- 排序参数要尽量稳定可控

## 运行方式

```bash
cd 2026-04-29-day14
python3 -m uvicorn app:app --reload
```

## 测试示例

```bash
curl "http://127.0.0.1:8000/users?page=1&page_size=2"
curl "http://127.0.0.1:8000/users?keyword=mi"
curl "http://127.0.0.1:8000/users?role=student&sort_by=id&sort_order=asc"
```

## 查漏补缺

1. `page / page_size` 是面向前端分页的常见设计
2. `skip / limit` 是服务端内部和数据库层常见设计
3. 排序字段不能完全放开，否则会有安全和维护问题
