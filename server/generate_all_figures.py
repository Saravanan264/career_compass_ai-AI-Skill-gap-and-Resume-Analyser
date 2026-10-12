import os
from PIL import Image, ImageDraw, ImageFont

# Set up output directories
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "figures")
CH3_DIR = os.path.join(BASE_DIR, "chapter3")
CH5_DIR = os.path.join(BASE_DIR, "chapter5")
CH6_DIR = os.path.join(BASE_DIR, "chapter6")
CH7_DIR = os.path.join(BASE_DIR, "chapter7")

for d in [CH3_DIR, CH5_DIR, CH6_DIR, CH7_DIR]:
    os.makedirs(d, exist_ok=True)

print("Created directory structure for docs/figures/")

def create_box_diagram(width, height, title, subtitle, boxes, arrows, output_path):
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Try loading default font
    try:
        title_font = ImageFont.truetype("arial.ttf", 22)
        sub_font = ImageFont.truetype("arial.ttf", 14)
        box_title_font = ImageFont.truetype("arialbd.ttf", 15)
        text_font = ImageFont.truetype("arial.ttf", 13)
    except:
        title_font = ImageFont.load_default()
        sub_font = title_font
        box_title_font = title_font
        text_font = title_font

    # Draw Title Header
    draw.rectangle([0, 0, width, 60], fill=(245, 247, 250), outline=(210, 215, 220))
    draw.text((20, 12), title.upper(), fill=(15, 23, 42), font=title_font)
    draw.text((20, 38), subtitle, fill=(100, 116, 139), font=sub_font)
    
    # Draw Boxes
    for b in boxes:
        # b: (x, y, w, h, header_text, body_lines, fill_color, border_color)
        x, y, w, h = b[0], b[1], b[2], b[3]
        header = b[4]
        body = b[5]
        fill = b[6] if len(b) > 6 else (255, 255, 255)
        border = b[7] if len(b) > 7 else (51, 65, 85)
        
        draw.rectangle([x, y, x+w, y+h], fill=fill, outline=border, width=2)
        
        # Header banner
        draw.rectangle([x, y, x+w, y+30], fill=(230, 235, 245), outline=border, width=1)
        draw.text((x + 10, y + 6), header, fill=(30, 41, 59), font=box_title_font)
        
        # Body text
        curr_y = y + 36
        for line in body:
            draw.text((x + 10, curr_y), line, fill=(51, 65, 85), font=text_font)
            curr_y += 18
            
    # Draw Arrows
    for a in arrows:
        # a: (x1, y1, x2, y2, label)
        x1, y1, x2, y2 = a[0], a[1], a[2], a[3]
        label = a[4] if len(a) > 4 else ""
        
        draw.line([x1, y1, x2, y2], fill=(71, 85, 105), width=2)
        # Arrow head
        if x1 == x2: # Vertical
            if y2 > y1:
                draw.polygon([(x2-5, y2-8), (x2+5, y2-8), (x2, y2)], fill=(71, 85, 105))
            else:
                draw.polygon([(x2-5, y2+8), (x2+5, y2+8), (x2, y2)], fill=(71, 85, 105))
        elif y1 == y2: # Horizontal
            if x2 > x1:
                draw.polygon([(x2-8, y2-5), (x2-8, y2+5), (x2, y2)], fill=(71, 85, 105))
            else:
                draw.polygon([(x2+8, y2-5), (x2+8, y2+5), (x2, y2)], fill=(71, 85, 105))
                
        if label:
            lx = (x1 + x2) // 2 + 5
            ly = (y1 + y2) // 2 - 10
            draw.text((lx, ly), label, fill=(100, 116, 139), font=text_font)

    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Generated diagram: {os.path.basename(output_path)}")

