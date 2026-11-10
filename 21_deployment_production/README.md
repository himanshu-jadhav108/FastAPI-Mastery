# 21 — Deployment & Production Concerns

## Theory

This module is mostly conceptual — deployment infrastructure varies by
where you host, but the concepts transfer everywhere.

### Uvicorn vs Gunicorn+Uvicorn workers

`fastapi dev` / plain `uvicorn app:app --reload` is a **development**
server — one process, auto-reload on file changes, not built for
production load.

For production, run multiple worker processes so requests are handled in
parallel across CPU cores:

```bash
# Option A: Uvicorn's own multi-worker mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Option B: Gunicorn managing Uvicorn workers (more mature process management)
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

A common starting point for `--workers` is `(2 x CPU cores) + 1`, then
tune based on actual load testing.

### Dockerizing a FastAPI app

```dockerfile
FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Key points:
- `--host 0.0.0.0` — required in Docker so the server accepts connections
  from outside the container (`127.0.0.1` would only accept connections
  from inside it)
- Copy `requirements.txt` and install dependencies **before** copying the
  rest of the app — Docker caches layers, so your dependency install only
  reruns when `requirements.txt` actually changes, not on every code edit
- Don't run `--reload` in production images — it adds file-watching
  overhead you don't want

### Environment-specific configuration

You already built this in module 19 — `Settings` reads from environment
variables. In Docker/production, you set those via `docker run -e
SECRET_KEY=... ` or your platform's environment/secrets manager, never
baked into the image.

### `/health` endpoints matter

Load balancers and container orchestrators (Kubernetes, ECS, etc.) need
a cheap endpoint to poll to know if your app is alive:

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

For a more thorough check, verify the database connection too:

```python
@app.get("/health")
def health(session: SessionDep):
    try:
        session.exec(select(1))
        return {"status": "ok", "database": "connected"}
    except Exception:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Database unavailable")
```

### Don't leak internals

In production, disable `/docs` and `/redoc` (or protect them) if your
API isn't meant to be publicly browsable — anyone can see your entire
schema otherwise:

```python
import os

app = FastAPI(
    docs_url="/docs" if os.getenv("DEBUG") == "true" else None,
    redoc_url="/redoc" if os.getenv("DEBUG") == "true" else None,
)
```

Also make sure your generic-exception handler (module 15) never returns
a raw traceback to the client — that leaks file paths, library versions,
and sometimes secrets.

### CORS in production

Revisit module 10 — `allow_origins` should list your actual frontend
domain(s), never `"*"`, once you're live.

### A production checklist

- [ ] `SECRET_KEY` and all secrets come from environment variables, not
      code
- [ ] Debug mode / `/docs` disabled or protected in production
- [ ] CORS `allow_origins` is an explicit list, not `"*"`
- [ ] Database uses connection pooling appropriate to your DB (async
      engine + a real Postgres in production, not SQLite)
- [ ] Migrations (Alembic) are run as a deploy step, not
      `create_all()` in code
- [ ] Logging goes somewhere durable (not just stdout lost on restart)
- [ ] `/health` endpoint exists and is wired into your platform's health
      checks
- [ ] Rate limiting exists on public-facing write endpoints (a reverse
      proxy or API gateway typically handles this)
- [ ] Uvicorn/Gunicorn run with multiple workers, not the dev server
- [ ] HTTPS is terminated somewhere (a load balancer, reverse proxy, or
      platform-managed certificate) — Uvicorn itself is usually not
      handling TLS directly in production

## Task

No new code to write — this is a wiring/assembly exercise using
everything from modules 16-20.

1. Open `project/` — it's the module 16 router-based project, now with
   a `Dockerfile` and `requirements.txt` already included.
2. Read the `Dockerfile` line by line and match each line to the theory
   above.
3. Build the image: `docker build -t task-manager-api .` (from inside
   `project/`).
4. Run it: `docker run -p 8000:8000 -e SECRET_KEY=some-real-secret
   task-manager-api`
5. Confirm `http://localhost:8000/health` responds from inside the
   container.
6. As a stretch task: add the `/health` DB-check version shown above,
   rebuild, and confirm it still returns 200 with a real (even if
   SQLite-based) database connected.

If you don't have Docker installed, read through steps 2-6 conceptually
— the goal is understanding what each line does and why, which transfers
to any container platform.
