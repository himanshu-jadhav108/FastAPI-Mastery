<div align="center">

# ⚙️ Module 19: 12-Factor Settings Management with Pydantic-Settings

[![Level](https://img.shields.io/badge/Level-Advanced-red?style=for-the-badge)](#)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)](#)

[⏮️ Previous: 18 Migrations with Alembic](../18_migrations_alembic/README.md) • [📚 Course Overview](../README.md) • [Next: 20 Testing with Pytest ⏭️](../20_testing/README.md)

---

</div>

## 📌 Architectural Overview

Hardcoding secrets, database URLs, and configuration flags into source code is one of the most critical security vulnerabilities in software engineering. When code is pushed to Git repositories, leaked credentials can compromise production databases and authentication tokens.

The **12-Factor App methodology** dictates strict separation of config from code. **`pydantic-settings`** parses, validates, and type-checks environment variables and `.env` files into an immutable, strongly-typed configuration singleton.

```mermaid
flowchart LR
    classDef srcStyle fill:#0284c7,stroke:#0369a1,stroke-width:2px,color:#ffffff,font-weight:bold;
    classDef parseStyle fill:#7c3aed,stroke:#6d28d9,stroke-width:2px,color:#ffffff,font-weight:bold;
    classDef errStyle fill:#dc2626,stroke:#b91c1c,stroke-width:2px,color:#ffffff,font-weight:bold;
    classDef passStyle fill:#059669,stroke:#047857,stroke-width:2px,color:#ffffff,font-weight:bold;

    subgraph Config Sources
        EnvVars["🖥️ System Environment"]:::srcStyle
        DotEnv["📄 .env File on Disk"]:::srcStyle
    end
    Config Sources --> PS["⚙️ BaseSettings Parser"]:::parseStyle
    PS --> Validate{"🔍 Strict Type Validation"}:::parseStyle
    Validate -->|Missing Secret / Invalid Type| Error["❌ Fail Fast: ValidationError"]:::errStyle
    Validate -->|Valid Config| SettingsObj["✅ Typed Settings Singleton"]:::passStyle
    SettingsObj --> App["🚀 FastAPI Application"]:::passStyle
```

---

## 💡 Core Theoretical Concepts

### 1. Declaring Configuration via `BaseSettings`

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Task Manager API"
    debug: bool = False
    database_url: str = "sqlite:///./tasks.db"
    secret_key: str  # Required! No default provided -> fails fast if not set
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### 2. Key Architectural Advantages

- **Fail-Fast Bootstrapping**: If `SECRET_KEY` is missing from the environment, the application refuses to start up, preventing insecure execution.
- **Type Casting**: Strings like `"false"`, `"0"`, or `"no"` are automatically parsed into boolean `False`.
- **Cached Singleton via `@lru_cache`**: Prevents repeatedly reading `.env` files from disk on every incoming HTTP request.
- **Dependency Injected Settings**: Settings can be injected into route handlers using `Depends(get_settings)`, enabling seamless mocking during unit and integration tests.

### 3. The `.env.example` Pattern

Never commit `.env` into git! Instead, commit a sanitized `.env.example` template with placeholder values:

```bash
# .env.example
APP_NAME="Task Manager API"
DEBUG=true
DATABASE_URL="sqlite:///./tasks.db"
SECRET_KEY="replace-with-a-real-cryptographic-secret-key-32-chars-minimum"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🎯 Task Specifications

Update `question/starter.py` to refactor all hardcoded secrets and paths into a validated `Settings` model.

### Requirements

1. Define `Settings` inheriting from `BaseSettings`.
2. Configure `model_config` pointing to `.env`.
3. Declare fields:
   - `app_name: str = "Task Manager API"`
   - `secret_key: str` (mandatory)
   - `database_url: str = "sqlite:///./tasks.db"`
   - `access_token_expire_minutes: int = 30`
   - `debug: bool = False`
4. Implement cached getter `get_settings()` with `@lru_cache`.
5. Wire `settings.database_url` into the database engine, and `settings.secret_key` into JWT token creation and verification functions.
6. Verify behavior when `.env` is absent vs present.

---

## 🛠️ Step-by-Step Implementation

1. Open `question/starter.py`.
2. Create `.env` from the provided `.env.example`.
3. Implement `Settings` class with `pydantic-settings`.
4. Replace hardcoded `SECRET_KEY` and `DATABASE_URL` with attributes from `settings`.
5. Launch app and verify `/docs` title reflects `settings.app_name`.

---

## 🧪 Verification Commands

```bash
# Test with custom environment variable overrides
SECRET_KEY="my-production-secret-key" DEBUG=true fastapi dev question/starter.py

# Verify settings in endpoint
curl -X GET http://127.0.0.1:8000/info
```

---

<div align="center">

[⏮️ Previous: 18 Migrations with Alembic](../18_migrations_alembic/README.md) • [📚 Course Overview](../README.md) • [Next: 20 Testing with Pytest ⏭️](../20_testing/README.md)

</div>
