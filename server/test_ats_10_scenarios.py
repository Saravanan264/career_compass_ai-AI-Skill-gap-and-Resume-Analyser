import sys
from pathlib import Path

# Add current directory (server) to Python path for IDE linters and runtime resolution
server_dir = Path(__file__).parent
if str(server_dir) not in sys.path:
    sys.path.insert(0, str(server_dir))

from services.resume_analyzer import evaluate_parseability, evaluate_education_alignment, evaluate_experience_alignment, evaluate_impact_evidence, compute_ats
from services.skill_extractor import extract_skills

print("============================================================")
print("     CAREER COMPASS AI — 10 ATS SCENARIOS VALIDATION TEST")
print("============================================================")

resumes = {
    "Strong_Backend": """
        John Doe | Senior Software Engineer
        Email: john.doe@email.com | Phone: (555) 123-4567 | LinkedIn: linkedin.com/in/johndoe | GitHub: github.com/johndoe
        
        SUMMARY:
        Results-driven Senior Backend Engineer with 6+ years of experience designing and deploying scalable microservices, REST APIs, and database architectures.
        
        EDUCATION:
        Bachelor of Science in Computer Science | State University | Graduated 2018
        
        EXPERIENCE:
        Lead Backend Developer | Tech Solutions Inc. | 2021 - Present
        - Engineered microservices architecture using Python, FastAPI, Docker, and PostgreSQL, increasing system throughput by 45%.
        - Reduced API latency by 35% through Redis caching and SQL query optimization.
        - Managed a team of 5 software engineers, delivering 12 production releases on AWS cloud infrastructure.
        - Improved test coverage from 60% to 92%, saving 15 hours of manual QA per sprint.
        
        Software Engineer | Data Systems Corp | 2018 - 2021
        - Built RESTful web services in Java, Spring Boot, and MySQL supporting 500k active users.
        - Deployed Kubernetes clusters and CI/CD pipelines, reducing deployment times by 50%.
        
        SKILLS:
        Python, FastAPI, Java, Spring Boot, PostgreSQL, MySQL, Redis, Docker, Kubernetes, AWS, REST API, Microservices, Git, CI/CD, Unit Testing
    """,
    "Moderate_Software": """
        Jane Smith
        Email: jane@example.com | Phone: 555-987-6543
        
        SUMMARY:
        Software Developer with experience in web applications and database integration.
        
        EDUCATION:
        Bachelor of Technology in Information Technology | City College
        
        EXPERIENCE:
        Software Developer | Web Tech Ltd | 2 years
        - Developed web applications using JavaScript, Node.js, and SQL.
        - Worked with team to build REST APIs and fix bugs.
        - Improved database query performance.
        
        SKILLS:
        JavaScript, Node.js, SQL, REST API, Git, HTML, CSS
    """,
    "Weak_Minimal": """
        Alex Brown
        Contact: alex@mail.com
        
        Summary:
        Looking for a job in IT.
        
        Education:
        High School Diploma
        
        Experience:
        Assistant
        - Helped with computer tasks.
        
        Skills:
        Computer Basics, Word, Excel
    """,
    "Alias_Skills": """
        Chris Taylor | Fullstack Developer
        Email: chris@dev.io | Phone: 555-333-2222 | GitHub: github.com/ctaylor
        
        EDUCATION:
        Bachelor of Science in Software Engineering | Tech Institute
        
        EXPERIENCE:
        Frontend Engineer | WebApps Co | 3 years
        - Built web application interfaces using ReactJS, NodeJS, and RESTful API services.
        - Managed SQL database schemas and written Python 3 scripts for automated testing.
        
        SKILLS:
        ReactJS, NodeJS, RESTful API, Python 3, SQL database
    """,
    "Poor_Format": """
        unformatted text without sections or contact details just listing some words like python sql developer
    """,
    "Quantified_Impact": """
        Sarah Jenkins | Performance Engineer
        Email: sarah@perf.com | Phone: 555-777-8888
        
        EDUCATION:
        Master of Science in Computer Science | Science University
        
        EXPERIENCE:
        Systems Engineer | Cloud Platforms | 4 years
        - Optimized database queries, reducing response times by 65% and saving $120k annually.
        - Increased pipeline throughput by 80% across 50+ microservices.
        - Achieved 99.99% uptime for 2M daily active users.
        - Launched automated CI/CD pipeline, reducing deployment failures by 40%.
        
        SKILLS:
        Python, Docker, Kubernetes, SQL, AWS, CI/CD, Microservices, REST API
    """,
    "Missing_Education": """
        Michael Reed | Self-Taught Backend Engineer
        Email: michael@code.dev | Phone: 555-999-0000 | GitHub: github.com/mreed
        
        SUMMARY:
        Experienced developer with 4 years building APIs.
        
        EXPERIENCE:
        Backend Engineer | Startup X | 4 years
        - Engineered REST APIs using Python, FastAPI, SQL, and Docker.
        
        SKILLS:
        Python, FastAPI, SQL, Docker, REST API, Git
    """
}

