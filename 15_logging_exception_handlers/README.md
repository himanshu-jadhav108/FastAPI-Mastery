<div align="center">

# 📝 Module 15: Structured Logging & Custom Exception Handlers

[![Level](https://img.shields.io/badge/Level-Intermediate-blue?style=for-the-badge)](#)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)](#)

[⏮️ Previous: 14 Lifespan Events](../14_lifespan_events/README.md) • [📚 Course Overview](../README.md) • [Next: 16 Routers & Project Structure ⏭️](../16_routers_project_structure/README.md)

---

</div>

## 📌 Architectural Overview

Ad-hoc `print()` statements are unacceptable in production systems: they lack timestamps, cannot be routed to observability backends (Datadog, CloudWatch, Loki), and leak sensitive stack traces to users on uncaught errors.

This module introduces two critical operational patterns:
1. **Standardized Python Structured Logging**: Tiered severity levels with consistent formatting.
2. **Centralized Domain Exception Handlers**: Intercepting business exceptions at the framework boundary to transform domain errors into uniform JSON contracts.

```
       [Route Handler]
              │
              ▼ raises
       [TaskNotFoundError(task_id=42)]
              │
              ▼ intercepted by
       [@app.exception_handler(TaskNotFoundError)]
              │
              ├─► [Log structured warning to logger]
              └─► [Return uniform JSONResponse(status_code=404)]
```

---

## 💡 Core Theoretical Concepts

### 1. Python Standard Library `logging` Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# Idiomatic logging uses format parameters, not f-strings:
logger.info("Processing task id: %s", task_id)
```

### 2. Custom Domain Exception Handlers

Instead of littering route handlers with repetitive `try/except` and `HTTPException` raises, create expressive domain exceptions and register handlers:

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id

@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    logger.warning("Resource lookup failed for task_id: %s on path: %s", exc.task_id, request.url.path)
    return JSONResponse(
        status_code=404,
        content={"error": "task_not_found", "message": f"Task with id {exc.task_id} does not exist."},
    )
```

### 3. Global Exception Sanitization (Traceback Leak Prevention)

> [!WARNING]
> Uncaught exceptions default to returning an ugly 500 error page that can expose server file structures, secret keys, or Python package versions. Catch generic exceptions to sanitize outgoing responses:

```python
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.critical("Unhandled critical failure on %s: %s", request.url.path, exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "message": "An unexpected error occurred. Please contact support."},
    )
```

---

## 🎯 Task Specifications

Update `question/starter.py` with structured logging and domain exception interception.

### Requirements

1. Configure `logging.basicConfig` with a custom formatter and instantiate `logger`.
2. Define `TaskNotFoundError(Exception)` carrying `task_id`.
3. Register `@app.exception_handler(TaskNotFoundError)` returning `404` JSON with `{"error": "task_not_found", "task_id": ...}`.
4. Replace `HTTPException(404)` in `GET /tasks/{task_id}` with `raise TaskNotFoundError(task_id)`.
5. Register `@app.exception_handler(ValueError)` returning `400` JSON.
6. Build `POST /tasks/{task_id}/divide?by=int` that raises `ValueError("Cannot divide by zero")` if `by == 0`, and verify the clean 400 response.

---

## 🛠️ Step-by-Step Implementation

1. Open `question/starter.py`.
2. Set up `logging` configuration and module logger.
3. Declare custom `TaskNotFoundError` class.
4. Wire the exception handlers using `@app.exception_handler()`.
5. Refactor route logic to raise domain exceptions.
6. Verify via terminal logs and Swagger UI.

---

## 🧪 Verification Commands

```bash
# 1. Trigger custom TaskNotFoundError handler
curl -X GET http://127.0.0.1:8000/tasks/999

# Response:
# {"error": "task_not_found", "task_id": 999}

# 2. Trigger ValueError handler (Division by Zero)
curl -X POST "http://127.0.0.1:8000/tasks/1/divide?by=0"

# Response:
# {"error": "value_error", "detail": "Cannot divide by zero."}
```

---

<div align="center">

[⏮️ Previous: 14 Lifespan Events](../14_lifespan_events/README.md) • [📚 Course Overview](../README.md) • [Next: 16 Routers & Project Structure ⏭️](../16_routers_project_structure/README.md)

</div>
