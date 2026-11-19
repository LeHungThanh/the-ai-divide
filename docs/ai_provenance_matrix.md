# Assignment 3 Part 2 — Team AI provenance

## Evidence and attribution standard

This record separates verified project artifacts from member-specific claims. The team roster and page assignments below were supplied in the project instructions. The repository documents project-level Codex assistance, but it does not preserve per-member chat exports, model/version metadata, or signed member confirmations. A Git commit's configured author name is not sufficient evidence that its code was written without AI or that the named person performed every review step.

“Workstream evidenced” means the described implementation is present in the repository and can be checked. It does not, by itself, prove which person authored, edited, or tested it. Where a member's own AI interaction is unavailable, this matrix says so rather than assigning project-wide AI use to that person.

## Summary matrix

| Member and assigned section | Evidence status | AI tool / model | Member confirmation |
|---|---|---|---|
| Mehul Joshi — Country Divide | Workstream evidenced; individual AI use and authorship not established | Project-level Codex assistance is disclosed; no member-specific tool or model record | Required |
| Yixin Huang — Company Size | Workstream evidenced; individual AI use and authorship not established | Project-level Codex assistance is disclosed; no member-specific tool or model record | Required |
| Ashwinlingesh Sangeetha Ravichand — Industry Divide | Workstream evidenced; individual AI use and authorship not established | Project-level Codex assistance is disclosed; no member-specific tool or model record | Required |
| Le Hung Thanh — Adoption Barriers | User-requested barrier requirements and project-level Codex implementation are evidenced; personal review and final member confirmation are not | OpenAI Codex; exact model/version is not recorded | Required |

## Project-wide integration and development record

| Field | Evidence-based record |
|---|---|
| Tool and model | The project disclosure names OpenAI Codex. The exact model/version for the historical work is not recorded in the repository or commit metadata. |
| Period and tasks | Project history spans 21 October–19 November 2026. The documented Codex-assisted work includes the Streamlit application structure and Python implementation, chart design and data-selection logic, visual redesign and motion work, reproducible Eurostat preparation/validation scripts, documentation, and automated tests. This is a project-level record and is not assigned wholesale to any one page member. |
| Prompt evidence | The chat history contains user requests for the MVP, interface improvements, the animation experiment, barrier comparisons, reproducibility and Part 2 completion. Exact prompts and full session transcripts are not archived as project artifacts; prompts for other members are unavailable. |
| Output retained | `app.py`, `pages/`, `src/`, `scripts/`, `tests/`, `docs/`, and review artifacts. The data remain the bundled Eurostat source snapshots and their processed outputs. |
| Human direction and edits | The project owner supplied requirements, corrected scope, reviewed outputs, and directed which changes to retain. Repository history does not identify line-by-line human edits separately from AI-generated or AI-assisted changes. No manual edit is attributed to another member without that member's account. |
| Verification | On 19 November 2026, the project suite passed 15 tests, including page smoke/workflow checks, data and barrier regressions, accessibility checks, and exact-output reproducibility. CSV regeneration retained the committed SHA-256 values; `scripts/validate_data.py` passed with a documented Eurostat publication-vintage warning. These are project checks, not proof of an individual member's personal verification. |
| Outcome | Project implementation and verification evidence are retained. Member-specific prompts, outputs, edits, and confirmations remain incomplete and must be supplied by the members. |

Relevant history: `6409a1d` (MVP, 21 Oct 2026), `4d47d42` (barrier size-filter correction, 21 Oct 2026), `c52252a` (visual redesign, 14 Nov 2026), `61dd495` (motion experiment, 18 Nov 2026), `ed13010` (barrier comparison upgrade, 18 Nov 2026), `b2c16f1` (Part 2 evidence and reproducibility, 18 Nov 2026), and `68f3176` (publication/performance record, 19 Nov 2026). These commits identify project artifacts and dates; the configured Git author is not used here as sole proof of individual authorship.

## Member 1 — Mehul Joshi — Country Divide

