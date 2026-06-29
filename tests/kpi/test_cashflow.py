from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_ratio,
    cfo_quality_label,
    capex_intensity,
    capex_label,
    fcf_conversion_rate,
    capital_allocation_pattern,
)


# ==========================================================
# Day 11 - Cash Flow KPI Tests
# ==========================================================

def test_free_cash_flow():
    assert free_cash_flow(1000, -400) == 600


def test_cfo_quality_ratio():
    assert cfo_quality_ratio(1200, 1000) == 1.2


def test_cfo_quality_ratio_zero_pat():
    assert cfo_quality_ratio(1000, 0) is None


def test_cfo_quality_labels():
    assert cfo_quality_label(1.2) == "High Quality"
    assert cfo_quality_label(0.8) == "Moderate"
    assert cfo_quality_label(0.3) == "Accrual Risk"


def test_capex_intensity():
    assert capex_intensity(-500, 10000) == 5.0


def test_capex_labels():
    assert capex_label(2) == "Asset Light"
    assert capex_label(5) == "Moderate"
    assert capex_label(10) == "Capital Intensive"


def test_fcf_conversion_rate():
    fcf = free_cash_flow(1000, -400)
    assert fcf_conversion_rate(fcf, 800) == 75.0


def test_fcf_conversion_zero_operating_profit():
    fcf = free_cash_flow(1000, -400)
    assert fcf_conversion_rate(fcf, 0) is None


def test_capital_allocation_patterns():
    assert capital_allocation_pattern(100, -50, -20) == "Reinvestor"
    assert capital_allocation_pattern(100, -50, -20, 1.2) == "Shareholder Returns"
    assert capital_allocation_pattern(-100, 50, 20) == "Distress Signal"
    assert capital_allocation_pattern(-100, -50, 20) == "Growth Funded by Debt"
    assert capital_allocation_pattern(100, 50, 20) == "Cash Accumulator"
    assert capital_allocation_pattern(-100, -50, -20) == "Pre-Revenue"
    assert capital_allocation_pattern(100, -50, 20) == "Mixed"