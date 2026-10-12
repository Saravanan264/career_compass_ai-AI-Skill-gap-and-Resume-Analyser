import re
from typing import Dict, Any, List, Optional
from services.skill_extractor import extract_skills, normalize_text, load_skills_db
from services.jd_parser import clean_jd_text

KNOWN_TITLES = [
    "Backend Developer", "Frontend Developer", "Full Stack Developer",
    "Data Scientist", "Data Analyst", "Machine Learning Engineer",
    "DevOps Engineer", "Software Engineer", "Systems Engineer",
    "Mobile Developer", "QA Engineer", "Product Manager"
]

def extract_job_title(text: str, provided_title: Optional[str] = None) -> str:
    if provided_title and provided_title.strip() and provided_title.lower() != "custom":
        return provided_title.strip()
    
    norm_text = text.lower()
    for title in KNOWN_TITLES:
        if title.lower() in norm_text:
            return title
            
    return "Custom Job Role"

def is_skill_negated(skill_norm: str, norm_text: str, idx: int) -> bool:
    """
    Check if a skill is explicitly negated (e.g., 'not required', 'no experience needed').
    """
    preceding = norm_text[max(0, idx - 60): idx]
    succeeding = norm_text[idx + len(skill_norm): idx + len(skill_norm) + 40]

    negation_patterns = [
        "not required", "is not required", "no experience required",
        "not mandatory", "no prior experience needed", "optional and not required"
    ]

    if any(pattern in preceding for pattern in negation_patterns) or any(pattern in succeeding for pattern in negation_patterns):
        return True
    return False

