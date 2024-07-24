import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from passlib.context import CryptContext
from fastapi import Request
from datetime import timedelta
from .exceptions import credentials_exception
from app.common.utils.timezone import timezone
from app.core.config import settings, logger
from app.api.models.jwt import TokenData
from app.core.db import get_db
from app.api.models.users import User
from app.common.exceptions.errors import TokenError
from sqlalchemy.orm import Session

__all__ = ["JWTUtil", "get_current_user", "login_required"]

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class JWTUtil:
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Encrypt passwords using the hash algorithm

        :param password:
        :return:
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_text, hashed_text):
        """
        Password verification

        :param plain_text: The password to verify
        :param hashed_text: The hash ciphers to compare
        :return:
        """
        return pwd_context.verify(plain_text, hashed_text)

    @staticmethod
    def create_access_token(data: dict, expire_delta: timedelta | None = None, **kwargs) -> str:
        to_encode = data.copy()
        if expire_delta:
            expire = timezone.now() + expire_delta
            expire_seconds = int(expire_delta.seconds)
        else:
            expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
            expire_seconds = settings.TOKEN_EXPIRE_SECONDS

        to_encode.update({'exp': expire, **kwargs})
        token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.TOKEN_ALGORITHM)
        return token

    @staticmethod
    def decode_token(token: str) -> str:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
            user_email = payload.get('sub')
            if not user_email:
                raise TokenError(msg="Invalid Token")

        except ExpiredSignatureError:
            raise TokenError(msg='Token Expired')
        except (jwt.PyJWTError, Exception):
            raise TokenError(msg="Invalid Token")

        return user_email

    @staticmethod
    def get_user_by_email(email):
        db = next(get_db())
        return db.query(User).filter_by(email=email).first()


def get_current_user(token) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        email: str = payload.get('sub')

        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)

    except InvalidTokenError:
        raise credentials_exception

    user = get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception

    return user


def login_required(request: Request) -> User:
    """Whenever you this as the dependency it required the authorization headers in the request"""
    if 'Authorization' not in request.headers:
        logger.error(f"Token Header is missing from the request")
        raise credentials_exception

    scheme, token = request.headers['Authorization'].split(" ")
    if scheme.lower() != 'bearer':
        logger.error(f"Token type not matched")
        raise credentials_exception

    user = get_current_user(token)
    return user


def get_user_by_email(email):
    db = next(get_db())
    return db.query(User).filter_by(email=email).first()
