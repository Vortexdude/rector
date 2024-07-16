from __future__ import annotations
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.common.utils. files import model_list
from .pathconf import BasePath, SQLITE_DATABASE_FILE


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{BasePath}/.env", env_ignore_empty=True, extra="ignore"
    )
    DOMAIN: str = os.getenv('DOMAIN', "localhost")
    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'Rector')
    API_V1_STR: str = os.getenv('API_V1_STR', "/api/v1")
    DOCS_URL: str = os.getenv('DOCS_URL', f'{API_V1_STR}/docs')
    REDOCS_URL: str = os.getenv('REDOCS_URL', f'{API_V1_STR}/redocs')
    OPENAPI_URL: str = os.getenv('OPENAPI_URL', f'{API_V1_STR}/openapi')
    DESCRIPTION: str = os.getenv('DESCRIPTION',  'FastAPI Best Architecture')
    SQLALCHEMY_DATABASE_URL: str = os.getenv('SQLALCHEMY_DATABASE_URL', SQLITE_DATABASE_FILE)
    NURAL_NETWORK_STYLE_PATH: str = os.path.join(BasePath, "models")
    UPLOAD_DIR: str = os.path.join(BasePath, "uploads")
    OUTPUT_DIR: str = os.path.join(BasePath, "outputs")
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', '12jh5439ck3s04jt94dsfsdpdfprad344784')
    TOKEN_ALGORITHM: str = 'HS256'
    ACTIVE_ROUTES: list = ['auth', 'transform_image', 'ssl_cert_util']
    MODEL_LIST: list = model_list(BasePath)

    # DateTime
    DATETIME_TIMEZONE: str = 'Asia/Kolkata'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'
    TOKEN_EXPIRE_SECONDS: int = 900  # 15 minutes


settings = Settings()
