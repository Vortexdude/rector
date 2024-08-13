from fastapi import APIRouter
from app.core.config import logger
from importlib import import_module
from app.core.config import settings

__all__ = ["api_router"]

api_router = APIRouter()

# dynamically add the routes using importlib module REFS - app/core/config.py
for route in settings.ACTIVE_ROUTES:
    logger.debug(f"importing route app.api.routes.{route} ")
    router = import_module(f'app.api.routes.{route}')
    api_router.include_router(router.router)
logger.debug(f"imported all the routes")
