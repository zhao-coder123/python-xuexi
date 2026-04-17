"""Day 6: 项目分层示例入口。"""

from fastapi import FastAPI

from app.core.config import get_settings
from app.routers.users import router as users_router


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="用于学习 router / service / schema / model 分层、配置管理和 Depends 依赖注入。",
    version="0.1.0",
)

app.include_router(users_router, prefix=settings.api_prefix)
