from typing import Annotated
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.api.schema.users import UserCreateSchema, UserLoginSchema
from app.api.services.users import UserService


router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/me")
def get_details():
    return {"status": "doing nothing!"}


@router.post("/signup")
def user_register(db: db_dependency, data: UserCreateSchema = Body()):

    return UserService(db).register_user(data)


@router.post("/login")
def user_login(db: db_dependency, data: UserLoginSchema):
    """Processes user's authentication and returns a token
    on successful authentication.

    request body:

    - email: Unique identifier for a user 'e.g' email,
                phone number, name

    - password:
    """
    return UserService(db).login(data)
