"""
Reusable Sidebar Components
"""

import streamlit as st
from src.dashboard.utils.db import (
    get_companies,
    get_sectors,
)


def company_selector():
    """Company dropdown."""
    companies = get_companies()

    names = companies["company_name"].tolist()

    selected = st.sidebar.selectbox(
        "🏢 Company",
        names,
    )

    company_id = companies.loc[
        companies["company_name"] == selected,
        "company_id",
    ].iloc[0]

    return company_id, selected


def year_selector(years):
    """Financial year selector."""
    years = sorted([str(y) for y in years if str(y).upper() != "TTM"])

    if not years:
        return None

    return st.sidebar.selectbox(
        "📅 Financial Year",
        years,
        index=len(years) - 1,
    )


def sector_selector():
    """Sector dropdown."""
    sectors = get_sectors()

    values = (
        sectors["broad_sector"]
        .dropna()
        .sort_values()
        .unique()
        .tolist()
    )

    return st.sidebar.selectbox(
        "🏭 Sector",
        values,
    )


def peer_selector(peer_groups):
    """Peer group selector."""
    groups = sorted(peer_groups)

    return st.sidebar.selectbox(
        "🤝 Peer Group",
        groups,
    )