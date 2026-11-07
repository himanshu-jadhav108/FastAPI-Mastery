"""
Minimal SQLModel app for the Alembic exercise.

Start with this. Step 5 of the README asks you to add `due_date` here
and generate a second migration for it.
"""

from sqlmodel import Field as SQLField
from sqlmodel import SQLModel


class Task(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    title: str
    priority: int = 3
    done: bool = False
    # Step 5: add   due_date: str | None = None   here, then generate
    # a new migration for it.
