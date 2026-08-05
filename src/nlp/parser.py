import sqlite3
import pandas as pd
import re
from pathlib import Path

DB_PATH = "db/nifty100.db"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def extract_percent(text):
    """
    Extract numeric percentage from strings like
    '10 Years: 21%'
    """

    if pd.isna(text):
        return None

    match = re.search(r"(-?\d+(\.\d+)?)\s*%", str(text))

    if match:
        return float(match.group(1))

    return None


conn = sqlite3.connect(DB_PATH)

analysis = pd.read_sql(
    "SELECT * FROM analysis",
    conn
)

conn.close()

parsed = analysis.copy()

columns = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

for col in columns:
    parsed[col + "_pct"] = parsed[col].apply(extract_percent)

parsed.to_csv(
    OUTPUT_DIR / "analysis_parsed.csv",
    index=False
)

print("Analysis parser completed.")
print(f"Rows parsed : {len(parsed)}")
print("Saved -> output/analysis_parsed.csv")