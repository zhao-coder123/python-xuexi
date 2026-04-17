"""Day 4: FastAPI 路由与参数示例入口。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.ping import router as ping_router
from app.routers.users import router as users_router


app = FastAPI(
    title="Day 4 FastAPI Router Demo",
    description="用于学习路由拆分、Query 参数、Path 参数、Body 参数、Pydantic 校验和 CORS 配置。",
    version="0.1.0",
)


# CORS 的作用是允许前端页面跨域访问当前接口。
# 本地开发阶段经常会遇到：前端 5173 端口，后端 8000 端口。
# 如果不配置允许来源，浏览器会拦截跨域请求。
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ping_router)
app.include_router(users_router)
