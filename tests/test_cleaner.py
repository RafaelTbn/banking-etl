from etl.cleaner import clean_record

def test_whitespace_trimming():
    r = {"transaction_id": " TXN0000001 "}
    out = clean_record(r)
    assert out["transaction_id"] == "TXN0000001"

def test_date_normalization():
    r = {"transaction_date": "01/01/2024"}
    out = clean_record(r)
    assert out["transaction_date"] == "2024-01-01"

def test_missing_merchant_category():
    r = {"merchant_category": None}
    out = clean_record(r)
    assert out["merchant_category"] == "UNKNOWN"
