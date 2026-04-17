# Day 13: 鉴权与权限

今天重点是：

- 依赖注入方式鉴权
- 当前用户获取
- `admin / editor` 角色
- 权限拦截思路

## 运行方式

```bash
cd 2026-04-28-day13
python3 -m uvicorn app.main:app --reload
```

## 推荐测试顺序

1. 先请求 `/auth/login/admin`
2. 拿到 token 后请求 `/me`
3. 再访问 `/admin/dashboard`
4. 再用 editor token 试一下，会看到权限差异

## 查漏补缺

这里最容易混淆的点：

1. 鉴权：你是谁
2. 权限：你能做什么
3. Token 能证明身份，不自动等于拥有所有权限
