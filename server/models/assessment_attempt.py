from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    role_id = Column(String, nullable=True)
    role_title = Column(String, nullable=False)
    overall_score = Column(Integer, nullable=False)
    time_taken_seconds = Column(Integer, nullable=False, default=0)
    skill_breakdown = Column(JSON, nullable=False)  # dict of skill -> score/percentage
    question_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="assessment_attempts")
