# The AI Divide: Who Is Being Left Behind?

**Live dashboard:** [the-ai-divide-sibscn8eceqt5wl6nrpwpt.streamlit.app](https://the-ai-divide-sibscn8eceqt5wl6nrpwpt.streamlit.app/)

**Research question:** Is AI adoption becoming more inclusive across European businesses, or is a digital divide emerging?

**Audience and persona:** EU policymakers who decide where to target digital-skills, SME and AI-adoption support, and need comparable evidence about countries, enterprise sizes, industries and reported barriers.

This six-page Streamlit data narrative brings together Eurostat evidence on overall EU adoption, country differences, enterprise size, industry, and reported non-adoption barriers. The question is arguable: adoption can rise overall while country, size, and industry gaps persist, so the same descriptive data can support different assessments of inclusion.

The group workstreams are Country Divide (Mehul Joshi), Company Size (Yixin Huang), Industry Divide (Ashwinlingesh Sangeetha Ravichand), and Adoption Barriers (Le Hung Thanh). See [member contributions](docs/member_contributions.md) for assigned responsibilities and the [AI provenance matrix](docs/ai_provenance_matrix.md) for reconstructed AI-use records and project-level verification evidence.

## Run locally

From this repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

On Windows, activate with `.venv\Scripts\activate`. Then open the URL printed by Streamlit, normally `http://localhost:8501`. The four processed CSVs and their exact Eurostat JSON-stat source snapshots are included. No download is required for either the app or reproducible processing.

## Policymaker user stories and walkthroughs

1. **As an EU policymaker, I want to compare AI adoption across Member States, so that I can identify countries that may need targeted digital-capacity support.**
   - **Page:** Country Divide. Choose a survey year and a Member State. The horizontal ranking shows the 27 country observations and Eurostat's EU27 benchmark; the country trend compares that Member State with the EU across available years. The benchmark is supplied by Eurostat, not calculated as a country average.
   - **Insight:** See the country's position relative to peers and the EU and whether its adoption trend diverges. Source flags and exact observation provenance are available below the chart.
   - **Workflow check:** The page loads with 2025 selected, offers all four observed years and Member States, and renders both ranking and trend charts; missing source rows remain missing.

2. **As an EU policymaker, I want to compare AI adoption among small and large enterprises, so that I can assess whether firm size is associated with unequal access to AI.**
   - **Page:** Company Size. Select a country or the EU aggregate and a survey year. The page compares Eurostat's 10–49, 50–249 and 250+ employee classes and reports the large-minus-small gap in percentage points.
   - **Insight:** Identify the size classes with different adoption rates and inspect how that gap changes across the available survey years. Percentages are compared within the same country and year.
   - **Workflow check:** The page offers all three non-overlapping size classes, country and year filters, a comparison chart and a trend; no missing values are imputed.

3. **As an EU policymaker, I want to compare the barriers reported by businesses that considered AI but did not adopt it, so that I can target support at the obstacles they actually identify.**
   - **Page:** Adoption Barriers. Select a Member State, year and enterprise size for the ranked barriers; separate controls compare small with large firms and the selected country with Eurostat's EU27 aggregate.
   - **Insight:** Find the most frequently reported barriers and see how responses differ by firm size and from the EU benchmark. These are multiple-response questions and percentages use the `PC_ENT_AI_EC` considered-but-not-adopted denominator; they do not sum to 100%.
   - **Workflow check:** The main size defaults to `GE10`; all three comparison sections update from their filters, preserve the common denominator, and show explanatory empty states when observations are unavailable.

Each workflow was checked against the page's controls, source data selection and chart construction. Automated checks are listed in [the data validation report](docs/data_validation_report.md) and [reproducibility instructions](docs/reproducibility.md).

## Deployment

The published application is hosted on [Streamlit Community Cloud](https://the-ai-divide-sibscn8eceqt5wl6nrpwpt.streamlit.app/) with `app.py` as its entry point. It reads the four bundled processed CSV files at runtime and requires no secrets or external API calls.

## Data, methods and documentation

The application uses bundled Eurostat JSON-stat source snapshots and processed CSV files. The data covers 2021, 2023, 2024, and 2025; 2022 is unavailable. The 2025 EU expertise-barrier observation is 70.31% in the bundled June 2026 source snapshot, compared with 70.89% in a December 2025 Eurostat article; this documented source-vintage difference is not adjusted in the app.

Supporting material:

- [Data dictionary](docs/data_dictionary.md) and [source and licence notes](docs/data_sources.md)
- [Reproducibility guide](docs/reproducibility.md) and [data validation report](docs/data_validation_report.md)
- [Accessibility review](docs/accessibility_review.md) and [performance review](docs/performance_review.md)
- [AI disclosure](docs/ai_usage.md) and [AI provenance matrix](docs/ai_provenance_matrix.md)

## Reproduce and verify

```sh
python -m unittest discover -s tests -v
python -m streamlit run app.py --server.headless true
```

To verify and regenerate the processed files from the bundled source snapshots:

```sh
python scripts/prepare_data.py
python scripts/validate_data.py
python -m unittest discover -s tests -v
```

The preparation script writes the same four processed files and the reproducibility checks compare them byte-for-byte with the checked-in versions. Charts retain missing observations as missing; they are never treated as zero.
