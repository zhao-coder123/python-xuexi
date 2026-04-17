"""Day 13 鉴权工具。"""

from typing import Callable

import jwt
from fastapi import Depends, Header, HTTPException, status


SECRET_KEY = "day13-secret"
ALGORITHM = "HS256"

fake_users_db = {
    1: {"id": 1, "username": "admin", "role": "admin"},
    2: {"id": 2, "username": "editor_user", "role": "editor"},
}


def create_demo_token(user_id: int) -> str:
    return jwt.encode({"sub": str(user_id)}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(authorization: str = Header(default="")) -> dict[str, object]:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="缺少 Bearer Token"
        )

    token = authorization.replace("Bearer ", "", 1)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token 无效"
        ) from error

    user_id = int(payload["sub"])
    user = fake_users_db.get(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在"
        )

    return user


def require_role(role: str) -> Callable:
    def dependency(
        current_user: dict[str, object] = Depends(get_current_user),
    ) -> dict[str, object]:
        if current_user["role"] != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="权限不足"
            )
        return current_user

    return dependency
