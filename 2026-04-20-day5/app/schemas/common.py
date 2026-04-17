"""Day 5 通用响应模型。"""

from typing import Any

from pydantic import BaseModel


class ApiResponse(BaseModel):
    """统一成功响应模型。

    这里把 data 定义成 Any，
    是为了让前五天的示例保持简单，
    不在现在就把泛型响应模型复杂化。
    """

    code: int
    message: str
    data: Any = None


class ApiErrorResponse(BaseModel):
    """统一错误响应模型。"""

    code: int
    message: str
    data: Any = None
