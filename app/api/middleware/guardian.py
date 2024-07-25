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
        if 'curl' in request.headers.get('user-agent'):
            os, device, browser = 'curl', 'curl', 'curl'
        else:
            os, device, browser = extract_user_info(request)

        host = request.client.host
        try:
            username = request.user.name
        except AttributeError:
            username = None
        print(f"{request.user.name}")
        method = request.method
        port = request.url.port
        url = request.url.path
        router = request.scope.get('route')
        summary = getattr(router, 'summary', None) or ''
        latency = f"{total_time:.5f}ms"
        print(f"{os=}, {device=}, {browser=}, {host=}, {username=}, {method=}, {summary=}")
        _record = {
            'os': os, 'device': device, 'browser': browser, 'host': host, 'username': username, 'url': url,
            'method': method, 'port': port, 'time': latency
        }
        UserActivity().set_info(**_record)

        return response
