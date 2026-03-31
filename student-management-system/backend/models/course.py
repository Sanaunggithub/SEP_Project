from sqlalchemy import Column, String, Text, Integer, JSON, Time, ForeignKey, DateTime, Enum, Index, func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import BaseModel

class CourseStatus(PyEnum):
    active = "active"
    cancelled = "cancelled"
    completed = "completed"

class Course(BaseModel):
    __tablename__ = "courses"
    
    course_code = Column(String(20), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    credit_hours = Column(Integer, nullable=False)
    max_seats = Column(Integer, nullable=False)
    enrolled_count = Column(Integer, default=0, nullable=False)
    schedule_days = Column(JSON, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    semester = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    prerequisite_ids = Column(JSON, nullable=True)
    instructor_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    room_location = Column(String(100), nullable=False)
    status = Column(Enum(CourseStatus), default=CourseStatus.active, nullable=False)

    # Relationships
    instructor = relationship("User", back_populates="taught_courses")
    enrollments = relationship("CourseEnrollment", back_populates="course", cascade="all, delete-orphan")
    grades = relationship("Grade", back_populates="course", cascade="all, delete-orphan")
    attendances = relationship("Attendance", back_populates="course", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_course_instructor', 'instructor_id'),
        Index('idx_course_code', 'course_code'),
    )

class CourseEnrollment(BaseModel):
    __tablename__ = "course_enrollments"
    
    student_id = Column(ForeignKey('students.id'), nullable=False, index=True)
    course_id = Column(ForeignKey('courses.id'), nullable=False, index=True)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(Enum(CourseStatus), default=CourseStatus.active, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

    __table_args__ = (
        Index('idx_enrollment_student', 'student_id'),
        Index('idx_enrollment_course', 'course_id'),
    )
