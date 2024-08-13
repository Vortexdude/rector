from sqlalchemy.orm import Session
from app.api.models import Guardian
from app.core.db import get_db

__all__ = ["UserActivity"]


class UserActivity:
    def __init__(self, db: Session = next(get_db())):
        self.db = db

    async def set_info(self, *args, **kwargs):

        record = Guardian(*args, **kwargs)
        self.db.add(record)
        self.db.commit()
        self.db.flush(record)
