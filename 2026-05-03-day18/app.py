"""Day 18: 操作日志与审计示例。"""

from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="Day 18 Audit Demo",
    description="用于学习操作日志和审计记录。",
    version="0.1.0",
)


class UserUpdate(BaseModel):
    nickname: str = Field(..., min_length=2, max_length=20)


fake_users_db = [
    {"id": 1, "nickname": "Minda"},
    {"id": 2, "nickname": "Tom"},
]
operation_logs = []


def record_log(
    user_id: int, module: str, action: str, detail: dict[str, object]
) -> None:
    operation_logs.append(
        {
            "id": len(operation_logs) + 1,
            "user_id": user_id,
            "module": module,
            "action": action,
            "detail": detail,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
    )


@app.patch("/users/{user_id}", summary="更新用户昵称")
def update_user(user_id: int, data: UserUpdate) -> dict[str, object]:
    for user in fake_users_db:
        if user["id"] == user_id:
            before = user.copy()
            user["nickname"] = data.nickname
            record_log(
                user_id=user_id,
                module="users",
                action="update",
                detail={"before": before, "after": user.copy()},
            )
            return {"message": "user updated", "data": user}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")


@app.delete("/users/{user_id}", summary="删除用户")
def delete_user(user_id: int) -> dict[str, object]:
    for index, user in enumerate(fake_users_db):
        if user["id"] == user_id:
            deleted_user = fake_users_db.pop(index)
            record_log(
                user_id=user_id,
                module="users",
                action="delete",
                detail={"deleted": deleted_user},
            )
            return {"message": "user deleted", "data": None}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")


@app.get("/operation-logs", summary="操作日志列表")
def list_logs() -> dict[str, object]:
    return {"message": "success", "data": operation_logs}
