from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

class ChannelEnum(str, Enum):
    email = "email"
    sms = "sms"
    in_app = "in_app"

class NotificationTypeEnum(str, Enum):
    announcement = "announcement"
    grade = "grade"
    attendance = "attendance"
    deadline = "deadline"
    general = "general"

class NotificationBase(BaseModel):
    title: str
    message: str
    channel: ChannelEnum
    notification_type: NotificationTypeEnum

class NotificationCreate(NotificationBase):
    recipient_id: str
    sender_id: Optional[str] = None
    course_id: Optional[str] = None

class BroadcastCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    is_read: bool

class NotificationResponse(NotificationBase):
    id: str
    recipient_id: str
    sender_id: Optional[str] = None
    is_read: bool
    sent_at: datetime
    course_id: Optional[str] = None
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
