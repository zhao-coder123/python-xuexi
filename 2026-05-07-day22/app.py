"""Day 22: 模型 API 基础接入。"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

from llm_service import generate_text


app = FastAPI(
    title="Day 22 LLM Demo",
    description="用于学习模型 API 请求结构、Prompt 基础和最小 AI 功能接口。",
    version="0.1.0",
)


class SummaryRequest(BaseModel):
    content: str = Field(..., min_length=10)


class TitleRequest(BaseModel):
    content: str = Field(..., min_length=10)


@app.post("/ai/summary", summary="文章摘要")
async def article_summary(data: SummaryRequest) -> dict[str, object]:
    prompt = f"请为下面内容生成 1 段简短摘要：\n\n{data.content}"
    result = await generate_text("summary", prompt)
    return {"message": "success", "data": result}


@app.post("/ai/title", summary="标题生成")
async def article_title(data: TitleRequest) -> dict[str, object]:
    prompt = f"请基于下面内容生成 3 个标题：\n\n{data.content}"
    result = await generate_text("title", prompt)
    return {"message": "success", "data": result}
