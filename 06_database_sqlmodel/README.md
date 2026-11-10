<div align="center">

# 🗄️ Module 06: Database Persistence with SQLModel

[![Level](https://img.shields.io/badge/Level-Intermediate-blue?style=for-the-badge)](#)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)](#)

[⏮️ Previous: 05 Dependency Injection](../05_dependency_injection/README.md) • [📚 Course Overview](../README.md) • [Next: 07 Full CRUD & Pagination ⏭️](../07_crud_pagination/README.md)

---

</div>

## 📌 Architectural Overview

Until now, data lived in volatile in-memory Python lists that vanished on server restart. This module introduces persistent relational database storage with **SQLModel**.

SQLModel bridges the gap between **SQLAlchemy** (the industry-standard Python ORM) and **Pydantic** (FastAPI’s validation engine), allowing a single class declaration to represent both a database table schema and a validation model.

```
+-------------------------------------------------------------+
|                     SQLModel Class                          |
|                                                             |
|  [SQLAlchemy Table Model]  <=======>  [Pydantic BaseModel]  |
|   (Columns, Primary Keys)              (Parsing & Types)    |
+-------------------------------------------------------------+
                               |
                               v
                     +-------------------+
                     | SQLite / Postgres |
                     +-------------------+
```

---

## 💡 Core Theoretical Concepts

### 1. Declaring Tables with SQLModel

Set `table=True` to flag the class as an active relational database table:

```python
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    priority: int = Field(default=3)
    done: bool = Field(default=False)
```

- `primary_key=True`: Marks `id` as the primary key.
- `default=None`: Allows Pydantic and SQLite to auto-generate the autoincrement ID when inserting new rows.

### 2. The Engine & SQLite Threading

The `engine` coordinates connection pooling and SQL dialect translation:

```python
from sqlmodel import create_engine

DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
```

> [!NOTE]
> `connect_args={"check_same_thread": False}` is required exclusively for SQLite to allow multiple asynchronous FastAPI worker threads to interact with the database file without thread-safety exceptions.

### 3. Yield-Based Session Dependency (`SessionDep`)

Database transactions must be scoped per HTTP request. Using a generator dependency with `yield` guarantees sessions are automatically closed and resources released, even if exceptions occur during request processing:

```python
from sqlmodel import Session
from typing import Annotated
from fastapi import Depends

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
```

### 4. Basic CRUD Operations

```python
# Create
session.add(new_task)
session.commit()
session.refresh(new_task)

# Read
task = session.get(Task, task_id)
tasks = session.exec(select(Task)).all()
```

---

## 🎯 Task Specifications

Upgrade `question/starter.py` to persist all tasks in a local SQLite database (`tasks.db`).

### Route Contract

| Method | Path               | Request Body | Success Code  | Description                                                                  |
| :----- | :----------------- | :----------- | :-----------: | :--------------------------------------------------------------------------- |
| `POST` | `/tasks`           | `Task`       | `201 Created` | Persist task in database, refresh auto-generated `id`, return created entity |
| `GET`  | `/tasks`           | None         |   `200 OK`    | Fetch all tasks from database via `select(Task)`                             |
| `GET`  | `/tasks/{task_id}` | None         |   `200 OK`    | Fetch task by primary key with `session.get()`, raise 404 if missing         |

---

## 🛠️ Step-by-Step Implementation

1. Open `question/starter.py`.
2. Define the `Task` table model inheriting from `SQLModel`.
3. Create the database engine pointing to `sqlite:///./tasks.db`.
4. Initialize the database schema with `SQLModel.metadata.create_all(engine)`.
5. Implement `get_session()` generator dependency and define `SessionDep`.
6. Implement `POST /tasks`, `GET /tasks`, and `GET /tasks/{task_id}`.
7. Restart your server and verify data persists across restarts!

---

## 🧪 Verification Commands

```bash
# 1. Create Task
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Verify database persistence", "priority": 4}'

# 2. Query All Tasks
curl -X GET http://127.0.0.1:8000/tasks

# 3. Retrieve Specific Task
curl -X GET http://127.0.0.1:8000/tasks/1
```

---

<div align="center">

[⏮️ Previous: 05 Dependency Injection](../05_dependency_injection/README.md) • [📚 Course Overview](../README.md) • [Next: 07 Full CRUD & Pagination ⏭️](../07_crud_pagination/README.md)

</div>
