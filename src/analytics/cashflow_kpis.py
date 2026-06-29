"""
Financial Ratio Engine
Day 11 – Cash Flow KPIs
"""

from typing import Optional


def free_cash_flow(
    operating_activity: float,
    investing_activity: float
) -> float:
    """
    Free Cash Flow (FCF)

    Formula:
        CFO + CFI

    Negative values are allowed.
    """

    return operating_activity + investing_activity


def cfo_quality_ratio(
    operating_activity: float,
    net_profit: float
) -> Optional[float]:
    """
    CFO / PAT

    Return None if PAT == 0
    """

    if net_profit == 0:
        return None

    return operating_activity / net_profit


def cfo_quality_label(
    ratio: Optional[float]
) -> Optional[str]:
    """
    Classify CFO Quality.

    > 1.0  -> High Quality
    0.5-1.0 -> Moderate
    < 0.5 -> Accrual Risk
    """

    if ratio is None:
        return None

    if ratio > 1:
        return "High Quality"

    if ratio >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(
    investing_activity: float,
    sales: float
) -> Optional[float]:
    """
    CapEx Intensity

    |CFI| / Sales × 100
    """

    if sales <= 0:
        return None

    return abs(investing_activity) / sales * 100


def capex_label(
    intensity: Optional[float]
) -> Optional[str]:
    """
    Asset Light
    Moderate
    Capital Intensive
    """

    if intensity is None:
        return None

    if intensity < 3:
        return "Asset Light"

    if intensity <= 8:
        return "Moderate"

    return "Capital Intensive"


def fcf_conversion_rate(
    free_cash_flow_value: float,
    operating_profit: float
) -> Optional[float]:
    """
    FCF / Operating Profit ×100
    """

    if operating_profit == 0:
        return None

    return (
        free_cash_flow_value /
        operating_profit
    ) * 100


def capital_allocation_pattern(
    operating_activity: float,
    investing_activity: float,
    financing_activity: float,
    cfo_quality: Optional[float] = None
) -> str:
    """
    8-pattern capital allocation classifier.
    """

    cfo = "+" if operating_activity >= 0 else "-"
    cfi = "+" if investing_activity >= 0 else "-"
    cff = "+" if financing_activity >= 0 else "-"

    pattern = (cfo, cfi, cff)

    if pattern == ("+", "-", "-"):
        if cfo_quality is not None and cfo_quality > 1:
            return "Shareholder Returns"
        return "Reinvestor"

    if pattern == ("+", "+", "-"):
        return "Liquidating Assets"

    if pattern == ("-", "+", "+"):
        return "Distress Signal"

    if pattern == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if pattern == ("+", "+", "+"):
        return "Cash Accumulator"

    if pattern == ("-", "-", "-"):
        return "Pre-Revenue"

    if pattern == ("+", "-", "+"):
        return "Mixed"

    return "Other"