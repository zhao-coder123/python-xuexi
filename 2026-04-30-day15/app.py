"""Day 15: 内容管理模块示例。"""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="Day 15 Articles Demo",
    description="用于学习后台业务模块设计和文章 CRUD。",
    version="0.1.0",
)


class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    summary: str = Field(default="", max_length=500)
    content: str = Field(..., min_length=10)
    status: str = Field(default="draft")


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=200)
    summary: Optional[str] = Field(default=None, max_length=500)
    content: Optional[str] = Field(default=None, min_length=10)
    status: Optional[str] = Field(default=None)


fake_articles_db = [
    {
        "id": 1,
        "title": "Python 基础",
        "summary": "Day 1 总结",
        "content": "这是第一天文章内容示例。",
        "status": "published",
    }
]


@app.get("/articles")
def list_articles() -> dict[str, object]:
    return {"message": "success", "data": fake_articles_db}


@app.get("/articles/{article_id}")
def get_article(article_id: int) -> dict[str, object]:
    for article in fake_articles_db:
        if article["id"] == article_id:
            return {"message": "success", "data": article}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")


@app.post("/articles", status_code=status.HTTP_201_CREATED)
def create_article(article: ArticleCreate) -> dict[str, object]:
    new_article = article.model_dump()
    new_article["id"] = len(fake_articles_db) + 1
    fake_articles_db.append(new_article)
    return {"message": "article created", "data": new_article}


@app.patch("/articles/{article_id}")
def update_article(article_id: int, article: ArticleUpdate) -> dict[str, object]:
    update_data = article.model_dump(exclude_none=True)
    for item in fake_articles_db:
        if item["id"] == article_id:
            item.update(update_data)
            return {"message": "article updated", "data": item}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")


@app.delete("/articles/{article_id}")
def delete_article(article_id: int) -> dict[str, object]:
    for index, item in enumerate(fake_articles_db):
        if item["id"] == article_id:
            fake_articles_db.pop(index)
            return {"message": "article deleted", "data": None}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")
