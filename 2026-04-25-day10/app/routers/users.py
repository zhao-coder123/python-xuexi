"""Day 10 用户路由。"""

from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services import user_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[UserOut], summary="获取用户列表")
def list_users(db: Session = Depends(get_db)) -> list:
    return user_service.list_users(db)


@router.get("/{user_id}", response_model=UserOut, summary="获取单个用户")
def get_user(user_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    return user


@router.post(
    "", response_model=UserOut, status_code=status.HTTP_201_CREATED, summary="创建用户"
)
def create_user(user: UserCreate = Body(...), db: Session = Depends(get_db)):
    return user_service.create_user(db, user)


@router.patch("/{user_id}", response_model=UserOut, summary="更新用户")
def update_user(
    user_id: int = Path(..., ge=1),
    user: UserUpdate = Body(...),
    db: Session = Depends(get_db),
):
    updated_user = user_service.update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    return updated_user
