import requests
import fitz
import io

BASE_URL = "http://127.0.0.1:8000/api"

def create_sample_pdf():
    doc = fitz.open()
    page = doc.new_page()
    text = """
    Saravanan V
    Email: saravanan@example.com | Phone: +1-555-0199 | LinkedIn: linkedin.com/in/saravanan
    
    Summary:
    Experienced Software Engineer with expertise in Python, Java, React, SQL, and REST APIs.
    
    Education:
    Bachelor of Science in Computer Science, University of Technology
    
    Experience:
    Software Engineer | Tech Corp | 2021 - Present
    - Developed microservices using Python, FastAPI, and Docker.
    - Improved system performance by 35% and reduced latency.
    - Created frontend dashboards using React, TypeScript, and CSS.
    - Managed PostgreSQL database queries and optimized SQL performance.
    
    Skills:
    Python, Java, JavaScript, TypeScript, React, SQL, PostgreSQL, Docker, Git, REST API, Machine Learning, Data Analysis
    """
    page.insert_text((50, 50), text)
    pdf_bytes = doc.write()
    doc.close()
    return pdf_bytes

def run_tests():
    print("--- Starting Phase 2 Backend Verification ---")

    # 1. Health check
    res = requests.get(f"{BASE_URL}/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("[PASS] 1. Health endpoint working")

    # 2. Register user A
    user_a_email = "usera_p2@example.com"
    reg_data = {"name": "User A", "email": user_a_email, "password": "password123"}
    res = requests.post(f"{BASE_URL}/auth/register", json=reg_data)
    if res.status_code != 200:
        print("User A might exist, logging in directly...")
    
    # Login user A
    login_data = {"email": user_a_email, "password": "password123"}
    res = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    assert res.status_code == 200, f"User A login failed: {res.text}"
    token_a = res.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}
    print("[PASS] 2. User A registered & logged in successfully")

    # 3. Register user B
    user_b_email = "userb_p2@example.com"
    reg_b = {"name": "User B", "email": user_b_email, "password": "password123"}
    requests.post(f"{BASE_URL}/auth/register", json=reg_b)
    res = requests.post(f"{BASE_URL}/auth/login", json={"email": user_b_email, "password": "password123"})
    assert res.status_code == 200, f"User B login failed: {res.text}"
    token_b = res.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    print("[PASS] 3. User B registered & logged in successfully")

    # 4. Upload resume PDF for User A
    pdf_bytes = create_sample_pdf()
    files = {"file": ("saravanan_resume.pdf", pdf_bytes, "application/pdf")}
    res = requests.post(f"{BASE_URL}/resumes/upload", headers=headers_a, files=files)
    assert res.status_code == 200, f"Resume upload failed: {res.text}"
    upload_res = res.json()
    resume_id = upload_res["id"]
    print(f"[PASS] 4. Resume uploaded for User A, ID: {resume_id}")
    print(f"      Detected Skills: {upload_res['analysis']['skillsDetected']}")
    print(f"      Overall Score: {upload_res['analysis']['ats']['overallScore']}")

    # 5. Fetch user A resumes
    res = requests.get(f"{BASE_URL}/resumes", headers=headers_a)
    assert res.status_code == 200, f"Get resumes failed: {res.text}"
    resumes_list = res.json()
    assert len(resumes_list) >= 1, "Resumes list empty"
    print(f"[PASS] 5. User A resumes fetched successfully ({len(resumes_list)} items)")

    # 6. Fetch specific resume details & analysis for User A
    res = requests.get(f"{BASE_URL}/resumes/{resume_id}", headers=headers_a)
    assert res.status_code == 200, f"Get resume by id failed: {res.text}"
    resume_detail = res.json()
    assert resume_detail["analysis"] is not None
    print("[PASS] 6. User A fetched specific resume and analysis")

    # 7. Test User Ownership Protection (User B tries accessing User A's resume)
    res = requests.get(f"{BASE_URL}/resumes/{resume_id}", headers=headers_b)
    assert res.status_code == 404, f"Security vulnerability! User B accessed User A resume: {res.status_code}"
    print("[PASS] 7. Ownership check verified: User B cannot access User A's resume (404 returned)")

    # 8. Test uploading invalid non-PDF file
    invalid_file = {"file": ("test.txt", b"plain text", "text/plain")}
    res = requests.post(f"{BASE_URL}/resumes/upload", headers=headers_a, files=invalid_file)
    assert res.status_code == 400, f"Invalid file check failed: {res.status_code}"
    print("[PASS] 8. Non-PDF upload rejected with status 400")

    print("\n--- ALL BACKEND PHASE 2 TESTS PASSED PERFECTLY! ---")

if __name__ == "__main__":
    run_tests()
