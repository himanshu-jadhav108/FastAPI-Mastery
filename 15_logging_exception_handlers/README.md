# 15 — Logging & Custom Exception Handlers

## Theory

`print()` was fine for exercises; real apps use the `logging` module —
it gives you levels (DEBUG/INFO/WARNING/ERROR), timestamps, and the
ability to route output to files, external services, etc.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

logger.info("Server starting")
logger.warning("Deprecated endpoint called: %s", path)
logger.error("Failed to process task %s: %s", task_id, error)
```

Use `%s` placeholders (not f-strings) in logger calls — the string is
only formatted if that log level is actually enabled, which is slightly
more efficient and is the idiomatic style.

**Custom exception handlers** let you define what response an entire
*category* of exception produces, instead of writing the same
`try/except` in every route:

```python
class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id

@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    logger.warning("Task not found: %s", exc.task_id)
    return JSONResponse(
        status_code=404,
        content={"error": "task_not_found", "task_id": exc.task_id},
    )
```

Now any route can just `raise TaskNotFoundError(task_id)` and this
handler produces a consistent response shape everywhere — useful once
you have many endpoints that should all fail the same documented way.

You can also override the built-in handler for generic `Exception` to
guarantee no raw Python traceback ever leaks to a client in production:

```python
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled error at %s: %s", request.url.path, exc)
    return JSONResponse(status_code=500, content={"error": "internal_server_error"})
```

## Task

Open `starter.py`.

1. Configure `logging.basicConfig` as shown, get a module-level `logger`.
2. Define `TaskNotFoundError(Exception)` carrying `task_id`.
3. Register an `@app.exception_handler(TaskNotFoundError)` that logs a
   warning and returns a `404` `JSONResponse` with
   `{"error": "task_not_found", "task_id": ...}`.
4. `GET /tasks/{task_id}` → raise `TaskNotFoundError(task_id)` instead of
   `HTTPException` when missing (this is the payoff — cleaner route code).
5. Register an `@app.exception_handler(ValueError)` that logs the error
   and returns `400` with `{"error": "value_error", "detail": str(exc)}`.
6. `POST /tasks/{task_id}/divide` → query param `by: int`. If `by == 0`,
   `raise ValueError("Cannot divide by zero.")` — confirm your handler
   catches it instead of a raw 500.
