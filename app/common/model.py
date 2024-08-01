from uuid import uuid4
from typing import Annotated
from sqlalchemy import String
from datetime import datetime
from app.common.utils.timezone import timezone
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass

id_key = Annotated[str, mapped_column(String, default=lambda: str(uuid4()), unique=True, primary_key=True)]


class DatetimeMixing(MappedAsDataclass):
    created_at: Mapped[datetime] = mapped_column(
        init=False, default_factory=timezone.now()
    )
    updated_at = Mapped[datetime] = mapped_column(
        init=False, onupdate=timezone.now()
    )


class MappedBase(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class DataClassBase(MappedAsDataclass, MappedBase):

    __abstract__ = True


class Base(DataClassBase, DatetimeMixing):

    __abstract__ = True




