# Member pages and design decisions

The division below describes the MVP workstream and page responsibilities, not verified individual labor or names. The group can replace these role descriptions with its actual contribution record before submission.

| Member | Page | Design decision | Source dataset |
|---|---|---|---|
| 1 | Country Divide | Rank national observations separately from the Eurostat EU benchmark; permit a selected-country trend. | `01_country_adoption.csv` |
| 2 | Company Size | Compare only nonoverlapping small, medium and large classes and show a percentage-point gap. | `02_company_size.csv` |
| 3 | Industry Divide | Use a distinct NACE comparison partition and show both a year-by-sector heatmap and ranking. | `03_industry_adoption.csv` |
| 4 | Adoption Barriers | Keep the `PC_ENT_AI_EC` conditional denominator and multi-response explanation; compare the disjoint `10-49` and `GE250` classes and each Member State with Eurostat's supplied EU27 aggregate using signed percentage-point gaps. | `04_ai_adoption_barriers.csv` |

The Overview and Conclusion & Sources pages integrate the four workstreams. All member pages expose filters, missing/flagged-cell counts, and a source-trace expander for a displayed value. Shared design and data rules live in `src/`. The project group should review the prose and interpretation before assessment or public deployment.
