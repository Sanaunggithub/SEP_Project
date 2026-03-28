from sqlalchemy import Column, Integer, Date, Boolean, ForeignKey
from .base import Base

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    date = Column(Date)
    present = Column(Boolean)
