from mdoc.classifiers.rules import classify

def test_invoice():
    c = classify("ФАКТУРА № 123 ДДС IBAN BG11AAAA12345678901234")
    assert c.doc_type == "invoice"

def test_complaint():
    c = classify("Подавам жалба за нерегламентирано депониране. Моля за проверка.")
    assert c.doc_type == "complaint"

def test_unknown():
    c = classify("random text with nothing relevant")
    assert c.doc_type in ("unknown", "letter")
