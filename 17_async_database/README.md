# 17 — Async Database (SQLAlchemy Async + asyncpg)

## Theory

Every module so far used SQLModel's **sync** engine — each database call
blocks the worker thread. FastAPI handles this fine at moderate scale
(it runs sync route functions in a thread pool automatically), but at
higher concurrency, a true **async** database layer lets a single worker
handle far more simultaneous requests, since the event loop can serve
another request while waiting on I/O instead of blocking a thread.

**Async engine + session:**

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession  # NOT sqlalchemy's AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///./tasks_async.db"
# Production Postgres would be:
# DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=False)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session
```

**Import gotcha:** use `sqlmodel.ext.asyncio.session.AsyncSession`, not
`sqlalchemy.ext.asyncio.AsyncSession`. Plain SQLAlchemy's `AsyncSession`
doesn't have `.exec()` — only SQLModel's subclass does. Mixing them up
gives `AttributeError: 'AsyncSession' object has no attribute 'exec'`.

Note the driver prefix: `sqlite+aiosqlite://` and `postgresql+asyncpg://`
— the part after `+` names the async driver library.

**Every database call becomes `await`-ed**, and route functions become
`async def`:

```python
from sqlmodel import select

@app.post("/tasks", response_model=TaskRead)
async def create_task(task: TaskCreate, session: SessionDep):
    new_task = Task(**task.model_dump())
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task

@app.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, session: SessionDep):
    task = await session.get(Task, task_id)
    ...

@app.get("/tasks", response_model=list[TaskRead])
async def list_tasks(session: SessionDep):
    result = await session.exec(select(Task))
    return result.all()
```

**Table creation is also async:**

```python
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

`run_sync` is needed because `create_all` itself is a sync SQLAlchemy
function — this bridges it onto the async connection.

**When to actually reach for this:** if your app is I/O-heavy and needs
high concurrency (many simultaneous slow requests — calling other APIs,
etc.), async is a real win. For most CRUD apps at moderate traffic, the
sync SQLModel pattern from earlier modules is simpler and completely
fine. Don't reach for async DB just because it's "more advanced" —
reach for it when you have a concrete concurrency need.

## Task

Open `starter.py`. It's the module 07 CRUD app, ported to need async.

1. Set `DATABASE_URL = "sqlite+aiosqlite:///./tasks_async.db"`,
   `engine = create_async_engine(...)`.
2. Write `async def create_db_and_tables()` using `conn.run_sync(...)` as
   shown, and call it inside an async `lifespan` (combine with what you
   learned in module 14).
3. Write `async def get_session()` yielding an `AsyncSession`, and
   `SessionDep`.
4. Convert every route to `async def` and `await` every database
   operation: `session.add` stays sync (no await), but `commit`,
   `refresh`, `get`, and `exec` all need `await`. `session.exec(...)`
   returns a result object — call `.all()` on it (not awaited itself, the
   `exec` call is what's awaited).
5. Run it and confirm full CRUD still works via `/docs`.
