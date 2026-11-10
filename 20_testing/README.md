<div align="center">

# 🧪 Module 20: Comprehensive Testing with Pytest & TestClient

[![Level](https://img.shields.io/badge/Level-Advanced-red?style=for-the-badge)](#)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)](#)

[⏮️ Previous: 19 Pydantic Settings](../19_pydantic_settings/README.md) • [📚 Course Overview](../README.md) • [Next: 21 Deployment & Production ⏭️](../21_deployment_production/README.md)

---

</div>

## 📌 Architectural Overview

Shipping software without automated tests is reckless. FastAPI includes first-class integration with **HTTPX** via `TestClient`.

The `TestClient` mounts your ASGI application directly **in-process**. It does not spawn a network port or listen on a TCP socket; it feeds simulated HTTP request byte-streams straight into the ASGI application interface. Tests run in milliseconds and can execute thousands of assertions inside CI/CD pipelines in seconds.

```
       [Pytest Test Runner]
                 │
                 ▼ invokes
       [FastAPI TestClient(app)]
                 │
                 ▼ (In-Process ASGI Invocation - No Network Lag)
       [Dependency Overrides: In-Memory SQLite Test DB]
                 │
                 ▼
       [FastAPI Route Handler & Logic]
                 │
                 ▼ returns
       [HTTP Response Object for Assertions]
```

---

## 💡 Core Theoretical Concepts

### 1. `TestClient` Basics

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager API is running"}
```

### 2. Isolated Test Database with Dependency Overrides

Never run integration tests against a live development or production database! Use FastAPI's `app.dependency_overrides` dictionary to swap out the real database session with an isolated SQLite in-memory database:

```python
import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.database import get_session

# In-memory single-thread SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

### 3. Testing Authentication & Headers

```python
def test_create_task_authenticated(client: TestClient):
    token = get_auth_token(client, username="alice", password="password123")
    response = client.post(
        "/tasks",
        json={"title": "Test task", "priority": 4},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test task"
```

---

## 🎯 Task Specifications

Open `question/test_app.py` and implement a complete test suite for the Task Manager API in `solution/app_to_test.py`.

### Test Scenarios to Cover

1. `test_read_root`: Assert status `200` and greeting message.
2. `test_create_task_valid`: Assert status `201`, verified ID, and returned title.
3. `test_create_task_invalid_title`: Assert status `422` when sending an empty string title.
4. `test_get_task_not_found`: Assert status `404` for non-existent ID `999`.
5. `test_list_tasks_pagination`: Seed 5 tasks; assert `limit=2` returns exactly 2 tasks.
6. `test_delete_task`: Create task, delete it, assert status `204`, then assert subsequent `GET` returns `404`.

---

## 🛠️ Step-by-Step Implementation

1. Open `question/test_app.py`.
2. Configure the `session` and `client` fixtures using `app.dependency_overrides`.
3. Write test functions with descriptive names prefixed with `test_`.
4. Run `pytest` and confirm all assertions pass.

---

## 🧪 Verification Commands

```bash
# Run the test suite with verbose output
pytest question/test_app.py -v

# Run with test coverage report
pytest --cov=solution 20_testing/solution/solution_test_app.py -v
```

---

<div align="center">

[⏮️ Previous: 19 Pydantic Settings](../19_pydantic_settings/README.md) • [📚 Course Overview](../README.md) • [Next: 21 Deployment & Production ⏭️](../21_deployment_production/README.md)

</div>
