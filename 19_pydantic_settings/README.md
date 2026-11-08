# 19 — Settings Management with pydantic-settings

## Theory

Every module so far hardcoded things like `SECRET_KEY =
"dev-only-secret-change-this"` directly in the code. That's fine for
exercises, dangerous in real life — secrets belong in environment
variables, not source code (which ends up in git history).

**`pydantic-settings`** reads environment variables (and `.env` files)
into a typed, validated object:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./tasks.db"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    debug: bool = False

settings = Settings()
```

- Fields with a default are optional; `secret_key: str` (no default) is
  **required** — the app refuses to start without it, which is the
  correct failure mode (fail loud at startup, not silently at runtime).
- Values come from, in priority order: actual environment variables >
  the `.env` file > the field default.
- Types are validated exactly like request bodies — `debug: bool` reads
  the string `"true"`/`"1"` from the environment and gives you a real
  Python `bool`.

**`.env` file** (never commit this — add it to `.gitignore`):
```
SECRET_KEY=a-real-random-secret-generate-this-properly
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/proddb
DEBUG=false
```

pydantic-settings matches env var names to field names case-insensitively
by default, so `SECRET_KEY` in `.env` maps to `secret_key` on the model.

**Using settings via dependency injection**, so tests can override it:

```python
from functools import lru_cache

@lru_cache
def get_settings() -> Settings:
    return Settings()

SettingsDep = Annotated[Settings, Depends(get_settings)]

@app.get("/config-check")
def config_check(settings: SettingsDep):
    return {"debug": settings.debug, "algorithm": settings.algorithm}
```

`@lru_cache` means `Settings()` (which reads env vars / parses `.env`)
only runs once, not on every request.

## Task

Open `starter.py` and `.env.example` (copy it to `.env` before running).

1. Define `Settings(BaseSettings)`: `secret_key: str` (required),
   `algorithm: str = "HS256"`, `access_token_expire_minutes: int = 30`,
   `database_url: str = "sqlite:///./tasks_19.db"`, `debug: bool = False`.
2. `get_settings()` with `@lru_cache`, and `SettingsDep`.
3. `GET /config-check` → returns `{"debug": ..., "algorithm": ...,
   "database_url": ...}` — **never return `secret_key` in a response.**
4. Rewrite `create_access_token` to accept `settings: Settings` as a
   parameter instead of reading a module-level constant, so it uses
   `settings.secret_key`/`settings.algorithm`/
   `settings.access_token_expire_minutes`.
5. Test: run without a `.env` file / without `SECRET_KEY` set — confirm
   the app **fails to start** with a clear Pydantic validation error.
   Then create `.env` from `.env.example`, set a real value, and confirm
   it starts.
