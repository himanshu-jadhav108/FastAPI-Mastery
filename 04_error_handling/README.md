<div align="center">

# 🚨 Module 04: Error Handling & Semantic HTTP Statuses

[![Level](https://img.shields.io/badge/Level-Foundations-green?style=for-the-badge)](#)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)](#)

[⏮️ Previous: 03 Pydantic Validation](../03_pydantic_validation/README.md) • [📚 Course Overview](../README.md) • [Next: 05 Dependency Injection ⏭️](../05_dependency_injection/README.md)

---

</div>

## 📌 Architectural Overview

In a resilient RESTful service, errors must never result in silent failures or unhandled 500 crashes. FastAPI provides `HTTPException` as a first-class control-flow primitive that immediately short-circuits request execution and returns standard RFC 7807-compliant JSON error bodies.

```
Request ──> [Route Logic] ──> [Invalid State Detected]
                                       │
                                       ▼
                       raise HTTPException(status, detail)
                                       │
                                       ▼ (Immediate Short-Circuit)
Response <── [Status Code + {"detail": "Error description"}]
```

---

## 💡 Core Theoretical Concepts

### 1. The `HTTPException` Pattern

Always use `fastapi.status` constants rather than raw integer codes for self-documenting code and IDE autocomplete:

```python
from fastapi import HTTPException, status

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found."
        )
    return task
```

### 2. Industry Standard HTTP Status Reference

| Status Code | Constant Name | Usage Scenario |
| :---: | :--- | :--- |
| `200` | `HTTP_200_OK` | Successful retrieval (`GET`) or mutation (`PUT`/`PATCH`) |
| `201` | `HTTP_201_CREATED` | Successful entity creation (`POST`) |
| `204` | `HTTP_204_NO_CONTENT` | Successful action with empty response (`DELETE`) |
| `400` | `HTTP_400_BAD_REQUEST` | Client syntax or business logic error |
| `401` | `HTTP_401_UNAUTHORIZED` | Missing or invalid authentication token |
| `403` | `HTTP_403_FORBIDDEN` | Authenticated user lacks required permissions |
| `404` | `HTTP_404_NOT_FOUND` | Target resource does not exist |
| `409` | `HTTP_409_CONFLICT` | Duplicate unique constraint violation |
| `422` | `HTTP_422_UNPROCESSABLE_ENTITY` | Pydantic schema validation failure |

### 3. Partial Updates via `PATCH` & `exclude_unset=True`

When updating a resource partially with `PATCH`, define all fields in `TaskUpdate` as optional (`None`). Then use `.model_dump(exclude_unset=True)` to extract **only** the fields explicitly provided by the caller:

```python
class TaskUpdate(BaseModel):
    title: str | None = None
    priority: int | None = None
    done: bool | None = None

update_data = payload.model_dump(exclude_unset=True)
for key, value in update_data.items():
    setattr(task, key, value)
```

---

## 🎯 Task Specifications

Update `question/starter.py` with rigorous validation and robust exception flows.

### Route Contract

| Method | Path | Request Body | Success Code | Error Handling Logic |
| :--- | :--- | :--- | :---: | :--- |
| `GET` | `/tasks/{task_id}` | None | `200 OK` | `404 Not Found` if `task_id` does not exist |
| `DELETE` | `/tasks/{task_id}` | None | `200 OK` / `204` | `404 Not Found` if `task_id` does not exist |
| `POST` | `/tasks` | `TaskCreate` | `201 Created` | `409 Conflict` if title already exists (case-insensitive) |
| `PATCH` | `/tasks/{task_id}` | `TaskUpdate` | `200 OK` | `404 Not Found` if not found; updates only provided fields |

---

## 🛠️ Step-by-Step Implementation

1. Open `question/starter.py`.
2. Implement duplicate detection in `POST /tasks` and raise `HTTP_409_CONFLICT` with detail `"A task with this title already exists."`.
3. Update `GET /tasks/{task_id}` and `DELETE /tasks/{task_id}` to raise `HTTP_404_NOT_FOUND` with detail `"Task not found."`.
4. Implement `PATCH /tasks/{task_id}` accepting `TaskUpdate`. Use `.model_dump(exclude_unset=True)` to mutate existing record fields.
5. Verify error behavior using `/docs`.

---

## 🧪 Verification Commands

```bash
# 1. Trigger 409 Conflict with Duplicate Task
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Unique Task", "priority": 3}'

curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "unique task", "priority": 1}'

# 2. Trigger 404 on Missing Resource
curl -X GET http://127.0.0.1:8000/tasks/99999

# 3. Successful Partial Update (PATCH)
curl -X PATCH http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

---

<div align="center">

[⏮️ Previous: 03 Pydantic Validation](../03_pydantic_validation/README.md) • [📚 Course Overview](../README.md) • [Next: 05 Dependency Injection ⏭️](../05_dependency_injection/README.md)

</div>
