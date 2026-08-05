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