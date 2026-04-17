"""Day 6 用户服务层。"""

from typing import Optional

from app.models.user import User
from app.schemas.user import UserCreate


fake_users_db = [
    User(id=1, name="Minda", age=24, role="student", city="Hangzhou"),
    User(id=2, name="Tom", age=26, role="developer", city="Shanghai"),
    User(id=3, name="Alice", age=22, role="student", city="Beijing"),
]


def list_users(
    skip: int, limit: int, role: Optional[str] = None
) -> tuple[list[User], int]:
    """获取用户列表。"""

    result = fake_users_db
    if role is not None:
        result = [user for user in result if user.role == role]

    total = len(result)
    sliced = result[skip : skip + limit]
    return sliced, total


def get_user_by_id(user_id: int) -> Optional[User]:
    """根据 id 获取用户。"""

    for user in fake_users_db:
        if user.id == user_id:
            return user

    return None


def create_user(user: UserCreate) -> User:
    """创建用户。"""

    new_user = User(
        id=len(fake_users_db) + 1,
        name=user.name,
        age=user.age,
        role=user.role,
        city=user.city,
    )
    fake_users_db.append(new_user)
    return new_user
