import zoneinfo
from datetime import datetime
from app.core.config import settings


class Timezone:

    def __init__(self, tz: str = settings.DATETIME_TIMEZONE):
        self.tz = zoneinfo.ZoneInfo(tz)

    def now(self) -> datetime:
        return datetime.now(tz=self.tz)


timezone = Timezone()
