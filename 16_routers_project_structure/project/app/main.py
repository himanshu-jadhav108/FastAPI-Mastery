"""
Module 16 — main.py
Run with (from inside project/): fastapi dev app/main.py
"""

from fastapi import FastAPI

from .database import create_db_and_tables

# TODO 1: from .routers import auth, tasks

app = FastAPI(title="Task Manager API")

create_db_and_tables()

# TODO 2: app.include_router(auth.router)
# TODO 3: app.include_router(tasks.router)


@app.get("/")
def home():
    return {"message": "Task Manager API is running"}
