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