from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date
from typing import Optional, List
from enum import Enum

class AttendanceStatusEnum(str, Enum):
    present = "present"
    absent = "absent"
    late = "late"
    excused = "excused"

class AttendanceBase(BaseModel):
    student_id: str
    course_id: str
    date: date
    status: AttendanceStatusEnum

class AttendanceCreate(AttendanceBase):
    check_in_time: Optional[datetime] = None


class AttendanceBulkCreate(BaseModel):
    course_id: str
    date: date
    records: List[dict] = Field(..., description="List of {student_id, status}")

class AttendanceUpdate(BaseModel):
    status: Optional[AttendanceStatusEnum] = None
    check_in_time: Optional[datetime] = None

class AttendanceResponse(AttendanceBase):
    id: str
    check_in_time: Optional[datetime] = None
    marked_by: str
    attendance_percentage: Optional[float] = None
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class AtRiskStudentResponse(BaseModel):
    student_id: str
    course_id: str
    attendance_percentage: float
    total_classes: int
    attended_classes: int
