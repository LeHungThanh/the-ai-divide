# Data sources and interpretation

The supplied archive is preserved locally at `data/processed.zip` for reproducibility; the four extracted CSVs are the deployment files.

The MVP reads the four CSVs supplied in `processed.zip` and extracted to `data/processed/`. The processed files report their source datasets as [Eurostat `isoc_eb_ai`](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table?lang=en) and [Eurostat `isoc_eb_ain2`](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ain2/default/table?lang=en). The [official statistics API guide](https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-getting-started/api) describes the JSON-stat source format. The supplied rows say the source dataset was updated 15 June 2026. The ZIP **does not contain the original Eurostat raw JSON-stat responses**. Each row carries a URL, update timestamp, raw-file path, SHA-256 and JSON-stat observation index from the prior processing run. Those fields allow a source lookup but cannot be independently verified against the absent raw cube in this MVP.

## Selections

- Overall adoption: `E_AI_TANY`, `PC_ENT`, `GE10`, `C10-S951_X_K`. Country charts use the 27 national observations; the EU benchmark is the supplied `EU27_2020` observation, never an unweighted country mean.
- Size: `10-49`, `50-249`, and `GE250`. Gap = large rate minus small rate in percentage points, within the same country and year. Other source size classes overlap or have sparse optional coverage.
- Industry: `E_AI_TANY`, `PC_ENT`, `GE10` with distinct NACE categories C, D, E, F, G, H, I, J, L, M, N and S951. Broader aggregates and subgroups in the source CSV overlap these rows. Sector percentages cannot be summed or averaged into an overall percentage.
- Barriers: use `PC_ENT_AI_EC` throughout the page. It is the relevant population of enterprises that considered AI but did not use it. `PC_ENT`, `PC_ENT_AI_TX` and `PC_ENT_IUSE` have different denominators. The eight barrier questions allow multiple responses, so results need not sum to 100%.

The four survey years are 2021, 2023, 2024 and 2025. Missing percentage fields are loaded as missing and excluded from plotted marks; never converted to zero. Source observation flags, including time-series breaks and low reliability, are exposed in chart hover and a quality-flags expander. The standard survey is of enterprises with at least 10 persons employed in selected NACE activities, excluding agriculture, mining and finance. See the [Eurostat explanatory article](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) for survey context.

## Comparability and publication vintage

Eurostat's [December 2025 news item](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2) says AI generation of pictures, video and sound/audio was a new 2025 category, absent from the 2024 questionnaire. Adoption changes across years may therefore reflect both uptake and changing technology scope. The article reports a 2025 EU expertise barrier of 70.89%, while the supplied later processed source snapshot has 70.31% for `EU27_2020 / GE10 / E_AI_BLE / PC_ENT_AI_EC`. The original data-preparation report attributes this plausibly to the later data vintage, but the precise revision reason is not known. The app uses the supplied 70.31% and makes the difference visible.

The dashboard is descriptive. It does not estimate causal effects, recompute EU aggregates, or interpolate gaps in the survey series.
