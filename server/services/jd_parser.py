import re

def clean_jd_text(text: str) -> str:
    """
    Cleans and normalizes job description text while preserving
    technical terms, experience mentions, and section boundaries.
    """
    if not text:
        return ""
    
    # Replace non-standard whitespace characters with regular spaces
    cleaned = re.sub(r'[\r\t\f\v]', ' ', text)
    # Replace multiple consecutive blank lines with double newline
    cleaned = re.sub(r'\n\s*\n+', '\n\n', cleaned)
    # Replace multiple horizontal spaces with single space
    lines = [re.sub(r' +', ' ', line).strip() for line in cleaned.split('\n')]
    return '\n'.join(lines).strip()
