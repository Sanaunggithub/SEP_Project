from pydantic import BaseModel
from datetime import date

class AssignmentBase(BaseModel):
    course_id: int
    title: str
    due_date: date

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentResponse(AssignmentBase):
    id: int

    class Config:
        orm_mode = True
