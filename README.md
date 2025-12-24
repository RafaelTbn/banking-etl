﻿# Banking ETL Assessment

## Ringkasan
Proyek kecil ini adalah contoh mini ETL (Extract, Transform, Load) untuk transaksi perbankan. Selain pipeline ETL sederhana, terdapat modul utilitas untuk pemanggilan API asinkron dan suite pengujian menggunakan `pytest`.

Struktur proyek:

```
banking_etl_assessment/
├── README.md
├── data/
│   └── banking_transactions.csv
├── etl/
│   ├── __init__.py
│   ├── loader.py
│   ├── validator.py
│   ├── cleaner.py
│   └── transformer.py
├── utils/
│   ├── __init__.py
│   └── async_api.py
└── tests/
                ├── conftest.py
                ├── test_cleaner.py
                ├── test_loader.py
                ├── test_transformer.py
                ├── test_utils.py
                └── test_validator.py
```

## Alur ETL
- Loader (`etl/loader.py`): membaca file CSV dan mengembalikan list of dict. Memeriksa header, mendeteksi baris kosong, dan jumlah kolom yang salah. Melempar `CSVFormatError` bila format CSV bermasalah.
- Cleaner (`etl/cleaner.py`): membersihkan data dengan menghapus spasi, menormalkan tanggal ke format `YYYY-MM-DD`, mengubah huruf currency menjadi uppercase dan memvalidasinya, mengonversi field numerik, serta mengisi `merchant_category` jika kosong.
- Validator (`etl/validator.py`): menerapkan aturan validasi spesifik perbankan (lihat bagian aturan) dan melempar `ValidationError` bila data tidak valid.
- Transformer (`etl/transformer.py`): mengonversi tipe data (mis. tanggal ke `datetime.date`, amount ke `float`) dan menghasilkan fitur turunan seperti `is_large_transaction`, `is_crossborder`, `transaction_day`, dan `amount_log`.

## Aturan Validasi (Banking)
- Field wajib: `transaction_id`, `transaction_date`, `customer_id`, `account_id`, `amount`, `currency`.
- `transaction_id`: harus mengikuti pola `TXNxxxxxxx` (7 digit setelah `TXN`).
- `transaction_date`: menerima format `YYYY-MM-DD` dan `DD/MM/YYYY`.
- `amount`: harus numerik, tidak boleh negatif, dan tidak boleh melebihi `10_000_000` (batas anomali).
- `currency`: hanya `IDR`, `USD`, `SGD` yang dianggap valid.
- `direction`: harus `DEBIT` atau `CREDIT`.
- `account_type`: harus salah satu `SAVINGS`, `CURRENT`, `CREDIT_CARD`, `LOAN`.

## Cara Menjalankan ETL (contoh penggunaan)
1. (Opsional) Install project secara editable agar package `etl` dapat diimpor dari mana saja:
```powershell
cd 'D:\Jatis Mobile\banking_etl_assessment'
pip install -e .
```
2. Contoh penggunaan interaktif (Python):
```python
from etl.loader import load_csv
from etl.cleaner import clean_record
from etl.validator import validate_record
from etl.transformer import transform_record

rows = load_csv('data/banking_transactions.csv')
for r in rows:
        c = clean_record(r)
        validate_record(c)
        t = transform_record(c)
        # proses hasil t
```

## Setup environment dan Menjalankan Test (Windows PowerShell)
Ikuti langkah-langkah ini setelah membuka folder proyek di VS Code atau terminal:

1. Buat virtual environment dan aktifkan:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
(untuk macOS/Linux: `python -m venv .venv` lalu `source .venv/bin/activate`)

2. Upgrade pip dan pasang dependensi (paket minimal sudah ada di `requirements.txt`):
```powershell
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
```

3. (Direkomendasikan) Install package secara editable supaya modul `etl` dapat diimport:
```powershell
python -m pip install -e .
```

4. Jalankan seluruh test:
```powershell
python -m pytest -q
```

5. Menjalankan dengan detail per-test:
```powershell
python -m pytest -v
```

6. Menjalankan satu file test:
```powershell
python -m pytest tests/test_cleaner.py -q
```

7. Menjalankan satu fungsi test:
```powershell
python -m pytest tests/test_cleaner.py::test_cleaner -q
```

8. Menjalankan test dan lihat output print/log (non-captured):
```powershell
python -m pytest -s -v
```

