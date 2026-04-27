# Day 5 Gap Fill: 前五天查漏补缺

这个目录专门补前五天里“已经提到，但还没有真正练扎实”的内容。

重点补 5 件事：

1. `venv`、依赖安装、`requirements.txt`
2. 包、模块、`__init__.py`、`python -m`
3. `PUT / PATCH / DELETE` 的语义区别
4. `Authorization` 请求头
5. `response_model`、统一错误响应、`Enum`
6. 异步里什么叫“阻塞”

## 目录说明

```text
2026-04-20-day5-gap-fill/
  README.md
  async_demo.py
  package_demo/
    __init__.py
    models.py
    services.py
    main.py
  api_demo/
    __init__.py
    app.py
    schemas.py
```

## 先补工程基础

前五天你已经会运行单个 Python 文件，但正式项目里还要再建立三个习惯：

- 进入项目后先激活虚拟环境
- 安装依赖尽量基于 `requirements.txt`
- 包内入口优先用 `python -m 包名.模块名`

### 推荐流程

在仓库根目录执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

为什么不直接全局安装：

- 不同项目依赖版本会冲突
- 换电脑后很难复现
- FastAPI、SQLAlchemy、PyJWT 这种库版本变化比较快

## 1. 包和模块怎么练

进入补漏目录后运行：

```bash
cd 2026-04-20-day5-gap-fill
python3 -m package_demo.main
```

这个示例专门演示：

- 为什么目录里要有 `__init__.py`
- 为什么包内导入优先写成 `from package_demo.xxx import ...`
- 为什么推荐用 `python -m package_demo.main`，而不是在包目录里乱切路径跑文件

## 2. HTTP 语义和鉴权头怎么练

启动 API 示例：

```bash
cd 2026-04-20-day5-gap-fill
python3 -m uvicorn api_demo.app:app --reload
```

打开：

```text
http://127.0.0.1:8000/docs
```

这个示例专门补：

- `PUT`：整体替换资源
- `PATCH`：部分更新资源
- `DELETE`：删除资源
- `Authorization: Bearer ...`
- `response_model`
- 统一成功响应和错误响应文档
- `Enum` 限制角色字段

### 推荐测试顺序

1. 先调 `GET /users`
2. 再调 `GET /users/{user_id}`，观察 `Authorization` 头校验
3. 再调 `PUT /users/{user_id}`，观察整体替换
4. 再调 `PATCH /users/{user_id}`，观察部分更新
5. 最后调 `DELETE /users/{user_id}`

### 可直接用的请求示例

获取用户列表：

```bash
curl http://127.0.0.1:8000/users
```

带鉴权头获取单个用户：

```bash
curl http://127.0.0.1:8000/users/1 \
  -H "Authorization: Bearer demo-token"
```

整体替换：

```bash
curl -X PUT http://127.0.0.1:8000/users/1 \
  -H "Authorization: Bearer demo-token" \
  -H "Content-Type: application/json" \
  -d '{"name":"Minda","age":25,"role":"developer","city":"Shanghai"}'
```

部分更新：

```bash
curl -X PATCH http://127.0.0.1:8000/users/1 \
  -H "Authorization: Bearer demo-token" \
  -H "Content-Type: application/json" \
  -d '{"city":"Shenzhen"}'
```

删除：

```bash
curl -X DELETE http://127.0.0.1:8000/users/2 \
  -H "Authorization: Bearer demo-token"
```

## 3. 异步为什么还要继续补

前五天你已经看过 `async` 和 `await`，但还需要真正理解：

- `async def` 不等于一定高性能
- 只要里面用了阻塞代码，照样会卡住
- `time.sleep()` 会阻塞
- `await asyncio.sleep()` 不会阻塞
- CPU 或阻塞 IO 任务有时要交给线程池

运行：

```bash
cd 2026-04-20-day5-gap-fill
python3 async_demo.py
```

你会看到三种情况：

1. 顺序等待
2. 并发等待但内部没阻塞
3. 协程里误用了阻塞函数

## 你现在最该形成的认知

### 工程层

- 能跑不等于适合项目维护
- 包结构、依赖隔离、稳定入口都属于后端基本功

### API 层

- HTTP 状态码是协议语义
- 响应体里的 `code` 是业务语义
- `PUT` 和 `PATCH` 不要混着理解
- 不是所有接口都该匿名访问

### 模型层

- 请求模型和响应模型最好分开
- 错误响应也值得进 Swagger 文档
- `Enum` 比随便传字符串更稳

### 异步层

- 协程不是魔法
- 真正重要的是“有没有阻塞事件循环”

## 建议你补完后的自测题

1. 说清楚 `python foo.py` 和 `python -m package.module` 的区别
2. 说清楚 `PUT` 和 `PATCH` 的区别
3. 说清楚为什么 `Authorization` 不该放在 query 参数里
4. 说清楚 `response_model` 解决了什么问题
5. 说清楚为什么 `async def` 里不能随便写 `time.sleep()`
