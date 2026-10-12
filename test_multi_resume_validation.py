import sys
from pathlib import Path

server_dir = Path(__file__).parent / "server"
if str(server_dir) not in sys.path:
    sys.path.insert(0, str(server_dir))

from server.services.resume_analyzer import compute_ats, analyze_resume_text
from server.services.skill_extractor import extract_skills

resumes = {
    "Backend_Dev": """
        Senior Backend Developer | john@backend.dev | (555) 123-4567 | linkedin.com/in/johnbackend | github.com/johnbackend
        SUMMARY:
        Architect with 5+ years of experience in microservices, REST APIs, and database engineering.
        EDUCATION:
        B.Tech in Computer Science | State University | GPA: 3.8
        EXPERIENCE:
        Lead Backend Engineer | Tech Solutions Inc | 2021 - Present
        - Built scalable microservices using Python, FastAPI, Docker, and PostgreSQL, improving throughput by 45%.
        - Reduced API latency by 35% using Redis caching and SQL query optimization for 500k active users.
        SKILLS:
        Python, FastAPI, SQL, PostgreSQL, Redis, Docker, REST API, Git, Microservices, CI/CD
    """,
    "Fullstack_Dev": """
        Full Stack Developer | jane@fullstack.io | (555) 234-5678 | github.com/janefs
        SUMMARY:
        Fullstack Developer with 3 years building web apps.
        EDUCATION:
        B.S. in Software Engineering | Tech College
        EXPERIENCE:
        Full Stack Engineer | WebWorks | 2022 - Present
        - Developed web apps using React, Node.js, Express, and MongoDB.
        - Designed RESTful APIs and responsive UI components.
        SKILLS:
        JavaScript, TypeScript, React, Node.js, Express, HTML, CSS, SQL, Git
    """,
    "Data_Scientist": """
        Data Scientist | sara@datascience.ai | (555) 345-6789 | linkedin.com/in/sarads
        SUMMARY:
        Data Scientist with 4 years experience in statistical modeling and machine learning.
        EDUCATION:
        M.S. in Data Science | National University
        EXPERIENCE:
        Data Scientist | Analytics Corp | 2021 - Present
        - Built predictive ML models using Python, Pandas, NumPy, Scikit-Learn, and PyTorch, boosting prediction accuracy by 28%.
        - Processed large datasets with SQL and Spark, generating BI dashboards in Tableau.
        SKILLS:
        Python, R, Pandas, NumPy, Machine Learning, Scikit-Learn, PyTorch, SQL, Statistics, Data Analysis
    """,
    "AI_ML_Engineer": """
        AI / ML Engineer | alex@aiml.org | (555) 456-7890 | github.com/alexai
        SUMMARY:
        AI Engineer specializing in Deep Learning and LLM fine-tuning.
        EDUCATION:
        Master of Science in Artificial Intelligence | Institute of Tech
        EXPERIENCE:
        AI Engineer | DeepTech Labs | 3 years
        - Trained Transformer models using PyTorch, TensorFlow, and HuggingFace, scaling inference to 1M daily requests.
        - Deployed ML pipelines on AWS SageMaker with Docker.
        SKILLS:
        Python, PyTorch, TensorFlow, Machine Learning, Deep Learning, Computer Vision, Natural Language Processing, HuggingFace, Docker, AWS
    """,
    "Cloud_DevOps": """
        Cloud & DevOps Engineer | sam@cloudops.com | (555) 567-8901 | linkedin.com/in/samdevops
        SUMMARY:
        DevOps Engineer with 5 years experience in Kubernetes and AWS cloud infrastructure.
        EDUCATION:
        B.E. in Information Technology | City Institute
        EXPERIENCE:
        Senior DevOps Engineer | CloudScale | 2020 - Present
        - Automated CI/CD pipelines using Jenkins and GitHub Actions, cutting deployment time by 60%.
        - Managed Kubernetes clusters and Terraform infrastructure on AWS.
        SKILLS:
        AWS, Docker, Kubernetes, Terraform, Linux, CI/CD, Jenkins, Python, Shell Scripting, Git
    """,
    "Weak_Minimal": """
        Alex Smith
        Contact: alex@mail.com
        Summary: Looking for IT job.
        Education: High School Diploma
        Experience: Helper - assisted with computers.
        Skills: Word, Excel, Basic Computer
    """,
    "Strong_Professional": """
        Principal Systems Architect | victoria@architect.io | (555) 999-8888 | linkedin.com/in/varch | github.com/varch
        SUMMARY:
        Seasoned Principal Engineer with 8+ years designing high-throughput distributed systems.
        EDUCATION:
        M.S. in Computer Science & Engineering | Ivy League University | Honors Graduate
        EXPERIENCE:
        Principal Software Architect | Enterprise Cloud | 2018 - Present
        - Architected cloud platform supporting 10M active users with 99.999% uptime, saving $500k annually.
        - Spearheaded engineering team of 15 across 4 international offices, delivering 20+ production releases.
        - Reduced infrastructure cost by 40% through Kubernetes auto-scaling and AWS serverless migration.
        SKILLS:
        Python, Java, Go, Architecture, Distributed Systems, Kubernetes, Docker, AWS, Microservices, PostgreSQL, Kafka, Redis, CI/CD, System Design
    """
}

