from fastapi import APIRouter, Body, Depends
from app.core.db import SessionLocal
from .resource import UserResource, RoleResource, GroupResource, PermissionResource, create_admin_user
from .schema import UserRegisterSchema, RoleCreate, GroupCreate, PermissionCreate
from typing import Annotated
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/")
def create_users(data: Annotated[UserRegisterSchema, Body(...)], db: Session = Depends(get_db)):
    return UserResource(db).insert(data)


@router.post("/roles/")
def create_role(data: Annotated[RoleCreate, Body(...)], db: Session = Depends(get_db)):
    return RoleResource(db).insert(data)


@router.post("/groups/")
def create_group(data: Annotated[GroupCreate, Body(...)], db: Session = Depends(get_db)):
    return GroupResource(db).insert(data)


@router.post("/permission/")
def create_permission(data: Annotated[PermissionCreate, Body(...)], db: Session = Depends(get_db)):
    return PermissionResource(db).insert(data)


@router.post("/create_admin_user")
def create_admin(data: Annotated[UserRegisterSchema, Body(...)], db: Session = Depends(get_db)):
    return create_admin_user(data, db)


@router.get("/me")
def me(user_email: str, db: Session = Depends(get_db)):
    return UserResource(db).find_by_email(user_email)