Catatan:
- Test async membutuhkan plugin `pytest-asyncio` (termasuk di `requirements.txt`).
- Jangan commit folder `.venv/` atau `.pytest_cache/` ke repository; tambahkan `.gitignore`.

## Utilities
- `utils/async_api.py` berisi implementasi `fetch_quote(symbol)` menggunakan `aiohttp` dengan mekanisme retry dan timeout.

## Perbaikan yang Disarankan
- Tambahkan CI (mis. GitHub Actions) untuk menjalankan test otomatis pada push/PR.
- Tambahkan contoh file CSV sampel atau dokumentasi header kolom di `data/`.

## Cara Submit
- Kamu bisa mengemas folder menjadi ZIP atau mem-push repository ke GitHub. Pastikan `README.md` dan `tests/` termasuk, dan jangan sertakan `.venv/`.

# Banking ETL Assessment

## Overview Project

Project ini adalah **mini ETL (Extract, Transform, Load) pipeline** yang dirancang khusus untuk memproses data transaksi perbankan. Project ini mendemonstrasikan praktik data engineering yang production-ready, mencakup validasi data, pembersihan, transformasi, dan integrasi API asynchronous.

Tujuan utama project ini adalah sebagai **persiapan hands-on untuk product development** yang lebih kompleks seperti pembangunan RAG (Retrieval-Augmented Generation) dan agentic systems di bidang financial services.

## Struktur Project

```
banking_etl_assessment/
├── README.md
├── data/
│   └── banking_transactions.csv      # Sample data transaksi
├── etl/
│   ├── __init__.py
│   ├── loader.py                     # Load CSV dengan deteksi error
│   ├── validator.py                  # Validasi banking rules
│   ├── cleaner.py                    # Cleaning & normalisasi data
│   └── transformer.py                # Feature engineering & konversi tipe
├── utils/
│   ├── __init__.py
│   └── async_api.py                  # Async API caller dengan retry
└── tests/
    ├── conftest.py                   # Pytest configuration
    ├── test_loader.py                # Unit test loader
    ├── test_validator.py             # Unit test validator
    ├── test_cleaner.py               # Unit test cleaner
    ├── test_transformer.py           # Unit test transformer
    └── test_utils.py                 # Unit test async API
```

## ETL Flow Explanation

Pipeline ETL berjalan dalam 4 tahap berurutan:

```
┌─────────────────┐
│  1. LOADER      │  → Membaca CSV dan deteksi error struktural
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. VALIDATOR   │  → Validasi business rules perbankan
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. CLEANER     │  → Normalisasi dan cleaning data
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. TRANSFORMER │  → Konversi tipe & feature engineering
└────────┬────────┘
         │
         ▼
    [Clean Data]
```

### 1. Loader (`etl/loader.py`)

**Fungsi utama:** `load_csv(path: str) -> list[dict]`

**Tugas:**
- Membaca file CSV menjadi list of dictionaries
- Mendeteksi error struktural:
  - ✓ Empty rows (baris kosong)
  - ✓ Wrong column count (jumlah kolom tidak konsisten)
  - ✓ Missing mandatory columns (kolom wajib hilang)
- Logging setiap operasi
- Raise `CSVFormatError` jika ditemukan error

**Mandatory Columns:**
- `transaction_id`
- `transaction_date`
- `customer_id`
- `account_id`
- `amount`
- `currency`

### 2. Validator (`etl/validator.py`)

**Fungsi utama:** `validate_record(rec: dict) -> bool`

**Banking Validation Rules:**

| Field | Aturan Validasi | Contoh Valid | Contoh Invalid |
|-------|----------------|--------------|----------------|
| `transaction_id` | Pattern: `TXN` + 7 digit angka | `TXN0000001` | `ABC123`, `TXN123` |
| `transaction_date` | Format: `YYYY-MM-DD` atau `DD/MM/YYYY` | `2024-01-01`, `01/01/2024` | `99-99-9999` |
| `amount` | Harus positif, ≤ 10,000,000 IDR | `5000000` | `-100`, `15000000` |
| `currency` | Harus: IDR, USD, atau SGD | `IDR`, `USD` | `RP`, `XXX`, `ABC` |
| `direction` | Harus: DEBIT atau CREDIT | `DEBIT` | `IN`, `OUT` |
| `account_type` | SAVINGS, CURRENT, CREDIT_CARD, LOAN | `SAVINGS` | `CHECKING` |

