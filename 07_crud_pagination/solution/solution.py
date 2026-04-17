
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

class TaskBase(SQLModel):
    title   : str
    priority: int  = 3
    done    : bool = False

class Task(TaskBase, table=True):
    id : int | None = SQLField(default=None, primary_key=True)

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int

class TaskUpdate(SQLModel):
    title   : str  | None = None
    priority: int  | None = None
    done    : bool | None = None

SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, session: SessionDep):
    db_task = Task(**task.model_dump())
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(
    session  : SessionDep,
    done     : bool | None = None,
    priority : int | None = None,
    skip     : int = 0,
    limit    : int = Query(default=10, ge=1, le=100),
):
    statement = select(Task)
    if done is not None:
        statement = statement.where(Task.done == done)
    if priority is not None:
        statement = statement.where(Task.priority == priority)
    statement = statement.offset(skip).limit(limit)
    tasks = session.exec(statement).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_update: TaskUpdate, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    session.delete(task)
    session.commit()
    return {"deleted": task_id}
