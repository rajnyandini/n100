from src.etl.loader import normalize_year, normalize_ticker


# normalize_year tests

def test_year_1():
    assert normalize_year("Mar 2014") == 2014

def test_year_2():
    assert normalize_year("Dec 2012") == 2012

def test_year_3():
    assert normalize_year("FY2020") == 2020

def test_year_4():
    assert normalize_year("2021") == 2021

def test_year_5():
    assert normalize_year("FY 2022") == 2022

def test_year_6():
    assert normalize_year("Mar 2023") == 2023

def test_year_7():
    assert normalize_year("Dec 2024") == 2024

def test_year_8():
    assert normalize_year(2025) == 2025

def test_year_9():
    assert normalize_year("2019") == 2019

def test_year_10():
    assert normalize_year("FY2018") == 2018

def test_year_none():
    assert normalize_year(None) is None


# normalize_ticker tests

def test_ticker_1():
    assert normalize_ticker("ABB") == "ABB"

def test_ticker_2():
    assert normalize_ticker("abb") == "ABB"

def test_ticker_3():
    assert normalize_ticker(" abb ") == "ABB"

def test_ticker_4():
    assert normalize_ticker("TCS.NS") == "TCSNS"

def test_ticker_5():
    assert normalize_ticker("HDFC-BANK") == "HDFCBANK"

def test_ticker_6():
    assert normalize_ticker("RELIANCE") == "RELIANCE"

def test_ticker_none():
    assert normalize_ticker(None) is None