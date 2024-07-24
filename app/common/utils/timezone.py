import zoneinfo
from datetime import datetime, timedelta
from app.core.config import settings


class Timezone:

    def __init__(self, tz: str = settings.DATETIME_TIMEZONE):
        self.tz = zoneinfo.ZoneInfo(tz)

    def now(self) -> datetime:
        return datetime.now(tz=self.tz)

    @property
    def min(self) -> datetime:
        return datetime.min

    @property
    def now_tz(self):
        return datetime.now().replace(tzinfo=None)

    @staticmethod
    def timedelta(*args, **kwargs) -> timedelta:
        """Adding new functionality"""
        return timedelta(*args, **kwargs)


timezone = Timezone()
