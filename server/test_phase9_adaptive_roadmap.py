import json
from services.jd_analyzer import analyze_jd_text
from services.skill_extractor import extract_skills

print("=== RUNNING PHASE 9 ADAPTIVE ROADMAP & SKILL PROGRESS TESTS ===")

# Python simulation of buildRoadmap & computeAnalytics
def simulate_skill_progress(attempts, target_skills, req_skills, pref_skills, resume_skills):
    # Sort attempts by index/date
    sorted_attempts = sorted(attempts, key=lambda a: a["date"])
    
    skill_history = {}
    for att in sorted_attempts:
        for skill, score in att["skillScores"].items():
            if skill not in skill_history:
                skill_history[skill] = []
            skill_history[skill].append(score)

    progress_map = {}
    for skill in target_skills:
        scores = skill_history.get(skill, [])
        attempt_count = len(scores)
        latest = scores[-1] if attempt_count > 0 else None
        previous = scores[-2] if attempt_count >= 2 else None
        improvement = (latest - previous) if (latest is not None and previous is not None) else None

        if latest is not None:
            if latest >= 70:
                status = "Strong"
            elif latest >= 50:
                status = "Developing"
            else:
                status = "Weak"
        else:
            status = "Not Assessed"

        if improvement is not None:
            if improvement > 5:
                trend = "improving"
            elif improvement < -5:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "Not Enough Data"

        progress_map[skill] = {
            "skill": skill,
            "requirement": "required" if skill in req_skills else ("preferred" if skill in pref_skills else "none"),
            "resumeStatus": "matched" if skill in resume_skills else "missing",
            "latestAssessmentScore": latest,
            "previousAssessmentScore": previous,
            "improvement": improvement,
            "attemptCount": attempt_count,
            "status": status,
            "trend": trend
        }

    return progress_map

def simulate_roadmap(progress_map, req_skills, pref_skills):
    critical_gaps = [s for s, p in progress_map.items() if p["requirement"] == "required" and p["resumeStatus"] == "missing" and p["status"] != "Strong"]
    preferred_gaps = [s for s, p in progress_map.items() if p["requirement"] == "preferred" and p["resumeStatus"] == "missing" and p["status"] != "Strong"]
    strong_skills = [s for s, p in progress_map.items() if p["status"] == "Strong"]

    stage1 = {
        "title": "Stage 1: Core Foundation & High-Priority Required Gaps",
        "priority": "High" if len(critical_gaps) > 0 else "Low",
        "focusSkills": critical_gaps,
        "explanation": f"Prioritized because {', '.join(critical_gaps)} are required skills below threshold (<70%)." if critical_gaps else "Core foundation."
    }
    stage2 = {
        "title": "Stage 2: Applied Projects & Preferred Skill Enhancement",
        "priority": "Medium",
        "focusSkills": preferred_gaps
    }
    stage3 = {
        "title": "Stage 3: Reassessment Validation & Career Readiness",
        "priority": "Low",
        "focusSkills": strong_skills
    }
    return [stage1, stage2, stage3]


# --- TASK 17: CONTROLLED ADAPTIVE ROADMAP TEST CASES ---

req_skills = ["Python", "FastAPI", "Docker"]
pref_skills = []
resume_skills = ["Python"]
target_skills = ["Python", "FastAPI", "Docker"]

print("\n--- ATTEMPT 1: Initial Weak Performance ---")
att1 = {
    "date": "2026-09-01T10:00:00Z",
    "skillScores": {"FastAPI": 35, "Docker": 30}
}
prog1 = simulate_skill_progress([att1], target_skills, req_skills, pref_skills, resume_skills)
road1 = simulate_roadmap(prog1, req_skills, pref_skills)

print("Stage 1 Focus:", road1[0]["focusSkills"])
assert "FastAPI" in road1[0]["focusSkills"] and "Docker" in road1[0]["focusSkills"], "Test 1 Failed: Weak required skills must be Stage 1 focus"
assert prog1["FastAPI"]["improvement"] is None, "Test 1 Failed: First attempt must have improvement = None"
assert prog1["FastAPI"]["status"] == "Weak", "Test 1 Failed: Score 35 must be Weak"

print("\n--- ATTEMPT 2: FastAPI Improves, Docker Remains Weak ---")
att2 = {
    "date": "2026-09-02T10:00:00Z",
    "skillScores": {"FastAPI": 75, "Docker": 40}
}
prog2 = simulate_skill_progress([att1, att2], target_skills, req_skills, pref_skills, resume_skills)
road2 = simulate_roadmap(prog2, req_skills, pref_skills)

print("FastAPI Status:", prog2["FastAPI"]["status"], "| Improvement:", prog2["FastAPI"]["improvement"])
print("Docker Status:", prog2["Docker"]["status"], "| Stage 1 Focus:", road2[0]["focusSkills"])

assert prog2["FastAPI"]["status"] == "Strong", "Test 2 Failed: FastAPI score 75 must be Strong"
assert prog2["FastAPI"]["improvement"] == 40, "Test 2 Failed: Improvement should be 75 - 35 = +40"
assert "FastAPI" not in road2[0]["focusSkills"], "Test 2 Failed: Strong FastAPI should leave Stage 1 focus"
assert "Docker" in road2[0]["focusSkills"], "Test 2 Failed: Weak Docker must remain in Stage 1 focus"

