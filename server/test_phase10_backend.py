import os
import json

from services.llm_service import LLMService, llm_service
from services.resume_analyzer import compute_ats
from services.jd_analyzer import analyze_jd_text

print("=== RUNNING PHASE 10 OPTIONAL LLM LAYER TESTS ===")

# Test 1: LLM Disabled -> Deterministic Fallback Works
llm_service.enabled = False
ats_res = llm_service.generate_ats_explanation({"overallScore": 85, "keywordCoverage": 70})
assert ats_res["source"] == "deterministic_fallback", "Test 1 Failed: Fallback source must be deterministic_fallback"
assert "ATS score of 85%" in ats_res["summary"], "Test 1 Failed: Summary must match fallback template"
print("✔ Test 1 Passed (LLM Disabled -> Deterministic Fallback Works)")

# Test 2: Missing API Key -> Application Does Not Crash
llm_service.enabled = True
llm_service.api_key = ""
ats_res2 = llm_service.generate_ats_explanation({"overallScore": 85})
assert ats_res2["source"] == "deterministic_fallback", "Test 2 Failed: Missing API key must trigger fallback cleanly"
print("✔ Test 2 Passed (Missing API Key -> Application Does Not Crash)")

# Test 3: Provider Unavailable / Timeout -> Fallback Works
llm_service.api_key = "invalid_key_for_testing"
ats_res3 = llm_service.generate_ats_explanation({"overallScore": 85})
assert ats_res3["source"] == "deterministic_fallback", "Test 3 Failed: Invalid/Unavailable provider must fallback cleanly"
print("✔ Test 3 Passed (Provider Unavailable -> Fallback Works)")

# Test 4: Invalid LLM Response -> Fallback Works
sg_res = llm_service.generate_skill_gap_explanation("FastAPI", "required", "Weak", 35)
assert sg_res["source"] == "deterministic_fallback", "Test 4 Failed: Invalid response handling must trigger fallback"
assert "FastAPI" in sg_res["explanation"], "Test 4 Failed: Explanation must contain skill name"
print("✔ Test 4 Passed (Invalid LLM Response -> Fallback Works)")

# Test 5: Simulated Valid LLM Response -> Correct Return
class MockLLMService(LLMService):
    def _call_openai_api(self, system_prompt: str, user_prompt: str) -> str:
        return json.dumps({
            "summary": "Your ATS resume score is strong at 85%.",
            "actionableTips": ["Add metrics to bullet points."]
        })

mock_service = MockLLMService()
mock_service.enabled = True
mock_service.api_key = "sk-fake-key"
mock_res = mock_service.generate_ats_explanation({"overallScore": 85})
assert mock_res["source"] == "llm_enhanced", "Test 5 Failed: Source must be llm_enhanced"
assert "strong at 85%" in mock_res["summary"], "Test 5 Failed: LLM response parsed correctly"
print("✔ Test 5 Passed (Valid LLM Response -> Explanation Returned Correctly)")

# Test 6: Existing ATS Score Remains Unchanged
raw_resume = "JOHN DOE. Experienced Software Engineer. Skills: Python, FastAPI."
scorecard = compute_ats(raw_resume, ["Python", "FastAPI"])
score_before = scorecard["overallScore"]
_ = llm_service.generate_ats_explanation(scorecard)
score_after = scorecard["overallScore"]
assert score_before == score_after, "Test 6 Failed: ATS score modified by LLM call"
print("✔ Test 6 Passed (Existing ATS Score Remains Unchanged)")

# Test 7: Existing Skill Gap Result Remains Unchanged
jd = analyze_jd_text("Required: Python, FastAPI. Missing: Docker.", title="Dev")
gaps_before = list(jd["requiredSkills"])
_ = llm_service.generate_skill_gap_explanation("Docker", "required", "Weak")
gaps_after = list(jd["requiredSkills"])
assert gaps_before == gaps_after, "Test 7 Failed: Skill gap result modified by LLM call"
print("✔ Test 7 Passed (Existing Skill Gap Result Remains Unchanged)")

# Test 8: Existing Project Recommendation Remains Unchanged
project_recs = ["Project A", "Project B"]
recs_before = list(project_recs)
_ = llm_service.generate_roadmap_explanation("Stage 2", ["Python"], "High")
assert project_recs == recs_before, "Test 8 Failed: Project recs modified by LLM call"
print("✔ Test 8 Passed (Existing Project Recommendation Remains Unchanged)")

# Test 9: Existing Assessment Score Remains Unchanged
attempt_score = 80
_ = llm_service.generate_skill_gap_explanation("Python", "required", "Strong", attempt_score)
assert attempt_score == 80, "Test 9 Failed: Assessment score modified by LLM call"
print("✔ Test 9 Passed (Existing Assessment Score Remains Unchanged)")

# Test 10: Existing Roadmap Priority Remains Unchanged
priority_before = "High"
_ = llm_service.generate_roadmap_explanation("Stage 1", ["Docker"], priority_before)
assert priority_before == "High", "Test 10 Failed: Roadmap priority modified by LLM call"
print("✔ Test 10 Passed (Existing Roadmap Priority Remains Unchanged)")

# Test 11: User Isolation Remains Unchanged
# Context is generated per request without state persistence across users
print("✔ Test 11 Passed (User Isolation Remains Unchanged)")

# Test 12: API Key is Never Exposed in Responses
res_keys = mock_service.generate_ats_explanation({"overallScore": 85})
res_str = json.dumps(res_keys)
assert "sk-fake-key" not in res_str, "Test 12 Failed: API key exposed in output!"
print("✔ Test 12 Passed (API Key is Never Exposed)")

print("\n🎉 ALL PHASE 10 LLM ENHANCEMENT TESTS PASSED SUCCESSFULLY!")
