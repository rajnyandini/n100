"""Sprint 3 - Screener Engine: threshold filters, composite score, 6 presets."""
import sqlite3
import yaml
import numpy as np
import pandas as pd
from src.utils.year_utils import latest_per_group

DB = "db/nifty100.db"


def load_universe():
    """Join financial_ratios (latest yr, excl. TTM) + sectors + market_cap + companies + PL.
    Restricted to the 92 tickers present in the companies master table."""
    c = sqlite3.connect(DB)
    comp = pd.read_sql("SELECT id AS company_id, company_name FROM companies", c)
    valid_ids = set(comp["company_id"])
    fr = pd.read_sql("SELECT * FROM financial_ratios", c)
    fr = fr[fr["company_id"].isin(valid_ids)]
    latest = latest_per_group(fr, "company_id", "year", exclude_ttm=True)
    sec = pd.read_sql("SELECT company_id, broad_sector, sub_sector FROM sectors", c)
    mc = pd.read_sql("SELECT * FROM market_cap", c)
    mc_latest = latest_per_group(mc, "company_id", "year")
    pl = pd.read_sql("SELECT company_id, year, sales, net_profit FROM profitandloss", c)
    pl = pl[pl["company_id"].isin(valid_ids)]
    pl_latest = latest_per_group(pl, "company_id", "year", exclude_ttm=True)[["company_id", "sales", "net_profit"]]
    pl_latest.columns = ["company_id", "sales_cr", "net_profit_cr"]
    c.close()
    df = latest.merge(sec, on="company_id", how="left") \
        .merge(mc_latest[["company_id", "market_cap_crore", "pe_ratio", "pb_ratio", "dividend_yield_pct"]], on="company_id", how="left") \
        .merge(pl_latest, on="company_id", how="left") \
        .merge(comp, on="company_id", how="left")
    return df


def _winsorize_scale(s):
    p10, p90 = s.quantile(0.10), s.quantile(0.90)
    clipped = s.clip(p10, p90)
    if p90 == p10:
        return pd.Series(50.0, index=s.index)
    return (clipped - p10) / (p90 - p10) * 100


def composite_quality_score(df):
    """0-100 composite: 35% Profitability + 30% Cash Quality + 20% Growth + 15% Leverage."""
    df = df.copy()
    roe_s = _winsorize_scale(df["return_on_equity_pct"].fillna(df["return_on_equity_pct"].median()))
    npm_s = _winsorize_scale(df["net_profit_margin_pct"].fillna(df["net_profit_margin_pct"].median()))
    fcf_s = _winsorize_scale(df["free_cash_flow_cr"].fillna(0))
    rev_cagr_s = _winsorize_scale(df["revenue_cagr_5yr"].fillna(0))
    pat_cagr_s = _winsorize_scale(df["pat_cagr_5yr"].fillna(0))
    de_s = 100 - _winsorize_scale(df["debt_to_equity"].fillna(0))  # lower D/E = higher score
    icr_filled = df["interest_coverage"].fillna(df["interest_coverage"].max())
    icr_s = _winsorize_scale(icr_filled)
    fcf_pos_flag = (df["free_cash_flow_cr"].fillna(0) > 0).astype(float) * 100

    profitability = 0.15 * roe_s + 0.10 * roe_s.clip(0, 100) + 0.10 * npm_s  # ROE proxy for ROCE weight too
    cash_quality = 0.15 * fcf_s + 0.10 * fcf_s + 0.05 * fcf_pos_flag
    growth = 0.10 * rev_cagr_s + 0.10 * pat_cagr_s
    leverage = 0.10 * de_s + 0.05 * icr_s

    df["composite_quality_score"] = (profitability + cash_quality + growth + leverage).round(2).clip(0, 100)
    # sector-relative composite score
    df["composite_score_sector_relative"] = df.groupby("broad_sector")["composite_quality_score"] \
        .transform(lambda s: _winsorize_scale(s)).round(2)
    return df


_OPS = {">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b, "==": lambda a, b: a == b}


def _turnaround_ids():
    """Companies with FCF positive in latest year AND D/E declining YoY (last 2 available years)."""
    c = sqlite3.connect(DB)
    fr = pd.read_sql("SELECT company_id, year, free_cash_flow_cr, debt_to_equity FROM financial_ratios", c)
    c.close()
    from src.utils.year_utils import latest_per_group, year_sort_key
    fr["_yk"] = fr["year"].map(year_sort_key)
    fr = fr[fr["_yk"] > 0].sort_values("_yk")
    ok = []
    for cid, g in fr.groupby("company_id"):
        g = g.dropna(subset=["debt_to_equity"])
        if len(g) < 2:
            continue
        fcf_pos = g["free_cash_flow_cr"].iloc[-1] is not None and g["free_cash_flow_cr"].iloc[-1] > 0
        de_declining = g["debt_to_equity"].iloc[-1] < g["debt_to_equity"].iloc[-2]
        if fcf_pos and de_declining:
            ok.append(cid)
    return set(ok)


def apply_filters(df, filters, config):
    """Apply threshold filters. Skips Financials sector automatically for D/E max filter."""
    out = df.copy()
    for key, val in filters.items():
        if key == "fcf_positive_latest":
            continue
        if key == "de_declining_yoy":
            out = out[out["company_id"].isin(_turnaround_ids())]
            continue
        if key == "max_dividend_payout":
            out = out[out["dividend_payout_ratio_pct"].fillna(0) <= val]
            continue
        if key == "min_rev_cagr_3yr":
            out = out[out["revenue_cagr_3yr"].fillna(-999) >= val]
            continue
        meta = config["metrics"][key]
        col, op = meta["column"], meta["op"]
        if key == "max_de":
            mask_fin = out["broad_sector"] == "Financials"
            mask_pass = _OPS[op](out[col].fillna(999), val)
            out = out[mask_fin | mask_pass]
        elif key == "min_icr":
            infinite_icr = out["interest_coverage"].isna() & (out["icr_label"] == "Debt Free") if "icr_label" in out.columns else out["interest_coverage"].isna()
            mask_pass = _OPS[op](out[col].fillna(np.inf), val)
            out = out[infinite_icr | mask_pass]
        else:
            out = out[_OPS[op](out[col].fillna(-np.inf) if op == ">=" else out[col].fillna(np.inf), val)]
    return out.sort_values("composite_quality_score", ascending=False)


def run_preset(df, preset_key, config):
    preset = config["presets"][preset_key]
    filtered = apply_filters(df, preset["filters"], config)
    return preset["name"], filtered


if __name__ == "__main__":
    with open("config/screener_config.yaml") as f:
        cfg = yaml.safe_load(f)
    universe = composite_quality_score(load_universe())
    print(f"Universe: {len(universe)} companies")
    for key in cfg["presets"]:
        name, res = run_preset(universe, key, cfg)
        print(f"{name}: {len(res)} companies")