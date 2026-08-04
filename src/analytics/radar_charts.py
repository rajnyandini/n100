"""Sprint 3 Day 19 - radar/polar charts per company, peer avg overlay, PNG export."""
import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.utils.year_utils import latest_per_group

DB = "db/nifty100.db"
AXES = ["ROE", "ROCE", "NPM", "D/E (inv)", "FCF score", "PAT CAGR 5yr", "Revenue CAGR 5yr", "Composite Score"]
OUTDIR = "reports/radar_charts"


def _company_axis_values(cid, ratios, comp_meta, universe_stats):
    row = ratios[ratios["company_id"] == cid]
    if row.empty:
        return None
    row = row.iloc[0]
    roce = comp_meta.loc[comp_meta["company_id"] == cid, "roce_percentage"]
    roce = roce.iloc[0] if len(roce) else np.nan

    def scale(val, lo, hi):
        if pd.isna(val):
            return 0
        return float(np.clip((val - lo) / (hi - lo) * 100, 0, 100))

    de = row.get("debt_to_equity", np.nan)
    de_inv = scale(-de if pd.notna(de) else np.nan, -5, 0) if pd.notna(de) else 0
    fcf = row.get("free_cash_flow_cr", np.nan)
    fcf_score = 100 if pd.notna(fcf) and fcf > 0 else (0 if pd.notna(fcf) else 0)
    comp_score = row.get("composite_quality_score", np.nan)
    return [
        scale(row.get("return_on_equity_pct"), 0, 40),
        scale(roce, 0, 40),
        scale(row.get("net_profit_margin_pct"), 0, 30),
        de_inv,
        fcf_score,
        scale(row.get("pat_cagr_5yr"), -10, 40),
        scale(row.get("revenue_cagr_5yr"), -10, 30),
        float(np.clip(comp_score, 0, 100)) if pd.notna(comp_score) else 0,
    ]


def generate_all():
    os.makedirs(OUTDIR, exist_ok=True)
    c = sqlite3.connect(DB)
    comp_meta = pd.read_sql("SELECT id AS company_id, company_name, roce_percentage FROM companies", c)
    fr = pd.read_sql("SELECT * FROM financial_ratios", c)
    peer_groups = pd.read_sql("SELECT * FROM peer_groups", c)
    c.close()
    fr = fr[fr["company_id"].isin(comp_meta["company_id"])]
    ratios = latest_per_group(fr, "company_id", "year", exclude_ttm=True)

    cid_to_group = peer_groups.set_index("company_id")["peer_group_name"].to_dict()
    angles = np.linspace(0, 2 * np.pi, len(AXES), endpoint=False).tolist()
    angles += angles[:1]

    count = 0
    for cid in comp_meta["company_id"]:
        vals = _company_axis_values(cid, ratios, comp_meta, None)
        if vals is None:
            continue
        vals_plot = vals + vals[:1]

        group = cid_to_group.get(cid)
        peer_avg = None
        if group:
            members = peer_groups.loc[peer_groups["peer_group_name"] == group, "company_id"]
            peer_vals = [_company_axis_values(m, ratios, comp_meta, None) for m in members if m != cid]
            peer_vals = [v for v in peer_vals if v is not None]
            if peer_vals:
                peer_avg = np.mean(peer_vals, axis=0).tolist()
                peer_avg += peer_avg[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.plot(angles, vals_plot, color="#1f77b4", linewidth=2)
        ax.fill(angles, vals_plot, color="#1f77b4", alpha=0.25)
        if peer_avg:
            ax.plot(angles, peer_avg, color="#d62728", linewidth=1.5, linestyle="--", label="Peer group avg")
            ax.legend(loc="upper right", fontsize=8, bbox_to_anchor=(1.25, 1.1))
        else:
            ax.set_title("No peer group — showing company only", fontsize=8, y=-0.12)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(AXES, fontsize=8)
        ax.set_ylim(0, 100)
        name = comp_meta.loc[comp_meta["company_id"] == cid, "company_name"].iloc[0]
        ax.set_title(f"{cid} — {name}", fontsize=10, pad=20)
        fig.tight_layout()
        fig.savefig(f"{OUTDIR}/{cid}_radar.png", dpi=110)
        plt.close(fig)
        count += 1
    print(f"Generated {count} radar charts in {OUTDIR}/")


if __name__ == "__main__":
    generate_all()