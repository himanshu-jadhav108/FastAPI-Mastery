# 01 — Basics: Your First App

## Theory

A FastAPI app starts with one object:

```python
from fastapi import FastAPI
app = FastAPI()
```

`app` is what Uvicorn runs. You attach endpoints to it with **decorators**
that name an HTTP method:

```python
@app.get("/")
def home():
    return {"message": "hello"}
```

- `@app.get(...)` → responds to HTTP GET requests at that path
- The function's **return value** is automatically converted to JSON
- FastAPI infers the response is JSON; you don't call `json.dumps` yourself

The four other common decorators: `@app.post`, `@app.put`, `@app.patch`,
`@app.delete`. Which one you use is a convention (not enforced by Python)
that signals intent:
- `GET` — read data, no side effects
- `POST` — create something new
- `PUT` — replace something entirely
- `PATCH` — partially update something
- `DELETE` — remove something

## Your project: Task Manager API

Starting now, you're building a Task Manager API. Tasks are stored in a
plain Python list for this module — no database yet (that comes in
module 06).

## Task

Open `starter.py`. Fill in the `TODO`s to create:

1. `GET /` → returns `{"message": "Task Manager API is running"}`
2. `GET /tasks` → returns the full `tasks` list
3. `POST /tasks` → for now, just returns `{"received": "ok"}` (we'll accept
   real data with Pydantic in module 03)
4. `GET /ping` → returns `{"pong": True}`

Run it and check all four routes work in `/docs` before opening
`solution.py`.