# Target JDs
backend_jd = {
    "requiredSkills": ["Python", "FastAPI", "SQL", "Docker", "REST API"],
    "preferredSkills": ["Microservices", "AWS", "Redis", "CI/CD"],
    "structuredExperience": {"minimumYears": 3},
    "structuredEducation": {"recognizedDegrees": ["Bachelor of Science"]}
}

ds_jd = {
    "requiredSkills": ["Python", "Pandas", "NumPy", "Machine Learning", "Statistics"],
    "preferredSkills": ["PyTorch", "SQL", "Scikit-Learn"],
    "structuredExperience": {"minimumYears": 3},
    "structuredEducation": {"recognizedDegrees": ["Master of Science"]}
}

print("=== PART 14 MULTI-RESUME TEST ===")
print("| Resume | JD | Resume Quality | Job Compatibility | Keyword Coverage | Format | Skills | Overall |")
print("|-------|----|----------------|-------------------|------------------|--------|--------|---------|")

for name, text in resumes.items():
    skills = extract_skills(text)
    
    # 1. No JD
    ats_no_jd = compute_ats(text, skills, None)
    rq = ats_no_jd["overallScore"]
    jc = "-"
    kc = ats_no_jd["keywordCoverage"]
    fmt = ats_no_jd["sectionScores"]["format"]
    skl = ats_no_jd["sectionScores"]["skills"]
    ovr = ats_no_jd["overallScore"]
    print(f"| {name} | None | {rq} | {jc} | {kc}% | {fmt} | {skl} | {ovr} |")

    # 2. Matching JD (Backend for Backend, DS for DS, Backend for others)
    jd_match = ds_jd if name in ["Data_Scientist", "AI_ML_Engineer"] else backend_jd
    ats_match = compute_ats(text, skills, jd_match)
    rq = (ats_match["sectionScores"]["format"] * 0.15 + ats_match["sectionScores"]["experience"] * 0.20 + ats_match["sectionScores"]["skills"] * 0.25 + ats_match["sectionScores"]["education"] * 0.15 + ats_match["sectionScores"]["impact"] * 0.10)
    jc = (ats_match["atsScorecard"]["requiredSkillCoverage"]["score"] * 0.40 + ats_match["atsScorecard"]["preferredSkillCoverage"]["score"] * 0.20 + ats_match["atsScorecard"]["experienceAlignment"]["score"] * 0.20 + ats_match["atsScorecard"]["educationAlignment"]["score"] * 0.20)
    print(f"| {name} | Match JD | {round(rq,1)} | {round(jc,1)} | {ats_match['keywordCoverage']}% | {ats_match['sectionScores']['format']} | {ats_match['sectionScores']['skills']} | {ats_match['overallScore']} |")

    # 3. Unrelated JD
    jd_unrelated = ds_jd if name not in ["Data_Scientist", "AI_ML_Engineer"] else backend_jd
    ats_unrel = compute_ats(text, skills, jd_unrelated)
    rq = (ats_unrel["sectionScores"]["format"] * 0.15 + ats_unrel["sectionScores"]["experience"] * 0.20 + ats_unrel["sectionScores"]["skills"] * 0.25 + ats_unrel["sectionScores"]["education"] * 0.15 + ats_unrel["sectionScores"]["impact"] * 0.10)
    jc = (ats_unrel["atsScorecard"]["requiredSkillCoverage"]["score"] * 0.40 + ats_unrel["atsScorecard"]["preferredSkillCoverage"]["score"] * 0.20 + ats_unrel["atsScorecard"]["experienceAlignment"]["score"] * 0.20 + ats_unrel["atsScorecard"]["educationAlignment"]["score"] * 0.20)
    print(f"| {name} | Unrelated JD | {round(rq,1)} | {round(jc,1)} | {ats_unrel['keywordCoverage']}% | {ats_unrel['sectionScores']['format']} | {ats_unrel['sectionScores']['skills']} | {ats_unrel['overallScore']} |")

