import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_pl,
)

st.set_page_config(page_title="Company Profile", layout="wide")

st.title("🏢 Company Profile")

companies = get_companies()

company_names = companies["company_name"].tolist()

selected = st.selectbox(
    "Select Company",
    company_names
)

company_id = companies.loc[
    companies["company_name"] == selected,
    "company_id"
].iloc[0]

ratios = get_ratios(company_id)
pl = get_pl(company_id)

if ratios.empty:

    st.warning("Ticker not found — please try another.")

    st.stop()

latest = ratios.iloc[-1]

st.subheader(selected)

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "ROE",
        f"{latest['return_on_equity_pct']:.2f}%"
    )

    st.metric(
        "ROCE",
        f"{latest.get('roce_pct',0):.2f}%"
    )

with c2:

    st.metric(
        "Net Profit Margin",
        f"{latest['net_profit_margin_pct']:.2f}%"
    )

    st.metric(
        "Debt / Equity",
        f"{latest['debt_to_equity']:.2f}"
    )

with c3:

    st.metric(
        "Revenue CAGR",
        f"{latest['revenue_cagr_5yr']:.2f}%"
    )

    st.metric(
        "Free Cash Flow",
        f"{latest['free_cash_flow_cr']:.0f} Cr"
    )

st.divider()

st.subheader("Revenue vs Net Profit")

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=pl["year"],
        y=pl["sales"],
        name="Revenue"
    )
)

fig.add_trace(
    go.Scatter(
        x=pl["year"],
        y=pl["net_profit"],
        mode="lines+markers",
        name="Net Profit"
    )
)

fig.update_layout(
    height=500,
    xaxis_title="Year",
    yaxis_title="₹ Crore"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.divider()

# ---------------------------------
# ROE vs ROCE Trend
# ---------------------------------

st.subheader("ROE vs ROCE Trend")

trend = ratios.copy()

if "roce_pct" not in trend.columns:
    trend["roce_pct"] = None

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=trend["year"],
        y=trend["return_on_equity_pct"],
        mode="lines+markers",
        name="ROE"
    )
)

fig2.add_trace(
    go.Scatter(
        x=trend["year"],
        y=trend["roce_pct"],
        mode="lines+markers",
        name="ROCE"
    )
)

fig2.update_layout(
    height=450,
    xaxis_title="Year",
    yaxis_title="Percent"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.divider()

# ---------------------------------
# Company Information
# ---------------------------------

company_info = pd.read_sql_query(
    """
    SELECT *
    FROM companies
    WHERE id=?
    """,
    __import__("sqlite3").connect("db/nifty100.db"),
    params=(company_id,)
)

if not company_info.empty:

    info = company_info.iloc[0]

    st.subheader("Company Information")

    c1, c2 = st.columns(2)

    with c1:

        st.write("**Company ID:**", info["id"])

        if "company_name" in info:
            st.write("**Company:**", info["company_name"])

        if "nse_code" in info:
            st.write("**NSE:**", info["nse_code"])

        if "bse_code" in info:
            st.write("**BSE:**", info["bse_code"])

    with c2:

        if "roe_percentage" in info:
            st.write("**Source ROE:**", info["roe_percentage"])

        if "roce_percentage" in info:
            st.write("**Source ROCE:**", info["roce_percentage"])

        if "market_cap" in info:
            st.write("**Market Cap:**", info["market_cap"])

st.divider()

# ---------------------------------
# Pros & Cons
# ---------------------------------

st.subheader("Pros & Cons")

try:

    import sqlite3

    conn = sqlite3.connect("db/nifty100.db")

    pc = pd.read_sql_query(
        """
        SELECT *
        FROM prosandcons
        WHERE company_id=?
        """,
        conn,
        params=(company_id,)
    )

    conn.close()

    if not pc.empty:

        left, right = st.columns(2)

        with left:

            st.markdown("### ✅ Pros")

            pros = pc[
                pc.iloc[:,1].astype(str)
                .str.contains("pro",case=False,na=False)
            ]

            if len(pros)==0:
                st.write("No data available")

            for _,row in pros.iterrows():
                st.success(row.iloc[-1])

        with right:

            st.markdown("### ❌ Cons")

            cons = pc[
                pc.iloc[:,1].astype(str)
                .str.contains("con",case=False,na=False)
            ]

            if len(cons)==0:
                st.write("No data available")

            for _,row in cons.iterrows():
                st.error(row.iloc[-1])

    else:

        st.info("No pros & cons available.")

except Exception as e:

    st.warning(f"Unable to load Pros & Cons ({e})")

st.divider()

# ---------------------------------
# Latest Financial Ratios
# ---------------------------------

st.subheader("Latest Financial Ratios")

ratio_cols = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "revenue_cagr_3yr",
    "revenue_cagr_5yr",
    "pat_cagr_3yr",
    "pat_cagr_5yr",
    "eps_cagr_3yr",
    "eps_cagr_5yr",
    "composite_quality_score"
]

available = [c for c in ratio_cols if c in latest.index]

ratio_df = pd.DataFrame({
    "Metric": available,
    "Value": [latest[c] for c in available]
})

ratio_df["Value"] = ratio_df["Value"].fillna("N/A")

st.dataframe(
    ratio_df,
    hide_index=True,
    use_container_width=True
)

st.divider()

# ---------------------------------
# Financial History
# ---------------------------------

st.subheader("Financial History")

history_cols = [
    "year",
    "sales",
    "net_profit",
    "eps"
]

history_cols = [c for c in history_cols if c in pl.columns]

history = pl[history_cols].copy()

history = history.fillna("N/A")

st.dataframe(
    history,
    hide_index=True,
    use_container_width=True
)

st.divider()

st.success("Company profile loaded successfully.")