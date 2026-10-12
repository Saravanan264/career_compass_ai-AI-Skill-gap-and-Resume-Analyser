from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
from reportlab.lib import colors

def add_part1_sections(story, styles, NAVY, INDIGO, TEAL, SLATE_BG, TEXT_DARK, BORDER_COLOR, AMBER, WHITE):
    
    # COVER / TITLE BANNER
    story.append(Spacer(1, 10))
    title_p = Paragraph("<font color='#0F172A'><b>CAREER COMPASS AI</b></font><br/><font color='#4F46E5' size=14>Complete Interview-Ready Technical Documentation</font>", styles['DocTitle'])
    story.append(title_p)
    story.append(Spacer(1, 6))
    
    sub_p = Paragraph("<b>Project Subtitle:</b> AI Skill Gap & Resume Analyser | Full Codebase Architecture & Technical Interview Defense", styles['NormalText'])
    story.append(sub_p)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=INDIGO, spaceBefore=0, spaceAfter=15))

    # SECTION 1: PROJECT OVERVIEW
    story.append(Paragraph("1. PROJECT OVERVIEW", styles['SecHeading']))
    
    overview_text = """
    <b>Project Title:</b> AI Skill Gap and Resume Analyser / Career Compass AI<br/>
    <b>Problem Statement:</b> Job seekers and students struggle to align their resumes with dynamic industry Job Descriptions (JDs). ATS systems reject up to 75% of resumes due to keyword mismatches, formatting flaws, and unquantified impact. Candidates lack objective, data-driven feedback on exact skill gaps, domain readiness, and structured learning paths.<br/><br/>
    <b>Why This Problem Matters:</b> Without automated analysis, candidates waste hundreds of hours applying blindly without knowing why their applications fail. Bridging this gap requires objective text processing, skill classification, ATS scoring, and targeted roadmap generation.<br/><br/>
    <b>Target Users:</b> Job seekers, university students, career switchers, technical recruiters, and educational institutions.<br/><br/>
    <b>Main Objective:</b> Provide an end-to-end web platform that parses PDF resumes, extracts skills via rule-based NLP, evaluates Job Descriptions, computes weighted ATS & skill gap scores, generates domain readiness metrics, and provides adaptive learning roadmaps and project recommendations.
    """
    story.append(Paragraph(overview_text, styles['NormalText']))
    story.append(Spacer(1, 10))

    # Features callout box
    features_html = """
    <b>Key Features Implemented:</b><br/>
    • <b>Multi-Page PDF Parsing:</b> Client-side (PDF.js) and Server-side (PyMuPDF fitz) text extraction.<br/>
    • <b>Rule-Based NLP Skill Extraction:</b> Normalization & alias dictionary matching across 100+ technical skills.<br/>
    • <b>Weighted ATS Scoring Engine:</b> Evaluates Format (20%), Experience (25%), Skills (30%), Education (10%), & Impact (15%).<br/>
    • <b>Job Description Classification:</b> Distinguishes Required vs. Preferred skills using contextual heuristics.<br/>
    • <b>Skill Gap & Priority Calculation:</b> Computes coverage %, job match %, and prioritizes missing skills (High/Med/Low).<br/>
    • <b>Domain Fit & Career Readiness:</b> Evaluates readiness across software domains (Frontend, Backend, Data Science, etc.).<br/>
    • <b>Interactive Assessment & Analytics:</b> Role-based technical quiz engine with historical attempt tracking.<br/>
    • <b>Adaptive Roadmaps & Project Recommender:</b> Maps missing skills to actionable projects and learning timelines.
    """
    story.append(Table([[Paragraph(features_html, styles['CalloutText'])]], colWidths=[540], style=[
        ('BACKGROUND', (0,0), (-1,-1), SLATE_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(Spacer(1, 10))

    # Software Engineering vs AI/DS
    se_vs_ai = """
    <b>Software Development vs. AI/Data Science Breakdown:</b><br/>
    • <b>Software Engineering (Full-Stack):</b> React 19, TypeScript, Vite, Wouter routing, Tailwind CSS, Zustand state stores, Recharts visualization, FastAPI server, SQLAlchemy ORM, SQLite database.<br/>
    • <b>AI / Data Science (NLP & Analytics):</b> PyMuPDF text parsing, regex normalization, entity keyword matching, heuristic skill classification, weighted scoring vector algorithms, domain fit analytics.
    """
    story.append(Paragraph(se_vs_ai, styles['NormalText']))
    story.append(Spacer(1, 10))

    # Pitch Box
    pitch_html = """
    <b>INTERVIEW ELEVATOR PITCHES:</b><br/>
    • <b>30-Second Pitch:</b> "Career Compass AI is an intelligent resume analyzer and skill gap detection platform. It parses candidate resumes, extracts technical skills using NLP text normalization, compares them against job descriptions, and calculates an objective ATS score and skill gap matrix to provide custom learning roadmaps."<br/>
    • <b>1-Minute Pitch:</b> "I developed Career Compass AI to solve high ATS rejection rates for job seekers. The system extracts text from PDF resumes using PyMuPDF, normalizes terms to resolve alias variations, and extracts skills across 100+ technical domains. It then analyzes JDs to classify required vs. preferred skills, computes a weighted ATS score based on format, impact, experience, education, and skills, and generates domain readiness scores alongside targeted project recommendations."<br/>
    • <b>2-Minute Pitch:</b> "Career Compass AI is a full-stack AI/Data Science application built with React 19, TypeScript, FastAPI, and Python NLP services. When a candidate uploads a PDF resume, our dual-parsing layer extracts raw text, applies regex normalization, and executes dictionary pattern matching to identify candidate skills. On the job side, our JD engine classifies skills into required and preferred based on contextual text heuristics. The candidate-to-JD engine performs weighted set matching, producing an ATS score breakdown, skill gap priority queue, and domain readiness radar. Furthermore, candidates can take adaptive technical assessments to benchmark their proficiency and receive customized project roadmaps."
    """
    story.append(Table([[Paragraph(pitch_html, styles['NormalText'])]], colWidths=[540], style=[
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
        ('BOX', (0,0), (-1,-1), 1, INDIGO),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(Spacer(1, 15))

    # SECTION 2: TECHNOLOGY STACK — ACTUAL PROJECT
    story.append(Paragraph("2. TECHNOLOGY STACK — ACTUAL PROJECT", styles['SecHeading']))
    
    tech_data = [
        [Paragraph("<b>Technology</b>", styles['TableHeader']),
         Paragraph("<b>Where Used</b>", styles['TableHeader']),
         Paragraph("<b>Why Used</b>", styles['TableHeader']),
         Paragraph("<b>Alternative</b>", styles['TableHeader']),
         Paragraph("<b>Why This Choice</b>", styles['TableHeader'])],
        
        [Paragraph("React 19", styles['TableText']), Paragraph("client/src", styles['TableText']), Paragraph("Component UI architecture", styles['TableText']), Paragraph("Vue / Angular", styles['TableText']), Paragraph("Ecosystem & Virtual DOM speed", styles['TableText'])],
        [Paragraph("TypeScript 5.6", styles['TableText']), Paragraph("client/src", styles['TableText']), Paragraph("Strict type safety", styles['TableText']), Paragraph("Plain JS", styles['TableText']), Paragraph("Prevents runtime state bugs", styles['TableText'])],
        [Paragraph("Vite 7.1", styles['TableText']), Paragraph("Root / client", styles['TableText']), Paragraph("Fast HMR build tool", styles['TableText']), Paragraph("Webpack / CRA", styles['TableText']), Paragraph("Instant dev server start", styles['TableText'])],
        [Paragraph("Tailwind CSS 4", styles['TableText']), Paragraph("client/src/index.css", styles['TableText']), Paragraph("Utility-first styling", styles['TableText']), Paragraph("Bootstrap", styles['TableText']), Paragraph("Custom dark glassmorphism design", styles['TableText'])],
        [Paragraph("Wouter 3.3", styles['TableText']), Paragraph("client/src/App.tsx", styles['TableText']), Paragraph("Lightweight router", styles['TableText']), Paragraph("React Router v6", styles['TableText']), Paragraph("Minimal footprint (<1.5KB)", styles['TableText'])],
        [Paragraph("Zustand 5.0", styles['TableText']), Paragraph("client/src/state", styles['TableText']), Paragraph("Global state management", styles['TableText']), Paragraph("Redux Toolkit", styles['TableText']), Paragraph("Boilerplate-free hook state", styles['TableText'])],
        [Paragraph("Recharts 2.15", styles['TableText']), Paragraph("client/src/components/charts", styles['TableText']), Paragraph("Data visualization", styles['TableText']), Paragraph("Chart.js", styles['TableText']), Paragraph("Native React SVG support", styles['TableText'])],
        [Paragraph("PDF.js 3.11", styles['TableText']), Paragraph("client/src/lib/pdf.ts", styles['TableText']), Paragraph("Client PDF text extract", styles['TableText']), Paragraph("pdf-parse", styles['TableText']), Paragraph("Client-side browser parsing", styles['TableText'])],
        [Paragraph("Python 3.11 / FastAPI", styles['TableText']), Paragraph("server/main.py", styles['TableText']), Paragraph("High-perf REST backend", styles['TableText']), Paragraph("Node.js Express", styles['TableText']), Paragraph("Native NLP & ML library support", styles['TableText'])],
        [Paragraph("PyMuPDF (fitz)", styles['TableText']), Paragraph("server/services/resume_parser.py", styles['TableText']), Paragraph("Server PDF extraction", styles['TableText']), Paragraph("PyPDF2 / pdfplumber", styles['TableText']), Paragraph("10x faster execution speed", styles['TableText'])],
        [Paragraph("SQLAlchemy", styles['TableText']), Paragraph("server/core/database.py", styles['TableText']), Paragraph("Python Database ORM", styles['TableText']), Paragraph("Raw SQL", styles['TableText']), Paragraph("Type-safe database abstraction", styles['TableText'])],
        [Paragraph("SQLite / PyMongo", styles['TableText']), Paragraph("server/career_compass.db", styles['TableText']), Paragraph("Local relational DB", styles['TableText']), Paragraph("PostgreSQL", styles['TableText']), Paragraph("Zero-config local persistence", styles['TableText'])]
    ]

    t_tech = Table(tech_data, colWidths=[70, 80, 130, 90, 170])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, SLATE_BG]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 15))

    # SECTION 3: COMPLETE FOLDER STRUCTURE
    story.append(Paragraph("3. COMPLETE FOLDER STRUCTURE", styles['SecHeading']))
    
    struct_text = """
    <b>Project Codebase Directory Layout:</b><br/>
    • <b>server/main.py:</b> FastAPI entry point, CORS setup, router inclusion (`/api/auth`, `/api/resumes`, `/api/job-descriptions`, `/api/assessments`).<br/>
    • <b>server/services/resume_parser.py:</b> PDF byte parser using PyMuPDF (`fitz`), clean text regex processing.<br/>
    • <b>server/services/skill_extractor.py:</b> Text normalization and alias keyword matching engine.<br/>
    • <b>server/services/resume_analyzer.py:</b> ATS scoring engine (5 signals), domain fit calculator, scorecard generator.<br/>
    • <b>server/services/jd_analyzer.py:</b> Job Description title extraction, required vs preferred skill classifier.<br/>
    • <b>server/data/skills.json & domains.json:</b> Canonical skills database and target domain skill mappings.<br/>
    • <b>client/src/App.tsx:</b> Wouter client routing table and QueryClientProvider wrapper.<br/>
    • <b>client/src/lib/pdf.ts:</b> PDF.js browser text extraction service with progress callback.<br/>
    • <b>client/src/lib/analyzer.ts:</b> Client-side resume analysis fallback engine.<br/>
    • <b>client/src/lib/skill-matcher.ts:</b> Candidate vs. JD skill comparison & priority sorting.<br/>
    • <b>client/src/state/*.ts:</b> Zustand global state stores (`resume-store`, `job-store`, `assessment-store`, `auth-store`).<br/>
    • <b>client/src/pages/*.tsx:</b> 15 full UI views (`dashboard`, `resume-upload`, `ats-dashboard`, `job-analysis`, `skill-gap-analysis`, `assessment`, `analytics`, `learning-roadmap`, `readiness`).
    """
    story.append(Paragraph(struct_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 4: COMPLETE END-TO-END FLOW
    story.append(Paragraph("4. COMPLETE END-TO-END FLOW", styles['SecHeading']))
    
    flow_html = """
    <b>Step-by-Step Data Flow (User Upload to Dashboard):</b><br/>
    1. <b>User Upload:</b> Candidate selects a PDF file via drag-and-drop on `client/src/pages/resume-upload.tsx`.<br/>
    2. <b>Client Processing & API Dispatch:</b> File is validated (<10MB, PDF format). Client uses `pdf.ts` (PDF.js) or dispatches `POST /api/resumes/upload` with FormData via `api.ts`.<br/>
    3. <b>Text Extraction:</b> PyMuPDF (`fitz.open`) reads bytes in `resume_parser.py`, extracts page strings, and raises error if scanned/encrypted.<br/>
    4. <b>Text Preprocessing:</b> `clean_resume_text` normalizes whitespace, tabs, and line breaks while preserving technical characters (+, #, .).<br/>
    5. <b>Skill Extraction & Normalization:</b> `extract_skills` normalizes text to lowercase, strips punctuation, and matches against `skills.json` names and alias arrays.<br/>
    6. <b>JD Analysis & Classification:</b> `jd_analyzer.py` parses JD text, identifying required skills (near "must have") vs preferred skills (near "nice to have").<br/>
    7. <b>Candidate vs. JD Comparison:</b> `matchResumeToJd` (`skill-matcher.ts`) filters matching vs missing skills and computes priority levels.<br/>
    8. <b>ATS Scoring & Domain Fit:</b> `compute_ats` evaluates Format, Experience, Skills, Education, & Impact. `compute_domain_fits` computes radar chart vector scores.<br/>
    9. <b>Recommendation & Roadmap:</b> Missing skills feed `project-recommender.ts` and `roadmap.ts` to build personalized career steps.<br/>
    10. <b>UI Render:</b> Zustand stores update and React components render scorecards, Recharts radar/bar charts, and skill gap tables.
    """
    story.append(Table([[Paragraph(flow_html, styles['NormalText'])]], colWidths=[540], style=[
        ('BACKGROUND', (0,0), (-1,-1), SLATE_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(Spacer(1, 15))

    # SECTION 5: RESUME PDF PROCESSING
    story.append(Paragraph("5. RESUME PDF PROCESSING", styles['SecHeading']))
    
    pdf_text = """
    <b>Accepted File Types:</b> `.pdf` (validated via file extension and `content_type == 'application/pdf'`).<br/>
    <b>Client PDF Extraction:</b> Implemented in `client/src/lib/pdf.ts` using `pdfjs-dist/legacy/build/pdf`. ArrayBuffer is loaded via `pdfjsLib.getDocument`, iterating through pages and assembling text content.<br/>
    <b>Backend PDF Extraction:</b> Implemented in `server/services/resume_parser.py` using PyMuPDF (`fitz`). Reads raw bytes with `fitz.open(stream=pdf_bytes, filetype="pdf")`.<br/>
    <b>Error Handling & Edge Cases:</b><br/>
    • Encrypted PDF -> Raises `400 Bad Request` ("Password-protected PDF files are not supported").<br/>
    • Zero pages / Empty file -> Raises `400 Bad Request` or `413 Payload Too Large` if >10MB.<br/>
    • Scanned / Image-only PDF -> Detects empty text string post-parsing and raises `400 Bad Request` ("Could not extract text from PDF. The file may be image-only or scanned without OCR text").<br/><br/>
    <b>Tanglish Explanation:</b> PDF file-a open panni, PyMuPDF load panno. Pages illana or password protection irundha immediate-a error raise panno. Scanned images-ah irundha text extract aagadhu, so validation throw panno.<br/><br/>
    <b>Interview Defense Strategy:</b> "We chose PyMuPDF on the backend because it runs natively in C (MuPDF engine), making it 10x faster than pure-Python parsers like PyPDF2. On the frontend, we integrated PDF.js so candidates receive immediate feedback even before backend upload."
    """
    story.append(Paragraph(pdf_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 6: NLP / TEXT PROCESSING
    story.append(Paragraph("6. NLP / TEXT PROCESSING", styles['SecHeading']))
    
    nlp_text = """
    <b>Techniques Implemented:</b><br/>
    • <b>Tokenization & Lowercasing:</b> All text is converted to lowercase via `text.lower()`.<br/>
    • <b>Punctuation Cleaning with Character Preservation:</b> `re.sub(r'[^a-z0-9+.#\s-]', ' ', text)` cleans special symbols while preserving critical tech tokens like `C++`, `C#`, `.NET`, `Node.js`.<br/>
    • <b>Whitespace Normalization:</b> `re.sub(r'\s+', ' ', text)` collapses multi-spaces and newlines into uniform single spaces.<br/>
    • <b>Regex Pattern Matching:</b> Used in `jd_analyzer.py` for experience detection (`re.search(r'\d+\+?\s*years', text)`) and education degree detection (`re.search(r'bachelor|master|phd', text)`).<br/><br/>
    <b>Critical AI Distinction:</b> This project utilizes <b>Rule-Based NLP and Heuristic Text Analytics</b>. It does NOT use trained deep learning weights or LLM transformers, guaranteeing 100% deterministic, instant, and reproducible results.
    """
    story.append(Paragraph(nlp_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 7: SKILL EXTRACTION
    story.append(Paragraph("7. SKILL EXTRACTION", styles['SecHeading']))
    
    extraction_text = """
    <b>Skill Extraction Logic:</b><br/>
    Skills are extracted using `extract_skills()` in `server/services/skill_extractor.py` and `client/src/lib/analyzer.ts`. The system loads `skills.json`, where each skill defines a canonical name and an array of alias keywords.<br/><br/>
    <b>Concrete Code Trace & Example:</b><br/>
    • <i>Resume Text:</i> "Experienced in React.js, Java, Python, and MySQL."<br/>
    • <i>JD Text:</i> "Required: React, Java, Docker, AWS."<br/>
    1. Text is normalized: `"experienced in react.js java python and mysql"`<br/>
    2. Skill loop evaluates `React`: Canonical name = `"React"`, Keywords = `["React", "React.js", "ReactJS"]`. Normalized keyword `"react.js"` is found in text -> Match added: `"React"`.<br/>
    3. Output: `["Java", "MySQL", "Python", "React"]` (Sorted alphabetically, deduplicated).
    """
    story.append(Paragraph(extraction_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 8: SKILL NORMALIZATION
    story.append(Paragraph("8. SKILL NORMALIZATION", styles['SecHeading']))
    
    norm_table_data = [
        [Paragraph("<b>Raw Skill Input</b>", styles['TableHeader']), Paragraph("<b>Normalized Text</b>", styles['TableHeader']), Paragraph("<b>Canonical Skill Output</b>", styles['TableHeader'])],
        [Paragraph("React.js / ReactJS / React JS", styles['TableText']), Paragraph("react js", styles['TableText']), Paragraph("React", styles['TableText'])],
        [Paragraph("Node.js / NodeJS / Node", styles['TableText']), Paragraph("node js", styles['TableText']), Paragraph("Node.js", styles['TableText'])],
        [Paragraph("Python / python / PYTHON", styles['TableText']), Paragraph("python", styles['TableText']), Paragraph("Python", styles['TableText'])],
        [Paragraph("Amazon Web Services / AWS", styles['TableText']), Paragraph("aws", styles['TableText']), Paragraph("AWS", styles['TableText'])],
        [Paragraph("PostgreSQL / Postgres / PG", styles['TableText']), Paragraph("postgres", styles['TableText']), Paragraph("PostgreSQL", styles['TableText'])]
    ]
    t_norm = Table(norm_table_data, colWidths=[180, 180, 180])
    t_norm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, SLATE_BG]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_norm)
    story.append(Spacer(1, 15))

    # SECTION 9: SKILL MATCHING ALGORITHM
    story.append(Paragraph("9. SKILL MATCHING ALGORITHM", styles['SecHeading']))
    
    matching_text = """
    <b>Matching Engine (`client/src/lib/skill-matcher.ts`):</b><br/>
    • <b>Matched Skills:</b> $S_{\\text{matched}} = S_{\\text{resume}} \\cap S_{\\text{JD}}$<br/>
    • <b>Missing Skills (Required):</b> $S_{\\text{missing}} = S_{\\text{JD, required}} \\setminus S_{\\text{resume}}$<br/>
    • <b>Improvement Areas (Preferred):</b> $S_{\\text{improve}} = S_{\\text{JD, preferred}} \\setminus S_{\\text{resume}}$<br/><br/>
    <b>Priority Sorting:</b><br/>
    • <i>High Priority:</i> Skill is missing AND JD Importance $\\ge 8$.<br/>
    • <i>Medium Priority:</i> Skill is missing AND JD Importance $\\ge 5$.<br/>
    • <i>Low Priority:</i> Skill is preferred or optional.<br/><br/>
    <b>Time Complexity:</b> $O(N \\times M)$ where $N$ is candidate skills and $M$ is JD skills. With normalized set hash lookups, matching reduces to $O(N + M)$.
    """
    story.append(Paragraph(matching_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 10: SKILL GAP CALCULATION
    story.append(Paragraph("10. SKILL GAP CALCULATION", styles['SecHeading']))
    
    gap_text = """
    <b>Formulas:</b><br/>
    1. <b>Required Skill Coverage:</b><br/>
    $$\\text{Skill Coverage (\\%)} = \\left( \\frac{|S_{\\text{matched required}}|}{{|S_{\\text{total required}}|}} \\right) \\times 100$$<br/>
    2. <b>Weighted Job Match Score:</b><br/>
    $$\\text{Job Match Score (\\%)} = \\left( \\frac{\\sum_{s \\in S_{\\text{matched}}} \\text{Importance}(s)}{\\sum_{s \\in S_{\\text{all JD}}} \\text{Importance}(s)} \\right) \\times 100$$<br/><br/>
    <b>Numerical Worked Example:</b><br/>
    • Total JD Required Skills = 10. Matched Required Skills = 7.<br/>
    • Skill Coverage = $(7 / 10) \\times 100 = 70\\%$.<br/>
    • Total Importance Weight = 80. Matched Importance Weight = 60.<br/>
    • Job Match Score = $(60 / 80) \\times 100 = 75\\%$.
    """
    story.append(Paragraph(gap_text, styles['NormalText']))
    story.append(Spacer(1, 15))

print("Part 1 sections defined.")
