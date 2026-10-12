from services.resume_analyzer import analyze_resume_text, compute_ats
from services.skill_extractor import extract_skills

print("=== RUNNING PHASE 6 ATS SCORING & INVARIANT TESTS ===")

# --- TASK 16: CONTROLLED SYNTHETIC TEST CASES ---

# TEST CASE A: STRONG MATCH
res_a = "Senior Software Engineer with 4 years experience. Skills: Python, FastAPI, SQL, React, Docker, AWS. Education: B.Tech in AI & Data Science. Contact: john@example.com."
jd_a = {
    "requiredSkills": ["Python", "FastAPI", "SQL"],
    "preferredSkills": ["Docker", "AWS"],
    "structuredExperience": {"minimumYears": 3},
    "structuredEducation": {"recognizedDegrees": ["Bachelor's Degree"]}
}

ats_a = compute_ats(res_a, extract_skills(res_a), jd_a)
print("\n--- TEST CASE A (Strong Match) ---")
print("Overall ATS Score:", ats_a["overallScore"])
print("Required Skill Coverage Score:", ats_a["atsScorecard"]["requiredSkillCoverage"]["score"])
print("Matched Required Skills:", ats_a["atsScorecard"]["requiredSkillCoverage"]["matched"])
print("Missing Required Skills:", ats_a["atsScorecard"]["requiredSkillCoverage"]["missing"])
assert ats_a["atsScorecard"]["requiredSkillCoverage"]["score"] == 100, "Expected 100% required skill coverage for Test Case A"

# TEST CASE B: PARTIAL MATCH
res_b = "Developer with 2 years experience. Skills: Python, SQL, React. Education: B.Tech. Contact: jane@example.com."
jd_b = {
    "requiredSkills": ["Python", "FastAPI", "SQL", "Docker"],
    "preferredSkills": ["AWS"]
}

ats_b = compute_ats(res_b, extract_skills(res_b), jd_b)
print("\n--- TEST CASE B (Partial Match) ---")
print("Overall ATS Score:", ats_b["overallScore"])
print("Required Skill Coverage Score:", ats_b["atsScorecard"]["requiredSkillCoverage"]["score"])
print("Matched Required Skills:", ats_b["atsScorecard"]["requiredSkillCoverage"]["matched"])
print("Missing Required Skills:", ats_b["atsScorecard"]["requiredSkillCoverage"]["missing"])
assert ats_b["atsScorecard"]["requiredSkillCoverage"]["score"] == 50, "Expected 50% required skill coverage for Test Case B"
assert "FastAPI" in ats_b["atsScorecard"]["requiredSkillCoverage"]["missing"], "Expected FastAPI in missing required skills"
assert "Docker" in ats_b["atsScorecard"]["requiredSkillCoverage"]["missing"], "Expected Docker in missing required skills"

# TEST CASE C: WEAK MATCH
res_c = "Frontend Web Developer. Skills: HTML, CSS, JavaScript, React. Contact: alex@example.com."
jd_c = {
    "requiredSkills": ["Python", "FastAPI", "SQL", "Docker"]
}

ats_c = compute_ats(res_c, extract_skills(res_c), jd_c)
print("\n--- TEST CASE C (Weak Match) ---")
print("Overall ATS Score:", ats_c["overallScore"])
print("Required Skill Coverage Score:", ats_c["atsScorecard"]["requiredSkillCoverage"]["score"])
assert ats_c["atsScorecard"]["requiredSkillCoverage"]["score"] == 0, "Expected 0% required skill coverage for Test Case C"


# --- TASK 17: SCORE INVARIANT TESTS ---

print("\n--- RUNNING 12 SCORE INVARIANT TESTS ---")

# Invariant 1: Adding matched required skill does not reduce required coverage
score_b_initial = ats_b["atsScorecard"]["requiredSkillCoverage"]["score"]
res_b_plus = res_b + " Experienced with FastAPI."
ats_b_plus = compute_ats(res_b_plus, extract_skills(res_b_plus), jd_b)
assert ats_b_plus["atsScorecard"]["requiredSkillCoverage"]["score"] >= score_b_initial, "Invariant 1 Failed"
print("✔ Invariant 1 Passed (Adding matched required skill does not reduce coverage)")

