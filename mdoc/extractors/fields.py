from __future__ import annotations
from dataclasses import dataclass
import re
from .text_extractor import ExtractedText
from ..utils import clean_whitespace

@dataclass
class ExtractedFields:
    incoming_no: str | None = None
    invoice_no: str | None = None
    sender: str | None = None
    subject: str | None = None
    amount: str | None = None

IBAN_RE = re.compile(r"\bBG\d{2}[A-Z]{4}\d{14}\b")
EIK_RE = re.compile(r"\b\d{9,13}\b")
INCOMING_RE = re.compile(r"(вх\.?\s*№\s*([\w\-\/]+))", re.IGNORECASE)
INVOICE_NO_RE = re.compile(r"(фактура\s*№\s*([\w\-\/]+)|invoice\s*no\.?\s*([\w\-\/]+))", re.IGNORECASE)
AMOUNT_RE = re.compile(r"(общо\s*[:\-]?\s*([0-9]+(?:[\.,][0-9]{2})?)\s*(лв\.?|bgn|eur)?)", re.IGNORECASE)

def extract_fields(ex: ExtractedText) -> ExtractedFields:
    txt = ex.text or ""
    fields = ExtractedFields()

    m = INCOMING_RE.search(txt)
    if m:
        fields.incoming_no = clean_whitespace(m.group(2))

    m = INVOICE_NO_RE.search(txt)
    if m:
        fields.invoice_no = clean_whitespace(m.group(2) or m.group(3) or "")

    m = AMOUNT_RE.search(txt)
    if m:
        fields.amount = clean_whitespace(m.group(2))

    # crude subject: first line containing "Относно" else first non-empty line
    subj = None
    for line in txt.splitlines():
        l = line.strip()
        if not l:
            continue
        if re.search(r"Относно\s*[:\-]", l, flags=re.IGNORECASE):
            subj = re.sub(r"(?i)относно\s*[:\-]\s*", "", l).strip()
            break
        if subj is None:
            subj = l
    if subj:
        fields.subject = clean_whitespace(subj)[:180]

    # sender heuristic: look for "От:" line
    sender = None
    for line in txt.splitlines()[:30]:
        l = line.strip()
        if re.search(r"^(От|From)\s*[:\-]", l, flags=re.IGNORECASE):
            sender = re.sub(r"(?i)^(от|from)\s*[:\-]\s*", "", l).strip()
            break
    if sender:
        fields.sender = clean_whitespace(sender)[:180]

    return fields
