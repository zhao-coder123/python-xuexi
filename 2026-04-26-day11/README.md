# Day 11: Alembic 迁移

Day 11 的重点不是再写一个接口，而是学会“正规管理表结构变化”。

你今天要补上的核心认知：

- 为什么不能手改线上表结构
- 为什么需要 migration
- Alembic 是怎么管理版本的
- `upgrade` / `downgrade` 是什么

## 这次给你的文件

- `migration_example.py`
- `day11_alembic_commands.md`

## 迁移最小流程

1. 安装 Alembic
2. 初始化 Alembic 目录
3. 配置数据库连接
4. 生成迁移脚本
5. 执行迁移

## 查漏补缺

如果你前 10 天已经会建表，但还不会迁移，那你还缺这几个意识：

1. 数据库结构也需要版本管理
2. 新人接手项目不能靠口口相传建表
3. `CREATE TABLE` 只是起点，表结构未来一定会变
4. 迁移脚本需要可回滚思维

## 真实数据库配置

这个目录会读取本地 `.env.local`，但这个文件已经被 Git 忽略。

你可以在本地使用真实 MySQL 连接测试 Alembic。
