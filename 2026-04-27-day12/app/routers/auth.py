"""Day 12 认证路由。"""

from fastapi import APIRouter, Body, HTTPException, status

from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth_service import create_user, login_user


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", summary="注册")
def register(data: RegisterRequest = Body(...)) -> dict[str, object]:
    try:
        user = create_user(data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
        ) from error

    return {"message": "register success", "data": user}


@router.post("/login", summary="登录")
def login(data: LoginRequest = Body(...)) -> dict[str, object]:
    result = login_user(data)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
        )

    return {"message": "login success", "data": result}
