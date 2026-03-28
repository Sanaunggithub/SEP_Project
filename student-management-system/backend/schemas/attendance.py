from pydantic import BaseModel
from datetime import date

class AttendanceBase(BaseModel):
    student_id: int
    course_id: int
    date: date
    present: bool

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceResponse(AttendanceBase):
    id: int

    class Config:
        orm_mode = True
