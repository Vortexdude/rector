from fastapi import APIRouter
from importlib import import_module
from app.core.config import settings

api_router = APIRouter()

# dynamically add the routes using importlib module REFS - app/core/config.py
for route in settings.ACTIVE_ROUTES:
    router = import_module(f'app.api.routes.{route}')
    api_router.include_router(router.router)
