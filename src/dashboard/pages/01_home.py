import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import plotly.express as px

from src.dashboard.components.styles import load_css
from src.dashboard.utils.db import get_dashboard_data

st.set_page_config(page_title="Overview", layout="wide")

load_css()

df = get_dashboard_data()

if df.empty:
    st.error("No data found.")
    st.stop()

# Latest available year

import pandas as pd

df["year_num"] = pd.to_numeric(
    df["year"].astype(str).str.extract(r"(\d{4})")[0],
    errors="coerce"
)

df = df.dropna(subset=["year_num"]).copy()
df["year_num"] = df["year_num"].astype(int)

years = sorted(df["year_num"].unique())

year = st.sidebar.selectbox(
    "Financial Year",
    years,
    index=len(years) - 1
)

df = df[df["year_num"] == year]

st.title("Overview")
st.caption("N100 Financial Intelligence Platform")

# ---------------- KPI ---------------- #

c1, c2, c3, c4 = st.columns(4)

c1.metric("Companies", df["id"].nunique())

c2.metric(
    "Average ROE",
    f"{df['return_on_equity_pct'].mean():.2f}%"
)

c3.metric(
    "Median PE",
    f"{df['pe_ratio'].median():.2f}"
)

c4.metric(
    "Avg Quality Score",
    f"{df['composite_quality_score'].mean():.1f}"
)

st.divider()

# ---------------- Charts ---------------- #

left, right = st.columns((1.3,1))

with left:

    st.subheader("Sector Distribution")

    sector = (
        df.groupby("broad_sector")
        .size()
        .reset_index(name="Companies")
    )

    fig = px.pie(
        sector,
        names="broad_sector",
        values="Companies",
        hole=.55,
    )

    fig.update_layout(height=420)

    st.plotly_chart(fig, use_container_width=True)

with right:

    st.subheader("Top Quality Companies")

    top = (
        df[
            [
                "company_name",
                "return_on_equity_pct",
                "composite_quality_score"
            ]
        ]
        .sort_values(
            "composite_quality_score",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top,
        use_container_width=True,
        hide_index=True,
        height=420
    )

st.divider()

st.subheader("Market Snapshot")

snapshot = df[
    [
        "company_name",
        "broad_sector",
        "market_cap_crore",
        "pe_ratio",
        "pb_ratio",
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "composite_quality_score"
    ]
].sort_values(
    "composite_quality_score",
    ascending=False
)

st.dataframe(
    snapshot,
    use_container_width=True,
    hide_index=True,
    height=550
)