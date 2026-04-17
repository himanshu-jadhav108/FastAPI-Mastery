"""
Module 06 — Database with SQLModel
Run with: fastapi dev starter.py
"""

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Field as SQLField
from sqlmodel import Session, SQLModel, create_engine, select

# TODO 1: define Task(SQLModel, table=True)
#   id: int | None = SQLField(default=None, primary_key=True)
#   title: str
#   priority: int = 3
#   done: bool = False


# TODO 2: DATABASE_URL = "sqlite:///./tasks.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# TODO 3: def create_db_and_tables(): SQLModel.metadata.create_all(engine)
# Call it once here at import time (module 14 will do this properly).


# TODO 4: def get_session(): with Session(engine) as session: yield session
# SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: "Task", session: "SessionDep"):
    # TODO 5: session.add(task); session.commit(); session.refresh(task); return task
    ...


@app.get("/tasks")
def list_tasks(session: "SessionDep"):
    # TODO 6: return session.exec(select(Task)).all()
    ...


@app.get("/tasks/{task_id}")
def get_task(task_id: int, session: "SessionDep"):
    # TODO 7: task = session.get(Task, task_id); 404 if None; else return it
    ...
