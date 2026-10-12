from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
from reportlab.lib import colors

def add_part3_sections(story, styles, NAVY, INDIGO, TEAL, SLATE_BG, TEXT_DARK, BORDER_COLOR, AMBER, WHITE):

    # SECTION 21: TECHNICAL PROBLEMS AND DEBUGGING
    story.append(Paragraph("21. TECHNICAL PROBLEMS AND DEBUGGING", styles['SecHeading']))
    
    debug_text = """
    <b>5 Real Engineering Challenges Resolved:</b><br/><br/>
    <b>1. Skill Name Alias Mismatch (`React` vs `React.js` vs `ReactJS`):</b><br/>
    • <i>Problem:</i> Resumes had "React.js", JDs had "ReactJS", causing failed exact string matches.<br/>
    • <i>Root Cause:</i> Raw string equality missing canonical normalization.<br/>
    • <i>Fix:</i> Implemented alias mapping array in `skills.json` and regex character normalization in `skill_extractor.py`.<br/><br/>
    <b>2. Multi-Word Skill Truncation (`Spring Boot`, `Machine Learning`):</b><br/>
    • <i>Problem:</i> Naive unigram tokenization split "Spring Boot" into "Spring" and "Boot".<br/>
    • <i>Root Cause:</i> Word-based splitting destroyed multi-word entities.<br/>
    • <i>Fix:</i> Evaluated full multi-word phrase patterns against normalized text before fallback unigram checking.<br/><br/>
    <b>3. Scanned PDF Text Extraction Failure:</b><br/>
    • <i>Problem:</i> Image-only PDFs returned blank strings, causing silent score zeroes.<br/>
    • <i>Root Cause:</i> Lack of embedded font vector layer in scanned PDFs.<br/>
    • <i>Fix:</i> Added post-extraction text length checks raising explicit HTTP 400 validation error informing candidates.<br/><br/>
    <b>4. Zustand State Hydration Desynchronization:</b><br/>
    • <i>Problem:</i> Uploading a new resume did not clear previous JD match state on page navigation.<br/>
    • <i>Root Cause:</i> Independent Zustand stores without reset subscriptions.<br/>
    • <i>Fix:</i> Added explicit store reset action triggers on upload completion in `resume-store.ts`.<br/><br/>
    <b>5. CORS Block on FastAPI Server during Vite Dev:</b><br/>
    • <i>Problem:</i> Browser blocked API requests from `localhost:5000` to `localhost:8000`.<br/>
    • <i>Root Cause:</i> Missing origin headers in FastAPI CORSMiddleware.<br/>
    • <i>Fix:</i> Configured `allow_origins=["http://localhost:5000", "http://localhost:5173"]` in `server/main.py`.
    """
    story.append(Paragraph(debug_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 22: PERFORMANCE
    story.append(Paragraph("22. PERFORMANCE", styles['SecHeading']))
    
    perf_text = """
    <b>Performance Optimization & Scale Benchmarks:</b><br/>
    • <b>Current Latency:</b> PDF Text Extraction (~15ms) + NLP Skill Normalization (~8ms) + Scoring (~5ms) = <b>Total Response Time ~28ms</b>.<br/>
    • <b>Bottlenecks at Scale:</b> Synchronous PDF parsing in main ASGI event loop during concurrent multi-user uploads.<br/>
    • <b>Capacity Analysis:</b><br/>
      - <i>100 Users:</i> Handled single-instance FastAPI + Uvicorn effortlessly (~2% CPU usage).<br/>
      - <i>1,000 Users:</i> Requires Gunicorn process manager with 4 Uvicorn worker instances.<br/>
      - <i>10,000 Users:</i> Requires Redis queue + Celery async background workers to offload PDF parsing.
    """
    story.append(Paragraph(perf_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 23: SECURITY
    story.append(Paragraph("23. SECURITY", styles['SecHeading']))
    
    sec_text = """
    <b>Current Security Implementation vs. Production Roadmap:</b><br/>
    • <b>Current:</b> JWT Token Authentication (Bearer scheme), Passlib with Bcrypt password hashing, Strict File Extension & MIME Type verification, 10MB payload size limits.<br/>
    • <b>Production Additions:</b> Presigned S3 upload URLs to bypass application server bandwidth, ClamAV anti-virus file scanning buffer, Rate Limiting (SlowAPI), Data anonymization / PII scrubbing (phone/email stripping before DB storage), HTTPS with TLS 1.3 encryption.
    """
    story.append(Paragraph(sec_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 24: PRODUCTION ARCHITECTURE
    story.append(Paragraph("24. PRODUCTION ARCHITECTURE", styles['SecHeading']))
    
    prod_arch_text = """
    <b>Proposed Enterprise Production Architecture:</b><br/>
    Cloudflare CDN $\\rightarrow$ API Gateway (Kong / NGINX) $\\rightarrow$ FastAPI Stateless Microservices (Docker / Kubernetes) $\\rightarrow$ RabbitMQ / Celery Worker Queue $\\rightarrow$ PyMuPDF Async Parsing Nodes $\\rightarrow$ PostgreSQL Database + Redis Cache + AWS S3 Storage.
    """
    story.append(Paragraph(prod_arch_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 25: SCALABILITY
    story.append(Paragraph("25. SCALABILITY", styles['SecHeading']))
    
    scale_text = """
    <b>Horizontal Scaling Strategy:</b><br/>
    • <b>Stateless API Nodes:</b> FastAPI server instances maintain no session state in memory; all state is persisted in JWT tokens and database.<br/>
    • <b>Database Optimization:</b> B-Tree indexing on `user_id`, `created_at`, and `resume_id` foreign keys.<br/>
    • <b>Caching:</b> Redis cache for static `skills.json` and canonical domain mappings.
    """
    story.append(Paragraph(scale_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 26: IF I HAD TO ADD REAL LLM/GENAI
    story.append(Paragraph("26. IF I HAD TO ADD REAL LLM/GENAI", styles['SecHeading']))
    
    genai_text = """
    <b>GenAI & Semantic Upgrade Roadmap:</b><br/>
    • <b>Current Keyword Matching:</b> Exact string match after normalization.<br/>
    • <b>Semantic Vector Match (SentenceTransformers / OpenAI Embeddings):</b> Computes cosine similarity between candidate experience vectors and JD vectors. (e.g., Maps "Built RESTful endpoints in Spring Boot" $\\approx$ "Backend API Development" with score 0.89).<br/>
    • <b>LLM RAG Feedback (GPT-4o / Llama-3):</b> Generates personalized bullet-point rewriting suggestions and mock interview practice questions based on exact skill gaps.
    """
    story.append(Paragraph(genai_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 27: WHY THESE TECHNOLOGIES?
    story.append(Paragraph("27. WHY THESE TECHNOLOGIES?", styles['SecHeading']))
    
    why_text = """
    <b>Interview Technical Justifications:</b><br/>
    • <b>Why React 19 + TypeScript?</b> Enables component reusability, modular chart rendering, and strict compile-time type safety.<br/>
    • <b>Why FastAPI + Python?</b> Sub-millisecond performance via Starlette/Pydantic, combined with Python's rich ecosystem for text processing.<br/>
    • <b>Why PyMuPDF over PyPDF2?</b> PyMuPDF is written in C (MuPDF), executing PDF extraction up to 10x faster with superior text layout fidelity.<br/>
    • <b>Why Rule-Based over Pure LLM?</b> Instant execution (28ms vs 3000ms), zero cost per API call, and 100% deterministic explainability.
    """
    story.append(Paragraph(why_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 28: INTERVIEW CROSS QUESTIONS
    story.append(Paragraph("28. INTERVIEW CROSS QUESTIONS (TOP SELECTIONS)", styles['SecHeading']))
    
    q_data = [
        [Paragraph("<b>Category</b>", styles['TableHeader']), Paragraph("<b>Question & Professional English Answer</b>", styles['TableHeader']), Paragraph("<b>Tanglish Summary & Follow-Up</b>", styles['TableHeader'])],
        
        [Paragraph("Easy / Core", styles['TableText']),
         Paragraph("<b>Q: How does PDF text extraction work in your project?</b><br/>A: We use a dual approach: PDF.js on the client for instant browser preview, and PyMuPDF (fitz) on the backend server for robust parsing of raw bytes.", styles['TableText']),
         Paragraph("<b>Tanglish:</b> Client PDF.js-u preview kaaga, backend PyMuPDF fast text extract-panna use aagudhu.<br/><b>Follow-Up:</b> What if PDF has password? We check `doc.is_encrypted` and throw 400 error.", styles['TableText'])],
        
        [Paragraph("Medium / NLP", styles['TableText']),
         Paragraph("<b>Q: How do you handle skill alias variations like React vs React.js?</b><br/>A: We normalize text using regex `[^a-z0-9+.#\\s-]` and match keywords against a canonical alias database in `skills.json`.", styles['TableText']),
         Paragraph("<b>Tanglish:</b> Text lowercase-ah maathi special characters clean panni, `skills.json` alias list oda match pannoom.<br/><b>Follow-Up:</b> How do you prevent partial word false hits? Boundary matching and full phrase priority.", styles['TableText'])],
        
        [Paragraph("Deep Tech / Alg", styles['TableText']),
         Paragraph("<b>Q: Explain your ATS Scoring formula.</b><br/>A: ATS score is a weighted linear combination: Format (20%), Experience (25%), Skills (30%), Education (10%), and Impact (15%).", styles['TableText']),
         Paragraph("<b>Tanglish:</b> 5 parameters ku weightage set panni, average weighted score calculate pannoom.<br/><b>Follow-Up:</b> Why 30% for skills? Skills correlate highest with JD match.", styles['TableText'])],

        [Paragraph("AI / ML", styles['TableText']),
         Paragraph("<b>Q: Is there a trained ML model in your project?</b><br/>A: No, it is a deterministic Symbolic AI system using NLP regex normalization and heuristic vector scoring.", styles['TableText']),
         Paragraph("<b>Tanglish:</b> Machine learning weights training panna la; rule-based NLP algorithms dhaan use pannoom.<br/><b>Follow-Up:</b> How to add AI? Add SentenceTransformer embeddings.", styles['TableText'])],

        [Paragraph("Architecture", styles['TableText']),
         Paragraph("<b>Q: How would you scale this to 100,000 users?</b><br/>A: Offload PDF parsing to Redis + Celery workers, use Gunicorn with multiple Uvicorn workers, and cache skills data.", styles['TableText']),
         Paragraph("<b>Tanglish:</b> API nodes stateless-ah maathi, background worker queue and Redis cache containerize pannoom.<br/><b>Follow-Up:</b> Database choice? Migrate SQLite to PostgreSQL.", styles['TableText'])]
    ]
    t_q = Table(q_data, colWidths=[80, 240, 220])
    t_q.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, SLATE_BG]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_q)
    story.append(Spacer(1, 15))

    # SECTION 29: "I BUILT THIS" DEFENSE
    story.append(Paragraph("29. 'I BUILT THIS' DEFENSE", styles['SecHeading']))
    
    defense_text = """
    <b>Personal Contribution Defense Strategy:</b><br/>
    • <b>My Personal Contributions:</b> I architected the full-stack system, designed the database schema in SQLAlchemy, implemented the PyMuPDF text parser (`server/services/resume_parser.py`), built the 5-signal ATS scoring engine (`resume_analyzer.py`), and developed the Zustand state-driven frontend components in React.<br/>
    • <b>Hardest Technical Bug:</b> Resolving multi-word skill extraction without word boundary truncation. Fixed by evaluating multi-word phrase keys before unigram dictionary checks.<br/>
    • <b>Verification:</b> Verified accuracy using test scripts (`test_phase2_backend.py`, `test_phase3_backend.py`) validating scoring edge cases.
    """
    story.append(Paragraph(defense_text, styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 30: COMPLETE PROJECT PITCH
    story.append(Paragraph("30. COMPLETE PROJECT PITCH", styles['SecHeading']))
    
    story.append(Paragraph("<b>5-Minute Deep Technical Pitch:</b><br/>'Career Compass AI is an end-to-end resume intelligence platform engineered to bridge candidate skill gaps using rule-based NLP, weighted scoring algorithms, and dynamic career roadmaps. When a user uploads a PDF, PyMuPDF parses raw bytes in under 15ms. The text is passed through a regex normalization pipeline that strips noise while preserving tech symbols like C++ or Node.js. Our skill extractor cross-references text against a canonical database of over 100 skills and alias mappings. On the JD side, our parser uses contextual heuristics to classify skills into required versus preferred. We then run a candidate-vs-JD set matching engine that computes a weighted ATS score across 5 core dimensions, a skill coverage percentage, and domain fit metrics displayed on interactive Recharts visualizations. Finally, missing skills dynamically generate personalized project recommendations and learning roadmaps.'", styles['NormalText']))
    story.append(Spacer(1, 15))

    # SECTION 31: FINAL ONE-PAGE REVISION SHEET
    story.append(Paragraph("31. FINAL REVISION CHEAT SHEET", styles['SecHeading']))
    
    cheat_data = [
        [Paragraph("<b>Core Workflow</b>", styles['TableHeader']), Paragraph("<b>10 Must-Remember Technical Points</b>", styles['TableHeader']), Paragraph("<b>10 Likely Interview Questions</b>", styles['TableHeader'])],
        
        [Paragraph("Upload PDF $\\rightarrow$<br/>PyMuPDF Extract $\\rightarrow$<br/>Regex Normalize $\\rightarrow$<br/>Skill Extract $\\rightarrow$<br/>JD Classify $\\rightarrow$<br/>Set Match $\\rightarrow$<br/>ATS Score $\\rightarrow$<br/>Roadmap Render", styles['TableText']),
         Paragraph("1. PyMuPDF fast C engine<br/>2. PDF.js client preview<br/>3. Regex `[^a-z0-9+.#\\s-]`<br/>4. Canonical `skills.json`<br/>5. ATS 5-factor weighting<br/>6. Required vs Preferred<br/>7. Set match $O(N+M)$<br/>8. Zustand global stores<br/>9. FastAPI async ASGI<br/>10. Symbolic Rule NLP", styles['TableText']),
         Paragraph("1. Why PyMuPDF over PyPDF2?<br/>2. How is ATS score computed?<br/>3. How are aliases handled?<br/>4. Is this an ML project?<br/>5. How to handle scanned PDFs?<br/>6. Why FastAPI over Express?<br/>7. How does JD parsing work?<br/>8. How to scale to 10k users?<br/>9. Security measures used?<br/>10. How to add GenAI RAG?", styles['TableText'])]
    ]
    t_cheat = Table(cheat_data, colWidths=[160, 190, 190])
    t_cheat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, SLATE_BG]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_cheat)
    story.append(Spacer(1, 10))

print("Part 3 sections defined.")
