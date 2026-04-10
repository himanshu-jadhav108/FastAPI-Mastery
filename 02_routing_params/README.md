# 02 — Path Parameters & Query Parameters

## Theory

**Path parameters** are part of the URL itself and are always required:

```python
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    ...
```

`{task_id}` in the path must match a parameter name in the function.
FastAPI reads the type hint (`int`) and:
- converts the URL string to an `int`
- returns a `422 Unprocessable Entity` automatically if conversion fails

**Query parameters** are anything *not* in the path — they come from
`?key=value` in the URL, and are just regular function parameters with
default values:

```python
@app.get("/tasks")
def list_tasks(done: bool | None = None, limit: int = 10):
    ...
```

Call this as `/tasks?done=true&limit=5`. Parameters with a default value
are optional; parameters with no default are required.

For extra validation on query params (min/max, length, regex) use `Query`:

```python
from fastapi import Query

def list_tasks(limit: int = Query(default=10, ge=1, le=100)):
    ...
```

`ge`/`le` = greater-or-equal / less-or-equal. This makes `/tasks?limit=500`
return a `422` instead of silently accepting it.

## Task

Extend the Task Manager. Open `starter.py`.

1. Give each task a unique `id` (int) — the seed data already has this.
2. `GET /tasks/{task_id}` → return the matching task, or raise a `404`-style
   dict for now (`{"error": "not found"}`) — real `HTTPException` comes in
   module 04.
3. `GET /tasks` → accept two **optional** query params:
   - `done: bool | None` — if provided, filter tasks by their `done` status
   - `limit: int` — default `10`, must be between `1` and `100` (use `Query`)
4. `DELETE /tasks/{task_id}` → remove the task with that id from the list,
   return `{"deleted": task_id}`

Test in `/docs`: try `/tasks?done=true`, `/tasks?limit=500` (should 422),
and a `task_id` that doesn't exist.
