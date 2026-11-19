# Assignment 3 Part 2 — 30-check audit

Rubric source: the assignment brief supplied in the project conversation (Part 2, 30 binary checks). Reviewed against `codex/part2-requirements` and the published `origin/main` on 19 November 2026. PASS means evidence exists in the published project; UNVERIFIED means an external performance threshold or genuine teammate evidence is still required. No criterion is inferred from a documentation claim alone when a test or app check was available.

| # | Status | Evidence and assessment | Remaining action |
|---:|---|---|---|
| 1 | PASS | `README.md` states the research question as one sentence. | — |
| 2 | PASS | `app.py` and `pages/1_Overview.py` show the question on the opening screen; locally rendered with AppTest and in the public app. | — |
| 3 | PASS | README explains why evidence can show rising adoption alongside persistent divides, allowing different evidence-based conclusions. | — |
| 4 | PASS | README names EU policymakers and the targeting decision the dashboard serves. | — |
| 5 | PASS | README contains three stories in the requested “As a …, I want …, so that …” form. | — |
| 6 | PASS | README maps each story to a page, filters and insight. `tests/test_page_smoke.py` and local browser checks exercised country/year, firm-size/country, barriers/year and industry empty-state workflows. | — |
| 7 | PASS | Four CSVs trace cells to bundled raw JSON-stat data with keys, status, hash and observation index; `scripts/validate_data.py` checks each row against the cubes. | — |
| 8 | PASS | Conclusion page states the evidence-based answer: adoption rose while enterprise and sector divides persist. | — |
| 9 | PASS | Conclusion and methods pages state limits on causality, scope, comparability, missing data and overlapping industry groups. | — |
| 10 | PASS | Pages label rates, percentage-point gaps, denominators, country/EU baselines and available survey years. | — |
| 11 | PASS | Claims are descriptive and explicitly avoid causal interpretation; barrier claims are limited to the reported population. | — |
| 12 | PASS | Each Plotly chart has a title; explanatory captions and labels are visible in page code and screenshots. | — |
| 13 | PASS | App has more than four charts across its six pages; all six pages render in `PageSmokeTests`. | — |
| 14 | PASS | Visual families include ranked bars, time-series lines, a heatmap, and paired barrier comparisons. | — |
| 15 | PASS | Chart forms align with ranking, trend, sector-by-year and group-comparison questions; see page implementations and screenshots under `review/animations/`. | — |
| 16 | PASS | Axes state survey year and percentage units; series legends identify country/size. Direct labels and page explanations retain group definitions. | — |
| 17 | PASS | Direct data labels appear on charts and heatmap tiles; tabular comparison values are also shown. Screenshots are 1366×768. | — |
| 18 | PASS | Protanopia/deuteranopia previews were generated for all six pages using the documented Machado model and visually inspected. Values, positions, category names and line patterns preserve meaning. Evidence: `docs/accessibility_review.md` and `review/accessibility/`. | — |
| 19 | UNVERIFIED | Local fresh-process startup was 1.154 s and warm `/` response 0.005 s. Public Cloud was confirmed asleep; after requesting wake it was still waking at 10 s and rendered by the next 15 s check. This was manually sampled, not a controlled exact timing. See `docs/performance_review.md`. | Needs a controlled public cold-start timing. Do not claim under five seconds from local timing. |
| 20 | PASS | Overview opens with Eurostat's EU27 adoption rate, its latest change and the large/small gap—values supported by processed data and raw trace. | — |
| 21 | PASS | Real local browser interaction changed the country-year finding in 638 ms and company-size KPI in 557 ms; AppTest also exercised year/country and barrier filters. See `docs/performance_review.md`. | — |
| 22 | PASS | Clearing all industry sectors displays “Select at least one sector to display the heatmap” without an exception; tested in AppTest and the browser. | — |
| 23 | PASS | Six committed 1366×768 visual-audit screenshots show vertical scrolling and no horizontal overflow. A live narrower 831 px browser viewport also reported document width equal to viewport width. | — |
| 24 | PASS | Every page footer displays the Eurostat source, dataset update date (15 June 2026) and source-file retrieval date (21 October 2026); all six pages are checked in AppTest. | — |
| 25 | PASS | `data/raw/` holds both raw source cubes and the manifest; `data/processed/` holds the four app CSVs. `processed.zip` is excluded as a duplicate. | — |
| 26 | PASS | `docs/data_dictionary.md` covers purpose, source/API URL, reuse evidence, fields/units, key, geography/time, latest 2025 examples and transformations for every output. | — |
| 27 | PASS | Published commit `7c9ea53e9a0e1bec41b90cc293dfeeddc19850f5` is the fast-forwarded `origin/main`; the remote tree contains the required app, six pages, source files, documentation and four processed CSVs. The existing public Streamlit app rendered the updated overview and its six-page navigation after waking. | Submit the exact published commit hash. |
| 28 | UNVERIFIED | `docs/ai_provenance_matrix.md` has a pending row for each member; no member-specific tools, prompts, uses or checks were invented. | Each of four members must supply and confirm their actual provenance and a falsifiable verification check. |
| 29 | PASS | `docs/ai_usage.md` contains the project Data and AI disclosure statement and links the pending team matrix. | — |
| 30 | PASS | Bundled source cubes regenerate all four CSVs with the exact existing SHA-256 values; `scripts/prepare_data.py`, `scripts/validate_data.py` and `tests/test_reproducibility.py` verify the pipeline. | — |

## Result

**28 PASS · 0 FAIL · 2 UNVERIFIED.** Remaining tasks are to establish the public cold-start threshold with a controlled timing and obtain genuine AI-use records from all four members. The published barrier default remains `GE10`; all processed CSV hashes are unchanged. The provenance matrix remains a pending template and does not fabricate member records.
