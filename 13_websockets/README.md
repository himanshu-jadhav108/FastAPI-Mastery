# 13 — WebSockets

## Theory

HTTP is request → response, then the connection is done. **WebSockets**
keep a connection open so both sides can send messages at any time —
useful for chat, live notifications, or real-time dashboards.

```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"Echo: {message}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

- `await websocket.accept()` — must be called before send/receive
- `await websocket.receive_text()` — blocks until the client sends
  something (or disconnects, raising `WebSocketDisconnect`)
- `await websocket.send_text(...)` — send a message back

**Broadcasting to multiple clients** means tracking connections yourself:

```python
connected: list[WebSocket] = []

@app.websocket("/ws/notifications")
async def notifications(websocket: WebSocket):
    await websocket.accept()
    connected.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep the connection alive
    except WebSocketDisconnect:
        connected.remove(websocket)

async def broadcast(message: str):
    for ws in connected:
        await ws.send_text(message)
```

`broadcast` can then be called from a regular HTTP endpoint (e.g. after
creating a task) to push a live update to every connected client.

Note: this in-memory `connected` list only works with a single server
process. Multiple workers/servers need a shared pub/sub layer (Redis,
etc.) to broadcast across all of them — out of scope here, but good to
know before you deploy this pattern.

## Task

Open `starter.py`.

1. Build `/ws/notifications` as shown — track connected clients, remove
   them on disconnect.
2. Write `async def broadcast(message: str)` that sends to all connected
   clients.
3. `POST /tasks` → create the task (in-memory list is fine), then
   `await broadcast(f"New task created: {title}")`.
4. Test it: open two browser tabs to a simple WebSocket test page (or use
   `wscat`/Postman's WebSocket support) connected to `/ws/notifications`,
   then `POST /tasks` from `/docs` in a third tab — confirm both
   WebSocket clients receive the broadcast instantly.
