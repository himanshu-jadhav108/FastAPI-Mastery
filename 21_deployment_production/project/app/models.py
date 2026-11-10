"""SQLModel table models."""

from sqlmodel import Field as SQLField
from sqlmodel import SQLModel


class User(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    username: str = SQLField(index=True, unique=True)
    email: str = SQLField(index=True, unique=True)
    hashed_password: str
    role: str = "user"


class Task(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    title: str
    priority: int = 3
    done: bool = False
    owner_id: int
