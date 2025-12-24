from etl.transformer import transform_record

def test_derived_features():
    r = {
        "transaction_date": "2024-01-01",
        "amount": 6000000,
        "currency": "USD"
    }
    out = transform_record(r)
    assert out["is_large_transaction"] is True
    assert out["is_crossborder"] is True
    assert out["transaction_day"] == "Monday"

def test_type_conversion():
    r = {
        "transaction_date": "2024-01-01",
        "amount": "1000",
        "currency": "IDR"
    }
    out = transform_record(r)
    assert isinstance(out["amount"], float)
