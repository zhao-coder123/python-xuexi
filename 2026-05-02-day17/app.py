"""Day 17: Redis 缓存示例。"""

from __future__ import annotations

import json
from typing import Optional

import redis
from fastapi import FastAPI


app = FastAPI(
    title="Day 17 Redis Demo",
    description="用于学习热点接口缓存和 Redis 基础。",
    version="0.1.0",
)


REDIS_URL = "redis://127.0.0.1:6379/0"
memory_cache: dict[str, str] = {}


def get_redis_client() -> Optional[redis.Redis]:
    try:
        client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        client.ping()
        return client
    except redis.RedisError:
        return None


def get_hot_articles_from_source() -> list[dict[str, object]]:
    return [
        {"id": 1, "title": "FastAPI 实战", "views": 1024},
        {"id": 2, "title": "Python 后端学习", "views": 986},
    ]


@app.get("/articles/hot", summary="热点文章列表")
def hot_articles() -> dict[str, object]:
    cache_key = "hot_articles"
    client = get_redis_client()

    if client is not None:
        cached = client.get(cache_key)
        if cached:
            return {"message": "success", "data": json.loads(cached), "cache": "redis"}

        articles = get_hot_articles_from_source()
        client.setex(cache_key, 60, json.dumps(articles, ensure_ascii=False))
        return {"message": "success", "data": articles, "cache": "miss->redis"}

    if cache_key in memory_cache:
        return {
            "message": "success",
            "data": json.loads(memory_cache[cache_key]),
            "cache": "memory",
        }

    articles = get_hot_articles_from_source()
    memory_cache[cache_key] = json.dumps(articles, ensure_ascii=False)
    return {"message": "success", "data": articles, "cache": "miss->memory"}


@app.get("/cache/status", summary="缓存状态")
def cache_status() -> dict[str, object]:
    client = get_redis_client()
    return {"message": "success", "data": {"redis_available": client is not None}}
