"""Day 13 登录演示路由。"""

from fastapi import APIRouter

from app.core.security import create_demo_token


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login/admin", summary="管理员登录")
def login_admin() -> dict[str, object]:
    return {"access_token": create_demo_token(1), "token_type": "bearer"}


@router.post("/login/editor", summary="编辑登录")
def login_editor() -> dict[str, object]:
    return {"access_token": create_demo_token(2), "token_type": "bearer"}
