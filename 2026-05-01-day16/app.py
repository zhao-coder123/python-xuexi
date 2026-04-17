"""Day 16: 文件上传示例。"""

from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile, status


app = FastAPI(
    title="Day 16 Upload Demo",
    description="用于学习 Multipart 上传、文件存储和元数据记录。",
    version="0.1.0",
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

fake_files_db = []
ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "application/pdf"}


@app.post("/files/upload", summary="上传文件")
async def upload_file(file: UploadFile = File(...)) -> dict[str, object]:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="不支持的文件类型"
        )

    file_ext = Path(file.filename or "").suffix
    saved_name = f"{uuid4().hex}{file_ext}"
    target_path = UPLOAD_DIR / saved_name

    content = await file.read()
    target_path.write_bytes(content)

    file_record = {
        "id": len(fake_files_db) + 1,
        "original_name": file.filename,
        "saved_name": saved_name,
        "content_type": file.content_type,
        "size": len(content),
        "path": str(target_path),
    }
    fake_files_db.append(file_record)

    return {"message": "upload success", "data": file_record}


@app.get("/files", summary="文件列表")
def list_files() -> dict[str, object]:
    return {"message": "success", "data": fake_files_db}
