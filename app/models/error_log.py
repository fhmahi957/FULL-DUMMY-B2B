from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database import Base

class ErrorType(str, PyEnum):
    validation_error = "validation_error"
    duplicate_entry = "duplicate_entry"
    api_failure = "api_failure"
    timeout = "timeout"
    payment_failure = "payment_failure"  # ✅ ADD THIS LINE
    database_error = "database_error"
    integration_failure = "integration_failure"
    manual_intervention_required = "manual_intervention_required"

class ResolutionStatus(str, PyEnum):
    unresolved = "unresolved"
    resolved = "resolved"
    ignored = "ignored"

class ErrorLog(Base):
    __tablename__ = "error_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_type = Column(String(50), nullable=False)  # "order", "refund", "lead", "email"
    workflow_run_id = Column(String(100), nullable=True)
    step_name = Column(String(100), nullable=False)
    error_type = Column(SAEnum(ErrorType), nullable=False)
    error_message = Column(Text, nullable=False)
    http_status_code = Column(Integer, nullable=True)
    resolution_status = Column(SAEnum(ResolutionStatus), default=ResolutionStatus.unresolved)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolution_note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # ✅ Must have server_default
    
    # Relationship to Manual Review
    manual_review = relationship("ManualReview", back_populates="error_log", uselist=False)