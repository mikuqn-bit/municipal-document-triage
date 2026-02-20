from pathlib import Path
from mdoc.writers.registry_xlsx import append_row, RegistryRow

def test_append_row(tmp_path: Path):
    xlsx = tmp_path / "registry.xlsx"
    append_row(xlsx, RegistryRow(
        received_date="19.02.2026",
        doc_type="invoice",
        incoming_no="",
        invoice_no="INV-1",
        company_name="",
        sender="ACME",
        subject="Test",
        amount="10.00",
    ))
    assert xlsx.exists()
