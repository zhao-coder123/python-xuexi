"""Day 27: AI 任务记录与异步化示例。"""

from __future__ import annotations

import time
from datetime import datetime
from threading import Lock

from fastapi import BackgroundTasks, FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="Day 27 AI Tasks Demo",
    description="用于学习 AI 任务记录和后台异步执行思路。",
    version="0.1.0",
)


class AITaskCreate(BaseModel):
    task_type: str = Field(..., min_length=2)
    content: str = Field(..., min_length=5)


ai_tasks: list[dict[str, object]] = []
task_lock = Lock()


def run_ai_task(task_id: int) -> None:
    with task_lock:
        task = next(item for item in ai_tasks if item["id"] == task_id)
        task["status"] = "running"
        task["started_at"] = datetime.now().isoformat(timespec="seconds")

    start = time.perf_counter()
    time.sleep(1.2)
    output = f"[mock result] {task['task_type']}: {str(task['content'])[:60]}"
    duration_ms = (time.perf_counter() - start) * 1000

    with task_lock:
        task["status"] = "success"
        task["output"] = output
        task["duration_ms"] = round(duration_ms, 2)
        task["finished_at"] = datetime.now().isoformat(timespec="seconds")


@app.post("/ai-tasks", status_code=status.HTTP_201_CREATED)
def create_ai_task(
    data: AITaskCreate, background_tasks: BackgroundTasks
) -> dict[str, object]:
    task = {
        "id": len(ai_tasks) + 1,
        "task_type": data.task_type,
        "content": data.content,
        "status": "pending",
        "output": None,
        "duration_ms": None,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    ai_tasks.append(task)
    background_tasks.add_task(run_ai_task, task["id"])
    return {"message": "task created", "data": task}


@app.get("/ai-tasks")
def list_ai_tasks() -> dict[str, object]:
    return {"message": "success", "data": ai_tasks}


@app.get("/ai-tasks/{task_id}")
def get_ai_task(task_id: int) -> dict[str, object]:
    for task in ai_tasks:
        if task["id"] == task_id:
            return {"message": "success", "data": task}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
