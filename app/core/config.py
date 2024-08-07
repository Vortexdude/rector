from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv
from functools import lru_cache
from app.common.utils.log import Logger
from .pathconf import BasePath, SQLITE_DATABASE_FILE
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()
__all__ = ["settings", "logger"]


class PostgresSecret(BaseSettings):
    user: str
    password: str
    db: str
    host: str = "127.0.0.1"
    port: int

    model_config = SettingsConfigDict(env_prefix="POSTGRES_", )


class DATABASE:
    @property
    def uri(self) -> str:
        if os.getenv("ENV") == 'development':
            return SQLITE_DATABASE_FILE

        _pg: PostgresSecret = PostgresSecret()

        POSTGRES = {
            'user': _pg.user,
            'pw': _pg.password,
            'host': _pg.host,
            'db': _pg.db,
            'port': str(_pg.port),
        }

        return "postgresql+psycopg2://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{BasePath}/.env", env_ignore_empty=True, extra="ignore"
    )
    SSL: bool = False
    # filepaths
    NURAL_NETWORK_STYLE_PATH: str = os.path.join(BasePath, "models")
    UPLOAD_DIR: str = os.path.join(BasePath, "uploads")
    OUTPUT_DIR: str = os.path.join(BasePath, "outputs")

    # JWT Config
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = 'HS256'
    ACTIVE_ROUTES: list = ['auth', 'transform_image', 'ssl_cert_util', 'video_transcoding', 'cloud']

    # logging
    LOGFILE_PATH: str = os.path.join(BasePath, "log")

    # DateTime
    DATETIME_TIMEZONE: str = 'Asia/Kolkata'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'
    TOKEN_EXPIRE_SECONDS: int = 900  # 15 minutes

    # middleware
    API_REQUEST_PER_MINUTE: int = 10
    SERVER_HOST: str = '0.0.0.0'
    SERVER_PORT: int = 8000
    DOMAIN: str = 'localhost'
    ENV: str = 'dev'
    PROJECT_NAME: str = 'rector'
    API_V1_STR: str = os.getenv('API_V1_STR', "/api/v1")
    if SSL:
        BASE_URL: str = f"https://192.168.1.76:{SERVER_PORT}{API_V1_STR}"
    else:
        BASE_URL: str = f"http://192.168.1.76:{SERVER_PORT}{API_V1_STR}"
    DOCS_URL: str = os.getenv('DOCS_URL', f'{API_V1_STR}/docs')
    REDOCS_URL: str = os.getenv('REDOCS_URL', f'{API_V1_STR}/redocs')
    OPENAPI_URL: str = os.getenv('OPENAPI_URL', f'{API_V1_STR}/openapi')
    DESCRIPTION: str = os.getenv('DESCRIPTION', 'FastAPI Best Architecture')
    SQLALCHEMY_DATABASE_URL: str = DATABASE().uri

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
        f"/api/v1/signup",
        f"/api/v1/videos"
    ]

    UNAUTHENTICATED_FILTER: list[str] = [".html", ".m3u8", '.ts']
    BASE_PATH: Path = BasePath


class DevelopmentConfig(BaseConfig):
    ENV: str = 'development'
    API_REQUEST_PER_MINUTE: int = 50
    JWT_SECRET_KEY: str = '12jh5439ck3s04jt94dsfsdpdfprad344784'
    SERVER_HOST: str = '127.0.0.1'


class ProductionConfig(BaseConfig):
    ENV: str = 'production'
    API_REQUEST_PER_MINUTE: int = 20
    JWT_SECRET_KEY: str = '12jh5439ck3s04jt94ad344784t0u7'
    SERVER_HOST: str = '0.0.0.0'


@lru_cache()
def get_settings() -> BaseSettings:
    config_cls_dict = {
        'development': DevelopmentConfig,
        'production': ProductionConfig
    }
    config_name = os.environ.get('ENV', 'development')
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
logger_namespace = os.path.basename(BasePath.parent)
log_init = Logger('debug', logger_namespace=logger_namespace, logfile=settings.LOGFILE_PATH)
logger = log_init.get_logger()
