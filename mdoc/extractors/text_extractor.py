from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ExtractedText:
    text: str
    ok: bool
    error: str | None = None
    pages: int | None = None

def extract_text(path: Path) -> ExtractedText:
    suffix = path.suffix.lower()
    try:
        if suffix == ".txt":
            return ExtractedText(text=path.read_text(encoding="utf-8", errors="ignore"), ok=True)
        if suffix == ".docx":
            return _extract_docx(path)
        if suffix == ".pdf":
            return _extract_pdf(path)
        return ExtractedText(text="", ok=False, error=f"Unsupported file type: {suffix}")
    except Exception as e:
        return ExtractedText(text="", ok=False, error=str(e))

def _extract_docx(path: Path) -> ExtractedText:
    from docx import Document
    doc = Document(str(path))
    parts = [p.text for p in doc.paragraphs if p.text]
    return ExtractedText(text="\n".join(parts), ok=True)

def _extract_pdf(path: Path) -> ExtractedText:
    # Text-based PDFs only (no OCR)
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    texts = []
    for page in reader.pages:
        t = page.extract_text() or ""
        texts.append(t)
    return ExtractedText(text="\n".join(texts), ok=True, pages=len(reader.pages))
