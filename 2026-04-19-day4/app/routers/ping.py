"""Day 4 健康检查路由。"""

from datetime import datetime

from fastapi import APIRouter, Request


router = APIRouter(tags=["Health"])


@router.get("/ping", summary="健康检查")
def ping(request: Request) -> dict[str, object]:
    """返回一个最简单的接口响应。

    这里保留读取 header 的写法，
    让你继续熟悉 Request 对象。
    """

    return {
        "message": "pong",
        "method": request.method,
        "time": datetime.now().isoformat(timespec="seconds"),
        "user_agent": request.headers.get("user-agent", "unknown"),
    }
