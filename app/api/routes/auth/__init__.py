from fastapi import APIRouter, Body
from app.core.config import logger
from app.core.db import db_dependency
from app.api.schema import UserCreateSchema, UserLoginSchema, UserBase
from app.api.services import UserService
from app.api.models import Token
from app.common.security import user_identity_dependency


router = APIRouter()


@router.get("/me")
def read_own_items(db: db_dependency, user: user_identity_dependency) -> UserBase:
    logger.debug(f"GET /me > with {user.email}")
    return UserService(db).current_user(user.email)


@router.post("/signup")
def user_register(db: db_dependency, data: UserCreateSchema = Body()):
    logger.debug(f"POST /signup > with {data}")
    return UserService(db).register_user(data)


@router.post("/login")
async def login_for_access_token(db: db_dependency, form_data: UserLoginSchema) -> Token:
    logger.debug(f"POST /login > with {form_data.email}")
    return UserService(db).login(form_data)
