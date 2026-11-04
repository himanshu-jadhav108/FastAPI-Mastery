"""Reusable dependencies: current user, role checks."""

from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import select

from .database import SessionDep
from .models import User
from .security import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_by_username(session, username: str):
    return session.exec(select(User).where(User.username == username)).first()


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> User:
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
