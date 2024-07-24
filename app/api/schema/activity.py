from pydantic import BaseModel
from datetime import datetime
from app.common.utils.timezone import timezone


class Activity(BaseModel):
    user_id: str
    activity: str
    time_stamp: datetime = timezone.now()
