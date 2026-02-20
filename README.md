# Municipal Document Triage Assistant (mdoc)

Python CLI tool for triaging municipal documents (invoices, letters, complaints):
- Extracts text from PDF/DOCX/TXT
- Classifies document type (rules-based)
- Extracts key fields (invoice no, sender, amount, incoming number, subject)
- Appends a row to an **Excel registry (.xlsx)** using your schema
- Generates drafts and short summaries
- Writes an audit log (JSONL)

## Quick start

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt

python -m mdoc ingest --inbox inbox --out out --registry registry.xlsx
pytest -q
```

## CLI

- `ingest`: process all files in inbox folder (dedup by hash)
- Outputs:
  - `out/registry.xlsx` (appends rows)
  - `out/drafts/*.txt`
  - `out/summaries/*.md`
  - `out/logs/processing_log.jsonl`

## Notes
- OCR for scanned PDFs is intentionally not included in MVP (admin rights / binaries).
