"""Password hashing and JWT helpers."""

import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

# In production this MUST come from a real environment variable / secrets
# manager (see module 19). This default only exists so the app doesn't
# crash if you forget to set it locally — never rely on it for anything
# beyond your own laptop.
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-secret-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
