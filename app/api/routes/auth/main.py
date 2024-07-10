from datetime import timedelta
from starlette import status
from fastapi import APIRouter, HTTPException
from .deps import token_request_dep
from app.core.db import db_dependency
from .schema import CreateUserRequest, Token
from app.api.models import User
from app.core.deps import create_access_token, create_pass_hash, authenticate_user

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        password_hash=create_pass_hash(create_user_request.password),
        email=create_user_request.email
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: token_request_dep, db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
