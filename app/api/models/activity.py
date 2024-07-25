from sqlalchemy import String, DATETIME
from sqlalchemy.orm import mapped_column, Mapped
from .users import SurrogatePK
from app.common.utils.timezone import timezone
from datetime import datetime


class ActivityLog(SurrogatePK):
    __tablename__ = 'activity_logs'
    user_id: Mapped[str] = mapped_column(String(50), nullable=False)
    activity: Mapped[str] = mapped_column(String(254), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DATETIME, default=timezone.now())


class Guardian(SurrogatePK):
    __tablename__ = "guardian"

    timestamp: Mapped[datetime] = mapped_column(DATETIME, default=timezone.now())
    os: Mapped[str] = mapped_column(String(10), nullable=True)
    device: Mapped[str] = mapped_column(String(10), nullable=True)
    browser: Mapped[str] = mapped_column(String(30), nullable=True)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    method: Mapped[str] = mapped_column(String(10))
    host: Mapped[str] = mapped_column(String(50))
    url: Mapped[int] = mapped_column(String(20))
    port: Mapped[int] = mapped_column(String(20))
    time: Mapped[str] = mapped_column(String(30))



