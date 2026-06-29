import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = ["profitandloss", "balancesheet", "cashflow"]

for table in tables:
    print(f"\n===== {table} =====")

    query = f"""
    SELECT
        company_id,
        year,
        COUNT(*) AS cnt
    FROM {table}
    GROUP BY company_id, year
    HAVING COUNT(*) > 1
    ORDER BY cnt DESC;
    """

    df = pd.read_sql(query, conn)

    print(df.head(20))
    print("Duplicate groups:", len(df))

conn.close()