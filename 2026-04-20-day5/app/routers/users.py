"""Day 5 用户路由。

重点演示：
1. 统一成功响应
2. 抛出业务异常
3. 使用更清晰的状态码
4. 让 Swagger 文档更可读
"""

from typing import Optional

from fastapi import APIRouter, Body, Path, Query, status

from app.core.exceptions import AppException
from app.core.response import success_response
from app.data import fake_users_db
from app.schemas.common import ApiResponse
from app.schemas.user import UserCreate, UserUpdate


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    summary="获取用户列表",
    description="支持按角色和最小年龄筛选用户列表。",
    response_model=ApiResponse,
)
def list_users(
    role: Optional[str] = Query(default=None, description="按角色筛选"),
    min_age: Optional[int] = Query(default=None, ge=1, description="最小年龄"),
) -> dict[str, object]:
    """统一返回用户列表。"""

    result = fake_users_db

    if role is not None:
        result = [user for user in result if user["role"] == role]

    if min_age is not None:
        result = [user for user in result if user["age"] >= min_age]

    return success_response(
        data={
            "total": len(result),
            "items": result,
        }
    )


@router.get(
    "/{user_id}",
    summary="获取单个用户",
    description="根据用户 id 获取用户详情。",
    response_model=ApiResponse,
)
def get_user(
    user_id: int = Path(..., ge=1, description="用户 id"),
) -> dict[str, object]:
    """获取单个用户，不存在时抛出业务异常。"""

    for user in fake_users_db:
        if user["id"] == user_id:
            return success_response(data=user)

    raise AppException(
        message=f"id 为 {user_id} 的用户不存在",
        code=40401,
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="创建用户",
    response_model=ApiResponse,
)
def create_user(
    user: UserCreate = Body(..., description="创建用户需要的 JSON 请求体"),
) -> dict[str, object]:
    """创建用户，演示统一成功响应和业务异常。"""

    for item in fake_users_db:
        if item["name"].lower() == user.name.lower():
            raise AppException(
                message="用户名已存在",
                code=40001,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    new_user = {
        "id": len(fake_users_db) + 1,
        "name": user.name,
        "age": user.age,
        "role": user.role,
        "city": user.city,
    }
    fake_users_db.append(new_user)

    return success_response(data=new_user, message="user created")


@router.patch("/{user_id}", summary="更新用户", response_model=ApiResponse)
def update_user(
    user_id: int = Path(..., ge=1, description="用户 id"),
    user: UserUpdate = Body(..., description="允许部分更新的用户信息"),
) -> dict[str, object]:
    """部分更新用户信息。"""

    update_data = user.model_dump(exclude_none=True)

    for item in fake_users_db:
        if item["id"] == user_id:
            item.update(update_data)
            return success_response(data=item, message="user updated")

    raise AppException(
        message=f"id 为 {user_id} 的用户不存在",
        code=40401,
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.get("/demo/error", summary="演示 500 错误")
def raise_demo_error() -> dict[str, object]:
    """主动抛出一个未处理异常，方便观察全局异常效果。"""

    raise RuntimeError("这是一个演示用的未处理异常")
