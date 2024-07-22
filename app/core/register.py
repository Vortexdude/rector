from fastapi import FastAPI
from app.api import routes
from app.core.config import settings, logger
from app.core.db import Base, engine

__all__ = ["register_app"]


def register_app():
    register_db()
    register_logger()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        openapi_url=settings.OPENAPI_URL,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
    )
    app.logger = logger
    register_logger()
    register_middleware()
    register_routes(app)
    register_exceptions()

    return app


def register_logger() -> None:
    import logging
    # adding the passlib logger to get rid of the warning about the version of bcrypt
    # https://github.com/pyca/bcrypt/issues/684#issuecomment-1858400267
    logging.getLogger('passlib').setLevel(logging.ERROR)


def register_middleware() -> None:
    pass


def register_routes(app) -> None:
    app.include_router(prefix=settings.API_V1_STR, router=routes.api_router)


def register_exceptions() -> None:
    pass


def register_db() -> None:
    Base.metadata.create_all(bind=engine)
