import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def run_tests():
    print("=== PHASE 3 BACKEND VERIFICATION TEST ===")
    
    # 1. Health Check
    res = requests.get(f"{BASE_URL}/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("✔ 1. Health Check PASS")

    # 2. Register & Login User 1
    email_u1 = "phase3_user1@example.com"
    password_u1 = "Password123!"
    
    reg_res = requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Phase3 User 1",
        "email": email_u1,
        "password": password_u1,
        "confirmPassword": password_u1
    })
    
    login_res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email_u1,
        "password": password_u1
    })
    assert login_res.status_code == 200, f"User 1 login failed: {login_res.text}"
    login_json = login_res.json()
    token_u1 = login_json.get("access_token") or login_json.get("accessToken")
    headers_u1 = {"Authorization": f"Bearer {token_u1}"}
    print("✔ 2. User 1 Registration & Login PASS")

    # 3. Submit Valid JD
    jd_payload = {
        "title": "Senior Backend Engineer",
        "company_name": "Tech Corp",
        "description": """
        We are seeking a Senior Backend Engineer with 3+ years experience.
        Required skills: Must have strong proficiency in Python, FastAPI, PostgreSQL, and Docker.
        Preferred skills: Experience with AWS and Redis is nice to have.
        Education: Bachelor degree in Computer Science or related field required.
        """
    }
    
    create_res = requests.post(f"{BASE_URL}/job-descriptions", json=jd_payload, headers=headers_u1)
    assert create_res.status_code == 200, f"JD creation failed: {create_res.text}"
    jd_data = create_res.json()
    jd_id = jd_data["id"]
    analysis = jd_data["analysis"]
    
    assert jd_data["title"] == "Senior Backend Engineer"
    assert jd_data["company_name"] == "Tech Corp"
    assert "Python" in analysis["requiredSkills"]
    assert "FastAPI" in analysis["requiredSkills"]
    assert "PostgreSQL" in analysis["requiredSkills"]
    assert "Docker" in analysis["requiredSkills"]
    assert "AWS" in analysis["preferredSkills"] or "AWS" in analysis["requiredSkills"]
    assert analysis["experienceRequirements"] is not None
    assert "3+ years" in analysis["experienceRequirements"].lower() or "3" in analysis["experienceRequirements"]
    assert analysis["educationRequirements"] is not None
    assert "bachelor" in analysis["educationRequirements"].lower()
    print("✔ 3. JD Creation & Skill/Exp/Edu Extraction PASS")

    # 4. GET User Job Descriptions List
    list_res = requests.get(f"{BASE_URL}/job-descriptions", headers=headers_u1)
    assert list_res.status_code == 200, f"List JDs failed: {list_res.text}"
    jds = list_res.json()
    assert len(jds) >= 1
    assert jds[0]["id"] == jd_id
    print("✔ 4. GET User Job Descriptions PASS")

    # 5. GET Specific Job Description
    get_res = requests.get(f"{BASE_URL}/job-descriptions/{jd_id}", headers=headers_u1)
    assert get_res.status_code == 200, f"Get JD by ID failed: {get_res.text}"
    assert get_res.json()["id"] == jd_id
    print("✔ 5. GET Specific JD PASS")

    # 6. GET JD Analysis
    analysis_res = requests.get(f"{BASE_URL}/job-descriptions/{jd_id}/analysis", headers=headers_u1)
    assert analysis_res.status_code == 200, f"Get JD Analysis failed: {analysis_res.text}"
    assert "extractedTitle" in analysis_res.json()
    print("✔ 6. GET JD Analysis PASS")

    # 7. User Data Isolation Test (User 2)
    email_u2 = "phase3_user2@example.com"
    password_u2 = "Password123!"
    requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Phase3 User 2",
        "email": email_u2,
        "password": password_u2,
        "confirmPassword": password_u2
    })
    login_u2 = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email_u2,
        "password": password_u2
    })
    login_u2_json = login_u2.json()
    token_u2 = login_u2_json.get("access_token") or login_u2_json.get("accessToken")
    headers_u2 = {"Authorization": f"Bearer {token_u2}"}

    u2_get_res = requests.get(f"{BASE_URL}/job-descriptions/{jd_id}", headers=headers_u2)
    assert u2_get_res.status_code == 404, f"Isolation failure! User 2 accessed User 1 JD: {u2_get_res.status_code}"
    print("✔ 7. User Data Isolation (404 for unauthorized access) PASS")

    # 8. Empty JD Validation Test
    empty_res = requests.post(f"{BASE_URL}/job-descriptions", json={"description": "   "}, headers=headers_u1)
    assert empty_res.status_code == 422 or empty_res.status_code == 400, f"Validation failure: {empty_res.status_code}"
    print("✔ 8. Empty Input Validation PASS")

    print("\nALL PHASE 3 BACKEND TESTS PASSED SUCCESSFULLY! 🎉")

if __name__ == "__main__":
    run_tests()
