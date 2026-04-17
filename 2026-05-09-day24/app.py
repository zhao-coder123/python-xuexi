"""Day 24: Dify 接入示例。"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

from dify_service import call_dify


app = FastAPI(
    title="Day 24 Dify Demo",
    description="用于学习 Dify API 调用和最小 FastAPI 封装。",
    version="0.1.0",
)


class DifyRequest(BaseModel):
    query: str = Field(..., min_length=3)


@app.post("/dify/chat", summary="Dify 对话")
async def dify_chat(data: DifyRequest) -> dict[str, object]:
    result = await call_dify(data.query)
    return {"message": "success", "data": result}
