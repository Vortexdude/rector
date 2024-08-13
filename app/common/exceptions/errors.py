from typing import Any
from fastapi import HTTPException
from app.common.responses.main import StandardResponseCode


class HTTPError(HTTPException):
    def __init__(self, *, code: int, msg: str = None, headers: dict[str, Any] = None):
        super().__init__(status_code=code, detail=msg, headers=headers)


class TokenError(HTTPError):
    code = StandardResponseCode.HTTP_401

    def __init__(self, *, msg: str = "Not Authenticated", headers: dict[str, Any] = None):
        super().__init__(code=self.code, msg=msg, headers=headers or {"WWW-Authenticated": "Bearer"})


class AwsConnectionError(HTTPError):
    code = StandardResponseCode.HTTP_502

    def __init__(self, *, msg: str = "Cant able to communication with AWS servers", headers: dict[str, Any] = None):
        super().__init__(code=self.code, msg=msg, headers=headers or {"WWW-Authentication-Bearer"})
