"""
Module 12 — File Upload & Download
Run with: fastapi dev starter.py
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
    # TODO 1: sanitize the filename with Path(file.filename or "upload").name
    # TODO 2: read the file content with `await file.read()`
    # TODO 3: if len(content) > MAX_SIZE_BYTES, raise 413
    # TODO 4: build saved_name = f"{task_id}_{safe_name}"
    # TODO 5: write content to UPLOAD_DIR / saved_name using .write_bytes()
    # TODO 6: return {"filename": saved_name, "size_bytes": len(content)}
    ...


@app.get("/tasks/{task_id}/attachment/{filename}")
def download_attachment(task_id: int, filename: str):
    # TODO 7: sanitize filename with Path(filename).name
    # TODO 8: build the expected path: UPLOAD_DIR / f"{task_id}_{safe_name}"
    # TODO 9: 404 if it doesn't exist, else return FileResponse(path=..., filename=safe_name)
    ...
