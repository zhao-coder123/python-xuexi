"""Day 6 用户请求模型。"""

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """创建用户请求模型。"""

    name: str = Field(..., min_length=2, max_length=20, description="用户名")
    age: int = Field(..., ge=1, le=120, description="年龄")
    role: str = Field(
        default="student", min_length=2, max_length=20, description="角色"
    )
    city: str = Field(
        default="Hangzhou", min_length=2, max_length=30, description="城市"
    )
