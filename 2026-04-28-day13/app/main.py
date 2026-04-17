"""Day 13: 鉴权与权限入口。"""

from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.protected import router as protected_router


app = FastAPI(
    title="Day 13 Permission Demo",
    description="用于学习依赖注入鉴权、当前用户获取和角色权限基础。",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(protected_router)
