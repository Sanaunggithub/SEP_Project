from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime, date, time
from typing import Optional, List
from enum import Enum

# ==================== Enums ====================
class RoleEnum(str, Enum):
    student = "student"
    instructor = "instructor"
    admin = "admin"

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class AccountStatusEnum(str, Enum):
    active = "active"
    suspended = "suspended"
    inactive = "inactive"

class CourseStatusEnum(str, Enum):
    active = "active"
    cancelled = "cancelled"
    completed = "completed"

class ComponentTypeEnum(str, Enum):
    assignment = "assignment"
    quiz = "quiz"
    midterm = "midterm"
    final = "final"

class AttendanceStatusEnum(str, Enum):
    present = "present"
    absent = "absent"
    late = "late"
    excused = "excused"

class SubmissionStatusEnum(str, Enum):
    submitted = "submitted"
    graded = "graded"
    rejected = "rejected"


class ReportTypeEnum(str, Enum):
    enrollment = "enrollment"
    attendance = "attendance"
    grades = "grades"
    performance = "performance"

class ExportFormatEnum(str, Enum):
    pdf = "pdf"
    excel = "excel"
    csv = "csv"

# ==================== Base Schema ====================
class BaseSchema(BaseModel):
    id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_active: bool = True

    class Config:
        from_attributes = True

# ==================== User/Auth Schemas ====================
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: RoleEnum
    phone_number: str
    date_of_birth: date
    gender: GenderEnum
    address: str
    emergency_contact_name: str
    emergency_contact_phone: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    profile_picture_url: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class UserResponse(BaseSchema, UserBase):
    profile_picture_url: Optional[str] = None
    account_status: AccountStatusEnum = AccountStatusEnum.active

# ==================== Course Schemas ====================
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
    prerequisite_ids: Optional[List[str]] = None
    room_location: str

class CourseCreate(CourseBase):
    instructor_id: str

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

class CourseSchema(BaseSchema, CourseBase):
    enrolled_count: int = 0
    status: CourseStatusEnum = CourseStatusEnum.active
    instructor_id: str

class CourseEnrollmentCreate(BaseModel):
    student_id: str
    course_id: str

class CourseEnrollmentSchema(BaseSchema):
    student_id: str
    course_id: str
    enrolled_at: datetime
    status: CourseStatusEnum

# ==================== Grade Schemas ====================
class GradeCreate(BaseModel):
    student_id: str
    course_id: str
    component_type: ComponentTypeEnum
    score: float
    max_score: float
    weight: float
    remarks: Optional[str] = None

class GradeSchema(BaseSchema):
    student_id: str
    course_id: str
    component_type: ComponentTypeEnum
    score: float
    max_score: float
    weight: float
    graded_at: datetime
    remarks: Optional[str] = None

class GPACreate(BaseModel):
    student_id: str
    semester: str
    year: int
    gpa_value: float

class GPASchema(BaseSchema):
    student_id: str
    semester: str
    year: int
    gpa_value: float

# ==================== Attendance Schemas ====================
class AttendanceCreate(BaseModel):
    student_id: str
    course_id: str
    date: date
    status: AttendanceStatusEnum
    marked_by: str
    check_in_time: Optional[datetime] = None

class AttendanceSchema(BaseSchema):
    student_id: str
    course_id: str
    date: date
    check_in_time: Optional[datetime] = None
    status: AttendanceStatusEnum
    marked_by: str
    attendance_percentage: Optional[float] = None

# ==================== Assignment Schemas ====================
class AssignmentCreate(BaseModel):
    course_id: str
    title: str
    description: Optional[str] = None
    due_date: datetime
    max_score: float
    allow_late_submission: bool = False
    late_penalty_percent: float = 0.0
    file_types_allowed: Optional[List[str]] = None

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    max_score: Optional[float] = None
    allow_late_submission: Optional[bool] = None
    late_penalty_percent: Optional[float] = None

class AssignmentSchema(BaseSchema):
    course_id: str
    title: str
    description: Optional[str] = None
    due_date: datetime
    max_score: float
    allow_late_submission: bool
    late_penalty_percent: float
    file_types_allowed: Optional[List[str]] = None

class SubmissionCreate(BaseModel):
    student_id: str
    assignment_id: str
    file_url: str

class SubmissionUpdate(BaseModel):
    plagiarism_score: Optional[float] = None
    score: Optional[float] = None
    feedback: Optional[str] = None
    status: Optional[SubmissionStatusEnum] = None

class SubmissionSchema(BaseSchema):
    student_id: str
    assignment_id: str
    submitted_at: datetime
    file_url: str
    is_late: bool
    plagiarism_score: Optional[float] = None
    score: Optional[float] = None
    feedback: Optional[str] = None
    status: SubmissionStatusEnum


# ==================== Analytics Schemas ====================
class ReportSnapshotCreate(BaseModel):
    report_type: ReportTypeEnum
    generated_by: str
    parameters: Optional[dict] = None
    export_format: ExportFormatEnum

class ReportSnapshotSchema(BaseSchema):
    report_type: ReportTypeEnum
    generated_by: str
    parameters: Optional[dict] = None
    result_summary: Optional[dict] = None
    export_format: ExportFormatEnum
    generated_at: datetime
