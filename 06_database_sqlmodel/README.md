# 06 — Database with SQLModel

## Theory

Everything so far lived in a Python list that reset every time you
restarted the server. Real apps need a database.

**SQLModel** (by the FastAPI author) combines Pydantic + SQLAlchemy: one
class is *both* your validation schema and your database table.

```python
from sqlmodel import SQLModel, Field as SQLField

class Task(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    title: str
    priority: int = 3
    done: bool = False
```

`table=True` tells SQLModel this is a real database table, not just a
validation schema.

**Engine** — the connection to the database file/server:

```python
from sqlmodel import create_engine

DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
```

`connect_args={"check_same_thread": False}` is SQLite-specific — it allows
the connection to be used across the different threads FastAPI may run
requests on.

**Sessions** — a session is a "conversation" with the database for one
request. You get a fresh one per-request via a `yield` dependency:

```python
from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
```

The `with` block guarantees the session closes even if the request
errors out. This is the same `yield`-dependency pattern from module 05.

**Creating tables:**

```python
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```

Call this once at startup (you'll formalize "at startup" with lifespan
events in module 14 — for now just call it directly at import time).

**Basic session operations:**

```python
session.add(task)      # stage an insert/update
session.commit()       # write it to the database
session.refresh(task)  # reload it (gets the auto-generated id back)

session.get(Task, task_id)              # fetch by primary key
session.exec(select(Task)).all()        # fetch all rows
```

## Task

Open `starter.py`.

1. Define `Task` as a `SQLModel` table: `id`, `title`, `priority` (default
   3), `done` (default `False`).
2. Set up the engine (SQLite file `tasks.db`) and `create_db_and_tables()`.
3. Write `get_session()` and a `SessionDep` alias.
4. `POST /tasks` → accept a `Task` body (SQLModel classes work directly as
   request bodies too), save it, return it.
5. `GET /tasks` → `session.exec(select(Task)).all()`
6. `GET /tasks/{task_id}` → `session.get(Task, task_id)`, 404 if `None`.

Run it, create a few tasks, then **stop the server and restart it** —
confirm the tasks are still there. That's the whole point of this module.
