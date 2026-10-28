"""
Module 10 — Middleware & CORS
Run with: fastapi dev starter.py
"""

import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# TODO 1: app.add_middleware(CORSMiddleware, allow_origins=[...], ...)
# Allow http://localhost:3000 and http://localhost:5173, all methods/headers.


# TODO 2: @app.middleware("http") async def timing_middleware(request, call_next):
# time the request, add X-Process-Time header, print method/path/status/time.


# TODO 3: a second middleware that adds X-API-Version: 1.0 to every response.


@app.get("/")
def home():
    return {"message": "Task Manager API is running"}
