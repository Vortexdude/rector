from sqlalchemy.orm import Session
from app.api.models import ActivityLog
from app.common.utils.timezone import timezone


class UserActivity:
    def __init__(self, db):
        self.db: Session = db

    def set_info(self, user, activity: str):

        log = ActivityLog(
            user_id=user.id,
            activity=activity,
            timestamp=timezone.now()
        )
        self.db.add(log)
        self.db.commit()
        self.db.flush(log)
