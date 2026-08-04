"""
Dashboard Constants
"""

PAGE_TITLE = "N100 Financial Intelligence Platform"

PAGE_ICON = "📈"

LAYOUT = "wide"

SIDEBAR_STATE = "expanded"

DB_PATH = "db/nifty100.db"

SIMULATED_LABEL = "⚠️ Market Cap & Stock Prices are simulated datasets."

PRIMARY_COLOR = "#2563EB"
SUCCESS_COLOR = "#16A34A"
WARNING_COLOR = "#F59E0B"
DANGER_COLOR = "#DC2626"

KPI_COLUMNS = [
    "return_on_equity_pct",
    "roce_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr",
    "free_cash_flow_cr",
    "interest_coverage",
    "asset_turnover",
    "composite_quality_score",
]

SCREENER_PRESETS = [
    "Quality Compounder",
    "Value Pick",
    "Growth Accelerator",
    "Dividend Champion",
    "Debt-Free Blue Chip",
    "Turnaround Watch",
]