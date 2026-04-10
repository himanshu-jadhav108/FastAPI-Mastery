from fastapi import FastAPI, Query

app = FastAPI()

tasks: list[dict] = [
    {"id": 1, "title": "Learn FastAPI Basics", "done": True},
    {"id": 2, "title": "Learn path parameters", "done": False},
    {"id": 3, "title": "Learn query parameters", "done": False},
]

@app.get("/")
def home():
    return {
        "message" : "Task Manager API is running"
    }

@app.get("/tasks")
def list_tasks(
    done: bool | None = None,
    limit: int = Query(default=10, ge=1, le=100),    
):
    result = tasks
    if done is not None:
        result = [t for t in result if t["done"] == done]
    return result[:limit]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return {
        "error" : "Task not found"
    }

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return {
        "deleted" : task_id
    }