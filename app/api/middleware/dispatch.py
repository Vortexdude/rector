from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from app.common.utils.timezone import timezone
from app.core.config import logger


class DispatchMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = timezone.now()
        response = await call_next(request)
        end_time = timezone.now()
        logger.info(
            f"{request.client.host: <15} | {request.method: <8} | {response.status_code: <6} | " +
            f"{request.url.path: <15} | {(end_time - start_time).total_seconds() * 1000.0:.5f}ms"
        )
        return response
