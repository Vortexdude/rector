from datetime import timedelta
from sqlalchemy.orm import Session
from app.core.config import settings
from app.api.models.jwt import Token
from app.api.models.users import User
from sqlalchemy.exc import SQLAlchemyError
from app.common.security.jwt_util import JWTUtil
from app.common.security.exceptions import credentials_exception


__all__ = ["UserService"]


class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def register_user(self, data):
        user = User(
            name=data.name,
            email=data.email,
            hashed_password=JWTUtil.get_password_hash(data.password)
        )
        try:
            self.db.add(user)
            self.db.commit()
            self.db.flush(user)
            return {"status": "done"}
        except SQLAlchemyError as e:
            return {"error": "User Already exists"}

    def get_by_email(self, email):
        return self.db.query(User).filter_by(email=email).first()

    def authenticate_user(self, data):
        user = self.get_by_email(email=data.email)
        if not user:
            return False
        if not JWTUtil.verify_password(data.password, user.hashed_password):
            return False
        return user

    def login(self, form_data) -> Token:
        user = self.get_by_email(email=form_data.email)
        if not user:
            raise credentials_exception
        access_token_expire = timedelta(minutes=settings.TOKEN_EXPIRE_SECONDS)
        access_token = JWTUtil.create_access_token(data={'sub': user.email}, expire_delta=access_token_expire)
        return Token(access_token=access_token, token_type='bearer')

    def current_user(self, email):
        user = self.get_by_email(email)
        return user if user else False
