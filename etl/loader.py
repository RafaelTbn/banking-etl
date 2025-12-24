import csv
import logging

logger = logging.getLogger(__name__)


class CSVFormatError(Exception):
    pass


def load_csv(path: str) -> list[dict]:
    mandatory = [
        "transaction_id", "transaction_date",
        "customer_id", "account_id",
        "amount", "currency"
    ]

    rows = []
    logger.debug("Loading CSV from %s", path)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
# =========================== Cek Misiing File ===========================
        except StopIteration:
            logger.error("CSV file is empty: %s", path)
            raise CSVFormatError("CSV file is empty")

        header = [h.strip() for h in header]
        logger.debug("Parsed header: %s", header)

# =========================== Cek mandatory columns ===========================
        for m in mandatory:
            if m not in header:
                logger.error("Missing mandatory column: %s", m)
                raise CSVFormatError(f"Missing mandatory column: {m}")

        expected_cols = len(header)

        f.seek(0)
        dict_reader = csv.DictReader(f)

        for i, row in enumerate(dict_reader, start=2):

# =========================== Cek empty row ===========================
            if not any(row.values()):
                logger.error("Empty row detected at line %d", i)
                raise CSVFormatError(f"Empty row detected at line {i}")

#=========================== Cek wrong column count ===========================
            if len(row) != expected_cols:
                logger.error("Wrong column count at line %d (expected=%d got=%d)", i, expected_cols, len(row))
                raise CSVFormatError(f"Wrong column count at line {i}")

            cleaned = {k: v.strip() if v else v for k, v in row.items()}
            rows.append(cleaned)

    logger.info("Loaded %d rows from %s", len(rows), path)
    return rows
