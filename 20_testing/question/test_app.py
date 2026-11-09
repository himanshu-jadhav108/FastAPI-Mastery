"""
Module 20 — Testing with pytest + TestClient
Run with: pytest -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app_to_test import app, get_session


# TODO 1: @pytest.fixture(name="session")
# def session_fixture():
#     engine = create_engine(
#         "sqlite://",
#         connect_args={"check_same_thread": False},
#         poolclass=StaticPool,
#     )
#     SQLModel.metadata.create_all(engine)
#     with Session(engine) as session:
#         yield session


# TODO 2: @pytest.fixture(name="client")
# def client_fixture(session: Session):
#     def get_session_override():
#         return session
#     app.dependency_overrides[get_session] = get_session_override
#     client = TestClient(app)
#     yield client
#     app.dependency_overrides.clear()


# TODO 3: def test_health_check(client: TestClient):
#     response = client.get("/health")
#     assert response.status_code == 200
#     assert response.json() == {"status": "ok"}


# TODO 4: def test_register_and_login(client: TestClient):
# Register a user (username="alice", email="alice@example.com",
# password="secret123"), assert 201. Then log in with the same
# credentials (form data, not JSON), assert 200 and that
# response.json() has "access_token".


# TODO 5: def test_create_task_requires_auth(client: TestClient):
# POST /tasks with no Authorization header, assert 401.


# TODO 6: def test_full_task_lifecycle(client: TestClient):
# Register + log in a user, grab the token.
# POST /tasks with the auth header, assert 201, grab the task id.
# GET /tasks/{id}, assert 200 and title matches.
# PATCH /tasks/{id} with {"done": true}, assert 200 and done is True.
# DELETE /tasks/{id}, assert 200.
# GET /tasks/{id} again, assert 404.


# TODO 7: def test_cannot_delete_others_task(client: TestClient):
# Register user A and user B (different usernames/emails).
# Log in as A, create a task, grab its id.
# Log in as B, try to DELETE that task id using B's token.
# Assert 403.
