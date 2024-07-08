from fastapi import APIRouter, Body, Depends
from ...core.db import get_db, User, session_local
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
router = APIRouter()


class UserRegisterSchema(BaseModel):
    name: str | None = None
    email: str | None = None


@router.post("/register")
def create_users(data: Annotated[UserRegisterSchema, Body(...)], db: Session = Depends(get_db)):
    return register_user(data, db)


def register_user(user: UserRegisterSchema, session: Session):
    users = User(**user.model_dump())
    session.add(users)
    session.commit()
    session.refresh(users)
    return users
