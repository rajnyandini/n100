import pandas as pd
import re
from pathlib import Path


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
    Load excel with header row = 1
    """

    return pd.read_excel(file_path, header=1)


def load_all_core_files(data_dir):
    """
    Load all 7 core datasets.
    """

    files = {
        "companies": "companies.xlsx",
        "profitandloss": "profitandloss.xlsx",
        "balancesheet": "balancesheet.xlsx",
        "cashflow": "cashflow.xlsx",
        "analysis": "analysis.xlsx",
        "documents": "documents.xlsx",
        "prosandcons": "prosandcons.xlsx"
    }

    datasets = {}

    for name, file in files.items():
        path = Path(data_dir) / file
        datasets[name] = load_excel(path)

    return datasets


if __name__ == "__main__":
    datasets = load_all_core_files("data/raw")

    for name, df in datasets.items():
        print(f"{name}: {df.shape}")