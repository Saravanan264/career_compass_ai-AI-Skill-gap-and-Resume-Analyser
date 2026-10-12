from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
from reportlab.lib import colors

def add_part2_sections(story, styles, NAVY, INDIGO, TEAL, SLATE_BG, TEXT_DARK, BORDER_COLOR, AMBER, WHITE):

    # SECTION 11: ATS / RESUME SCORE
    story.append(Paragraph("11. ATS / RESUME SCORE", styles['SecHeading']))
    
    ats_text = """
    <b>Weighted Scoring Signals (`server/services/resume_analyzer.py` & `client/src/lib/analyzer.ts`):</b><br/>
    • <b>Format Score (20% Weight):</b> Checks presence of 8 section headers (`email`, `phone`, `linkedin`, `github`, `experience`, `education`, `skills`, `projects`).<br/>
    • <b>Experience Score (25% Weight):</b> Checks industry terms (`intern`, `engineer`, `developer`, `analyst`, `lead`, `manager`, `team`).<br/>
    • <b>Skills Score (30% Weight):</b> Calculated as $\\min(100, \\max(20, \\text{Coverage} \\times 1.25))$, measuring hits against top 26 skills in database.<br/>
    • <b>Education Score (10% Weight):</b> Checks degree terms (`bachelor`, `master`, `b.sc`, `m.sc`, `phd`, `university`).<br/>
    • <b>Impact Score (15% Weight):</b> Checks metrics and action verbs (`%`, `increased`, `reduced`, `improved`, `optimized`, `launched`, `saved`).<br/><br/>
    <b>Formulas:</b><br/>
    $$\\text{ATS Score} = 0.20 \\cdot F + 0.25 \\cdot E_{\\text{exp}} + 0.30 \\cdot S + 0.10 \\cdot E_{\\text{edu}} + 0.15 \\cdot I$$<br/>
    $$\\text{Final Scorecard} = 0.55 \\cdot \\text{ATS} + 0.15 \\cdot \\text{Coverage} + 0.10 \\cdot \\text{Impact} + 0.10 \\cdot \\text{Format} + 0.10 \\cdot \\text{DomainFit}$$<br/><br/>
    <b>Numerical Calculation Example:</b><br/>
    • $F = 87.5\\%$, $E_{\\text{exp}} = 75.0\\%$, $S = 80.0\\%$, $E_{\\text{edu}} = 100.0\\%$, $I = 60.0\\%$.<br/>
    • $\\text{ATS} = (87.5 \\times 0.20) + (75 \\times 0.25) + (80 \\times 0.30) + (100 \\times 0.10) + (60 \\times 0.15) = 17.5 + 18.75 + 24.0 + 10.0 + 9.0 = \\mathbf{79.25 \\rightarrow 79\\%}$.
    """
    story.append(Paragraph(ats_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 12: COMPANY MATCH / JOB ROLE MATCHING
    story.append(Paragraph("12. COMPANY MATCH / JOB ROLE MATCHING", styles['SecHeading']))
    
    comp_text = """
    <b>Company Readiness Engine (`client/src/lib/readiness-engine.ts`):</b><br/>
    Evaluates candidate readiness across tech companies (e.g., Google, Amazon, TCS, Startups) and job roles using three weighted dimensions:<br/>
    $$\\text{Readiness Score} = 0.30 \\times \\text{Profile Match} + 0.30 \\times \\text{Skill Coverage} + 0.40 \\times \\text{Assessment Performance}$$<br/><br/>
    • <b>Profile Match (30%):</b> Weighted skill match against required + preferred skills.<br/>
    • <b>Skill Coverage (30%):</b> Percentage of essential required skills matched.<br/>
    • <b>Assessment Performance (40%):</b> Candidate's quiz score on relevant skill topics.
    """
    story.append(Paragraph(comp_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 13: RECOMMENDATION ENGINE
    story.append(Paragraph("13. RECOMMENDATION ENGINE", styles['SecHeading']))
    
    rec_text = """
    <b>Recommendation Logic:</b><br/>
    • <b>Project Recommender (`client/src/lib/project-recommender.ts`):</b> Ranks target portfolio projects from `projects.json` based on missing skill coverage. High-priority missing skills count double.<br/>
    • <b>Roadmap Generator (`client/src/lib/roadmap.ts`):</b> Maps missing domain skills to structured learning stages (Fundamentals, Advanced, Portfolio Project) from `roadmap.json`.<br/>
    • <i>Deterministic Mapping:</i> Fully data-driven rule engine without random hallucinatory output.
    """
    story.append(Paragraph(rec_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 14: AI / DATA SCIENCE CONTRIBUTION
    story.append(Paragraph("14. AI / DATA SCIENCE CONTRIBUTION", styles['SecHeading']))
    
    ai_box = """
    <b>CRITICAL INTERVIEW DEFENSE: IS THIS REALLY AN AI PROJECT?</b><br/><br/>
    <b>Q1: Is this really an AI project?</b><br/>
    <b>Answer:</b> "Yes, it belongs to the domain of <b>Symbolic AI and Natural Language Processing (NLP)</b>. AI encompasses both deterministic rule-based expert systems and statistical machine learning. Our system uses NLP text cleaning, entity extraction, pattern heuristics, and vector-like scoring algorithms."<br/><br/>
    <b>Q2: Did you train your own Machine Learning model?</b><br/>
    <b>Answer:</b> "No. We deliberately chose a rule-based NLP parser over an ML model like BERT or LLMs for three key reasons: 1) 100% deterministic accuracy with zero hallucinations, 2) sub-50ms execution latency, and 3) full explainability of scoring metrics for candidates."<br/><br/>
    <b>Q3: What algorithm did you use?</b><br/>
    <b>Answer:</b> "We implemented a custom pipeline combining Regex Token Normalization, Canonical Alias Dictionary Matching, Weighted Multi-Factor Linear Scoring, and Set Difference Priority Classification."
    """
    story.append(Table([[Paragraph(ai_box, styles['NormalText'])]], colWidths=[540], style=[
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, AMBER),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(Spacer(1, 15))

    # SECTION 15: COMPLETE ARCHITECTURE
    story.append(Paragraph("15. COMPLETE ARCHITECTURE", styles['SecHeading']))
    
    arch_text = """
    <b>System Layered Architecture:</b><br/>
    1. <b>Presentation Layer (Frontend):</b> React 19 SPA, Tailwind CSS glassmorphism UI, Wouter router, Lucide icons, Recharts SVG charts.<br/>
    2. <b>Client State & Engine Layer:</b> Zustand global state stores (`resume-store`, `job-store`, `assessment-store`), PDF.js client text extractor.<br/>
    3. <b>API Gateway / Service Bridge:</b> Fetch API with Bearer token authentication headers targeting `http://localhost:8000/api`.<br/>
    4. <b>Application Server (Backend):</b> FastAPI framework, Pydantic data schemas, Dependency Injection (`Depends(get_db)`).<br/>
    5. <b>NLP & Business Logic Layer:</b> `resume_parser.py` (PyMuPDF), `skill_extractor.py`, `resume_analyzer.py`, `jd_analyzer.py`.<br/>
    6. <b>Persistence Layer (Database):</b> SQLAlchemy ORM, SQLite database (`server/career_compass.db`) storing Users, Resumes, Analyses, JDs, and Assessments.
    """
    story.append(Paragraph(arch_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 16: DATA FLOW
    story.append(Paragraph("16. DATA FLOW", styles['SecHeading']))
    
    data_flow_text = """
    <b>Data Transformation Objects:</b><br/>
    • <i>Raw PDF File (Binary ArrayBuffer)</i> $\\rightarrow$<br/>
    • <i>Clean Text String</i> (`"experienced in react python mysql..."`) $\\rightarrow$<br/>
    • <i>Extracted Skill Array</i> (`["MySQL", "Python", "React"]`) $\\rightarrow$<br/>
    • <i>Analysis Result JSON:</i>
    """
    story.append(Paragraph(data_flow_text, styles['NormalText']))
    
    json_sample = """
    {
      "ats": { "overallScore": 82, "keywordCoverage": 75, "sectionScores": { "format": 90, "experience": 80, "skills": 85, "education": 100, "impact": 65 } },
      "skillsDetected": ["FastAPI", "Python", "React", "SQLAlchemy", "TypeScript"],
      "bestFitDomain": "Full Stack Development",
      "confidence": 88
    }
    """
    story.append(Paragraph(f"<font face='Courier' size=8 color='#1E293B'>{json_sample.replace(chr(10), '<br/>')}</font>", styles['CodeText']))
    story.append(Spacer(1, 15))

    # SECTION 17: STATE MANAGEMENT
    story.append(Paragraph("17. STATE MANAGEMENT", styles['SecHeading']))
    
    state_text = """
    <b>Zustand Store Architecture (`client/src/state/`):</b><br/>
    • <b>`auth-store.ts`:</b> Persists `accessToken`, `user` object, and login state in `localStorage` under key `"career-compass-auth"`.<br/>
    • <b>`resume-store.ts`:</b> Stores current `parsedText`, `skillsDetected`, `atsScore`, and `analysis` state.<br/>
    • <b>`job-store.ts`:</b> Holds active `jdAnalysis`, candidate match results (`matchingSkills`, `missingSkills`, `jobMatchScore`).<br/>
    • <b>`assessment-store.ts`:</b> Tracks quiz attempt history, active question queue, and skill-wise correctness scores.<br/>
    • <b>TanStack React Query:</b> Manages server synchronization, caching, and auto-refetching.
    """
    story.append(Paragraph(state_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 18: ROUTING
    story.append(Paragraph("18. ROUTING", styles['SecHeading']))
    
    route_data = [
        [Paragraph("<b>Route Path</b>", styles['TableHeader']), Paragraph("<b>Component</b>", styles['TableHeader']), Paragraph("<b>Purpose & Key Action</b>", styles['TableHeader'])],
        [Paragraph("/login", styles['TableText']), Paragraph("Login.tsx", styles['TableText']), Paragraph("User authentication & JWT token retrieval", styles['TableText'])],
        [Paragraph("/register", styles['TableText']), Paragraph("Register.tsx", styles['TableText']), Paragraph("New user registration & account setup", styles['TableText'])],
        [Paragraph("/dashboard", styles['TableText']), Paragraph("Dashboard.tsx", styles['TableText']), Paragraph("Main overview metrics, overall score, quick links", styles['TableText'])],
        [Paragraph("/upload", styles['TableText']), Paragraph("ResumeUpload.tsx", styles['TableText']), Paragraph("Drag-and-drop PDF upload & text parsing", styles['TableText'])],
        [Paragraph("/ats", styles['TableText']), Paragraph("AtsDashboard.tsx", styles['TableText']), Paragraph("ATS score breakdown & section radar metrics", styles['TableText'])],
        [Paragraph("/job-analysis", styles['TableText']), Paragraph("JobAnalysis.tsx", styles['TableText']), Paragraph("Paste JD text or select predefined job role", styles['TableText'])],
        [Paragraph("/skills", styles['TableText']), Paragraph("SkillGapAnalysis.tsx", styles['TableText']), Paragraph("Candidate vs JD match, missing skill priority matrix", styles['TableText'])],
        [Paragraph("/assessment", styles['TableText']), Paragraph("Assessment.tsx", styles['TableText']), Paragraph("Interactive technical quiz for skill validation", styles['TableText'])],
        [Paragraph("/analytics", styles['TableText']), Paragraph("Analytics.tsx", styles['TableText']), Paragraph("Historical attempt trends & skill improvement charts", styles['TableText'])],
        [Paragraph("/roadmap", styles['TableText']), Paragraph("LearningRoadmap.tsx", styles['TableText']), Paragraph("Step-by-step domain learning stages & timelines", styles['TableText'])],
        [Paragraph("/readiness", styles['TableText']), Paragraph("Readiness.tsx", styles['TableText']), Paragraph("Company readiness scores across target employers", styles['TableText'])]
    ]
    t_route = Table(route_data, colWidths=[90, 130, 320])
    t_route.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, SLATE_BG]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_route)
    story.append(Spacer(1, 15))

    # SECTION 19: VISUALIZATION
    story.append(Paragraph("19. VISUALIZATION", styles['SecHeading']))
    
    vis_text = """
    <b>Recharts Components (`client/src/components/charts/`):</b><br/>
    • <b>`ats-score-breakdown.tsx`:</b> BarChart rendering section scores (Format, Experience, Skills, Education, Impact).<br/>
    • <b>`domain-fit-radar.tsx`:</b> RadarChart comparing candidate skills against target domain requirement vectors.<br/>
    • <b>Line Charts (`analytics.tsx`):</b> Tracks score progression across sequential assessment attempts over time.
    """
    story.append(Paragraph(vis_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 20: ERROR HANDLING
    story.append(Paragraph("20. ERROR HANDLING", styles['SecHeading']))
    
    err_text = """
    <b>Robust Exception Handling Matrix:</b><br/>
    • <b>Non-PDF File Upload:</b> Frontend restricts input to `.pdf`; Backend validates content-type and extension, returning `400 Bad Request` ("Only PDF files are supported").<br/>
    • <b>File Size >10MB:</b> Backend checks byte length before processing, raising `413 Payload Too Large`.<br/>
    • <b>Scanned / Image PDF:</b> System catches empty parsed text post-processing, raising `400 Bad Request` informing user of missing OCR layer.<br/>
    • <b>Corrupted / Password-Protected PDF:</b> `fitz.open()` exceptions and `doc.is_encrypted` checks return immediate `400 Bad Request`.<br/>
    • <b>UI Feedback:</b> Integrated with `sonner` / `toaster` notification banners displaying actionable user messages.
    """
    story.append(Paragraph(err_text, styles['NormalText']))
    story.append(Spacer(1, 15))

print("Part 2 sections defined.")
