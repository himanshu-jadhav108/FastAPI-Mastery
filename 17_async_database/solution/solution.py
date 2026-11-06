"""
Module 17 — Async Database (SQLAlchemy Async + aiosqlite) — SOLUTION
"""

from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Field as SQLField
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///./tasks_async.db"
engine = create_async_engine(DATABASE_URL, echo=False)


class TaskBase(SQLModel):
    title: str
    priority: int = 3
    done: bool = False


class Task(TaskBase, table=True):
    id: int | None = SQLField(default=None, primary_key=True)


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int


class TaskUpdate(SQLModel):
    title: str | None = None
    priority: int | None = None
    done: bool | None = None


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, session: SessionDep):
    new_task = Task(**task.model_dump())
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task


@app.get("/tasks", response_model=list[TaskRead])
async def list_tasks(
    session: SessionDep,
    done: bool | None = None,
    skip: int = 0,
    limit: int = Query(default=10, ge=1, le=100),
):
    statement = select(Task)
    if done is not None:
        statement = statement.where(Task.done == done)
    statement = statement.offset(skip).limit(limit)
    result = await session.exec(statement)
    return result.all()


@app.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, session: SessionDep):
    task = await session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, update: TaskUpdate, session: SessionDep):
    task = await session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, session: SessionDep):
    task = await session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    await session.delete(task)
    await session.commit()
    return {"deleted": task_id}
