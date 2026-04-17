"""Day 10 用户服务层。"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id.asc()).all()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(name=user.name, age=user.age, role=user.role, city=user.city)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        return None

    update_data = user.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user
