import streamlit as st
from src.data import load, adoption, barriers, record, EU
from src.ui import header, insight, footer

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
insight("Adoption rose across the EU, yet enterprise size and sector differences remain substantial. "
        "The survey describes these divides; it cannot establish what caused them.", label="Policy reading")
st.subheader("Three signals from the evidence")
adoption_col, gap_col, barrier_col = st.columns(3)
with adoption_col:
    st.metric(f"EU adoption · {latest}", f"{eu_latest.percentage:.2f}%",
              f"{eu_latest.percentage-eu_first.percentage:+.2f} pp since {first}")
    st.caption("Eurostat's supplied EU27 aggregate; national uptake remains uneven.")
with gap_col:
    st.metric("Large–small gap", f"{large.percentage-small.percentage:.2f} pp")
    st.caption(f"{large.percentage:.2f}% of large firms versus {small.percentage:.2f}% of small firms in {latest}.")
with barrier_col:
    st.metric("Lack of expertise", f"{expertise.percentage:.2f}%")
    st.caption("Among enterprises that considered AI but did not adopt it; responses may overlap.")
with st.container(border=True):
    st.subheader("Limits that matter for policy")
    st.markdown("Survey years are **2021, 2023, 2024 and 2025**; 2022 is absent. Standard adoption rates cover enterprises with at least 10 persons employed in selected activities. "
                "The source includes quality flags and missing observations; charts omit missing values without replacing them. Industry categories overlap unless the comparison selection is used. "
                "The 2025 questionnaire added AI generation of pictures, video and sound/audio, so year-to-year changes partly reflect an expanded technology definition.")
st.warning("The ZIP has processed CSVs and source-observation identifiers, but no original Eurostat JSON-stat files. "
           "The 2025 EU expertise barrier is 70.31% in the processed snapshot versus 70.89% in the December 2025 publication; the exact revision reason is unconfirmed.")
st.subheader("Official sources")
sources_left, sources_right = st.columns(2)
with sources_left:
    st.markdown("- [Eurostat: AI by enterprise size (isoc_eb_ai)](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table?lang=en)\n"
                "- [Eurostat: AI by NACE activity (isoc_eb_ain2)](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ain2/default/table?lang=en)\n"
                "- [Eurostat Statistics Explained: use of AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)")
with sources_right:
    st.markdown("- [Eurostat Statistics API guide](https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-getting-started/api)\n"
                "- [Eurostat 2025 news and definition note](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2)")
st.caption("Methods and member contributions are documented in docs/. AI assistance is disclosed in docs/ai_usage.md.")
footer()
