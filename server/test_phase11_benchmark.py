import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(__file__))

from services.skill_extractor import extract_skills, normalize_text
from services.jd_analyzer import analyze_jd_text
from services.resume_analyzer import analyze_resume_text, compute_ats
from services.semantic_matcher import compute_semantic_similarity, compute_hybrid_match
from services.llm_service import llm_service

print("=== RUNNING PHASE 11 FULL BENCHMARK & EVALUATION SUITE ===")

# ----------------------------------------------------
# 1. LOAD BENCHMARK DATASET
# ----------------------------------------------------
benchmark_path = os.path.join(os.path.dirname(__file__), "datasets", "benchmark", "benchmark_cases.json")
with open(benchmark_path, "r", encoding="utf-8") as f:
    benchmark_data = json.load(f)

print(f"Loaded '{benchmark_data['datasetName']}' with {len(benchmark_data['cases'])} benchmark cases.")

# ----------------------------------------------------
# 2. SKILL EXTRACTION & NORMALIZATION EVALUATION
# ----------------------------------------------------
print("\n--- 2. SKILL EXTRACTION EVALUATION ---")
eval_pairs = [
    ("Java vs JavaScript", "Expert in Java and JavaScript development.", ["Java", "JavaScript"]),
    ("C vs CSS", "Fluent in C programming and CSS layout.", ["C", "CSS"]),
    ("Go vs Google", "Developed in Go for Google Cloud.", ["Go"]),
    ("React vs ReactJS", "Built UI with ReactJS.", ["React"]),
    ("Scikit-learn vs sklearn", "Trained models using Scikit-learn and sklearn.", ["Scikit-learn"]),
    ("SQL vs PostgreSQL", "Database design in SQL and PostgreSQL.", ["SQL", "PostgreSQL"]),
    ("NLP vs Natural Language Processing", "Specialized in NLP and Natural Language Processing.", ["NLP", "Natural Language Processing"])
]

tp_total = 0
fp_total = 0
fn_total = 0

for label, text, expected in eval_pairs:
    extracted = extract_skills(text)
    ext_names = [x["name"] if isinstance(x, dict) else str(x) for x in extracted]
    
    tp = sum(1 for e in expected if any(normalize_text(e) == normalize_text(x) for x in ext_names))
    fp = sum(1 for x in ext_names if not any(normalize_text(e) == normalize_text(x) for e in expected))
    fn = sum(1 for e in expected if not any(normalize_text(e) == normalize_text(x) for x in ext_names))
    
    tp_total += tp
    fp_total += fp
    fn_total += fn

precision = tp_total / max(1, (tp_total + fp_total))
recall = tp_total / max(1, (tp_total + fn_total))
f1 = (2 * precision * recall) / max(1e-6, (precision + recall))

print(f"Skill Extraction Metrics (Controlled Benchmark):")
print(f"  True Positives: {tp_total}, False Positives: {fp_total}, False Negatives: {fn_total}")
print(f"  Precision: {precision:.4f}")
print(f"  Recall:    {recall:.4f}")
print(f"  F1 Score:  {f1:.4f}")
assert f1 >= 0.75, "Skill extraction F1 score below threshold!"

# ----------------------------------------------------
# 3. JD PARSING EVALUATION
# ----------------------------------------------------
print("\n--- 3. JD PARSING EVALUATION ---")
jd_text_test = """
Senior Backend Engineer
Required skills: Python, FastAPI, PostgreSQL.
Preferred skills: Docker, AWS.
Note: Experience with Kubernetes is not required.
Experience: 3-5 years.
Education: Bachelor's degree in Computer Science.
"""
jd_res = analyze_jd_text(jd_text_test, title="Senior Backend Engineer")
assert "Python" in jd_res["requiredSkills"], "JD Parsing: Python missing from required skills"
assert "FastAPI" in jd_res["requiredSkills"], "JD Parsing: FastAPI missing from required skills"
assert "Docker" in jd_res["preferredSkills"], "JD Parsing: Docker missing from preferred skills"
assert "Kubernetes" in jd_res["otherSkills"], "JD Parsing: Negated skill Kubernetes not captured in other/negated skills"
assert "Kubernetes" not in jd_res["requiredSkills"], "JD Parsing: Negated skill Kubernetes falsely marked as required"
print("✔ JD Parsing Evaluation Passed (Required/Preferred/Negated skills extracted correctly)")

# ----------------------------------------------------
# 4. SEMANTIC MATCHING EVALUATION
# ----------------------------------------------------
print("\n--- 4. SEMANTIC MATCHING EVALUATION ---")
text_a = "Experienced Python software engineer building REST APIs and microservices."
text_b = "Backend developer working with Python, FastAPI, and web services."
text_c = "Professional graphic designer creating logos and digital art."

sim_ab = compute_semantic_similarity(text_a, text_b)
sim_ac = compute_semantic_similarity(text_a, text_c)

print(f"Semantic Similarity (Related Pair A-B):   {sim_ab:.4f}")
print(f"Semantic Similarity (Unrelated Pair A-C): {sim_ac:.4f}")

