from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from services.llm_service import llm_service

router = APIRouter(prefix="/api/llm", tags=["LLM Enhancement"])

class AtsExplanationRequest(BaseModel):
    overallScore: float
    keywordCoverage: float
    missingTopKeywords: List[str] = []

class SkillGapExplanationRequest(BaseModel):
    skill: str
    requirement: str
    candidate_status: str
    assessment_score: Optional[float] = None

class RoadmapExplanationRequest(BaseModel):
    stage_title: str
    focus_skills: List[str] = []
    priority: str

@router.get("/status")
def get_llm_status():
    return {
        "enabled": llm_service.enabled,
        "available": llm_service.is_available(),
        "provider": llm_service.provider if llm_service.is_available() else "none"
    }

@router.post("/explain-ats")
def explain_ats(req: AtsExplanationRequest):
    return llm_service.generate_ats_explanation(req.dict())

@router.post("/explain-skill-gap")
def explain_skill_gap(req: SkillGapExplanationRequest):
    return llm_service.generate_skill_gap_explanation(
        skill=req.skill,
        requirement=req.requirement,
        candidate_status=req.candidate_status,
        assessment_score=req.assessment_score
    )

@router.post("/explain-roadmap")
def explain_roadmap(req: RoadmapExplanationRequest):
    return llm_service.generate_roadmap_explanation(
        stage_title=req.stage_title,
        focus_skills=req.focus_skills,
        priority=req.priority
    )
