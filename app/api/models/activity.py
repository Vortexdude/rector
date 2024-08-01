from datetime import datetime
from .users import SurrogatePK
from app.common.utils.timezone import timezone
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, DATETIME, TIMESTAMP


class ActivityLog(SurrogatePK):
    __tablename__ = 'activity_logs'

    user_id: Mapped[str] = mapped_column(String(50), nullable=False)
    activity: Mapped[str] = mapped_column(String(254), nullable=True)
    timestamps: Mapped[datetime] = mapped_column(TIMESTAMP, default=timezone.now())


class Guardian(SurrogatePK):
    __tablename__ = "guardian"

    timestamps: Mapped[datetime] = mapped_column(TIMESTAMP, default=timezone.now())
    os: Mapped[str] = mapped_column(String(10), nullable=True)
    device: Mapped[str] = mapped_column(String(10), nullable=True)
    browser: Mapped[str] = mapped_column(String(30), nullable=True)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    method: Mapped[str] = mapped_column(String(10))
    host: Mapped[str] = mapped_column(String(256))
    url: Mapped[int] = mapped_column(String(256))
    port: Mapped[int] = mapped_column(String(20))
    time: Mapped[str] = mapped_column(String(30))
