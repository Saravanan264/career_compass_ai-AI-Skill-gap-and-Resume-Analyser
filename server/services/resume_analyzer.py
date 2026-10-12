import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from services.skill_extractor import extract_skills, normalize_text, load_skills_db
from services.resume_parser import validate_resume_structure

DATA_DIR = Path(__file__).parent.parent / "data"

# Configurable ATS Scorecard Weights
DEFAULT_ATS_WEIGHTS = {
    "format": 0.15,
    "sectionCompleteness": 0.15,
    "requiredSkillCoverage": 0.25,
    "preferredSkillCoverage": 0.10,
    "experienceAlignment": 0.15,
    "educationAlignment": 0.10,
    "impactEvidence": 0.10
}

def load_domains_db() -> List[Dict[str, Any]]:
    domains_file = DATA_DIR / "domains.json"
    with open(domains_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("domains", [])

def count_matches(text: str, keywords: List[str]) -> int:
    hits = 0
    for k in keywords:
        kk = normalize_text(k)
        if kk and kk in text:
            hits += 1
    return hits

def score_presence(text: str, patterns: List[str], max_score: int = 100) -> int:
    n = count_matches(text, patterns)
    denom = max(1, len(patterns))
    return int(round((n / denom) * max_score))

def evaluate_parseability(text_raw: str) -> Dict[str, Any]:
    """
    Evaluates format, scannability, structural clarity, and parseability of extracted text.
    Returns a dynamic score (0 to 100) based on actual document characteristics.
    """
    if not text_raw or not text_raw.strip():
        return {
            "score": 0,
            "checks": {
                "textExtracted": False,
                "hasMinimumLength": False,
                "hasContactDetails": False,
                "scannableStructure": False
            },
            "warnings": ["Uploaded resume text is empty or unreadable."]
        }

    text_norm = normalize_text(text_raw)
    char_len = len(text_raw.strip())
    
    # 1. Contact details completeness (up to 25 pts)
    has_email = bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text_raw))
    has_phone = bool(re.search(r'\b(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b|\b\d{10}\b', text_raw)) or "phone" in text_norm
    has_profile = any(k in text_norm for k in ["linkedin", "github", "portfolio", "address", "location"])
    
    contact_score = 0
    if has_email: contact_score += 10
    if has_phone: contact_score += 8
    if has_profile: contact_score += 7
    has_contact = contact_score >= 10

    # 2. Structural section presence (up to 30 pts)
    sections_found = {
        "summary": any(k in text_norm for k in ["summary", "objective", "profile", "about"]),
        "experience": any(k in text_norm for k in ["experience", "employment", "work history", "internship"]),
        "education": any(k in text_norm for k in ["education", "academic", "university", "degree"]),
        "skills": any(k in text_norm for k in ["skills", "technologies", "proficiencies", "competencies"]),
        "projects": any(k in text_norm for k in ["projects", "personal projects", "academic projects"]),
    }
    core_section_count = sum(1 for v in sections_found.values() if v)
    if core_section_count >= 4:
        section_score = 30
    elif core_section_count == 3:
        section_score = 22
    elif core_section_count == 2:
        section_score = 15
    elif core_section_count == 1:
        section_score = 8
    else:
        section_score = 0
    has_sections = core_section_count >= 2

    # 3. Document text length & density appropriateness (up to 25 pts)
    if 1200 <= char_len <= 6000:
        length_score = 25
    elif 600 <= char_len < 1200 or 6000 < char_len <= 9000:
        length_score = 18
    elif 250 <= char_len < 600:
        length_score = 10
    else:
        length_score = 5
    has_length = char_len >= 250

    # 4. Bullet points and list organization (up to 20 pts)
    bullet_matches = len(re.findall(r'(?:^|\n)\s*[\u2022\u2023\u25b6\u25c0\u2013\u2014\-\*]\s+|(?:\d+\.\s+)', text_raw))
    if bullet_matches >= 5:
        format_org_score = 20
    elif bullet_matches >= 2:
        format_org_score = 12
    elif "\n" in text_raw and char_len >= 300:
        format_org_score = 8
    else:
        format_org_score = 5

    total_format_score = min(100, contact_score + section_score + length_score + format_org_score)

    checks = {
        "textExtracted": char_len > 0,
        "hasMinimumLength": has_length,
        "hasContactDetails": has_contact,
        "scannableStructure": has_sections
    }

    warnings = []
    if not has_email:
        warnings.append("Missing explicit email address in contact info.")
    if not has_phone:
        warnings.append("Missing explicit phone number.")
    if not has_length:
        warnings.append("Resume content is brief.")
    if core_section_count < 3:
        warnings.append("Resume lacks clear structural section headers.")

    return {
        "score": total_format_score,
        "checks": checks,
        "warnings": warnings
    }

