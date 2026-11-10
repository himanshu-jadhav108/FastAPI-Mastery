<div align="center">

# 🛠️ Module 00: Environment Setup & Tooling

[![Level](https://img.shields.io/badge/Level-Foundations-green?style=for-the-badge)](#)
[![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)](#)

[📚 Course Overview](../README.md) • [Next: 01 Basics ⏭️](../01_basics/README.md)

---

</div>

## 📌 Architectural Overview

FastAPI is a modern, high-performance web framework for building APIs with Python 3.10+ based on standard Python type hints. Unlike legacy frameworks, FastAPI is built on two battle-tested pillars:

1. **Starlette**: Powers the lightning-fast web routing, ASGI core engine, WebSockets, and background tasks.
2. **Pydantic**: Powers data parsing, schema validation, serialization, and automated OpenAPI 3.1 generation.

```
                           +--------------------------------+
                           |       Client HTTP Request      |
                           +--------------------------------+
                                           |
                                           v
                           +--------------------------------+
                           |       Uvicorn (ASGI Server)    |
                           +--------------------------------+
                                           |
                                           v
       +------------------------------------------------------------------------+
       |                           FastAPI Layer                                |
       |                                                                        |
       |  [Starlette Web Routing] <=====> [Pydantic Validation & Serialization] |
       +------------------------------------------------------------------------+
                                           |
                                           v
                           +--------------------------------+
                           |      HTTP JSON / WS Response   |
                           +--------------------------------+
```

---

## 🎯 What Makes FastAPI Different?

| Feature             | FastAPI                                                 | Traditional Frameworks (e.g. Flask)      |
| :------------------ | :------------------------------------------------------ | :--------------------------------------- |
| **Type Validation** | Native & automatic via Pydantic type annotations        | Manual payload checks / external plugins |
| **Concurrency**     | Native `async` / `await` ASGI event loop                | WSGI blocking or complex threading       |
| **Documentation**   | Auto-generated interactive Swagger UI (`/docs`) & ReDoc | Manual OpenAPI / Postman syncing         |
| **Performance**     | On par with NodeJS and Go (via Starlette & Uvicorn)     | Higher overhead per request              |

---

## 🚀 Environment Setup

### 1. Create and Activate Virtual Environment

```bash
# Navigate to the project root
cd d:/Learnings/fastapi-course

# Create virtual environment
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Linux / macOS:
source venv/bin/activate
```

### 2. Install Project Dependencies

```bash
pip install -r requirements.txt
```

#### What We Install & Why

- `fastapi`: Core API framework.
- `uvicorn[standard]`: Blazing-fast ASGI server with cythonized HTTP parsers and event loops.
- `sqlmodel`: Ergonomic combination of SQLAlchemy ORM + Pydantic models.
- `sqlalchemy[asyncio]`, `asyncpg`, `aiosqlite`: Modern async database drivers for high concurrency.
- `pyjwt`, `pwdlib[argon2]`: Military-grade cryptographic password hashing and JWT token handling.
- `python-multipart`: Required to parse form bodies, OAuth2 token requests, and file uploads.
- `alembic`: Database migration tool for versioned schema evolutions.
- `pydantic-settings`: 12-factor configuration management from `.env` files.
- `pytest`, `httpx`: High-speed in-process testing harness.

---

## 💻 Running Any Module

FastAPI provides the modern `fastapi dev` CLI tool for instant hot-reloading development:

```bash
# Using the FastAPI CLI (Recommended)
fastapi dev starter.py

# Or using Uvicorn directly
uvicorn starter:app --reload --host 127.0.0.1 --port 8000
```

Once running, access:

- 📖 **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`
- 📑 **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`
- 📜 **Raw OpenAPI Schema**: `http://127.0.0.1:8000/openapi.json`

---

## 🧪 Verification Check

Verify that your Python environment has FastAPI properly installed and accessible:

```bash
python -c "import fastapi; print(f'FastAPI version {fastapi.__version__} successfully initialized!')"
```

If a valid version number prints without errors, you are ready to build!

---

<div align="center">

[📚 Course Overview](../README.md) • [Next: 01 Basics ⏭️](../01_basics/README.md)

</div>
