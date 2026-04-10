from fastapi import FastAPI, status
from pydantic import BaseModel, Field, field_validator

app =FastAPI()

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
            raise ValueError("Title Cannot be Blanck or WhiteSpace")
        return stripped

class TaskRead(BaseModel):
    id       : int
    title    : str
    priority : int
    done     : bool

@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    global next_id
    new_task = {"id" : next_id, **task.model_dump()}
    tasks.append(new_task)
    next_id += 1
    return new_task

@app.get("/tasks", response_model=list[TaskRead])
def list_tasks():
    return tasks