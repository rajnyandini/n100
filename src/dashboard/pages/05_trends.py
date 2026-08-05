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
    get_ratios,
    get_pl,
)

st.set_page_config(
    page_title="Financial Trends",
    layout="wide"
)

load_css()

st.title("Financial Trends")

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_id = companies.loc[
    companies["company_name"] == company,
    "company_id"
].iloc[0]

ratios = get_ratios(company_id)
pl = get_pl(company_id)

st.divider()

st.subheader("Revenue Trend")

if not pl.empty:

    revenue = pl.copy()

    revenue["year_num"] = pd.to_numeric(
        revenue["year"].astype(str).str.extract(r"(\d{4})")[0],
        errors="coerce"
    )

    revenue = revenue.dropna(subset=["year_num"])
    revenue = revenue.sort_values("year_num")

    fig = px.line(
        revenue,
        x="year_num",
        y="sales",
        markers=True,
        template="plotly_dark"
    )

    fig.update_layout(
        height=450,
        xaxis_title="Year",
        yaxis_title="Revenue (₹ Cr)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

st.subheader("Net Profit Trend")

if not pl.empty:

    profit = pl.copy()

    profit["year_num"] = pd.to_numeric(
        profit["year"].astype(str).str.extract(r"(\d{4})")[0],
        errors="coerce"
    )

    profit = profit.dropna(subset=["year_num"])
    profit = profit.sort_values("year_num")

    fig = px.line(
        profit,
        x="year_num",
        y="net_profit",
        markers=True,
        template="plotly_dark"
    )

    fig.update_traces(line=dict(width=3))

    fig.update_layout(
        height=450,
        xaxis_title="Year",
        yaxis_title="Net Profit (₹ Cr)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

st.subheader("ROE Trend")

if not ratios.empty:

    roe = ratios.copy()

    roe["year_num"] = pd.to_numeric(
        roe["year"].astype(str).str.extract(r"(\d{4})")[0],
        errors="coerce"
    )

    roe = roe.dropna(subset=["year_num"])
    roe = roe.sort_values("year_num")

    fig = px.line(
        roe,
        x="year_num",
        y="return_on_equity_pct",
        markers=True,
        template="plotly_dark"
    )

    fig.update_traces(line=dict(width=3))

    fig.update_layout(
        height=450,
        xaxis_title="Year",
        yaxis_title="ROE (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

st.subheader("Free Cash Flow")

if not ratios.empty:

    fcf = ratios.copy()

    fcf["year_num"] = pd.to_numeric(
        fcf["year"].astype(str).str.extract(r"(\d{4})")[0],
        errors="coerce"
    )

    fcf = fcf.dropna(subset=["year_num"])
    fcf = fcf.sort_values("year_num")

    fig = px.bar(
        fcf,
        x="year_num",
        y="free_cash_flow_cr",
        template="plotly_dark"
    )

    fig.update_layout(
        height=450,
        xaxis_title="Year",
        yaxis_title="Free Cash Flow (₹ Cr)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

