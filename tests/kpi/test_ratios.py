import pytest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    opm_crosscheck,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
)


def test_net_profit_margin_normal():
    assert net_profit_margin(100, 1000) == 10.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin_normal():
    assert operating_profit_margin(250, 1000) == 25.0


def test_opm_crosscheck_match():
    assert opm_crosscheck(25.0, 25.4, tolerance=1.0)


def test_opm_crosscheck_mismatch():
    assert not opm_crosscheck(25.0, 27.5, tolerance=1.0)


def test_return_on_equity_negative_equity():
    assert return_on_equity(100, -100, 50) is None


def test_return_on_capital_employed_normal():
    result = return_on_capital_employed(
        500,
        50,
        1000,
        2000,
        500
    )

    assert round(result, 2) == 15.71


def test_return_on_assets_zero_assets():
    assert return_on_assets(100, 0) is None


# ==========================================================
# Day 09 Tests
# ==========================================================

from src.analytics.ratios import (
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning,
    net_debt,
    asset_turnover,
)


def test_debt_to_equity_normal():
    assert debt_to_equity(500, 1000, 500) == 500 / 1500


def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 1000, 500) == 0


def test_debt_to_equity_negative_equity():
    assert debt_to_equity(100, -500, 200) is None


def test_high_leverage_flag():
    assert high_leverage_flag(6)


def test_interest_coverage_zero_interest():
    assert interest_coverage_ratio(600, 50, 0) is None


def test_icr_label_debt_free():
    assert icr_label(0) == "Debt Free"


def test_icr_warning():
    assert icr_warning(1.2)
    assert not icr_warning(2.5)


def test_asset_turnover_zero_assets():
    assert asset_turnover(5000, 0) is None  