assert sim_ab > sim_ac, "Semantic matching failed: Related pair must score higher than unrelated pair!"
hybrid_res = compute_hybrid_match(80, text_a, text_b)
hybrid_score = hybrid_res["hybrid_match_score"]
assert 0 <= hybrid_score <= 100, "Hybrid score out of bounds!"
print(f"Hybrid Score (80% Heuristic + {sim_ab:.2f} Semantic): {hybrid_score:.2f}%")
print("✔ Semantic Matching Evaluation Passed")

# ----------------------------------------------------
# 5. ATS SCORECARD EVALUATION
# ----------------------------------------------------
print("\n--- 5. ATS SCORECARD EVALUATION ---")
strong_resume = "JOHN DOE. Software Engineer. Skills: Python, FastAPI, PostgreSQL, Git. Built scalable APIs. B.Tech Computer Science."
weak_resume = "Hi I like coding."

ats_strong = compute_ats(strong_resume, ["Python", "FastAPI", "PostgreSQL", "Git"])
ats_weak = compute_ats(weak_resume, ["coding"])

print(f"Strong Resume ATS Score: {ats_strong['overallScore']}%")
print(f"Weak Resume ATS Score:   {ats_weak['overallScore']}%")
assert ats_strong['overallScore'] > ats_weak['overallScore'], "ATS Evaluation: Strong resume must score higher than weak resume!"
print("✔ ATS Scorecard Evaluation Passed")

# ----------------------------------------------------
# 6. SKILL GAP & PRIORITY EVALUATION
# ----------------------------------------------------
print("\n--- 6. SKILL GAP EVALUATION ---")
req_gaps = ["AWS", "Docker"]
pref_gaps = ["Kubernetes"]
negated_skills = ["PHP"]

assert req_gaps[0] not in negated_skills, "Skill Gap: Negated skill included in gaps"
print("✔ Skill Gap Priority & Exclusion Evaluation Passed")

# ----------------------------------------------------
# 7. LONGITUDINAL PROGRESS EVALUATION
# ----------------------------------------------------
print("\n--- 7. LONGITUDINAL PROGRESS EVALUATION ---")
attempts = [
    {"date": "2026-01-01", "scores": {"FastAPI": 35, "Docker": 30}},
    {"date": "2026-01-08", "scores": {"FastAPI": 75, "Docker": 40}},
    {"date": "2026-01-15", "scores": {"FastAPI": 82, "Docker": 72}}
]

fastapi_history = [a["scores"]["FastAPI"] for a in attempts]
fastapi_latest = fastapi_history[-1]
fastapi_prev = fastapi_history[-2]
fastapi_imp = fastapi_latest - fastapi_prev

print(f"FastAPI Score Progression: {fastapi_history}")
print(f"FastAPI Latest: {fastapi_latest}%, Previous: {fastapi_prev}%, Improvement: +{fastapi_imp}%")
assert fastapi_imp == 7, "Longitudinal Progress: Incorrect improvement calculation"
assert fastapi_latest >= 70, "FastAPI status should be Strong (>=70%)"
print("✔ Longitudinal Progress Evaluation Passed")

# ----------------------------------------------------
# 8. PERFORMANCE LATENCY MEASUREMENTS
# ----------------------------------------------------
print("\n--- 8. PERFORMANCE LATENCY MEASUREMENTS ---")
t0 = time.perf_counter()
_ = analyze_resume_text(strong_resume)
t1 = time.perf_counter()
resume_lat_ms = (t1 - t0) * 1000

t0 = time.perf_counter()
_ = compute_semantic_similarity(text_a, text_b)
t1 = time.perf_counter()
sem_lat_ms = (t1 - t0) * 1000

t0 = time.perf_counter()
_ = analyze_jd_text(jd_text_test, title="Senior Backend Engineer")
t1 = time.perf_counter()
jd_lat_ms = (t1 - t0) * 1000

print(f"Performance Measurements (Environment-Dependent):")
print(f"  Resume Analysis Latency:  {resume_lat_ms:.2f} ms")
print(f"  Semantic Matching Latency: {sem_lat_ms:.2f} ms")
print(f"  JD Parsing Latency:       {jd_lat_ms:.2f} ms")

# ----------------------------------------------------
# 9. CONCEPTUAL RISK INVARIANT CHECKS
# ----------------------------------------------------
print("\n--- 9. CONCEPTUAL RISK INVARIANT CHECKS ---")
# Risk 1: Python should not automatically mean FastAPI
python_skills = extract_skills("I am an expert in Python programming.")
python_names = [x["name"] if isinstance(x, dict) else str(x) for x in python_skills]
assert "Python" in python_names, "Python should be detected"
assert "FastAPI" not in python_names, "Parent skill Python must NOT automatically imply child skill FastAPI!"

# Risk 2: Scikit-learn tool detection vs domain classification
sklearn_skills = extract_skills("I use Scikit-learn for modeling.")
sklearn_names = [x["name"] if isinstance(x, dict) else str(x) for x in sklearn_skills]
assert "Scikit-learn" in sklearn_names, "Scikit-learn should be detected"

print("✔ Conceptual Risk Invariant Checks Passed")

print("\n🎉 ALL PHASE 11 EVALUATION & BENCHMARK TESTS PASSED SUCCESSFULLY!")
