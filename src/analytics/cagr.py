"""
Financial Ratio Engine
Day 10 – CAGR Engine
"""

from typing import Optional, Tuple


def calculate_cagr(
    start_value: float,
    end_value: float,
    years: int
) -> Tuple[Optional[float], Optional[str]]:
    """
    Generic CAGR Calculator.

    Returns
    -------
    (cagr_value, flag)

    flag is one of:

    None
    ZERO_BASE
    INSUFFICIENT
    TURNAROUND
    DECLINE_TO_LOSS
    BOTH_NEGATIVE
    """

    if years <= 0:
        return None, "INSUFFICIENT"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    cagr = (
        ((end_value / start_value) ** (1 / years))
        - 1
    ) * 100

    return cagr, None