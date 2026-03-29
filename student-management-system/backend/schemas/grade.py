from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, Dict
from enum import Enum

class ComponentTypeEnum(str, Enum):
    assignment = "assignment"
    quiz = "quiz"
    midterm = "midterm"
    final = "final"

class GradeBase(BaseModel):
    student_id: str
    course_id: str
    component_type: ComponentTypeEnum
    score: float
    max_score: float
    weight: float

class GradeCreate(GradeBase):
    remarks: Optional[str] = None

class GradeUpdate(BaseModel):
    score: Optional[float] = None
    max_score: Optional[float] = None
    weight: Optional[float] = None
    remarks: Optional[str] = None

class GradeResponse(GradeBase):
    id: str
    graded_at: datetime
    remarks: Optional[str] = None
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class GPAResponse(BaseModel):
    id: str
    student_id: str
    semester: str
    year: int
    gpa_value: float
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class GradeDistributionResponse(BaseModel):
    course_id: str
    total_students: int
    average_score: float
    highest_score: float
    lowest_score: float
    median_score: float
    distribution: Dict[str, int] = Field(default_factory=dict, description="Grade ranges and their counts")
