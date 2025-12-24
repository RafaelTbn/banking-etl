import pytest

@pytest.fixture(autouse=True)
def auto_tmp(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path
