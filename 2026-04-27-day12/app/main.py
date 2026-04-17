"""Day 12: 注册、登录、JWT 示例入口。"""

from fastapi import FastAPI

from app.routers.auth import router as auth_router


app = FastAPI(
    title="Day 12 Auth Demo",
    description="用于学习用户注册、密码加密、登录接口和 JWT 基础。",
    version="0.1.0",
)

app.include_router(auth_router)
