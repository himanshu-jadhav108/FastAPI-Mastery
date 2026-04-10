# FastAPI: Zero to Production

A hands-on FastAPI course, organized as one folder per topic. Every module
follows the same pattern and every module builds the **same app** —
a Task Manager API — a little further than the last one.

## How each module works

```
NN_topic_name/
  README.md        <- theory (short) + what you'll build + the task
  starter.py        <- code with # TODO markers for you to fill in
  solution.py        <- reference answer, don't open until you've tried
  test_it.py          <- (from module 07 onward) quick checks you can run
```

**Workflow for every module:**
1. Read `README.md` — theory first, then the task.
2. Open `starter.py`, fill in the `TODO`s.
3. Run it (`fastapi dev starter.py` or `uvicorn starter:app --reload`) and
   test it at `http://127.0.0.1:8000/docs`.
4. Compare against `solution.py` only after you've genuinely tried.
5. Move to the next numbered folder — later modules assume you completed
   earlier ones, since the app grows incrementally.

## The running project: Task Manager API

Starting in module 01 you build a simple `/tasks` API. By module 21 it has:
users, auth, roles, a real async Postgres-ready database layer, migrations,
routers split by feature, background jobs, file attachments, websocket
notifications, tests, environment-based settings, and a production
deployment setup.

## Path

| # | Module | Level |
|---|--------|-------|
| 00 | Setup & tooling | — |
| 01 | Basics — your first app | Beginner |
| 02 | Routing, path & query params | Beginner |
| 03 | Pydantic models & validation | Beginner |
| 04 | Error handling (HTTPException) | Beginner |
| 05 | Dependency Injection | Beginner→Intermediate |
| 06 | Database with SQLModel | Intermediate |
| 07 | CRUD + pagination/filtering | Intermediate |
| 08 | Auth — OAuth2 + JWT | Intermediate |
| 09 | Role-based authorization | Intermediate |
| 10 | Middleware & CORS | Intermediate |
| 11 | Background tasks | Intermediate |
| 12 | File upload/download | Intermediate |
| 13 | WebSockets | Intermediate |
| 14 | Lifespan events | Intermediate |
| 15 | Logging & custom exception handlers | Intermediate |
| 16 | Routers & project structure | Advanced |
| 17 | Async database (SQLAlchemy async + asyncpg) | Advanced |
| 18 | Migrations with Alembic | Advanced |
| 19 | Settings management (pydantic-settings) | Advanced |
| 20 | Testing (pytest + TestClient) | Advanced |
| 21 | Deployment & production concerns | Advanced |

## Install once

```bash
pip install fastapi "uvicorn[standard]" sqlmodel pyjwt "pwdlib[argon2]" \
    python-multipart sqlalchemy[asyncio] asyncpg aiosqlite alembic \
    pydantic-settings pytest httpx
```

Start each module with:
```bash
cd 01_basics
fastapi dev starter.py
```

Go in order. Good luck.
