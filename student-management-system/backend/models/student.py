from sqlalchemy import Column, String, Date, Integer, Float, Boolean, Text, Enum, ForeignKey, Index, func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import BaseModel

class AcademicStatus(PyEnum):
    active = "active"
    probation = "probation"
    graduated = "graduated"
    dropped = "dropped"

class Student(BaseModel):
    __tablename__ = "students"
    
    user_id = Column(ForeignKey('users.id'), unique=True, nullable=False, index=True)
    student_id_number = Column(String(50), unique=True, nullable=False, index=True)
    enrollment_date = Column(Date, nullable=False)
    program = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False)
    year_level = Column(Integer, nullable=False)
    academic_status = Column(Enum(AcademicStatus), default=AcademicStatus.active, nullable=False)
    gpa = Column(Float, nullable=True)
    academic_history = Column(String(1000), nullable=True)  # JSON stored as string
    guardian_name = Column(String(255), nullable=True)
    guardian_phone = Column(String(20), nullable=True)
    guardian_email = Column(String(255), nullable=True)
    scholarship_status = Column(Boolean, default=False, nullable=False)
    notes = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", uselist=False)
    enrollments = relationship("CourseEnrollment", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")
    submissions = relationship("Submission", back_populates="student")
    grades = relationship("Grade", back_populates="student")
    gpas = relationship("GPA", back_populates="student")
    
    __table_args__ = (
        Index('idx_student_user', 'user_id'),
        Index('idx_student_id_number', 'student_id_number'),
    )
