# 03 — Pydantic Models & Validation

## Theory

So far, `POST` endpoints haven't accepted real data. A **request body** is
JSON sent by the client, and FastAPI parses it using a Pydantic model:

```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    priority: int = Field(default=1, ge=1, le=5)

@app.post("/tasks")
def create_task(task: TaskCreate):
    ...
```

When a client `POST`s JSON, FastAPI:
1. Parses the JSON body
2. Validates it against `TaskCreate`
3. If invalid → returns `422` with a detailed error, your function never runs
4. If valid → `task` is a real `TaskCreate` **object** — `task.title` etc.

**Why separate "create" schemas from your internal data?** A client
shouldn't be able to set a task's `id` or `created_at` — those are decided
by the server. So `TaskCreate` (what the client sends) is a different
shape than the full `Task` (what you store/return).

**Custom validators** run extra logic beyond type + range checks:

```python
from pydantic import field_validator

class TaskCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Title cannot be blank or whitespace.")
        return value.strip()
```

**`response_model`** does the same validation in reverse — it controls
exactly what shape gets sent back to the client, even if your Python
object has extra fields:

```python
@app.post("/tasks", response_model=TaskRead)
def create_task(task: TaskCreate):
    ...
```

## Task

Open `starter.py`.

1. Define `TaskCreate` (input schema): `title: str` (1-100 chars),
   `priority: int` (1-5, default 3), `done: bool = False`.
2. Add a `field_validator` on `title` that strips whitespace and rejects
   blank titles.
3. Define `TaskRead` (output schema): everything in `TaskCreate` plus
   `id: int`.
4. `POST /tasks` → accepts a `TaskCreate` body, assigns the next id,
   stores it, returns it with `response_model=TaskRead` and status `201`.
5. `GET /tasks` → `response_model=list[TaskRead]`.

Test: try posting a task with a blank title and confirm you get a `422`.
