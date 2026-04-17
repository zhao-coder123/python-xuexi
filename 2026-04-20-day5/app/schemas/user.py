"""Day 5 用户相关 Pydantic 模型。"""

from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """创建用户请求模型。"""

    name: str = Field(..., min_length=2, max_length=20, description="用户名")
    age: int = Field(..., ge=1, le=120, description="年龄")
    role: str = Field(
        default="student", min_length=2, max_length=20, description="角色"
    )
    city: str = Field(
        default="Hangzhou", min_length=2, max_length=30, description="所在城市"
    )


class UserUpdate(BaseModel):
    """部分更新请求模型。

    Optional 表示这些字段都不是必填，
    非常适合 PATCH 这种“部分更新”场景。
    """

    age: Optional[int] = Field(default=None, ge=1, le=120, description="年龄")
    role: Optional[str] = Field(
        default=None, min_length=2, max_length=20, description="角色"
    )
    city: Optional[str] = Field(
        default=None, min_length=2, max_length=30, description="所在城市"
    )


class UserListItem(BaseModel):
    """用户列表项模型。

    这里先保留给你做认知，当前示例里不强制使用 response_model，
    是为了让 Day 5 先聚焦统一响应体和异常处理。
    """

    id: int
    name: str
    age: int
    role: str
    city: str
