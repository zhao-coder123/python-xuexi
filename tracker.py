"""
30 天 Python 学习进度追踪器
启动: python3 tracker.py
访问: http://localhost:8000
"""

from __future__ import annotations

import json
import os
import subprocess
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROGRESS_FILE = os.path.join(BASE_DIR, "progress.json")

app = FastAPI(title="30天Python学习进度追踪")


# ---------- 工具函数 ----------

def load_progress() -> dict:
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_progress(data: dict):
    # 重新计算统计
    total = 0
    done = 0
    for week in data.get("weeks", []):
        for item in week.get("deliverables", []):
            total += 1
            done += int(item["done"])
        for day in week.get("days", []):
            for sec in day.get("sections", []):
                for item in sec.get("items", []):
                    total += 1
                    done += int(item["done"])
        for item in week.get("review", []):
            total += 1
            done += int(item["done"])
    for extra in data.get("extras", []):
        for item in extra.get("items", []):
            total += 1
            done += int(item["done"])
        for sec in extra.get("sections", []):
            for item in sec.get("items", []):
                total += 1
                done += int(item["done"])
    data["stats"] = {"total": total, "done": done}

    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_and_update_item(data: dict, item_id: str, done: bool) -> bool:
    """在整个 JSON 树中查找 item 并更新状态"""
    for week in data.get("weeks", []):
        for item in week.get("deliverables", []):
            if item["id"] == item_id:
                item["done"] = done
                return True
        for day in week.get("days", []):
            for sec in day.get("sections", []):
                for item in sec.get("items", []):
                    if item["id"] == item_id:
                        item["done"] = done
                        return True
        for item in week.get("review", []):
            if item["id"] == item_id:
                item["done"] = done
                return True
    for extra in data.get("extras", []):
        for item in extra.get("items", []):
            if item["id"] == item_id:
                item["done"] = done
                return True
        for sec in extra.get("sections", []):
            for item in sec.get("items", []):
                if item["id"] == item_id:
                    item["done"] = done
                    return True
    return False


def get_day_info(data: dict, day_num: int) -> dict | None:
    for week in data.get("weeks", []):
        for day in week.get("days", []):
            if day.get("day") == day_num:
                return day
    return None


# ---------- 页面 ----------

@app.get("/")
async def index():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))


# ---------- API ----------

@app.get("/api/progress")
async def get_progress():
    return load_progress()


class ToggleRequest(BaseModel):
    done: bool


@app.patch("/api/progress/{item_id}")
async def toggle_item(item_id: str, req: ToggleRequest):
    data = load_progress()
    found = find_and_update_item(data, item_id, req.done)
    if not found:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    save_progress(data)
    return {"ok": True, "id": item_id, "done": req.done, "stats": data["stats"]}


class BatchToggleRequest(BaseModel):
    items: Dict[str, bool]  # { item_id: done }


@app.patch("/api/progress")
async def batch_toggle(req: BatchToggleRequest):
    data = load_progress()
    updated = []
    for item_id, done in req.items.items():
        if find_and_update_item(data, item_id, done):
            updated.append(item_id)
    save_progress(data)
    return {"ok": True, "updated": updated, "stats": data["stats"]}


class StartDayRequest(BaseModel):
    day: int


@app.post("/api/start-day")
async def start_day(req: StartDayRequest):
    data = load_progress()
    day_info = get_day_info(data, req.day)
    if not day_info:
        raise HTTPException(status_code=404, detail=f"Day {req.day} not found")

    branch_name = f"day{req.day:02d}"
    folder_path = os.path.join(BASE_DIR, f"day{req.day:02d}")

    # 创建 git 分支
    branch_result = subprocess.run(
        ["git", "checkout", "-b", branch_name],
        capture_output=True, text=True, cwd=BASE_DIR,
    )
    branch_created = branch_result.returncode == 0
    if not branch_created:
        # 分支已存在，尝试切换
        switch_result = subprocess.run(
            ["git", "checkout", branch_name],
            capture_output=True, text=True, cwd=BASE_DIR,
        )
        if switch_result.returncode != 0:
            raise HTTPException(
                status_code=400,
                detail=f"无法创建或切换到分支 {branch_name}: {switch_result.stderr}",
            )

    # 创建文件夹
    os.makedirs(folder_path, exist_ok=True)

    # 创建当天 README
    readme_path = os.path.join(folder_path, "README.md")
    if not os.path.exists(readme_path):
        lines = [f"# Day {req.day}: {day_info['title']}\n\n"]
        for sec in day_info.get("sections", []):
            lines.append(f"## {sec['title']}\n\n")
            for item in sec.get("items", []):
                lines.append(f"- [ ] {item['text']}\n")
            lines.append("\n")
        lines.append("## 笔记\n\n")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    # 创建空的 main.py
    main_py = os.path.join(folder_path, "main.py")
    if not os.path.exists(main_py):
        with open(main_py, "w", encoding="utf-8") as f:
            f.write(f'"""\nDay {req.day}: {day_info["title"]}\n"""\n')

    return {
        "ok": True,
        "branch": branch_name,
        "folder": f"day{req.day:02d}/",
        "branch_created": branch_created,
        "message": f"已{'创建' if branch_created else '切换到'}分支 {branch_name}，文件夹 day{req.day:02d}/ 已就绪",
    }


@app.get("/api/current-branch")
async def current_branch():
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True, text=True, cwd=BASE_DIR,
    )
    return {"branch": result.stdout.strip()}


if __name__ == "__main__":
    import uvicorn

    print("=" * 50)
    print("  30天 Python 学习进度追踪器")
    print("  访问 http://localhost:8000")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)
