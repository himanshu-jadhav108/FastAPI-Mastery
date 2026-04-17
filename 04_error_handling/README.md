# 04 — Error Handling with HTTPException

## Theory

`HTTPException` is how you deliberately stop a request and return an
error status + message:

```python
from fastapi import HTTPException, status

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )
    return task
```

Raising it immediately halts the function and sends:
```json
{"detail": "Task not found."}
```
with the given status code. Use `status.HTTP_xxx` constants instead of raw
numbers — they're more readable and you get autocomplete.

**Status codes you'll use constantly:**

| Code | Meaning | When |
|---|---|---|
| 200 | OK | successful GET/PUT/PATCH |
| 201 | Created | successful POST that creates something |
| 400 | Bad Request | malformed input the client should fix |
| 401 | Unauthorized | not authenticated (missing/invalid credentials) |
| 403 | Forbidden | authenticated, but not allowed |
| 404 | Not Found | resource doesn't exist |
| 409 | Conflict | e.g. duplicate unique field |
| 422 | Unprocessable Entity | Pydantic validation failure (automatic) |
| 500 | Server Error | uncaught bug — you want to avoid these on purpose |

## Task

Rewrite `starter.py` (carried over from module 03) so that:

1. `GET /tasks/{task_id}` → raises `404` with detail `"Task not found."`
   if no task has that id.
2. `DELETE /tasks/{task_id}` → raises `404` the same way if nothing was
   deleted.
3. `POST /tasks` → raises `409 Conflict` with detail
   `"A task with this title already exists."` if a task with the same
   title (case-insensitive) already exists.
4. `PATCH /tasks/{task_id}` → new endpoint. Accepts a `TaskUpdate` model
   where every field is optional. Raises `404` if not found. Updates only
   the fields the client actually sent (hint: `.model_dump(exclude_unset=True)`).
