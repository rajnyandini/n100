import os
import sys

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
    get_valuation,
)

st.set_page_config(
    page_title="Reports",
    layout="wide"
)

load_css()

st.title("Reports")

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
valuation = get_valuation(company_id)

report_type = st.radio(
    "Choose Report",
    [
        "Financial History",
        "Financial Ratios",
        "Valuation History"
    ],
    horizontal=True
)

if report_type == "Financial History":
    report = pl

elif report_type == "Financial Ratios":
    report = ratios

else:
    report = valuation

st.dataframe(
    report,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "⬇ Download CSV",
    report.to_csv(index=False),
    file_name=f"{company}_{report_type}.csv",
    mime="text/csv"
)

