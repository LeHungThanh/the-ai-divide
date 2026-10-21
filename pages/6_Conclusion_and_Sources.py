import streamlit as st
from src.data import load, adoption, barriers, record, EU
from src.ui import header, footer

header("Synthesis · evidence and caveats", "Conclusion & Sources",
       "The evidence points to growing AI use alongside persistent divides. Interpret changes as descriptive survey results, not as proof that any policy or barrier caused adoption.")
country = adoption(load("country"))
size = adoption(load("size"), size=None)
barrier = barriers(load("barrier"))
years = sorted(country.year.unique())
first, latest = years[0], years[-1]
eu_first = record(country, country_code=EU, year=first)
eu_latest = record(country, country_code=EU, year=latest)
small = record(size, country_code=EU, year=latest, size_emp="10-49")
large = record(size, country_code=EU, year=latest, size_emp="GE250")
expertise = record(barrier, country_code=EU, year=latest, size_emp="GE10", indicator_code="E_AI_BLE")
st.markdown(f"**Adoption rose:** Eurostat's EU aggregate moved from **{eu_first.percentage:.2f}% in {first}** to **{eu_latest.percentage:.2f}% in {latest}**. "
            "The country ranking shows that uptake remains uneven across member states.")
st.markdown(f"**Size still matters:** the EU large–small gap in {latest} was **{large.percentage-small.percentage:.2f} percentage points** "
            f"({large.percentage:.2f}% versus {small.percentage:.2f}%). The industry page identifies further variation across nonoverlapping sectors.")
st.markdown(f"**Capacity is a reported obstacle:** **{expertise.percentage:.2f}%** of EU enterprises in the relevant conditional barrier population "
            f"reported lack of expertise in {latest}. Multiple barrier responses are allowed.")
st.subheader("Limits that matter for policy")
st.markdown("Survey years are **2021, 2023, 2024 and 2025**; 2022 is absent. Standard adoption rates cover enterprises with at least 10 persons employed in selected activities. "
            "The source includes quality flags and missing observations; charts omit missing values without replacing them. Industry categories overlap unless the comparison selection is used. "
            "The 2025 questionnaire added AI generation of pictures, video and sound/audio, so year-to-year changes partly reflect an expanded technology definition.")
st.warning("The ZIP has processed CSVs and source-observation identifiers, but no original Eurostat JSON-stat files. "
           "The 2025 EU expertise barrier is 70.31% in the processed snapshot versus 70.89% in the December 2025 publication; the exact revision reason is unconfirmed.")
st.subheader("Official sources")
st.markdown("- [Eurostat: AI by enterprise size (isoc_eb_ai)](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table?lang=en)\n"
            "- [Eurostat: AI by NACE activity (isoc_eb_ain2)](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ain2/default/table?lang=en)\n"
            "- [Eurostat Statistics Explained: use of AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)\n"
            "- [Eurostat Statistics API guide](https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-getting-started/api)\n"
            "- [Eurostat 2025 news and definition note](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2)")
st.caption("Methods and member contributions are documented in docs/. AI assistance is disclosed in docs/ai_usage.md.")
footer()
