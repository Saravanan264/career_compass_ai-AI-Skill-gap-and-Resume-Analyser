import os
import time
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "figures")
CH6_DIR = os.path.join(BASE_DIR, "chapter6")
CH7_DIR = os.path.join(BASE_DIR, "chapter7")

os.makedirs(CH6_DIR, exist_ok=True)
os.makedirs(CH7_DIR, exist_ok=True)

def run():
    print("Starting Playwright browser to capture Chapter 6 & 7 screenshots...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1366, "height": 768})
        page = context.new_page()

        # Step 1: Open app & Login/Register
        try:
            page.goto("http://localhost:5000/login", wait_until="networkidle")
            time.sleep(1)

            # Try to register if login fails or directly login
            email_field = page.query_selector('input[type="email"], input[name="email"]')
            pass_field = page.query_selector('input[type="password"], input[name="password"]')

            if email_field and pass_field:
                email_field.fill("eval_user@compass.ai")
                pass_field.fill("password123")
                
                login_btn = page.query_selector('button[type="submit"]')
                if login_btn:
                    login_btn.click()
                    time.sleep(2)
        except Exception as e:
            print(f"Login navigation note: {e}")

        # Map of Figure Name -> URL Path
        route_map = [
            ("figure_6_1_resume_upload_and_processing_output.png", "/upload"),
            ("figure_6_2_resume_analysis_dashboard.png", "/ats"),
            ("figure_6_3_job_description_analysis_output.png", "/job-analysis"),
            ("figure_6_4_matching_and_missing_skills.png", "/skills"),
            ("figure_6_5_skill_gap_analysis.png", "/skills"),
            ("figure_6_6_project_recommendation_output.png", "/projects"),
            ("figure_6_7_mock_assessment_interface.png", "/assessment"),
            ("figure_6_8_skill_progress_analytics.png", "/analytics"),
            ("figure_6_9_personalized_roadmap.png", "/roadmap"),
            ("figure_6_10_career_readiness_dashboard.png", "/readiness"),
        ]

        for fname, route in route_map:
            out_path = os.path.join(CH6_DIR, fname)
            try:
                page.goto(f"http://localhost:5000{route}", wait_until="networkidle")
                time.sleep(1.5) # Allow dynamic UI charts and metrics to render completely
                page.screenshot(path=out_path, full_page=False)
                print(f"Captured: {fname} (from http://localhost:5000{route})")
            except Exception as e:
                print(f"Failed capturing {fname}: {e}")

        # Chapter 7 Validation Figure
        ch7_path = os.path.join(CH7_DIR, "figure_7_1_frontend_and_backend_validation.png")
        try:
            page.goto("http://localhost:5000/dashboard", wait_until="networkidle")
            time.sleep(1.5)
            page.screenshot(path=ch7_path, full_page=False)
            print(f"Captured: figure_7_1_frontend_and_backend_validation.png (from http://localhost:5000/dashboard)")
        except Exception as e:
            print(f"Failed capturing Chapter 7 figure: {e}")

        browser.close()
    print("Screenshot capture completed!")

if __name__ == "__main__":
    run()
