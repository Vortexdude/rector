from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, declared_attr
from uuid import uuid4
from datetime import datetime
from typing import Annotated
from app.common.utils.timezone import timezone

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




