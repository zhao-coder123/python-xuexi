# Day 6: 项目分层

前五天你已经会写最小 API 了。

Day 6 要开始学“项目结构为什么要拆层”。

今天重点是：

- `router / service / schema / model / core` 分层
- 配置管理
- 环境变量
- `pydantic-settings`
- `Depends` 依赖注入继续深入

## 这次结构

```text
app/
  main.py
  routers/
    users.py
  services/
    user_service.py
  schemas/
    user.py
  models/
    user.py
  core/
    config.py
    deps.py
```

## 每层是干嘛的

- `routers/`：接收 HTTP 请求，定义接口
- `services/`：写业务逻辑
- `schemas/`：定义请求和响应的数据结构
- `models/`：定义领域模型
- `core/`：放配置、依赖、通用能力

## 这次补上的两个关键工程点

### 1. `pydantic-settings`

你现在开始用它来统一管理配置。

这意味着你以后可以用同一种方式管理：

- 数据库地址
- Redis 地址
- JWT 密钥
- 调试开关

### 2. `Depends`

这次不是只拿它来做参数，而是开始拿它封装公共逻辑：

- 分页参数依赖
- 配置对象依赖

## 运行方式

```bash
cd 2026-04-21-day6
python3 -m uvicorn app.main:app --reload
```

文档地址：

```text
http://127.0.0.1:8000/docs
```

## 可测试接口

```bash
curl "http://127.0.0.1:8000/api/v1/users?role=student&skip=0&limit=2"
curl "http://127.0.0.1:8000/api/v1/users/1"
curl -X POST "http://127.0.0.1:8000/api/v1/users" -H "Content-Type: application/json" -d '{"name":"Bob","age":25,"role":"student","city":"Shanghai"}'
```

## Day 6 学完后的标准

- 你知道为什么要分层
- 你知道配置不该写死在代码里
- 你能看懂 `Depends` 不是只用来做鉴权
- 你知道分页依赖这种公共逻辑怎么封装
