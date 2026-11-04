"""
Task routes — currently using @app.* by mistake. Fix the TODOs.
"""

from fastapi import HTTPException, status
from sqlmodel import select

from ..database import SessionDep
from ..dependencies import CurrentUserDep
from ..models import Task
from ..schemas import TaskCreate, TaskRead

# TODO 1: replace this with:
# from fastapi import APIRouter
# router = APIRouter(prefix="/tasks", tags=["tasks"])
app = None  # placeholder — remove once `router` exists


# TODO 2: change every @app.<method> below to @router.<method>


@app.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, current_user: CurrentUserDep, session: SessionDep):
    new_task = Task(**task.model_dump(), owner_id=current_user.id)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@app.get("/mine", response_model=list[TaskRead])
def my_tasks(current_user: CurrentUserDep, session: SessionDep):
    return session.exec(select(Task).where(Task.owner_id == current_user.id)).all()


@app.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    return task


@app.delete("/{task_id}")
def delete_task(task_id: int, current_user: CurrentUserDep, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    if task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your task.")
    session.delete(task)
    session.commit()
    return {"deleted": task_id}
