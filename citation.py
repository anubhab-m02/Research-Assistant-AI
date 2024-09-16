import re
from typing import List

def extract_citations(text: str) -> List[str]:
    # Simple regex-based citation extraction
    # This pattern looks for parentheses containing a year
    citations = re.findall(r'\((?:[^()]*\d{4}[^()]*)\)', text)
    return citations

def format_citation(citation: str, style: str = 'APA') -> str:
    # Simple formatting function
    # Note: This is a basic implementation and doesn't follow strict citation rules
    if style == 'APA':
        return f"APA style: {citation}"
    elif style == 'MLA':
        return f"MLA style: {citation}"
    elif style == 'Chicago':
        return f"Chicago style: {citation}"
    else:
        return citation
