from __future__ import annotations
from pathlib import Path
from datetime import date
from .cli import IngestConfig
from .utils import file_sha256
from .extractors.text_extractor import extract_text
from .classifiers.rules import classify
from .extractors.fields import extract_fields
from .templates.drafts import DraftContext, make_draft
from .writers.registry_xlsx import RegistryRow, append_row
from .writers.audit_log import log_event

SUPPORTED = {".pdf", ".docx", ".txt"}


def run_ingest(cfg: IngestConfig) -> None:
    cfg.out.mkdir(parents=True, exist_ok=True)
    (cfg.out / "drafts").mkdir(parents=True, exist_ok=True)
    (cfg.out / "summaries").mkdir(parents=True, exist_ok=True)
    (cfg.out / "logs").mkdir(parents=True, exist_ok=True)

    seen_hashes = _load_seen_hashes(cfg.out / "logs" / "seen_hashes.txt")

    for path in sorted(cfg.inbox.glob("*")):
        if path.suffix.lower() not in SUPPORTED:
            continue

        h = file_sha256(path)
        if h in seen_hashes:
            continue

        ex = extract_text(path)
        cls = classify(ex.text if ex.ok else "")
        fields = extract_fields(ex) if ex.ok else None

        row = RegistryRow(
            received_date=date.today().strftime("%d.%m.%Y"),
            doc_type=cls.doc_type,
            incoming_no=getattr(fields, "incoming_no", None) if fields else None,
            invoice_no=getattr(fields, "invoice_no", None) if fields else None,
            party=getattr(fields, "sender", None) if fields else None,
            subject=getattr(fields, "subject", None) if fields else None,
            amount=getattr(fields, "amount", None) if fields else None,
            currency="BGN",
            status="Нов",
            notes=None,
        )

        append_row(cfg.registry, row)

        draft = make_draft(
            DraftContext(
                doc_type=cls.doc_type,
                sender=row.party,
                subject=row.subject,
                incoming_no=row.incoming_no,
                invoice_no=row.invoice_no,
                amount=row.amount,
            )
        )

        (cfg.out / "drafts" / f"{path.stem}.txt").write_text(draft, encoding="utf-8")

        summary = _make_summary(path.name, cls, row, ex)
        (cfg.out / "summaries" / f"{path.stem}.md").write_text(summary, encoding="utf-8")

        log_event(
            cfg.out / "logs" / "processing_log.jsonl",
            {
                "file": path.name,
                "sha256": h,
                "ok": ex.ok,
                "error": ex.error,
                "doc_type": cls.doc_type,
                "score": cls.score,
                "rationale": cls.rationale,
            },
        )

        _mark_seen(cfg.out / "logs" / "seen_hashes.txt", h)
        seen_hashes.add(h)


def _make_summary(filename: str, cls, row, ex) -> str:
    return "\n".join(
        [
            f"# Summary: {filename}",
            f"- Type: {cls.doc_type}",
            f"- Incoming №: {row.incoming_no or '—'}",
            f"- Invoice №: {row.invoice_no or '—'}",
            f"- Party: {row.party or '—'}",
            f"- Subject: {row.subject or '—'}",
            f"- Amount: {row.amount or '—'}",
        ]
    )


def _load_seen_hashes(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return set(
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )


def _mark_seen(path: Path, h: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(h + "\n")
