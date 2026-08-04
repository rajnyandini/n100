"""Year label parsing. Source year labels appear as 'YYYY', 'Mon YYYY', or 'TTM'."""

_MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
    "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
    "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}


def year_sort_key(value):
    """Return a numeric key so labels sort chronologically. TTM sorts as most recent."""
    if value is None:
        return -1

    v = str(value).strip()

    if v.upper() == "TTM":
        return 999912

    parts = v.split()

    if len(parts) == 2 and parts[0] in _MONTHS:
        return int(parts[1]) * 12 + _MONTHS[parts[0]]

    if v.isdigit():
        return int(v) * 12

    return -1


def latest_per_group(df, group_col="company_id", year_col="year", exclude_ttm=False):
    """Return one row per group_col = the chronologically latest year_col."""
    d = df.copy()

    if exclude_ttm:
        d = d[d[year_col].astype(str).str.upper() != "TTM"]

    d["_yk"] = d[year_col].map(year_sort_key)

    d = (
        d.sort_values("_yk")
         .groupby(group_col, as_index=False)
         .tail(1)
    )

    return d.drop(columns="_yk")