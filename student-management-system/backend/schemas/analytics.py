from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, Dict
from enum import Enum

class ReportTypeEnum(str, Enum):
    enrollment = "enrollment"
    attendance = "attendance"
    grades = "grades"
    performance = "performance"

class ExportFormatEnum(str, Enum):
    pdf = "pdf"
    excel = "excel"
    csv = "csv"

class ReportSnapshotBase(BaseModel):
    report_type: ReportTypeEnum
    export_format: ExportFormatEnum

class ReportSnapshotCreate(ReportSnapshotBase):
    parameters: Optional[Dict] = None

class ReportSnapshotResponse(ReportSnapshotBase):
    id: str
    generated_by: str
    parameters: Optional[Dict] = None
    result_summary: Optional[Dict] = None
    generated_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class EnrollmentTrendResponse(BaseModel):
    semester: str
    year: int
    course_id: str
    enrolled_count: int

class AttendancePatternResponse(BaseModel):
    course_id: str
    week: int
    attendance_rate: float = Field(..., ge=0, le=100)

class StudentPerformanceResponse(BaseModel):
    student_id: str
    course_id: str
    gpa: float
    attendance_percentage: float = Field(..., ge=0, le=100)
    assignment_completion_rate: float = Field(..., ge=0, le=100)
