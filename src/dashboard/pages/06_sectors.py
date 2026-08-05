import os
import sys
import plotly.express as px

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd

from src.dashboard.components.styles import load_css
from src.dashboard.utils.db import get_screener_data

st.set_page_config(
    page_title="Sector Analysis",
    layout="wide"
)

load_css()

st.title("Sector Analysis")

df = get_screener_data()

if df.empty:
    st.error("No data available.")
    st.stop()

st.divider()

st.subheader("Sector Distribution")

sector_count = (
    df.groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
)

fig = px.pie(
    sector_count,
    names="broad_sector",
    values="Companies",
    hole=0.5,
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("Average ROE by Sector")

roe = (
    df.groupby("broad_sector")["return_on_equity_pct"]
    .mean()
    .reset_index()
    .sort_values("return_on_equity_pct", ascending=False)
)

fig = px.bar(
    roe,
    x="broad_sector",
    y="return_on_equity_pct",
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("Average PE by Sector")

pe = (
    df.groupby("broad_sector")["pe_ratio"]
    .mean()
    .reset_index()
    .sort_values("pe_ratio", ascending=False)
)

fig = px.bar(
    pe,
    x="broad_sector",
    y="pe_ratio",
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("Sector Statistics")

summary = (
    df.groupby("broad_sector")
    .agg({
        "company_name": "count",
        "market_cap_crore": "mean",
        "return_on_equity_pct": "mean",
        "pe_ratio": "mean"
    })
    .reset_index()
)

summary.columns = [
    "Sector",
    "Companies",
    "Average Market Cap",
    "Average ROE",
    "Average PE"
]

st.dataframe(
    summary,
    hide_index=True,
    use_container_width=True
)