from fastapi import FastAPI

app = FastAPI()

tasks: list[dict] = []

@app.get("/")
def home():
    return {
        "message" : "Task Manager API is running"
    }

@app.get("/tasks")
def tasks_list():
    return tasks

@app.post("/tasks")
def create_task():
    return {
        "received" : "ok"
    }

@app.get("/ping")
def ping():
    return {
        "pong": True
    }