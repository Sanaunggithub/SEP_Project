from sqlalchemy import Column, String, Text, Date, Enum, Index
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from datetime import date
from .base import BaseModel

class Role(PyEnum):
    student = "student"
    instructor = "instructor"
    admin = "admin"

class Gender(PyEnum):
    male = "male"
    female = "female"
    other = "other"

class AccountStatus(PyEnum):
    active = "active"
    suspended = "suspended"
    inactive = "inactive"

class User(BaseModel):
    __tablename__ = "users"
    
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(Role), nullable=False)
    profile_picture_url = Column(String(500), nullable=True)
    phone_number = Column(String(20), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    address = Column(Text, nullable=False)
    emergency_contact_name = Column(String(255), nullable=False)
    emergency_contact_phone = Column(String(20), nullable=False)
    account_status = Column(Enum(AccountStatus), default=AccountStatus.active, nullable=False)

    # Relationships
    taught_courses = relationship("Course", back_populates="instructor")
    marked_attendances = relationship("Attendance", back_populates="marker", foreign_keys="Attendance.marked_by")
    generated_reports = relationship("ReportSnapshot", back_populates="generator")

    __table_args__ = (
        Index('idx_user_email', 'email'),
    )
