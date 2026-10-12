# Career Compass AI 🧭
### AI-Powered Resume Analyzer, Skill Gap Assessor & Adaptive Career Navigator

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript-61DAFB?style=flat-square&logo=react)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Bundler-Vite-646CFF?style=flat-square&logo=vite)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38B2AC?style=flat-square&logo=tailwind-css)](https://tailwindcss.com/)

---

## 📌 Overview

**Career Compass AI** is an intelligent, full-stack career development and recruitment preparation platform. It evaluates resumes against industry job descriptions, identifies critical skill gaps, administers adaptive skill assessments, and generates personalized learning roadmaps and hands-on project recommendations to bridge those gaps.

---

## 🚀 Key Features

- **Dynamic ATS Scoring & Resume Parsing**:
  - Multi-page and multi-format document parser (PDF, DOCX, TXT).
  - Evidence-based ATS scoring covering formatting, keyword alignment, quantified achievements, and section completeness.
- **Job Description (JD) Alignment**:
  - Automated keyword extraction and technical requirement parsing.
  - Role-specific compatibility indexing.
- **Skill Gap Analysis**:
  - Highlights strong, moderate, and missing skills based on targeted job profiles.
  - Domain-tailored benchmarks across AI/ML, Full Stack, Cloud/DevOps, Data Engineering, and more.
- **Adaptive 30-Question Assessment Engine**:
  - Dynamic question selection prioritized by resume-detected skills and job-role requirements.
- **Smart Project & Roadmap Generator**:
  - Curated, hands-on portfolio projects targeting identified skill gaps.
  - Step-by-step progressive learning roadmaps with curated resources.
- **Comprehensive PDF Reporting**:
  - Automated generation of technical interview reports, candidate breakdowns, and academic reviews.

---

## 📁 Repository Structure

```
├── client/                 # React + TypeScript Frontend (Vite)
│   ├── src/
│   │   ├── components/     # UI & Layout Components (shadcn/ui + Radix)
│   │   ├── pages/          # ATS Dashboard, Assessments, Roadmaps, Projects
│   │   ├── lib/            # Analytics, analyzers, scoring logic, API client
│   │   └── state/          # Zustand / State management stores
│   └── package.json
├── server/                 # FastAPI Python Backend
│   ├── api/                # API Endpoints (Auth, Resumes, JDs, Assessments)
│   ├── core/               # Database, Security, Config
│   ├── models/             # SQLAlchemy / Pydantic models
│   ├── schemas/            # Request & Response schemas
│   ├── services/           # Resume parser, JD analyzer, skill extractor
│   ├── requirements.txt    # Python dependencies
│   └── main.py             # FastAPI Application entry point
├── docs/                   # Architectural & Technical Documentation
├── project_reports/        # Presentation decks & Academic Reviews
│   ├── career_compass_ai_final review.pptx
│   ├── confrence paper_career_compass_ai.pdf
│   ├── plagarism_report.pdf
│   └── skill gap report_merged.pdf
├── run_project.bat         # One-click startup script for Windows
└── package.json            # Root project metadata & scripts
```

---

## 🛠️ Quick Start & Setup

### Prerequisites
- **Node.js** (v18+) & **npm**
- **Python** (v3.10+)

### 1. One-Click Launch (Windows)
Double-click `run_project.bat` or run:
```cmd
run_project.bat
```
This automatically boots both:
- **FastAPI Backend**: `http://localhost:8000` (API Docs at `/docs`)
- **Vite Frontend**: `http://localhost:5000`

---

### 2. Manual Setup

#### Backend Setup
```bash
cd server
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### Frontend Setup
```bash
# In the project root:
npm install
npm run dev
```

---

## 📄 License
This project is licensed under the MIT License.
