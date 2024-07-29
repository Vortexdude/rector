from starlette.requests import Request
from starlette.responses import Response
from .common import Middleware
from app.common.utils.timezone import timezone
from app.core.config import logger
from app.common.utils.parsers import extract_user_info
from app.api.services.logging.main import UserActivity

__all__ = ["LoggingMiddleware"]


class LoggingMiddleware(Middleware):

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = timezone.now()
        response = await call_next(request)
        end_time = timezone.now()
        total_time = (end_time - start_time).total_seconds() * 1000.0
        logger.info(
            f"logger=rector,{request.client.host=},{request.method=},{response.status_code=},{total_time:.5f}ms"
        )
        try:
            os, device, browser = extract_user_info(request)
        except KeyError:
            os, device, browser = "null", "null", "null"

        host = request.client.host
        try:
            username = request.user.name
        except AttributeError:
            username = None
        method = request.method
        port = request.url.port or 8000
        url = request.url.path
        latency = f"{total_time:.5f}ms"
        _record = {
            'os': os, 'device': device, 'browser': browser, 'host': host, 'username': username, 'url': url,
            'method': method, 'port': port, 'time': latency
        }
        await UserActivity().set_info(**_record)

        return response