# JDs
backend_jd = {
    "requiredSkills": ["Python", "FastAPI", "SQL", "Docker", "REST API"],
    "preferredSkills": ["Microservices", "AWS", "Redis", "CI/CD"],
    "structuredExperience": {"minimumYears": 3},
    "structuredEducation": {"recognizedDegrees": ["Bachelor of Science"]}
}

data_science_jd = {
    "requiredSkills": ["Python", "R", "Pandas", "NumPy", "Machine Learning", "Statistics"],
    "preferredSkills": ["PyTorch", "TensorFlow", "Tableau", "SQL"],
    "structuredExperience": {"minimumYears": 3},
    "structuredEducation": {"recognizedDegrees": ["Master of Science"]}
}

# TEST 1
sk1 = extract_skills(resumes["Strong_Backend"])
ats1 = compute_ats(resumes["Strong_Backend"], sk1, backend_jd)
print(f"TEST 1: Strong Backend + Backend JD -> Score: {ats1['overallScore']}")

# TEST 2
ats2 = compute_ats(resumes["Strong_Backend"], sk1, data_science_jd)
print(f"TEST 2: Strong Backend + Data Science JD -> Score: {ats2['overallScore']}")

# TEST 3
sk3 = extract_skills(resumes["Weak_Minimal"])
ats3 = compute_ats(resumes["Weak_Minimal"], sk3, backend_jd)
print(f"TEST 3: Weak Resume + Backend JD -> Score: {ats3['overallScore']}")

# TEST 4
ats4 = compute_ats(resumes["Strong_Backend"], sk1, None)
print(f"TEST 4: Strong Resume + Standalone / No JD -> Score: {ats4['overallScore']}")

# TEST 5
sk5 = extract_skills(resumes["Moderate_Software"])
ats5 = compute_ats(resumes["Moderate_Software"], sk5, backend_jd)
print(f"TEST 5: Moderate Resume + Backend JD -> Score: {ats5['overallScore']}")

# TEST 6
ats6_a = compute_ats(resumes["Strong_Backend"], sk1, backend_jd)
ats6_b = compute_ats(resumes["Strong_Backend"], sk1, backend_jd)
print(f"TEST 6: Repeatability -> Match: {ats6_a['overallScore'] == ats6_b['overallScore']} ({ats6_a['overallScore']})")

# TEST 7
sk7 = extract_skills(resumes["Alias_Skills"])
ats7 = compute_ats(resumes["Alias_Skills"], sk7, backend_jd)
print(f"TEST 7: Alias Skill Resume + Backend JD -> Score: {ats7['overallScore']}, Skills: {sk7}")

# TEST 8
sk8 = extract_skills(resumes["Poor_Format"])
ats8 = compute_ats(resumes["Poor_Format"], sk8, backend_jd)
print(f"TEST 8: Poor Formatting Resume -> Score: {ats8['overallScore']}, Parseability Score: {ats8['atsScorecard']['parseability']['score']}")

# TEST 9
sk9 = extract_skills(resumes["Quantified_Impact"])
ats9 = compute_ats(resumes["Quantified_Impact"], sk9, backend_jd)
print(f"TEST 9: Quantified Impact Resume -> Score: {ats9['overallScore']}, Impact Score: {ats9['atsScorecard']['impactEvidence']['score']}")

# TEST 10
sk10 = extract_skills(resumes["Missing_Education"])
ats10 = compute_ats(resumes["Missing_Education"], sk10, backend_jd)
print(f"TEST 10: Missing Education Resume -> Score: {ats10['overallScore']}, Edu Score: {ats10['atsScorecard']['educationAlignment']['score']}")
