"""Day 20: 测试基础示例应用。"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(title="Day 20 Test Demo", version="0.1.0")

users = [{"id": 1, "username": "admin"}]
articles = []


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)


class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)


@app.post("/auth/register")
def register(data: RegisterRequest) -> dict[str, object]:
    if any(item["username"] == data.username for item in users):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在"
        )

    new_user = {"id": len(users) + 1, "username": data.username}
    users.append(new_user)
    return {"message": "register success", "data": new_user}


@app.post("/auth/login")
def login() -> dict[str, object]:
    return {"message": "login success", "data": {"access_token": "demo-token"}}


@app.get("/users")
def list_users() -> dict[str, object]:
    return {"message": "success", "data": users}


@app.post("/articles")
def create_article(data: ArticleCreate) -> dict[str, object]:
    article = {"id": len(articles) + 1, "title": data.title}
    articles.append(article)
    return {"message": "article created", "data": article}
