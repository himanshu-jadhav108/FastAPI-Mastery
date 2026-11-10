"""
Module 21 — main.py
Run locally with: fastapi dev app/main.py
Run in Docker via the Dockerfile in this folder.
"""

import os

from fastapi import FastAPI, HTTPException, status
from sqlmodel import select

from .database import SessionDep, create_db_and_tables
from .routers import auth, tasks

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

app = FastAPI(
    title="Task Manager API",
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
)

create_db_and_tables()

app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/")
def home():
    return {"message": "Task Manager API is running"}


@app.get("/health")
def health(session: SessionDep):
    try:
        session.exec(select(1))
        return {"status": "ok", "database": "connected"}
    except Exception:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Database unavailable",
        )
