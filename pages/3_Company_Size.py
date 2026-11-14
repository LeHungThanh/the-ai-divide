import pandas as pd
import plotly.express as px
import streamlit as st
from src.data import load, adoption, record, EU, SIZES
from src.ui import header, insight, chart, country_picker, footer, trace, status_note

header("Member 2 · enterprise scale", "Company Size",
       "Small, medium and large businesses face different capacity constraints. Compare their adoption rates within the same country and year; subtracting rates gives a percentage-point gap.")
all_data = adoption(load("size"), size=None)
country_col, year_col = st.columns([1.6, 1])
with country_col:
    country = country_picker(all_data, key="size_country", default=EU)
with year_col:
    years = sorted(all_data.year.unique())
    year = st.selectbox("Survey year", years, index=len(years) - 1)
data = all_data.loc[all_data.country_code.eq(country) & all_data.size_emp.isin(SIZES)]
selected = data.loc[data.year.eq(year)].copy()
selected["Size"] = selected.size_emp.map(SIZES)
selected["Size"] = pd.Categorical(selected["Size"], categories=list(SIZES.values()), ordered=True)
small = record(selected, size_emp="10-49")
large = record(selected, size_emp="GE250")
metric_col, finding_col = st.columns([1, 2])
with metric_col:
    st.metric("Large–small adoption gap", f"{large.percentage-small.percentage:.2f} pp" if small is not None and large is not None else "Unavailable")
with finding_col:
    if small is not None and large is not None:
        insight(f"In **{small.country_name}** in **{year}**, large firms reached **{large.percentage:.2f}%** "
                f"while small firms reached **{small.percentage:.2f}%**. The gap is **{large.percentage-small.percentage:.2f} percentage points**.")
    else:
        st.info("A size gap is unavailable for this selection because one or both rates are missing.")
fig = px.bar(selected.dropna(subset=["percentage"]), x="Size", y="percentage", color="Size",
             title=f"AI adoption by enterprise size · {year}",
             color_discrete_map={"Small (10–49)": "#659B9D", "Medium (50–249)": "#007E87", "Large (250+)": "#17324D"},
             labels={"percentage": "Enterprises using AI (%)"},
             text="percentage",
             hover_data={"size_label": True, "observation_status": True, "percentage": ":.2f"})
fig.update_traces(texttemplate="%{y:.1f}%", textposition="outside", cliponaxis=False,
                  textfont=dict(size=12, color="#17324D"))
fig.update_yaxes(range=[0, max(65, selected.percentage.max(skipna=True) + 8)])
chart(fig, key="size_bar")
st.caption("These three official size classes do not overlap. Other source size codes, including GE10 and 10–249, would overlap this comparison and are excluded.")
trend = data.dropna(subset=["percentage"]).copy()
trend["Size"] = trend.size_emp.map(SIZES)
fig = px.line(trend, x="year", y="percentage", color="Size", markers=True,
              title="Size-class trend", labels={"year": "Survey year", "percentage": "Enterprises using AI (%)"},
              color_discrete_map={"Small (10–49)": "#659B9D", "Medium (50–249)": "#007E87", "Large (250+)": "#17324D"},
              hover_data={"percentage": ":.2f", "observation_status": True})
fig.update_xaxes(dtick=1)
for series in fig.data:
    is_large = series.name == "Large (250+)"
    is_small = series.name == "Small (10–49)"
    series.update(mode="lines+markers+text", line_width=3,
                  line_dash="dash" if is_small else "dot" if is_large else "solid",
                  marker_symbol="diamond" if is_small else "square" if is_large else "circle",
                  marker_size=8, text=[f"{value:.1f}%" for value in series.y],
                  textposition="bottom center" if is_small else "top center",
                  textfont=dict(size=10, color="#17324D"))
chart(fig, key="size_trend")
st.caption("A positive gap means adoption is more concentrated among larger firms; inspect the trend before drawing a conclusion about convergence.")
available_trace = selected.dropna(subset=["percentage"])
trace(large if large is not None else small if small is not None else
      (available_trace.iloc[0] if not available_trace.empty else None))
status_note(data)
footer()
