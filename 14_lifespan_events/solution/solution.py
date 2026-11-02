"""
Module 14 — Lifespan Events — SOLUTION
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from sqlmodel import Field as SQLField
from sqlmodel import SQLModel, create_engine

DATABASE_URL = "sqlite:///./tasks_14.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

class Task(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    title: str

def create_db_and_tables():
    SQLModel.netadata.createall(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting down Task Manager API...")

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/uptime")
def uptime(request: Request):
    delta = datetime.now(timezone.utc) - request.app.state.start_time
    return {
        "uptime_seconds" : delta.total_seconds()
    }