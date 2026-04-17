"""Day 25: 把 Dify 接到业务模块里。"""

from fastapi import FastAPI, HTTPException, status

from dify_service import process_article


app = FastAPI(
    title="Day 25 Articles AI Demo",
    description="用于学习把 AI 能力挂到文章模块里。",
    version="0.1.0",
)


fake_articles_db = [
    {
        "id": 1,
        "title": "FastAPI 入门",
        "content": "FastAPI 是一个现代 Python Web 框架，支持异步编程和自动文档生成。",
    }
]


def get_article_or_404(article_id: int) -> dict[str, object]:
    for article in fake_articles_db:
        if article["id"] == article_id:
            return article

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")


@app.get("/articles")
def list_articles() -> dict[str, object]:
    return {"message": "success", "data": fake_articles_db}


@app.post("/articles/{article_id}/summary")
async def article_summary(article_id: int) -> dict[str, object]:
    article = get_article_or_404(article_id)
    result = await process_article("摘要", article["content"])
    return {"message": "success", "data": result}


@app.post("/articles/{article_id}/rewrite")
async def article_rewrite(article_id: int) -> dict[str, object]:
    article = get_article_or_404(article_id)
    result = await process_article("改写", article["content"])
    return {"message": "success", "data": result}


@app.post("/articles/{article_id}/title-optimize")
async def article_title_optimize(article_id: int) -> dict[str, object]:
    article = get_article_or_404(article_id)
    result = await process_article("标题优化", article["content"])
    return {"message": "success", "data": result}
