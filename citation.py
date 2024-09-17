from typing import List
import re

def extract_citations(text: str) -> List[dict]:
    # Simple regex-based citation extraction
    citations = re.findall(r'\((?:[^()]*\d{4}[^()]*)\)', text)
    
    # Convert extracted citations to a list of dictionaries
    return [{"raw": citation} for citation in citations]

def format_citation(citation: dict, style: str = 'apa') -> str:
    raw_citation = citation.get("raw", "")
    
    if style.lower() == 'apa':
        return f"APA Style: {raw_citation}"
    elif style.lower() == 'mla':
        return f"MLA Style: {raw_citation}"
    elif style.lower() == 'chicago':
        return f"Chicago Style: {raw_citation}"
    else:
        return f"Unknown Style: {raw_citation}"
