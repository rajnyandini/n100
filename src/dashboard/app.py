import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

from src.dashboard.components.styles import load_css

st.set_page_config(
    page_title="N100 Financial Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

st.markdown("""
<h1>N100 Financial Intelligence Platform</h1>
<p style="font-size:18px;color:#9CA3AF;margin-top:-10px;">
Professional Equity Research & Financial Analytics Dashboard
</p>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

cards = [
    ("Companies", "92"),
    ("Peer Groups", "11"),
    ("Financial Ratios", "50+"),
    ("Years Covered", "10+")
]

for col, (title, value) in zip([c1, c2, c3, c4], cards):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("## Dashboard Modules")

left, right = st.columns(2)

with left:
    st.markdown("""
<div class="panel">

### Analytics

- Overview
- Company Profile
- Stock Screener
- Peer Comparison

</div>
""", unsafe_allow_html=True)

with right:
    st.markdown("""
<div class="panel">

### Insights

- Trend Analysis
- Sector Analysis
- Capital Allocation
- Reports

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="panel">

### About

This dashboard provides financial analytics for the Nifty 100 universe using
SQLite, Python, Plotly and Streamlit.

Features include:

- Financial ratio analysis
- Stock screening
- Peer benchmarking
- Trend visualization
- Sector analytics
- Capital allocation insights
- Company reports

</div>
""", unsafe_allow_html=True)