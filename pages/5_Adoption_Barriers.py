import plotly.express as px
import streamlit as st
from src.data import load, barriers, record, EU
from src.ui import header, insight, chart, country_picker, footer, trace, status_note

NAMES = {
    "E_AI_BLE": "Lack of expertise", "E_AI_BLEG": "Legal uncertainty",
    "E_AI_BCDP": "Data protection / privacy", "E_AI_BCST": "Cost",
    "E_AI_BINC": "System incompatibility", "E_AI_BDDT": "Data availability / quality",
    "E_AI_BEC": "Ethical concerns", "E_AI_BNU": "Not useful for enterprise",
}
header("Member 4 · adoption frictions", "Adoption Barriers",
       "These are reported reasons for non-adoption among enterprises that **considered AI but did not use it**. "
       "Responses can overlap, so percentages do not sum to 100%.")
all_data = barriers(load("barrier"), size=None)
country_col, year_col, size_col = st.columns([1.45, 0.65, 1.3])
with country_col:
    country = country_picker(all_data, key="barrier_country", default=EU)
with year_col:
    years = sorted(all_data.year.unique())
    year = st.selectbox("Survey year", years, index=len(years) - 1)
size_labels = (all_data[["size_emp", "size_label"]].drop_duplicates()
               .set_index("size_emp")["size_label"].to_dict())
size_options = list(size_labels)
default_size_index = size_options.index("GE10") if "GE10" in size_options else 0
with size_col:
    size = st.selectbox("Enterprise size", size_options, index=default_size_index,
                        format_func=lambda x: size_labels[x])
selected = all_data.loc[all_data.country_code.eq(country) & all_data.year.eq(year) & all_data.size_emp.eq(size)].copy()
selected["barrier"] = selected.indicator_code.map(NAMES).fillna(selected.indicator_label)
ranking = selected.dropna(subset=["percentage"]).sort_values("percentage")
if ranking.empty:
    st.info("No barrier observations are available for this selection. Try another year, country or size.")
    trace(None)
else:
    top = ranking.iloc[-1]
    insight(f"The leading reported barrier in **{top.country_name}** in **{year}** was "
            f"**{top.barrier.lower()} ({top.percentage:.2f}%)** among enterprises that considered AI but did not use it.")
    fig = px.bar(ranking, x="percentage", y="barrier", orientation="h",
                 title=f"Reasons for not adopting AI · {year}",
                 labels={"barrier": "Reported reason", "percentage": "Share of considered-but-nonadopting enterprises (%)"},
                 color_discrete_sequence=["#B65F3D"], text="percentage", height=410,
                 hover_data={"indicator_code": True, "indicator_label": True,
                             "denominator_definition": True, "observation_status": True, "percentage": ":.2f"})
    fig.update_traces(texttemplate="%{x:.1f}%", textposition="outside", cliponaxis=False,
                      textfont=dict(size=11, color="#17324D"))
    fig.update_xaxes(range=[0, 100])
    chart(fig, key="barrier_rank")
    st.caption("Barrier rates are conditional shares of the selected enterprise group; responses can overlap and need not sum to 100%.")
    trace(top)
st.info("Denominator: Eurostat unit PC_ENT_AI_EC. For these barrier indicators, it refers to enterprises that had considered AI use but did not adopt it. "
        "The dashboard does not mix this with PC_ENT, PC_ENT_AI_TX or PC_ENT_IUSE.")
st.caption("For the EU's 2025 GE10 (10+ employees) group, the processed expertise observation is 70.31%; Eurostat's December 2025 article reported 70.89%. The ZIP reflects a later API snapshot. This difference is documented in Sources.")
status_note(selected)
footer()
