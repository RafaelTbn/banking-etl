import pytest
from etl.loader import load_csv, CSVFormatError

def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load_csv("not_found.csv")

def test_empty_row(tmp_path):
    f = tmp_path / "x.csv"
    f.write_text(
        "transaction_id,transaction_date,customer_id,account_id,amount,currency\n"
        "TXN0000001,2024-01-01,C1,A1,100,IDR\n"
        ",,,,,\n"
    )
    with pytest.raises(CSVFormatError):
        load_csv(str(f))

def test_wrong_column_count(tmp_path):
    f = tmp_path / "bad.csv"
    f.write_text(
        "transaction_id,transaction_date,customer_id\n"
        "TXN0000001,2024-01-01,C1\n"
    )
    with pytest.raises(CSVFormatError):
        load_csv(str(f))
