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

def test_year_11():
    assert normalize_year("Jan 2010") == 2010

def test_year_12():
    assert normalize_year("Feb 2011") == 2011

def test_year_13():
    assert normalize_year("Apr 2018") == 2018

def test_year_14():
    assert normalize_year("May 2019") == 2019

def test_year_15():
    assert normalize_year("Jun 2020") == 2020

def test_year_16():
    assert normalize_year("Jul 2021") == 2021

def test_year_17():
    assert normalize_year("Aug 2022") == 2022

def test_year_18():
    assert normalize_year("Sep 2023") == 2023

def test_year_19():
    assert normalize_year("Oct 2024") == 2024

def test_year_20():
    assert normalize_year("Nov 2025") == 2025

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

def test_ticker_8():
    assert normalize_ticker("INFY") == "INFY"

def test_ticker_9():
    assert normalize_ticker("infy") == "INFY"

def test_ticker_10():
    assert normalize_ticker("SBI") == "SBI"

def test_ticker_11():
    assert normalize_ticker("sbi ") == "SBI"

def test_ticker_12():
    assert normalize_ticker("HCL-TECH") == "HCLTECH"

def test_ticker_13():
    assert normalize_ticker("LT.NS") == "LTNS"

def test_ticker_14():
    assert normalize_ticker(" ITC ") == "ITC"

def test_ticker_15():
    assert normalize_ticker("ASIAN-PAINTS") == "ASIANPAINTS"

def test_ticker_none():
    assert normalize_ticker(None) is None