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