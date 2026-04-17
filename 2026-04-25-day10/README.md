# Day 10: SQLAlchemy 入门

Day 10 开始正式进入 ORM。

今天重点要看懂这些：

- ORM 是什么
- Model 怎么定义
- Session 是什么
- 查询、提交、刷新是怎么做的
- 数据库连接如何管理
- `get_db()` 为什么这么写

## 这次为什么默认用 SQLite

计划里写的是 MySQL + SQLAlchemy，方向没有变。

但为了让你现在本地可以直接跑起来，
这次示例默认使用 SQLite：

- 不需要额外装 MySQL
- 不影响你理解 SQLAlchemy ORM 的核心用法

等你本机 MySQL 准备好后，把 `.env` 里的连接串改掉就行。

另外，这个示例启动时会自动插入两条演示用户数据，
这样你第一次访问 `/users` 就能直接看到 ORM 查询结果。

## 这次结构

```text
app/
  main.py
  core/
    config.py
    database.py
  models/
    user.py
  schemas/
    user.py
  services/
    user_service.py
  routers/
    users.py
```

## 关键点说明

### 1. ORM Model

`app/models/user.py` 里定义了 `User` 表映射。

### 2. Session

`app/core/database.py` 里定义了：

- `engine`
- `SessionLocal`
- `get_db()`

这就是 FastAPI + SQLAlchemy 的经典组合。

### 3. `get_db()` 依赖注入

这一段非常重要：

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

它的作用是：

- 每次请求拿到一个数据库会话
- 用完后自动关闭

## 运行方式

```bash
cd 2026-04-25-day10
python3 -m uvicorn app.main:app --reload
```

## 测试接口

```bash
curl "http://127.0.0.1:8000/users"
curl -X POST "http://127.0.0.1:8000/users" -H "Content-Type: application/json" -d '{"name":"Bob","age":25,"role":"student","city":"Shanghai"}'
curl "http://127.0.0.1:8000/users/1"
curl -X PATCH "http://127.0.0.1:8000/users/1" -H "Content-Type: application/json" -d '{"city":"Shenzhen"}'
```

## 切换到 MySQL 时怎么改

把 `.env` 改成类似：

```text
DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/ai_admin_demo
```

然后再安装 MySQL 驱动，例如：

```bash
pip install pymysql
```

## Day 10 学完后的标准

- 你知道 ORM 和手写 SQL 的关系
- 你知道 `Model / Session / get_db()` 的基本职责
- 你能看懂 SQLAlchemy 最小 CRUD 流程
