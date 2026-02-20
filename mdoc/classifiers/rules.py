from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
import re

DocType = Literal["invoice", "letter", "complaint", "unknown"]

@dataclass(frozen=True)
class Classification:
    doc_type: DocType
    score: int
    rationale: str

INVOICE_PATTERNS = [
    (r"\bФАКТУРА\b", 6),
    (r"\bINVOICE\b", 6),
    (r"\bДДС\b", 3),
    (r"\bVAT\b", 3),
    (r"\bIBAN\b", 3),
    (r"\bЕИК\b", 2),
]
COMPLAINT_PATTERNS = [
    (r"\bжалб", 6),
    (r"\bсигнал\b", 5),
    (r"\bнерегламентиран", 4),
    (r"\bмоля\b", 2),
]
LETTER_PATTERNS = [
    (r"Уважаеми", 4),
    (r"Относно", 3),
    (r"изх\.?\s*№", 3),
    (r"вх\.?\s*№", 3),
]

def classify(text: str) -> Classification:
    t = text or ""
    inv = _score(t, INVOICE_PATTERNS)
    comp = _score(t, COMPLAINT_PATTERNS)
    let = _score(t, LETTER_PATTERNS)

    best = max([("invoice", inv), ("complaint", comp), ("letter", let)], key=lambda x: x[1])
    doc_type, score = best
    if score <= 2:
        return Classification(doc_type="unknown", score=score, rationale=f"Low confidence: inv={inv}, comp={comp}, let={let}")
    return Classification(doc_type=doc_type, score=score, rationale=f"inv={inv}, comp={comp}, let={let}")

def _score(text: str, patterns: list[tuple[str, int]]) -> int:
    s = 0
    for pat, w in patterns:
        if re.search(pat, text, flags=re.IGNORECASE):
            s += w
    return s
