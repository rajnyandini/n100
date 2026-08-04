"""
Reusable Dashboard Tables
"""

import streamlit as st
import pandas as pd


def show_table(df, title=None, height=450):
    """Display a dataframe."""
    if title:
        st.subheader(title)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=height,
    )


def top_n(df, column, n=5, ascending=False):
    """Return top/bottom N rows."""
    if column not in df.columns:
        return pd.DataFrame()

    return (
        df.sort_values(column, ascending=ascending)
        .head(n)
        .reset_index(drop=True)
    )


def metric_table(df, columns):
    """Display selected metric columns."""
    cols = [c for c in columns if c in df.columns]

    if not cols:
        st.info("No data available.")
        return

    st.dataframe(
        df[cols],
        use_container_width=True,
        hide_index=True,
    )


def download_csv(df, filename="export.csv"):
    """CSV download button."""
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv",
    )