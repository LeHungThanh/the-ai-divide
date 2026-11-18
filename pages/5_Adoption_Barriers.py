import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

from src.barrier_comparisons import country_eu_barrier_comparison, size_barrier_comparison
from src.data import CONSIDERED, EU, load, barriers
from src.ui import header, insight, chart, country_picker, footer, trace, status_note

NAMES = {
    "E_AI_BLE": "Lack of expertise", "E_AI_BLEG": "Legal uncertainty",
    "E_AI_BCDP": "Data protection / privacy", "E_AI_BCST": "Cost",
    "E_AI_BINC": "System incompatibility", "E_AI_BDDT": "Data availability / quality",
    "E_AI_BEC": "Ethical concerns", "E_AI_BNU": "Not useful for enterprise",
}
SMALL_COLOR = "#246B8E"
LARGE_COLOR = "#B65F3D"
EU_COLOR = "#246B8E"
COUNTRY_COLOR = "#B65F3D"


def size_dumbbell(comparison, country_name: str, year: int):
    data = comparison.dropna(subset=["small_pct", "large_pct"], how="all").copy()
    if data.empty:
        return None
    data["barrier"] = data["indicator_code"].map(NAMES).fillna(data["indicator_label"])
    data["abs_gap"] = data["difference_pp"].abs()
    data = data.sort_values("abs_gap", ascending=False, na_position="last").reset_index(drop=True)
    positions = list(range(len(data)))
    small_y, large_y = [], []
    connector_x, connector_y = [], []
    for y, row in zip(positions, data.itertuples()):
        small_y.append(y - 0.12)
        large_y.append(y + 0.12)
        if pd.notna(row.small_pct) and pd.notna(row.large_pct):
            connector_x.extend([row.small_pct, row.large_pct, None])
            connector_y.extend([y - 0.12, y + 0.12, None])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=connector_x, y=connector_y, mode="lines",
                             line=dict(color="#A7B7BF", width=1.5),
                             hoverinfo="skip", showlegend=False))
    for column, ys, label, color, symbol, is_small in [
        ("small_pct", small_y, "Small · 10–49", SMALL_COLOR, "circle", True),
        ("large_pct", large_y, "Large · 250+", LARGE_COLOR, "diamond", False),
    ]:
        valid = data[column].notna()
        subset = data.loc[valid]
        flag_column = "small_status" if is_small else "large_status"
        point_ys = [value for value, keep in zip(ys, valid) if keep]
        positions_text = []
        for row in subset.itertuples():
            if pd.isna(row.small_pct) or pd.isna(row.large_pct):
                positions_text.append("middle right")
            elif (row.small_pct < row.large_pct) == is_small:
                positions_text.append("middle left")
            else:
                positions_text.append("middle right")
        fig.add_trace(go.Scatter(
            x=subset[column], y=point_ys, mode="markers+text", name=label,
            marker=dict(color=color, size=11, symbol=symbol,
                        line=dict(color="white", width=1.5)),
            text=[f"{value:.1f}%" for value in subset[column]],
            textposition=positions_text, textfont=dict(size=10, color="#17324D"),
            customdata=list(zip(subset["barrier"], subset["difference_pp"], subset[flag_column])),
            hovertemplate=("%{customdata[0]}<br>" + label + ": %{x:.2f}%"
                           "<br>Small minus large: %{customdata[1]:+.2f} pp"
                           "<br>Eurostat flag: %{customdata[2]}<extra></extra>"),
        ))
    fig.update_layout(title=f"Reported barrier shares by enterprise size · {country_name} · {year}",
                      height=470, xaxis_title="Enterprises that considered AI but did not adopt it (%)",
                      yaxis_title="", barmode="overlay", showlegend=True,
                      legend=dict(orientation="h", y=-0.16, x=0.02))
    fig.update_xaxes(range=[0, 100], ticksuffix="%")
    fig.update_yaxes(tickmode="array", tickvals=positions, ticktext=data["barrier"],
                     autorange="reversed", range=[len(data) - 0.45, -0.45], fixedrange=True)
    return fig, data


