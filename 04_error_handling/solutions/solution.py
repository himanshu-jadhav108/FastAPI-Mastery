from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

tasks: list[dict] = []
next_id = 1

class TaskCreate(BaseModel):
    title    : str  = Field(min_length=1, max_length=100)
    priority : int  = Field(default=3, ge=1, le=5)
    done     : bool = False

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Title cannot be blank or whitespace")
        return stripped

class TaskUpdate(BaseModel):
    title    : str  | None = Field(default=None, min_length=1, max_length=100)
    priority : int  | None = Field(default=None, ge=1, le=5)
    done     : bool | None = None

class TaskRead(BaseModel):
    id       : int
    title    : str
    priority : int
    done     : bool

@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    global next_id
    if any(t["title"].lower() == task.title.lower() for t in tasks):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A task with this title already exists"
        )
    new_task = {"id" : next_id, **task.model_dump()}
    tasks.append(new_task)
    next_id += 1
    return new_task

@app.get("/tasks", response_model=list[TaskRead])
def list_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="Task Not Found"
    )

@app.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, update: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task.update(update.model_dump(exclude_unset=True))
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found.",
    )

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    if not any(t["id"] == task_id for t in tasks):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not Found"
        )
    task = [t for t in tasks if t["id"] != task_id]
    return {"deleted": task_id}
