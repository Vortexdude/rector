from fastapi import APIRouter, Body
from app.core.db import SessionLocal
from .resource import UserResource, RoleResource, GroupResource, PermissionResource, create_admin_user
from .schema import UserRegisterSchema, RoleCreate, GroupCreate, PermissionCreate
from typing import Annotated
from app.api.routes.auth.deps import user_dep
from app.core.db import db_dependency

router = APIRouter()


@router.post("/users/")
def create_users(data: Annotated[UserRegisterSchema, Body(...)], db=db_dependency):
    return UserResource(db).insert(data)


@router.post("/roles/")
def create_role(data: Annotated[RoleCreate, Body(...)], db=db_dependency):
    return RoleResource(db).insert(data)


@router.post("/groups/")
def create_group(data: Annotated[GroupCreate, Body(...)], db=db_dependency):
    return GroupResource(db).insert(data)


@router.post("/permission/")
def create_permission(data: Annotated[PermissionCreate, Body(...)], db=db_dependency):
    return PermissionResource(db).insert(data)


@router.post("/create_admin_user")
def create_admin(data: Annotated[UserRegisterSchema, Body(...)], db=db_dependency):
    return create_admin_user(data, db)


@router.get("/me")
def me(user: user_dep, db=db_dependency):
    return UserResource(db).find_by_username(user_name=user.get('username'))
