import requests
import sys

BASE_URL = "http://localhost:8000/api"

def test_auth_pipeline():
    print("==================================================")
    print("PART A — TESTING BACKEND AUTHENTICATION PIPELINE")
    print("==================================================")

    # 1. Register test user
    email = "authtest@careercompass.ai"
    password = "password123"
    name = "Auth Test User"

    print(f"\n[1] Registering test user ({email})...")
    res = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password, "name": name})
    if res.status_code == 400 and "already registered" in res.text:
        print("  User already registered, proceeding to login.")
    elif res.status_code == 200:
        print("  User registered successfully.")
    else:
        print(f"  Registration error: {res.status_code} {res.text}")

    # 2. Login test user
    print("\n[2] Logging in test user...")
    login_res = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    print(f"  Status: {login_res.status_code}")
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    data = login_res.json()
    token = data["access_token"]
    print(f"  Access Token Received: {token[:20]}...{token[-10:]}")

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Test /api/auth/me
    print("\n[3] Testing GET /api/auth/me with Bearer token...")
    me_res = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"  Status: {me_res.status_code}, User: {me_res.json().get('email')}")
    assert me_res.status_code == 200

    # 4. Test GET /api/job-descriptions
    print("\n[4] Testing GET /api/job-descriptions with Bearer token...")
    jd_res = requests.get(f"{BASE_URL}/job-descriptions", headers=headers)
    print(f"  Status: {jd_res.status_code}")
    assert jd_res.status_code == 200

    # 5. Test GET /api/assessments
    print("\n[5] Testing GET /api/assessments with Bearer token...")
    ass_res = requests.get(f"{BASE_URL}/assessments", headers=headers)
    print(f"  Status: {ass_res.status_code}")
    assert ass_res.status_code == 200

    print("\n==================================================")
    print("✔ PART A AUTHENTICATION PIPELINE VERIFIED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_auth_pipeline()
