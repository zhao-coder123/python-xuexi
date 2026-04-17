"""Day 7 统一响应。"""

from typing import Any


def success_response(data: Any = None, message: str = "success") -> dict[str, Any]:
    return {"code": 0, "message": message, "data": data}


def error_response(message: str, code: int, data: Any = None) -> dict[str, Any]:
    return {"code": code, "message": message, "data": data}
