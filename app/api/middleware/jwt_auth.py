import typing
from typing import Any
from starlette.authentication import AuthenticationBackend
from fastapi import Request, Response
from app.core.config import logger
from app.common.security.jwt_util import JWTUtil
from app.common.exceptions.errors import TokenError
from starlette.authentication import AuthenticationError, AuthCredentials
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse
import msgspec


skip_route: list = ["/api/v1/login", "/api/v1/docs", "/api/v1/redocs", "/api/v1/openapi"]


class MsgSpecJsonResponse(JSONResponse):
    """
    Json Response using high-performance msgspec library to serialize data into JSON
    """

    def render(self, content: Any) -> bytes:
        return msgspec.json.encode(content)


class _AuthenticateError(AuthenticationError):
    def __init__(self, *, code: int = None, msg: str = None, headers: dict[str, Any] = None):
        self.code = code
        self.msg = msg
        self.headers = headers


class JWTAuthMiddleware(AuthenticationBackend):

    @staticmethod
    def auth_exception_handler(conn: HTTPConnection, exc: _AuthenticateError) -> Response:
        return MsgSpecJsonResponse(content={"code": exc.code, "msg": exc.msg, "data": None}, status_code=exc.code)

    async def authenticate(self, request: Request):
        auth = request.headers.get("Authorization")
        if request.url.path in skip_route:
            return

        if not auth:
            logger.error(f"Token Header is missing from the request")
            return

        scheme, token = auth.split()
        if scheme.lower() != 'bearer':
            logger.error(f"Token type not matched")
            return
        try:
            email = JWTUtil.decode_token(token=token)
            user = JWTUtil.get_user_by_email(email)

        except TokenError as exc:
            raise _AuthenticateError(code=exc.code, msg=exc.detail, headers=exc.headers)

        except Exception as e:
            logger.error(e)
            raise _AuthenticateError(code=getattr(e, 'code', 500), msg=getattr(e, 'msg', 'Internal Server Error'))

        # more https://www.starlette.io/authentication
        return AuthCredentials(['authenticated']), user
