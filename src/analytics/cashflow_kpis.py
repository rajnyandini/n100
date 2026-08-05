import sqlite3
import pandas as pd
from pathlib import Path
import numpy as np

DB_PATH = "db/nifty100.db"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

cashflow = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        operating_activity,
        investing_activity,
        financing_activity,
        net_cash_flow
    FROM cashflow
    """,
    conn
)

conn.close()

df = cashflow.copy()

# Cash Flow Quality
df["operating_positive"] = df["operating_activity"] > 0
df["investing_negative"] = df["investing_activity"] < 0
df["financing_positive"] = df["financing_activity"] > 0

# Capital Allocation Pattern
def classify(row):

    o = "+" if row["operating_activity"] >= 0 else "-"
    i = "+" if row["investing_activity"] >= 0 else "-"
    f = "+" if row["financing_activity"] >= 0 else "-"

    pattern = (o, i, f)

    if pattern == ("+", "-", "-"):
        return "Healthy Reinvestment"

    if pattern == ("+", "-", "+"):
        return "Growth Funded"

    if pattern == ("+", "+", "-"):
        return "Asset Liquidation"

    if pattern == ("-", "+", "+"):
        return "Financial Distress"

    if pattern == ("+", "+", "+"):
        return "Cash Accumulator"

    return "Mixed"

df["capital_pattern"] = df.apply(classify, axis=1)

# Operating Cash Flow Ratio
import numpy as np

df["operating_share"] = np.where(
    df["net_cash_flow"] != 0,
    (df["operating_activity"] / df["net_cash_flow"]).round(2),
    np.nan
)

output_file = OUTPUT_DIR / "cashflow_intelligence.xlsx"

with pd.ExcelWriter(output_file) as writer:
    df.to_excel(
        writer,
        sheet_name="Cash Flow Intelligence",
        index=False
    )

print("Cash Flow Intelligence generated.")
print(f"Rows exported : {len(df)}")
print(f"Saved -> {output_file}")