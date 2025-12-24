from datetime import datetime

def _try_date(s):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except:
            continue
    return None

def clean_record(r: dict) -> dict:
    for k, v in r.items():
        # trim whitespace
        if isinstance(v, str):
            r[k] = v.strip()
        # ubah empty string -> None
        if r[k] == "":
            r[k] = None

    # normalisasi tanggal
    td = r.get("transaction_date")
    if td:
        d = _try_date(td)
        if d:
            r["transaction_date"] = d.strftime("%Y-%m-%d")

    # normalisasi currency
    if r.get("currency"):
        c = r["currency"].upper()
        if c in ("IDR", "USD", "SGD"):
            r["currency"] = c
        else:
            r["currency"] = None

    # convert numeric
    for num in ("amount", "risk_score", "is_fraud_suspected"):
        val = r.get(num)
        if val is None:
            continue
        try:
            r[num] = float(val)
        except:
            r[num] = None

    # imputasi merchant_category
    if not r.get("merchant_category"):
        r["merchant_category"] = "UNKNOWN"

    return r
