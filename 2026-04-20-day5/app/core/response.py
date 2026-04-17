"""Day 5 统一响应结构。"""

from typing import Any


def success_response(
    data: Any = None, message: str = "success", code: int = 0
) -> dict[str, Any]:
    """统一成功响应。"""

    return {
        "code": code,
        "message": message,
        "data": data,
    }


def error_response(message: str, code: int, data: Any = None) -> dict[str, Any]:
    """统一失败响应。"""

    return {
        "code": code,
        "message": message,
        "data": data,
    }
