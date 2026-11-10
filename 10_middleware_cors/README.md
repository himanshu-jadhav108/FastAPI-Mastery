<div align="center">

# 🌐 Module 10: Custom Middleware & CORS Configuration

[![Level](https://img.shields.io/badge/Level-Intermediate-blue?style=for-the-badge)](#)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)](#)

[⏮️ Previous: 09 Role-Based Authorization](../09_authorization_roles/README.md) • [📚 Course Overview](../README.md) • [Next: 11 Background Tasks ⏭️](../11_background_tasks/README.md)

---

</div>

## 📌 Architectural Overview

**Middleware** wraps the entire request-response execution lifecycle of your application. Every incoming request passes through middleware *before* reaching any router or route handler, and every response passes through middleware *on its way back* to the client.

```
                    +------------------------------------+
                    |        Client HTTP Request         |
                    +------------------------------------+
                                      |
                                      v
                    +------------------------------------+
                    |       Middleware: Before Call      |
                    | (Start Timer, Inspect Headers)     |
                    +------------------------------------+
                                      |
                                      v
                    +------------------------------------+
                    |         Route Handler Logic        |
                    +------------------------------------+
                                      |
                                      v
                    +------------------------------------+
                    |       Middleware: After Call       |
                    | (Inject X-Process-Time, Log)       |
                    +------------------------------------+
                                      |
                                      v
                    +------------------------------------+
                    |        Final HTTP Response         |
                    +------------------------------------+
```

---

## 💡 Core Theoretical Concepts

### 1. The `@app.middleware("http")` Pipeline

Middleware intercepts requests and passes control downstream using `await call_next(request)`:

```python
import time
from fastapi import Request

@app.middleware("http")
async def process_timer(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{duration:.4f}s"
    return response
```

> [!NOTE]
> When defining multiple middleware functions, they execute in the **reverse order** of addition on the incoming path (onion model: last added runs first on request; first added runs first on response).

### 2. Cross-Origin Resource Sharing (CORS)

Browsers enforce the **Same-Origin Policy (SOP)**: scripts running on domain `http://frontend.com` cannot call APIs on `http://api.backend.com` unless the server explicitly grants permission via HTTP CORS response headers (`Access-Control-Allow-Origin`).

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # React dev server
        "http://localhost:5173",   # Vite dev server
        "https://app.mydomain.com" # Production client
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

> [!WARNING]
> **Production Anti-Pattern**: Never set `allow_origins=["*"]` when `allow_credentials=True`. Browsers strictly reject credentialed requests (cookies/authorization headers) configured with wildcard origins.

---

## 🎯 Task Specifications

Update `question/starter.py` with custom performance instrumentation and standard frontend origin permissions.

### Requirements

1. **CORS Middleware**:
   - Allow origins `http://localhost:3000` and `http://localhost:5173`.
   - Allow credentials, all methods (`*`), and all headers (`*`).
2. **Process Timing Middleware**:
   - Compute total elapsed time using `time.perf_counter()`.
   - Append `X-Process-Time` header to outgoing response.
   - Log request details: method, path, HTTP status, and duration.
3. **API Versioning Middleware**:
   - Append `X-API-Version: 1.0` to every response.

---

## 🛠️ Step-by-Step Implementation

1. Open `question/starter.py`.
2. Add `CORSMiddleware` using `app.add_middleware()`.
3. Implement `@app.middleware("http")` for elapsed duration calculation.
4. Implement a second middleware attaching `X-API-Version`.
5. Run the server and inspect the response headers in your terminal or browser devtools.

---

## 🧪 Verification Commands

```bash
# Query the API and inspect returned headers (-i flag)
curl -i http://127.0.0.1:8000/tasks

# Expected Response Headers:
# HTTP/1.1 200 OK
# X-Process-Time: 0.0012s
# X-API-Version: 1.0
# content-type: application/json
```

---

<div align="center">

[⏮️ Previous: 09 Role-Based Authorization](../09_authorization_roles/README.md) • [📚 Course Overview](../README.md) • [Next: 11 Background Tasks ⏭️](../11_background_tasks/README.md)

</div>
