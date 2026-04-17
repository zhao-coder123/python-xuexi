"""Day 12 密码和 JWT 工具。"""

import base64
import hashlib
import hmac
import os
from datetime import datetime, timedelta

import jwt

from app.core.config import get_settings


def hash_password(password: str) -> str:
    """使用 PBKDF2 对密码做哈希。

    学习阶段先用标准库就够了，
    正式项目里常见的是 `passlib + bcrypt`。
    """

    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 100000
    )
    return base64.b64encode(salt + password_hash).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    raw = base64.b64decode(hashed_password.encode("utf-8"))
    salt = raw[:16]
    stored_hash = raw[16:]
    candidate_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 100000
    )
    return hmac.compare_digest(candidate_hash, stored_hash)


def create_access_token(user_id: int, username: str) -> str:
    settings = get_settings()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": str(user_id), "username": username, "exp": expire}
    return jwt.encode(
        payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
