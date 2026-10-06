"""
Module 08 — Authentication: OAuth2 Password Flow + JWT
Run with: fastapi dev starter.py
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel, Field
from sqlmodel import Field as SQLField
from sqlmodel import Session, SQLModel, create_engine, select

SECRET_KEY = "dev-only-secret-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_URL = "sqlite:///./tasks_08.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

# TODO 1: password_hash = PasswordHash.recommended()
# def hash_password(password): return password_hash.hash(password)
# def verify_password(password, hashed): return password_hash.verify(password, hashed)


# TODO 2: User(SQLModel, table=True)
#   id: int | None = SQLField(default=None, primary_key=True)
#   username: str = SQLField(index=True, unique=True)
#   email: str = SQLField(index=True, unique=True)
#   hashed_password: str
#   is_active: bool = True


class Task(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    title: str
    priority: int = 3
    done: bool = False
    owner_id: int  # TODO 3 is really just noting this field exists


# TODO 4: UserCreate(BaseModel): username, email, password (with Field length limits)
# TODO 5: UserRead(BaseModel): id, username, email, is_active  (NO password/hash!)


SQLModel.metadata.create_all(engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app = FastAPI()


# TODO 6: create_access_token(subject: str, expires_delta: timedelta | None = None) -> str
# Build payload {"sub": subject, "exp": expire}, jwt.encode with SECRET_KEY/ALGORITHM.


def get_user_by_username(session: Session, username: str):
    return session.exec(select(User).where(User.username == username)).first()


@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: "UserCreate", session: SessionDep):
    # TODO 7: 409 if username or email already exists.
    # Hash the password, create + save a User, return it (response_model=UserRead).
    ...


@app.post("/auth/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
):
    # TODO 8: look up user, verify_password, 401 if either fails.
    # Create a token with create_access_token, return
    # {"access_token": token, "token_type": "bearer"}
    ...


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
):
    # TODO 9: jwt.decode the token (catch InvalidTokenError -> 401),
    # read "sub" from payload, look up the user, 401 if not found, return user.
    ...


CurrentUserDep = Annotated["User", Depends(get_current_user)]


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(title: str, current_user: CurrentUserDep, session: SessionDep):
    # TODO 10: create a Task with owner_id = current_user.id, save, return it
    ...


@app.get("/tasks/mine")
def my_tasks(current_user: CurrentUserDep, session: SessionDep):
    # TODO 11: return only tasks where owner_id == current_user.id
    ...
