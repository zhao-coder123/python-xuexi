"""前五天 HTTP / Pydantic / 鉴权补漏示例。

运行:
    python3 -m uvicorn api_demo.app:app --reload
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Header, Path, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api_demo.schemas import (
    ApiErrorResponse,
    ApiResponse,
    UserItem,
    UserPatch,
    UserReplace,
)

app = FastAPI(
    title="Day 5 Gap Fill API Demo",
    description="补充 PUT/PATCH/DELETE、Authorization、response_model 和错误响应文档。",
    version="0.1.0",
)

fake_users_db = [
    {"id": 1, "name": "Minda", "age": 24, "role": "student", "city": "Hangzhou"},
    {"id": 2, "name": "Tom", "age": 26, "role": "developer", "city": "Shanghai"},
]


def success_response(data: Any = None, message: str = "success") -> dict[str, Any]:
    return {"code": 0, "message": message, "data": data}


def error_response(code: int, message: str, data: Any = None) -> dict[str, Any]:
    return {"code": code, "message": message, "data": data}


def require_bearer_token(authorization: str | None) -> None:
    """演示最基础的 Authorization 头校验。"""

    if authorization is None:
        raise DemoAPIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code=40100,
            message="缺少 Authorization 请求头",
        )

    if not authorization.startswith("Bearer "):
        raise DemoAPIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code=40101,
            message="Authorization 必须使用 Bearer Token 格式",
        )

    token = authorization.removeprefix("Bearer ").strip()
    if token != "demo-token":
        raise DemoAPIException(
            status_code=status.HTTP_403_FORBIDDEN,
            code=40300,
            message="Token 无效或没有权限访问",
        )


def find_user_index(user_id: int) -> int:
    for index, user in enumerate(fake_users_db):
        if user["id"] == user_id:
            return index

    raise DemoAPIException(
        status_code=status.HTTP_404_NOT_FOUND,
        code=40401,
        message=f"id 为 {user_id} 的用户不存在",
    )


class DemoAPIException(Exception):
    def __init__(self, status_code: int, code: int, message: str) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(message)


@app.exception_handler(DemoAPIException)
async def demo_exception_handler(_, exc: DemoAPIException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(code=exc.code, message=exc.message),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            code=42200,
            message="请求参数校验失败",
            data=exc.errors(),
        ),
    )


error_responses = {
    401: {"model": ApiErrorResponse, "description": "未提供或格式错误的认证信息"},
    403: {"model": ApiErrorResponse, "description": "认证通过但没有访问权限"},
    404: {"model": ApiErrorResponse, "description": "资源不存在"},
    422: {"model": ApiErrorResponse, "description": "请求参数校验失败"},
}


@app.get("/users", response_model=ApiResponse, summary="获取用户列表")
def list_users() -> dict[str, Any]:
    items = [UserItem(**item).model_dump() for item in fake_users_db]
    return success_response(data={"total": len(items), "items": items})


@app.get(
    "/users/{user_id}",
    response_model=ApiResponse,
    responses=error_responses,
    summary="获取单个用户",
)
def get_user(
    user_id: int = Path(..., ge=1, description="用户 id"),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> dict[str, Any]:
    require_bearer_token(authorization)
    user_index = find_user_index(user_id)
    user = UserItem(**fake_users_db[user_index]).model_dump()
    return success_response(data=user)


@app.put(
    "/users/{user_id}",
    response_model=ApiResponse,
    responses=error_responses,
    summary="整体替换用户",
)
def replace_user(
    payload: UserReplace,
    user_id: int = Path(..., ge=1, description="用户 id"),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> dict[str, Any]:
    require_bearer_token(authorization)
    user_index = find_user_index(user_id)

    replaced_user = {"id": user_id, **payload.model_dump()}
    fake_users_db[user_index] = replaced_user
    return success_response(
        data=UserItem(**replaced_user).model_dump(),
        message="user replaced",
    )


@app.patch(
    "/users/{user_id}",
    response_model=ApiResponse,
    responses=error_responses,
    summary="部分更新用户",
)
def patch_user(
    payload: UserPatch,
    user_id: int = Path(..., ge=1, description="用户 id"),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> dict[str, Any]:
    require_bearer_token(authorization)
    user_index = find_user_index(user_id)

    current_user = fake_users_db[user_index].copy()
    current_user.update(payload.model_dump(exclude_none=True))
    fake_users_db[user_index] = current_user

    return success_response(
        data=UserItem(**current_user).model_dump(),
        message="user patched",
    )


@app.delete(
    "/users/{user_id}",
    response_model=ApiResponse,
    responses=error_responses,
    summary="删除用户",
)
def delete_user(
    user_id: int = Path(..., ge=1, description="用户 id"),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> dict[str, Any]:
    require_bearer_token(authorization)
    user_index = find_user_index(user_id)
    deleted_user = fake_users_db.pop(user_index)
    return success_response(
        data=UserItem(**deleted_user).model_dump(),
        message="user deleted",
    )
