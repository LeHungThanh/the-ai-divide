import streamlit as st
import plotly.express as px
from src.data import load, adoption, record, EU
from src.ui import header, chart, country_picker, footer, trace, status_note

header("Member 1 · geography", "Country Divide",
       "Compare adoption across the 27 EU countries against Eurostat's EU aggregate. A country can improve over time while the distance to leading countries remains large.")
data = adoption(load("country"))
year = st.select_slider("Survey year", options=sorted(data.year.unique()), value=int(data.year.max()))
selected = data.loc[data.year.eq(year)]
eu = record(selected, country_code=EU)
ranked = selected.loc[selected.country_code.ne(EU)].dropna(subset=["percentage"]).sort_values("percentage")
if ranked.empty:
    st.info("No observations for this year.")
else:
    fig = px.bar(ranked, x="percentage", y="country_name", orientation="h", height=700,
                 title=f"EU country adoption in {year}", color="percentage",
                 color_continuous_scale=[[0, "#ADCBD0"], [1, "#007F86"]],
                 labels={"country_name": "Country", "percentage": "Enterprises using AI (%)"},
                 hover_data={"country_code": True, "observation_status": True, "percentage": ":.2f"})
    if eu is not None:
        fig.add_vline(x=float(eu.percentage), line_dash="dash", line_color="#D96C49",
                      annotation_text=f"EU {eu.percentage:.2f}%", annotation_position="top")
    fig.update_layout(coloraxis_showscale=False)
    chart(fig, key="country_rank")
    st.caption("The dashed line is Eurostat's supplied EU27_2020 statistic. Rankings exclude the aggregate; flagged observations remain visible and can be inspected below.")
choice = country_picker(data.loc[data.country_code.ne(EU)], key="country_trend")
trend = data.loc[data.country_code.isin([choice, EU])].dropna(subset=["percentage"]).sort_values("year")
fig = px.line(trend, x="year", y="percentage", color="country_name", markers=True,
              title="Selected country versus EU", labels={"year": "Survey year", "percentage": "Enterprises using AI (%)"},
              color_discrete_map={EU: "#D96C49"}, hover_data={"percentage": ":.2f", "observation_status": True})
fig.update_xaxes(dtick=1)
chart(fig, key="country_line")
row = record(data, country_code=choice, year=year)
if row is not None and eu is not None:
    st.markdown(f"In **{year}**, **{row.country_name}** was **{row.percentage-eu.percentage:+.2f} percentage points** from the EU benchmark. "
                "The survey covers enterprises with 10 or more persons employed in the included NACE activities.")
trace(row if row is not None else (ranked.iloc[-1] if not ranked.empty else None))
status_note(selected)
footer()
