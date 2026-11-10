<div align="center">

# 📁 Module 12: File Uploads, Downloads & Path Sanitization

[![Level](https://img.shields.io/badge/Level-Intermediate-blue?style=for-the-badge)](#)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)](#)

[⏮️ Previous: 11 Background Tasks](../11_background_tasks/README.md) • [📚 Course Overview](../README.md) • [Next: 13 WebSockets ⏭️](../13_websockets/README.md)

---

</div>

## 📌 Architectural Overview

Handling file attachments requires specialized memory management and strict security controls. Reading files entirely into memory as raw `bytes` risks crashing server worker processes during concurrent large uploads.

FastAPI provides `UploadFile`, a streaming abstraction backed by Spooled Temporary Files that buffers small files in memory and seamlessly rolls larger files onto disk.

```
                           +--------------------------------+
                           |   Multipart Form HTTP Request  |
                           +--------------------------------+
                                           |
                                           v
                           +--------------------------------+
                           |  UploadFile Streaming Buffer   |
                           +--------------------------------+
                                           |
                                           v
       +------------------------------------------------------------------------+
       |                         Security Checks & Storage                      |
       |                                                                        |
       |  [Path Traversal Defense: Path.name]  --->  [File Size Guard (5MB MAX)]|
       +------------------------------------------------------------------------+
                                           |
                                           v
                           +--------------------------------+
                           |   Persistent Storage (uploads/) |
                           +--------------------------------+
```

---

## 💡 Core Theoretical Concepts

### 1. `UploadFile` vs Raw `bytes`

| Feature | `UploadFile` | `bytes` |
| :--- | :--- | :--- |
| **Memory Strategy** | Spooled temporary file (streams to disk) | Loads entire payload directly into RAM |
| **File Metadata** | Provides `filename`, `content_type`, headers | None |
| **Methods** | Async `.read()`, `.write()`, `.seek()`, `.close()` | Synchronous in-memory byte slice |

```python
from fastapi import File, UploadFile
from typing import Annotated

@app.post("/upload")
async def handle_upload(file: Annotated[UploadFile, File(...)]):
    content = await file.read()
    return {"filename": file.filename, "size_bytes": len(content)}
```

### 2. Path Traversal Security Defense

> [!CAUTION]
> **Severe Vulnerability**: Never trust client-provided filenames! A malicious client could send `filename="../../etc/shadow"` or `../../app/main.py` to overwrite critical host files.
> Always sanitize the filename by extracting solely the leaf component:

```python
from pathlib import Path

# Strips any directory traversals (e.g. "../../virus.exe" becomes "virus.exe")
safe_filename = Path(file.filename or "upload.bin").name
destination_path = UPLOAD_DIR / f"{task_id}_{safe_filename}"
```

### 3. High-Performance File Downloads with `FileResponse`

FastAPI’s `FileResponse` streams files in chunks with proper HTTP headers (`Content-Disposition`, `Content-Length`, `Content-Type`):

```python
from fastapi.responses import FileResponse

@app.get("/files/{filename}")
def download_file(filename: str):
    safe_name = Path(filename).name
    file_path = UPLOAD_DIR / safe_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename=safe_name)
```

---

## 🎯 Task Specifications

Enhance `question/starter.py` to allow users to attach documents and images to tasks.

### Route Contract

| Method | Path | Request Format | Success Code | Description |
| :--- | :--- | :--- | :---: | :--- |
| `POST` | `/tasks/{task_id}/attachment` | `multipart/form-data` | `201 Created` | Validates file size (≤ 5MB), sanitizes filename, saves to `uploads/` directory |
| `GET` | `/tasks/{task_id}/attachment/{filename}` | None | `200 OK` | Streams saved file back via `FileResponse` (404 if missing) |

---

## 🛠️ Step-by-Step Implementation

1. Open `question/starter.py`.
2. Define `UPLOAD_DIR = Path("uploads")` and ensure the folder is created automatically (`UPLOAD_DIR.mkdir(exist_ok=True)`).
3. In `POST /tasks/{task_id}/attachment`:
   - Sanitize `file.filename` using `Path(...).name`.
   - Read content and enforce a 5 MB limit (`5 * 1024 * 1024` bytes). Raise `413 Request Entity Too Large` if violated.
   - Write file content to disk as `{task_id}_{safe_filename}`.
4. In `GET /tasks/{task_id}/attachment/{filename}`:
   - Verify file existence under `uploads/` and return `FileResponse`.

---

## 🧪 Verification Commands

```bash
# 1. Create a dummy test file
echo "Task documentation notes" > test_note.txt

# 2. Upload file attachment
curl -X POST http://127.0.0.1:8000/tasks/1/attachment \
  -F "file=@test_note.txt"

# 3. Download the attached file
curl -O http://127.0.0.1:8000/tasks/1/attachment/1_test_note.txt
```

---

<div align="center">

[⏮️ Previous: 11 Background Tasks](../11_background_tasks/README.md) • [📚 Course Overview](../README.md) • [Next: 13 WebSockets ⏭️](../13_websockets/README.md)

</div>
