# 10 — Middleware & CORS

## Theory

**Middleware** runs on *every* request, wrapping your route handlers:

```
request  ->  middleware (before)  ->  route handler  ->  middleware (after)  ->  response
```

```python
import time
from fastapi import Request

@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{elapsed:.4f}"
    return response
```

`call_next(request)` runs the actual route (and any other middleware
after this one) and gives you back the response — you can inspect or
modify it before returning it. This is useful for timing, logging, adding
security headers, or short-circuiting requests (e.g. IP blocking) before
they hit your route.

**CORS (Cross-Origin Resource Sharing)** — browsers block JavaScript on
one domain (`myapp.com`) from calling an API on another domain
(`api.myapp.com` or `localhost:8000`) *unless* the API explicitly allows
it. This is a browser security feature, not something Python enforces —
it only matters when your API is called from browser JS.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://myapp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Never use `allow_origins=["*"]` together with `allow_credentials=True` in
production — that combination is explicitly disallowed by browsers for
security reasons, and even where technically allowed, `"*"` defeats the
purpose of CORS entirely.

## Task

Open `starter.py`.

1. Add `CORSMiddleware` allowing origins `http://localhost:3000` and
   `http://localhost:5173` (typical React/Vite dev ports), all methods,
   all headers.
2. Write a custom `@app.middleware("http")` function that:
   - times each request
   - adds an `X-Process-Time` response header
   - logs (just `print` is fine) the method, path, status code, and time
3. Write a second middleware that adds a header `X-API-Version: 1.0` to
   every response.
4. Confirm in `/docs` (Network tab of your browser's devtools, not
   Swagger itself) that both custom headers appear on responses.

Note: when you stack multiple `@app.middleware("http")` calls, they wrap
in the reverse order they were added — the last one added runs first on
the way in.
