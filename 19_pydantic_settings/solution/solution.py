"""
Module 19 — Settings Management with pydantic-settings — SOLUTION
Copy .env.example to .env first (and set a real SECRET_KEY), then run:
    fastapi dev solution.py
"""

from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite:///./tasks_19.db"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]

app = FastAPI()


@app.get("/config-check")
def config_check(settings: SettingsDep):
    return {
        "debug": settings.debug,
        "algorithm": settings.algorithm,
        "database_url": settings.database_url,
    }


def create_access_token(subject: str, settings: Settings) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


@app.post("/demo-token")
def demo_token(username: str, settings: SettingsDep):
    token = create_access_token(username, settings)
    return {"access_token": token, "token_type": "bearer"}
