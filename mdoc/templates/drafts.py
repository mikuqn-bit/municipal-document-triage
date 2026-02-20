from __future__ import annotations
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class DraftContext:
    doc_type: str
    sender: str | None
    subject: str | None
    incoming_no: str | None
    invoice_no: str | None
    amount: str | None

def make_draft(ctx: DraftContext) -> str:
    today = date.today().strftime("%d.%m.%Y")
    if ctx.doc_type == "invoice":
        return (
            f"СЛУЖЕБНА БЕЛЕЖКА\n"
            f"Дата: {today}\n\n"
            f"Получен е документ: Фактура № {ctx.invoice_no or '—'}\n"
            f"Доставчик/подател: {ctx.sender or '—'}\n"
            f"Сума: {ctx.amount or '—'}\n\n"
            f"Действие: Да се предаде за счетоводна обработка и проверка по договор/основание.\n"
        )
    if ctx.doc_type == "complaint":
        return (
            f"ОТГОВОР (чернова)\n"
            f"Дата: {today}\n\n"
            f"Относно: {ctx.subject or '—'}\n"
            f"Вх. №: {ctx.incoming_no or '—'}\n\n"
            f"Уважаеми/а {ctx.sender or 'гражданин'},\n"
            f"Потвърждаваме получаването на Вашия сигнал/жалба. Ще бъде извършена проверка и ще бъдете уведомени за резултата в законоустановения срок.\n"
        )
    return (
        f"ПИСМО (чернова)\n"
        f"Дата: {today}\n\n"
        f"Относно: {ctx.subject or '—'}\n"
        f"Вх. №: {ctx.incoming_no or '—'}\n\n"
        f"Уважаеми госпожи/господа,\n"
        f"Потвърждаваме получаването на Вашето писмо. При необходимост ще изискаме допълнителни данни.\n"
    )
