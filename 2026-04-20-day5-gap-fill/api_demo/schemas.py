"""API 示例的请求和响应模型。"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    student = "student"
    developer = "developer"
    admin = "admin"


class UserItem(BaseModel):
    id: int
    name: str
    age: int = Field(..., ge=1, le=120)
    role: UserRole
    city: str


class UserReplace(BaseModel):
    """PUT 使用的整体替换模型。"""

    name: str = Field(..., min_length=2, max_length=20)
    age: int = Field(..., ge=1, le=120)
    role: UserRole
    city: str = Field(..., min_length=2, max_length=30)


class UserPatch(BaseModel):
    """PATCH 使用的部分更新模型。"""

    name: Optional[str] = Field(default=None, min_length=2, max_length=20)
    age: Optional[int] = Field(default=None, ge=1, le=120)
    role: Optional[UserRole] = None
    city: Optional[str] = Field(default=None, min_length=2, max_length=30)


class ApiResponse(BaseModel):
    code: int
    message: str
    data: Any = None


class ApiErrorResponse(BaseModel):
    code: int
    message: str
    data: Any = None
