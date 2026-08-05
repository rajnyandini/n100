import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd

from src.dashboard.components.styles import load_css
from src.dashboard.utils.db import get_screener_data

st.set_page_config(
    page_title="Stock Screener",
    layout="wide"
)

load_css()

st.title("Stock Screener")

df = get_screener_data()

if df.empty:
    st.error("No data found.")
    st.stop()

st.sidebar.header("Filters")

sector = st.sidebar.selectbox(
    "Sector",
    ["All"] + sorted(df["broad_sector"].dropna().unique().tolist())
)

if sector != "All":
    df = df[df["broad_sector"] == sector]

roe_min = st.sidebar.slider(
    "Minimum ROE (%)",
    0,
    50,
    10
)

df = df[
    (df["return_on_equity_pct"].fillna(0) >= roe_min)
]

pe_max = st.sidebar.slider(
    "Maximum PE",
    0,
    150,
    40
)

df = df[
    df["pe_ratio"].fillna(999) <= pe_max
]

quality = st.sidebar.slider(
    "Minimum Quality Score",
    0.0,
    5.0,
    2.0
)

df = df[
    df["composite_quality_score"].fillna(0) >= quality
]

st.subheader("Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Companies", len(df))

with c2:
    st.metric(
        "Average ROE",
        f'{df["return_on_equity_pct"].mean():.2f}%'
        if df["return_on_equity_pct"].notna().any()
        else "N/A"
    )

with c3:
    st.metric(
        "Average PE",
        f'{df["pe_ratio"].mean():.2f}'
        if df["pe_ratio"].notna().any()
        else "N/A"
    )

with c4:
    st.metric(
        "Average Market Cap",
        f'₹ {df["market_cap_crore"].mean():,.0f} Cr'
        if df["market_cap_crore"].notna().any()
        else "N/A"
    )

st.divider()

st.subheader(f"Matching Companies ({len(df)})")

sort_by = st.selectbox(
    "Sort By",
    [
        "Market Cap",
        "PE",
        "ROE",
        "Quality Score"
    ]
)

if sort_by == "Market Cap":
    df = df.sort_values("market_cap_crore", ascending=False)

elif sort_by == "PE":
    df = df.sort_values("pe_ratio")

elif sort_by == "ROE":
    df = df.sort_values("return_on_equity_pct", ascending=False)

elif sort_by == "Quality Score":
    df = df.sort_values("composite_quality_score", ascending=False)

display = df[
    [
        "company_name",
        "broad_sector",
        "market_cap_crore",
        "pe_ratio",
        "pb_ratio",
        "return_on_equity_pct",
        "debt_to_equity",
        "composite_quality_score",
    ]
].copy()

display.columns = [
    "Company",
    "Sector",
    "Market Cap (₹ Cr)",
    "PE",
    "PB",
    "ROE (%)",
    "Debt/Equity",
    "Quality Score",
]

display["Market Cap (₹ Cr)"] = display["Market Cap (₹ Cr)"].apply(
    lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A"
)

for col in ["PE", "PB", "ROE (%)", "Debt/Equity", "Quality Score"]:
    display[col] = display[col].apply(
        lambda x: f"{x:.2f}" if pd.notna(x) else "N/A"
    )

st.dataframe(
    display,
    hide_index=True,
    use_container_width=True
)

csv = display.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Results (CSV)",
    data=csv,
    file_name="stock_screener.csv",
    mime="text/csv"
)