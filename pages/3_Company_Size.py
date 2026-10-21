import pandas as pd
import plotly.express as px
import streamlit as st
from src.data import load, adoption, record, EU, SIZES
from src.ui import header, chart, country_picker, footer, trace, status_note

header("Member 2 · enterprise scale", "Company Size",
       "Small, medium and large businesses face different capacity constraints. Compare their adoption rates within the same country and year; subtracting rates gives a percentage-point gap.")
all_data = adoption(load("size"), size=None)
country = country_picker(all_data, key="size_country", default=EU)
year = st.select_slider("Survey year", options=sorted(all_data.year.unique()), value=int(all_data.year.max()))
data = all_data.loc[all_data.country_code.eq(country) & all_data.size_emp.isin(SIZES)]
selected = data.loc[data.year.eq(year)].copy()
selected["Size"] = selected.size_emp.map(SIZES)
selected["Size"] = pd.Categorical(selected["Size"], categories=list(SIZES.values()), ordered=True)
fig = px.bar(selected.dropna(subset=["percentage"]), x="Size", y="percentage", color="Size",
             title=f"AI adoption by enterprise size · {year}",
             color_discrete_sequence=["#76B5B4", "#007F86", "#17324D"],
             labels={"percentage": "Enterprises using AI (%)"},
             hover_data={"size_label": True, "observation_status": True, "percentage": ":.2f"})
chart(fig, key="size_bar")
small = record(selected, size_emp="10-49")
large = record(selected, size_emp="GE250")
st.metric("Large–small adoption gap", f"{large.percentage-small.percentage:.2f} pp" if small is not None and large is not None else "Unavailable")
st.caption("These three official size classes do not overlap. Other source size codes, including GE10 and 10–249, would overlap this comparison and are excluded.")
trend = data.dropna(subset=["percentage"]).copy()
trend["Size"] = trend.size_emp.map(SIZES)
fig = px.line(trend, x="year", y="percentage", color="Size", markers=True,
              title="Size-class trend", labels={"year": "Survey year", "percentage": "Enterprises using AI (%)"},
              color_discrete_map={"Small (10–49)": "#76B5B4", "Medium (50–249)": "#007F86", "Large (250+)": "#17324D"},
              hover_data={"percentage": ":.2f", "observation_status": True})
fig.update_xaxes(dtick=1)
chart(fig, key="size_trend")
if small is not None and large is not None:
    st.markdown(f"For **{small.country_name}** in **{year}**, large enterprises led small enterprises by **{large.percentage-small.percentage:.2f} pp**. "
                "A positive gap means adoption is more concentrated among larger firms; inspect the trend before drawing a conclusion about convergence.")
available_trace = selected.dropna(subset=["percentage"])
trace(large if large is not None else small if small is not None else
      (available_trace.iloc[0] if not available_trace.empty else None))
status_note(data)
footer()
