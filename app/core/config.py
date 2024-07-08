from __future__ import annotations
from typing import Any, Callable, Set, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

CURDIR = os.getcwd()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    DOMAIN: str = "localhost"
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    NURAL_NETWORK_STYLE_PATH: str = os.path.join(CURDIR, "app/models")
    UPLOAD_DIR: str = os.path.join(CURDIR, "app/uploads")
    OUTPUT_DIR: str = os.path.join(CURDIR, "app/outputs")


settings = Settings()
