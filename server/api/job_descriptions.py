from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from api.auth import get_current_user
from models.user import User
from models.job_description import JobDescription
from models.job_description_analysis import JobDescriptionAnalysis
from schemas.job_description import (
    JobDescriptionCreate,
    JobDescriptionResponse,
    JobDescriptionAnalysisResponse
)
from services.jd_analyzer import analyze_jd_text

router = APIRouter()

@router.post("", response_model=JobDescriptionResponse)
def create_job_description(
    payload: JobDescriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not payload.description or not payload.description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description text cannot be empty."
        )

    # Analyze JD text
    analysis_data = analyze_jd_text(
        text_raw=payload.description,
        title=payload.title,
        company_name=payload.company_name
    )

    jd_title = payload.title or analysis_data["extractedTitle"]

    # Store JobDescription record
    db_jd = JobDescription(
        user_id=current_user.id,
        title=jd_title,
        company_name=payload.company_name,
        description=payload.description,
        source_type="text"
    )
    db.add(db_jd)
    db.commit()
    db.refresh(db_jd)

    # Store JobDescriptionAnalysis record
    db_analysis = JobDescriptionAnalysis(
        job_description_id=db_jd.id,
        extracted_title=analysis_data["extractedTitle"],
        required_skills=analysis_data["requiredSkills"],
        preferred_skills=analysis_data["preferredSkills"],
        tools=analysis_data["tools"],
        frameworks=analysis_data["frameworks"],
        databases=analysis_data["databases"],
        cloud_technologies=analysis_data["cloudTechnologies"],
        soft_skills=analysis_data["softSkills"],
        experience_requirements=analysis_data["experienceRequirements"],
        education_requirements=analysis_data["educationRequirements"],
        importance=analysis_data["importance"]
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    return {
        "id": db_jd.id,
        "user_id": db_jd.user_id,
        "title": db_jd.title,
        "company_name": db_jd.company_name,
        "description": db_jd.description,
        "source_type": db_jd.source_type,
        "created_at": db_jd.created_at,
        "updated_at": db_jd.updated_at,
        "analysis": {
            "extractedTitle": db_analysis.extracted_title,
            "companyName": db_jd.company_name,
            "requiredSkills": db_analysis.required_skills,
            "preferredSkills": db_analysis.preferred_skills,
            "allSkills": list(set(db_analysis.required_skills + db_analysis.preferred_skills)),
            "tools": db_analysis.tools,
            "frameworks": db_analysis.frameworks,
            "databases": db_analysis.databases,
            "cloudTechnologies": db_analysis.cloud_technologies,
            "softSkills": db_analysis.soft_skills,
            "experienceRequirements": db_analysis.experience_requirements,
            "educationRequirements": db_analysis.education_requirements,
            "importance": db_analysis.importance
        }
    }

@router.get("", response_model=List[JobDescriptionResponse])
def get_user_job_descriptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    jds = db.query(JobDescription).filter(JobDescription.user_id == current_user.id).order_by(JobDescription.created_at.desc()).all()
    
    result = []
    for jd in jds:
        analysis_resp = None
        if jd.analysis:
            a = jd.analysis
            analysis_resp = {
                "extractedTitle": a.extracted_title,
                "companyName": jd.company_name,
                "requiredSkills": a.required_skills,
                "preferredSkills": a.preferred_skills,
                "allSkills": list(set(a.required_skills + a.preferred_skills)),
                "tools": a.tools,
                "frameworks": a.frameworks,
                "databases": a.databases,
                "cloudTechnologies": a.cloud_technologies,
                "softSkills": a.soft_skills,
                "experienceRequirements": a.experience_requirements,
                "educationRequirements": a.education_requirements,
                "importance": a.importance
            }
        
        result.append({
            "id": jd.id,
            "user_id": jd.user_id,
            "title": jd.title,
            "company_name": jd.company_name,
            "description": jd.description,
            "source_type": jd.source_type,
            "created_at": jd.created_at,
            "updated_at": jd.updated_at,
            "analysis": analysis_resp
        })

    return result

@router.get("/{jd_id}", response_model=JobDescriptionResponse)
def get_job_description_by_id(
    jd_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id, JobDescription.user_id == current_user.id).first()
    if not jd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found or access denied."
        )

    analysis_resp = None
    if jd.analysis:
        a = jd.analysis
        analysis_resp = {
            "extractedTitle": a.extracted_title,
            "companyName": jd.company_name,
            "requiredSkills": a.required_skills,
            "preferredSkills": a.preferred_skills,
            "allSkills": list(set(a.required_skills + a.preferred_skills)),
            "tools": a.tools,
            "frameworks": a.frameworks,
            "databases": a.databases,
            "cloudTechnologies": a.cloud_technologies,
            "softSkills": a.soft_skills,
            "experienceRequirements": a.experience_requirements,
            "educationRequirements": a.education_requirements,
            "importance": a.importance
        }

    return {
        "id": jd.id,
        "user_id": jd.user_id,
        "title": jd.title,
        "company_name": jd.company_name,
        "description": jd.description,
        "source_type": jd.source_type,
        "created_at": jd.created_at,
        "updated_at": jd.updated_at,
        "analysis": analysis_resp
    }

@router.get("/{jd_id}/analysis", response_model=JobDescriptionAnalysisResponse)
def get_job_description_analysis(
    jd_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    jd = db.query(JobDescription).filter(JobDescription.id == jd_id, JobDescription.user_id == current_user.id).first()
    if not jd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found or access denied."
        )

    if not jd.analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found for this job description."
        )

    a = jd.analysis
    return {
        "extractedTitle": a.extracted_title,
        "companyName": jd.company_name,
        "requiredSkills": a.required_skills,
        "preferredSkills": a.preferred_skills,
        "allSkills": list(set(a.required_skills + a.preferred_skills)),
        "tools": a.tools,
        "frameworks": a.frameworks,
        "databases": a.databases,
        "cloudTechnologies": a.cloud_technologies,
        "softSkills": a.soft_skills,
        "experienceRequirements": a.experience_requirements,
        "educationRequirements": a.education_requirements,
        "importance": a.importance
    }
