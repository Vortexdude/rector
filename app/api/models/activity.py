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
