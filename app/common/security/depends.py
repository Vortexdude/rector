from typing import Annotated, Optional
from fastapi import Depends
from fastapi.security import OAuth2
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Form
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_401_UNAUTHORIZED
from typing_extensions import Doc
from starlette.requests import Request
from .jwt_util import login_required

__all__ = ["user_identity_dependency"]


class OpenapiLogin:
    def __init__(
            self,
            *,
            email: Annotated[
                str,
                Form(),
                Doc(
                    """
                    `email` string. The OAuth2 spec requires the exact field name
                    `email`.
                    """
                ),
            ],
            password: Annotated[
                str,
                Form(),
                Doc(
                    """
                    `password` string. The OAuth2 spec requires the exact field name
                    `password".
                    """
                )
            ]
    ):
        self.email = email
        self.password = password


class Oauth2ClientCredentials(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


# For Annotated the first argument is class or type of the datatype and other is dependency or empty
user_identity_dependency = Annotated[str, Depends(login_required)]
