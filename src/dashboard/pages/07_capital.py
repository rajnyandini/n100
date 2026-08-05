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
    get_valuation,
)

st.set_page_config(
    page_title="Valuation Dashboard",
    layout="wide"
)

load_css()

st.title("Valuation Dashboard")

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_id = companies.loc[
    companies["company_name"] == company,
    "company_id"
].iloc[0]

valuation = get_valuation(company_id)

if valuation.empty:
    st.warning("No valuation data available.")
    st.stop()

latest = valuation.iloc[-1]

st.divider()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Market Cap", f"₹ {latest['market_cap_crore']:,.0f} Cr")
c2.metric("PE Ratio", f"{latest['pe_ratio']:.2f}")
c3.metric("PB Ratio", f"{latest['pb_ratio']:.2f}")
c4.metric("EV / EBITDA", f"{latest['ev_ebitda']:.2f}")
c5.metric("Dividend Yield", f"{latest['dividend_yield_pct']:.2f}%")

st.divider()

valuation_chart = valuation.copy()

valuation_chart["year"] = pd.to_numeric(
    valuation_chart["year"],
    errors="coerce"
)

valuation_chart = valuation_chart.dropna(subset=["year"])
valuation_chart = valuation_chart.sort_values("year")

fig = px.line(
    valuation_chart,
    x="year",
    y="market_cap_crore",
    markers=True,
    template="plotly_dark"
)

fig.update_layout(
    title="Market Cap Trend",
    xaxis_title="Year",
    yaxis_title="Market Cap (₹ Cr)"
)

fig.update_traces(
    mode="lines+markers",
    line=dict(width=3)
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False}
)

st.divider()

left, right = st.columns(2)

with left:
    fig_pe = px.line(
        valuation_chart,
        x="year",
        y="pe_ratio",
        markers=True,
        template="plotly_dark",
        title="PE Ratio Trend"
    )
    st.plotly_chart(fig_pe, use_container_width=True)

with right:
    fig_pb = px.line(
        valuation_chart,
        x="year",
        y="pb_ratio",
        markers=True,
        template="plotly_dark",
        title="PB Ratio Trend"
    )
    st.plotly_chart(fig_pb, use_container_width=True)



