from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    message: str
    timestamp: datetime

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id: int

    class Config:
        orm_mode = True
