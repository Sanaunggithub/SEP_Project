from sqlalchemy import Column, ForeignKey, String, Text, Enum, Boolean, DateTime, Index, func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import BaseModel

class Channel(PyEnum):
    email = "email"
    sms = "sms"
    in_app = "in_app"

class NotificationType(PyEnum):
    announcement = "announcement"
    grade = "grade"
    attendance = "attendance"
    deadline = "deadline"
    general = "general"

class Notification(BaseModel):
    __tablename__ = "notifications"
    
    recipient_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    sender_id = Column(ForeignKey('users.id'), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    channel = Column(Enum(Channel), nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    course_id = Column(ForeignKey('courses.id'), nullable=True, index=True)

    # Relationships
    recipient = relationship("User", back_populates="received_notifications", foreign_keys=[recipient_id])
    sender = relationship("User", back_populates="sent_notifications", foreign_keys=[sender_id])
    course = relationship("Course", back_populates="notifications")

    __table_args__ = (
        Index('idx_notification_recipient', 'recipient_id'),
        Index('idx_notification_sender', 'sender_id'),
        Index('idx_notification_course', 'course_id'),
    )
