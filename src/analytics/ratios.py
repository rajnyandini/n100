"""
Financial Ratio Engine
Day 08 – Profitability Ratios
"""

from typing import Optional


def net_profit_margin(
    net_profit: float,
    sales: float
) -> Optional[float]:
    """
    Net Profit Margin (%)

    Formula:
        (Net Profit / Sales) × 100

    Edge Case:
        Return None if sales <= 0
    """

    if sales <= 0:
        return None

    return (net_profit / sales) * 100


def operating_profit_margin(
    operating_profit: float,
    sales: float
) -> Optional[float]:
    """
    Operating Profit Margin (%)

    Formula:
        (Operating Profit / Sales) × 100
    """

    if sales <= 0:
        return None

    return (operating_profit / sales) * 100


def opm_crosscheck(
    calculated_opm: Optional[float],
    source_opm: float,
    tolerance: float = 1.0
) -> bool:
    """
    Compare calculated OPM with source OPM.

    Returns:
        True  -> values match
        False -> mismatch (> tolerance)
    """

    if calculated_opm is None:
        return False

    return abs(calculated_opm - source_opm) <= tolerance


def return_on_equity(
    net_profit: float,
    equity_capital: float,
    reserves: float
) -> Optional[float]:
    """
    ROE (%)

    Formula:
        Net Profit /
        (Equity Capital + Reserves)
        × 100
    """

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return (net_profit / equity) * 100


def return_on_capital_employed(
    profit_before_tax: float,
    interest: float,
    equity_capital: float,
    reserves: float,
    borrowings: float
) -> Optional[float]:
    """
    ROCE (%)

    EBIT = Profit Before Tax + Interest

    Capital Employed =
        Equity + Reserves + Borrowings
    """

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    ebit = profit_before_tax + interest

    return (ebit / capital) * 100


def return_on_assets(
    net_profit: float,
    total_assets: float
) -> Optional[float]:
    """
    ROA (%)

    Formula:
        Net Profit / Total Assets × 100
    """

    if total_assets <= 0:
        return None

    return (net_profit / total_assets) * 100   


# ==========================================================
# Day 09 - Leverage & Efficiency Ratios
# ==========================================================

def debt_to_equity(
    borrowings: float,
    equity_capital: float,
    reserves: float
) -> Optional[float]:
    """
    Debt-to-Equity Ratio

    Formula:
        Borrowings / (Equity Capital + Reserves)

    Rules:
    - Return 0 if borrowings == 0
    - Return None if equity <= 0
    """

    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return borrowings / equity


def high_leverage_flag(
    debt_to_equity_ratio: Optional[float]
) -> bool:
    """
    High leverage if D/E > 5.
    Financial-sector exception is handled later
    in the ratio engine.
    """

    if debt_to_equity_ratio is None:
        return False

    return debt_to_equity_ratio > 5


def interest_coverage_ratio(
    operating_profit: float,
    other_income: float,
    interest: float
) -> Optional[float]:
    """
    Interest Coverage Ratio

    Formula:
        (Operating Profit + Other Income)
        / Interest

    Return None if interest == 0.
    """

    if interest == 0:
        return None

    return (operating_profit + other_income) / interest


def icr_label(
    interest: float
) -> Optional[str]:
    """
    Return 'Debt Free'
    when interest expense is zero.
    """

    if interest == 0:
        return "Debt Free"

    return None


def icr_warning(
    icr: Optional[float]
) -> bool:
    """
    Warning if ICR < 1.5
    """

    if icr is None:
        return False

    return icr < 1.5


def net_debt(
    borrowings: float,
    investments: float
) -> float:
    """
    Net Debt

    Borrowings - Investments
    """

    return borrowings - investments


def asset_turnover(
    sales: float,
    total_assets: float
) -> Optional[float]:
    """
    Asset Turnover

    Sales / Total Assets
    """

    if total_assets <= 0:
        return None

    return sales / total_assets