# ---------------------------------------------------------
# FIGURE 3.1: OVERALL ARCHITECTURE OF THE PROPOSED SYSTEM
# ---------------------------------------------------------
b31 = [
    (350, 80, 200, 45, "STUDENT / USER", ["Browser Web App"], (240, 249, 255), (14, 116, 144)),
    (350, 160, 200, 50, "FRONTEND LAYER", ["React 19 + Vite + TS", "Tailwind CSS"], (245, 243, 255), (109, 40, 217)),
    (350, 250, 200, 50, "BACKEND LAYER", ["FastAPI Python Server", "Uvicorn + JWT Auth"], (240, 253, 244), (21, 128, 61)),
    (50, 340, 800, 130, "APPLICATION SERVICES", [
        "• Resume Analysis Engine       • JD NLP Analysis Engine        • Semantic Matching Engine",
        "• Skill Gap Analysis Engine     • Project Recommendation Engine • Role-Aware Assessment Engine",
        "• Skill Analytics Engine        • Adaptive Roadmap Engine       • Career Readiness Analysis"
    ], (254, 243, 199), (180, 83, 9)),
    (150, 500, 280, 55, "NLP / SEMANTIC LAYER", ["SentenceTransformer (all-MiniLM-L6-v2)", "TF-IDF Vector Cosine Fallback"], (241, 245, 249), (51, 65, 85)),
    (470, 500, 280, 55, "PERSISTENCE LAYER", ["SQLite + SQLAlchemy Database", "JSON Taxonomy Datasets"], (241, 245, 249), (51, 65, 85))
]
a31 = [
    (450, 125, 450, 160, ""),
    (450, 210, 450, 250, "HTTP / REST"),
    (450, 300, 450, 340, ""),
    (290, 470, 290, 500, ""),
    (610, 470, 610, 500, "")
]
create_box_diagram(900, 580, "Figure 3.1: Overall Architecture of the Proposed System", "System Components and Layer Interactions", b31, a31, os.path.join(CH3_DIR, "figure_3_1_overall_architecture.png"))

# ---------------------------------------------------------
# FIGURE 3.2: COMPLETE CAREER COMPASS AI WORKFLOW
# ---------------------------------------------------------
b32 = [
    (50, 80, 160, 45, "1. RESUME UPLOAD", ["Upload PDF Resume"], (241, 245, 249), (51, 65, 85)),
    (250, 80, 160, 45, "2. RESUME PARSING", ["PyMuPDF Text Extract"], (241, 245, 249), (51, 65, 85)),
    (450, 80, 160, 45, "3. RESUME ANALYSIS", ["Skill/Section Extraction"], (241, 245, 249), (51, 65, 85)),
    (650, 80, 160, 45, "4. TARGET JD SELECT", ["Paste or Pick Role JD"], (241, 245, 249), (51, 65, 85)),
    
    (650, 170, 160, 45, "5. JD NLP ANALYSIS", ["Req/Pref Skill Extract"], (241, 245, 249), (51, 65, 85)),
    (450, 170, 160, 45, "6. SEMANTIC MATCH", ["Hybrid Similarity 60/40"], (241, 245, 249), (51, 65, 85)),
    (250, 170, 160, 45, "7. SKILL GAP IDENT", ["Required/Pref Missing"], (241, 245, 249), (51, 65, 85)),
    (50, 170, 160, 45, "8. PROJECT REC", ["Multi-Skill Matrix Cover"], (241, 245, 249), (51, 65, 85)),

    (50, 260, 160, 45, "9. ROLE REC", ["Profile Alignment Rank"], (241, 245, 249), (51, 65, 85)),
    (250, 260, 160, 45, "10. MCQ ASSESSMENT", ["Role-Aware Questions"], (241, 245, 249), (51, 65, 85)),
    (450, 260, 160, 45, "11. SKILL ANALYTICS", ["Longitudinal History"], (241, 245, 249), (51, 65, 85)),
    (650, 260, 160, 45, "12. ADAPTIVE ROADMAP", ["Stage 1/2/3 Milestones"], (241, 245, 249), (51, 65, 85)),

    (350, 350, 160, 45, "13. CAREER READINESS", ["Employability Index"], (240, 253, 244), (21, 128, 61))
]
a32 = [
    (210, 102, 250, 102, ""), (410, 102, 450, 102, ""), (610, 102, 650, 102, ""),
    (730, 125, 730, 170, ""),
    (650, 192, 610, 192, ""), (450, 192, 410, 192, ""), (250, 192, 210, 192, ""),
    (130, 215, 130, 260, ""),
    (210, 282, 250, 282, ""), (410, 282, 450, 282, ""), (610, 282, 650, 282, ""),
    (730, 305, 730, 372, ""), (730, 372, 510, 372, "")
]
create_box_diagram(860, 430, "Figure 3.2: Complete Career Compass AI Workflow", "End-to-End Candidate Processing Flow", b32, a32, os.path.join(CH3_DIR, "figure_3_2_complete_workflow.png"))

