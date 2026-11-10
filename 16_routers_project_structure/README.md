<div align="center">

# 🏛️ Module 16: Routers & Clean Architecture Project Structure

[![Level](https://img.shields.io/badge/Level-Advanced-red?style=for-the-badge)](#)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)](#)

[⏮️ Previous: 15 Logging & Exception Handlers](../15_logging_exception_handlers/README.md) • [📚 Course Overview](../README.md) • [Next: 17 Async Database ⏭️](../17_async_database/README.md)

---

</div>

## 📌 Architectural Overview

Monolithic single-file applications (`main.py` containing 1000+ lines) become unmaintainable as projects scale. Real-world microservices are structured into feature-sliced modules using **`APIRouter`**.

An `APIRouter` operates as an independent "miniature FastAPI application" that groups related endpoints, schemas, and dependencies, and mounts seamlessly onto the central root application.

```
                           +--------------------------------+
                           |          app/main.py           |
                           |       (Root FastAPI App)       |
                           +--------------------------------+
                                     /             \
                   include_router() /               \ include_router()
                                   v                 v
            +---------------------------+   +---------------------------+
            |      routers/auth.py      |   |      routers/tasks.py     |
            |  prefix: "/auth"          |   |  prefix: "/tasks"         |
            |  tags: ["Authentication"] |   |  tags: ["Tasks"]          |
            +---------------------------+   +---------------------------+
```

---

## 💡 Core Theoretical Concepts

### 1. The `APIRouter` Primitives

```python
# app/routers/tasks.py
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    dependencies=[Depends(verify_active_session)], # Applied to all routes in router
)

@router.get("/")
def list_tasks():
    ...
```

- `prefix="/tasks"`: Automatically prefixes every route defined on this router (`GET /tasks/`, `GET /tasks/{id}`).
- `tags=["Tasks"]`: Groups and organizes all endpoints under a dedicated collapsable section in the interactive `/docs` UI.
- `dependencies`: Router-level dependencies execute on _every_ request hitting this router (e.g. enforcing authentication across an entire domain).

### 2. Industry Standard Clean Project Layout

```
project/app/
├── __init__.py
├── main.py              # Root FastAPI instance & router registration
├── database.py          # Engine creation, metadata, and SessionDep
├── models.py            # SQLModel table definitions (DB entities)
├── schemas.py           # Pydantic request/response validation schemas
├── security.py          # Password hashing (Argon2) and JWT generation
├── dependencies.py      # Auth dependencies (get_current_user, require_role)
└── routers/
    ├── __init__.py
    ├── auth.py          # Login, registration, token issuance
    └── tasks.py         # Full CRUD task operations
```

---

## 🎯 Task Specifications

Open the scaffolded application in `project/app/` and assemble the modular system.

### Wiring Requirements

1. **`project/app/routers/tasks.py`**:
   - Instantiate `router = APIRouter(prefix="/tasks", tags=["tasks"])`.
   - Switch route decorators from `@app` to `@router`.
2. **`project/app/routers/auth.py`**:
   - Instantiate `router = APIRouter(prefix="/auth", tags=["auth"])`.
   - Switch route decorators to `@router`.
3. **`project/app/main.py`**:
   - Import `auth` and `tasks` routers.
   - Register them via `app.include_router(auth.router)` and `app.include_router(tasks.router)`.
4. Run the project from inside `project/` with `fastapi dev app/main.py`.

---

## 🛠️ Step-by-Step Implementation

1. Navigate into `project/`.
2. Update `app/routers/tasks.py` with `APIRouter` declaration.
3. Update `app/routers/auth.py` with `APIRouter` declaration.
4. Mount both routers inside `app/main.py`.
5. Verify in Swagger UI that all routes are grouped by their respective tags (`auth` and `tasks`).

---

## 🧪 Verification Commands

```bash
cd project

# Run the modular application
fastapi dev app/main.py

# Query modular endpoints
curl -X GET http://127.0.0.1:8000/tasks/
curl -X GET http://127.0.0.1:8000/docs
```

---

<div align="center">

[⏮️ Previous: 15 Logging & Exception Handlers](../15_logging_exception_handlers/README.md) • [📚 Course Overview](../README.md) • [Next: 17 Async Database ⏭️](../17_async_database/README.md)

</div>
