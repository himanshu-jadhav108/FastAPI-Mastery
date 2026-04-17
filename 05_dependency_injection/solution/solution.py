from typing import Annotated

from fastapi import Depends, FastAPI, Query

app = FastAPI()

tasks: list[dict] = [
    {"id": 1, "title": "Learn FastAPI basics", "priority": 3, "done": True},
    {"id": 2, "title": "Learn dependency injection", "priority": 2, "done": False},
    {"id": 3, "title": "Build the task manager", "priority": 1, "done": False},
]

def pagination_params(
        skip  : int = 0,
        limit : int = Query(default=10, ge=1, le=100)
):
    return {"skip" : skip, "limit" : limit}

PaginationDep = Annotated[dict, Depends(pagination_params)]

def verify_title_query(search: str | None = None) -> str | None:
    return search.lower() if search else None

SearchDep = Annotated[str | None, Depends(verify_title_query)]

@app.get("/tasks")
def list_tasks(pagination: PaginationDep, search: SearchDep):
    result = tasks
    if search:
        result = [t for t in result if search in t["title"].lower()]
        skip = pagination["skip"]
        limit = pagination["limit"]
        return result[skip: skip + limit]
    