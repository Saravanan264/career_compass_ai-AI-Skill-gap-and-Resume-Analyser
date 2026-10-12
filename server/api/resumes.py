from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from api.auth import get_current_user
from models.user import User
from models.resume import Resume
from models.resume_analysis import ResumeAnalysis
from schemas.resume import (
    ResumeResponse,
    ResumeWithAnalysisResponse,
    ResumeAnalysisResponse,
    ResumeUploadResponse
)
from services.resume_parser import extract_text_from_pdf_bytes, validate_resume_structure
from services.resume_analyzer import analyze_resume_text

router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB limit

@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing")

    filename = file.filename
    if not filename.lower().endswith(".pdf") and file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    pdf_bytes = await file.read()
    file_size = len(pdf_bytes)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds maximum allowed limit of 10MB."
        )

    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # Step 4 & 5: Text Extraction & Cleaning
    parsed_text = extract_text_from_pdf_bytes(pdf_bytes)

    # Step 5b: Resume Structure Validation
    validation = validate_resume_structure(parsed_text)
    if not validation["is_valid_resume"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=validation["validation_reason"]
        )

    # Step 6, 7 & 8: Skill Extraction & Resume Analysis Engine
    analysis_data = analyze_resume_text(parsed_text)


    # Step 2: Store Resume record
    db_resume = Resume(
        user_id=current_user.id,
        file_name=filename,
        file_type=file.content_type or "application/pdf",
        file_size=file_size,
        parsed_text=parsed_text,
        analysis_status="completed"
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)

    # Step 9: Store Resume Analysis record
    db_analysis = ResumeAnalysis(
        resume_id=db_resume.id,
        overall_score=analysis_data["ats"]["overallScore"],
        format_score=analysis_data["ats"]["sectionScores"]["format"],
        experience_score=analysis_data["ats"]["sectionScores"]["experience"],
        skills_score=analysis_data["ats"]["sectionScores"]["skills"],
        education_score=analysis_data["ats"]["sectionScores"]["education"],
        impact_score=analysis_data["ats"]["sectionScores"]["impact"],
        keyword_coverage=analysis_data["ats"]["keywordCoverage"],
        detected_skills=analysis_data["skillsDetected"],
        domains=analysis_data["domains"],
        best_fit_domain=analysis_data["bestFitDomain"],
        confidence=analysis_data["confidence"],
        final_scorecard=analysis_data["finalScorecard"]
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    return {
        "id": db_resume.id,
        "file_name": db_resume.file_name,
        "status": "processed",
        "message": "Resume uploaded and processed successfully",
        "analysis": analysis_data
    }

@router.get("", response_model=List[ResumeResponse])
def get_user_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).all()
    return resumes

@router.get("/{resume_id}", response_model=ResumeWithAnalysisResponse)
def get_resume_by_id(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found or access denied"
        )
    
    analysis_resp = None
    if resume.analysis:
        analysis_resp = {
            "ats": {
                "overallScore": resume.analysis.overall_score,
                "keywordCoverage": resume.analysis.keyword_coverage,
                "sectionScores": {
                    "format": resume.analysis.format_score,
                    "experience": resume.analysis.experience_score,
                    "skills": resume.analysis.skills_score,
                    "education": resume.analysis.education_score,
                    "impact": resume.analysis.impact_score,
                },
                "missingTopKeywords": resume.analysis.final_scorecard.get("missingTopKeywords", [])
                if isinstance(resume.analysis.final_scorecard, dict) else []
            },
            "skillsDetected": resume.analysis.detected_skills,
            "domains": resume.analysis.domains,
            "bestFitDomain": resume.analysis.best_fit_domain,
            "confidence": resume.analysis.confidence,
            "finalScorecard": resume.analysis.final_scorecard
        }

    return {
        "id": resume.id,
        "user_id": resume.user_id,
        "file_name": resume.file_name,
        "file_type": resume.file_type,
        "file_size": resume.file_size,
        "analysis_status": resume.analysis_status,
        "created_at": resume.created_at,
        "updated_at": resume.updated_at,
        "parsed_text": resume.parsed_text,
        "analysis": analysis_resp
    }

@router.get("/{resume_id}/analysis", response_model=ResumeAnalysisResponse)
def get_resume_analysis(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found or access denied"
        )
    
    if not resume.analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found for this resume"
        )

    a = resume.analysis
    all_skills = load_skills_db_helper()
    top_keywords = [s["name"] for s in all_skills[:26]]
    missing_top = [k for k in top_keywords if k not in a.detected_skills]

    return {
        "ats": {
            "overallScore": a.overall_score,
            "keywordCoverage": a.keyword_coverage,
            "sectionScores": {
                "format": a.format_score,
                "experience": a.experience_score,
                "skills": a.skills_score,
                "education": a.education_score,
                "impact": a.impact_score,
            },
            "missingTopKeywords": missing_top
        },
        "skillsDetected": a.detected_skills,
        "domains": a.domains,
        "bestFitDomain": a.best_fit_domain,
        "confidence": a.confidence,
        "finalScorecard": a.final_scorecard
    }

@router.post("/{resume_id}/analyze", response_model=ResumeAnalysisResponse)
def reanalyze_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume or not resume.parsed_text:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume or parsed text not found"
        )

    analysis_data = analyze_resume_text(resume.parsed_text)

    if resume.analysis:
        a = resume.analysis
        a.overall_score = analysis_data["ats"]["overallScore"]
        a.format_score = analysis_data["ats"]["sectionScores"]["format"]
        a.experience_score = analysis_data["ats"]["sectionScores"]["experience"]
        a.skills_score = analysis_data["ats"]["sectionScores"]["skills"]
        a.education_score = analysis_data["ats"]["sectionScores"]["education"]
        a.impact_score = analysis_data["ats"]["sectionScores"]["impact"]
        a.keyword_coverage = analysis_data["ats"]["keywordCoverage"]
        a.detected_skills = analysis_data["skillsDetected"]
        a.domains = analysis_data["domains"]
        a.best_fit_domain = analysis_data["bestFitDomain"]
        a.confidence = analysis_data["confidence"]
        a.final_scorecard = analysis_data["finalScorecard"]
    else:
        a = ResumeAnalysis(
            resume_id=resume.id,
            overall_score=analysis_data["ats"]["overallScore"],
            format_score=analysis_data["ats"]["sectionScores"]["format"],
            experience_score=analysis_data["ats"]["sectionScores"]["experience"],
            skills_score=analysis_data["ats"]["sectionScores"]["skills"],
            education_score=analysis_data["ats"]["sectionScores"]["education"],
            impact_score=analysis_data["ats"]["sectionScores"]["impact"],
            keyword_coverage=analysis_data["ats"]["keywordCoverage"],
            detected_skills=analysis_data["skillsDetected"],
            domains=analysis_data["domains"],
            best_fit_domain=analysis_data["bestFitDomain"],
            confidence=analysis_data["confidence"],
            final_scorecard=analysis_data["finalScorecard"]
        )
        db.add(a)

    db.commit()
    return analysis_data

def load_skills_db_helper():
    from services.skill_extractor import load_skills_db
    return load_skills_db()
