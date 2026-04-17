# Day 4: FastAPI 路由与参数

Day 3 你已经知道接口是什么。

Day 4 要开始学“怎么把接口写得更像正式项目”。

今天的重点是：

- 路由拆分
- Query 参数
- Path 参数
- Body 参数
- Pydantic 请求校验
- CORS 跨域配置

## 1. 为什么要拆分路由

Day 3 把所有接口都写在一个 `app.py` 里，是为了方便入门。

但正式项目里，如果所有接口都堆在一个文件里，会越来越难维护。

所以 Day 4 你要开始认识这种结构：

```text
app/
  main.py
  routers/
  schemas/
```

这次我给你拆成了：

- `app/main.py`：应用入口
- `app/routers/ping.py`：健康检查路由
- `app/routers/users.py`：用户相关路由
- `app/schemas/user.py`：Pydantic 模型
- `app/data.py`：模拟数据

## 2. Query 参数

Query 参数在 URL 后面，用来做：

- 筛选
- 搜索
- 分页
- 排序

例子：

```text
/users?role=student
/users?role=student&min_age=23
```

在 `users.py` 里，你会看到：

```python
role: Optional[str] = Query(default=None, description="按角色筛选")
```

这种写法比直接写 `role: str = None` 更清楚，
因为你能明确告诉 FastAPI：

- 它是 Query 参数
- 它的说明是什么
- 它的默认值是什么

## 3. Path 参数

Path 参数写在 URL 路径里，通常表示资源 id。

例子：

```text
/users/1
```

在代码里对应：

```python
user_id: int = Path(..., ge=1, description="用户 id")
```

这里的 `ge=1` 表示必须大于等于 1。

## 4. Body 参数

Body 参数一般是前端提交的 JSON 数据。

例子：

```json
{
  "name": "Bob",
  "age": 25,
  "role": "student",
  "city": "Hangzhou"
}
```

在代码里由 Pydantic 模型接收：

```python
user: UserCreate = Body(...)
```

## 5. Pydantic 请求校验

这是 FastAPI 很重要的一部分。

你现在先建立一个直觉：

- 前端传过来的 JSON，不能直接相信
- 后端要先校验
- 校验通过再处理业务逻辑

这次你会看到：

```python
name: str = Field(..., min_length=2, max_length=20)
age: int = Field(..., ge=1, le=120)
```

这表示：

- 名字长度要在 2 到 20 之间
- 年龄要在 1 到 120 之间

如果不符合，FastAPI 会自动返回 `422`。

## 6. CORS 跨域配置

这是前后端联调时非常常见的问题。

典型场景：

- 前端跑在 `http://localhost:5173`
- 后端跑在 `http://127.0.0.1:8000`

虽然都是本机，但端口不同，浏览器就认为是跨域。

所以后端要明确允许前端来源访问。

这次我在 `app/main.py` 里加了：

```python
app.add_middleware(CORSMiddleware, ...)
```

## 运行方式

进入目录：

```bash
cd 2026-04-19-day4
```

启动服务：

```bash
python3 -m uvicorn app.main:app --reload
```

打开文档：

```text
http://127.0.0.1:8000/docs
```

## 建议你测试这几个接口

### 健康检查

```bash
curl http://127.0.0.1:8000/ping
```

### 用户列表筛选

```bash
curl "http://127.0.0.1:8000/users?role=student&min_age=23"
```

### 获取单个用户

```bash
curl "http://127.0.0.1:8000/users/1?include_message=true"
```

### 创建用户

```bash
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name":"Bob","age":25,"role":"student","city":"Shanghai"}'
```

## Day 4 学完后的标准

如果你能做到这些，就算 Day 4 过关：

- 知道为什么要拆 `routers/`
- 知道 Query、Path、Body 的区别
- 会写简单的 Pydantic 请求模型
- 知道 CORS 是干嘛的
- 能在 `/docs` 里直接测试接口

## 你现在还要继续补的意识

1. 参数说明要写清楚
2. 字段校验要尽量前置
3. 路由、模型、数据不要全混在一个文件里
4. 浏览器跨域问题本质上是浏览器安全策略，不是 FastAPI 独有问题
