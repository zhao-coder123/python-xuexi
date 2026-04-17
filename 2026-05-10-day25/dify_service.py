"""Day 25 文章 AI 服务。"""

from __future__ import annotations

import httpx
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    dify_base_url: str = "https://api.dify.ai"
    dify_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=(".env.local", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()


async def process_article(action: str, content: str) -> dict[str, object]:
    if not settings.dify_api_key:
        return {
            "action": action,
            "result": f"[mock {action}] {content[:60]}",
            "source": "mock",
        }

    query = f"请对下面文章执行 {action}:\n\n{content}"
    url = settings.dify_base_url.rstrip("/") + "/v1/chat-messages"
    headers = {
        "Authorization": f"Bearer {settings.dify_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "user": "article-demo-user",
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    return {"action": action, "result": data.get("answer", ""), "source": "remote"}
