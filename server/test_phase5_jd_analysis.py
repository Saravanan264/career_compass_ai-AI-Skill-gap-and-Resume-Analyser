from services.jd_analyzer import analyze_jd_text

print("=== RUNNING PHASE 5 JD NLP ANALYSIS TESTS ===")

jd1 = """
Junior Backend Developer
We are looking for a Junior Backend Developer.
Required skills: Python, FastAPI, REST API, SQL.
Preferred skills: AWS.
Experience with Docker is not required.
Experience: 1-2 years of backend experience.
Education: B.Tech / B.E. in Computer Science or related field.
"""

res1 = analyze_jd_text(jd1, title="Junior Backend Developer")
print("\n--- TEST JD 1 RESULTS ---")
print("Title:", res1["extractedTitle"])
print("Required Skills:", res1["requiredSkills"])
print("Preferred Skills:", res1["preferredSkills"])
print("Other/Negated Skills:", res1["otherSkills"])
print("Experience Struct:", res1["structuredExperience"])
print("Education Struct:", res1["structuredEducation"])

jd2 = """
Frontend Developer
Required: JavaScript, React, HTML, CSS.
Preferred: TypeScript, Next.js.
"""

res2 = analyze_jd_text(jd2, title="Frontend Developer")
print("\n--- TEST JD 2 RESULTS ---")
print("Required Skills:", res2["requiredSkills"])
print("Preferred Skills:", res2["preferredSkills"])

jd3 = """
AI/ML Engineer
Required: Python, Machine Learning, Scikit-learn.
Preferred: PyTorch, NLP, Generative AI.
"""

res3 = analyze_jd_text(jd3, title="AI/ML Engineer")
print("\n--- TEST JD 3 RESULTS ---")
print("Required Skills:", res3["requiredSkills"])
print("Preferred Skills:", res3["preferredSkills"])
print("Categorized AI/ML Skills:", res3["categorizedSkills"]["ai_ml"])
print("Categorized Generative AI Skills:", res3["categorizedSkills"]["generative_ai"])

print("\n✔ PHASE 5 JD NLP ANALYSIS TESTS COMPLETED!")
