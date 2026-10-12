from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.user import User
from models.assessment_attempt import AssessmentAttempt
from schemas.assessment import AssessmentAttemptCreate, AssessmentAttemptResponse
from api.auth import get_current_user

router = APIRouter()

@router.post("", response_model=AssessmentAttemptResponse)
def submit_assessment(
    attempt_in: AssessmentAttemptCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    attempt = AssessmentAttempt(
        user_id=current_user.id,
        role_id=attempt_in.role_id,
        role_title=attempt_in.role_title,
        overall_score=attempt_in.overall_score,
        time_taken_seconds=attempt_in.time_taken_seconds,
        question_count=attempt_in.question_count,
        skill_breakdown=attempt_in.skill_breakdown
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt

@router.get("", response_model=List[AssessmentAttemptResponse])
def list_assessments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    attempts = (
        db.query(AssessmentAttempt)
        .filter(AssessmentAttempt.user_id == current_user.id)
        .order_by(AssessmentAttempt.created_at.desc())
        .all()
    )
    return attempts
