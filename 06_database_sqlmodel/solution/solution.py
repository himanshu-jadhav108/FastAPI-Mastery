from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Field as SQLField
from sqlmodel import Session, SQLModel, create_engine, select

class Task(SQLModel, table=True):
    id       : int | None = SQLField(default=None, primary_key=True)
    title    : str
    priority : int = 3
    done     : bool = False

DATABASE_URL = "sqlite:///.tasks.db"
engine        = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

create_db_and_tables()

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: Task, session: SessionDep):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.get("/tasks")
def list_tasks(session: SessionDep):
    return session.exec(select(Task)).all()

@app.get("/tasks/{task_id}")
def get_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task Not Found"
        )
    return task