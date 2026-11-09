"""
Module 20 — Testing with pytest + TestClient — SOLUTION
Run with: pytest -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app_to_test import app, get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
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


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register_and_login(client: TestClient):
    register_response = client.post(
        "/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "secret123"},
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={"username": "alice", "password": "secret123"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_create_task_requires_auth(client: TestClient):
    response = client.post("/tasks", json={"title": "Unauthorized task"})
    assert response.status_code == 401


def test_full_task_lifecycle(client: TestClient):
    client.post(
        "/auth/register",
        json={"username": "bob", "email": "bob@example.com", "password": "secret123"},
    )
    login = client.post("/auth/login", data={"username": "bob", "password": "secret123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post("/tasks", json={"title": "Write tests"}, headers=headers)
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]
    assert create_response.json()["title"] == "Write tests"

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Write tests"

    patch_response = client.patch(f"/tasks/{task_id}", json={"done": True})
    assert patch_response.status_code == 200
    assert patch_response.json()["done"] is True

    delete_response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == 200

    final_get = client.get(f"/tasks/{task_id}")
    assert final_get.status_code == 404


def test_cannot_delete_others_task(client: TestClient):
    client.post(
        "/auth/register",
        json={"username": "carol", "email": "carol@example.com", "password": "secret123"},
    )
    client.post(
        "/auth/register",
        json={"username": "dave", "email": "dave@example.com", "password": "secret123"},
    )

    carol_login = client.post("/auth/login", data={"username": "carol", "password": "secret123"})
    carol_token = carol_login.json()["access_token"]
    carol_headers = {"Authorization": f"Bearer {carol_token}"}

    create_response = client.post(
        "/tasks", json={"title": "Carol's task"}, headers=carol_headers
    )
    task_id = create_response.json()["id"]

    dave_login = client.post("/auth/login", data={"username": "dave", "password": "secret123"})
    dave_token = dave_login.json()["access_token"]
    dave_headers = {"Authorization": f"Bearer {dave_token}"}

    delete_response = client.delete(f"/tasks/{task_id}", headers=dave_headers)
    assert delete_response.status_code == 403