# ---------------------------------------------------------
# CHAPTER 5 WORKFLOW DIAGRAMS (5.1 TO 5.12)
# ---------------------------------------------------------
ch5_configs = [
    ("Figure 5.1: User Authentication Workflow", "figure_5_1_user_authentication_workflow.png", [
        ("Register/Login", ["User Credentials Input"]),
        ("Validation", ["FastAPI Email/Pass Check"]),
        ("Password Hash", ["bcrypt Hashing/Verification"]),
        ("JWT Auth", ["Generate Access Token"]),
        ("Session", ["Authenticated User Session"]),
        ("Dashboard", ["Redirect to User Dashboard"])
    ]),
    ("Figure 5.2: Resume Upload and Parsing Workflow", "figure_5_2_resume_upload_and_parsing_workflow.png", [
        ("Resume PDF", ["Candidate File Upload"]),
        ("Validation", ["File Extension & MIME Check"]),
        ("PyMuPDF Extract", ["Stream Text Extraction"]),
        ("Text Cleaning", ["Normalize Whitespace & Symbols"]),
        ("Resume Content", ["Clean Raw Resume Text"]),
        ("Extraction", ["Skill & Section Parsing"])
    ]),
    ("Figure 5.3: Resume Analysis Workflow", "figure_5_3_resume_analysis_workflow.png", [
        ("Parsed Resume", ["Extracted Text Stream"]),
        ("Section Detect", ["Identify Experience/Skills"]),
        ("Skill Extract", ["Match against Skills DB"]),
        ("Quality Analysis", ["Check Contact & Action Verbs"]),
        ("ATS Scorecard", ["7-Component Score Calculation"]),
        ("Dashboard", ["Render ATS & Quality Insights"])
    ]),
    ("Figure 5.4: Job Description Analysis Workflow", "figure_5_4_job_description_analysis_workflow.png", [
        ("Job Description", ["Paste or Select Target Role"]),
        ("Text Process", ["Clean & Normalize Text"]),
        ("Req Extraction", ["Extract Required Skills"]),
        ("Pref Extraction", ["Extract Preferred Skills"]),
        ("Negation Detect", ["Exclude 'Not Required' Terms"]),
        ("JD Profile", ["Structured Target Requirements"])
    ]),
    ("Figure 5.5: Resume-Job Skill Matching Workflow", "figure_5_5_resume_job_skill_matching_workflow.png", [
        ("Resume Skills", ["Extracted Candidate Skills"]),
        ("Job Skills", ["Extracted JD Skills"]),
        ("Normalization", ["Canonical Taxonomy Mapping"]),
        ("Rule Match", ["Exact Keyword Comparison"]),
        ("Semantic Match", ["all-MiniLM-L6-v2 Embeddings"]),
        ("Hybrid Output", ["60% Rule + 40% Semantic Match"])
    ]),
    ("Figure 5.6: Skill Gap Identification Workflow", "figure_5_6_skill_gap_identification_workflow.png", [
        ("Required Skills", ["Target Job Requirements"]),
        ("Comparison", ["Cross-Check Candidate Profile"]),
        ("Match Classify", ["Exact / Related / Missing"]),
        ("Missing Skills", ["Unmatched Required/Preferred"]),
        ("Priority Assign", ["Required Priority > Preferred"]),
        ("Gap Output", ["Critical & Moderate Skill Gaps"])
    ]),
    ("Figure 5.7: Project Recommendation Workflow", "figure_5_7_project_recommendation_workflow.png", [
        ("Missing Skills", ["Identified Candidate Gaps"]),
        ("Project Map", ["Query Capstone Database"]),
        ("Coverage Calc", ["Multi-Skill Matrix Scoring"]),
        ("Project Rank", ["Sort by Missing Skill Fit"]),
        ("Recommended", ["Top Ranked Projects"]),
        ("Target Skills", ["Skills to be Developed"])
    ]),
    ("Figure 5.8: Job Role Recommendation Workflow", "figure_5_8_job_role_recommendation_workflow.png", [
        ("User Profile", ["Detected Candidate Skills"]),
        ("Role DB", ["Target Role Taxonomy Maps"]),
        ("Skill Matching", ["Calculate Skill Coverage"]),
        ("Suitability", ["Profile Alignment Ranking"]),
        ("Recommended", ["Top Suitable Job Roles"]),
        ("Gap Summary", ["Missing Skills per Role"])
    ]),
    ("Figure 5.9: AI Mock Assessment Workflow", "figure_5_9_ai_mock_assessment_workflow.png", [
        ("Context Input", ["Role + Skill Gaps + History"]),
        ("Question Select", ["Role-Aware Question Query"]),
        ("Difficulty Adjust", ["Easy / Medium / Hard Weighting"]),
        ("Mock Test", ["Present MCQ Assessment"]),
        ("Evaluation", ["Evaluate User Answers"]),
        ("Score Output", ["Overall & Skill-wise Scores"])
    ]),
    ("Figure 5.10: Skill Analytics & Progress Tracking Workflow", "figure_5_10_skill_analytics_and_progress_tracking.png", [
        ("Attempts History", ["Sequential Test Scores"]),
        ("Skill Scores", ["Aggregate Skill Performance"]),
        ("Comparison", ["Latest vs Previous Score"]),
        ("Improvement", ["Calculate Net Growth %"]),
        ("Trend Analysis", ["Weak / Developing / Strong"]),
        ("Priority Update", ["Update Candidate Focus Areas"])
    ]),
    ("Figure 5.11: Personalized Roadmap Workflow", "figure_5_11_personalized_roadmap_workflow.png", [
        ("Profile Input", ["Resume + JD + Gaps + Scores"]),
        ("Priority Calc", ["Rank Missing Required Skills"]),
        ("Stage Order", ["Stage 1: High, Stage 2: Med, Stage 3: Low"]),
        ("Project Milestones", ["Attach Capstone Projects"]),
        ("Progress Check", ["Graduation on Strong Status"]),
        ("Updated Roadmap", ["Adaptive Learning Milestones"])
    ]),
    ("Figure 5.12: Career Readiness Indicator Workflow", "figure_5_12_career_readiness_indicator.png", [
        ("Resume Score", ["ATS & Quality Metrics"]),
        ("Skill Coverage", ["Required Skill Match %"]),
        ("Assessment Perf", ["MCQ Skill Mastery Scores"]),
        ("Readiness Calc", ["Weighted Profile Alignment"]),
        ("Role Fit Index", ["Target Role Suitability Index"]),
        ("Readiness Output", ["Career Readiness Dashboard"])
    ])
]

for title, fname, steps in ch5_configs:
    boxes = []
    arrows = []
    x = 40
    y = 80
    w = 115
    h = 45
    for i, (hdr, bdy) in enumerate(steps):
        boxes.append((x, y, w, h, f"{i+1}. {hdr}", bdy, (241, 245, 249), (51, 65, 85)))
        if i < len(steps) - 1:
            arrows.append((x + w, y + 22, x + w + 20, y + 22, ""))
        x += w + 20
        
    create_box_diagram(850, 160, title, "Implementation Workflow Step Sequence", boxes, arrows, os.path.join(CH5_DIR, fname))

print("All Chapter 3 and Chapter 5 technical diagrams generated successfully!")

