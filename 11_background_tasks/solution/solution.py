import time
from datetime import datetime, timezone
from pathlib import Path 

from fastapi import BackgroundTasks, FastAPI, HTTPException, status

app = FastAPI()

tasks: list[dict] = []
next_id = 1

LOG_PATH = Path("activity.log")

def write_activity_log(username: str, message: str):
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} | {username} | {message}\n")

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(title: str, background_tasks: BackgroundTasks):
    global next_id
    task = {"id": next_id, "title": title}
    tasks.append(task)
    next_id += 1
    background_tasks.add_task(write_activity_log, "system", f"Created task: {title}")
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, background_tasks: BackgroundTasks):
    global tasks
    if not any(t["id"] == task_id for t in tasks):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    tasks = [t for t in tasks if t["id"] != task_id]
    background_tasks.add_task(write_activity_log, "system", f"Deleted task: {task_id}")
    return {"deleted": task_id}

def send_slow_notification(task_id: int):
    time.sleep(2)
    write_activity_log("system", f"Notification sent for task {task_id}")   

@app.post("/tasks/{task_id}/notify")
def notify(task_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_slow_notification, task_id)
    return {"message": "Notification scheduled"}