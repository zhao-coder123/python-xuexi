"""Day 7 用户服务层。"""

from typing import Optional

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


fake_users_db = [
    User(id=1, name="Minda", age=24, role="student", city="Hangzhou"),
    User(id=2, name="Tom", age=26, role="developer", city="Shanghai"),
]


def list_users(keyword: str) -> list[User]:
    if not keyword:
        return fake_users_db

    keyword_lower = keyword.lower()
    return [user for user in fake_users_db if keyword_lower in user.name.lower()]


def get_user_by_id(user_id: int) -> Optional[User]:
    for user in fake_users_db:
        if user.id == user_id:
            return user

    return None


def create_user(user: UserCreate) -> User:
    new_user = User(
        id=len(fake_users_db) + 1,
        name=user.name,
        age=user.age,
        role=user.role,
        city=user.city,
    )
    fake_users_db.append(new_user)
    return new_user


def update_user(user_id: int, user: UserUpdate) -> Optional[User]:
    update_data = user.model_dump(exclude_none=True)

    for item in fake_users_db:
        if item.id == user_id:
            for key, value in update_data.items():
                setattr(item, key, value)
            return item

    return None


def delete_user(user_id: int) -> bool:
    for index, item in enumerate(fake_users_db):
        if item.id == user_id:
            fake_users_db.pop(index)
            return True

    return False
