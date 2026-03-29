from pydantic import BaseModel, ConfigDict
from datetime import datetime, time
from typing import Optional, List
from enum import Enum

class CourseStatusEnum(str, Enum):
    active = "active"
    cancelled = "cancelled"
    completed = "completed"

class CourseBase(BaseModel):
    course_code: str
    title: str
    description: Optional[str] = None
    credit_hours: int
    max_seats: int
    schedule_days: List[str]
    start_time: time
    end_time: time
    semester: str
    year: int
    room_location: str

class CourseCreate(CourseBase):
    instructor_id: str
    prerequisite_ids: Optional[List[str]] = None

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    credit_hours: Optional[int] = None
    max_seats: Optional[int] = None
    schedule_days: Optional[List[str]] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    room_location: Optional[str] = None
    status: Optional[CourseStatusEnum] = None

class CourseResponse(CourseBase):
    id: str
    enrolled_count: int = 0
    status: CourseStatusEnum
    instructor_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: str

class EnrollmentResponse(BaseModel):
    id: str
    student_id: str
    course_id: str
    enrolled_at: datetime
    status: CourseStatusEnum
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
