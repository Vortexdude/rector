from uuid import uuid4
from sqlalchemy import String, Boolean
from sqlalchemy.orm import mapped_column, Mapped
from passlib.context import CryptContext
from . import Base
from app.core.config import settings


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
ALGORITHM = 'HS256'
SECRETKEY = settings.JWT_SECRET_KEY


class SurrogatePK(Base):
    __abstract__ = True
    id: Mapped[str] = mapped_column(String(50), default=lambda: str(uuid4()), primary_key=True, unique=True)


class User(SurrogatePK):
    """Models a user table"""
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    def __repr__(self):
        """Returns string representation of model instance"""
        return "<User {name!r}>".format(name=self.name)