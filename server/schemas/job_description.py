from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class JobDescriptionCreate(BaseModel):
    title: Optional[str] = None
    company_name: Optional[str] = None
    description: str = Field(..., min_length=10, description="Job description text must not be empty.")

class JobDescriptionAnalysisResponse(BaseModel):
    extractedTitle: str
    companyName: Optional[str] = None
    requiredSkills: List[str]
    preferredSkills: List[str]
    allSkills: List[str]
    tools: List[str]
    frameworks: List[str]
    databases: List[str]
    cloudTechnologies: List[str]
    softSkills: List[str]
    experienceRequirements: Optional[str] = None
    educationRequirements: Optional[str] = None
    importance: Dict[str, int]

    class Config:
        from_attributes = True

class JobDescriptionResponse(BaseModel):
    id: str
    user_id: str
    title: str
    company_name: Optional[str] = None
    description: str
    source_type: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    analysis: Optional[JobDescriptionAnalysisResponse] = None

    class Config:
        from_attributes = True
