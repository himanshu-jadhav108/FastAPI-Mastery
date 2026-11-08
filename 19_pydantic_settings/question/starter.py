"""
Module 19 — Settings Management with pydantic-settings
Copy .env.example to .env first (and set a real SECRET_KEY), then run:
    fastapi dev starter.py
"""

from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict


# TODO 1: class Settings(BaseSettings):
#     model_config = SettingsConfigDict(env_file=".env", extra="ignore")
#     secret_key: str
#     algorithm: str = "HS256"
#     access_token_expire_minutes: int = 30
#     database_url: str = "sqlite:///./tasks_19.db"
#     debug: bool = False


# TODO 2: @lru_cache
# def get_settings() -> Settings:
#     return Settings()
# SettingsDep = Annotated[Settings, Depends(get_settings)]


app = FastAPI()


@app.get("/config-check")
def config_check(settings: "SettingsDep"):
    # TODO 3: return {"debug": ..., "algorithm": ..., "database_url": ...}
    # Deliberately do NOT include settings.secret_key in the response.
    ...


def create_access_token(subject: str, settings: "Settings") -> str:
    # TODO 4: use settings.secret_key, settings.algorithm,
    # settings.access_token_expire_minutes instead of hardcoded constants.
    ...


@app.post("/demo-token")
def demo_token(username: str, settings: "SettingsDep"):
    token = create_access_token(username, settings)
    return {"access_token": token, "token_type": "bearer"}
