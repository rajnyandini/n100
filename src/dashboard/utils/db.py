import sqlite3
import pandas as pd
import streamlit as st

DB = "db/nifty100.db"


@st.cache_data(ttl=600)
def query(sql, params=None):
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query(sql, conn, params=params or ())
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_companies():
    return query("""
        SELECT id AS company_id,
               company_name
        FROM companies
        ORDER BY company_name
    """)


@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):
    sql = """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
    """
    params = [ticker]

    if year:
        sql += " AND year=?"
        params.append(year)

    sql += " ORDER BY year"

    return query(sql, params)


@st.cache_data(ttl=600)
def get_pl(ticker):
    return query("""
        SELECT *
        FROM profitandloss
        WHERE company_id=?
        ORDER BY year
    """, [ticker])


@st.cache_data(ttl=600)
def get_bs(ticker):
    return query("""
        SELECT *
        FROM balancesheet
        WHERE company_id=?
        ORDER BY year
    """, [ticker])


@st.cache_data(ttl=600)
def get_cf(ticker):
    return query("""
        SELECT *
        FROM cashflow
        WHERE company_id=?
        ORDER BY year
    """, [ticker])


@st.cache_data(ttl=600)
def get_sectors():
    return query("""
        SELECT *
        FROM sectors
    """)


@st.cache_data(ttl=600)
def get_peers(group_name):
    return query("""
        SELECT *
        FROM peer_groups
        WHERE peer_group_name=?
    """, [group_name])


@st.cache_data(ttl=600)
def get_valuation(ticker):
    return query("""
        SELECT *
        FROM market_cap
        WHERE company_id=?
        ORDER BY year
    """, [ticker])

@st.cache_data(ttl=600)
def get_all_ratios():
    return query("""
        SELECT *
        FROM financial_ratios
    """)


@st.cache_data(ttl=600)
def get_market_cap():
    return query("""
        SELECT *
        FROM market_cap
    """)


@st.cache_data(ttl=600)
def get_peer_groups():
    return query("""
        SELECT *
        FROM peer_groups
    """)


@st.cache_data(ttl=600)
def get_company(company_id):
    return query("""
        SELECT *
        FROM companies
        WHERE id=?
    """,[company_id])

@st.cache_data(ttl=600)
def get_dashboard_data():
    return query("""
    SELECT

        c.id,
        c.company_name,
        c.about_company,
        c.company_logo,

        c.roce_percentage,

        c.roe_percentage,

        s.broad_sector,
        s.sub_sector,

        fr.year,

        fr.return_on_equity_pct,
        fr.net_profit_margin_pct,
        fr.operating_profit_margin_pct,
        fr.debt_to_equity,
        fr.interest_coverage,
        fr.asset_turnover,
        fr.free_cash_flow_cr,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,
        fr.eps_cagr_5yr,
        fr.composite_quality_score,

        mc.market_cap_crore,
        mc.pe_ratio,
        mc.pb_ratio,
        mc.ev_ebitda,
        mc.dividend_yield_pct

    FROM financial_ratios fr

    LEFT JOIN companies c
        ON fr.company_id=c.id

    LEFT JOIN sectors s
        ON fr.company_id=s.company_id

    LEFT JOIN market_cap mc
        ON fr.company_id = mc.company_id
        AND substr(fr.year, -4) = CAST(mc.year AS TEXT)
    """)

@st.cache_data(ttl=600)
def get_company_profile(company_id):
    return query("""
        SELECT
            c.*,
            s.broad_sector,
            s.sub_sector
        FROM companies c
        LEFT JOIN sectors s
            ON c.id = s.company_id
        WHERE c.id = ?
    """, [company_id])