def evaluate_section_completeness(text_raw: str) -> Dict[str, Any]:
    """
    Evaluates presence of key resume sections.
    """
    text_norm = normalize_text(text_raw)
    sections = {
        "contact": any(k in text_norm for k in ["email", "phone", "linkedin", "github", "address", "contact"]),
        "summary": any(k in text_norm for k in ["summary", "objective", "profile", "about"]),
        "education": any(k in text_norm for k in ["education", "university", "college", "degree", "bachelor", "master"]),
        "skills": any(k in text_norm for k in ["skills", "technologies", "proficiencies", "competencies"]),
        "projects": any(k in text_norm for k in ["projects", "personal projects", "academic projects"]),
        "experience": any(k in text_norm for k in ["experience", "employment", "work history", "internship"]),
        "certifications": any(k in text_norm for k in ["certification", "certifications", "licenses", "courses"]),
        "achievements": any(k in text_norm for k in ["achievements", "awards", "honors", "accomplishments"])
    }

    # Core 6 sections evaluate completeness
    core_keys = ["contact", "education", "skills", "projects", "experience", "summary"]
    core_present = sum(1 for k in core_keys if sections[k])
    score = int(round((core_present / len(core_keys)) * 100))

    return {
        "score": score,
        "sections": sections
    }

def evaluate_impact_evidence(text_raw: str) -> Dict[str, Any]:
    """
    Evaluates metrics, percentages, numbers, and action verbs in resume.
    """
    text_norm = normalize_text(text_raw)
    
    # Check for quantitative figures / percentages
    metrics_matches = re.findall(r'\b\d+[\%\+]?\b|\b\d+\s*(?:percent|users|customers|k|m|ms|sec|hours|sprint)\b', text_raw, re.IGNORECASE)
    metric_count = len(metrics_matches)
    if metric_count >= 3:
        metric_score = 40
    elif metric_count >= 1:
        metric_score = 25
    else:
        metric_score = 5
    
    action_verbs = ["increased", "reduced", "improved", "optimized", "launched", "delivered", "saved", "grew", "achieved", "developed", "built", "engineered", "architected", "automated", "created", "designed", "spearheaded", "transformed", "implemented"]
    matched_verbs = list(set([v for v in action_verbs if v in text_norm]))
    verb_count = len(matched_verbs)
    if verb_count >= 6:
        verb_score = 40
    elif verb_count >= 3:
        verb_score = 25
    elif verb_count >= 1:
        verb_score = 15
    else:
        verb_score = 0

    scale_words = ["production", "scaled", "automated", "benchmark", "uptime", "latency", "revenue", "efficiency", "throughput"]
    matched_scale = [w for w in scale_words if w in text_norm]
    if len(matched_scale) >= 2:
        scale_score = 20
    elif len(matched_scale) == 1:
        scale_score = 10
    else:
        scale_score = 0

    total_score = min(100, max(5, metric_score + verb_score + scale_score))

    return {
        "score": total_score,
        "hasQuantitativeMetrics": metric_count > 0,
        "matchedActionVerbs": matched_verbs
    }

