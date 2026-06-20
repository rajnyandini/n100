import pandas as pd


def dq01_pk_uniqueness(df, table_name):
    """
    DQ-01: Primary key uniqueness
    """
    duplicates = df[df["id"].duplicated()]

    if len(duplicates) > 0:
        return [{
            "rule_id": "DQ-01",
            "severity": "CRITICAL",
            "table_name": table_name,
            "record_id": row["id"],
            "message": "Duplicate primary key"
        } for _, row in duplicates.iterrows()]

    return []


def dq02_company_year_uniqueness(df, table_name):
    """
    DQ-02: (company_id, year) uniqueness
    """

    if "company_id" not in df.columns or "year" not in df.columns:
        return []

    duplicates = df[
        df.duplicated(subset=["company_id", "year"], keep=False)
    ]

    failures = []

    for _, row in duplicates.iterrows():
        failures.append({
            "rule_id": "DQ-02",
            "severity": "CRITICAL",
            "table_name": table_name,
            "record_id": row["id"],
            "message": f"Duplicate ({row['company_id']}, {row['year']})"
        })

    return failures

def dq03_fk_integrity(df, table_name, valid_company_ids):
    """
    DQ-03: Foreign key integrity
    """

    if "company_id" not in df.columns:
        return []

    failures = []

    invalid_rows = df[
        ~df["company_id"].isin(valid_company_ids)
    ]

    for _, row in invalid_rows.iterrows():
        failures.append({
            "rule_id": "DQ-03",
            "severity": "CRITICAL",
            "table_name": table_name,
            "record_id": row["id"],
            "message": f"Invalid company_id: {row['company_id']}"
        })

    return failures


def dq04_balance_sheet_balance(df):
    """
    DQ-04: Balance Sheet Balance Check
    Assets and Liabilities should differ by less than 1%
    """

    required_cols = [
        "total_liabilities",
        "total_assets"
    ]

    if not all(col in df.columns for col in required_cols):
        return []

    failures = []

    for _, row in df.iterrows():

        liabilities = row["total_liabilities"]
        assets = row["total_assets"]

        if pd.isna(liabilities) or pd.isna(assets):
            continue

        max_value = max(abs(liabilities), abs(assets))

        if max_value == 0:
            continue

        difference_pct = (
            abs(liabilities - assets)
            / max_value
        ) * 100

        if difference_pct > 1:

            failures.append({
                "rule_id": "DQ-04",
                "severity": "WARNING",
                "table_name": "balancesheet",
                "record_id": row["id"],
                "message": f"Balance sheet mismatch {difference_pct:.2f}%"
            })

    return failures

def dq05_opm_crosscheck(df):
    """
    DQ-05: OPM Cross Check
    OPM should match:
    (operating_profit / sales) * 100
    """

    required_cols = [
        "sales",
        "operating_profit",
        "opm_percentage"
    ]

    if not all(col in df.columns for col in required_cols):
        return []

    failures = []

    for _, row in df.iterrows():

        sales = row["sales"]
        op = row["operating_profit"]
        opm = row["opm_percentage"]

        # Handle values stored as 2214 = 22.14%
        if opm > 100:
            opm = opm / 100

        if pd.isna(sales) or pd.isna(op) or pd.isna(opm):
            continue

        if sales == 0:
            continue

        calculated_opm = (op / sales) * 100

        difference = abs(calculated_opm - opm)

        if difference > 1:

            failures.append({
                "rule_id": "DQ-05",
                "severity": "WARNING",
                "table_name": "profitandloss",
                "record_id": row["id"],
                "message": f"OPM mismatch {difference:.2f}%"
            })

    return failures

def dq06_positive_sales(df):
    """
    DQ-06: Sales must be positive
    """

    if "sales" not in df.columns:
        return []

    failures = []

    invalid_rows = df[df["sales"] <= 0]

    for _, row in invalid_rows.iterrows():

        failures.append({
            "rule_id": "DQ-06",
            "severity": "WARNING",
            "table_name": "profitandloss",
            "record_id": row["id"],
            "message": f"Non-positive sales: {row['sales']}"
        })

    return failures 

def main():

    failures = []

    companies_df = pd.read_excel(
        "data/raw/companies.xlsx",
        header=1
    )

    valid_company_ids = set(
        companies_df["id"]
    )

    files = {
        "companies": pd.read_excel("data/raw/companies.xlsx", header=1),
        "profitandloss": pd.read_excel("data/raw/profitandloss.xlsx", header=1),
        "balancesheet": pd.read_excel("data/raw/balancesheet.xlsx", header=1),
        "cashflow": pd.read_excel("data/raw/cashflow.xlsx", header=1)
    }

    for table_name, df in files.items():

        failures.extend(
            dq01_pk_uniqueness(df, table_name)
        )

        failures.extend(
            dq02_company_year_uniqueness(df, table_name)
        )

        failures.extend(
            dq03_fk_integrity(
                df,
                table_name,
                valid_company_ids
            )
        )

        if table_name == "balancesheet":

            failures.extend(
                dq04_balance_sheet_balance(df)
            )

        if table_name == "profitandloss":

            failures.extend(
                dq05_opm_crosscheck(df)
            )

            failures.extend(
                dq06_positive_sales(df)
            )

    pd.DataFrame(failures).to_csv(
        "output/validation_failures.csv",
        index=False
    )

    print(f"Failures found: {len(failures)}")


if __name__ == "__main__":
    main()