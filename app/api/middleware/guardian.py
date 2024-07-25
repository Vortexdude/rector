from app.common.utils.timezone import timezone
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
        start_time = timezone.now()
        response = await call_next(request)
        end_time = timezone.now()
        total_time = (end_time - start_time).total_seconds() * 1000.0
        logger.info(
            f"logger=rector,{request.client.host=},{request.method=},{response.status_code=},{total_time:.5f}ms"
        )
        return response
