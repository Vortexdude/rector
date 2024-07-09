from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta, UTC
from sqlalchemy.orm import Session
from starlette import status
from app.core.db import SessionLocal
from app.api.models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

router = APIRouter(prefix='/auth', tags=['Auth'])

SECRETKEY = 'kj34s9845kjhv7y4t0hdf'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    email: str
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        password_hash=bcrypt_context.hash(create_user_request.password),
        email=create_user_request.email
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}


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
