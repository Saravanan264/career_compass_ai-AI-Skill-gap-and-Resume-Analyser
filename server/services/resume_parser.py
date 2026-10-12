import fitz  # PyMuPDF
import re
from fastapi import HTTPException, status

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extracts text from raw PDF bytes using PyMuPDF.
    Handles empty, encrypted, corrupted, or scanned/image-only PDFs.
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Corrupted or invalid PDF file: {str(e)}"
        )

    if doc.is_encrypted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password-protected PDF files are not supported."
        )

    if doc.page_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded PDF contains no pages."
        )

    extracted_pages = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        if text:
            extracted_pages.append(text)

    doc.close()

    full_text = "\n".join(extracted_pages).strip()

    if not full_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract text from PDF. The file may be image-only or scanned without OCR text."
        )

    return clean_resume_text(full_text)

def clean_resume_text(text: str) -> str:
    """
    Normalizes whitespace while preserving section breaks and technical details.
    """
    # Replace non-standard whitespace characters with regular spaces
    text = re.sub(r'[\r\t\f\v]', ' ', text)
    # Replace multiple consecutive blank lines with double newline
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    # Replace multiple horizontal spaces with single space
    lines = [re.sub(r' +', ' ', line).strip() for line in text.split('\n')]
    return '\n'.join(lines).strip()

def validate_resume_structure(text_raw: str) -> dict:
    """
    Validates whether the extracted text represents a valid resume.
    Prevents non-resume documents (reports, papers, assignments, syllabus, blank PDFs, etc.)
    from being classified or scored as resumes.
    """
    if not text_raw or not text_raw.strip():
        return {
            "is_valid_resume": False,
            "resume_confidence": 0,
            "validation_reason": "This document does not appear to be a valid resume. Please upload a resume containing candidate details, skills, education, experience, projects, or other resume sections.",
            "checks": {
                "has_minimum_length": False,
                "has_contact_info": False,
                "has_resume_sections": False,
                "has_content_signals": False
            }
        }

    text_norm = text_raw.lower()
    text_norm = re.sub(r'[^a-z0-9+.#\s-]', ' ', text_norm)
    text_norm = re.sub(r'\s+', ' ', text_norm).strip()
    
    char_len = len(text_raw.strip())
    words = re.findall(r'\b[a-zA-Z]{2,}\b', text_raw)
    word_count = len(words)

    # 1. Minimum meaningful text length
    has_minimum_length = char_len >= 150 and word_count >= 25

    # 2. Presence of candidate contact information
    has_email = bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text_raw))
    has_phone = bool(re.search(r'\b(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b|\b\d{10}\b', text_raw))
    has_profile_links = any(k in text_norm for k in ["linkedin", "github", "portfolio", "address", "location"])
    has_contact_info = has_email or has_phone or has_profile_links

    # 3. Presence of standard resume section headers
    section_patterns = [
        r'\b(?:work\s+)?experience\b', r'\bemployment\b', r'\bwork\s+history\b', r'\bcareer\s+history\b',
        r'\beducation\b', r'\bacademic\s+(?:background|history|qualification)\b', r'\bdegree\b',
        r'\bskills\b', r'\btechnical\s+skills\b', r'\bcore\s+competencies\b', r'\bproficiencies\b',
        r'\bprojects\b', r'\bpersonal\s+projects\b', r'\bkey\s+projects\b',
        r'\bsummary\b', r'\bexecutive\s+summary\b', r'\bprofessional\s+summary\b', r'\bcareer\s+objective\b', r'\bprofile\b',
        r'\bcertifications?\b', r'\baccomplishments?\b', r'\bachievements?\b'
    ]
    sections_matched = sum(1 for p in section_patterns if re.search(p, text_norm))
    has_resume_sections = sections_matched >= 2

    # 4. Presence of resume-like content / candidate signals
    role_terms = ["developer", "engineer", "analyst", "architect", "manager", "specialist", "intern", "consultant", "lead", "designer", "administrator"]
    edu_terms = ["bachelor", "master", "degree", "university", "college", "institute", "b.tech", "b.e", "b.sc", "m.tech", "m.sc", "phd", "gpa"]
    content_signal_count = sum(1 for t in role_terms + edu_terms if t in text_norm)
    has_content_signals = content_signal_count >= 2

    # A valid resume MUST have minimum length AND (contact info OR at least 2 resume sections OR content signals with at least 1 section/contact)
    is_valid = has_minimum_length and (
        (has_contact_info and has_resume_sections) or
        (has_resume_sections and has_content_signals) or
        (has_contact_info and has_content_signals and sections_matched >= 1)
    )

    confidence = 0
    if is_valid:
        confidence = 50
        if has_contact_info: confidence += 20
        if has_resume_sections: confidence += 20
        if has_content_signals: confidence += 10
        confidence = min(98, confidence)

    reason = "Valid resume document detected." if is_valid else "This document does not appear to be a valid resume. Please upload a resume containing candidate details, skills, education, experience, projects, or other resume sections."

    return {
        "is_valid_resume": is_valid,
        "resume_confidence": confidence,
        "validation_reason": reason,
        "checks": {
            "has_minimum_length": has_minimum_length,
            "has_contact_info": has_contact_info,
            "has_resume_sections": has_resume_sections,
            "has_content_signals": has_content_signals
        }
    }

