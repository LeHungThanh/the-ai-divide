import plotly.express as px
import streamlit as st
from src.data import load, barriers, record, EU
from src.ui import header, chart, country_picker, footer, trace, status_note

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
country = country_picker(all_data, key="barrier_country", default=EU)
year = st.select_slider("Survey year", options=sorted(all_data.year.unique()), value=int(all_data.year.max()))
size_labels = (all_data[["size_emp", "size_label"]].drop_duplicates()
               .set_index("size_emp")["size_label"].to_dict())
size = st.selectbox("Enterprise size", list(size_labels), format_func=lambda x: size_labels[x])
selected = all_data.loc[all_data.country_code.eq(country) & all_data.year.eq(year) & all_data.size_emp.eq(size)].copy()
selected["barrier"] = selected.indicator_code.map(NAMES).fillna(selected.indicator_label)
ranking = selected.dropna(subset=["percentage"]).sort_values("percentage")
if ranking.empty:
    st.info("No barrier observations are available for this selection. Try another year, country or size.")
    trace(None)
else:
    fig = px.bar(ranking, x="percentage", y="barrier", orientation="h",
                 title=f"Reasons for not adopting AI · {year}",
                 labels={"barrier": "Reported reason", "percentage": "Share of considered-but-nonadopting enterprises (%)"},
                 color_discrete_sequence=["#D96C49"],
                 hover_data={"indicator_code": True, "indicator_label": True,
                             "denominator_definition": True, "observation_status": True, "percentage": ":.2f"})
    chart(fig, key="barrier_rank")
    top = ranking.iloc[-1]
    st.markdown(f"The most frequently reported reason in **{top.country_name}** in **{year}** is **{top.barrier.lower()}** "
                f"(**{top.percentage:.2f}%** of the specified group). This is a conditional share, not a share of all enterprises.")
    trace(top)
st.info("Denominator: Eurostat unit PC_ENT_AI_EC. For these barrier indicators, it refers to enterprises that had considered AI use but did not adopt it. "
        "The dashboard does not mix this with PC_ENT, PC_ENT_AI_TX or PC_ENT_IUSE.")
st.caption("The current EU 2025 expertise observation is 70.31%; Eurostat's December 2025 article reported 70.89%. The ZIP reflects a later API snapshot. This difference is documented in Sources.")
status_note(selected)
footer()
