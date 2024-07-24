from sqlalchemy.orm import Session
from app.api.models import ActivityLog


class UserActivity:
    def __init__(self, db):
        self.db: Session = db

    def set_info(self, user_id: str, activity: str):
        log = ActivityLog(
            user_id=user_id,
            activity=activity,
        )
        self.db.add(log)
        self.db.commit()
        self.db.flush(log)
