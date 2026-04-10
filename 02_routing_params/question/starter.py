"""
Module 02 — Path & Query Parameters
Run with: fastapi dev starter.py
"""

from fastapi import FastAPI, Query

app = FastAPI()

tasks: list[dict] = [
    {"id": 1, "title": "Learn FastAPI basics", "done": True},
    {"id": 2, "title": "Learn path parameters", "done": False},
    {"id": 3, "title": "Learn query parameters", "done": False},
]


@app.get("/")
def home():
    return {"message": "Task Manager API is running"}


# TODO 1: GET /tasks
# Accept optional query params:
#   done: bool | None = None
#   limit: int = Query(default=10, ge=1, le=100)
# Filter `tasks` by `done` if it was provided, then return only the
# first `limit` results.


# TODO 2: GET /tasks/{task_id}
# task_id: int (path parameter)
# Find the task with matching id in `tasks`.
# If found, return it.
# If not found, return {"error": "not found"}  (proper 404s come in module 04)


# TODO 3: DELETE /tasks/{task_id}
# Remove the task with matching id from `tasks` (if present).
# Return {"deleted": task_id}
