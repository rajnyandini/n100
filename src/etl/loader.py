import pandas as pd
import sqlite3
import re
from pathlib import Path


DB_PATH = "db/nifty100.db"


def normalize_year(year):
    """
    Convert year values into integer format.
    Examples:
    FY2024 -> 2024
    2024-03 -> 2024
    2024 -> 2024
    """

    if pd.isna(year):
        return None

    year = str(year).strip()

    match = re.search(r"(20\d{2}|19\d{2})", year)

    if match:
        return int(match.group())

    return None


def normalize_ticker(ticker):
    """
    Standardize ticker symbols.
    """

    if pd.isna(ticker):
        return None

    ticker = str(ticker).strip().upper()

    ticker = re.sub(r"[^A-Z0-9]", "", ticker)

    return ticker


def load_excel(file_path):
    """
    Load Excel file with header row = 1
    """

    return pd.read_excel(file_path, header=1)


def load_to_sqlite():

    conn = sqlite3.connect(DB_PATH)

    files = {
        "companies": "data/raw/companies.xlsx",
        "profitandloss": "data/raw/profitandloss.xlsx",
        "balancesheet": "data/raw/balancesheet.xlsx",
        "cashflow": "data/raw/cashflow.xlsx",
        "analysis": "data/raw/analysis.xlsx",
        "documents": "data/raw/documents.xlsx",
        "prosandcons": "data/raw/prosandcons.xlsx",
        "sectors": "data/raw/supporting/sectors.xlsx",
        "stock_prices": "data/raw/supporting/stock_prices.xlsx",
        "financial_ratios": "data/raw/supporting/financial_ratios.xlsx",
        "peer_groups": "data/raw/supporting/peer_groups.xlsx",
        "market_cap": "data/raw/supporting/market_cap.xlsx"
    }

    audit = []

    for table_name, file_path in files.items():

        print(f"Loading {table_name}...")

        if "supporting" in file_path:
            df = pd.read_excel(file_path)
        else:
            df = pd.read_excel(file_path, header=1)

        df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=False
        )

        audit.append({
            "table_name": table_name,
            "rows_loaded": len(df),
            "rows_rejected": 0
        })

        print(f"Loaded {len(df)} rows")

    audit_df = pd.DataFrame(audit)

    audit_df.to_csv(
        "output/load_audit.csv",
        index=False
    )

    conn.commit()
    conn.close()

    print("\nData loaded successfully")
    print("load_audit.csv generated")


if __name__ == "__main__":
    load_to_sqlite()