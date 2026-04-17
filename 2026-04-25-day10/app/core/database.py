"""Day 10 数据库连接和 Session 管理。"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


settings = get_settings()


class Base(DeclarativeBase):
    """所有 ORM 模型的基类。"""


connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url, echo=False, future=True, connect_args=connect_args
)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, class_=Session
)


def get_db() -> Generator[Session, None, None]:
    """数据库 Session 依赖。

    这是 FastAPI + SQLAlchemy 非常经典的依赖注入写法。
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