print("\n=== PART 15 CONTROLLED SENSITIVITY TEST ===")
base_resume = resumes["Backend_Dev"]

# TEST A: Original
sk_a = extract_skills(base_resume)
ats_a = compute_ats(base_resume, sk_a, backend_jd)
print(f"TEST A (Original): Overall = {ats_a['overallScore']}, Skills = {ats_a['sectionScores']['skills']}, Coverage = {ats_a['keywordCoverage']}%")

# TEST B: Remove technical skills
text_b = base_resume.replace("Python, FastAPI, SQL, PostgreSQL, Redis, Docker, REST API, Git, Microservices, CI/CD", "Git")
sk_b = extract_skills(text_b)
ats_b = compute_ats(text_b, sk_b, backend_jd)
print(f"TEST B (Remove Skills): Overall = {ats_b['overallScore']}, Skills = {ats_b['sectionScores']['skills']}, Coverage = {ats_b['keywordCoverage']}% (Expected: Decrease)")

# TEST C: Add relevant skills
text_c = base_resume + "\nAdditional Skills: AWS, Kubernetes, GraphQL, gRPC, Terraform, CI/CD, Unit Testing"
sk_c = extract_skills(text_c)
ats_c = compute_ats(text_c, sk_c, backend_jd)
print(f"TEST C (Add Skills): Overall = {ats_c['overallScore']}, Skills = {ats_c['sectionScores']['skills']}, Coverage = {ats_c['keywordCoverage']}% (Expected: Increase)")

# TEST D: Remove projects/experience
text_d = base_resume.replace("Lead Backend Engineer | Tech Solutions Inc | 2021 - Present\n        - Built scalable microservices using Python, FastAPI, Docker, and PostgreSQL, improving throughput by 45%.\n        - Reduced API latency by 35% using Redis caching and SQL query optimization for 500k active users.", "")
sk_d = extract_skills(text_d)
ats_d = compute_ats(text_d, sk_d, backend_jd)
print(f"TEST D (Remove Exp): Overall = {ats_d['overallScore']}, Exp = {ats_d['sectionScores']['experience']} (Expected: Decrease)")

# TEST E: Add measurable achievements
text_e = base_resume + "\n- Scaled database queries reducing response time by 80% and saving 200 hours per sprint across 1M active users."
sk_e = extract_skills(text_e)
ats_e = compute_ats(text_e, sk_e, backend_jd)
print(f"TEST E (Add Impact): Overall = {ats_e['overallScore']}, Impact = {ats_e['sectionScores']['impact']} (Expected: Increase)")

# TEST F: Remove education
text_f = base_resume.replace("EDUCATION:\n        B.Tech in Computer Science | State University | GPA: 3.8", "")
sk_f = extract_skills(text_f)
ats_f = compute_ats(text_f, sk_f, backend_jd)
print(f"TEST F (Remove Edu): Overall = {ats_f['overallScore']}, Edu = {ats_f['sectionScores']['education']} (Expected: Decrease)")

# TEST G: Unrelated JD
ats_g = compute_ats(base_resume, sk_a, ds_jd)
print(f"TEST G (Unrelated JD): Overall = {ats_g['overallScore']}, Req Coverage = {ats_g['atsScorecard']['requiredSkillCoverage']['score']}% (Expected: Low Match)")

# TEST H: Highly relevant JD
ats_h = compute_ats(base_resume, sk_a, backend_jd)
print(f"TEST H (Relevant JD): Overall = {ats_h['overallScore']}, Req Coverage = {ats_h['atsScorecard']['requiredSkillCoverage']['score']}% (Expected: High Match)")
