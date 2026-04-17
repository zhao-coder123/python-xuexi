"""Day 4 用户相关 Pydantic 模型。"""

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """创建用户时的请求模型。

    这就是 Body 参数校验最常见的写法。
    当前端传过来的 JSON 不符合要求时，
    FastAPI 会自动返回 422 校验错误。
    """

    name: str = Field(..., min_length=2, max_length=20, description="用户名")
    age: int = Field(..., ge=1, le=120, description="年龄")
    role: str = Field(
        default="student", min_length=2, max_length=20, description="角色"
    )
    city: str = Field(
        default="Hangzhou", min_length=2, max_length=30, description="所在城市"
    )


class UserOut(BaseModel):
    """返回给前端看的用户结构。"""

    id: int
    name: str
    age: int
    role: str
    city: str
