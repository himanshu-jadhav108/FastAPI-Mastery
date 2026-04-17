# 07 — Full CRUD + Pagination & Filtering

## Theory

CRUD = Create, Read, Update, Delete. You've built pieces of this already;
this module assembles the complete, production-shaped set for one
resource, plus real pagination/filtering against the database (not a
Python list slice).

**Separating schemas from the table model** (recap from module 03, now
applied to SQLModel): even though `Task` the table model *could* be used
directly as a request/response body, real projects split them:

```python
class TaskBase(SQLModel):
    title: str
    priority: int = 3
    done: bool = False

class Task(TaskBase, table=True):
    id: int | None = SQLField(default=None, primary_key=True)

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int

class TaskUpdate(SQLModel):
    title: str | None = None
    priority: int | None = None
    done: bool | None = None
```

This means a client can never set `id` on create, and `TaskUpdate` fields
are all optional for partial updates.

**Filtering + pagination with SQL**, instead of slicing a Python list:

```python
statement = select(Task)
if done is not None:
    statement = statement.where(Task.done == done)
statement = statement.offset(skip).limit(limit)
results = session.exec(statement).all()
```

Building the `statement` up conditionally, then executing it once, is the
standard pattern — it lets the database do the filtering (fast, scales)
instead of Python (loads everything into memory first).

## Task

Open `starter.py` (this module switches to a fresh `tasks.db`).

1. Define `TaskBase`, `Task(TaskBase, table=True)`, `TaskCreate`,
   `TaskRead`, `TaskUpdate` as shown above.
2. `POST /tasks` → `response_model=TaskRead`, 201.
3. `GET /tasks` → query params `done: bool | None`, `skip: int = 0`,
   `limit: int = Query(default=10, ge=1, le=100)`. Build the `statement`
   conditionally as shown. `response_model=list[TaskRead]`.
4. `GET /tasks/{task_id}` → 404 if missing.
5. `PATCH /tasks/{task_id}` → partial update using
   `update.model_dump(exclude_unset=True)`, then
   `session.add`/`commit`/`refresh`. 404 if missing.
6. `DELETE /tasks/{task_id}` → `session.delete(task)`, `session.commit()`.
   404 if missing. Return `{"deleted": task_id}`.

Test the full lifecycle in `/docs`: create 5 tasks, filter by `done`,
paginate with `skip`/`limit`, patch one, delete one.
