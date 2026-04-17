"""Day 6 用户路由。"""

from dataclasses import asdict
from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from app.core.config import Settings, get_settings
from app.core.deps import PaginationParams, get_pagination
from app.schemas.user import UserCreate
from app.services.user_service import create_user, get_user_by_id, list_users


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", summary="获取用户列表")
def get_users(
    role: Optional[str] = Query(default=None, description="按角色筛选"),
    pagination: PaginationParams = Depends(get_pagination),
    settings: Settings = Depends(get_settings),
) -> dict[str, object]:
    """获取用户列表。

    这里同时演示两个依赖：
    1. 分页依赖
    2. 配置依赖
    """

    users, total = list_users(skip=pagination.skip, limit=pagination.limit, role=role)

    return {
        "message": "success",
        "app_name": settings.app_name,
        "pagination": {
            "skip": pagination.skip,
            "limit": pagination.limit,
            "total": total,
        },
        "data": [asdict(user) for user in users],
    }


@router.get("/{user_id}", summary="获取单个用户")
def get_user(
    user_id: int = Path(..., ge=1, description="用户 id"),
) -> dict[str, object]:
    """根据 id 获取单个用户。"""

    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    return {"message": "success", "data": asdict(user)}


@router.post("", status_code=status.HTTP_201_CREATED, summary="创建用户")
def add_user(
    user: UserCreate = Body(..., description="创建用户请求体"),
) -> dict[str, object]:
    """创建用户。"""

    new_user = create_user(user)
    return {"message": "user created", "data": asdict(new_user)}
