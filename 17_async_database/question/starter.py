"""
Module 17 — Async Database (SQLAlchemy Async + aiosqlite)
Run with: fastapi dev starter.py
"""

from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Field as SQLField
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession  # SQLModel's async session (adds .exec())

# TODO 1: DATABASE_URL = "sqlite+aiosqlite:///./tasks_async.db"
# engine = create_async_engine(DATABASE_URL, echo=False)


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


# TODO 2: async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)


# TODO 3: @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_db_and_tables()
#     yield


app = FastAPI()  # TODO 4: pass lifespan=lifespan


# TODO 5: async def get_session():
#     async with AsyncSession(engine) as session:
#         yield session
# SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, session: "SessionDep"):
    # TODO 6: make this `async def`. Build Task, session.add (no await),
    # `await session.commit()`, `await session.refresh(new_task)`, return it.
    ...


@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(
    session: "SessionDep",
    done: bool | None = None,
    skip: int = 0,
    limit: int = Query(default=10, ge=1, le=100),
):
    # TODO 7: make this `async def`. Build the statement conditionally
    # (same pattern as module 07), then:
    # result = await session.exec(statement)
    # return result.all()
    ...


@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: "SessionDep"):
    # TODO 8: make this `async def`. `task = await session.get(Task, task_id)`
    # 404 if None, else return it.
    ...


@app.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, update: TaskUpdate, session: "SessionDep"):
    # TODO 9: make this `async def`. await session.get, 404 if missing,
    # apply exclude_unset fields, await commit, await refresh, return.
    ...


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: "SessionDep"):
    # TODO 10: make this `async def`. await session.get, 404 if missing,
    # `await session.delete(task)`, `await session.commit()`,
    # return {"deleted": task_id}
    ...