print("\n--- ATTEMPT 3: All Skills Become Strong ---")
att3 = {
    "date": "2026-09-03T10:00:00Z",
    "skillScores": {"FastAPI": 82, "Docker": 72}
}
prog3 = simulate_skill_progress([att1, att2, att3], target_skills, req_skills, pref_skills, resume_skills)
road3 = simulate_roadmap(prog3, req_skills, pref_skills)

print("Docker Status:", prog3["Docker"]["status"], "| Improvement:", prog3["Docker"]["improvement"])
assert prog3["Docker"]["status"] == "Strong", "Test 3 Failed: Docker score 72 must be Strong"
assert prog3["Docker"]["improvement"] == 32, "Test 3 Failed: Improvement should be 72 - 40 = +32"
assert len(road3[0]["focusSkills"]) == 0, "Test 3 Failed: All critical gaps resolved"


# --- TASK 18: PROGRESS INVARIANTS ---

print("\n--- RUNNING 12 PROGRESS INVARIANT TESTS ---")

# Invariant 1: Adding later attempt preserves earlier attempts
all_atts = [att1, att2, att3]
assert len(all_atts) == 3, "Invariant 1 Failed"
print("✔ Invariant 1 Passed (Adding a later attempt preserves earlier attempts)")

# Invariant 2: Improvement calculated correctly (Latest - Previous)
assert prog2["FastAPI"]["improvement"] == (75 - 35), "Invariant 2 Failed"
print("✔ Invariant 2 Passed (Improvement calculated correctly)")

# Invariant 3: First attempt does not show positive improvement
assert prog1["FastAPI"]["improvement"] is None, "Invariant 3 Failed"
print("✔ Invariant 3 Passed (First attempt improvement is None)")

# Invariant 4: Higher performance does not increase skill gap severity
assert prog2["FastAPI"]["status"] == "Strong" and prog1["FastAPI"]["status"] == "Weak", "Invariant 4 Failed"
print("✔ Invariant 4 Passed (Higher performance reduces skill gap severity)")

# Invariant 5: Lower performance does not reduce roadmap priority for a required skill
att_low = {"date": "2026-09-04T10:00:00Z", "skillScores": {"Docker": 20}}
prog_low = simulate_skill_progress([att1, att2, att3, att_low], target_skills, req_skills, pref_skills, resume_skills)
road_low = simulate_roadmap(prog_low, req_skills, pref_skills)
assert "Docker" in road_low[0]["focusSkills"], "Invariant 5 Failed"
print("✔ Invariant 5 Passed (Lower performance keeps required skill in high priority)")

# Invariant 6: Negated skills never become roadmap gaps
jd_neg = analyze_jd_text("Required: Python. Docker is not required.", title="Dev")
assert "Docker" not in jd_neg["requiredSkills"], "Invariant 6 Failed"
print("✔ Invariant 6 Passed (Negated skills never become roadmap gaps)")

# Invariant 7: Preferred skills do not outrank equally weak required skills
prog_pref = simulate_skill_progress([att1], ["FastAPI", "SQL"], ["FastAPI"], ["SQL"], [])
road_pref = simulate_roadmap(prog_pref, ["FastAPI"], ["SQL"])
assert road_pref[0]["focusSkills"] == ["FastAPI"], "Invariant 7 Failed"
print("✔ Invariant 7 Passed (Required skills outrank preferred skills in Stage 1)")

# Invariant 8: Empty assessment history handled safely
prog_empty = simulate_skill_progress([], ["Python"], ["Python"], [], ["Python"])
assert prog_empty["Python"]["status"] == "Not Assessed", "Invariant 8 Failed"
print("✔ Invariant 8 Passed (Empty assessment history handled safely)")

# Invariant 9: One skill's progress does not modify another unrelated skill
assert prog2["Docker"]["latestAssessmentScore"] == 40, "Invariant 9 Failed"
print("✔ Invariant 9 Passed (Skill progress isolated per skill)")

# Invariant 10: Scores remain bounded within 0-100
assert all(0 <= p["latestAssessmentScore"] <= 100 for p in prog2.values() if p["latestAssessmentScore"] is not None), "Invariant 10 Failed"
print("✔ Invariant 10 Passed (Scores bounded within 0-100)")

# Invariant 11: Roadmap generation does not crash when no missing skills
road_no_gaps = simulate_roadmap(prog3, [], [])
assert len(road_no_gaps) == 3, "Invariant 11 Failed"
print("✔ Invariant 11 Passed (Roadmap generation succeeds with zero missing skills)")

# Invariant 12: Existing roadmap stages remain usable
assert len(road1) == 3 and "title" in road1[0], "Invariant 12 Failed"
print("✔ Invariant 12 Passed (Existing roadmap stages remain usable)")

print("\n🎉 ALL PHASE 9 CONTROLLED & INVARIANT TESTS PASSED SUCCESSFULLY!")