def classify_skills(detected_skills: List[str], norm_text: str):
    required_skills = []
    preferred_skills = []
    other_skills = []
    importance = {}

    req_patterns = ["required", "must have", "must possess", "mandatory", "minimum requirement", "essential", "basic", "hands-on experience"]
    pref_patterns = ["preferred", "nice to have", "good to have", "plus", "bonus", "desirable", "optional", "a plus"]

    skills_db = {s["name"]: s for s in load_skills_db()}

    for skill in detected_skills:
        skill_norm = normalize_text(skill)
        idx = norm_text.find(skill_norm)
        
        is_preferred = False
        is_negated = False

        if idx != -1:
            is_negated = is_skill_negated(skill_norm, norm_text, idx)
            preceding = norm_text[max(0, idx - 80): idx]
            succeeding = norm_text[idx + len(skill_norm): idx + len(skill_norm) + 30]
            
            has_pref_before = any(p in preceding for p in pref_patterns)
            has_req_before = any(r in preceding for r in req_patterns)

            if has_pref_before:
                pref_pos = max(preceding.rfind(p) for p in pref_patterns if p in preceding)
                req_pos = max(preceding.rfind(r) for r in req_patterns if r in preceding) if has_req_before else -1
                if pref_pos > req_pos:
                    is_preferred = True
            
            if not is_preferred and any(p in succeeding for p in ["is a plus", "nice to have", "is preferred", "bonus"]):
                is_preferred = True

        if is_negated:
            other_skills.append(skill)
        elif is_preferred:
            preferred_skills.append(skill)
        else:
            required_skills.append(skill)

    # Assign importance scores (10-1)
    for i, s in enumerate(required_skills):
        importance[s] = max(7, 10 - (i // 2))
    for i, s in enumerate(preferred_skills):
        importance[s] = max(4, 6 - (i // 2))
    for s in other_skills:
        importance[s] = 3

    return required_skills, preferred_skills, other_skills, importance

def categorize_skills_dynamic(detected_skills: List[str]) -> Dict[str, List[str]]:
    """
    Categorize detected skills dynamically using the central taxonomy.
    """
    all_taxonomy = load_skills_db()
    taxonomy_map = {s["name"].lower(): s for s in all_taxonomy}

    result = {
        "programming_languages": [],
        "frontend": [],
        "backend": [],
        "frameworks": [],
        "databases": [],
        "cloud_technologies": [],
        "devops": [],
        "ai_ml": [],
        "nlp": [],
        "generative_ai": [],
        "testing": [],
        "tools": [],
        "soft_skills": []
    }

    for skill in detected_skills:
        tax_entry = taxonomy_map.get(skill.lower())
        if not tax_entry:
            result["tools"].append(skill)
            continue

        cat = tax_entry.get("category", "")
        if cat == "Programming Languages":
            result["programming_languages"].append(skill)
        elif cat in ["Web Technologies", "Frontend Frameworks"]:
            if "Framework" in cat:
                result["frameworks"].append(skill)
            else:
                result["frontend"].append(skill)
        elif cat == "Backend Frameworks":
            result["backend"].append(skill)
            result["frameworks"].append(skill)
        elif cat == "Databases":
            result["databases"].append(skill)
        elif cat == "Cloud Technologies":
            result["cloud_technologies"].append(skill)
        elif cat in ["DevOps", "Version Control", "Systems & Infrastructure"]:
            result["devops"].append(skill)
        elif cat in ["Machine Learning", "Deep Learning", "Data Science"]:
            result["ai_ml"].append(skill)
        elif cat == "NLP":
            result["nlp"].append(skill)
            result["ai_ml"].append(skill)
        elif cat == "Generative AI":
            result["generative_ai"].append(skill)
            result["ai_ml"].append(skill)
        elif cat == "Testing & Quality":
            result["testing"].append(skill)
        elif cat == "Soft Skills":
            result["soft_skills"].append(skill)
        else:
            result["tools"].append(skill)

    return result

def extract_experience_req(text: str) -> Dict[str, Any]:
    """
    Extract structured experience requirements (min, max, level, raw).
    """
    # Check range pattern (e.g. 2-4 years, 2 to 5 yrs)
    range_match = re.search(r'\b(\d+)\s*(?:-|to|–)\s*(\d+)\s*(?:years?|yrs?)\b', text, re.IGNORECASE)
    if range_match:
        min_y = int(range_match.group(1))
        max_y = int(range_match.group(2))
        return {
            "rawText": range_match.group(0).strip(),
            "minimumYears": min_y,
            "maximumYears": max_y,
            "experienceLevel": "Mid Level" if min_y >= 2 else "Entry Level"
        }

    # Check plus/minimum pattern (e.g. 3+ years, 3 years, min 2 yrs)
    min_match = re.search(r'\b(?:minimum|at least)?\s*(\d+)\s*\+?\s*(?:years?|yrs?)\b', text, re.IGNORECASE)
    if min_match:
        min_y = int(min_match.group(1))
        level = "Senior Level" if min_y >= 5 else ("Mid Level" if min_y >= 2 else "Entry Level")
        return {
            "rawText": min_match.group(0).strip(),
            "minimumYears": min_y,
            "maximumYears": None,
            "experienceLevel": level
        }

    # Check entry level / fresher pattern
    if re.search(r'\b(fresher|entry[\s-]level|internship)\b', text, re.IGNORECASE):
        return {
            "rawText": "Entry Level / Internship",
            "minimumYears": 0,
            "maximumYears": 1,
            "experienceLevel": "Entry Level"
        }

    return {
        "rawText": "Not specified",
        "minimumYears": None,
        "maximumYears": None,
        "experienceLevel": "Unknown"
    }

def extract_education_req(text: str) -> Dict[str, Any]:
    """
    Extract structured education requirements.
    """
    degrees = []
    if re.search(r'\b(b\.tech|b\.e|bachelor|b\.sc)\b', text, re.IGNORECASE):
        degrees.append("Bachelor's Degree (B.Tech/B.E./B.Sc)")
    if re.search(r'\b(m\.tech|m\.e|master|m\.sc)\b', text, re.IGNORECASE):
        degrees.append("Master's Degree (M.Tech/M.E./M.Sc)")
    if re.search(r'\b(phd|doctorate)\b', text, re.IGNORECASE):
        degrees.append("PhD / Doctorate")

    majors = []
    if re.search(r'\bcomputer science\b', text, re.IGNORECASE):
        majors.append("Computer Science")
    if re.search(r'\binformation technology\b', text, re.IGNORECASE):
        majors.append("Information Technology")
    if re.search(r'\bartificial intelligence|ai\b', text, re.IGNORECASE):
        majors.append("Artificial Intelligence")
    if re.search(r'\bdata science\b', text, re.IGNORECASE):
        majors.append("Data Science")

    raw_match = re.search(r'(\b(?:bachelor|master|b\.tech|m\.tech|b\.e|b\.sc|m\.sc|phd|degree)\b[^\n\.\,]*?(?:computer science|engineering|technology|field|related)?\b)', text, re.IGNORECASE)
    raw_str = raw_match.group(1).strip() if raw_match else (degrees[0] if degrees else "Not specified")

    return {
        "rawText": raw_str,
        "recognizedDegrees": degrees,
        "recognizedMajors": majors
    }

def analyze_jd_text(text_raw: str, title: Optional[str] = None, company_name: Optional[str] = None) -> Dict[str, Any]:
    cleaned_text = clean_jd_text(text_raw)
    norm_text = normalize_text(cleaned_text)

    extracted_title = extract_job_title(cleaned_text, title)
    detected_skills = extract_skills(cleaned_text)

    required_skills, preferred_skills, other_skills, importance = classify_skills(detected_skills, norm_text)
    categories = categorize_skills_dynamic(detected_skills)

    exp_struct = extract_experience_req(cleaned_text)
    edu_struct = extract_education_req(cleaned_text)

    return {
        "extractedTitle": extracted_title,
        "companyName": company_name or "Custom Company",
        "rawText": cleaned_text,
        "requiredSkills": required_skills,
        "preferredSkills": preferred_skills,
        "otherSkills": other_skills,
        "allSkills": detected_skills,
        "tools": categories["tools"],
        "frameworks": categories["frameworks"],
        "databases": categories["databases"],
        "cloudTechnologies": categories["cloud_technologies"],
        "softSkills": categories["soft_skills"],
        "categorizedSkills": categories,
        "experienceRequirements": exp_struct["rawText"],
        "structuredExperience": exp_struct,
        "educationRequirements": edu_struct["rawText"],
        "structuredEducation": edu_struct,
        "importance": importance
    }
