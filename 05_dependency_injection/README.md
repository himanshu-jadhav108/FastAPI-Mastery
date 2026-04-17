# 05 — Dependency Injection

## Theory

A **dependency** is just a function. `Depends()` tells FastAPI: "before
running this endpoint, call this function and pass its return value in."

```python
from fastapi import Depends
from typing import Annotated

def common_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/tasks")
def list_tasks(pagination: Annotated[dict, Depends(common_pagination)]):
    ...
```

Why bother, instead of just calling the function yourself inside the
endpoint?

1. **Reuse** — ten endpoints can share the exact same pagination logic
   without repeating the parameter list ten times.
2. **Composability** — dependencies can depend on other dependencies.
3. **Testability** — in tests, you can override a dependency (e.g. swap
   a real database for a fake one) without touching endpoint code.
4. **It's how auth works** — "get the current logged-in user" (module 08)
   is just a dependency.

**The `Annotated` pattern** — `Annotated[Type, Depends(fn)]` — lets you
define an alias once and reuse it everywhere:

```python
PaginationDep = Annotated[dict, Depends(common_pagination)]

@app.get("/tasks")
def list_tasks(pagination: PaginationDep):
    ...
```

**Dependencies with `yield`** are used for setup/teardown (you'll use this
exact pattern for database sessions in module 06):

```python
def get_resource():
    resource = acquire()
    try:
        yield resource
    finally:
        release(resource)
```

## Task

Open `starter.py`.

1. Write a `pagination_params` dependency: `skip: int = 0`,
   `limit: int = Query(default=10, ge=1, le=100)`. Return them as a dict.
2. Create a `PaginationDep` type alias using `Annotated`.
3. Use it in `GET /tasks` to skip/limit the results.
4. Write a **second** dependency, `verify_title_query`, that reads an
   optional query param `search: str | None = None` and returns it
   lowercased (or `None`). Use it in `GET /tasks` too, filtering tasks
   whose title contains the search string.
5. Confirm both dependencies work together: `/tasks?search=fastapi&limit=5`.
