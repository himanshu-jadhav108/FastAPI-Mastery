<div align="center">

# ⚡ Module 17: High-Concurrency Async Database Layer

[![Level](https://img.shields.io/badge/Level-Advanced-red?style=for-the-badge)](#)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)](#)

[⏮️ Previous: 16 Routers & Project Structure](../16_routers_project_structure/README.md) • [📚 Course Overview](../README.md) • [Next: 18 Migrations with Alembic ⏭️](../18_migrations_alembic/README.md)

---

</div>

## 📌 Architectural Overview

Until now, our database layer used synchronous drivers. In synchronous execution, while the database query executes over the network or disk, the underlying Python worker thread is **blocked** waiting on I/O.

By adopting a truly **asynchronous database layer** (SQLAlchemy 2.0 Async Engine + `aiosqlite` / `asyncpg`), the single-threaded ASGI event loop yields execution while waiting on database queries, enabling a single worker to effortlessly handle thousands of concurrent requests.

```
Synchronous I/O (Thread-Blocking):
Request A ──► [Wait on DB I/O (Thread Blocked)] ──► Response A
                                                     Request B ──► [Wait...]

Asynchronous Non-Blocking I/O (Event Loop):
Request A ──► [Await DB I/O] ── (Event Loop serves Request B) ──► Response A
               Request B ──► [Await DB I/O] ────────────────────► Response B
```

---

## 💡 Core Theoretical Concepts

### 1. Creating the Async Engine & Session

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated
from fastapi import Depends

DATABASE_URL = "sqlite+aiosqlite:///./tasks_async.db"
# In production PostgreSQL:
# DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/production_db"

engine = create_async_engine(DATABASE_URL, echo=False)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
```

> [!IMPORTANT]
> **Critical Import Gotcha**: Always import `AsyncSession` from `sqlmodel.ext.asyncio.session`, **NOT** from `sqlalchemy.ext.asyncio`. Plain SQLAlchemy’s `AsyncSession` lacks the `.exec()` helper method required by SQLModel queries!

### 2. Async Query Syntax Patterns

Every database I/O operation must be `await`-ed, and route handlers must be declared with `async def`:

```python
# 1. Fetch by Primary Key
task = await session.get(Task, task_id)

# 2. Execute Query
statement = select(Task).where(Task.done == False)
result = await session.exec(statement)
tasks = result.all()

# 3. Insert / Mutate
session.add(new_task) # session.add remains synchronous (in-memory staging)
await session.commit()
await session.refresh(new_task)
```

### 3. Async Table Creation via `run_sync` in Lifespan

Because `SQLModel.metadata.create_all` is inherently synchronous, use `conn.run_sync` inside your async lifespan startup:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    await engine.dispose()
```

---

## 🎯 Task Specifications

Port the synchronous CRUD application in `question/starter.py` to a non-blocking asynchronous pipeline.

### Requirements

1. Configure `DATABASE_URL = "sqlite+aiosqlite:///./tasks_async.db"`.
2. Construct `create_async_engine(DATABASE_URL)`.
3. Build `async def get_session()` yielding `AsyncSession`.
4. Migrate table initialization into an `asynccontextmanager` lifespan using `conn.run_sync()`.
5. Convert all route operations (`POST`, `GET`, `PATCH`, `DELETE`) to `async def` and `await` all session interactions.

---

## 🛠️ Step-by-Step Implementation

1. Open `question/starter.py`.
2. Update imports to include `create_async_engine` and `sqlmodel.ext.asyncio.session.AsyncSession`.
3. Construct the async engine and lifespan context manager.
4. Refactor endpoints to `async def` and apply `await` to `commit`, `refresh`, `get`, and `exec`.
5. Run tests and verify performance!

---

## 🧪 Verification Commands

```bash
# Launch the async application
fastapi dev question/starter.py

# Execute full CRUD suite asynchronously
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test async performance", "priority": 5}'

curl -X GET http://127.0.0.1:8000/tasks
```

---

<div align="center">

[⏮️ Previous: 16 Routers & Project Structure](../16_routers_project_structure/README.md) • [📚 Course Overview](../README.md) • [Next: 18 Migrations with Alembic ⏭️](../18_migrations_alembic/README.md)

</div>
