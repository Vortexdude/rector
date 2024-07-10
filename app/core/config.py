from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

CURDIR = os.getcwd()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    DOMAIN: str = os.getenv('DOMAIN', "localhost")
    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'Rector')
    API_V1_STR: str = os.getenv('API_V1_STR', "/api/v1")
    SQLALCHEMY_DATABASE_URL: str = os.getenv('SQLALCHEMY_DATABASE_URL', "sqlite:///test.db")
    NURAL_NETWORK_STYLE_PATH: str = os.path.join(CURDIR, "app/models")
    UPLOAD_DIR: str = os.path.join(CURDIR, "app/uploads")
    OUTPUT_DIR: str = os.path.join(CURDIR, "app/outputs")
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', '12jh5439ck3s04jt94dsfsdpdfprad344784')


settings = Settings()
