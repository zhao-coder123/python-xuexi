"""Day 14: 分页、过滤、排序示例。"""

from datetime import datetime, timedelta

from fastapi import FastAPI, Query


app = FastAPI(
    title="Day 14 List API Demo",
    description="用于学习分页、过滤、排序的列表接口设计。",
    version="0.1.0",
)


base_time = datetime(2026, 4, 1, 9, 0, 0)
fake_users_db = [
    {
        "id": 1,
        "name": "Minda",
        "role": "student",
        "created_at": base_time + timedelta(days=1),
    },
    {
        "id": 2,
        "name": "Tom",
        "role": "developer",
        "created_at": base_time + timedelta(days=2),
    },
    {
        "id": 3,
        "name": "Alice",
        "role": "student",
        "created_at": base_time + timedelta(days=3),
    },
    {
        "id": 4,
        "name": "Bob",
        "role": "admin",
        "created_at": base_time + timedelta(days=4),
    },
    {
        "id": 5,
        "name": "Cindy",
        "role": "editor",
        "created_at": base_time + timedelta(days=5),
    },
]


@app.get("/users", summary="分页列表接口")
def list_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=2, ge=1, le=100),
    keyword: str = Query(default=""),
    role: str = Query(default=""),
    sort_by: str = Query(default="created_at"),
    sort_order: str = Query(default="desc"),
) -> dict[str, object]:
    result = fake_users_db

    if keyword:
        lower_keyword = keyword.lower()
        result = [item for item in result if lower_keyword in item["name"].lower()]

    if role:
        result = [item for item in result if item["role"] == role]

    reverse = sort_order == "desc"
    if sort_by in {"id", "name", "created_at"}:
        result = sorted(result, key=lambda item: item[sort_by], reverse=reverse)

    total = len(result)
    start = (page - 1) * page_size
    end = start + page_size
    items = result[start:end]

    return {
        "message": "success",
        "data": {
            "items": items,
            "pagination": {"page": page, "page_size": page_size, "total": total},
        },
    }
