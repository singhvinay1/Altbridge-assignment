from io import BytesIO
from typing import Optional


def _extract_with_pdfplumber(data: bytes) -> Optional[str]:
    try:
        import pdfplumber  # type: ignore
    except Exception:
        return None

    try:
        text_chunks: list[str] = []
        with pdfplumber.open(BytesIO(data)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text_chunks.append(page_text)
        return "\n".join(text_chunks)
    except Exception:
        return None


def extract_text_from_pdf(data: bytes) -> str:
    text = _extract_with_pdfplumber(data)
    if text:
        return text
    # Fallback: return empty string to avoid crashing
    return ""



