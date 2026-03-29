from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class SubmissionStatusEnum(str, Enum):
    submitted = "submitted"
    graded = "graded"
    rejected = "rejected"

class AssignmentBase(BaseModel):
    course_id: str
    title: str
    description: Optional[str] = None
    due_date: datetime
    max_score: float
    allow_late_submission: bool = False
    late_penalty_percent: float = 0.0
    file_types_allowed: Optional[List[str]] = None

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    max_score: Optional[float] = None
    allow_late_submission: Optional[bool] = None
    late_penalty_percent: Optional[float] = None
    file_types_allowed: Optional[List[str]] = None

class AssignmentResponse(AssignmentBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class SubmissionCreate(BaseModel):
    assignment_id: str
    student_id: str
    file_url: str

class SubmissionUpdate(BaseModel):
    score: Optional[float] = None
    feedback: Optional[str] = None
    status: Optional[SubmissionStatusEnum] = None
    plagiarism_score: Optional[float] = None

class SubmissionResponse(BaseModel):
    id: str
    assignment_id: str
    student_id: str
    submitted_at: datetime
    file_url: str
    is_late: bool
    plagiarism_score: Optional[float] = None
    score: Optional[float] = None
    feedback: Optional[str] = None
    status: SubmissionStatusEnum
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
