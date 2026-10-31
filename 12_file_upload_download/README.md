# 12 — File Upload & Download

## Theory

**Uploading** uses `UploadFile`, not a raw `bytes` param — it streams the
file instead of loading it all into memory at once, and gives you
metadata (`filename`, `content_type`):

```python
from fastapi import File, UploadFile
from typing import Annotated

@app.post("/upload")
async def upload_file(file: Annotated[UploadFile, File(...)]):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}
```

Requires `python-multipart` installed (file uploads are sent as
`multipart/form-data`, not JSON).

**Never trust the client's filename directly** — a malicious filename
like `../../etc/passwd` could escape your intended directory (path
traversal). Always take just the final path component:

```python
from pathlib import Path

safe_name = Path(file.filename or "upload").name  # strips any directory parts
```

**Downloading** uses `FileResponse`:

```python
from fastapi.responses import FileResponse

@app.get("/files/{filename}")
def download(filename: str):
    safe_name = Path(filename).name  # sanitize here too — it's user input
    path = UPLOAD_DIR / safe_name
    if not path.exists():
        raise HTTPException(404, "File not found.")
    return FileResponse(path=path, filename=safe_name)
```

`FileResponse` streams the file efficiently and sets the right headers
(`Content-Disposition`, `Content-Type` guessed from the extension).

## Task

Open `starter.py`.

1. `POST /tasks/{task_id}/attachment` → protected (reuse `CurrentUserDep`
   pattern conceptually, but for this module a simple `require: str`
   query param check is fine — no need to redo full JWT auth here).
   Accept an `UploadFile`. Sanitize the filename with `Path(...).name`.
   Save it as `{task_id}_{filename}` under an `uploads/` directory
   (create it if missing). Return `{"filename": saved_name, "size_bytes": ...}`.
2. `GET /tasks/{task_id}/attachment/{filename}` → sanitize `filename`,
   404 if the file doesn't exist under `uploads/`, else return it via
   `FileResponse`.
3. Add a max-size guard: if the uploaded file is over 5 MB
   (`len(content) > 5 * 1024 * 1024`), raise `413` — there's no
   `status.HTTP_413_...` constant needed, just use `413` directly, or
   `status.HTTP_413_REQUEST_ENTITY_TOO_LARGE` if your FastAPI version has
   it.

Test by uploading a small text file via `/docs`, then downloading it back.
