from sqlalchemy import Column, ForeignKey, Date, DateTime, Float, Enum, Index
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import BaseModel

class AttendanceStatus(PyEnum):
    present = "present"
    absent = "absent"
    late = "late"
    excused = "excused"

class Attendance(BaseModel):
    __tablename__ = "attendances"
    
    student_id = Column(ForeignKey('students.id'), nullable=False, index=True)
    course_id = Column(ForeignKey('courses.id'), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    check_in_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(AttendanceStatus), nullable=False)
    marked_by = Column(ForeignKey('users.id'), nullable=False, index=True)
    attendance_percentage = Column(Float, nullable=True)

    # Relationships
    student = relationship("Student", back_populates="attendances", foreign_keys=[student_id])
    course = relationship("Course", back_populates="attendances")
    marker = relationship("User", back_populates="marked_attendances", foreign_keys=[marked_by])
    
    __table_args__ = (
        Index('idx_attendance_student', 'student_id'),
        Index('idx_attendance_course', 'course_id'),
        Index('idx_attendance_date', 'date'),
    )
