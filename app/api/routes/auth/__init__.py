from fastapi import APIRouter, Body
from app.core.db import db_dependency
from app.api.schema import UserCreateSchema, UserLoginSchema
from app.api.services import UserService
from app.api.models import Token
from starlette.requests import Request

router = APIRouter()


@router.get("/me")
def read_own_items(db: db_dependency, request: Request):
    return {"status": "done"}


@router.post("/signup")
def user_register(db: db_dependency, data: UserCreateSchema = Body()):
    return UserService(db).register_user(data)


@router.post("/login")
async def login_for_access_token(db: db_dependency, form_data: UserLoginSchema) -> Token:
    return UserService(db).login(form_data)
