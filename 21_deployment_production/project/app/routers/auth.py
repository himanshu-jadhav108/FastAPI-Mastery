"""Auth routes — SOLUTION."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..database import SessionDep
from ..dependencies import get_user_by_username
from ..models import User
from ..schemas import TokenResponse, UserCreate, UserRead
from ..security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
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


@router.post("/login", response_model=TokenResponse)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = get_user_by_username(session, form_data.username)
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect username or password")
    return {"access_token": create_access_token(user.username), "token_type": "bearer"}
