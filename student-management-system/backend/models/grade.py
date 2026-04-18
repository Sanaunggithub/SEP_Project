from sqlalchemy import Column, ForeignKey, Float, DateTime, Text, String, Integer, Enum, Index, func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import BaseModel

class ComponentType(PyEnum):
    assignment = "assignment"
    quiz = "quiz"
    midterm = "midterm"
    final = "final"

class Grade(BaseModel):
    __tablename__ = "grades"
    
    student_id = Column(ForeignKey('students.id'), nullable=False, index=True)
    course_id = Column(ForeignKey('courses.id', ondelete="SET NULL"), nullable=True, index=True)
    component_type = Column(Enum(ComponentType), nullable=False)
    score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    graded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    remarks = Column(Text, nullable=True)
    course_name = Column(String(255), nullable = True)

    # Relationships
    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")

    __table_args__ = (
        Index('idx_grade_student', 'student_id'),
        Index('idx_grade_course', 'course_id'),
    )

class GPA(BaseModel):
    __tablename__ = "gpas"
    
    student_id = Column(ForeignKey('students.id'), nullable=False, index=True)
    semester = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    gpa_value = Column(Float, nullable=False)

    # Relationships
    student = relationship("Student", back_populates="gpas")

    __table_args__ = (
        Index('idx_gpa_student', 'student_id'),
    )
