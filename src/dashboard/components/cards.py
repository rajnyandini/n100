"""
Reusable KPI Cards
"""

import streamlit as st
from src.dashboard.utils.formatters import (
    format_currency,
    format_percent,
    format_ratio,
    format_number,
)


def metric_card(title, value, kind="number", delta=None):
    """
    Display a formatted KPI metric.
    """

    if kind == "currency":
        value = format_currency(value)

    elif kind == "percent":
        value = format_percent(value)

    elif kind == "ratio":
        value = format_ratio(value)

    else:
        value = format_number(value)

    st.metric(
        label=title,
        value=value,
        delta=delta,
    )


def kpi_row(metrics):
    """
    metrics = [
        ("Average ROE", 21.4, "percent"),
        ("Median P/E", 32.1, "number"),
        ...
    ]
    """

    cols = st.columns(len(metrics))

    for col, (title, value, kind) in zip(cols, metrics):
        with col:
            metric_card(title, value, kind)