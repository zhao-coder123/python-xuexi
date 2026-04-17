"""Day 10 用户 Pydantic 模型。"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=20)
    age: int = Field(..., ge=1, le=120)
    role: str = Field(default="student", min_length=2, max_length=20)
    city: str = Field(default="Hangzhou", min_length=2, max_length=30)


class UserUpdate(BaseModel):
    age: Optional[int] = Field(default=None, ge=1, le=120)
    role: Optional[str] = Field(default=None, min_length=2, max_length=20)
    city: Optional[str] = Field(default=None, min_length=2, max_length=30)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    role: str
    city: str
