<div align="center">

# 🧭 Module 02: Path & Query Parameters

[![Level](https://img.shields.io/badge/Level-Foundations-green?style=for-the-badge)](#)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)](#)

[⏮️ Previous: 01 Basics](../01_basics/README.md) • [📚 Course Overview](../README.md) • [Next: 03 Pydantic Validation ⏭️](../03_pydantic_validation/README.md)

---

</div>

## 📌 Architectural Overview

FastAPI dynamically parses HTTP requests and maps parameters into function arguments based on where they appear in the route signature:
- **Path Parameters**: Extracted directly from URL path segments (`/tasks/{task_id}`).
- **Query Parameters**: Extracted from URL query strings (`/tasks?done=true&limit=10`).

FastAPI automatically parses, casts types, and validates values against Python type hints, instantly rejecting malformed inputs with detailed HTTP 422 errors.

```
       URL: http://api.com/tasks/42?done=true&limit=10
                                 │         │        │
             ┌───────────────────┘         │        │
             ▼                             ▼        ▼
       Path Parameter:                Query Parameters:
       task_id: int = 42              done: bool = True
                                      limit: int = 10
```

---

## 💡 Core Theoretical Concepts

### 1. Path Parameters

Path parameters are declared with curly braces `{param_name}` in the route path and must match the function argument name:

```python
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return {"task_id": task_id}
```

- **Type Coercion**: If a client calls `/tasks/42`, FastAPI casts `"42"` to integer `42`.
- **Validation**: If a client calls `/tasks/abc`, FastAPI immediately returns an HTTP `422 Unprocessable Entity` containing JSON explaining that `task_id` must be an integer.

### 2. Query Parameters

Function parameters that are not part of the path definition are automatically interpreted as query parameters:

```python
@app.get("/tasks")
def list_tasks(done: bool | None = None, limit: int = 10):
    return {"done": done, "limit": limit}
```

- **Optional Parameters**: Annotated as `Optional` or `type | None = None`.
- **Default Values**: Provide sensible defaults (e.g., `limit: int = 10`).

### 3. Advanced Parameter Validation with `Query` & `Path`

Using `Query()` or `Path()` from `fastapi`, you can enforce constraints, documentation strings, and boundary limits:

```python
from fastapi import Query
from typing import Annotated

@app.get("/tasks")
def list_tasks(
    limit: Annotated[int, Query(ge=1, le=100, description="Max tasks to return")] = 10,
    search: Annotated[str | None, Query(min_length=2, max_length=50)] = None,
):
    ...
```

---

## 🎯 Task Specifications

Enhance the Task Manager API to support parameter-based filtering, lookups, and pagination.

### Route Contract

| Method | Path | Query Params | Description | Response Code |
| :--- | :--- | :--- | :--- | :---: |
| `GET` | `/tasks` | `done: bool \| None`<br>`limit: int = 10 (1..100)`<br>`search: str \| None (min: 2)` | Filter tasks by completion status, limit results, or search keyword in title | `200 OK` |
| `GET` | `/tasks/{task_id}` | None | Retrieve a single task by its unique ID (return `None` or 404 message if missing) | `200 OK` |

---

## 🛠️ Step-by-Step Implementation

1. Open `question/starter.py`.
2. Update the `GET /tasks` endpoint:
   - Accept `done: bool | None = None`.
   - Accept `limit: int = Query(default=10, ge=1, le=100)`.
   - Accept `search: str | None = Query(default=None, min_length=2)`.
   - Filter the in-memory list accordingly.
3. Update the `GET /tasks/{task_id}` endpoint:
   - Accept `task_id: int`.
   - Search for the task with matching ID; return the item if found.
4. Launch and test via Swagger UI (`http://127.0.0.1:8000/docs`).

---

## 🧪 Verification Commands

```bash
# Valid task lookup
curl -X GET http://127.0.0.1:8000/tasks/1

# Invalid parameter type (Triggers HTTP 422)
curl -X GET http://127.0.0.1:8000/tasks/invalid-id

# Filter by completion status and limit
curl -X GET "http://127.0.0.1:8000/tasks?done=false&limit=5"
```

---

<div align="center">

[⏮️ Previous: 01 Basics](../01_basics/README.md) • [📚 Course Overview](../README.md) • [Next: 03 Pydantic Validation ⏭️](../03_pydantic_validation/README.md)

</div>
