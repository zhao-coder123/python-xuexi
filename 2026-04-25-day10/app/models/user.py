"""Day 10 用户 ORM 模型。"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    """SQLAlchemy ORM 模型。

    这张表默认会建在 SQLite 里，
    但换成 MySQL 连接串后，思路是一样的。
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="student")
    city: Mapped[str] = mapped_column(String(50), nullable=False, default="Hangzhou")
