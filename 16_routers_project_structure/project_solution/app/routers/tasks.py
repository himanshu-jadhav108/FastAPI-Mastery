"""Task routes — SOLUTION."""

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from ..database import SessionDep
from ..dependencies import CurrentUserDep
from ..models import Task
from ..schemas import TaskCreate, TaskRead

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, current_user: CurrentUserDep, session: SessionDep):
    new_task = Task(**task.model_dump(), owner_id=current_user.id)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@router.get("/mine", response_model=list[TaskRead])
def my_tasks(current_user: CurrentUserDep, session: SessionDep):
    return session.exec(select(Task).where(Task.owner_id == current_user.id)).all()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, current_user: CurrentUserDep, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    if task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your task.")
    session.delete(task)
    session.commit()
    return {"deleted": task_id}
