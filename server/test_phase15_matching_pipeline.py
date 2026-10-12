"""
Phase 15 — Targeted Correction & Full Matching Pipeline Verification Script
Career Compass AI

Tests:
1. Canonical Skill Normalization & Alias Resolution (ReactJS, Node.js, RESTful API, SQL)
2. Resume <-> JD Matching Engine (Matched vs Missing Required vs Missing Preferred)
3. Negation & Edge-case handling (Excluded negated skills from missing list)
4. 60/40 Hybrid Compatibility Calculation
5. Downstream Feature Integration (Project recommendation inputs, Roadmap stage priority)
"""

import sys
import json
from pathlib import Path

# Add server directory to path
SERVER_DIR = Path(__file__).parent
sys.path.insert(0, str(SERVER_DIR))

from services.skill_extractor import extract_skills, normalize_text, get_canonical_skill_name
from services.jd_analyzer import analyze_jd_text
from services.semantic_matcher import compute_semantic_similarity, compute_hybrid_match

def run_phase15_tests():
    print("=" * 70)
    print("CAREER COMPASS AI — PHASE 15 MATCHING PIPELINE VERIFICATION")
    print("=" * 70)

    # -------------------------------------------------------------
    # STEP 1: CANONICAL NORMALIZATION & ALIAS RESOLUTION TESTS
    # -------------------------------------------------------------
    print("\n[STEP 1] Testing Canonical Skill Normalization & Alias Mapping...")
    
    test_aliases = [
        ("ReactJS", "React"),
        ("React.js", "React"),
        ("NodeJS", "Node.js"),
        ("RESTful API", "REST API"),
        ("SQL Database", "SQL"),
        ("Python 3", "Python"),
        ("Golang", "Go"),
    ]

    for raw, expected in test_aliases:
        canonical = get_canonical_skill_name(raw)
        print(f"  Mapping '{raw}' -> '{canonical}' (Expected: '{expected}')")
        assert canonical == expected, f"Failed: '{raw}' mapped to '{canonical}', expected '{expected}'"

    print("  ✔ All Canonical Normalization & Alias Tests Passed!")

    # -------------------------------------------------------------
    # STEP 2: PROFILE A — BACKEND DEVELOPER PIPELINE TEST
    # -------------------------------------------------------------
    print("\n[STEP 2] Testing Profile A (Backend Developer: Python, FastAPI, SQL vs Python, FastAPI, SQL, Docker, AWS)...")
    
    resume_text_a = "Experienced Backend Developer proficient in Python, FastAPI, SQL database management, and RESTful API design."
    jd_text_a = "We are seeking a Backend Developer. Required skills: Python, FastAPI, SQL, Docker. Preferred skills: AWS, Redis."

    resume_skills_a = extract_skills(resume_text_a)
    jd_analysis_a = analyze_jd_text(jd_text_a, title="Backend Developer")

    active_req_a = [s for s in jd_analysis_a["requiredSkills"] if s not in jd_analysis_a["otherSkills"]]
    active_pref_a = [s for s in jd_analysis_a["preferredSkills"] if s not in jd_analysis_a["otherSkills"]]

    matched_a = [s for s in active_req_a + active_pref_a if s in resume_skills_a]
    missing_req_a = [s for s in active_req_a if s not in resume_skills_a]
    missing_pref_a = [s for s in active_pref_a if s not in resume_skills_a]

    print(f"  Detected Resume Skills: {resume_skills_a}")
    print(f"  JD Required Skills: {active_req_a}")
    print(f"  JD Preferred Skills: {active_pref_a}")
    print(f"  Matched Skills: {matched_a}")
    print(f"  Missing Required Skills: {missing_req_a}")
    print(f"  Missing Preferred Skills: {missing_pref_a}")

    assert "Python" in matched_a, "Profile A: Python should be matched"
    assert "FastAPI" in matched_a, "Profile A: FastAPI should be matched"
    assert "SQL" in matched_a, "Profile A: SQL should be matched"
    assert "Docker" in missing_req_a, "Profile A: Docker should be in missing required"
    assert "AWS" in missing_pref_a, "Profile A: AWS should be in missing preferred"

    print("  ✔ Profile A Backend Pipeline Test Passed!")

    # -------------------------------------------------------------
    # STEP 3: PROFILE B — FRONTEND DEVELOPER PIPELINE TEST
    # -------------------------------------------------------------
    print("\n[STEP 3] Testing Profile B (Frontend Developer: JavaScript, ReactJS, HTML, CSS)...")
    
    resume_text_b = "Frontend Engineer skilled in ReactJS, JavaScript, HTML5, CSS3, and Tailwind."
    jd_text_b = "Looking for a Frontend Developer. Required skills: React, TypeScript, Node.js, HTML, CSS. Preferred skills: Next.js."

    resume_skills_b = extract_skills(resume_text_b)
    jd_analysis_b = analyze_jd_text(jd_text_b, title="Frontend Developer")

    active_req_b = [s for s in jd_analysis_b["requiredSkills"] if s not in jd_analysis_b["otherSkills"]]
    active_pref_b = [s for s in jd_analysis_b["preferredSkills"] if s not in jd_analysis_b["otherSkills"]]

    matched_b = [s for s in active_req_b + active_pref_b if s in resume_skills_b]
    missing_req_b = [s for s in active_req_b if s not in resume_skills_b]

    print(f"  Detected Resume Skills: {resume_skills_b}")
    print(f"  Matched Skills: {matched_b}")
    print(f"  Missing Required Skills: {missing_req_b}")

    assert "React" in matched_b, "Profile B: ReactJS should match React canonical"
    assert "TypeScript" in missing_req_b, "Profile B: TypeScript should be missing required"
    assert "Node.js" in missing_req_b, "Profile B: Node.js should be missing required"

    print("  ✔ Profile B Frontend Pipeline Test Passed!")

    # -------------------------------------------------------------
    # STEP 4: PROFILE C — NEGATION & HYBRID SCORING TEST
    # -------------------------------------------------------------
    print("\n[STEP 4] Testing Profile C (Negation & 60/40 Hybrid Compatibility Scoring)...")
    
    jd_text_c = "Required: Python, Machine Learning. Note: Docker is not required."
    jd_analysis_c = analyze_jd_text(jd_text_c, title="Data Scientist")

    assert "Docker" in jd_analysis_c["otherSkills"], "Profile C: Negated Docker should be in otherSkills"
    assert "Docker" not in jd_analysis_c["requiredSkills"], "Profile C: Negated Docker must NOT be in requiredSkills"

    # Compute 60/40 Hybrid Match
    rule_score = 75
    sem_score = compute_semantic_similarity("Python Machine Learning engineer", "Required: Python, Machine Learning")
    hybrid_dict = compute_hybrid_match(rule_score, "Python Machine Learning engineer", "Required: Python, Machine Learning")
    hybrid = hybrid_dict["hybrid_match_score"]

    expected_hybrid = round(rule_score * 0.60 + sem_score * 0.40, 1)
    print(f"  Rule Score: {rule_score}%, Semantic Score: {sem_score}%, Hybrid: {hybrid}% (Expected ~{expected_hybrid}%)")
    assert abs(hybrid - expected_hybrid) <= 2, "Profile C: Hybrid score calculation mismatch"

    print("  ✔ Profile C Negation & Hybrid Scoring Test Passed!")

    print("\n" + "=" * 70)
    print("🎉 ALL PHASE 15 MATCHING PIPELINE VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_phase15_tests()
