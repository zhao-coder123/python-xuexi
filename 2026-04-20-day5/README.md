# Day 5: 响应、异常、文档

Day 5 的目标，是把接口从“能跑”推进到“更像正式项目”。

今天重点补这 4 个能力：

- 统一响应结构
- 全局异常处理
- Swagger / OpenAPI 文档
- 状态码规范

## 1. 为什么要统一响应结构

如果每个接口都随便返回，前端会很难用。

比如有的接口返回：

```json
{"message": "success", "data": {...}}
```

有的接口返回：

```json
{"ok": true, "result": {...}}
```

有的报错又返回：

```json
{"detail": "用户不存在"}
```

那前端每调一个接口都要重新猜字段。

所以正式项目里通常会统一成：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

报错也尽量统一：

```json
{
  "code": 40401,
  "message": "用户不存在",
  "data": null
}
```

这次我已经在 `app/core/response.py` 里帮你封装好了：

- `success_response()`
- `error_response()`

## 2. 为什么要做全局异常处理

如果不做全局异常处理，接口报错时返回格式会不统一。

比如：

- 业务错误一个格式
- 校验错误一个格式
- 代码异常又一个格式

这样前端处理起来很麻烦。

所以 Day 5 的重点就是：

- 业务异常统一拦截
- `HTTPException` 统一拦截
- 参数校验错误统一拦截
- 未知异常统一兜底

这次我在 `app/main.py` 里给你写了 4 个异常处理器。

## 3. 自定义业务异常

这次我给你加了：

```python
class AppException(Exception):
```

它的作用是：

- 当你明确知道这是一个业务错误时
- 不直接随便抛字符串
- 而是抛一个统一的业务异常对象

这样后面异常处理器就能把它转成稳定格式的 JSON 响应。

## 4. 状态码规范

Day 5 你不需要背全，但要先形成基本习惯：

- `200`：成功
- `201`：创建成功
- `400`：请求不合法
- `404`：资源不存在
- `422`：参数校验失败
- `500`：服务器内部错误

注意：

- HTTP 状态码是协议层语义
- `code` 是你们业务自己的语义

这两个不是一回事，但经常一起使用。

## 5. Swagger / OpenAPI 文档

FastAPI 的一个很大优点就是自带文档。

你现在要开始养成这个习惯：

- 给接口写 `summary`
- 给参数写 `description`
- 给应用写 `title` 和 `description`

这样 `/docs` 页面会更清楚。

这次我顺手把一个很适合现在补上的点也加进去了：

- `response_model`

它的作用是：

- 让 Swagger 文档更清楚
- 明确接口成功返回的大致结构
- 为后面更规范的响应模型设计打基础

## 当前目录结构

```text
app/
  main.py
  data.py
  core/
    response.py
    exceptions.py
  routers/
    users.py
  schemas/
    user.py
README.md
```

## 这次代码里你能学到什么

### `app/core/response.py`

- 成功响应封装
- 失败响应封装

### `app/core/exceptions.py`

- 自定义业务异常 `AppException`

### `app/main.py`

- 全局异常处理
- 统一错误输出
- FastAPI 文档元信息

### `app/routers/users.py`

- 统一成功响应
- 业务异常抛出
- `GET /users`
- `GET /users/{id}`
- `POST /users`
- `PATCH /users/{id}`
- 演示 500 错误的接口

## 运行方式

进入目录：

```bash
cd 2026-04-20-day5
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

### 获取用户列表

```bash
curl "http://127.0.0.1:8000/users?role=student"
```

### 获取单个用户

```bash
curl "http://127.0.0.1:8000/users/1"
```

### 创建用户

```bash
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name":"Bob","age":25,"role":"student","city":"Shanghai"}'
```

### 触发业务异常

```bash
curl "http://127.0.0.1:8000/users/999"
```

### 触发参数校验异常

```bash
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name":"A","age":-1,"role":"x","city":"y"}'
```

### 触发 500 异常

```bash
curl "http://127.0.0.1:8000/users/demo/error"
```

## Day 5 学完后的标准

如果你能做到这些，就算 Day 5 过关：

- 知道为什么要统一响应体
- 知道为什么要做全局异常处理
- 能区分业务错误、校验错误、服务器错误
- 知道 HTTP 状态码和业务 code 不是一回事
- 能在 Swagger 文档里直接调试接口

## 你接下来最该继续补的点

1. `response_model` 的使用
2. 更规范的错误码设计
3. 日志记录
4. 服务层和路由层继续拆分
5. 数据库接入后如何保持统一响应和统一异常
