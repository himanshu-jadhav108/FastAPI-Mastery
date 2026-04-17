"""
Module 05 — Dependency Injection
Run with: fastapi dev starter.py
"""

from typing import Annotated

from fastapi import Depends, FastAPI, Query

app = FastAPI()

tasks: list[dict] = [
    {"id": 1, "title": "Learn FastAPI basics", "priority": 3, "done": True},
    {"id": 2, "title": "Learn dependency injection", "priority": 2, "done": False},
    {"id": 3, "title": "Build the task manager", "priority": 1, "done": False},
]


# TODO 1: pagination_params(skip: int = 0, limit: int = Query(default=10, ge=1, le=100))
# -> return {"skip": skip, "limit": limit}


# TODO 2: PaginationDep = Annotated[dict, Depends(pagination_params)]


# TODO 3: verify_title_query(search: str | None = None) -> str | None
# -> return search.lower() if search else None


# TODO 4: SearchDep = Annotated[str | None, Depends(verify_title_query)]


@app.get("/tasks")
def list_tasks():
    # TODO 5: add `pagination: PaginationDep` and `search: SearchDep` params
    # Filter `tasks` by search (if not None, check it's a substring of
    # the lowercased title), then apply skip/limit slicing.
    return tasks