def country_eu_bars(comparison, country_name: str, year: int, size_label: str):
    data = comparison.dropna(subset=["country_pct", "eu_pct"], how="all").copy()
    if data.empty:
        return None
    data["barrier"] = data["indicator_code"].map(NAMES).fillna(data["indicator_label"])
    data["sort_value"] = data[["country_pct", "eu_pct"]].max(axis=1, skipna=True)
    data = data.sort_values("sort_value", ascending=True).reset_index(drop=True)
    fig = go.Figure()
    for column, label, color, flag_column in [
        ("eu_pct", "EU27_2020", EU_COLOR, "eu_status"),
        ("country_pct", country_name, COUNTRY_COLOR, "country_status"),
    ]:
        valid = data[column].notna()
        subset = data.loc[valid]
        fig.add_trace(go.Bar(
            x=subset[column], y=subset["barrier"], orientation="h", name=label,
            marker_color=color, text=[f"{value:.1f}%" for value in subset[column]],
            textposition="outside", cliponaxis=False,
            customdata=list(zip(subset["difference_pp"], subset["indicator_code"], subset[flag_column])),
            hovertemplate=("%{y}<br>" + label + ": %{x:.2f}%"
                           "<br>Country minus EU: %{customdata[0]:+.2f} pp"
                           "<br>Indicator: %{customdata[1]}"
                           "<br>Eurostat flag: %{customdata[2]}<extra></extra>"),
        ))
    fig.update_layout(title=f"{country_name} compared with Eurostat EU27 · {year} · {size_label}",
                      barmode="group", height=500,
                      xaxis_title="Enterprises that considered AI but did not adopt it (%)",
                      yaxis_title="", legend=dict(orientation="h", y=-0.16, x=0.02))
    fig.update_xaxes(range=[0, 100], ticksuffix="%")
    return fig, data


def _display_number(value, suffix: str = "%") -> str:
    return "—" if pd.isna(value) else f"{value:.2f}{suffix}"


header("Member 4 · adoption frictions", "Adoption Barriers",
       "These are reported reasons for non-adoption among enterprises that **considered AI but did not use it**. "
       "Responses can overlap, so percentages do not sum to 100%.")
all_data = barriers(load("barrier"), size=None)
country_col, year_col, size_col = st.columns([1.45, 0.65, 1.3])
with country_col:
    member_states = all_data.loc[~all_data.country_code.eq(EU)]
    country = country_picker(member_states, key="barrier_country", default="DK",
                             label="Member State")
with year_col:
    years = sorted(all_data.year.unique())
    year = st.selectbox("Survey year", years, index=len(years) - 1, key="barrier_year")
size_labels = (all_data[["size_emp", "size_label"]].drop_duplicates()
               .set_index("size_emp")["size_label"].to_dict())
size_options = list(size_labels)
default_size_index = size_options.index("GE10") if "GE10" in size_options else 0
with size_col:
    size = st.selectbox("Main chart size", size_options, index=default_size_index,
                        format_func=lambda value: size_labels[value], key="barrier_main_size")

selected = all_data.loc[
    all_data.country_code.eq(country) & all_data.year.eq(year) & all_data.size_emp.eq(size)
].copy()
selected["barrier"] = selected.indicator_code.map(NAMES).fillna(selected.indicator_label)
ranking = selected.dropna(subset=["percentage"]).sort_values("percentage")
country_names = dict(zip(all_data.country_code, all_data.country_name))
country_name = country_names.get(country, country)
size_comparison, size_source = size_barrier_comparison(load("barrier"), country, year)

st.subheader("1 · What are the main barriers?")
if ranking.empty:
    st.info("No barrier observations are available for this selection. Try another year, country or size.")
    top = None
else:
    top = ranking.iloc[-1]
    insight(f"The leading reported barrier in **{top.country_name}** in **{year}** was "
            f"**{top.barrier.lower()} ({top.percentage:.2f}%)** among enterprises that considered AI but did not use it.")
    fig = px.bar(ranking, x="percentage", y="barrier", orientation="h",
                 title=f"Reasons for not adopting AI · {year}",
                 labels={"barrier": "Reported reason", "percentage": "Share of considered-but-nonadopting enterprises (%)"},
                 color_discrete_sequence=["#B65F3D"], text="percentage", height=410,
                 hover_data={"indicator_code": True, "indicator_label": True,
                             "denominator_definition": True, "observation_status": True,
                             "percentage": ":.2f"})
    fig.update_traces(texttemplate="%{x:.1f}%", textposition="outside", cliponaxis=False,
                      textfont=dict(size=11, color="#17324D"),
                      marker_line_color="#854126", marker_line_width=0.7)
    fig.update_xaxes(range=[0, 100])
    chart(fig, key="barrier_rank", transition_ms=0)
    st.caption("Barrier rates are conditional shares of the selected enterprise group; responses can overlap and need not sum to 100%.")

st.subheader("2 · Which enterprise sizes report different barriers?")
st.markdown(f"Small enterprises are Eurostat's **10–49** group and large enterprises are **250+**. Both series use the selected country and year, and share the same percentage scale.")
size_result = size_dumbbell(size_comparison, country_name, year)
if size_result is None:
    st.info("No non-missing small or large enterprise observations are available for this selection.")
    size_ranked = pd.DataFrame()
    size_gap_row = None
