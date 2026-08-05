import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = "db/nifty100.db"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql(
    """
    SELECT
        company_id,
        pros,
        cons
    FROM prosandcons
    """,
    conn
)

conn.close()

# Replace missing values
df["pros"] = df["pros"].fillna("")
df["cons"] = df["cons"].fillna("")

# Remove duplicates
df = df.drop_duplicates()

# Remove completely empty rows
df = df[
    (df["pros"].str.strip() != "") |
    (df["cons"].str.strip() != "")
]

df.to_csv(
    OUTPUT_DIR / "pros_cons_generated.csv",
    index=False
)

print("Pros & Cons generation completed.")
print(f"Rows exported : {len(df)}")
print("Saved -> output/pros_cons_generated.csv")