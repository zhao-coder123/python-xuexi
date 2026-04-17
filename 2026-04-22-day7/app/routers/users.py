"""Day 7 用户 CRUD 路由。"""

from dataclasses import asdict

from fastapi import APIRouter, Body, Path, Query, status

from app.core.exceptions import AppException
from app.core.response import success_response
from app.schemas.user import UserCreate, UserUpdate
from app.services import user_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", summary="获取用户列表")
def list_users(
    keyword: str = Query(default="", description="按用户名关键字搜索"),
) -> dict[str, object]:
    users = user_service.list_users(keyword)
    return success_response(data=[asdict(user) for user in users])


@router.get("/{user_id}", summary="获取单个用户")
def get_user(
    user_id: int = Path(..., ge=1, description="用户 id"),
) -> dict[str, object]:
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise AppException(
            message="用户不存在", code=40401, status_code=status.HTTP_404_NOT_FOUND
        )

    return success_response(data=asdict(user))


@router.post("", status_code=status.HTTP_201_CREATED, summary="创建用户")
def create_user(
    user: UserCreate = Body(..., description="创建用户请求体"),
) -> dict[str, object]:
    new_user = user_service.create_user(user)
    return success_response(data=asdict(new_user), message="user created")


@router.patch("/{user_id}", summary="更新用户")
def update_user(
    user_id: int = Path(..., ge=1, description="用户 id"),
    user: UserUpdate = Body(..., description="部分更新用户请求体"),
) -> dict[str, object]:
    updated_user = user_service.update_user(user_id, user)
    if updated_user is None:
        raise AppException(
            message="用户不存在", code=40401, status_code=status.HTTP_404_NOT_FOUND
        )

    return success_response(data=asdict(updated_user), message="user updated")


@router.delete("/{user_id}", summary="删除用户")
def delete_user(
    user_id: int = Path(..., ge=1, description="用户 id"),
) -> dict[str, object]:
    deleted = user_service.delete_user(user_id)
    if not deleted:
        raise AppException(
            message="用户不存在", code=40401, status_code=status.HTTP_404_NOT_FOUND
        )

    return success_response(message="user deleted")
