from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.common.utils.timezone import timezone
from app.core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    """
    Encrypt passwords using the hash algorithm

    :param password:
    :return:
    """
    return pwd_context.hash(password)


def verify_password(plain_text, hashed_text):
    """
    Password verification

    :param plain_text: The password to verify
    :param hashed_text: The hash ciphers to compare
    :return:
    """
    return pwd_context.verify(plain_text, hashed_text)


async def create_access_token(sub: str, expire_delta: timedelta | None = None, **kwargs) -> tuple[str, str]:
    if expire_delta:
        expire = timezone.now() + expire_delta
        expire_seconds = int(expire_delta.seconds)
    else:
        expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
        expire_seconds = settings.TOKEN_EXPIRE_SECONDS

    to_encode = {'exp': expire, 'sub': sub, **kwargs}
    token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.TOKEN_ALGORITHM)
    return token, expire
