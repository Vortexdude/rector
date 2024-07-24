from app.core.config import logger
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

__all__ = ["LoggingMiddleware"]


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        logger.info(f"Start {self.__class__.__name__}")
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:

        return await call_next(request)
