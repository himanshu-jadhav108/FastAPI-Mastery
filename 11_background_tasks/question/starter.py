"""
Module 11 — Background Tasks
Run with: fastapi dev starter.py
"""

import time
from datetime import datetime, timezone
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, HTTPException, status

app = FastAPI()

tasks: list[dict] = []
next_id = 1

LOG_PATH = Path("activity.log")


# TODO 1: def write_activity_log(username: str, message: str):
# Append f"{datetime.now(timezone.utc).isoformat()} | {username} | {message}\n"
# to LOG_PATH (open in append mode).


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(title: str, background_tasks: BackgroundTasks):
    global next_id
    task = {"id": next_id, "title": title}
    tasks.append(task)
    next_id += 1
    # TODO 2: schedule write_activity_log("system", f"Created task: {title}")
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, background_tasks: BackgroundTasks):
    global tasks
    if not any(t["id"] == task_id for t in tasks):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    tasks = [t for t in tasks if t["id"] != task_id]
    # TODO 3: schedule write_activity_log("system", f"Deleted task: {task_id}")
    return {"deleted": task_id}


def send_slow_notification(task_id: int):
    # Simulates slow work (e.g. sending an email via a third-party API).
    time.sleep(2)
    # TODO 4: call write_activity_log here with
    # ("system", f"Notification sent for task {task_id}")


@app.post("/tasks/{task_id}/notify")
def notify(task_id: int, background_tasks: BackgroundTasks):
    # TODO 5: schedule send_slow_notification(task_id) and return immediately
    # with {"message": "Notification scheduled"}
    ...
