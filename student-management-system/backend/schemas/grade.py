from pydantic import BaseModel

class GradeBase(BaseModel):
    student_id: int
    course_id: int
    grade: float

class GradeCreate(GradeBase):
    pass

class GradeResponse(GradeBase):
    id: int

    class Config:
        orm_mode = True
