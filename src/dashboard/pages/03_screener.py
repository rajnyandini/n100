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

st.title("🔎 Stock Screener")

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

st.subheader("Matching Companies")

st.dataframe(
    df[
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
    ],
    use_container_width=True,
    hide_index=True
)