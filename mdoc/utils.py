from __future__ import annotations
import hashlib
from pathlib import Path
from datetime import datetime
import re

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def clean_whitespace(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()
