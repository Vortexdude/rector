from typing import Annotated
from fastapi import Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer
from fastapi.param_functions import Form
from typing_extensions import Doc


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


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_request_form = Annotated[OAuth2PasswordRequestForm, Depends()]
