from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class AtsSectionScores(BaseModel):
    format: int
    experience: int
    skills: int
    education: int
    impact: int

class AtsAnalysis(BaseModel):
    overallScore: int
    keywordCoverage: int
    sectionScores: AtsSectionScores
    missingTopKeywords: List[str]

class DomainFit(BaseModel):
    fitScore: int
    have: List[str]
    missing: List[str]

class FinalScoreMetric(BaseModel):
    key: str
    label: str
    score: int
    note: str

class FinalScorecard(BaseModel):
    resumeScore: int
    metrics: List[FinalScoreMetric]

class ResumeAnalysisResponse(BaseModel):
    ats: AtsAnalysis
    skillsDetected: List[str]
    domains: Dict[str, DomainFit]
    bestFitDomain: str
    confidence: int
    finalScorecard: FinalScorecard

    class Config:
        from_attributes = True

class ResumeResponse(BaseModel):
    id: str
    user_id: str
    file_name: str
    file_type: str
    file_size: int
    analysis_status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ResumeWithAnalysisResponse(ResumeResponse):
    parsed_text: Optional[str] = None
    analysis: Optional[ResumeAnalysisResponse] = None

class ResumeUploadResponse(BaseModel):
    id: str
    file_name: str
    status: str
    message: str
    analysis: Optional[ResumeAnalysisResponse] = None
