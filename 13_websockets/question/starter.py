"""
Module 13 — WebSockets
Run with: fastapi dev starter.py

Quick manual test page: open test_client.html in a browser (after
starting the server) to connect a WebSocket client without extra tools.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

tasks: list[dict] = []
next_id = 1

connected_clients: list[WebSocket] = []


# TODO 1: @app.websocket("/ws/notifications")
# async def notifications(websocket: WebSocket):
#     await websocket.accept()
#     connected_clients.append(websocket)
#     try:
#         while True:
#             await websocket.receive_text()  # just keeps the connection open
#     except WebSocketDisconnect:
#         connected_clients.remove(websocket)


# TODO 2: async def broadcast(message: str):
# loop over connected_clients and await ws.send_text(message) for each


@app.post("/tasks")
async def create_task(title: str):
    global next_id
    task = {"id": next_id, "title": title}
    tasks.append(task)
    next_id += 1
    # TODO 3: await broadcast(f"New task created: {title}")
    return task
