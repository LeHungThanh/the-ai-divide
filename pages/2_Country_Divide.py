import streamlit as st
import plotly.express as px
from src.data import load, adoption, record, EU
from src.ui import header, insight, chart, country_picker, footer, trace, status_note

header("Member 1 · geography", "Country Divide",
       "Compare adoption across the 27 EU countries against Eurostat's EU aggregate. A country can improve over time while the distance to leading countries remains large.")
data = adoption(load("country"))
year_col, country_col = st.columns([1, 1.6])
with year_col:
    years = sorted(data.year.unique())
    year = st.selectbox("Survey year", years, index=len(years) - 1)
with country_col:
    choice = country_picker(data.loc[data.country_code.ne(EU)], key="country_trend", label="Focus country")
selected = data.loc[data.year.eq(year)]
eu = record(selected, country_code=EU)
ranked = selected.loc[selected.country_code.ne(EU)].dropna(subset=["percentage"]).sort_values("percentage")
row = record(data, country_code=choice, year=year)
if row is not None and eu is not None:
    insight(f"**{row.country_name}: {row.percentage:.2f}%** of surveyed enterprises used AI in {year}, "
            f"**{row.percentage-eu.percentage:+.2f} percentage points** from the EU benchmark ({eu.percentage:.2f}%).")
if ranked.empty:
    st.info("No observations for this year.")
else:
    fig = px.bar(ranked, x="percentage", y="country_name", orientation="h", height=710,
                 title=f"EU country adoption in {year}", color="percentage",
                 color_continuous_scale=[[0, "#A7CFCE"], [1, "#007E87"]],
                 labels={"country_name": "Country", "percentage": "Enterprises using AI (%)"},
                 text="percentage",
                 hover_data={"country_code": True, "observation_status": True, "percentage": ":.2f"})
    if eu is not None:
        fig.add_vline(x=float(eu.percentage), line_dash="dash", line_color="#B65F3D",
                      annotation_text=f"EU {eu.percentage:.2f}%", annotation_position="top")
    fig.update_layout(coloraxis_showscale=False)
    fig.update_traces(texttemplate="%{x:.1f}%", textposition="outside", cliponaxis=False,
                      textfont=dict(size=10, color="#17324D"))
    chart(fig, key="country_rank")
    st.caption("The dashed line is Eurostat's supplied EU27_2020 statistic. Rankings exclude the aggregate; flagged observations remain visible and can be inspected below.")
trend = data.loc[data.country_code.isin([choice, EU])].dropna(subset=["percentage"]).sort_values("year").copy()
trend["Series"] = trend.country_name.where(trend.country_code.ne(EU), "EU27 benchmark")
fig = px.line(trend, x="year", y="percentage", color="Series", markers=True,
              title="Selected country versus EU", labels={"year": "Survey year", "percentage": "Enterprises using AI (%)"},
              color_discrete_map={"EU27 benchmark": "#B65F3D", str(row.country_name) if row is not None else "": "#007E87"},
              hover_data={"percentage": ":.2f", "observation_status": True})
fig.update_xaxes(dtick=1)
for series in fig.data:
    benchmark = series.name == "EU27 benchmark"
    series.update(mode="lines+markers+text", line_width=3,
                  line_dash="dash" if benchmark else "solid",
                  marker_symbol="square" if benchmark else "circle", marker_size=9,
                  text=[f"{value:.1f}%" for value in series.y],
                  textposition="bottom center" if benchmark else "top center",
                  textfont=dict(size=10, color="#17324D"))
chart(fig, key="country_line")
st.caption("Survey coverage: enterprises with 10 or more persons employed in the included NACE activities.")
trace(row if row is not None else (ranked.iloc[-1] if not ranked.empty else None))
status_note(selected)
footer()
