"""Comparable barrier observations for the Adoption Barriers page."""

import pandas as pd

from src.data import CONSIDERED, EU, OVERALL, barriers


def _selection(frame: pd.DataFrame, country: str, year: int) -> pd.DataFrame:
    """Keep the source denominator and overall activity definition explicit."""
    selected = barriers(frame, size=None)
    return selected.loc[
        selected["country_code"].isin([country, EU])
        & selected["year"].eq(year)
        & selected["unit"].eq(CONSIDERED)
        & selected["nace_r2"].eq(OVERALL)
    ].copy()


def _wide_pair(rows: pd.DataFrame, left_code: str, right_code: str,
               left_name: str, right_name: str) -> pd.DataFrame:
    """Create one row per barrier, retaining source labels and missing values."""
    values = rows.pivot(index="indicator_code", columns="size_emp", values="percentage")
    labels = rows.drop_duplicates("indicator_code").set_index("indicator_code")["indicator_label"]
    result = pd.DataFrame({
        "indicator_code": values.index,
        "indicator_label": labels.reindex(values.index).to_numpy(),
        left_name: values[left_code] if left_code in values else float("nan"),
        right_name: values[right_code] if right_code in values else float("nan"),
    }).reset_index(drop=True)
    flags = rows.pivot(index="indicator_code", columns="size_emp", values="observation_status")
    result[f"{left_name.removesuffix('_pct')}_status"] = (
        flags[left_code].reindex(values.index).fillna("").to_numpy()
        if left_code in flags else ""
    )
    result[f"{right_name.removesuffix('_pct')}_status"] = (
        flags[right_code].reindex(values.index).fillna("").to_numpy()
        if right_code in flags else ""
    )
    result["difference_pp"] = result[left_name] - result[right_name]
    return result


def size_barrier_comparison(frame: pd.DataFrame, country: str, year: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compare small (10–49) with large (250+) firms; return rows and source cells."""
    rows = _selection(frame, country, year)
    rows = rows.loc[rows["country_code"].eq(country)
                    & rows["size_emp"].isin(["10-49", "GE250"])]
    source = rows.copy()
    return _wide_pair(rows, "10-49", "GE250", "small_pct", "large_pct"), source


def country_eu_barrier_comparison(frame: pd.DataFrame, country: str, year: int,
                                  size: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compare one country with Eurostat's supplied EU27 aggregate at one size."""
    rows = _selection(frame, country, year)
    rows = rows.loc[rows["size_emp"].eq(size)]
    rows = rows.loc[rows["country_code"].isin([country, EU])]
    values = rows.pivot(index="indicator_code", columns="country_code", values="percentage")
    labels = rows.drop_duplicates("indicator_code").set_index("indicator_code")["indicator_label"]
    result = pd.DataFrame({
        "indicator_code": values.index,
        "indicator_label": labels.reindex(values.index).to_numpy(),
        "country_pct": values[country] if country in values else float("nan"),
        "eu_pct": values[EU] if EU in values else float("nan"),
    }).reset_index(drop=True)
    flags = rows.pivot(index="indicator_code", columns="country_code", values="observation_status")
    result["country_status"] = (
        flags[country].reindex(values.index).fillna("").to_numpy()
        if country in flags else ""
    )
    result["eu_status"] = (
        flags[EU].reindex(values.index).fillna("").to_numpy()
        if EU in flags else ""
    )
    result["difference_pp"] = result["country_pct"] - result["eu_pct"]
    source = rows.copy()
    return result, source
