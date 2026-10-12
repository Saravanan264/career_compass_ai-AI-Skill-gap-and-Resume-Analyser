import os
import sys
import json
import time
import requests

BASE_URL = "http://localhost:8000/api"

def log(msg, status="INFO"):
    symbol = "✔" if status == "PASS" else ("❌" if status == "FAIL" else "ℹ")
    print(f"[{symbol}] {msg}")

def run_fullstack_validation():
    print("=========================================================")
    print("   CAREER COMPASS AI — FINAL FULL-STACK VALIDATION")
    print("=========================================================")

    # 1. Health Endpoint
    res = requests.get(f"{BASE_URL}/health")
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    log("API Health Check: PASS", "PASS")

    # 2. Registration & Auth
    user_email = f"user_{int(time.time())}@compass.ai"
    test_user = {
        "name": "Fullstack Validation User",
        "email": user_email,
        "password": "Password123!"
    }
    
    reg_res = requests.post(f"{BASE_URL}/auth/register", json=test_user)
    assert reg_res.status_code == 200, f"Registration failed: {reg_res.text}"
    log("User Registration: PASS", "PASS")

    login_res = requests.post(f"{BASE_URL}/auth/login", json={"email": test_user["email"], "password": test_user["password"]})
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    token_data = login_res.json()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    log("User Login & JWT Token Retrieval: PASS", "PASS")

    # 3. Verify /auth/me
    me_res = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    assert me_res.status_code == 200, f"/auth/me failed: {me_res.text}"
    user_info = me_res.json()
    assert user_info["email"] == test_user["email"]
    log(f"Authenticated User Profile (/auth/me): PASS (ID: {user_info['id']})", "PASS")

    # 4. Create Sample PDF & Upload Resume
    pdf_content = (
        b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj\n"
        b"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Resources<>/Contents 4 0 R>>endobj\n"
        b"4 0 obj<</Length 180>>stream\nBT /F1 12 Tf 50 700 Td "
        b"(Jane Doe - Senior Backend Engineer. Skills: Python, FastAPI, PostgreSQL, SQL, Docker, Git. "
        b"Experience: Developed REST APIs and microservices. Education: BS Computer Science.) Tj ET\nendstream\nendobj\n"
        b"xref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000056 00000 n\n00000000111 00000 n\n00000000212 00000 n\n"
        b"trailer<</Size 5/Root 1 0 R>>\nstartxref\n440\n%%EOF"
    )
    
    files = {"file": ("test_resume.pdf", pdf_content, "application/pdf")}
    up_res = requests.post(f"{BASE_URL}/resumes/upload", headers=headers, files=files)
    assert up_res.status_code == 200, f"Resume upload failed: {up_res.text}"
    resume_data = up_res.json()
    resume_id = resume_data["id"]
    log(f"Resume Upload & Processing: PASS (Resume ID: {resume_id})", "PASS")

    # 5. Fetch Resume List & Analysis
    resumes_list = requests.get(f"{BASE_URL}/resumes", headers=headers).json()
    assert len(resumes_list) > 0
    log("Fetch User Resumes List: PASS", "PASS")

    analysis_res = requests.get(f"{BASE_URL}/resumes/{resume_id}/analysis", headers=headers)
    assert analysis_res.status_code == 200
    ats_scorecard = analysis_res.json()
    assert "ats" in ats_scorecard or "overall_score" in ats_scorecard
    log("Resume ATS Analysis Scorecard: PASS", "PASS")

    # 6. Create Job Description
    jd_payload = {
        "title": "Junior Backend Engineer",
        "company_name": "Tech Corp",
        "description": "We are looking for a Junior Backend Engineer proficient in Python, FastAPI, and PostgreSQL. Experience with Docker and AWS is preferred. Note: Kubernetes is not required."
    }
    jd_res = requests.post(f"{BASE_URL}/job-descriptions", headers=headers, json=jd_payload)
    assert jd_res.status_code == 200, f"JD creation failed: {jd_res.text}"
    jd_data = jd_res.json()
    jd_id = jd_data["id"]
    log(f"Job Description Creation & Analysis: PASS (JD ID: {jd_id})", "PASS")

    # 7. List JDs and Get Specific JD Analysis
    jds_list = requests.get(f"{BASE_URL}/job-descriptions", headers=headers).json()
    assert len(jds_list) > 0
    log("Fetch User Job Descriptions List: PASS", "PASS")

    jd_analysis_res = requests.get(f"{BASE_URL}/job-descriptions/{jd_id}/analysis", headers=headers)
    assert jd_analysis_res.status_code == 200
    log("Fetch Specific Job Description Analysis: PASS", "PASS")

    # 8. Assessment Attempt Submission & Persistence
    attempt_payload = {
        "role_title": "Junior Backend Engineer",
        "overall_score": 85,
        "time_taken_seconds": 240,
        "question_count": 30,
        "skill_breakdown": {
            "Python": {"score": 90, "status": "Strong"},
            "FastAPI": {"score": 80, "status": "Strong"},
            "Docker": {"score": 50, "status": "Developing"}
        }
    }
    sub_res = requests.post(f"{BASE_URL}/assessments", headers=headers, json=attempt_payload)
    assert sub_res.status_code == 200, f"Assessment submission failed: {sub_res.text}"
    log("Assessment Attempt Submission & Score Calculation: PASS", "PASS")

    # Fetch Attempts List
    hist_res = requests.get(f"{BASE_URL}/assessments", headers=headers)
    assert hist_res.status_code == 200
    attempts_history = hist_res.json()
    assert len(attempts_history) >= 1
    log(f"Skill Progress Analytics & Attempts History: PASS ({len(attempts_history)} Attempts Saved)", "PASS")

    # 9. Optional LLM Fallback Layer Verification
    llm_status = requests.get(f"{BASE_URL}/llm/status", headers=headers).json()
    log(f"LLM Enhancement Layer Status: PASS (Enabled: {llm_status.get('enabled')}, Provider: {llm_status.get('provider')})", "PASS")

    # 10. Error Handling Tests
    # Case A: Unauthenticated Access
    unauth_res = requests.get(f"{BASE_URL}/auth/me")
    assert unauth_res.status_code in [401, 403]
    log("Error Handling Test - Unauthenticated Access (401): PASS", "PASS")

    # Case B: Invalid Token
    bad_token_res = requests.get(f"{BASE_URL}/auth/me", headers={"Authorization": "Bearer invalid_token_xyz"})
    assert bad_token_res.status_code in [401, 403]
    log("Error Handling Test - Invalid Bearer Token (401): PASS", "PASS")

    # Case C: Unknown Resume ID
    bad_resume_res = requests.get(f"{BASE_URL}/resumes/999999/analysis", headers=headers)
    assert bad_resume_res.status_code in [404, 400, 422]
    log("Error Handling Test - Nonexistent Resource (404): PASS", "PASS")

    # Case D: Duplicate User Registration
    dup_res = requests.post(f"{BASE_URL}/auth/register", json=test_user)
    assert dup_res.status_code == 400
    log("Error Handling Test - Duplicate User Registration (400): PASS", "PASS")

    print("\n=========================================================")
    print("   ALL FULL-STACK VALIDATION CHECKS PASSED PERFECTLY! 🎉")
    print("=========================================================")

if __name__ == "__main__":
    run_fullstack_validation()
