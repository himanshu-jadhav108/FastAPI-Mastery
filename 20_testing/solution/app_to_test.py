"""
Module 20 — the app under test.
A small, complete Task Manager (CRUD + auth) reused from earlier modules.
You don't need to modify this file — write tests against it in test_app.py.
"""

from contextlib import asynccontextmanager
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

SECRET_KEY = "test-secret-key"
ALGORITHM = "HS256"

DATABASE_URL = "sqlite:///./tasks_20.db"
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


class Task(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    title: str
    done: bool = False
    owner_id: int


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: str = Field(min_length=5, max_length=120)
    password: str = Field(min_length=6, max_length=128)


class UserRead(BaseModel):
    id: int
    username: str
    email: str


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)


class TaskRead(BaseModel):
    id: int
    title: str
    done: bool
    owner_id: int


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@app.get("/health")
def health():
    return {"status": "ok"}


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    return jwt.encode({"sub": subject, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def get_user_by_username(session: Session, username: str):
    return session.exec(select(User).where(User.username == username)).first()


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


@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, current_user: CurrentUserDep, session: SessionDep):
    new_task = Task(title=task.title, owner_id=current_user.id)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, update: TaskUpdate, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: CurrentUserDep, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    if task.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your task.")
    session.delete(task)
    session.commit()
    return {"deleted": task_id}
