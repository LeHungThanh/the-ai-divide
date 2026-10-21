"""Shared design, charts, and source-trace controls."""
import pandas as pd
import plotly.express as px
import streamlit as st

PALETTE = {"ink": "#17324D", "teal": "#007F86", "coral": "#D96C49", "pale": "#F3F7FA"}


def inject_style() -> None:
    st.markdown("""<style>
    .stApp {background: #F7F9FB; color: #17324D;}
    [data-testid="stSidebar"] {background: #EAF2F5;}
    h1, h2, h3 {color: #17324D; letter-spacing: -.025em;}
    div[data-testid="stMetric"] {background: white; border: 1px solid #DCE6EB;
      border-radius: 12px; padding: 1rem;}
    .block-container {max-width: 1240px; padding-top: 2rem;}
    </style>""", unsafe_allow_html=True)


def header(kicker: str, title: str, introduction: str) -> None:
    st.caption(kicker.upper())
    st.title(title)
    st.markdown(introduction)


def chart(fig, *, key: str) -> None:
    fig.update_layout(
        template="plotly_white", font=dict(family="Arial", color=PALETTE["ink"]),
        margin=dict(l=10, r=10, t=55, b=20),
        hoverlabel=dict(bgcolor="white"),
        legend_title_text="", height=max(370, min(690, fig.layout.height or 410)),
    )
    st.plotly_chart(fig, width="stretch", key=key, config={"displayModeBar": False})


def trace(row: pd.Series | None, title: str = "Source trace for a displayed statistic") -> None:
    with st.expander(title):
        if row is None:
            st.info("No non-missing observation is available for this selection.")
            return
        st.markdown(f"**{row['country_name']} · {int(row['year'])} · {row['percentage']:.2f}%**")
        fields = ["source_dataset", "source_url", "country_code", "year", "size_emp",
                  "size_label", "nace_r2", "industry_label", "indicator_code", "unit",
                  "denominator_definition", "observation_status", "status_label", "source_updated",
                  "retrieved_utc", "raw_file", "raw_sha256", "source_observation_index"]
        details = {field: ("(none)" if pd.isna(row[field]) or row[field] == "" else str(row[field]))
                   for field in fields}
        st.dataframe(pd.DataFrame(details.items(), columns=["Field", "Source value"]),
                     hide_index=True, width="stretch")
        st.caption("The ZIP supplies this observation index and source hash, but contains no raw Eurostat cube for independent cell-level verification.")


def status_note(frame: pd.DataFrame) -> None:
    flagged = frame.loc[frame["observation_status"].ne("")]
    missing = int(frame["percentage"].isna().sum())
    st.caption(f"Selection: {len(frame):,} source cells · {missing:,} missing values · {len(flagged):,} flagged cells. Missing cells are omitted from charts, never treated as zero.")
    if not flagged.empty:
        with st.expander("Quality flags in this selection"):
            st.dataframe(flagged[["country_name", "year", "size_emp", "nace_r2", "percentage", "observation_status", "status_label"]],
                         hide_index=True, width="stretch")


def footer() -> None:
    st.divider()
    st.caption("Eurostat isoc_eb_ai / isoc_eb_ain2 · percentages of the stated denominator · source snapshot updated 15 June 2026")


def country_picker(frame: pd.DataFrame, *, key: str, default: str = "DK") -> str:
    options = (frame[["country_code", "country_name"]].drop_duplicates()
               .sort_values("country_name"))
    mapping = dict(zip(options.country_code, options.country_name))
    codes = list(mapping)
    return st.selectbox("Country", codes, index=codes.index(default) if default in codes else 0,
                        format_func=lambda c: mapping[c], key=key)


def bar(frame: pd.DataFrame, x: str, y: str, *, title: str, color: str = "#007F86", orientation="h"):
    return px.bar(frame, x=x, y=y, orientation=orientation, title=title,
                  color_discrete_sequence=[color], hover_data={x: ":.2f"} if x == "percentage" else None)
