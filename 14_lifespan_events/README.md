# 14 — Lifespan Events

## Theory

You've been calling `SQLModel.metadata.create_all(engine)` at import time
in earlier modules — that "works" but it's the wrong place for startup
logic. FastAPI has a proper mechanism: **lifespan**.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- STARTUP: runs once, before the app accepts requests ----
    print("Starting up...")
    create_db_and_tables()

    yield  # <-- the app runs here, handling requests

    # ---- SHUTDOWN: runs once, after the app stops accepting requests ----
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)
```

Everything before `yield` runs once at startup. Everything after `yield`
runs once at shutdown (e.g. closing a connection pool, flushing logs,
releasing external resources). This replaces the older `@app.on_event
("startup")` / `@app.on_event("shutdown")` decorators, which are
deprecated.

**Sharing startup-created resources with routes** — attach them to
`app.state`:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.start_time = datetime.now(timezone.utc)
    yield

@app.get("/uptime")
def uptime(request: Request):
    delta = datetime.now(timezone.utc) - request.app.state.start_time
    return {"uptime_seconds": delta.total_seconds()}
```

## Task

Open `starter.py`.

1. Write a `lifespan` function that:
   - on startup: calls `create_db_and_tables()`, logs
     `"Starting Task Manager API..."`, and stores
     `app.state.start_time = datetime.now(timezone.utc)`
   - on shutdown: logs `"Shutting down Task Manager API..."`
2. Pass `lifespan=lifespan` into `FastAPI(...)`.
3. `GET /health` → return `{"status": "ok"}` — you'll expand this in
   module 15/21.
4. `GET /uptime` → use `request: Request` to reach `request.app.state
   .start_time`, return `{"uptime_seconds": <float>}`.

Restart the server and confirm the startup/shutdown log lines print at
the right times (Ctrl+C to see the shutdown line).
