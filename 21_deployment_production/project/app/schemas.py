"""Pydantic request/response schemas — separate from the DB models."""

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: str = Field(min_length=5, max_length=120)
    password: str = Field(min_length=6, max_length=128)


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    role: str


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    priority: int = Field(default=3, ge=1, le=5)


class TaskRead(BaseModel):
    id: int
    title: str
    priority: int
    done: bool
    owner_id: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
