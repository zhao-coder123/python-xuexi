# Day 12: 登录与密码处理

今天重点是：

- 用户注册
- 密码加密
- 登录接口
- JWT 基础

## 这次你要补上的关键认知

1. 密码不能明文存数据库
2. 登录成功一般返回 token，不返回密码
3. JWT 只是令牌格式，不等于权限系统本身
4. 注册和登录是两个不同阶段的接口

## 运行方式

```bash
cd 2026-04-27-day12
python3 -m uvicorn app.main:app --reload
```

## 测试示例

```bash
curl -X POST "http://127.0.0.1:8000/auth/register" -H "Content-Type: application/json" -d '{"username":"minda","password":"12345678","nickname":"Minda"}'
curl -X POST "http://127.0.0.1:8000/auth/login" -H "Content-Type: application/json" -d '{"username":"minda","password":"12345678"}'
```

## 查漏补缺

你现在还要明确区分：

- 密码哈希 vs 密码加密
- access token vs refresh token
- 登录成功 vs 鉴权通过
