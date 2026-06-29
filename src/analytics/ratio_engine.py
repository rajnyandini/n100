"""
Sprint 2 - Financial Ratio Engine
Day 12

Loads all financial tables,
computes KPIs,
writes financial_ratios table.
"""

import sqlite3
import pandas as pd

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover,
)

from src.analytics.cashflow_kpis import (
    free_cash_flow,
)

from src.analytics.cagr import (
    calculate_cagr,
)

DB_PATH = "db/nifty100.db"


def load_tables():

    conn = sqlite3.connect(DB_PATH)

    profit = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    balance = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    cashflow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    sectors = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )

    conn.close()

    return (
        profit,
        balance,
        cashflow,
        companies,
        sectors,
    )


def remove_duplicates(df):

    return df.drop_duplicates(
        subset=["company_id", "year"],
        keep="first"
    )


def prepare_data():

    (
        profit,
        balance,
        cashflow,
        companies,
        sectors,
    ) = load_tables()

    profit = remove_duplicates(profit)
    balance = remove_duplicates(balance)
    cashflow = remove_duplicates(cashflow)

    merged = (
        profit
        .merge(
            balance,
            on=["company_id", "year"],
            how="left",
            suffixes=("", "_bs"),
        )
        .merge(
            cashflow,
            on=["company_id", "year"],
            how="left",
            suffixes=("", "_cf"),
        )
        .merge(
            companies,
            left_on="company_id",
            right_on="id",
            how="left",
        )
        .merge(
            sectors,
            on="company_id",
            how="left",
        )
    )

    merged = merged.drop(
        columns=[
            "id_x",
            "id_bs",
            "id_cf",
            "id_y",
            "id",
        ],
        errors="ignore",
    )

    return merged


def compute_kpis(row):

    # ---------- Basic KPIs ----------

    npm = net_profit_margin(
        row["net_profit"],
        row["sales"],
    )

    opm = operating_profit_margin(
        row["operating_profit"],
        row["sales"],
    )

    roe = return_on_equity(
        row["net_profit"],
        row["equity_capital"],
        row["reserves"],
    )

    roa = return_on_assets(
        row["net_profit"],
        row["total_assets"],
    )

    roce = return_on_capital_employed(
        row["operating_profit"],
        row["other_income"],
        row["equity_capital"],
        row["reserves"],
        row["borrowings"],
    )

    de = debt_to_equity(
        row["borrowings"],
        row["equity_capital"],
        row["reserves"],
    )

    icr = interest_coverage_ratio(
        row["operating_profit"],
        row["other_income"],
        row["interest"],
    )

    turnover = asset_turnover(
        row["sales"],
        row["total_assets"],
    )

    fcf = free_cash_flow(
        row["operating_activity"],
        row["investing_activity"],
    )

    capex = (
        abs(row["investing_activity"])
        if pd.notna(row["investing_activity"])
        else None
    )

    # ---------- Placeholder CAGR ----------
    revenue_cagr = None
    pat_cagr = None
    eps_cagr = None

    # ---------- Composite Score ----------
    score = 0

    if roe is not None and roe > 15:
        score += 1

    if de is not None and de < 1:
        score += 1

    if npm is not None and npm > 10:
        score += 1

    if icr is not None and icr > 3:
        score += 1

    if turnover is not None and turnover > 1:
        score += 1

    return {

        "company_id": row["company_id"],
        "year": row["year"],

        "net_profit_margin_pct": npm,

        "operating_profit_margin_pct": opm,

        "return_on_equity_pct": roe,

        "debt_to_equity": de,

        "interest_coverage": icr,

        "asset_turnover": turnover,

        "free_cash_flow_cr": fcf,

        "capex_cr": capex,

        "earnings_per_share": row["eps"],

        "book_value_per_share": row["book_value"],

        "dividend_payout_ratio_pct": row["dividend_payout"],

        "total_debt_cr": row["borrowings"],

        "cash_from_operations_cr": row["operating_activity"],

        "revenue_cagr_5yr": revenue_cagr,

        "pat_cagr_5yr": pat_cagr,

        "eps_cagr_5yr": eps_cagr,

        "composite_quality_score": score,

        # Used later in Day 13
        "roa": roa,
        "roce": roce,
    }


def build_ratio_table(df):

    rows = []

    for _, row in df.iterrows():
        rows.append(compute_kpis(row))

    result = pd.DataFrame(rows)

    return result


def save_to_database(result):

    # Keep only columns that exist in financial_ratios
    db_result = result[
        [
            "company_id",
            "year",
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "return_on_equity_pct",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "free_cash_flow_cr",
            "capex_cr",
            "earnings_per_share",
            "book_value_per_share",
            "dividend_payout_ratio_pct",
            "total_debt_cr",
            "cash_from_operations_cr",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "eps_cagr_5yr",
            "composite_quality_score",
        ]
    ]

    conn = sqlite3.connect(DB_PATH)

    conn.execute("DELETE FROM financial_ratios")

    db_result.to_sql(
        "financial_ratios",
        conn,
        if_exists="append",
        index=False,
    )

    count = conn.execute(
        "SELECT COUNT(*) FROM financial_ratios"
    ).fetchone()[0]

    conn.commit()
    conn.close()

    print()
    print("=" * 60)
    print("Financial Ratio Engine Completed")
    print("=" * 60)
    print(f"Rows inserted : {count}")
    print("=" * 60)

    return db_result


if __name__ == "__main__":

    print("=" * 60)
    print("Financial Ratio Engine")
    print("=" * 60)

    df = prepare_data()

    print(f"Merged rows : {len(df)}")

    print("\nComputing KPIs...")

    result = build_ratio_table(df)

    print("\nPreview")
    print(result.head())

    save_to_database(result)

    print("\nDone.")