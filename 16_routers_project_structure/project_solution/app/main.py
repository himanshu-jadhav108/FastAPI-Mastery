"""
Module 16 — main.py — SOLUTION
Run with (from inside project_solution/): fastapi dev app/main.py
"""

from fastapi import FastAPI

from .database import create_db_and_tables
from .routers import auth, tasks

app = FastAPI(title="Task Manager API")

create_db_and_tables()

app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/")
def home():
    return {"message": "Task Manager API is running"}