| Field | Record |
|---|---|
| Assigned technical workstream | Present Member State adoption rankings against Eurostat's supplied EU27 aggregate, with year selection and a selected-country time series. Country observations are not replaced by an unweighted EU mean. |
| Tool / model and date | The project-level disclosure confirms Codex assistance, but no interaction or model/version is attributable to Mehul. The page is present in the MVP and subsequent project history; Mehul's own development date is unavailable. |
| Prompt or request | No prompt authored by Mehul or page-specific chat transcript is preserved. The functional requirements in the project README and `docs/member_contributions.md` describe the workstream, not a verified prompt from him. |
| Output retained | `pages/2_Country_Divide.py` reads `data/processed/01_country_adoption.csv`, displays country rankings and an EU benchmark, and plots the selected country against the EU series. Source-trace and missing/flag notes use shared helpers in `src/ui.py`. |
| Human edits / decisions | The repository does not distinguish Mehul's edits from shared or AI-assisted edits. His personal design decisions and acceptance/revision history require his confirmation. |
| Verification and result | Project evidence: `tests/test_page_smoke.py` renders all six pages and exercises country/year workflows; `tests/test_data.py` checks reference values, source keys and missing observations. `scripts/validate_data.py` compares processed rows with bundled source cubes. The 15-test project suite passed on 19 Nov 2026. No member-specific test run by Mehul is evidenced. |
| Evidence references | `pages/2_Country_Divide.py`; `data/processed/01_country_adoption.csv`; `tests/test_page_smoke.py`; `tests/test_data.py`; `scripts/validate_data.py`; commits `6409a1d`, `c52252a`, `b2c16f1`. |
| Outcome / open item | The Country Divide workstream is implemented and project-verified. Mehul must confirm whether and how he used AI, provide any required prompt/output record, describe his own changes and review, and verify this entry. |

## Member 2 — Yixin Huang — Company Size

| Field | Record |
|---|---|
| Assigned technical workstream | Compare official small (`10–49`), medium (`50–249`) and large (`GE250`) enterprise classes, calculate a large-minus-small percentage-point gap, show the time trend, and allow country/year selection. Overlapping aggregates such as `GE10` are excluded from this three-class comparison. |
| Tool / model and date | Codex is disclosed for the shared project, but no AI session or model/version is attributable to Yixin. Her own development date is unavailable; commit dates only bound the presence of project files. |
| Prompt or request | No Yixin-authored prompt or member-specific session is preserved. README workflow descriptions and the project role table document expected functionality, not her exact prompt. |
| Output retained | `pages/3_Company_Size.py` renders the selected-year comparison and multi-year series from `data/processed/02_company_size.csv`; `src/data.py` defines the nonoverlapping size classes. The calculation is the difference between source percentages, in percentage points. |
| Human edits / decisions | Personal code edits, chart choices, and acceptance decisions cannot be isolated from the shared repository. These require Yixin's confirmation. |
| Verification and result | Project evidence: `tests/test_page_smoke.py` exercises company-size/year workflow; `tests/test_barrier_comparisons.py` checks analogous source-rate difference handling; `tests/test_data.py` checks data reference values and missingness. All 15 project tests passed on 19 Nov 2026. No Yixin-specific verification session is evidenced. |
| Evidence references | `pages/3_Company_Size.py`; `src/data.py`; `data/processed/02_company_size.csv`; `tests/test_page_smoke.py`; `tests/test_data.py`; commits `6409a1d`, `1934308`, `c52252a`, `b2c16f1`. |
| Outcome / open item | The Company Size workstream and its project checks are present. Yixin must confirm actual AI use or explicitly state none, describe her edits and review, provide required provenance evidence, and approve this entry. |

## Member 3 — Ashwinlingesh Sangeetha Ravichand — Industry Divide

| Field | Record |
|---|---|
| Assigned technical workstream | Show an industry-by-year heatmap and year-specific ranking, provide country/year/sector filters, avoid combining overlapping NACE aggregates, and leave missing source observations blank. |
| Tool / model and date | The repository's project-level Codex disclosure does not establish that Ashwinlingesh used Codex or any other AI tool. No member-specific model/version or development date is available. |
| Prompt or request | No prompt authored by Ashwinlingesh or page-specific AI record is preserved. The functional description in the project role table is an assignment summary, not a verified prompt. |
| Output retained | `pages/4_Industry_Divide.py` uses `comparison_sectors()` from `src/data.py` and `data/processed/03_industry_adoption.csv`. The selection comprises distinct NACE sections plus the covered repair group S951; an empty selection has an explanatory state, and missing cells are not filled with zero. |
| Human edits / decisions | The repository does not identify individual code edits or record Ashwinlingesh's own filter, sector-partition, or missing-data decisions. Member confirmation is needed. |
| Verification and result | `tests/test_page_smoke.py` renders the industry page and checks the clear-all empty state; `tests/test_data.py` checks distinct sectors and missing values. The project-wide 15-test suite passed on 19 Nov 2026, and source-level validation passed with its documented vintage warning. These checks are not attributed to Ashwinlingesh personally. |
| Evidence references | `pages/4_Industry_Divide.py`; `src/data.py`; `data/processed/03_industry_adoption.csv`; `tests/test_page_smoke.py`; `tests/test_data.py`; `scripts/validate_data.py`; commits `6409a1d`, `c52252a`, `b2c16f1`. |
| Outcome / open item | The Industry Divide workstream is implemented and project-verified. Ashwinlingesh must provide his AI-use or no-AI account, prompt/output and edit details where relevant, his own verification, and confirmation. |

