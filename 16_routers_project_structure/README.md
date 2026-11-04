# 16 — Routers & Project Structure

## Theory

Every module so far has been one file. Real projects split by feature
using `APIRouter` — a "mini FastAPI app" you build separately and plug
into the main app.

```python
# routers/tasks.py
from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
def list_tasks():
    ...

@router.get("/{task_id}")
def get_task(task_id: int):
    ...
```

```python
# main.py
from fastapi import FastAPI
from routers import tasks, auth, users

app = FastAPI()
app.include_router(tasks.router)
app.include_router(auth.router)
app.include_router(users.router)
```

- `prefix="/tasks"` — every route in this router is automatically under
  `/tasks`, so `@router.get("/")` becomes `GET /tasks/` and
  `@router.get("/{task_id}")` becomes `GET /tasks/{task_id}`
- `tags=["tasks"]` — groups these routes together in the `/docs` UI
- Routers can take their own `dependencies=[Depends(...)]` that apply to
  every route inside them — e.g. requiring auth for a whole router at once

## A conventional layout

```
app/
  main.py              # creates FastAPI(), includes routers
  database.py           # engine, get_session
  models.py              # SQLModel table models
  schemas.py               # Pydantic request/response schemas
  security.py                # password hashing, JWT
  dependencies.py               # get_current_user, require_role, etc.
  routers/
    __init__.py
    auth.py
    users.py
    tasks.py
```

This module gives you that layout already scaffolded under
`project/app/` with everything from modules 06-09 (database, auth,
tasks) working — but split into files instead of stuffed in one.

## Task

Open `project/app/`. The files are mostly complete but have TODOs where
router wiring is missing:

1. `project/app/routers/tasks.py` — TODO: create the `APIRouter` with
   `prefix="/tasks"` and `tags=["tasks"]`, and change every
   `@app.get(...)` etc. in this file to `@router.get(...)`.
2. `project/app/routers/auth.py` — same, `prefix="/auth"`,
   `tags=["auth"]`.
3. `project/app/main.py` — TODO: import both routers and
   `app.include_router(...)` each one.
4. Run it from inside `project/`: `fastapi dev app/main.py`. Confirm
   `/docs` still shows all routes grouped by tag, and everything from
   modules 08/09 still works end to end (register, login, create task).

This is the last module using SQLModel's sync engine — module 17 swaps
this exact project to an async database layer.
