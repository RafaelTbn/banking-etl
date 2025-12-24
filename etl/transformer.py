from datetime import datetime
import math

def transform_record(r: dict) -> dict:
    out = r.copy()

    # date
    try:
        out["transaction_date"] = datetime.strptime(
            out["transaction_date"], "%Y-%m-%d"
        ).date()
    except Exception:
        out["transaction_date"] = None

    # amount
    try:
        out["amount"] = float(out["amount"])
    except Exception:
        out["amount"] = None

    amt = out["amount"]

    out["is_large_transaction"] = amt is not None and amt > 5_000_000
    out["is_crossborder"] = out.get("currency") not in (None, "IDR")

    if amt is not None and amt > 0:
        out["amount_log"] = math.log(amt)
    else:
        out["amount_log"] = None

    if out["transaction_date"]:
        out["transaction_day"] = out["transaction_date"].strftime("%A")
    else:
        out["transaction_day"] = None

    return out