## Member 4 — Le Hung Thanh — Adoption Barriers

| Field | Record |
|---|---|
| Assigned technical workstream | Review barrier charts and comparison logic; keep `PC_ENT_AI_EC` as the denominator (enterprises that considered AI but did not adopt it); retain `GE10` as the main chart default; compare size groups and Member States against Eurostat's supplied EU27 values; inspect displayed values against source observations. |
| Tool / model and date | Codex assistance is documented for the shared application. The exact model/version is not recorded. The conversation includes a specific user request to let `barriers(size=None)` retain all classes, use that for barrier comparisons, preserve the denominator and filters, add regression coverage, and keep the page's `GE10` default. The associated project correction is commit `4d47d42` (21 Oct 2026); comparison development is also present in `ed13010` (18 Nov 2026). |
| Prompt summary | Evidence-supported summary of the user request: permit unfiltered size selection in `barriers()`, load all sizes for comparison calculations, preserve `PC_ENT_AI_EC` and other filters, keep the displayed main chart at `GE10`, and verify with a regression test. This task request is evidenced; it does not establish the full history of Le's other AI interactions. |
| Output retained | `src/data.py` supports `size=None`; `pages/5_Adoption_Barriers.py` loads all size rows for comparison logic and selects `GE10` for the main chart by default. `src/barrier_comparisons.py` filters by the considered-AI denominator and overall activity, compares the disjoint `10-49` and `GE250` groups, and compares country observations with the supplied EU aggregate. Plots preserve missing values, flags, and source traces. |
| Human direction, edits, and decision | Le specified the denominator, size behavior, default, preserved filters, and regression requirement in the conversation and directed the accepted change. The code and commit history do not show which exact lines were manually edited versus produced with Codex. His personal chart-by-chart inspection, independent Eurostat review, and final acceptance of each displayed comparison are not separately documented and need his confirmation. |
| Verification and result | `tests/test_data.py` checks denominator and `size=None` behavior; `tests/test_barrier_comparisons.py` checks denominator exclusion, source-rate gaps, flags/missing values, and comparison classes; `tests/test_page_smoke.py` confirms the main `GE10` default and three rendered charts. Project-level validation checks source observation indices against the bundled Eurostat cubes. The complete 15-test suite passed on 19 Nov 2026. These results verify the implementation, not Le's individual manual review. |
| Evidence references | `pages/5_Adoption_Barriers.py`; `src/data.py`; `src/barrier_comparisons.py`; `data/processed/04_ai_adoption_barriers.csv`; `tests/test_data.py`; `tests/test_barrier_comparisons.py`; `tests/test_page_smoke.py`; `scripts/validate_data.py`; commits `4d47d42`, `ed13010`, `b2c16f1`. |
| Outcome / open item | The specified barrier behavior is implemented and passes project regression checks. Le must confirm the accuracy of this record, add any actual personal review/modification details, and provide any other member-required prompt/tool evidence. His contribution is limited here to the documented Adoption Barriers workstream; broader Codex assistance is recorded separately above. |

## Criterion 28 status and remaining evidence

**Criterion 28 is not yet fully supported by verified individual evidence.** The project-level Codex disclosure and the code/test artifacts establish that AI-assisted project development occurred, but they do not establish each member's actual tools, prompts, retained outputs, human edits, personal checks, or confirmation. Le's specific barrier task request is documented in the conversation; it still does not substitute for his confirmation or a complete individual record. The three other members' AI use (including an explicit no-AI declaration where applicable) must be supplied by them. Update this matrix only from those direct accounts and retain any prompt or output evidence the assignment requires.
