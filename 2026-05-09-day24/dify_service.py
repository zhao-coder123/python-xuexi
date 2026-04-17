"""Day 24 Dify 调用服务。"""

from __future__ import annotations

import httpx

from config import get_settings


async def call_dify(query: str) -> dict[str, object]:
    settings = get_settings()

    if not settings.dify_api_key:
        return {"answer": f"[mock dify] {query}", "source": "mock"}

    url = settings.dify_base_url.rstrip("/") + "/v1/chat-messages"
    headers = {
        "Authorization": f"Bearer {settings.dify_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "user": "demo-user",
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    return {"answer": data.get("answer", ""), "source": "remote"}
