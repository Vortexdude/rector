from fastapi import APIRouter, Body
from app.core.config import logger
from app.core.db import db_dependency
from app.api.schema.users import UserCreateSchema, UserLoginSchema, UserBase
from app.api.services.users import UserService
from app.api.models.jwt import Token
from app.common.security.depends import user_identity_dependency


API_PREFIX = '/api/v1'
router = APIRouter(prefix=API_PREFIX)


@router.get("/me")
def read_own_items(db: db_dependency, user: user_identity_dependency) -> UserBase:
    logger.debug(f"GET {API_PREFIX}/me > with user.email")
    return UserService(db).current_user(user.email)


@router.post("/signup")
def user_register(db: db_dependency, data: UserCreateSchema = Body()):
    # logger.info(f"POST {API_PREFIX}/signup > with {data}")
    return UserService(db).register_user(data)


@router.post("/login")
async def login_for_access_token(db: db_dependency, form_data: UserLoginSchema) -> Token:
    # logger.info(f"POST {API_PREFIX}/login > with {form_data.email}")
    return UserService(db).login(form_data)
