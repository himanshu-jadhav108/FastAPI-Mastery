"""
Module 04 — Error Handling with HTTPException
Run with: fastapi dev starter.py
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

tasks: list[dict] = []
next_id = 1


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    priority: int = Field(default=3, ge=1, le=5)
    done: bool = False

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Title cannot be blank or whitespace.")
        return stripped


# TODO 1: Define TaskUpdate for PATCH — same fields as TaskCreate but
# ALL optional (title: str | None = None, etc.) so partial updates work.


class TaskRead(BaseModel):
    id: int
    title: str
    priority: int
    done: bool


@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    global next_id
    # TODO 2: raise 409 if any existing task's title matches (case-insensitive)
    new_task = {"id": next_id, **task.model_dump()}
    tasks.append(new_task)
    next_id += 1
    return new_task


@app.get("/tasks", response_model=list[TaskRead])
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int):
    # TODO 3: raise 404 with detail "Task not found." if missing
    for task in tasks:
        if task["id"] == task_id:
            return task


@app.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, update: "TaskUpdate"):
    # TODO 4: find the task, raise 404 if missing.
    # Apply only fields the client actually sent using
    # update.model_dump(exclude_unset=True), then return the updated task.
    ...


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    # TODO 5: raise 404 if no task had that id, else remove it and
    # return {"deleted": task_id}
    tasks = [t for t in tasks if t["id"] != task_id]
    return {"deleted": task_id}
