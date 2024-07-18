from fastapi import APIRouter, Body
from app.core.db import db_dependency
from app.api.schema.users import UserCreateSchema
from app.api.services.users import UserService
from app.api.models.jwt import Token
from app.common.security.depends import pwd_request_form
from app.common.security.jwt_util import current_user

router = APIRouter()


@router.get("/me")
def read_own_items(user: current_user):
    return [{"item_id": "Foo", "owner": user.email}]


@router.post("/signup")
def user_register(db: db_dependency, data: UserCreateSchema = Body()):
    return UserService(db).register_user(data)


@router.post("/login")
async def login_for_access_token(db: db_dependency, form_data: pwd_request_form) -> Token:
    """Processes user's authentication and returns a token
    on successful authentication.

    request body:

    - email: Unique identifier for a user 'e.g' email,
                phone number, name

    - password:
    """
    return UserService(db).login(form_data)
