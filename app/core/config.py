from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from .pathconf import BasePath, SQLITE_DATABASE_FILE
from app.common.utils.log import Logger

load_dotenv()
__all__ = ["settings", "logger"]


class PSQL:
    @property
    def uri(self) -> str:
        POSTGRES = {
            'user': os.getenv('POSTGRES_USER', 'rector'),
            'pw': os.getenv('POSTGRES_PASSWORD', 'rector'),
            'host': os.getenv('POSTGRES_HOST'),
            'db': os.getenv('POSTGRES_DB', 'rector'),
        }
        if not POSTGRES['host']:
            logger.debug("info")
            return SQLITE_DATABASE_FILE

        return "postgresql+psycopg2://%(user)s:%(pw)s@%(host)s:5432/%(db)s" % POSTGRES


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{BasePath}/.env", env_ignore_empty=True, extra="ignore"
    )
    SERVER_HOST: str = os.getenv('SERVER_HOST', "127.0.0.1")
    SERVER_PORT: int = os.getenv('SERVER_PORT', 8000)
    DOMAIN: str = os.getenv('DOMAIN', "localhost")
    ENV: str = os.getenv("ENV", "dev")
    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'Rector')
    API_V1_STR: str = os.getenv('API_V1_STR', "/api/v1")
    DOCS_URL: str = os.getenv('DOCS_URL', f'{API_V1_STR}/docs')
    REDOCS_URL: str = os.getenv('REDOCS_URL', f'{API_V1_STR}/redocs')
    OPENAPI_URL: str = os.getenv('OPENAPI_URL', f'{API_V1_STR}/openapi')
    DESCRIPTION: str = os.getenv('DESCRIPTION', 'FastAPI Best Architecture')
    SQLALCHEMY_DATABASE_URL: str = PSQL().uri

    # filepaths
    NURAL_NETWORK_STYLE_PATH: str = os.path.join(BasePath, "models")
    UPLOAD_DIR: str = os.path.join(BasePath, "uploads")
    OUTPUT_DIR: str = os.path.join(BasePath, "outputs")

    # JWT Config
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', '12jh5439ck3s04jt94dsfsdpdfprad344784')
    TOKEN_ALGORITHM: str = 'HS256'
    ACTIVE_ROUTES: list = ['auth', 'transform_image', 'ssl_cert_util', 'video_transcoding', 'cloud']

    # logging
    LOGFILE_PATH: str = os.path.join(BasePath, "log")

    # DateTime
    DATETIME_TIMEZONE: str = 'Asia/Kolkata'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'
    TOKEN_EXPIRE_SECONDS: int = 900  # 15 minutes

    # middleware
    API_REQUEST_PER_MINUTE: int = 10

    # routes
    UNAUTHENTICATED_ROUTES: list[str] = [
        "/favicon.ico",
        f'{API_V1_STR}/login',
        f'{API_V1_STR}/docs',
        f'{API_V1_STR}/redocs',
        f'{API_V1_STR}/openapi'
        f'{API_V1_STR}/signup',
        f'{API_V1_STR}/ec2/',
        f'{API_V1_STR}/s3/',
        f'/api/v1/openapi',
        f"/api/v1/signup"
    ]

    UNAUTHENTICATED_FILTER: list[str] = [".html", ".m3u8"]
    BASE_PATH: Path = BasePath
    BASE_URL: str = f"http://192.168.1.76:{SERVER_PORT}{API_V1_STR}"


settings = Settings()
logger_namespace = os.path.basename(BasePath.parent)
log_init = Logger('debug', logger_namespace=logger_namespace, logfile=settings.LOGFILE_PATH)
logger = log_init.get_logger()
