import pytest
from etl.validator import validate_record, ValidationError

def base():
    return {
        "transaction_id": "TXN0000001",
        "transaction_date": "2024-01-01",
        "customer_id": "C1",
        "account_id": "A1",
        "amount": "1000",
        "currency": "IDR",
    }

def test_negative_amount():
    r = base()
    r["amount"] = "-5"
    with pytest.raises(ValidationError):
        validate_record(r)

def test_invalid_currency():
    r = base()
    r["currency"] = "ABC"
    with pytest.raises(ValidationError):
        validate_record(r)

def test_wrong_transaction_id_pattern():
    r = base()
    r["transaction_id"] = "ABC123"
    with pytest.raises(ValidationError):
        validate_record(r)

def test_invalid_date_format():
    r = base()
    r["transaction_date"] = "99-99-9999"
    with pytest.raises(ValidationError):
        validate_record(r)
