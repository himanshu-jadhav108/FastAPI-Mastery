# 18 — Migrations with Alembic

## Theory

Every module so far used `SQLModel.metadata.create_all(engine)` — great
for a fresh database, useless once real data exists. If you add a column
to a model, `create_all` does **nothing** for existing tables (it only
creates tables that don't exist yet). **Migrations** are versioned,
incremental changes to your schema that can be applied to a database that
already has data in it — and rolled back if something goes wrong.

**Alembic** is SQLAlchemy's migration tool (SQLModel is built on
SQLAlchemy, so it works directly).

### One-time setup

```bash
pip install alembic
alembic init alembic
```

This creates an `alembic/` folder and `alembic.ini`. Two files matter:

**`alembic.ini`** — set the database URL:
```ini
sqlalchemy.url = sqlite:///./tasks.db
```

**`alembic/env.py`** — point it at your models so autogenerate can see
them:
```python
from app.models import SQLModel  # import your models module
target_metadata = SQLModel.metadata
```

### Day-to-day workflow

1. Change a model (add a field, rename something, add a table).
2. Autogenerate a migration by diffing your models against the current
   DB schema:
   ```bash
   alembic revision --autogenerate -m "add priority to task"
   ```
   This writes a new file in `alembic/versions/` with `upgrade()` and
   `downgrade()` functions — **always read the generated file**;
   autogenerate is a good first draft, not infallible (it can miss
   renames, seeing them as a drop+add instead).
3. Apply it:
   ```bash
   alembic upgrade head
   ```
4. If something's wrong, roll back one step:
   ```bash
   alembic downgrade -1
   ```

Alembic tracks which migrations have run in a table it creates called
`alembic_version` — so `alembic upgrade head` is always safe to re-run;
it only applies what hasn't been applied yet.

### A generated migration looks like this

```python
"""add priority to task

Revision ID: a1b2c3d4e5f6
Revises: (previous revision id)
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column("task", sa.Column("priority", sa.Integer(), nullable=False, server_default="3"))

def downgrade():
    op.drop_column("task", "priority")
```

## Task

This module has no `starter.py`/`solution.py` — it's a hands-on CLI
exercise using the `project/` folder (a minimal SQLModel app). Alembic
has already been initialized and wired up for you (see `NOTES.md` for
exactly what setup was done and why) so you can jump straight to the
part that's actually about migrations.

1. `cd` into `project/`, `pip install alembic` if you haven't already.
2. Run `alembic revision --autogenerate -m "initial tables"`. Open the
   generated file in `alembic/versions/` and read it — confirm it
   creates the `task` table with `id`, `title`, `priority`, `done`.
3. Run `alembic upgrade head`. Confirm `tasks_18.db` now exists with a
   `task` table (`sqlite3 tasks_18.db ".schema task"` or any SQLite
   browser).
4. Open `project/app/models.py`, add a new field `due_date: str | None =
   None` to `Task`.
5. Run `alembic revision --autogenerate -m "add due date to task"`,
   inspect the generated file (confirm it adds exactly **one** column —
   this is the "always read the generated file" habit from the theory
   section), then `alembic upgrade head`.
6. Confirm the column exists in the schema.
7. Practice a rollback: `alembic downgrade -1`, confirm the column is
   gone, then `alembic upgrade head` again to restore it.

**Read `NOTES.md` before step 2** — it documents one real gotcha you'd
otherwise hit (a `NameError: name 'sqlmodel' is not defined` inside a
generated migration) and how this project avoids it.
