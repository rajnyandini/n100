import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

# Pick 5 companies
companies = pd.read_sql(
    "SELECT id, company_name FROM companies ORDER BY RANDOM() LIMIT 5;",
    conn
)

print("=== Selected Companies ===")
print(companies)

for _, row in companies.iterrows():
    cid = row["id"]

    print("\n" + "=" * 70)
    print(f"{cid} - {row['company_name']}")

    for table in ["profitandloss", "balancesheet", "cashflow"]:
        count = pd.read_sql(
            f"""
            SELECT COUNT(*) AS records,
                   MIN(year) AS first_year,
                   MAX(year) AS last_year
            FROM {table}
            WHERE company_id='{cid}'
            """,
            conn,
        )

        print(f"\n{table}")
        print(count)

print("\n" + "=" * 70)
print("Companies with fewer than 5 years of Profit & Loss data")

coverage = pd.read_sql("""
SELECT company_id,
COUNT(*) AS years
FROM profitandloss
GROUP BY company_id
HAVING COUNT(*) < 5
ORDER BY years;
""", conn)

print(coverage)

conn.close()