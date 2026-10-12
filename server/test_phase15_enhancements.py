import os
import sys
import json

# Ensure server path is in python sys.path
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
if SERVER_DIR not in sys.path:
    sys.path.insert(0, SERVER_DIR)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("=== RUNNING PHASE 15 ENHANCEMENTS TEST SUITE ===")

# 1. Test Authentication Endpoint Connectivity
import time
unique_email = f"phase15_user_{int(time.time())}@careercompass.ai"
register_payload = {
    "name": "Phase15 Test User",
    "email": unique_email,
    "password": "Password123!"
}

resp_reg = client.post("/api/auth/register", json=register_payload)
assert resp_reg.status_code in [200, 201], f"Auth register failed: {resp_reg.status_code} {resp_reg.text}"

resp_login = client.post("/api/auth/login", json={"email": unique_email, "password": "Password123!"})
assert resp_login.status_code == 200, f"Auth login failed: {resp_login.status_code} {resp_login.text}"
token = resp_login.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("✔ Test 1 Passed: Authentication registration & JWT login succeed")

# 2. Test Assessment Creation & Retrieval API
assessment_payload = {
    "role_id": "software-engineer",
    "role_title": "Software Engineer",
    "overall_score": 85,
    "time_taken_seconds": 450,
    "question_count": 30,
    "skill_breakdown": {
        "Docker": 80,
        "Python": 90,
        "Microservices": 70,
        "FastAPI": 100
    }
}

resp_create_assessment = client.post("/api/assessments", json=assessment_payload, headers=headers)
assert resp_create_assessment.status_code == 200, f"Assessment creation failed: {resp_create_assessment.status_code} {resp_create_assessment.text}"
created_data = resp_create_assessment.json()
assert created_data["question_count"] == 30, f"Question count mismatch: {created_data['question_count']}"
assert created_data["overall_score"] == 85, f"Score mismatch: {created_data['overall_score']}"
print("✔ Test 2 Passed: 30-Question Assessment attempt persisted to backend DB")

resp_get_assessments = client.get("/api/assessments", headers=headers)
assert resp_get_assessments.status_code == 200, f"Get assessments failed: {resp_get_assessments.status_code}"
attempts_list = resp_get_assessments.json()
assert len(attempts_list) > 0, "No assessment attempts retrieved"
print("✔ Test 3 Passed: User assessment attempt history retrieved successfully")

# 3. Test Skill-Specific Roadmap API (GET /api/roadmap/skill/{skill_name})
for skill in ["Docker", "Microservices", "AWS", "Python", "React"]:
    resp_skill_roadmap = client.get(f"/api/roadmap/skill/{skill}", headers=headers)
    assert resp_skill_roadmap.status_code == 200, f"Skill roadmap endpoint failed for {skill}: {resp_skill_roadmap.status_code}"
    roadmap_json = resp_skill_roadmap.json()
    assert roadmap_json["skill"].lower() == skill.lower(), f"Skill name mismatch in payload for {skill}"
    assert "stages" in roadmap_json and len(roadmap_json["stages"]) >= 3, f"Invalid stages in {skill} roadmap"
    assert "handsOnProjects" in roadmap_json, f"Missing handsOnProjects in {skill} roadmap"
    assert "assessment" in roadmap_json, f"Missing assessment section in {skill} roadmap"
    assert "reassessment" in roadmap_json, f"Missing reassessment section in {skill} roadmap"

print("✔ Test 4 Passed: GET /api/roadmap/skill/{skill_name} returns structured BASIC->ADVANCED roadmap for all test skills")

# 4. Test Question Dataset Integrity (30 MCQs requirement)
questions_file = os.path.join(SERVER_DIR, "..", "client", "src", "data", "questions.json")
with open(questions_file, "r", encoding="utf-8") as f:
    q_data = json.load(f)

q_list = q_data.get("questions", [])
assert len(q_list) >= 30, f"Question database must contain at least 30 questions, found {len(q_list)}"

unique_ids = set(q["id"] for q in q_list)
assert len(unique_ids) == len(q_list), "Duplicate question IDs detected in dataset"
print(f"✔ Test 5 Passed: Question database validated ({len(q_list)} unique questions available)")

print("=== ALL PHASE 15 ENHANCEMENT TESTS PASSED PERFECTLY ===")
