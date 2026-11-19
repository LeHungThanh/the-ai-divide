# Assignment 3 Part 2 — Team AI Provenance

## Project use of Codex

The project used OpenAI Codex to assist with Streamlit development, chart design, data preparation, documentation and automated tests. The model version was not recorded. The entries below describe the assigned work, the resulting features and how to check them. A specific Codex request is documented for Adoption Barriers. Individual AI sessions and manual checks are otherwise undocumented.

The project record reports 15 passing tests on 19 November 2026. Regenerating the processed CSVs reproduced their committed SHA-256 hashes. Source validation passed with a documented warning about the Eurostat publication vintage. [Data validation script](../scripts/validate_data.py)

## Mehul Joshi — Country Divide

**Scope.** Rank EU Member States by AI adoption for the selected survey year and compare the selected country’s trend with Eurostat’s official EU27 series.

**Outcome.** A horizontal Plotly bar chart ranks countries and uses the supplied `EU27_2020` observation as a reference line. A second chart plots the focus country and EU27 over time. The charts omit unavailable rates and show percentages for available observations. [Page](../pages/2_Country_Divide.py) · [CSV](../data/processed/01_country_adoption.csv)

**Verification.** Project smoke tests exercise the year and country selectors. To check the chart against the source, match a plotted rate to the CSV by country and year, then match the reference line to the EU27 observation for that year. [Smoke tests](../tests/test_page_smoke.py)

## Yixin Huang — Company Size

**Scope.** Compare AI adoption by country and survey year across the 10–49, 50–249 and 250+ employee categories. Calculate the large-minus-small gap in percentage points.

**Outcome.** The page shows rates for the three disjoint size classes, a gap metric for the selected year and historical adoption rates for each class. The gap metric displays “Unavailable” when either source rate is missing. [Page](../pages/3_Company_Size.py) · [CSV](../data/processed/02_company_size.csv)

**Verification.** Project smoke tests check that changing the country updates the gap. To check the calculation, subtract the 10–49 rate from the 250+ rate for the same country and year, then compare the value and sign with the dashboard. [Smoke tests](../tests/test_page_smoke.py)

## Ashwinlingesh Sangeetha Ravichand — Industry Divide

**Scope.** Compare AI adoption by NACE sector and year, with country and sector controls and a ranking for the selected year.

**Outcome.** The page combines a heatmap of sectors by year with a ranked comparison. It uses distinct sectors, leaves missing heatmap cells blank and displays a message when all sectors are deselected. [Page](../pages/4_Industry_Divide.py) · [CSV](../data/processed/03_industry_adoption.csv)

**Verification.** The project smoke test checks the empty selection message. To check chart values, match a heatmap cell and a ranking bar to the CSV using country, sector and year. [Smoke tests](../tests/test_page_smoke.py)

## Le Hung Thanh — Adoption Barriers

**Scope and documented Codex request.** Allow `barriers(size=None)` to retain all size classes for comparisons. Keep `GE10` as the main ranking default and preserve `PC_ENT_AI_EC`, which uses enterprises that considered AI but did not adopt it as the denominator. Preserve the filters and add regression coverage.

**Outcome.** The page ranks reported barriers and compares the 10–49 and 250+ employee groups. It also compares a selected country with the supplied EU27 aggregate. It reports source rates and differences in percentage points and preserves missing values and source flags. [Page](../pages/5_Adoption_Barriers.py) · [Comparison logic](../src/barrier_comparisons.py) · [CSV](../data/processed/04_ai_adoption_barriers.csv)

**Verification.** Project tests cover the default size, denominator, size selection, comparison gaps and source flags. To spot-check a gap against the CSV, match the observations by barrier, year and denominator, then subtract the source rates in the order shown. For a country-to-EU27 comparison, also match the enterprise size. [Smoke tests](../tests/test_page_smoke.py) · [Data tests](../tests/test_data.py) · [Comparison tests](../tests/test_barrier_comparisons.py)

## Criterion 28

Individual AI use records and personal verification details remain open. The linked tests document checks of the shared application.