def evaluate_experience_alignment(text_raw: str, structured_jd_exp: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Evaluates candidate experience signals against JD experience requirements.
    """
    text_norm = normalize_text(text_raw)
    
    has_role_title = any(r in text_norm for r in ["engineer", "developer", "architect", "lead", "manager", "analyst", "consultant", "specialist", "intern"])
    has_work_section = any(s in text_norm for s in ["experience", "employment", "work history", "career history"])
    
    exp_match = re.search(r'\b(\d+)\s*\+?\s*(?:years?|yrs?)\b', text_raw, re.IGNORECASE)
    cand_years = int(exp_match.group(1)) if exp_match else None
    has_company = any(c in text_norm for c in ["company", "inc", "ltd", "corp", "solutions", "tech", "systems", "team", "startup"])
    
    base_signal_score = 0
    if has_role_title: base_signal_score += 25
    if has_work_section: base_signal_score += 25
    
    if cand_years is not None:
        if cand_years >= 5: base_signal_score += 30
        elif cand_years >= 3: base_signal_score += 25
        elif cand_years >= 1: base_signal_score += 20
        else: base_signal_score += 12
    else:
        base_signal_score += 10

    if has_company: base_signal_score += 20
    signal_score = min(100, max(15, base_signal_score))

    if not structured_jd_exp or structured_jd_exp.get("minimumYears") is None:
        return {
            "score": signal_score,
            "status": "sufficient",
            "requiredMinimumYears": None,
            "candidateYears": f"{cand_years} yrs" if cand_years is not None else "Detected from resume signals",
            "explanation": "No rigid minimum years specified in job description."
        }

    min_req = structured_jd_exp["minimumYears"]

    if cand_years is not None:
        if cand_years >= min_req:
            score = 100
            status = "aligned"
            explanation = f"Candidate experience ({cand_years} yrs) meets or exceeds requirement ({min_req} yrs)."
        else:
            score = max(30, int((cand_years / min_req) * 100))
            status = "below_requirement"
            explanation = f"Candidate experience ({cand_years} yrs) is below requirement ({min_req} yrs)."
    else:
        score = signal_score
        status = "unspecified"
        explanation = "Experience presence detected via role keywords."

    return {
        "score": score,
        "status": status,
        "requiredMinimumYears": min_req,
        "candidateYears": cand_years if cand_years is not None else "Unspecified",
        "explanation": explanation
    }

def evaluate_education_alignment(text_raw: str, structured_jd_edu: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Evaluates candidate education against JD education requirements.
    """
    text_norm = normalize_text(text_raw)
    
    has_higher_degree = any(d in text_norm for d in ["master", "phd", "doctorate", "m.tech", "m.sc", "m.s.", "ms degree"])
    has_bachelor = any(d in text_norm for d in ["bachelor", "b.tech", "b.e", "b.sc", "b.s", "bs degree", "b.a"])
    has_associate = any(d in text_norm for d in ["associate", "diploma", "coursework"])
    has_university = any(u in text_norm for u in ["university", "college", "institute", "school", "academy"])
    has_field = any(f in text_norm for f in ["computer science", "data science", "engineering", "information technology", "mathematics", "software", "information systems"])
    has_honors = any(h in text_norm for h in ["gpa", "cgpa", "honors", "cum laude", "first class"])

    degree_score = 15
    if has_higher_degree:
        degree_score = 45
    elif has_bachelor:
        degree_score = 40
    elif has_associate:
        degree_score = 25

    inst_score = 25 if has_university else 10
    field_score = 20 if has_field else 5
    honors_score = 10 if has_honors else 0

    signal_score = min(100, max(20, degree_score + inst_score + field_score + honors_score))
    has_degree_matched = has_higher_degree or has_bachelor
    
    if not structured_jd_edu or not structured_jd_edu.get("recognizedDegrees"):
        return {
            "score": signal_score,
            "matched": has_degree_matched,
            "requiredEducation": "Degree in related field",
            "candidateEducation": "Higher Education Degree detected" if has_degree_matched else ("Education section detected" if "education" in text_norm else "Not explicitly specified"),
            "explanation": "Candidate education evaluated from resume signals."
        }

    req_degrees = structured_jd_edu["recognizedDegrees"]
    req_text = " ".join(req_degrees).lower()
    
    if has_higher_degree and ("master" in req_text or "phd" in req_text or "graduate" in req_text):
        score = 100
    elif has_bachelor:
        score = 100 if any(b in req_text for b in ["bachelor", "b.tech", "b.s", "degree"]) else 75
    elif has_degree_matched:
        score = 75
    elif "education" in text_norm:
        score = 50
    else:
        score = 30

    return {
        "score": score,
        "matched": has_degree_matched,
        "requiredEducation": req_degrees[0] if req_degrees else "Higher Education Degree",
        "candidateEducation": "Bachelor/Master Degree" if has_degree_matched else "Self-Taught / Coursework",
        "explanation": "Education alignment evaluated against target job posting."
    }

def compute_ats(text_raw: str, detected_skills: List[str], jd_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Computes overall ATS evaluation and structured scorecard.
    """
    text = normalize_text(text_raw)

    parseability = evaluate_parseability(text_raw)
    section_comp = evaluate_section_completeness(text_raw)
    impact = evaluate_impact_evidence(text_raw)

    format_score = parseability["score"]
    impact_score = impact["score"]

    exp_align = evaluate_experience_alignment(text_raw, jd_data.get("structuredExperience") if jd_data else None)
    edu_align = evaluate_education_alignment(text_raw, jd_data.get("structuredEducation") if jd_data else None)
    experience_score = exp_align["score"]
    education_score = edu_align["score"]

    # Compute domain fit to find target domain required skills
    domain_fits = compute_domain_fits(detected_skills)
    best_domain_name = domain_fits["bestFitDomain"]
    best_domain_fit = domain_fits["domains"].get(best_domain_name, {})
    domain_have_count = len(best_domain_fit.get("have", []))
    domain_missing_count = len(best_domain_fit.get("missing", []))
    domain_req_count = max(10, domain_have_count + domain_missing_count)

    all_skills = load_skills_db()
    top_keywords = [s["name"] for s in all_skills[:26]]
    missing_top = [k for k in top_keywords if k not in detected_skills]

    # Evaluate required & preferred skill coverage if JD data is provided
    has_valid_jd = bool(jd_data and (jd_data.get("requiredSkills") or jd_data.get("preferredSkills")))
    req_coverage_score = 100
    pref_coverage_score = 100
    matched_req = []
    missing_req = []
    matched_pref = []
    missing_pref = []

    if has_valid_jd:
        req_skills = jd_data.get("requiredSkills", [])
        pref_skills = jd_data.get("preferredSkills", [])
        
        matched_req = [s for s in req_skills if s in detected_skills]
        missing_req = [s for s in req_skills if s not in detected_skills]
        
        matched_pref = [s for s in pref_skills if s in detected_skills]
        missing_pref = [s for s in pref_skills if s not in detected_skills]

        req_coverage_score = int(round((len(matched_req) / max(1, len(req_skills))) * 100))
        pref_coverage_score = int(round((len(matched_pref) / max(1, len(pref_skills))) * 100)) if pref_skills else 100
        
        total_jd = len(req_skills) + len(pref_skills)
        matched_total_jd = len(matched_req) + len(matched_pref)
        keyword_coverage = int(round((matched_total_jd / max(1, total_jd)) * 100)) if total_jd > 0 else req_coverage_score
        skills_score = int(round(req_coverage_score * 0.70 + pref_coverage_score * 0.30))
    else:
        keyword_coverage = min(100, int(round((domain_have_count / domain_req_count) * 100)))
        domain_ratio = domain_have_count / max(1, domain_have_count + domain_missing_count)
        overall_skills_ratio = len(detected_skills) / 25.0
        skills_score = min(100, max(15, int(round((domain_ratio * 0.65 + overall_skills_ratio * 0.35) * 100))))

    # Calibrated Weighted ATS Score Computation
    if has_valid_jd:
        # JD Mode: Combine Standalone Resume Quality (50%) + Job Compatibility (50%)
        resume_quality = (
            format_score * 0.15 +
            section_comp["score"] * 0.15 +
            skills_score * 0.25 +
            experience_score * 0.20 +
            education_score * 0.15 +
            impact_score * 0.10
        )
        job_compatibility = (
            req_coverage_score * 0.40 +
            pref_coverage_score * 0.20 +
            exp_align["score"] * 0.20 +
            edu_align["score"] * 0.20
        )
        overall = resume_quality * 0.50 + job_compatibility * 0.50
    else:
        # Standalone Mode: Resume Quality Score
        overall = (
            format_score * 0.15 +
            section_comp["score"] * 0.15 +
            skills_score * 0.25 +
            experience_score * 0.20 +
            education_score * 0.15 +
            impact_score * 0.10
        )

    overall_score = max(10, min(100, int(round(overall))))

    # Detailed ATS Scorecard
    weights = DEFAULT_ATS_WEIGHTS
    ats_scorecard = {
        "overallAtsScore": overall_score,
        "weights": weights,
        "parseability": parseability,
        "sectionCompleteness": section_comp,
        "requiredSkillCoverage": {
            "score": req_coverage_score,
            "matched": matched_req,
            "missing": missing_req,
            "explanation": f"{len(matched_req)} of {len(jd_data.get('requiredSkills', [])) if jd_data else len(detected_skills)} required skills matched."
        },
        "preferredSkillCoverage": {
            "score": pref_coverage_score,
            "matched": matched_pref,
            "missing": missing_pref,
            "explanation": f"{len(matched_pref)} of {len(jd_data.get('preferredSkills', [])) if jd_data else 0} preferred skills matched."
        },
        "experienceAlignment": exp_align,
        "educationAlignment": edu_align,
        "impactEvidence": impact,
        "strengths": [
            "Scannable document format and structural parseability.",
            f"Detected {len(detected_skills)} technical and domain skills.",
            "Strong quantitative impact signals and action verb usage."
        ],
        "warnings": parseability["warnings"]
    }

    return {
        "overallScore": overall_score,
        "keywordCoverage": keyword_coverage,
        "sectionScores": {
            "format": format_score,
            "experience": experience_score,
            "skills": skills_score,
            "education": education_score,
            "impact": impact_score
        },
        "missingTopKeywords": missing_top,
        "atsScorecard": ats_scorecard
    }

def compute_domain_fits(detected_skills: List[str]) -> Dict[str, Any]:
    domains = load_domains_db()
    by_domain = {}

    for d in domains:
        name = d["name"]
        required = list(set(d.get("requiredSkills", [])))
        have = [s for s in required if s in detected_skills]
        missing = [s for s in required if s not in detected_skills]
        fit_score = int(round((len(have) / max(1, len(required))) * 100))
        by_domain[name] = {
            "fitScore": fit_score,
            "have": have,
            "missing": missing
        }

    best_domain = None
    best_fit = -1
    for name, data in by_domain.items():
        if data["fitScore"] > best_fit:
            best_fit = data["fitScore"]
            best_domain = name

    if not best_domain and domains:
        best_domain = domains[0]["name"]

    return {
        "domains": by_domain,
        "bestFitDomain": best_domain or "Data Science"
    }

def compute_confidence(ats_score: int, best_fit_score: int, detected_skills_count: int) -> int:
    signal = min(100, int(round((detected_skills_count / 30) * 100)))
    blended = int(round(ats_score * 0.55 + best_fit_score * 0.30 + signal * 0.15))
    return max(25, min(98, blended))

def compute_final_scorecard(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    ats_score = analysis_data["atsScore"]
    coverage = analysis_data["coverage"]
    impact = analysis_data["impact"]
    format_score = analysis_data["format"]
    best_fit = analysis_data["bestFit"]

    resume_score = ats_score

    return {
        "resumeScore": resume_score,
        "metrics": [
            {
                "key": "ats",
                "label": "ATS Score",
                "score": ats_score,
                "note": "Weighted overall ATS-style score."
            },
            {
                "key": "coverage",
                "label": "Keyword Coverage",
                "score": coverage,
                "note": "How much of the skills database you hit."
            },
            {
                "key": "impact",
                "label": "Impact Signals",
                "score": impact,
                "note": "Quantified outcomes and strong action verbs."
            },
            {
                "key": "format",
                "label": "Format & Structure",
                "score": format_score,
                "note": "Clear sections, contact details, and scannability."
            },
            {
                "key": "domain",
                "label": "Domain Fit",
                "score": best_fit,
                "note": "Match against the target skill map."
            }
        ]
    }

def analyze_resume_text(text_raw: str, jd_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    validation = validate_resume_structure(text_raw)
    if not validation["is_valid_resume"]:
        return {
            "is_valid_resume": False,
            "validation_reason": validation["validation_reason"],
            "ats": {
                "overallScore": 0,
                "keywordCoverage": 0,
                "sectionScores": {
                    "format": 0,
                    "experience": 0,
                    "skills": 0,
                    "education": 0,
                    "impact": 0
                },
                "missingTopKeywords": [],
                "atsScorecard": {
                    "overallAtsScore": 0,
                    "warnings": [validation["validation_reason"]]
                }
            },
            "skillsDetected": [],
            "domains": {},
            "bestFitDomain": "None",
            "confidence": 0,
            "finalScorecard": {
                "resumeScore": 0,
                "metrics": []
            }
        }

    detected_skills = extract_skills(text_raw)
    ats = compute_ats(text_raw, detected_skills, jd_data)
    domain_fits = compute_domain_fits(detected_skills)
    
    best_fit_domain = domain_fits["bestFitDomain"]
    best_fit_score = domain_fits["domains"].get(best_fit_domain, {}).get("fitScore", 0)

    confidence = compute_confidence(ats["overallScore"], best_fit_score, len(detected_skills))

    final_scorecard = compute_final_scorecard({
        "atsScore": ats["overallScore"],
        "coverage": ats["keywordCoverage"],
        "impact": ats["sectionScores"]["impact"],
        "format": ats["sectionScores"]["format"],
        "bestFit": best_fit_score
    })

    return {
        "is_valid_resume": True,
        "validation_reason": validation["validation_reason"],
        "ats": ats,
        "skillsDetected": detected_skills,
        "domains": domain_fits["domains"],
        "bestFitDomain": best_fit_domain,
        "confidence": confidence,
        "finalScorecard": final_scorecard
    }

