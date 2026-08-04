"""
Dashboard Formatting Utilities
"""

import pandas as pd


def format_currency(value):
    """Format INR Crore values."""
    if pd.isna(value):
        return "N/A"

    if abs(value) >= 1000:
        return f"₹{value:,.0f} Cr"

    return f"₹{value:.2f} Cr"


def format_percent(value):
    """Format percentage values."""
    if pd.isna(value):
        return "N/A"

    return f"{value:.2f}%"


def format_ratio(value):
    """Format ratios like D/E."""
    if pd.isna(value):
        return "N/A"

    return f"{value:.2f}"


def format_number(value):
    """Generic numeric formatter."""
    if pd.isna(value):
        return "N/A"

    return f"{value:,.2f}"


def format_market_cap(value):
    """Pretty format market cap."""
    if pd.isna(value):
        return "N/A"

    if value >= 100000:
        return f"₹{value/100000:.2f} Lakh Cr"

    return f"₹{value:,.0f} Cr"


def highlight_positive_negative(value):
    """Return color for positive/negative values."""
    if pd.isna(value):
        return "gray"

    if value > 0:
        return "green"

    if value < 0:
        return "red"

    return "orange"