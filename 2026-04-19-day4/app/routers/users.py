"""Day 4 用户路由。

这个文件集中演示：
1. APIRouter 路由拆分
2. Query 参数
3. Path 参数
4. Body 参数
5. Pydantic 请求校验
"""

from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Path, Query, status

from app.data import fake_users_db
from app.schemas.user import UserCreate, UserOut


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", summary="获取用户列表")
def list_users(
    role: Optional[str] = Query(default=None, description="按角色筛选"),
    min_age: Optional[int] = Query(default=None, ge=1, description="最小年龄筛选"),
) -> dict[str, object]:
    """获取用户列表。

    这里的 `role` 和 `min_age` 都是 Query 参数。
    例子：
        /users
        /users?role=student
        /users?role=student&min_age=23
    """

    result = fake_users_db

    if role is not None:
        result = [user for user in result if user["role"] == role]

    if min_age is not None:
        result = [user for user in result if user["age"] >= min_age]

    return {
        "message": "success",
        "total": len(result),
        "data": result,
    }


@router.get("/{user_id}", summary="获取单个用户")
def get_user(
    user_id: int = Path(..., ge=1, description="用户 id"),
    include_message: bool = Query(default=False, description="是否返回额外说明"),
) -> dict[str, object]:
    """根据 Path 参数获取单个用户。"""

    for user in fake_users_db:
        if user["id"] == user_id:
            if include_message:
                return {
                    "message": "success",
                    "data": user,
                    "tips": "你开启了 include_message，所以这里返回了额外说明。",
                }

            return {"message": "success", "data": user}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"id 为 {user_id} 的用户不存在",
    )


@router.post("", status_code=status.HTTP_201_CREATED, summary="创建用户")
def create_user(
    user: UserCreate = Body(..., description="创建用户需要的 JSON 请求体"),
) -> dict[str, object]:
    """根据 Body 参数创建用户。"""

    for item in fake_users_db:
        if item["name"].lower() == user.name.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在",
            )

    new_user = {
        "id": len(fake_users_db) + 1,
        "name": user.name,
        "age": user.age,
        "role": user.role,
        "city": user.city,
    }
    fake_users_db.append(new_user)

    user_out = UserOut(**new_user)

    return {
        "message": "user created",
        "data": user_out.model_dump(),
    }
