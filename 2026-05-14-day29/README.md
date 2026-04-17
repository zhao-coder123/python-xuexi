# Day 29: 部署基础

今天重点：

- 环境变量管理
- Docker 基础
- 生产启动方式
- 反向代理认知
- `docker-compose` 多服务编排

## 这次给你的文件

- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`

## 查漏补缺

1. 开发环境能跑，不等于部署友好
2. Docker 解决的是环境一致性问题
3. `docker-compose` 适合把 MySQL、Redis、FastAPI 一起管理
4. `.env.local` 不能打进镜像或提交到 Git
