import os
import sys
import plotly.express as px

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd

from src.dashboard.components.styles import load_css
from src.dashboard.utils.db import (
    get_companies,
    get_company_profile,
    get_ratios,
    get_pl,
    get_valuation,
)

st.set_page_config(
    page_title="Company Profile",
    layout="wide"
)

load_css()

def format_market_cap(x):
    if pd.isna(x):
        return "N/A"

    if x >= 100000:
        return f"₹ {x/100000:.2f} LCr"

    return f"₹ {x/100000:.1f} LCr"
# -----------------------------
# Sidebar
# -----------------------------

companies = get_companies()

selected = st.sidebar.selectbox(
    "Company",
    companies["company_name"]
)

company_id = companies.loc[
    companies["company_name"] == selected,
    "company_id"
].iloc[0]

# -----------------------------
# Load Data
# -----------------------------

profile = get_company_profile(company_id)
ratios = get_ratios(company_id)
pl = get_pl(company_id)
valuation = get_valuation(company_id)

if profile.empty:
    st.error("Company not found.")
    st.stop()

profile = profile.iloc[0]

latest_ratio = (
    ratios.iloc[-1]
    if not ratios.empty
    else pd.Series(dtype="object")
)

latest_value = (
    valuation.iloc[-1]
    if not valuation.empty
    else pd.Series(dtype="object")
)

st.title(profile["company_name"])
st.caption(
    f'Company Profile • {profile.get("broad_sector", "Unknown")} • {profile.get("sub_sector", "Unknown")}'
)

left, right = st.columns([1,4])


with left:

    logo = str(profile.get("company_logo"))

    if "economictimes.com" in logo.lower():

        st.image(
            logo,
            width=120
        )

    else:

        initials = "".join(
            word[0].upper()
            for word in profile["company_name"].split()[:2]
        )

        st.markdown(
            f"""
            <div style="
                width:120px;
                height:120px;
                border-radius:16px;
                background:#1f2937;
                display:flex;
                justify-content:center;
                align-items:center;
                font-size:42px;
                font-weight:bold;
                color:white;
                border:1px solid #374151;">
                {initials}
            </div>
            """,
            unsafe_allow_html=True
        )

with right:

    st.markdown("### About")

    st.write(profile["about_company"])

    if pd.notna(profile["website"]):
        st.link_button(
            "Visit Website",
            profile["website"]
        )
st.divider()

c1,c2,c3,c4,c5,c6 = st.columns(6)

cards = [

    (
        "Market Cap",
        format_market_cap(
            latest_value.get("market_cap_crore")
        )
        if pd.notna(latest_value.get("market_cap_crore"))
        else "N/A"
    ),

    (
        "PE",
        f'{latest_value["pe_ratio"]:.2f}'
        if pd.notna(latest_value.get("pe_ratio"))
        else "N/A"
    ),

    (
        "PB",
        f'{latest_value["pb_ratio"]:.2f}'
        if pd.notna(latest_value.get("pb_ratio"))
        else "N/A"
    ),

    (
        "ROE",
        f'{latest_ratio["return_on_equity_pct"]:.2f}%'
        if pd.notna(latest_ratio.get("return_on_equity_pct"))
        else "N/A"
    ),

    (
        "ROCE",
        f'{profile["roce_percentage"]:.2f}%'
        if pd.notna(profile.get("roce_percentage"))
        else "N/A"
    ),

    (
        "Debt / Equity",
        f'{latest_ratio["debt_to_equity"]:.2f}'
        if pd.notna(latest_ratio.get("debt_to_equity"))
        else "N/A"
    )

]

for col,(title,value) in zip(
[c1,c2,c3,c4,c5,c6],
cards
):

    with col:

        st.markdown(f"""
<div class="metric-card">

<div class="metric-title">
{title}
</div>

<div class="metric-value">
{value}
</div>

</div>
""",unsafe_allow_html=True)

st.divider()

left, right = st.columns(2)

# ==========================================
# Revenue vs Net Profit
# ==========================================

