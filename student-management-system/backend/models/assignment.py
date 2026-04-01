from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Float, Boolean, JSON, Enum, Index, func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import BaseModel

class SubmissionStatus(PyEnum):
    submitted = "submitted"
    graded = "graded"
    rejected = "rejected"

class Assignment(BaseModel):
    __tablename__ = "assignments"
    
    course_id = Column(ForeignKey('courses.id'), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=False)
    max_score = Column(Float, nullable=False)
    allow_late_submission = Column(Boolean, default=False, nullable=False)
    late_penalty_percent = Column(Float, default=0.0, nullable=False)
    file_types_allowed = Column(JSON, nullable=True)
    
    # Relationships
    course = relationship("Course", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_assignment_course', 'course_id'),
    )

class Submission(BaseModel):
    __tablename__ = "submissions"
    
    student_id = Column(ForeignKey('students.id'), nullable=False, index=True)
    assignment_id = Column(ForeignKey('assignments.id'), nullable=False, index=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    file_url = Column(String(500), nullable=False)
    is_late = Column(Boolean, default=False, nullable=False)
    plagiarism_score = Column(Float, nullable=True)
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.submitted, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="submissions")
    assignment = relationship("Assignment", back_populates="submissions")

    __table_args__ = (
        Index('idx_submission_student', 'student_id'),
        Index('idx_submission_assignment', 'assignment_id'),
    )
