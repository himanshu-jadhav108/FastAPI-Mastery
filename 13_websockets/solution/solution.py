"""
Module 13 — WebSockets — SOLUTION
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

tasks: list[dict] = []
next_id = 1

connected_clients: list[WebSocket] = []

@app.websocket("/ws/notifications")
async def notifications(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def broadcast(message: str):
    for ws in connected_clients:
        await ws.send_text(message)

@app.post("/tasks")
async def create_task(title: str):
    global next_id
    task = {"id": next_id, "title": title}
    tasks.append(task)
    next_id += 1
    await broadcast(f"New task created: {title}")
    return task
