"""
Module 03 — Pydantic Models & Validation
Run with: fastapi dev starter.py
"""

from fastapi import FastAPI, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

tasks: list[dict] = []
next_id = 1


# TODO 1: Define TaskCreate
#   title: str, length 1-100
#   priority: int, 1-5, default 3
#   done: bool, default False


# TODO 2: Add a @field_validator on "title" that strips whitespace and
# raises ValueError if the stripped result is empty.


# TODO 3: Define TaskRead — same fields as TaskCreate, plus id: int


# TODO 4: POST /tasks
# - body: TaskCreate
# - response_model=TaskRead, status_code=201
# - assign the task an id using `next_id`, increment `next_id`
# - store it in `tasks` as a dict, return it


# TODO 5: GET /tasks
# - response_model=list[TaskRead]
# - just return `tasks`
