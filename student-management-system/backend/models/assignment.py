from sqlalchemy import Column, Integer, String, Date, ForeignKey
from .base import Base

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String)
    due_date = Column(Date)
