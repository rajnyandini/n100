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
    """

    if (
        "total_liabilities" not in df.columns
        or "total_assets" not in df.columns
    ):
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

        if pd.isna(sales) or pd.isna(op) or pd.isna(opm):
            continue

        if sales == 0:
            continue

        if opm > 100:
            opm = opm / 100

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


def dq07_tax_rate_range(df):
    """
    DQ-07: Tax Rate Range Check
    """

    if "tax_percentage" not in df.columns:
        return []

    failures = []

    invalid_rows = df[
        (df["tax_percentage"] < -100)
        | (df["tax_percentage"] > 100)
    ]

    for _, row in invalid_rows.iterrows():

        failures.append({
            "rule_id": "DQ-07",
            "severity": "WARNING",
            "table_name": "profitandloss",
            "record_id": row["id"],
            "message": f"Invalid tax rate: {row['tax_percentage']}"
        })

    return failures

def dq08_net_cash_flow_check(df):
    """
    DQ-08: Net Cash Flow Validation
    """

    required_cols = [
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "net_cash_flow"
    ]

    if not all(col in df.columns for col in required_cols):
        return []

    failures = []

    for _, row in df.iterrows():

        calculated = (
            row["operating_activity"]
            + row["investing_activity"]
            + row["financing_activity"]
        )

        reported = row["net_cash_flow"]

        if pd.isna(calculated) or pd.isna(reported):
            continue

        difference = abs(calculated - reported)

        if difference > 1:

            failures.append({
                "rule_id": "DQ-08",
                "severity": "WARNING",
                "table_name": "cashflow",
                "record_id": row["id"],
                "message": f"Net cash mismatch {difference:.2f}"
            })

    return failures

def dq09_dividend_payout(df):
    """
    DQ-09: Dividend payout must be non-negative
    """

    if "dividend_payout" not in df.columns:
        return []

    failures = []

    invalid_rows = df[
        df["dividend_payout"] < 0
    ]

    for _, row in invalid_rows.iterrows():

        failures.append({
            "rule_id": "DQ-09",
            "severity": "WARNING",
            "table_name": "profitandloss",
            "record_id": row["id"],
            "message": f"Negative dividend payout: {row['dividend_payout']}"
        })

    return failures

def dq10_eps_range(df):
    """
    DQ-10: EPS Range Check
    """

    if "eps" not in df.columns:
        return []

    failures = []

    invalid_rows = df[
        (df["eps"] < -1000)
        | (df["eps"] > 1000)
    ]

    for _, row in invalid_rows.iterrows():

        failures.append({
            "rule_id": "DQ-10",
            "severity": "WARNING",
            "table_name": "profitandloss",
            "record_id": row["id"],
            "message": f"Suspicious EPS: {row['eps']}"
        })

    return failures

def dq11_total_liabilities_check(df):
    """
    DQ-11: Total Liabilities Validation
    """

    required_cols = [
        "equity_capital",
        "reserves",
        "borrowings",
        "other_liabilities",
        "total_liabilities"
    ]

    if not all(col in df.columns for col in required_cols):
        return []

    failures = []

    for _, row in df.iterrows():

        calculated = (
            row["equity_capital"]
            + row["reserves"]
            + row["borrowings"]
            + row["other_liabilities"]
        )

        reported = row["total_liabilities"]

        if pd.isna(calculated) or pd.isna(reported):
            continue

        difference = abs(calculated - reported)

        if difference > 1:

            failures.append({
                "rule_id": "DQ-11",
                "severity": "WARNING",
                "table_name": "balancesheet",
                "record_id": row["id"],
                "message": f"Liabilities mismatch {difference:.2f}"
            })

    return failures

def dq12_url_validation(df):
    """
    DQ-12: URL Validation
    """

    url_columns = [
        "website",
        "company_logo",
        "chart_link",
        "nse_profile",
        "bse_profile"
    ]

    failures = []

    for col in url_columns:

        if col not in df.columns:
            continue

        invalid_rows = df[
            ~df[col].astype(str).str.startswith(
                ("http://", "https://"),
                na=False
            )
        ]

        for _, row in invalid_rows.iterrows():

            failures.append({
                "rule_id": "DQ-12",
                "severity": "WARNING",
                "table_name": "companies",
                "record_id": row["id"],
                "message": f"Invalid URL in {col}"
            })

    return failures

def dq13_total_assets_check(df):
    """
    DQ-13: Total Assets Validation
    """

    required_cols = [
        "fixed_assets",
        "cwip",
        "investments",
        "other_asset",
        "total_assets"
    ]

    if not all(col in df.columns for col in required_cols):
        return []

    failures = []

    for _, row in df.iterrows():

        calculated = (
            row["fixed_assets"]
            + row["cwip"]
            + row["investments"]
            + row["other_asset"]
        )

        reported = row["total_assets"]

        if pd.isna(calculated) or pd.isna(reported):
            continue

        difference = abs(calculated - reported)

        if difference > 1:

            failures.append({
                "rule_id": "DQ-13",
                "severity": "WARNING",
                "table_name": "balancesheet",
                "record_id": row["id"],
                "message": f"Assets mismatch {difference:.2f}"
            })

    return failures

def dq14_coverage_check(df):
    """
    DQ-14: Company must have at least 5 years of data
    """

    if "company_id" not in df.columns:
        return []

    coverage = (
        df.groupby("company_id")["year"]
        .count()
        .reset_index()
    )

    failures = []

    invalid_companies = coverage[
        coverage["year"] < 5
    ]

    for _, row in invalid_companies.iterrows():

        failures.append({
            "rule_id": "DQ-14",
            "severity": "WARNING",
            "table_name": "profitandloss",
            "record_id": row["company_id"],
            "message": f"Only {row['year']} years of data"
        })

    return failures

def dq15_mandatory_fields(df):
    """
    DQ-15: Mandatory Fields Check
    """

    required_columns = [
        "id",
        "company_name",
        "website"
    ]

    failures = []

    for col in required_columns:

        if col not in df.columns:
            continue

        invalid_rows = df[
            df[col].isna()
        ]

        for _, row in invalid_rows.iterrows():

            failures.append({
                "rule_id": "DQ-15",
                "severity": "WARNING",
                "table_name": "companies",
                "record_id": row["id"],
                "message": f"Missing value in {col}"
            })

    return failures

def dq16_roe_range(df):
    """
    DQ-16: ROE Range Check
    """

    if "roe_percentage" not in df.columns:
        return []

    failures = []

    invalid_rows = df[
        (df["roe_percentage"] < -100)
        | (df["roe_percentage"] > 100)
    ]

    for _, row in invalid_rows.iterrows():

        failures.append({
            "rule_id": "DQ-16",
            "severity": "WARNING",
            "table_name": "companies",
            "record_id": row["id"],
            "message": f"Invalid ROE: {row['roe_percentage']}"
        })

    return failures

def main():

    failures = []

    companies_df = pd.read_excel(
        "data/raw/companies.xlsx",
        header=1
    )

    valid_company_ids = set(companies_df["id"])

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

            failures.extend(
                dq11_total_liabilities_check(df)
            )

            failures.extend(
                dq13_total_assets_check(df)
            )

        if table_name == "profitandloss":

            failures.extend(
                dq05_opm_crosscheck(df)
            )

            failures.extend(
                dq06_positive_sales(df)
            )

            failures.extend(
                dq07_tax_rate_range(df)
            )
            failures.extend(
                dq09_dividend_payout(df)
            )

            failures.extend(
                dq10_eps_range(df)
            )

            failures.extend(
                dq14_coverage_check(df)
            )
        
        if table_name == "cashflow":

            failures.extend(
                dq08_net_cash_flow_check(df)
            )

        if table_name == "companies":

            failures.extend(
                dq12_url_validation(df)
            )

            failures.extend(
                dq15_mandatory_fields(df)
            )

            failures.extend(
                dq16_roe_range(df)
            )

    pd.DataFrame(failures).to_csv(
        "output/validation_failures.csv",
        index=False
    )

    print(f"Failures found: {len(failures)}")


if __name__ == "__main__":
    main()