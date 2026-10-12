from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class AssessmentAttemptCreate(BaseModel):
    role_id: Optional[str] = None
    role_title: str = Field(..., min_length=1)
    overall_score: int = Field(..., ge=0, le=100)
    time_taken_seconds: int = Field(0, ge=0)
    question_count: int = Field(0, ge=0)
    skill_breakdown: Dict[str, Any] = Field(default_factory=dict)

class AssessmentAttemptResponse(BaseModel):
    id: str
    user_id: str
    role_id: Optional[str]
    role_title: str
    overall_score: int
    time_taken_seconds: int
    question_count: int
    skill_breakdown: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True