with left:

    st.subheader("Revenue vs Net Profit")

    if not pl.empty:

        pl_chart = pl.copy()

        pl_chart["year_num"] = pd.to_numeric(
            pl_chart["year"].astype(str).str.extract(r"(\d{4})")[0],
            errors="coerce"
        )

        pl_chart = pl_chart.dropna(subset=["year_num"])
        pl_chart = pl_chart.sort_values("year_num")

        fig = px.bar(
            pl_chart,
            x="year_num",
            y="sales",
            labels={
                "sales": "Revenue",
                "year_num": "Year"
            },
            color_discrete_sequence=["#2563eb"]
        )

        fig.add_scatter(
            x=pl_chart["year_num"],
            y=pl_chart["net_profit"],
            mode="lines+markers",
            name="Net Profit",
            line=dict(color="#f97316", width=3)
        )

        fig.update_layout(
            template="plotly_dark",
            height=420,
            margin=dict(l=15, r=15, t=15, b=15),
            legend=dict(
                orientation="h",
                y=1.08
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.info("No Profit & Loss data available.")

# ==========================================
# ROE Trend
# ==========================================

with right:

    st.subheader("ROE Trend")

    if not ratios.empty:

        trend = ratios.copy()

        trend["year_num"] = pd.to_numeric(
            trend["year"].astype(str).str.extract(r"(\d{4})")[0],
            errors="coerce"
        )

        trend = trend.dropna(subset=["year_num"])
        trend = trend.sort_values("year_num")


        fig2 = px.line(
            trend,
            x="year_num",
            y="return_on_equity_pct",
            markers=True
        )

        fig2.update_traces(
            line=dict(
                color="#16a34a",
                width=3
            )
        )

        fig2.update_layout(
            template="plotly_dark",
            height=420,
            margin=dict(l=15,r=15,t=15,b=15),
            xaxis_title="Year",
            yaxis_title="ROE (%)"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    else:

        st.info("No ratio history available.")

st.divider()

st.subheader("Pros & Cons")

try:
    import sqlite3

    with sqlite3.connect("db/nifty100.db") as conn:
        pc = pd.read_sql_query(
            """
            SELECT *
            FROM prosandcons
            WHERE company_id=?
            """,
            conn,
            params=(company_id,)
        )
    
 

    left, right = st.columns(2)

    pros = []
    cons = []

    if not pc.empty:

        for _, row in pc.iterrows():

            text = str(row.iloc[-1])

            label = str(row.iloc[1]).lower()

            if "pro" in label:
                pros.append(text)
            elif "con" in label:
                cons.append(text)

    with left:

        st.markdown("### Strengths")

        if pros:
            for item in pros:
                st.write("•", item)
        else:
            st.caption("No strengths available.")

    with right:

        st.markdown("### Weaknesses")

        if cons:
            for item in cons:
                st.write("•", item)
        else:
            st.caption("No weaknesses available.")

except Exception as e:

    st.info(f"Unable to load Pros & Cons ({e})")

st.divider()

st.subheader("Latest Financial Ratios")

ratio_columns = [
    ("Return on Equity","return_on_equity_pct"),
    ("Net Profit Margin","net_profit_margin_pct"),
    ("Operating Margin","operating_profit_margin_pct"),
    ("Debt to Equity","debt_to_equity"),
    ("Interest Coverage","interest_coverage"),
    ("Asset Turnover","asset_turnover"),
    ("Free Cash Flow","free_cash_flow_cr"),
    ("Revenue CAGR (5Y)","revenue_cagr_5yr"),
    ("PAT CAGR (5Y)","pat_cagr_5yr"),
    ("EPS CAGR (5Y)","eps_cagr_5yr"),
    ("Composite Score","composite_quality_score"),
]
rows = []

for label, col in ratio_columns:

    if col in latest_ratio.index:

        value = latest_ratio[col]

        if pd.isna(value):
            display = "N/A"
        elif isinstance(value, (int, float)):
            display = f"{value:.2f}"
        else:
            display = str(value)

        rows.append({
            "Metric": label,
            "Value": display
        })

ratio_df = pd.DataFrame(rows)

ratio_df["Metric"] = ratio_df["Metric"].str.replace("_", " ")

st.dataframe(
    ratio_df,
    hide_index=True,
    use_container_width=True,
    height=350
)

st.divider()

st.subheader("Financial History")

history_cols=[
    "year",
    "sales",
    "operating_profit",
    "net_profit",
    "eps"
]

history_cols=[c for c in history_cols if c in pl.columns]

history = pl.copy()

history["year_num"] = pd.to_numeric(
    history["year"].astype(str).str.extract(r"(\d{4})")[0],
    errors="coerce"
)

history = history.sort_values("year_num")

history = history[history_cols].fillna("N/A")

st.dataframe(
    history,
    hide_index=True,
    use_container_width=True,
    height=350)

st.divider()
st.write("")
st.caption("N100 Financial Intelligence Platform • Company Profile")