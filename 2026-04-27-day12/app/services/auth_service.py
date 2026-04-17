"""Day 12 认证服务。"""

from __future__ import annotations

from typing import Optional

from app.core.security import create_access_token, hash_password, verify_password
from app.schemas.auth import LoginRequest, RegisterRequest


fake_users_db = [
    {
        "id": 1,
        "username": "admin",
        "nickname": "管理员",
        "password_hash": hash_password("12345678"),
    }
]


def create_user(data: RegisterRequest) -> dict[str, object]:
    for user in fake_users_db:
        if user["username"] == data.username:
            raise ValueError("用户名已存在")

    new_user = {
        "id": len(fake_users_db) + 1,
        "username": data.username,
        "nickname": data.nickname,
        "password_hash": hash_password(data.password),
    }
    fake_users_db.append(new_user)
    return {
        "id": new_user["id"],
        "username": new_user["username"],
        "nickname": new_user["nickname"],
    }


def login_user(data: LoginRequest) -> Optional[dict[str, object]]:
    for user in fake_users_db:
        if user["username"] == data.username and verify_password(
            data.password, user["password_hash"]
        ):
            token = create_access_token(user["id"], user["username"])
            return {"access_token": token, "token_type": "bearer"}

    return None
