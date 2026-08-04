"""Sprint 3 Day 18 - Peer percentile rankings across 11 peer groups, 10 metrics."""
import sqlite3
import pandas as pd
from src.utils.year_utils import latest_per_group

DB = "db/nifty100.db"

METRICS = ["return_on_equity_pct", "roce_pct", "net_profit_margin_pct", "debt_to_equity",
           "free_cash_flow_cr", "pat_cagr_5yr", "revenue_cagr_5yr", "eps_cagr_5yr",
           "interest_coverage", "asset_turnover"]
INVERT = {"debt_to_equity"}  # lower is better


def load_latest_ratios():
    c = sqlite3.connect(DB)
    fr = pd.read_sql("SELECT * FROM financial_ratios", c)
    comp = pd.read_sql("SELECT id AS company_id FROM companies", c)
    fr = fr[fr["company_id"].isin(comp["company_id"])]
    latest = latest_per_group(fr, "company_id", "year", exclude_ttm=True)
    # roce_pct not stored in financial_ratios -> pull from companies.roce_percentage as proxy
    roce = pd.read_sql("SELECT id AS company_id, roce_percentage AS roce_pct FROM companies", c)
    c.close()
    return latest.merge(roce, on="company_id", how="left")


def compute_peer_percentiles():
    c = sqlite3.connect(DB)
    peer_groups = pd.read_sql("SELECT * FROM peer_groups", c)
    c.close()
    ratios = load_latest_ratios()
    rows = []
    for group_name, members in peer_groups.groupby("peer_group_name"):
        sub = ratios[ratios["company_id"].isin(members["company_id"])].copy()
        year_val = sub["year"].iloc[0] if len(sub) else None
        for metric in METRICS:
            if metric not in sub.columns:
                continue
            pct = sub[metric].rank(pct=True)
            if metric in INVERT:
                pct = 1 - pct
            for cid, val, p in zip(sub["company_id"], sub[metric], pct):
                rows.append({"company_id": cid, "peer_group_name": group_name, "metric": metric,
                             "value": val, "percentile_rank": round(p * 100, 1) if pd.notna(p) else None,
                             "year": year_val})
    out = pd.DataFrame(rows)
    c = sqlite3.connect(DB)
    out.to_sql("peer_percentiles", c, if_exists="replace", index=False)
    c.close()
    return out


def companies_without_peer_group():
    c = sqlite3.connect(DB)
    comp = pd.read_sql("SELECT id AS company_id FROM companies", c)
    pg = pd.read_sql("SELECT DISTINCT company_id FROM peer_groups", c)
    c.close()
    missing = set(comp["company_id"]) - set(pg["company_id"])
    for m in missing:
        print(f"{m}: No peer group assigned")
    return missing


if __name__ == "__main__":
    df = compute_peer_percentiles()
    print(f"peer_percentiles rows: {len(df)}, groups: {df['peer_group_name'].nunique()}")
    companies_without_peer_group()