else:
    size_fig, size_ranked = size_result
    chart(size_fig, key="barrier_size_dumbbell", transition_ms=0)
    size_table = pd.DataFrame({
        "Reported barrier": size_ranked["barrier"],
        "Small (10–49, %)": size_ranked["small_pct"].map(_display_number),
        "Large (250+, %)": size_ranked["large_pct"].map(_display_number),
        "Small minus large (pp)": size_ranked["difference_pp"].map(
            lambda value: _display_number(value, " pp")
        ),
    })
    st.dataframe(
        size_table, hide_index=True, width="stretch", height=340,
    )
    complete_gaps = size_ranked.dropna(subset=["difference_pp"])
    size_gap_row = None if complete_gaps.empty else complete_gaps.iloc[0]
    if size_gap_row is not None:
        direction = "higher" if size_gap_row.difference_pp > 0 else "lower"
        insight(f"The largest absolute size difference was for **{size_gap_row.barrier.lower()}**: "
                f"small firms reported {size_gap_row.small_pct:.2f}% and large firms {size_gap_row.large_pct:.2f}% "
                f"({abs(size_gap_row.difference_pp):.2f} percentage points {direction} for small firms). "
                "This describes reported responses and does not establish why the difference exists.",
                label="Size comparison")

st.subheader("3 · How does the selected country compare with EU27?")
st.markdown("The country is compared with Eurostat's supplied **EU27_2020** aggregate for the same year, barrier and selected enterprise-size group. The EU value is not recalculated from member states.")
comparison_size = st.selectbox(
    "Enterprise size for country comparison", size_options, index=default_size_index,
    format_func=lambda value: size_labels[value], key="barrier_compare_size",
)
eu_comparison, eu_source = country_eu_barrier_comparison(
    load("barrier"), country, year, comparison_size,
)
country_result = country_eu_bars(eu_comparison, country_name, year, size_labels[comparison_size])
if country_result is None:
    st.info("No non-missing country or EU27 observations are available for this selection.")
    country_ranked = pd.DataFrame()
    country_gap_row = None
else:
    country_fig, country_ranked = country_result
    chart(country_fig, key="barrier_country_eu", transition_ms=0)
    country_table = pd.DataFrame({
        "Reported barrier": country_ranked["barrier"],
        f"{country_name} (%)": country_ranked["country_pct"].map(_display_number),
        "EU27_2020 (%)": country_ranked["eu_pct"].map(_display_number),
        "Country minus EU (pp)": country_ranked["difference_pp"].map(
            lambda value: _display_number(value, " pp")
        ),
    })
    st.dataframe(
        country_table, hide_index=True, width="stretch", height=340,
    )
    complete_gaps = country_ranked.dropna(subset=["difference_pp"])
    if country == EU:
        country_gap_row = None
        st.caption("The selected country is EU27_2020, so the comparison groups are identical; choose a Member State to see country differences.")
    else:
        country_gap_row = None if complete_gaps.empty else complete_gaps.iloc[
            complete_gaps["difference_pp"].abs().argmax()
        ]
        if country_gap_row is not None:
            direction = "above" if country_gap_row.difference_pp > 0 else "below"
            insight(f"The largest absolute difference was for **{country_gap_row.barrier.lower()}**: "
                    f"{country_name} was {country_gap_row.country_pct:.2f}% versus {country_gap_row.eu_pct:.2f}% for EU27 "
                    f"({abs(country_gap_row.difference_pp):.2f} percentage points {direction}). "
                    "This is a descriptive comparison of survey responses.", label="Country vs EU27")

st.subheader("4 · Methodology and sources")
st.markdown("**Denominator:** `PC_ENT_AI_EC` — enterprises that considered using AI but did not adopt it. This differs from `PC_ENT`, `PC_ENT_AI_TX` and `PC_ENT_IUSE`. Each barrier is a separate response, so multiple reasons can be reported and percentages do not need to total 100%. Comparisons use only matching years, overall activity (`C10-S951_X_K`) and the stated enterprise-size definition. Missing source values remain missing and are omitted from plotted marks; no 2022 values are inferred.")
st.caption("Source-vintage caveat: the supplied snapshot's EU 2025 GE10 expertise observation is 70.31%; Eurostat's December 2025 article reported 70.89%. The exact reason for this revision is not known; see Conclusion & Sources.")
st.caption("Small minus large is calculated as small percentage − large percentage. Country minus EU is country percentage − Eurostat's EU27_2020 percentage. A positive gap means the first group reported the reason more often.")

if top is not None:
    trace(top)
else:
    trace(None)
if size_gap_row is not None:
    size_trace = size_source.loc[
        size_source.indicator_code.eq(size_gap_row.indicator_code)
        & size_source.size_emp.isin(["10-49", "GE250"])
    ]
    if not size_trace.empty:
        trace(size_trace.sort_values("size_emp").iloc[0], "Source trace · size comparison")
if country_gap_row is not None:
    eu_trace = eu_source.loc[
        eu_source.indicator_code.eq(country_gap_row.indicator_code)
        & eu_source.country_code.eq(country)
    ]
    if not eu_trace.empty:
        trace(eu_trace.iloc[0], "Source trace · country comparison")

audit_selected = pd.concat([selected, size_source, eu_source], ignore_index=True)
if "source_observation_index" in audit_selected:
    audit_selected = audit_selected.drop_duplicates("source_observation_index")
status_note(audit_selected)
footer()
