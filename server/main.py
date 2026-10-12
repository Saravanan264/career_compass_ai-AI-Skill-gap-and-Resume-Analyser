import os
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
from core.config import settings
import models
from api.auth import router as auth_router
from api.resumes import router as resumes_router
from api.job_descriptions import router as job_descriptions_router
from api.assessments import router as assessments_router
from api.roadmap import router as roadmap_router
from api.llm import router as llm_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5000", "http://localhost:5173", "http://127.0.0.1:5173", "http://127.0.0.1:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "Career Compass AI API"}

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(resumes_router, prefix="/api/resumes", tags=["resumes"])
app.include_router(job_descriptions_router, prefix="/api/job-descriptions", tags=["job-descriptions"])
app.include_router(assessments_router, prefix="/api/assessments", tags=["assessments"])
app.include_router(roadmap_router, prefix="/api/roadmap", tags=["roadmap"])
app.include_router(llm_router)


