# Setup notes — what's already been done in `project/`

`alembic init alembic` was already run in `project/`, and two files were
edited so autogenerate works against the `Task` model:

### `alembic.ini`
```ini
sqlalchemy.url = sqlite:///./tasks_18.db
```

### `alembic/env.py`
Two additions near the top:
```python
from sqlmodel import SQLModel
from app.models import Task  # noqa: F401  (import so it registers on SQLModel.metadata)
```
and:
```python
target_metadata = SQLModel.metadata
```
(replacing the generated `target_metadata = None`).

## The gotcha this setup avoids

By default, a migration Alembic autogenerates for a SQLModel `str` field
references `sqlmodel.sql.sqltypes.AutoString()` — but the generated file
doesn't import `sqlmodel` by default, only `sqlalchemy as sa`. Running
that migration as-is fails with:

```
NameError: name 'sqlmodel' is not defined
```

This project's `alembic/script.py.mako` (the template Alembic uses to
generate every new migration file) has one added line:

```python
import sqlalchemy as sa
import sqlmodel        # <- added
```

So every migration generated in this project already has the import it
needs. If you ever run `alembic init` yourself on a new project, add this
same line to `script.py.mako` before generating your first migration —
it's a one-time fix, not something to redo per-migration.

## If you want to do the full setup yourself from scratch

1. `pip install alembic`
2. `alembic init alembic`
3. Edit `alembic.ini` and `alembic/env.py` as shown above
4. Add `import sqlmodel` to `alembic/script.py.mako` as shown above
5. Continue with the README's steps
