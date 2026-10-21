"""Load and select Eurostat observations without changing missing values."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
FILES = {
    "country": "01_country_adoption.csv",
    "size": "02_company_size.csv",
    "industry": "03_industry_adoption.csv",
    "barrier": "04_ai_adoption_barriers.csv",
}
EU = "EU27_2020"
OVERALL = "C10-S951_X_K"
ADOPTION = "E_AI_TANY"
PERCENT_ENTERPRISES = "PC_ENT"
CONSIDERED = "PC_ENT_AI_EC"
SIZES = {"10-49": "Small (10–49)", "50-249": "Medium (50–249)", "GE250": "Large (250+)"}
SECTORS = {"C", "D", "E", "F", "G", "H", "I", "J", "L", "M", "N", "S951"}


def load(name: str) -> pd.DataFrame:
    """Return a fresh frame. Missing percentages stay NaN; provenance stays text."""
    if name not in FILES:
        raise KeyError(name)
    path = DATA / FILES[name]
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Extract processed.zip into data/processed/.")
    frame = pd.read_csv(
        path,
        dtype={"country_code": "string", "nace_r2": "string", "size_emp": "string",
               "indicator_code": "string", "unit": "string", "observation_status": "string",
               "raw_sha256": "string", "source_observation_index": "Int64"},
        keep_default_na=True,
    )
    frame["year"] = pd.to_numeric(frame["year"], errors="raise").astype(int)
    frame["percentage"] = pd.to_numeric(frame["percentage"], errors="coerce")
    frame["observation_status"] = frame["observation_status"].fillna("")
    frame["status_label"] = frame["status_label"].fillna("")
    return frame


def adoption(frame: pd.DataFrame, *, size: str | None = "GE10", sector: str | None = OVERALL) -> pd.DataFrame:
    mask = (
        frame["indicator_code"].eq(ADOPTION)
        & frame["unit"].eq(PERCENT_ENTERPRISES)
    )
    if size is not None:
        mask &= frame["size_emp"].eq(size)
    if sector is not None:
        mask &= frame["nace_r2"].eq(sector)
    return frame.loc[mask].copy()


def comparison_sectors(frame: pd.DataFrame) -> pd.DataFrame:
    """Use a nonoverlapping NACE selection; source includes overlapping aggregates."""
    return frame.loc[frame["nace_r2"].isin(SECTORS)].copy()


def barriers(frame: pd.DataFrame, *, size: str | None = "GE10") -> pd.DataFrame:
    """Publication-compatible denominator: AI nonusers who had considered use."""
    mask = frame["unit"].eq(CONSIDERED) & frame["nace_r2"].eq(OVERALL)
    if size is not None:
        mask &= frame["size_emp"].eq(size)
    return frame.loc[mask].copy()


def record(frame: pd.DataFrame, **filters) -> pd.Series | None:
    rows = frame
    for column, value in filters.items():
        rows = rows.loc[rows[column].eq(value)]
    rows = rows.dropna(subset=["percentage"])
    return None if rows.empty else rows.iloc[0]


def years(*frames: pd.DataFrame) -> list[int]:
    return sorted(set.intersection(*(set(f["year"].unique()) for f in frames)))
