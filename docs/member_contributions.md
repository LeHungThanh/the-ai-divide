# Assigned workstreams and design decisions

This table records the group's assigned page responsibilities and design decisions. It is not an independently verified record of individual authorship or contribution. The [AI provenance matrix](ai_provenance_matrix.md) separately records reconstructed AI-use summaries and project-level verification procedures.

| Member | Page | Design decision | Source dataset |
|---|---|---|---|
| Mehul Joshi | Country Divide | Rank national observations separately from the Eurostat EU benchmark; permit a selected-country trend. | `01_country_adoption.csv` |
| Yixin Huang | Company Size | Compare only nonoverlapping small, medium and large classes and show a percentage-point gap. | `02_company_size.csv` |
| Ashwinlingesh Sangeetha Ravichand | Industry Divide | Use a distinct NACE comparison partition and show both a year-by-sector heatmap and ranking. | `03_industry_adoption.csv` |
| Le Hung Thanh | Adoption Barriers | Keep the `PC_ENT_AI_EC` conditional denominator and multi-response explanation; compare the disjoint `10-49` and `GE250` classes and each Member State with Eurostat's supplied EU27 aggregate using signed percentage-point gaps. | `04_ai_adoption_barriers.csv` |

The Overview and Conclusion & Sources pages integrate the four workstreams. All member pages expose filters, missing/flagged-cell counts, and a source-trace expander for a displayed value. Shared design and data rules live in `src/`.
