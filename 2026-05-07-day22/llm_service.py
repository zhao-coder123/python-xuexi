"""Day 22 模型 API 封装。"""

from __future__ import annotations

import httpx

from config import get_settings


async def generate_text(task_name: str, prompt: str) -> dict[str, object]:
    """调用模型 API。

    如果本地没有配置 API Key，就返回一个 mock 结果，
    这样你可以先把整个调用链跑通。
    """

    settings = get_settings()

    if not settings.llm_api_key:
        return {
            "task": task_name,
            "content": f"[mock] {task_name}: {prompt[:60]}",
            "source": "mock",
        }

    url = settings.llm_base_url.rstrip("/") + "/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.llm_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    return {
        "task": task_name,
        "content": data["choices"][0]["message"]["content"],
        "source": "remote",
    }
