"""Day 3: HTTP 和 API 基础示例。

这个文件的目标不是做完整项目，
而是让你在最小代码量里看懂下面这些后端基础：

1. HTTP 方法是什么
2. 状态码是什么
3. 请求头怎么读取
4. query / path / body 分别是什么
5. JSON 接口是怎么设计的

运行方式：
    uvicorn app:app --reload

启动后可以访问：
    http://127.0.0.1:8000/docs
"""

from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel, Field


# FastAPI 实例就是整个应用的入口。
# title / description 会展示在 Swagger 文档里。
app = FastAPI(
    title="Day 3 HTTP API Demo",
    description="用于学习 HTTP 方法、状态码、请求头、query/path/body 和 JSON 接口基础。",
    version="0.1.0",
)


class UserCreate(BaseModel):
    """创建用户时，请求体 body 应该长什么样。

    这里虽然 Day 4 会系统学 Pydantic，
    但 Day 3 先见一次是有必要的，
    因为 FastAPI 接收 JSON body 时非常常用。
    """

    name: str = Field(..., min_length=2, max_length=20, description="用户名")
    age: int = Field(..., ge=1, le=120, description="年龄")
    role: str = Field(default="student", description="用户角色")


# 用列表模拟数据库表。
# 正式项目里，这部分会换成 MySQL 或其他数据库。
fake_users_db = [
    {"id": 1, "name": "Minda", "age": 24, "role": "student"},
    {"id": 2, "name": "Tom", "age": 26, "role": "developer"},
]


@app.get("/")
def read_root() -> dict[str, str]:
    """根路径接口。

    一个最简单的 GET 接口，
    常用于告诉别人“服务已经启动”。
    """

    return {"message": "Day 3 API is running"}


@app.get("/ping")
def ping(request: Request) -> dict[str, object]:
    """最经典的健康检查接口。

    这里顺便演示“请求头 header”的读取方式。
    浏览器、Postman、前端请求都会带一些 header。
    """

    # Request 对象里能拿到请求的很多信息，
    # 比如 headers、url、method、client 等。
    user_agent = request.headers.get("user-agent", "unknown")

    return {
        "message": "pong",
        "method": request.method,
        "time": datetime.now().isoformat(timespec="seconds"),
        "user_agent": user_agent,
    }


@app.get("/users/{user_id}")
def get_user(user_id: int, verbose: bool = False) -> dict[str, object]:
    """根据用户 id 获取单个用户。

    这里同时演示两个重要概念：
    1. path 参数: `/users/{user_id}` 里的 `user_id`
    2. query 参数: URL 后面的 `?verbose=true`

    例子：
        /users/1
        /users/1?verbose=true
    """

    # path 参数通常用来表示“资源标识”，
    # 比如用户 id、文章 id、订单 id。
    for user in fake_users_db:
        if user["id"] == user_id:
            if verbose:
                return {
                    "message": "success",
                    "data": user,
                    "tips": "你使用了 verbose=true，所以返回了额外说明。",
                }

            return {"message": "success", "data": user}

    # 找不到数据时，后端通常不会返回普通字符串，
    # 而是返回合适的 HTTP 状态码。
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"id 为 {user_id} 的用户不存在",
    )


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate) -> dict[str, object]:
    """创建用户接口。

    这里的 `user: UserCreate` 就表示：
    前端必须传一个 JSON body，
    并且这个 JSON 结构要符合 UserCreate 模型。

    例如请求体：
    {
      "name": "Alice",
      "age": 23,
      "role": "student"
    }
    """

    # 正式项目里通常还会查数据库看用户名是否重复。
    for item in fake_users_db:
        if item["name"].lower() == user.name.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在",
            )

    new_user = {
        "id": len(fake_users_db) + 1,
        "name": user.name,
        "age": user.age,
        "role": user.role,
    }

    fake_users_db.append(new_user)

    # POST 创建成功时，常见状态码是 201 Created。
    return {
        "message": "user created",
        "data": new_user,
    }


@app.get("/users")
def list_users(role: Optional[str] = None) -> dict[str, object]:
    """用户列表接口。

    这个接口额外演示一个常见 query 参数场景：筛选。
    例子：
        /users
        /users?role=student
    """

    if role is None:
        return {
            "message": "success",
            "total": len(fake_users_db),
            "data": fake_users_db,
        }

    filtered_users = [user for user in fake_users_db if user["role"] == role]

    return {"message": "success", "total": len(filtered_users), "data": filtered_users}
