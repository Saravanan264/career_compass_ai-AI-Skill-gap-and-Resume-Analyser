import uuid
from sqlalchemy import Column, String, Integer, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class JobDescriptionAnalysis(Base):
    __tablename__ = "job_description_analyses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_description_id = Column(String, ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False, unique=True)
    extracted_title = Column(String, nullable=False)
    required_skills = Column(JSON, nullable=False, default=list)
    preferred_skills = Column(JSON, nullable=False, default=list)
    tools = Column(JSON, nullable=False, default=list)
    frameworks = Column(JSON, nullable=False, default=list)
    databases = Column(JSON, nullable=False, default=list)
    cloud_technologies = Column(JSON, nullable=False, default=list)
    soft_skills = Column(JSON, nullable=False, default=list)
    experience_requirements = Column(String, nullable=True)
    education_requirements = Column(String, nullable=True)
    importance = Column(JSON, nullable=False, default=dict)
    analysis_version = Column(String, default="1.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    job_description = relationship("JobDescription", back_populates="analysis")
