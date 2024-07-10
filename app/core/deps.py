from typing import Annotated
from datetime import datetime, timedelta, UTC
from app.api.models import User
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

ALGORITHM = 'HS256'
SECRETKEY = settings.JWT_SECRET_KEY


def authenticate_user(username, password, db):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password_hash):
        return False
    return user


def create_access_token(username: str, userid: str, expiration_time: timedelta):
    encode = {'sub': username, 'id': userid}
    expires = datetime.now(tz=UTC) + expiration_time
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRETKEY, algorithm=ALGORITHM)


#  dependency injection
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRETKEY, [ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        if not username or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate the user!")
        return {"username": username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate the user.")


def create_pass_hash(password: str) -> str:
    return bcrypt_context.hash(password)
