# 00 — Setup & Tooling

No coding in this module — get your environment ready.

## Theory: what is FastAPI?

FastAPI is a Python web framework for building APIs. Three things make it
different from something like Flask:

1. **Type hints ARE the validation layer.** You write `name: str`, FastAPI
   validates it, converts it, and documents it — automatically.
2. **Async-native.** Built on Starlette (ASGI), so it handles concurrent
   I/O-bound requests efficiently.
3. **Free interactive docs.** Every app gets `/docs` (Swagger UI) and
   `/redoc` for free, generated from your code.

## Install

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install fastapi "uvicorn[standard]" sqlmodel pyjwt "pwdlib[argon2]" \
    python-multipart sqlalchemy[asyncio] asyncpg aiosqlite alembic \
    pydantic-settings pytest httpx
```

- `fastapi` — the framework
- `uvicorn[standard]` — the ASGI server that actually runs your app
- `sqlmodel` — ORM used in modules 06-16 (simple, sync)
- `sqlalchemy[asyncio]` + `asyncpg`/`aiosqlite` — async DB layer for module 17+
- `pyjwt`, `pwdlib[argon2]` — auth (module 08)
- `python-multipart` — required for file uploads and OAuth2 forms
- `alembic` — migrations (module 18)
- `pydantic-settings` — settings management (module 19)
- `pytest`, `httpx` — testing (module 20)

## Running any module

Every module has a `starter.py`. From inside that module's folder:

```bash
fastapi dev starter.py
```

or, older style:

```bash
uvicorn starter:app --reload
```

Then open:
- `http://127.0.0.1:8000/docs` — Swagger UI, click-to-test every endpoint
- `http://127.0.0.1:8000/redoc` — read-only alternative docs

## Task

Nothing to build. Just confirm your environment works:

```bash
python -c "import fastapi; print(fastapi.__version__)"
```

If that prints a version number, you're ready for `01_basics`.
