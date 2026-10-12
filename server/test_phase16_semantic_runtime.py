"""
Phase 16 — Sentence Transformer Environment Error Fix & Real Semantic Matching Validation
Career Compass AI

Verifies:
1. Python Environment & sentence-transformers module import
2. SentenceTransformer ("all-MiniLM-L6-v2") model initialization & embedding dimension (384)
3. Real Dense Semantic Similarity Calculation (cos_sim)
4. Negative Semantic Matching (Unrelated skills are NOT matched)
5. Normalization & Taxonomy Alias Resolution
6. 60/40 Hybrid Match Score Calculation Formula
7. Real Full Resume + JD Pipeline Integration
"""

import sys
import os
from pathlib import Path

SERVER_DIR = Path(__file__).parent
sys.path.insert(0, str(SERVER_DIR))

# Force PyTorch backend
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"

def run_phase16_tests():
    print("=" * 75)
    print("CAREER COMPASS AI — PHASE 16 SEMANTIC MATCHING RUNTIME VERIFICATION")
    print("=" * 75)

    # -------------------------------------------------------------
    # STEP 1: ENVIRONMENT & MODULE IMPORT CHECK
    # -------------------------------------------------------------
    print("\n[STEP 1] Inspecting Python Environment & Importing sentence_transformers...")
    print(f"  Python Version: {sys.version.split()[0]}")
    print(f"  Executable Path: {sys.executable}")

    try:
        # pyrefly: ignore [missing-import]
        import sentence_transformers
        print(f"  sentence-transformers Version: {sentence_transformers.__version__}")
        # pyrefly: ignore [missing-import]
        from sentence_transformers import SentenceTransformer, util
        print("  ✔ sentence_transformers Import SUCCESSFUL!")
    except Exception as e:
        print(f"  ❌ Failed to import sentence_transformers: {e}")
        assert False, f"Import failure: {e}"

    # -------------------------------------------------------------
    # STEP 2: MODEL INITIALIZATION & EMBEDDING DIMENSION CHECK
    # -------------------------------------------------------------
    print("\n[STEP 2] Loading SentenceTransformer Model ('all-MiniLM-L6-v2')...")
    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        dim = model.get_sentence_embedding_dimension()
        print(f"  Model Name: all-MiniLM-L6-v2")
        print(f"  Embedding Dimension: {dim}")
        assert dim == 384, f"Expected dimension 384, got {dim}"
        print("  ✔ Model Initialization & Embedding Dimension 384 PASS!")
    except Exception as e:
        print(f"  ❌ Model loading failed: {e}")
        assert False, f"Model load failure: {e}"

    # -------------------------------------------------------------
    # STEP 3: DIRECT DENSE SEMANTIC SIMILARITY TEST
    # -------------------------------------------------------------
    print("\n[STEP 3] Testing Direct Dense Semantic Similarity Calculation...")
    res_text = "RESTful API development using Python and FastAPI"
    jd_text = "REST API engineering with Python"

    emb1 = model.encode(res_text, convert_to_tensor=True)
    emb2 = model.encode(jd_text, convert_to_tensor=True)
    cos_sim = util.cos_sim(emb1, emb2).item()
    sim_percent = round(cos_sim * 100, 1)

    print(f"  Resume Text: '{res_text}'")
    print(f"  JD Text:     '{jd_text}'")
    print(f"  Raw Cosine Similarity: {cos_sim:.4f}")
    print(f"  Semantic Similarity Score: {sim_percent}%")

    assert sim_percent >= 60.0, f"Expected high similarity >=60%, got {sim_percent}%"
    print("  ✔ Real SentenceTransformer Semantic Similarity Calculation PASS!")

    # -------------------------------------------------------------
    # STEP 4: NEGATIVE SEMANTIC TEST (NO OVERMATCHING)
    # -------------------------------------------------------------
    print("\n[STEP 4] Testing Negative Semantic Match (Unrelated Technologies)...")
    neg_pairs = [
        ("Python programming", "Docker containerization"),
        ("React frontend component", "Spring Boot Java backend"),
        ("SQL database queries", "Docker containerization"),
    ]

    for t1, t2 in neg_pairs:
        e1 = model.encode(t1, convert_to_tensor=True)
        e2 = model.encode(t2, convert_to_tensor=True)
        sim = util.cos_sim(e1, e2).item() * 100
        print(f"  Similarity between '{t1}' and '{t2}': {sim:.1f}%")
        assert sim < 50.0, f"Unrelated technologies overmatched: {t1} vs {t2} scored {sim:.1f}%"

    print("  ✔ Negative Semantic Test PASS (Unrelated skills properly distinguished)!")

    # -------------------------------------------------------------
    # STEP 5: SEMANTIC_MATCHER SERVICE INTEGRATION
    # -------------------------------------------------------------
    print("\n[STEP 5] Testing server/services/semantic_matcher.py functions...")
    from services.semantic_matcher import compute_semantic_similarity, compute_hybrid_match

    sem_score = compute_semantic_similarity(res_text, jd_text)
    print(f"  compute_semantic_similarity() result: {sem_score}%")
    assert sem_score >= 60.0, "Service semantic similarity failed"

    rule_score = 75.0
    hybrid_res = compute_hybrid_match(rule_score, res_text, jd_text)
    expected_hybrid = round(rule_score * 0.60 + sem_score * 0.40, 1)

    print(f"  Rule Score: {rule_score}%, Semantic Score: {sem_score}%, Hybrid Score: {hybrid_res['hybrid_match_score']}%")
    print(f"  Engine Used: {hybrid_res['engine']}")

    assert hybrid_res["engine"].startswith("SentenceTransformers"), f"Expected SentenceTransformers engine, got {hybrid_res['engine']}"
    assert abs(hybrid_res["hybrid_match_score"] - expected_hybrid) <= 0.1, "Hybrid formula calculation error"

    print("  ✔ semantic_matcher.py Integration & 60/40 Hybrid Formula PASS!")

    # -------------------------------------------------------------
    # STEP 6: FULL PIPELINE INTEGRATION TEST
    # -------------------------------------------------------------
    print("\n[STEP 6] Testing Full Resume + JD Pipeline Integration...")
    from services.skill_extractor import extract_skills, get_canonical_skill_name
    from services.jd_analyzer import analyze_jd_text

    full_resume = "Full Stack Engineer with 4 years experience in Python, FastAPI, SQL Database, ReactJS, and RESTful API development."
    full_jd = "Senior Full Stack Developer position. Required skills: Python, FastAPI, SQL, Docker, React. Preferred skills: AWS, TypeScript."

    resume_skills = extract_skills(full_resume)
    jd_analysis = analyze_jd_text(full_jd, title="Full Stack Developer")

    active_req = [s for s in jd_analysis["requiredSkills"] if s not in jd_analysis["otherSkills"]]
    active_pref = [s for s in jd_analysis["preferredSkills"] if s not in jd_analysis["otherSkills"]]

    matched = [s for s in active_req + active_pref if s in resume_skills]
    missing_req = [s for s in active_req if s not in resume_skills]
    missing_pref = [s for s in active_pref if s not in resume_skills]

    print(f"  Resume Skills Extracted: {resume_skills}")
    print(f"  Matched Skills: {matched}")
    print(f"  Missing Required Skills: {missing_req}")
    print(f"  Missing Preferred Skills: {missing_pref}")

    assert "Python" in matched and "FastAPI" in matched and "SQL" in matched and "React" in matched
    assert "Docker" in missing_req
    assert "AWS" in missing_pref

    print("  ✔ Full Pipeline Resume <-> JD Integration PASS!")

    print("\n" + "=" * 75)
    print("🎉 ALL PHASE 16 SEMANTIC MATCHING RUNTIME VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 75)

if __name__ == "__main__":
    run_phase16_tests()
