from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    resume_id = Column(String, ForeignKey("resumes.id"), nullable=False, unique=True, index=True)
    
    overall_score = Column(Integer, nullable=False)
    format_score = Column(Integer, nullable=False)
    experience_score = Column(Integer, nullable=False)
    skills_score = Column(Integer, nullable=False)
    education_score = Column(Integer, nullable=False)
    impact_score = Column(Integer, nullable=False)
    keyword_coverage = Column(Integer, nullable=False)
    
    detected_skills = Column(JSON, nullable=False)
    domains = Column(JSON, nullable=False)
    best_fit_domain = Column(String, nullable=False)
    confidence = Column(Integer, nullable=False)
    final_scorecard = Column(JSON, nullable=False)
    
    analysis_version = Column(String, default="1.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    resume = relationship("Resume", back_populates="analysis")
