"""PDF text extraction helpers used by the resume pipeline."""

import pdfplumber

def extract_text(pdf_path: str) -> str:
    """Extract all page text from a PDF file into a single string."""
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)
