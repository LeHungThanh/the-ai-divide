import pandas as pd
import plotly.express as px
import streamlit as st
from src.data import load, adoption, comparison_sectors, record, EU
from src.ui import header, insight, chart, country_picker, footer, trace, status_note

header("Member 3 · economic activity", "Industry Divide",
       "AI uptake varies by economic activity. The comparison uses distinct NACE sections plus the covered repair group S951, so broader aggregates and their components are not counted together.")
all_data = comparison_sectors(adoption(load("industry"), sector=None))
country_col, year_col = st.columns([1.6, 1])
with country_col:
    country = country_picker(all_data, key="industry_country", default=EU)
with year_col:
    years = sorted(all_data.year.unique())
    year = st.selectbox("Ranking year", years, index=len(years) - 1)
place = all_data.loc[all_data.country_code.eq(country)].copy()
mapping = (place[["nace_r2", "industry_label"]].drop_duplicates()
           .set_index("nace_r2")["industry_label"].to_dict())
codes = sorted(mapping)
if "industry_sectors" not in st.session_state:
    st.session_state.industry_sectors = codes
with st.expander("Filter sectors", expanded=False):
    controls = st.columns(2)
    if controls[0].button("Select all", key="industry_select_all", use_container_width=True):
        st.session_state.industry_sectors = codes
        st.rerun()
    if controls[1].button("Clear all", key="industry_clear_all", use_container_width=True):
        st.session_state.industry_sectors = []
        st.rerun()
    selected_codes = st.multiselect("Sectors", codes, key="industry_sectors",
                                    format_func=lambda x: f"{x} — {mapping[x]}")
st.caption(f"Showing {len(selected_codes)} of {len(codes)} nonoverlapping activity groups · change the selection in Filter sectors.")
place = place.loc[place.nace_r2.isin(selected_codes)]
ranking = place.loc[place.year.eq(year)].dropna(subset=["percentage"]).sort_values("percentage")
if not ranking.empty:
    top = ranking.iloc[-1]
    insight(f"**{top.nace_r2} — {top.industry_label}** recorded the highest adoption among selected sectors "
            f"in **{top.country_name}** in **{year}: {top.percentage:.2f}%**. "
            "These percentages describe separate enterprise populations and cannot be summed.")
matrix = place.pivot(index="nace_r2", columns="year", values="percentage").reindex(index=selected_codes)
if matrix.empty:
    st.info("Select at least one sector to display the heatmap.")
else:
    matrix.columns = matrix.columns.astype(str)
    fig = px.imshow(matrix, aspect="auto",
                    color_continuous_scale=[[0, "#EEF6F5"], [0.5, "#C3DFDF"], [1, "#82B5BB"]],
                    text_auto=".1f",
                    labels={"x": "Survey year", "y": "NACE sector", "color": "Adoption (%)"},
                    title="Industry adoption by year · missing cells remain blank")
    fig.update_traces(hovertemplate="Sector %{y}<br>Year %{x}<br>Adoption %{z:.2f}%<extra></extra>")
    chart(fig, key="industry_heatmap")
if not ranking.empty:
    fig = px.bar(ranking, x="percentage", y="nace_r2", orientation="h",
                 title=f"Sector ranking · {year}", labels={"nace_r2": "NACE sector", "percentage": "Enterprises using AI (%)"},
                 color_discrete_sequence=["#007E87"], text="percentage",
                 hover_data={"industry_label": True, "observation_status": True, "percentage": ":.2f"})
    fig.update_traces(texttemplate="%{x:.1f}%", textposition="outside", cliponaxis=False,
                      textfont=dict(size=11, color="#17324D"))
    chart(fig, key="industry_rank")
    trace(top)
else:
    trace(None)
status_note(place)
footer()
