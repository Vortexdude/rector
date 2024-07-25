from typing import Any
from starlette.authentication import AuthenticationBackend
from fastapi import Request, Response
from app.core.config import logger, settings
from app.common.security.jwt_util import JWTUtil
from app.common.exceptions.errors import TokenError
from app.common.responses.main import StandardResponseCode
from starlette.authentication import AuthenticationError, AuthCredentials, SimpleUser
from starlette.requests import HTTPConnection
from app.common.encodes.msgspec import MsgSpecJsonResponse


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
        if request.url.path in settings.UNAUTHENTICATED_ROUTES:
            return

        if not auth:
            logger.error(f"Token Header is missing from the request")
            if settings.ENV == 'dev':
                return
            raise _AuthenticateError(
                code=StandardResponseCode.HTTP_401,
                msg="Authentication header require",
                headers={"WWW-Authenticated": "Bearer"}
            )

        scheme, token = auth.split()
        if scheme.lower() != 'bearer':
            logger.error(f"Token type not matched")
            if settings.ENV == 'dev':
                return
            raise _AuthenticateError(
                code=StandardResponseCode.HTTP_400,
                msg="Authentication token is not matched",
                headers={"WWW-Authenticated": "Bearer"}
            )
        try:
            email = JWTUtil.decode_token(token=token)
            user = JWTUtil.get_user_by_email(email)

        except TokenError as exc:
            raise _AuthenticateError(code=exc.code, msg=exc.detail, headers=exc.headers)

        except Exception as e:
            logger.error(e)
            raise _AuthenticateError(code=getattr(e, 'code', 500), msg=getattr(e, 'msg', 'Internal Server Error'))

        # more https://www.starlette.io/authentication
        return AuthCredentials(['authenticated']), SimpleUser(user)
