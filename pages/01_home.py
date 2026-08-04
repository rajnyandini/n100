import streamlit as st
import plotly.express as px
from src.dashboard.utils.db import query

st.set_page_config(page_title="Home", layout="wide")

st.title("🏠 Nifty 100 Dashboard")

# -----------------------------
# Load Latest Data
# -----------------------------

ratios = query("""
SELECT *
FROM financial_ratios
WHERE year <> 'TTM'
""")

market = query("""
SELECT *
FROM market_cap
WHERE year <> 'TTM'
""")

companies = query("""
SELECT
id AS company_id,
company_name
FROM companies
""")

sectors = query("""
SELECT
company_id,
broad_sector,
sub_sector
FROM sectors
""")

# Latest record per company
ratios = (
    ratios
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)

market = (
    market
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)

df = (
    ratios
    .merge(
        market[
            [
                "company_id",
                "market_cap_crore",
                "pe_ratio",
                "pb_ratio",
                "dividend_yield_pct"
            ]
        ],
        on="company_id",
        how="left"
    )
    .merge(
        sectors,
        on="company_id",
        how="left"
    )
    .merge(
        companies,
        on="company_id",
        how="left"
    )
)

# -----------------------------
# Sidebar
# -----------------------------

years = sorted(
    df["year"].dropna().unique().tolist()
)

selected_year = st.sidebar.selectbox(
    "Financial Year",
    years,
    index=len(years)-1
)

df = df[df["year"] == selected_year]

# -----------------------------
# KPI Tiles
# -----------------------------

st.subheader("Market Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total Companies",
        len(df)
    )

    st.metric(
        "Average ROE",
        f"{df['return_on_equity_pct'].mean():.2f}%"
    )

with c2:

    st.metric(
        "Median P/E",
        f"{df['pe_ratio'].median():.2f}"
    )

    st.metric(
        "Median Debt / Equity",
        f"{df['debt_to_equity'].median():.2f}"
    )

with c3:

    st.metric(
        "Median Revenue CAGR (5Y)",
        f"{df['revenue_cagr_5yr'].median():.2f}%"
    )

    debt_free = (
        df["debt_to_equity"]
        .fillna(-1)
        .eq(0)
        .sum()
    )

    st.metric(
        "Debt-Free Companies",
        int(debt_free)
    )

st.divider()

# -----------------------------
# Charts
# -----------------------------

left, right = st.columns([1, 1])

with left:

    st.subheader("Sector Distribution")

    sector_df = (
        df.groupby("broad_sector")
        .size()
        .reset_index(name="Companies")
        .sort_values("Companies", ascending=False)
    )

    fig = px.pie(
        sector_df,
        names="broad_sector",
        values="Companies",
        hole=0.45,
        title="Companies by Broad Sector"
    )

    fig.update_traces(textposition="inside", textinfo="percent+label")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Top 5 Companies by Composite Score")

    cols = [
        "company_id",
        "company_name",
        "composite_quality_score",
        "return_on_equity_pct",
        "revenue_cagr_5yr",
        "pe_ratio"
    ]

    cols = [c for c in cols if c in df.columns]

    top5 = (
        df.sort_values(
            "composite_quality_score",
            ascending=False
        )[cols]
        .head(5)
    )

    st.dataframe(
        top5,
        hide_index=True,
        use_container_width=True
    )

st.divider()

# -----------------------------
# Latest Company Data
# -----------------------------

st.subheader("Latest Financial Snapshot")

display_cols = [
    "company_id",
    "company_name",
    "broad_sector",
    "market_cap_crore",
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "pe_ratio",
    "pb_ratio",
    "dividend_yield_pct",
    "composite_quality_score"
]

display_cols = [c for c in display_cols if c in df.columns]

display_df = (
    df[display_cols]
    .sort_values(
        "composite_quality_score",
        ascending=False
    )
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Data Source: nifty100.db | Latest available financial year | "
    "Market Capitalisation data is simulated."
)