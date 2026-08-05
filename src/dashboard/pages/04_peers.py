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
    get_valuation,
)

st.set_page_config(
    page_title="Peer Comparison",
    layout="wide"
)

load_css()

st.title("Peer Comparison")

companies = get_companies()

company_names = companies["company_name"].tolist()

left, right = st.columns(2)

with left:

    company1 = st.selectbox(
        "Company A",
        company_names,
        key="company1"
    )

with right:

    company2 = st.selectbox(
        "Company B",
        company_names,
        index=1 if len(company_names) > 1 else 0,
        key="company2"
    )

id1 = companies.loc[
    companies["company_name"] == company1,
    "company_id"
].iloc[0]

id2 = companies.loc[
    companies["company_name"] == company2,
    "company_id"
].iloc[0]

profile1 = get_company_profile(id1).iloc[0]
profile2 = get_company_profile(id2).iloc[0]

ratio1 = get_ratios(id1).iloc[-1]
ratio2 = get_ratios(id2).iloc[-1]

valuation1 = get_valuation(id1).iloc[-1]
valuation2 = get_valuation(id2).iloc[-1]

st.divider()

def fmt(value, percent=False):
    if pd.isna(value):
        return "N/A"

    if percent:
        return f"{value:.2f}%"

    return f"{value:,.2f}"

comparison = pd.DataFrame({
    "Metric": [
        "Market Cap",
        "PE",
        "PB",
        "ROE",
        "ROCE",
        "Debt / Equity"
    ],

    company1: [
        fmt(valuation1["market_cap_crore"]),
        fmt(valuation1["pe_ratio"]),
        fmt(valuation1["pb_ratio"]),
        fmt(ratio1["return_on_equity_pct"], True),
        fmt(profile1["roce_percentage"], True),
        fmt(ratio1["debt_to_equity"]),
    ],

    company2: [
        fmt(valuation2["market_cap_crore"]),
        fmt(valuation2["pe_ratio"]),
        fmt(valuation2["pb_ratio"]),
        fmt(ratio2["return_on_equity_pct"], True),
        fmt(profile2["roce_percentage"], True),
        fmt(ratio2["debt_to_equity"]),
    ]
})

st.subheader("Comparison Table")

st.dataframe(
    comparison,
    hide_index=True,
    use_container_width=True
)

st.divider()

st.subheader("Visual Comparison")

chart = pd.DataFrame({
    "Metric": [
        "PE",
        "PB",
        "ROCE"
    ],
    company1: [
        valuation1["pe_ratio"],
        valuation1["pb_ratio"],
        profile1["roce_percentage"],
    ],
    company2: [
        valuation2["pe_ratio"],
        valuation2["pb_ratio"],
        profile2["roce_percentage"],
    ]
})

chart = chart.melt(
    id_vars="Metric",
    var_name="Company",
    value_name="Value"
)

fig = px.bar(
    chart,
    x="Metric",
    y="Value",
    color="Company",
    barmode="group",
    template="plotly_dark",
)

fig.update_layout(
    height=500,
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True
)