**Exception:**
- Raise `ValidationError` jika ada rule yang dilanggar

### 3. Cleaner (`etl/cleaner.py`)

**Fungsi utama:** `clean_record(r: dict) -> dict`

**Operasi cleaning:**

1. **Whitespace Trimming**
   - Menghilangkan spasi di awal/akhir semua string
   - Contoh: `" TXN0000001 "` → `"TXN0000001"`

2. **Date Normalization**
   - Mengubah semua format tanggal ke `YYYY-MM-DD`
   - Support format: `DD/MM/YYYY` dan `YYYY-MM-DD`
   - Contoh: `"01/01/2024"` → `"2024-01-01"`

3. **Currency Normalization**
   - Uppercase dan validasi
   - Invalid currency → `None`
   - Contoh: `"idr"` → `"IDR"`, `"XXX"` → `None`

4. **Numeric Conversion**
   - Convert `amount`, `risk_score` ke float
   - Gagal convert → `None`

5. **Missing Value Imputation**
   - `merchant_category` kosong → `"UNKNOWN"`

### 4. Transformer (`etl/transformer.py`)

**Fungsi utama:** `transform_record(r: dict) -> dict`

**A. Type Conversion:**

| Field | Tipe Awal | Tipe Akhir |
|-------|-----------|------------|
| `transaction_date` | `str` | `datetime.date` |
| `amount` | `str` | `float` |
| `risk_score` | `str` | `float` atau `None` |

**B. Derived Features:**

| Feature Baru | Logika | Contoh |
|--------------|--------|--------|
| `is_large_transaction` | `amount > 5,000,000` | `True` jika amount = 6M |
| `is_crossborder` | `currency != "IDR"` | `True` jika currency = USD |
| `transaction_day` | Day of week dari date | `"Monday"`, `"Tuesday"` |
| `amount_log` | `log(amount)` | `15.90` untuk amount = 8M |

**Kegunaan derived features:**
- `is_large_transaction`: Flagging transaksi besar untuk review
- `is_crossborder`: Identifikasi transaksi lintas negara
- `transaction_day`: Analisis pola transaksi per hari
- `amount_log`: Normalisasi distribusi skewed untuk ML

## Utilities - Async API Caller

### `utils/async_api.py`

**Fungsi utama:** `async def fetch_quote(symbol: str) -> dict`

**Fitur:**
- ✓ Menggunakan `aiohttp` untuk async HTTP requests
- ✓ Retry logic otomatis saat request gagal
- ✓ Timeout handling untuk mencegah hanging
- ✓ Mock endpoint: `https://dummyjson.com/quotes/random`

**Use Case:**
Dapat dikembangkan untuk fetch data eksternal seperti:
- Real-time exchange rates
- Customer risk scores dari third-party
- Fraud detection API
- KYC verification services

## Setup Environment dan Instalasi

### Windows PowerShell

1. **Buat dan aktifkan virtual environment:**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. **Upgrade pip dan install dependencies:**
```powershell
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
```

3. **(Direkomendasikan) Install package secara editable:**
```powershell
python -m pip install -e .
```

### macOS/Linux

1. **Buat dan aktifkan virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate
```

2. **Upgrade pip dan install dependencies:**
```bash
python -m pip install -U pip setuptools wheel
python -m pip install -r requirements.txt
```

3. **(Direkomendasikan) Install package secara editable:**
```bash
python -m pip install -e .
```

## Cara Running Tests

### 1. Run Semua Tests

```bash
pytest
```

**Output expected:**
```
tests/test_cleaner.py ✓✓✓            3 passed
tests/test_loader.py ✓✓✓             3 passed
tests/test_transformer.py ✓✓         2 passed
tests/test_utils.py ✓                1 passed
tests/test_validator.py ✓✓✓✓         4 passed

============ 13 passed in 2.34s ============
```

### 2. Run Test Specific Module

```bash
# Test loader only
pytest tests/test_loader.py

# Test validator only
pytest tests/test_validator.py

# Test async utils
pytest tests/test_utils.py
```

### 3. Run dengan Verbose Output

```bash
pytest -v
```

### 4. Run dengan Coverage Report

```bash
# Install coverage
pip install pytest-cov

# Run dengan coverage
pytest --cov=etl --cov=utils

