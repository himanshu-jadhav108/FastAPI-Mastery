"""
Module 10 — Middleware & CORS — SOLUTION
"""

import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{elapsed:.4f}"
    print(f"{request.method} {request.url.path} -> {response.status_code} ({elapsed:.4f}s)")
    return response


@app.middleware("http")
async def version_header_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-API-Version"] = "1.0"
    return response


@app.get("/")
def home():
    return {"message": "Task Manager API is running"}
