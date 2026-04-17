# Day 3: HTTP 和 API 基础

Day 3 开始，你要从“会写 Python 代码”，进入“知道后端接口是怎么工作的”。

今天的重点不是把项目做复杂。

而是先把接口最核心的几个概念学明白。

## 1. HTTP 方法

HTTP 方法就是“这次请求想干什么”。

最常见的是：

- `GET`：读取数据
- `POST`：创建数据
- `PUT`：整体更新数据
- `PATCH`：部分更新数据
- `DELETE`：删除数据

今天你先重点记住两个：

- `GET`
- `POST`

因为 Day 3 的实践任务就是：

- 写 `GET /ping`
- 写 `GET /users/{id}`
- 写 `POST /users`

## 2. 状态码

状态码是后端对请求结果的“数字说明”。

你今天至少要先记住这些：

- `200 OK`：请求成功
- `201 Created`：创建成功
- `400 Bad Request`：请求参数有问题
- `404 Not Found`：资源不存在
- `500 Internal Server Error`：服务器内部错误

在 `app.py` 里你会看到：

- 查询成功默认返回 `200`
- 创建用户返回 `201`
- 用户不存在时返回 `404`
- 用户名重复时返回 `400`

## 3. 请求头 Header

请求头是附加在请求里的元信息。

常见场景：

- 浏览器身份信息 `User-Agent`
- 登录后的 `Authorization`
- 请求体格式 `Content-Type`

Day 3 先知道：

- Header 不属于 path
- Header 不属于 body
- 它是请求的“额外说明信息”

在 `GET /ping` 里，我给你演示了怎么读取：

```python
user_agent = request.headers.get("user-agent", "unknown")
```

## 4. Path / Query / Body 是什么

这是后端最核心的基础之一。

### Path 参数

写在 URL 路径里，用来表示资源 id。

例如：

```text
/users/1
```

这里的 `1` 就是 path 参数。

在代码里对应：

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
```

### Query 参数

写在 URL 后面，用 `?` 开始。

例如：

```text
/users/1?verbose=true
/users?role=student
```

它常用于：

- 筛选
- 搜索
- 分页
- 排序

### Body 参数

写在请求体里，通常是 JSON。

例如创建用户时：

```json
{
  "name": "Alice",
  "age": 23,
  "role": "student"
}
```

在代码里，这部分由 `UserCreate` 模型来接收。

## 5. JSON 接口设计基础

前后端通信里最常见的数据格式就是 JSON。

所以你要开始建立一个意识：

- 接口通常返回 JSON
- 前端通常发送 JSON
- 后端内部也会经常把对象转成 JSON 可用结构

一个最简单的接口返回值像这样：

```json
{
  "message": "success",
  "data": {
    "id": 1,
    "name": "Minda"
  }
}
```

Day 3 先不用纠结统一响应格式设计得多高级。

先建立两个习惯：

- 返回结构尽量清晰
- 字段命名尽量稳定

## 当前目录文件说明

- `app.py`：Day 3 的最小 FastAPI 示例
- `README.md`：Day 3 的知识点说明

## 这次代码里你能学到什么

`app.py` 里包含了这些接口：

### `GET /`

- 最简单的根路径接口
- 用来确认服务是否启动

### `GET /ping`

- 最经典的健康检查接口
- 演示读取请求头 `header`

### `GET /users/{user_id}`

- 演示 path 参数
- 演示 query 参数 `verbose`
- 演示 `404` 状态码

### `GET /users`

- 演示 query 参数筛选 `role`

### `POST /users`

- 演示 JSON body
- 演示创建成功 `201`
- 演示重复用户名时报 `400`

## 运行方式

进入目录：

```bash
cd 2026-04-18-day3
```

启动服务：

```bash
uvicorn app:app --reload
```

如果你本机没有全局 `uvicorn`，也可以用：

```bash
python -m uvicorn app:app --reload
```

启动后打开：

- `http://127.0.0.1:8000/docs`

这里是 FastAPI 自动生成的 Swagger 文档。

你可以直接在页面里测试接口。

## 推荐你手动测试这几个接口

### 1. 健康检查

```bash
curl http://127.0.0.1:8000/ping
```

### 2. 获取单个用户

```bash
curl "http://127.0.0.1:8000/users/1?verbose=true"
```

### 3. 获取用户列表

```bash
curl "http://127.0.0.1:8000/users?role=student"
```

### 4. 创建用户

```bash
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","age":23,"role":"student"}'
```

## 你现在还要额外补的知识

结合 Day 1、Day 2、Day 3，你接下来还要特别补这几个点：

### 1. 请求和响应的完整概念

你现在已经见过接口，但还要继续补：

- 请求行
- 请求头
- 请求体
- 响应头
- 响应体

只要这个概念一清楚，后面学 API 会轻松很多。

### 2. JSON 和 Python 字典的关系

你现在容易把两者混在一起。

要记住：

- Python 里常用 `dict`
- 网络传输里常用 JSON
- FastAPI 会帮你做很多转换，但你得知道它们不是一回事

### 3. 参数校验意识

现在你已经看到 body 校验了。

接下来要继续建立意识：

- 前端传什么，后端不能无脑信什么
- 参数必须校验
- 类型、范围、是否必填都要关心

### 4. REST 风格的基本直觉

你现在不需要背很多理论。

但先建立直觉：

- `/users` 通常表示资源集合
- `/users/1` 通常表示单个资源
- `GET /users` 是查列表
- `POST /users` 是创建

这个直觉越早有，后面写接口越不容易乱。

## 今天学完后的标准

如果你能做到这些，就算 Day 3 过关：

- 知道 `GET` 和 `POST` 的区别
- 知道 `200`、`201`、`400`、`404` 分别大概表示什么
- 知道 header、path、query、body 的区别
- 能看懂一个最简单的 FastAPI 接口文件
- 能启动服务并在 `/docs` 里测试接口

## 建议你自己再动手改 4 个地方

1. 给 `GET /users` 再加一个 `age` 筛选参数
2. 给 `POST /users` 加一个邮箱字段
3. 故意请求不存在的用户，观察 `404` 返回
4. 在浏览器和 `curl` 下都请求一次 `/ping`，对比 `user-agent`
