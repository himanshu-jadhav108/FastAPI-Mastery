"""
Module 09 — Role-Based Authorization — SOLUTION
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

DATABASE_URL = "sqlite:///./tasks_09.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

password_hash = PasswordHash.recommended()


def hash_password(p: str) -> str:
    return password_hash.hash(p)


def verify_password(p: str, h: str) -> bool:
    return password_hash.verify(p, h)


class User(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    username: str = SQLField(index=True, unique=True)
    email: str = SQLField(index=True, unique=True)
    hashed_password: str
    role: str = "user"


class Task(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    title: str
    owner_id: int


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: str = Field(min_length=5, max_length=120)
    password: str = Field(min_length=6, max_length=128)


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    role: str


SQLModel.metadata.create_all(engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
app = FastAPI()


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    return jwt.encode({"sub": subject, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def get_user_by_username(session: Session, username: str):
    return session.exec(select(User).where(User.username == username)).first()


@app.post("/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, session: SessionDep):
    if get_user_by_username(session, user_data.username):
        raise HTTPException(status.HTTP_409_CONFLICT, "Username already exists.")
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@app.post("/auth/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = get_user_by_username(session, form_data.username)
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect username or password")
    return {"access_token": create_access_token(user.username), "token_type": "bearer"}


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep) -> User:
    err = HTTPException(status.HTTP_401_UNAUTHORIZED, "Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise err
    except InvalidTokenError:
        raise err
    user = get_user_by_username(session, username)
    if user is None:
        raise err
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def require_role(required_role: str):
    def role_checker(current_user: CurrentUserDep) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                f"Requires '{required_role}' role.",
            )
        return current_user
    return role_checker


@app.get("/admin/users", response_model=list[UserRead])
def list_all_users(
    session: SessionDep,
    _admin: Annotated[User, Depends(require_role("admin"))],
):
    return session.exec(select(User)).all()


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(title: str, current_user: CurrentUserDep, session: SessionDep):
    task = Task(title=title, owner_id=current_user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: CurrentUserDep, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    if task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your task.")
    session.delete(task)
    session.commit()
    return {"deleted": task_id}


@app.patch("/tasks/{task_id}/reassign")
def reassign_task(
    task_id: int,
    new_owner_id: int,
    session: SessionDep,
    _admin: Annotated[User, Depends(require_role("admin"))],
):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    task.owner_id = new_owner_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
