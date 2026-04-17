# Day 7: Week 1 收口

Day 7 的目标很直接：

- 获取用户列表
- 获取单个用户
- 创建用户
- 更新用户
- 删除用户
- 文档可访问

也就是说，Week 1 到今天要收成一个最小 CRUD API。

## 这次你会学到什么

- 一个完整的最小 CRUD 闭环
- `GET / POST / PATCH / DELETE` 的基本职责
- Pydantic 请求校验
- 统一响应结构
- 自定义业务异常

## 运行方式

```bash
cd 2026-04-22-day7
python3 -m uvicorn app.main:app --reload
```

文档地址：

```text
http://127.0.0.1:8000/docs
```

## 推荐测试

```bash
curl "http://127.0.0.1:8000/users"
curl "http://127.0.0.1:8000/users/1"
curl -X POST "http://127.0.0.1:8000/users" -H "Content-Type: application/json" -d '{"name":"Alice","age":23,"role":"student","city":"Beijing"}'
curl -X PATCH "http://127.0.0.1:8000/users/1" -H "Content-Type: application/json" -d '{"city":"Shenzhen"}'
curl -X DELETE "http://127.0.0.1:8000/users/2"
```

## Day 7 学完后的标准

- 你有一个完整的最小 CRUD API
- 你能独立看懂用户增删改查接口
- 你知道一周内学过的内容怎么串起来
