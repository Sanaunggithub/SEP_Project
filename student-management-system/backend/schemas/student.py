from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import Optional, Dict, Any
from enum import Enum
from schemas.auth import UserResponse

class AcademicStatusEnum(str, Enum):
    active = "active"
    probation = "probation"
    graduated = "graduated"
    dropped = "dropped"

class StudentBase(BaseModel):
    student_id_number: str
    program: str
    department: str
    year_level: int
    scholarship_status: bool = False

class StudentCreate(StudentBase):
    user_id: str
    enrollment_date: date
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    guardian_email: Optional[str] = None
    academic_history: Optional[str] = None

class StudentUpdate(BaseModel):
    program: Optional[str] = None
    department: Optional[str] = None
    year_level: Optional[int] = None
    scholarship_status: Optional[bool] = None
    academic_status: Optional[AcademicStatusEnum] = None
    gpa: Optional[float] = None
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
    guardian_email: Optional[str] = None
    academic_history: Optional[str] = None
    notes: Optional[str] = None

class StudentResponse(StudentBase):
    id: str
    user_id: str
    academic_status: AcademicStatusEnum
    gpa: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool
    full_name:Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class StudentDetailResponse(StudentResponse):
    user: UserResponse
