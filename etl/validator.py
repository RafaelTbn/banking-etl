import re
from datetime import datetime

class ValidationError(Exception):
    pass

ALLOWED_CURRENCIES = {"IDR", "USD", "SGD"}
ALLOWED_DIRECTIONS = {"DEBIT", "CREDIT"}
ALLOWED_ACCOUNT_TYPES = {"SAVINGS", "CURRENT", "CREDIT_CARD", "LOAN"}

def _parse_date(s: str):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except:
            continue
    raise ValueError("Invalid date format")

def validate_record(rec: dict) -> bool:
    mandatory = [
        "transaction_id","transaction_date",
        "customer_id","account_id",
        "amount","currency"
    ]

    # cek mandatory field
    for m in mandatory:
        if rec.get(m) in (None, ""):
            raise ValidationError(f"Missing field: {m}")

    # cek pola transaction_id
    if not re.match(r"^TXN\d{7}$", rec["transaction_id"]):
        raise ValidationError("Invalid transaction_id pattern")

    # cek tanggal
    try:
        _ = _parse_date(rec["transaction_date"])
    except ValueError:
        raise ValidationError("Invalid date format")

    # cek amount
    try:
        amt = float(rec["amount"])
    except:
        raise ValidationError("Amount not numeric")
    if amt < 0:
        raise ValidationError("Amount cannot be negative")
    if amt > 10_000_000:
        raise ValidationError("Amount exceeds anomaly threshold (>10M IDR)")

    # cek currency
    if rec["currency"] not in ALLOWED_CURRENCIES:
        raise ValidationError("Invalid currency")

    # cek direction
    if rec.get("direction") not in ALLOWED_DIRECTIONS:
        raise ValidationError("Invalid direction")

    # cek account type
    if rec.get("account_type") not in ALLOWED_ACCOUNT_TYPES:
        raise ValidationError("Invalid account type")

    return True
