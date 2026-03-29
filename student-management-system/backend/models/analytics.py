from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, JSON, DateTime, Index, func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import Base
from .base import BaseModel

class ReportType(PyEnum):
    enrollment = "enrollment"
    attendance = "attendance"
    grades = "grades"
    performance = "performance"

class ExportFormat(PyEnum):
    pdf = "pdf"
    excel = "excel"
    csv = "csv"

class ReportSnapshot(BaseModel):
    __tablename__ = "report_snapshots"
    
    report_type = Column(Enum(ReportType), nullable=False)
    generated_by = Column(ForeignKey('users.id'), nullable=False, index=True)
    parameters = Column(JSON, nullable=True)
    result_summary = Column(JSON, nullable=True)
    export_format = Column(Enum(ExportFormat), nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    generator = relationship("User", back_populates="generated_reports")

    __table_args__ = (
        Index('idx_report_generator', 'generated_by'),
    )
