# 20 — Testing with pytest + TestClient

## Theory

`TestClient` (from `fastapi.testclient`) lets you call your API in-process
— no running server needed, no real network calls, fast enough to run
hundreds of times in CI.

```python
from fastapi.testclient import TestClient
from myapp.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager API is running"}
```

**The critical problem: tests must not touch your real database.** If
`myapp.main` hardcodes a database file, your tests will pollute (or
depend on) real data. The fix is **dependency overrides** — swap
`get_session` for a test-only version, only during tests:

```python
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from myapp.main import app
from myapp.database import get_session

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",  # in-memory, no file at all
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # keeps the same in-memory DB across connections
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

Every test that takes `client` as an argument now hits a fresh in-memory
database instead of your real one. `app.dependency_overrides` is a dict
FastAPI checks before resolving any `Depends(...)` — so overriding
`get_session` there transparently swaps it out anywhere it's used.

**Testing a protected (auth-required) route** — register + log in inside
the test itself to get a real token, same as a real client would:

```python
def test_create_task_requires_auth(client: TestClient):
    response = client.post("/tasks", json={"title": "Test"})
    assert response.status_code == 401

def test_create_task_with_auth(client: TestClient):
    client.post("/auth/register", json={
        "username": "alice", "email": "alice@example.com", "password": "secret123"
    })
    login = client.post("/auth/login", data={"username": "alice", "password": "secret123"})
    token = login.json()["access_token"]

    response = client.post(
        "/tasks",
        json={"title": "Test task"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test task"
```

**Running tests:**
```bash
pytest -v
```

## Task

Open `app_to_test.py` (a small, complete Task Manager app — CRUD +
auth, reused from earlier modules) and `test_app.py` (has the TODOs).

1. Write the `session` fixture as shown (in-memory SQLite +
   `StaticPool`).
2. Write the `client` fixture with the `get_session` override.
3. `test_health_check` — `GET /health` returns 200.
4. `test_register_and_login` — register a user, then log in, assert both
   succeed and login returns an `access_token`.
5. `test_create_task_requires_auth` — `POST /tasks` with no auth header
   returns 401.
6. `test_full_task_lifecycle` — register, log in, create a task, `GET`
   it back, `PATCH` it, `DELETE` it, then `GET` it again and confirm 404.
7. `test_cannot_delete_others_task` — register two users, user A creates
   a task, user B tries to delete it, assert 403.

Run `pytest -v` and confirm all tests pass.
