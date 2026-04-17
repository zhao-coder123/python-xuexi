"""Day 10: SQLAlchemy 入门示例入口。"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.core.database import Base, engine
from app.models.user import User
from app.routers.users import router as users_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # 示例启动时自动建表，方便本地直接运行。
    Base.metadata.create_all(bind=engine)

    # 如果表里还没有数据，就插入两条演示数据。
    with Session(engine) as session:
        user_count = session.query(User).count()
        if user_count == 0:
            session.add_all(
                [
                    User(name="Minda", age=24, role="student", city="Hangzhou"),
                    User(name="Tom", age=26, role="developer", city="Shanghai"),
                ]
            )
            session.commit()

    yield


app = FastAPI(
    title="Day 10 SQLAlchemy Demo",
    description="用于学习 ORM Model、Session、查询提交和 get_db() 依赖注入。",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(users_router)