# Generate HTML report
pytest --cov=etl --cov=utils --cov-report=html
```

### 5. Run Specific Test Function

```bash
# Test satu fungsi
pytest tests/test_validator.py::test_negative_amount

# Test dengan keyword
pytest -k "negative"
```

## Test Coverage Summary

| Module | Test Cases | Coverage |
|--------|-----------|----------|
| **loader.py** | Missing file, wrong column count, empty row | 3 tests |
| **validator.py** | Negative amount, invalid currency, wrong ID pattern, invalid date | 4 tests |
| **cleaner.py** | Whitespace trim, date normalization, missing merchant | 3 tests |
| **transformer.py** | Derived features, type conversions | 2 tests |
| **async_api.py** | Async API call dengan mock | 1 test |
| **Total** | | **13 tests** |

## Banking Validation Rules - Detail

### 1. Transaction ID Pattern

**Format:** `TXN` + 7 digit angka

| Valid ✓ | Invalid ✗ |
|---------|-----------|
| `TXN0000001` | `ABC123` |
| `TXN9999999` | `TXN123` |
| `TXN0123456` | `txn0000001` |

### 2. Amount Constraints

**Rules:**
- Harus numeric (dapat dikonversi ke float)
- Harus > 0 (tidak boleh negatif atau 0)
- Harus ≤ 10,000,000 IDR (threshold anomaly)

| Valid ✓ | Invalid ✗ | Error Message |
|---------|-----------|---------------|
| `1000` | `-100` | Amount cannot be negative |
| `5000000` | `abc` | Amount not numeric |
| `9999999` | `15000000` | Amount exceeds anomaly threshold |

### 3. Currency Codes

**Accepted:** IDR, USD, SGD

| Valid ✓ | Invalid ✗ |
|---------|-----------|
| `IDR` | `RP` |
| `USD` | `XXX` |
| `SGD` | `EUR` |

**Note:** Cleaner akan otomatis convert ke uppercase dan set invalid ke `None`

### 4. Date Formats

**Supported Input Formats:**
- `YYYY-MM-DD` (ISO format)
- `DD/MM/YYYY` (Indonesian format)

**Output Format:** Selalu `YYYY-MM-DD`

| Input | Output | Status |
|-------|--------|--------|
| `2024-01-01` | `2024-01-01` | ✓ Valid |
| `01/01/2024` | `2024-01-01` | ✓ Valid |
| `99-99-9999` | - | ✗ Invalid |
| `2024/01/01` | - | ✗ Invalid |

### 5. Transaction Direction

**Allowed Values:** `DEBIT`, `CREDIT`

- `DEBIT`: Uang keluar (transfer, pembayaran, penarikan)
- `CREDIT`: Uang masuk (deposit, receiving transfer)

### 6. Account Types

**Allowed Values:**
- `SAVINGS` - Rekening tabungan
- `CURRENT` - Rekening giro
- `CREDIT_CARD` - Kartu kredit
- `LOAN` - Rekening pinjaman

## Possible Improvements

### 1. Database Integration

**Load ke Database:**
```python
def load_to_postgres(records, conn_string):
    """Load processed data ke PostgreSQL"""
    engine = create_engine(conn_string)
    df = pd.DataFrame(records)
    df.to_sql('transactions', engine, if_exists='append')
```

**Supported Databases:**
- PostgreSQL (relational data)
- MongoDB (document store)
- Redis (caching layer)
- Elasticsearch (full-text search)

### 2. Data Quality Enhancements

**Data Profiling:**
```python
def generate_data_profile(records):
    return {
        'total_records': len(records),
        'missing_values': count_missing(records),
        'outliers': detect_outliers(records),
        'duplicates': find_duplicates(records)
    }
```

**Advanced Imputation:**
- KNN imputation untuk missing values
- MICE (Multiple Imputation by Chained Equations)
- Forward/backward fill untuk time series

**Data Quality Reports:**
- HTML dashboard dengan Plotly/Dash
- PDF reports dengan ReportLab
- Email alerts untuk data quality issues

### 3. API & Microservices

**REST API dengan FastAPI:**
```python
from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.post("/etl/process")
async def process_transactions(file: UploadFile):
    records = load_csv(file)
    processed = [transform_record(clean_record(r)) for r in records]
    return {"processed": len(processed), "data": processed}
```

**Microservices Architecture:**
- Loader Service (port 8001)
- Validator Service (port 8002)
- Transformer Service (port 8003)
- API Gateway (port 8000)