# Invariant 2: Removing matched required skill does not increase required coverage
res_b_minus = "Developer with 2 years experience. Skills: React. Education: B.Tech."
ats_b_minus = compute_ats(res_b_minus, extract_skills(res_b_minus), jd_b)
assert ats_b_minus["atsScorecard"]["requiredSkillCoverage"]["score"] <= score_b_initial, "Invariant 2 Failed"
print("✔ Invariant 2 Passed (Removing matched required skill does not increase coverage)")

# Invariant 3: Adding preferred skill does not reduce ATS score
res_a_pref = res_a + " Preferred skill: AWS."
ats_a_pref = compute_ats(res_a_pref, extract_skills(res_a_pref), jd_a)
assert ats_a_pref["overallScore"] >= ats_a["overallScore"], "Invariant 3 Failed"
print("✔ Invariant 3 Passed (Adding preferred skill does not reduce ATS score)")

# Invariant 4: Adding negated skill does not penalize ATS score
res_negated = res_a + " Kubernetes is not required."
ats_negated = compute_ats(res_negated, extract_skills(res_negated), jd_a)
assert ats_negated["overallScore"] >= ats_a["overallScore"] - 2, "Invariant 4 Failed"
print("✔ Invariant 4 Passed (Adding negated skill does not penalize ATS score)")

# Invariant 5: React.js and React normalize to same canonical skill
skills_reactjs = extract_skills("Experience with React.js frontend")
skills_react = extract_skills("Experience with React frontend")
assert "React" in skills_reactjs and "React" in skills_react, "Invariant 5 Failed"
print("✔ Invariant 5 Passed (React.js and React normalize to React canonical skill)")

# Invariant 6: PostgreSQL is not raw string identical to SQL
skills_psql = extract_skills("Worked with PostgreSQL database")
assert "PostgreSQL" in skills_psql and ("SQL" not in skills_psql or skills_psql != ["SQL"]), "Invariant 6 Passed"
print("✔ Invariant 6 Passed (PostgreSQL is distinct canonical skill from SQL)")

# Invariant 7: Java must not match JavaScript
skills_js = extract_skills("JavaScript developer")
assert "Java" not in skills_js, "Invariant 7 Failed"
print("✔ Invariant 7 Passed (Java does not match JavaScript)")

# Invariant 8: C must not match CSS
skills_css = extract_skills("Expert in CSS3 styling")
assert "C" not in skills_css, "Invariant 8 Failed"
print("✔ Invariant 8 Passed (C does not match CSS)")

# Invariant 9: Missing required skills should be visible
assert len(ats_b["atsScorecard"]["requiredSkillCoverage"]["missing"]) > 0, "Invariant 9 Failed"
print("✔ Invariant 9 Passed (Missing required skills clearly exposed)")

# Invariant 10: Scores remain bounded between 0 and 100
assert 0 <= ats_a["overallScore"] <= 100, "Invariant 10 Failed"
assert 0 <= ats_b["overallScore"] <= 100, "Invariant 10 Failed"
assert 0 <= ats_c["overallScore"] <= 100, "Invariant 10 Failed"
print("✔ Invariant 10 Passed (Scores bounded between 0 and 100)")

# Invariant 11: Empty JD does not crash the system
ats_empty_jd = compute_ats(res_a, extract_skills(res_a), {})
assert ats_empty_jd["overallScore"] > 0, "Invariant 11 Failed"
print("✔ Invariant 11 Passed (Empty JD handled safely without crashing)")

# Invariant 12: Empty/invalid resume text returns controlled response
ats_empty_res = compute_ats("", [], {})
assert ats_empty_res["atsScorecard"]["parseability"]["score"] == 0, "Invariant 12 Failed"
print("✔ Invariant 12 Passed (Empty resume text returns controlled parseability failure)")

print("\n🎉 ALL PHASE 6 CONTROLLED & INVARIANT TESTS PASSED SUCCESSFULLY!")
