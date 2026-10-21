import pandas as pd
import plotly.express as px
import streamlit as st
from src.data import load, adoption, comparison_sectors, record, EU
from src.ui import header, chart, country_picker, footer, trace, status_note

header("Member 3 · economic activity", "Industry Divide",
       "AI uptake varies by economic activity. The comparison uses distinct NACE sections plus the covered repair group S951, so broader aggregates and their components are not counted together.")
all_data = comparison_sectors(adoption(load("industry"), sector=None))
country = country_picker(all_data, key="industry_country", default=EU)
year = st.select_slider("Ranking year", options=sorted(all_data.year.unique()), value=int(all_data.year.max()))
place = all_data.loc[all_data.country_code.eq(country)].copy()
mapping = (place[["nace_r2", "industry_label"]].drop_duplicates()
           .set_index("nace_r2")["industry_label"].to_dict())
codes = sorted(mapping)
selected_codes = st.multiselect("Sectors", codes, default=codes,
                                format_func=lambda x: f"{x} — {mapping[x]}")
place = place.loc[place.nace_r2.isin(selected_codes)]
matrix = place.pivot(index="nace_r2", columns="year", values="percentage").reindex(index=selected_codes)
if matrix.empty:
    st.info("Select at least one sector to display the heatmap.")
else:
    fig = px.imshow(matrix, aspect="auto", color_continuous_scale="Teal", text_auto=".1f",
                    labels={"x": "Survey year", "y": "NACE sector", "color": "Adoption (%)"},
                    title="Industry adoption by year · missing cells remain blank")
    fig.update_traces(hovertemplate="Sector %{y}<br>Year %{x}<br>Adoption %{z:.2f}%<extra></extra>")
    chart(fig, key="industry_heatmap")
ranking = place.loc[place.year.eq(year)].dropna(subset=["percentage"]).sort_values("percentage")
if not ranking.empty:
    fig = px.bar(ranking, x="percentage", y="nace_r2", orientation="h",
                 title=f"Sector ranking · {year}", labels={"nace_r2": "NACE sector", "percentage": "Enterprises using AI (%)"},
                 color_discrete_sequence=["#007F86"],
                 hover_data={"industry_label": True, "observation_status": True, "percentage": ":.2f"})
    chart(fig, key="industry_rank")
    top = ranking.iloc[-1]
    st.markdown(f"In **{top.country_name}** in **{year}**, the highest available selected sector was **{top.nace_r2} — {top.industry_label}** "
                f"at **{top.percentage:.2f}%**. Sector percentages describe different enterprise populations and cannot be summed into an overall rate.")
    trace(top)
else:
    trace(None)
status_note(place)
footer()
