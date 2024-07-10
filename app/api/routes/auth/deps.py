from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from app.core.db import SessionLocal
from app.core.deps import get_current_user

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


token_request_dep = Annotated[OAuth2PasswordRequestForm, Depends()]
user_dep = Annotated[dict, Depends(get_current_user)]
