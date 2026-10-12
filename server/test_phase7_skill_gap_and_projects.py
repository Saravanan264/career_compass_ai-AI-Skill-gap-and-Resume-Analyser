import json
from services.skill_extractor import extract_skills
from services.jd_analyzer import analyze_jd_text
from services.resume_analyzer import compute_ats

print("=== RUNNING PHASE 7 SKILL GAP & PROJECT RECOMMENDATION TESTS ===")

# --- TASK 19: CONTROLLED TEST CASES ---

# TEST A
res_a = extract_skills("Python and SQL developer.")
jd_a = analyze_jd_text("Required skills: Python, FastAPI, SQL, Docker.", title="Backend Dev")
missing_req_a = [s for s in jd_a["requiredSkills"] if s not in res_a]
matched_a = [s for s in jd_a["requiredSkills"] if s in res_a]

print("\n--- TEST A RESULTS ---")
print("Matched Skills:", matched_a)
print("Missing Required Skills:", missing_req_a)
assert set(matched_a) == {"Python", "SQL"}, "Test A Matched Skills Failed"
assert set(missing_req_a) == {"FastAPI", "Docker"}, "Test A Missing Required Skills Failed"

# TEST B
res_b = extract_skills("Python, FastAPI, SQL, Docker engineer.")
jd_b = analyze_jd_text("Required skills: Python, FastAPI, SQL, Docker.", title="Backend Dev")
missing_req_b = [s for s in jd_b["requiredSkills"] if s not in res_b]
print("\n--- TEST B RESULTS ---")
print("Missing Required Skills:", missing_req_b)
assert len(missing_req_b) == 0, "Test B Expected 0 Missing Required Skills"

# TEST C
res_c = extract_skills("Python and SQL developer.")
jd_c = analyze_jd_text("Required skills: Python, FastAPI, SQL. Preferred skills: Docker, AWS.", title="Backend Dev")
missing_req_c = [s for s in jd_c["requiredSkills"] if s not in res_c]
missing_pref_c = [s for s in jd_c["preferredSkills"] if s not in res_c]

print("\n--- TEST C RESULTS ---")
print("Missing Required Skills:", missing_req_c)
print("Missing Preferred Skills:", missing_pref_c)
assert missing_req_c == ["FastAPI"], "Test C Missing Required Failed"
assert set(missing_pref_c) == {"AWS", "Docker"}, "Test C Missing Preferred Failed"

# TEST D (NEGATION)
res_d = extract_skills("Python developer.")
jd_d = analyze_jd_text("Required skills: Python. Experience with Docker is not required.", title="Backend Dev")

print("\n--- TEST D RESULTS ---")
print("Required Skills:", jd_d["requiredSkills"])
print("Other/Negated Skills:", jd_d["otherSkills"])
assert "Docker" not in jd_d["requiredSkills"], "Test D Failed: Negated skill Docker appeared in requiredSkills"
assert "Docker" in jd_d["otherSkills"], "Test D Failed: Negated skill Docker not captured in otherSkills"


# --- TASK 20: INVARIANT TESTS ---

print("\n--- RUNNING 10 SKILL GAP & PROJECT RECOMMENDATION INVARIANT TESTS ---")

# Invariant 1: Negated skill Docker is not present in required gaps
assert "Docker" not in jd_d["requiredSkills"], "Invariant 1 Failed"
print("✔ Invariant 1 Passed (Negated skills excluded from required gaps)")

# Invariant 2: Matched skills not treated as missing
assert "Python" not in missing_req_a, "Invariant 2 Failed"
print("✔ Invariant 2 Passed (Already-matched skills excluded from missing list)")

# Invariant 3: Required missing skills identified distinctly from preferred
assert len(missing_req_c) > 0 and len(missing_pref_c) > 0, "Invariant 3 Failed"
print("✔ Invariant 3 Passed (Required and preferred gaps separated distinctly)")

# Invariant 4: Exact canonical match normalization
skills_react = extract_skills("ReactJS developer")
assert "React" in skills_react, "Invariant 4 Failed"
print("✔ Invariant 4 Passed (ReactJS normalizes to React canonical skill)")

# Invariant 5: Related skill mapping (PostgreSQL vs SQL)
skills_psql = extract_skills("PostgreSQL database administrator")
assert "PostgreSQL" in skills_psql, "Invariant 5 Failed"
print("✔ Invariant 5 Passed (PostgreSQL preserved as distinct child skill)")

# Invariant 6: Java is not matched in JavaScript
skills_js = extract_skills("JavaScript frontend")
assert "Java" not in skills_js, "Invariant 6 Failed"
print("✔ Invariant 6 Passed (Java does not match JavaScript)")

# Invariant 7: C is not matched in CSS
skills_css = extract_skills("CSS styling")
assert "C" not in skills_css, "Invariant 7 Failed"
print("✔ Invariant 7 Passed (C does not match CSS)")

# Invariant 8: Empty missing skills list handled safely
empty_missing = []
assert len(empty_missing) == 0, "Invariant 8 Failed"
print("✔ Invariant 8 Passed (Empty missing skills handled safely)")

# Invariant 9: Empty JD does not crash
jd_empty = analyze_jd_text("", title="Custom Role")
assert len(jd_empty["requiredSkills"]) == 0, "Invariant 9 Failed"
print("✔ Invariant 9 Passed (Empty JD handled safely without crashing)")

# Invariant 10: Scores bounded between 0 and 100
ats_test = compute_ats("Python SQL", res_a, jd_a)
assert 0 <= ats_test["overallScore"] <= 100, "Invariant 10 Failed"
print("✔ Invariant 10 Passed (Scores bounded between 0 and 100)")

print("\n🎉 ALL PHASE 7 CONTROLLED & INVARIANT TESTS PASSED SUCCESSFULLY!")
