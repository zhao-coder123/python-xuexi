"""Day 23: 流式输出基础示例。"""

import asyncio
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse


app = FastAPI(
    title="Day 23 Streaming Demo",
    description="用于学习 SSE / 流式输出基础。",
    version="0.1.0",
)


async def stream_text() -> AsyncGenerator[str, None]:
    chunks = [
        "正在分析内容...",
        "正在提取关键点...",
        "正在组织摘要...",
        "摘要生成完成。",
    ]
    for chunk in chunks:
        await asyncio.sleep(0.5)
        yield f"data: {chunk}\n\n"


@app.get("/stream/summary", summary="流式摘要示例")
async def stream_summary() -> StreamingResponse:
    return StreamingResponse(stream_text(), media_type="text/event-stream")
