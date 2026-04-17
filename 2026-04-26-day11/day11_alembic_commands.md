# Day 11 Alembic 命令清单

## 1. 初始化 Alembic

```bash
alembic init migrations
```

## 2. 修改 `alembic.ini`

```ini
sqlalchemy.url = mysql+pymysql://root:123456@150.158.95.116:3306/ai_admin_demo
```

正式项目里更推荐从环境变量读取，而不是把密码直接写进仓库文件。

## 3. 生成迁移

```bash
alembic revision -m "create users and roles"
```

## 4. 执行迁移

```bash
alembic upgrade head
```

## 5. 回滚一步

```bash
alembic downgrade -1
```

## 查漏补缺

- `head` 表示当前最新版本
- `downgrade -1` 表示回退一步
- 迁移脚本不是只会升级，也要会回滚
