"""
Module 15 — Logging & Custom Exception Handlers
Run with: fastapi dev starter.py
"""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# TODO 1: logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
# logger = logging.getLogger(__name__)

app = FastAPI()

tasks: dict[int, dict] = {
    1: {"id": 1, "title": "Learn logging"},
    2: {"id": 2, "title": "Learn exception handlers"},
}


# TODO 2: class TaskNotFoundError(Exception):
#     def __init__(self, task_id: int):
#         self.task_id = task_id


# TODO 3: @app.exception_handler(TaskNotFoundError)
# async def task_not_found_handler(request: Request, exc):
#     logger.warning("Task not found: %s", exc.task_id)
#     return JSONResponse(status_code=404, content={"error": "task_not_found", "task_id": exc.task_id})


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    # TODO 4: raise TaskNotFoundError(task_id) if missing, instead of HTTPException
    task = tasks.get(task_id)
    return task


# TODO 5: @app.exception_handler(ValueError)
# async def value_error_handler(request: Request, exc: ValueError):
#     logger.error("ValueError at %s: %s", request.url.path, exc)
#     return JSONResponse(status_code=400, content={"error": "value_error", "detail": str(exc)})


@app.post("/tasks/{task_id}/divide")
def divide(task_id: int, by: int):
    # TODO 6: if by == 0: raise ValueError("Cannot divide by zero.")
    # else return {"result": 100 / by}
    ...
