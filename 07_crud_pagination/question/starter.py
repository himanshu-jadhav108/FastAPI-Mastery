"""
Module 07 — Full CRUD + Pagination & Filtering
Run with: fastapi dev starter.py
"""

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Field as SQLField
from sqlmodel import Session, SQLModel, create_engine, select

DATABASE_URL = "sqlite:///./tasks_07.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# TODO 1: TaskBase(SQLModel) with title: str, priority: int = 3, done: bool = False
# TODO 2: Task(TaskBase, table=True) adds id: int | None = SQLField(default=None, primary_key=True)
# TODO 3: TaskCreate(TaskBase): pass
# TODO 4: TaskRead(TaskBase): id: int
# TODO 5: TaskUpdate(SQLModel): title/priority/done, all optional, default None


SQLModel.metadata.create_all(engine)

app = FastAPI()


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: "TaskCreate", session: SessionDep):
    # TODO 6: build a Task from task.model_dump(), save, return (response_model=TaskRead)
    ...


@app.get("/tasks")
def list_tasks(
    session: SessionDep,
    done: bool | None = None,
    skip: int = 0,
    limit: int = Query(default=10, ge=1, le=100),
):
    # TODO 7: build the select(Task) statement conditionally (see README),
    # apply offset/limit, execute, return results (response_model=list[TaskRead])
    ...


@app.get("/tasks/{task_id}")
def get_task(task_id: int, session: SessionDep):
    # TODO 8: session.get, 404 if missing, else return (response_model=TaskRead)
    ...


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, update: "TaskUpdate", session: SessionDep):
    # TODO 9: fetch, 404 if missing, apply exclude_unset fields with setattr,
    # add/commit/refresh, return (response_model=TaskRead)
    ...


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: SessionDep):
    # TODO 10: fetch, 404 if missing, session.delete + commit,
    # return {"deleted": task_id}
    ...
