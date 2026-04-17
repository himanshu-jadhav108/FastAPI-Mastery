"""
Module 07 — Full CRUD + Pagination & Filtering — BETTER VERSION
"""

from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Field, Session, SQLModel, create_engine, select

# ---------------- Database Setup ----------------
DATABASE_URL = "sqlite:///./tasks_07.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# ---------------- Models ----------------
class TaskBase(SQLModel):
    title: Annotated[str, Field(min_length=1, max_length=100)]
    priority: Annotated[int, Field(default=3, ge=1, le=5)]
    done: bool = False

class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int

class TaskUpdate(SQLModel):
    title: str | None = None
    priority: int | None = None
    done: bool | None = None

# ---------------- App Initialization ----------------
SQLModel.metadata.create_all(engine)
app = FastAPI()

# ---------------- Endpoints ----------------
@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, session: SessionDep):
    new_task = Task(**task.model_dump())
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task

@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(
    session: SessionDep,
    done: bool | None = None,
    priority: int | None = None,
    skip: int = 0,
    limit: int = Query(default=10, ge=1, le=100),
):
    statement = select(Task)
    if done is not None:
        statement = statement.where(Task.done == done)
    if priority is not None:
        statement = statement.where(Task.priority == priority)
    statement = statement.offset(skip).limit(limit)
    return session.exec(statement).all()

@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    return task

@app.put("/tasks/{task_id}", response_model=TaskRead)
def replace_task(task_id: int, new_task: TaskCreate, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    for field, value in new_task.model_dump().items():
        setattr(task, field, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, update: TaskUpdate, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    session.delete(task)
    session.commit()
    return
