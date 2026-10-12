import requests

BASE_URL = "http://127.0.0.1:8000/api"

def run_tests():
    print("=== PHASE 4 BACKEND ASSESSMENT VERIFICATION TEST ===")
    
    # 1. Health check
    res = requests.get(f"{BASE_URL}/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("✔ 1. Health Check PASS")

    # 2. Register & Login User 1
    email_u1 = "phase4_user1@example.com"
    password_u1 = "Password123!"
    
    requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Phase4 User 1",
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

    # 3. Submit Assessment Attempt
    attempt_payload = {
        "role_id": "backend-dev",
        "role_title": "Backend Developer",
        "overall_score": 85,
        "time_taken_seconds": 240,
        "question_count": 10,
        "skill_breakdown": {
            "Python": 90,
            "FastAPI": 80,
            "Docker": 85
        }
    }
    
    submit_res = requests.post(f"{BASE_URL}/assessments", json=attempt_payload, headers=headers_u1)
    assert submit_res.status_code == 200, f"Assessment submission failed: {submit_res.text}"
    submitted = submit_res.json()
    attempt_id = submitted["id"]
    
    assert submitted["role_title"] == "Backend Developer"
    assert submitted["overall_score"] == 85
    assert submitted["time_taken_seconds"] == 240
    assert submitted["skill_breakdown"]["Python"] == 90
    print("✔ 3. Assessment Attempt Submission PASS")

    # 4. List User Assessment Attempts
    list_res = requests.get(f"{BASE_URL}/assessments", headers=headers_u1)
    assert list_res.status_code == 200, f"List assessments failed: {list_res.text}"
    attempts_list = list_res.json()
    assert len(attempts_list) >= 1
    assert attempts_list[0]["id"] == attempt_id
    print("✔ 4. GET User Assessment Attempts PASS")

    # 5. User Data Isolation Test
    email_u2 = "phase4_user2@example.com"
    password_u2 = "Password123!"
    requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Phase4 User 2",
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

    u2_list_res = requests.get(f"{BASE_URL}/assessments", headers=headers_u2)
    assert u2_list_res.status_code == 200, f"User 2 list failed: {u2_list_res.text}"
    u2_attempts = u2_list_res.json()
    assert len(u2_attempts) == 0, "Isolation failure! User 2 sees User 1 attempts"
    print("✔ 5. User Data Isolation PASS")

    print("\nALL PHASE 4 BACKEND TESTS PASSED SUCCESSFULLY! 🎉")

if __name__ == "__main__":
    run_tests()
