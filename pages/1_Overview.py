import streamlit as st
import plotly.express as px
from src.data import load, adoption, record, EU
from src.ui import header, chart, footer, status_note

header("Policy brief · EU27", "The AI Divide: Who Is Being Left Behind?",
       "**Research question:** Is AI adoption becoming more inclusive across European businesses, or is a digital divide emerging? "
       "This dashboard compares countries, enterprise sizes, economic activities and reported barriers using official Eurostat survey data.")
country = adoption(load("country"))
size = adoption(load("size"), size=None)
available = sorted(country.year.unique())
latest = max(available)
previous = max(y for y in available if y < latest)
eu_now = record(country, country_code=EU, year=latest)
eu_before = record(country, country_code=EU, year=previous)
large = record(size, country_code=EU, year=latest, size_emp="GE250")
small = record(size, country_code=EU, year=latest, size_emp="10-49")
a, b, c = st.columns(3)
a.metric(f"EU enterprises using AI · {latest}", f"{eu_now.percentage:.2f}%" if eu_now is not None else "Unavailable",
         f"{eu_now.percentage-eu_before.percentage:+.2f} pp since {previous}" if eu_now is not None and eu_before is not None else None)
b.metric("Large enterprises", f"{large.percentage:.2f}%" if large is not None else "Unavailable")
c.metric("Large–small gap", f"{large.percentage-small.percentage:.2f} pp" if large is not None and small is not None else "Unavailable")
st.caption("EU values are Eurostat's EU27_2020 aggregate. ‘pp’ means percentage points; rates are for enterprises with at least 10 persons employed.")
trend = country.loc[country.country_code.eq(EU)].dropna(subset=["percentage"]).sort_values("year")
fig = px.line(trend, x="year", y="percentage", markers=True, title="EU adoption across available survey years",
              labels={"year": "Survey year", "percentage": "Enterprises using AI (%)"},
              hover_data={"percentage": ":.2f", "year": True})
fig.update_traces(line_color="#007F86", line_width=3, marker_size=9)
fig.update_xaxes(dtick=1)
chart(fig, key="overview_trend")
st.markdown("**Read the evidence in sequence:** Country Divide shows where uptake differs; Company Size tests whether scale matters; "
            "Industry Divide compares nonoverlapping activities; Adoption Barriers shows reasons among firms that considered AI but did not use it. "
            "Available survey years are 2021, 2023, 2024 and 2025.")
status_note(country.loc[country.country_code.eq(EU)])
footer()
