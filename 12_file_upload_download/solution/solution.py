"""
Module 12 — File Upload & Download — SOLUTION
"""

from pathlib import Path
from typing import Annotated

from fastapi import File, HTTPException, FastAPI, UploadFile, status
from fastapi.responses import FileResponse

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


@app.post("/tasks/{task_id}/attachment")
async def upload_attachment(
    task_id: int,
    file: Annotated[UploadFile, File(...)],
):
    safe_name = Path(file.filename or "upload").name
    content = await file.read()

    if len(content) > MAX_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large (max 5 MB).",
        )

    saved_name = f"{task_id}_{safe_name}"
    (UPLOAD_DIR / saved_name).write_bytes(content)

    return {"filename": saved_name, "size_bytes": len(content)}


@app.get("/tasks/{task_id}/attachment/{filename}")
def download_attachment(task_id: int, filename: str):
    safe_name = Path(filename).name
    path = UPLOAD_DIR / f"{task_id}_{safe_name}"

    if not path.exists() or not path.is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found.")

    return FileResponse(path=path, filename=safe_name)
