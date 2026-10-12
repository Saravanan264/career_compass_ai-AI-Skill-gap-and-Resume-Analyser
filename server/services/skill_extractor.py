import json
import re
from pathlib import Path
from typing import List, Dict, Any

DATA_DIR = Path(__file__).parent.parent / "data"

def load_skills_db() -> List[Dict[str, Any]]:
    skills_file = DATA_DIR / "skills.json"
    with open(skills_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("skills", [])

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9+.#\s-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def matches_keyword(normalized_kw: str, text_normalized: str) -> bool:
    if not normalized_kw or not text_normalized:
        return False
    escaped_kw = re.escape(normalized_kw)
    pattern = r'(?<![a-z0-9])' + escaped_kw + r'(?![a-z0-9])'
    return bool(re.search(pattern, text_normalized))

def get_canonical_skill_name(skill_name: str) -> str:
    if not skill_name or not skill_name.strip():
        return ""
    
    explicit_aliases = {
        "reactjs": "React",
        "react.js": "React",
        "react js": "React",
        "react": "React",
        "nodejs": "Node.js",
        "node.js": "Node.js",
        "node js": "Node.js",
        "node": "Node.js",
        "restful api": "REST API",
        "rest api": "REST API",
        "rest apis": "REST API",
        "restful apis": "REST API",
        "restfulapi": "REST API",
        "restapi": "REST API",
        "restapis": "REST API",
        "python 3": "Python",
        "python3": "Python",
        "python": "Python",
        "sql database": "SQL",
        "sqldatabase": "SQL",
        "sql": "SQL",
        "javascript": "JavaScript",
        "js": "JavaScript",
    }
    
    lowered = skill_name.strip().lower()
    if lowered in explicit_aliases:
        return explicit_aliases[lowered]
        
    norm = normalize_text(skill_name)
    clean_key = re.sub(r'[^a-z0-9+#]', '', norm)
    
    if clean_key in explicit_aliases:
        return explicit_aliases[clean_key]

    all_skills = load_skills_db()
    for s in all_skills:
        canonical = s["name"]
        keywords = [canonical] + s.get("aliases", []) + s.get("keywords", [])
        for kw in keywords:
            kw_norm = normalize_text(kw)
            kw_clean = re.sub(r'[^a-z0-9+#]', '', kw_norm)
            if kw_norm == norm or kw_clean == clean_key:
                return canonical
    for s in all_skills:
        canonical = s["name"]
        keywords = [canonical] + s.get("aliases", []) + s.get("keywords", [])
        for kw in keywords:
            kw_clean = re.sub(r'[^a-z0-9+#]', '', normalize_text(kw))
            if len(kw_clean) >= 3 and (clean_key in kw_clean or kw_clean in clean_key):
                return canonical
    return skill_name.strip()

def extract_skills(text_raw: str) -> List[str]:
    text = normalize_text(text_raw)
    all_skills = load_skills_db()
    
    detected = []
    for skill in all_skills:
        name = skill["name"]
        keywords = [name] + skill.get("aliases", []) + skill.get("keywords", [])
        
        hit = False
        for kw in keywords:
            normalized_kw = normalize_text(kw)
            if matches_keyword(normalized_kw, text):
                hit = True
                break
        
        if hit:
            detected.append(name)
            
    # Unique and sorted alphabetically
    return sorted(list(set(detected)))

