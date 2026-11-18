# Data validation report

Generated (UTC): 2026-11-18T06:32:46.406870+00:00

Reproduce: `python3 scripts/validate_data.py`. Empty percentages mean missing, never zero.

## Raw source inventory

| Dataset | Cube cells | Numeric observations | Status entries | Updated |
|---|---:|---:|---:|---|
| isoc_eb_ai | 435,456 | 70,756 | 2,661 | 2026-06-15T11:00:00+0200 |
| isoc_eb_ain2 | 2,721,600 | 580,454 | 111,108 | 2026-06-15T11:00:00+0200 |

## Member 1: 01_country_adoption.csv

- Rows: **112**; non-missing: **112**; missing: **0**; duplicate keys: 0.
- Countries: AT, BE, BG, CY, CZ, DE, DK, EE, EL, ES, EU27_2020, FI, FR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK (27 countries + EU aggregate).
- Years: 2021, 2023, 2024, 2025.
- Sizes: GE10.
- Industries (1): C10-S951_X_K.
- Units: PC_ENT.
- Flags (including missing cells): `{'(none)': 109, 'b': 3}`.
- Every output cell was traced to its JSON-stat index, including missing values and flags.

### Non-missing coverage by year and unit

| Year | Unit | Rows | Non-missing |
|---|---|---:|---:|
| 2021 | PC_ENT | 28 | 28 |
| 2023 | PC_ENT | 28 | 28 |
| 2024 | PC_ENT | 28 | 28 |
| 2025 | PC_ENT | 28 | 28 |

### Sample raw trace

Key: `{'country_code': 'AT', 'year': '2021', 'freq': 'A', 'size_emp': 'GE10', 'nace_r2': 'C10-S951_X_K', 'indicator_code': 'E_AI_TANY', 'unit': 'PC_ENT'}`.
Value: 8.83; status: `(none)`; raw file: `data/raw/isoc_eb_ai_5c8d7f499bc36b74.json`; JSON-stat `value["278292"]`.

### Columns

`country_code, country_name, year, freq, size_emp, size_label, nace_r2, industry_label, industry_level, is_comparison_sector, indicator_code, indicator_label, unit, unit_label, denominator_definition, percentage, observation_status, status_label, source_dataset, source_url, source_updated, retrieved_utc, raw_file, raw_sha256, source_observation_index`

### Five sample observations

| Country | Year | Size | Industry | Indicator | Unit | Percentage | Flag |
|---|---|---|---|---|---|---:|---|
| AT | 2021 | GE10 | C10-S951_X_K | E_AI_TANY | PC_ENT | 8.83 |  |
| AT | 2023 | GE10 | C10-S951_X_K | E_AI_TANY | PC_ENT | 10.79 |  |
| AT | 2024 | GE10 | C10-S951_X_K | E_AI_TANY | PC_ENT | 20.27 |  |
| AT | 2025 | GE10 | C10-S951_X_K | E_AI_TANY | PC_ENT | 29.95 |  |
| BE | 2021 | GE10 | C10-S951_X_K | E_AI_TANY | PC_ENT | 10.32 |  |

## Member 2: 02_company_size.csv

- Rows: **896**; non-missing: **586**; missing: **310**; duplicate keys: 0.
- Countries: AT, BE, BG, CY, CZ, DE, DK, EE, EL, ES, EU27_2020, FI, FR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK (27 countries + EU aggregate).
- Years: 2021, 2023, 2024, 2025.
- Sizes: 0-9, 0_1, 10-249, 10-49, 2-9, 50-249, GE10, GE250.
- Industries (1): C10-S951_X_K.
- Units: PC_ENT.
- Flags (including missing cells): `{'(none)': 883, 'b': 13}`.
- Every output cell was traced to its JSON-stat index, including missing values and flags.

### Non-missing coverage by year and unit

| Year | Unit | Rows | Non-missing |
|---|---|---:|---:|
| 2021 | PC_ENT | 224 | 146 |
| 2023 | PC_ENT | 224 | 146 |
| 2024 | PC_ENT | 224 | 149 |
| 2025 | PC_ENT | 224 | 145 |

### Sample raw trace

Key: `{'country_code': 'AT', 'year': '2021', 'freq': 'A', 'size_emp': '10-49', 'nace_r2': 'C10-S951_X_K', 'indicator_code': 'E_AI_TANY', 'unit': 'PC_ENT'}`.
Value: 7.14; status: `(none)`; raw file: `data/raw/isoc_eb_ai_5c8d7f499bc36b74.json`; JSON-stat `value["169428"]`.

### Columns

`country_code, country_name, year, freq, size_emp, size_label, nace_r2, industry_label, industry_level, is_comparison_sector, indicator_code, indicator_label, unit, unit_label, denominator_definition, percentage, observation_status, status_label, source_dataset, source_url, source_updated, retrieved_utc, raw_file, raw_sha256, source_observation_index`

### Five sample observations

| Country | Year | Size | Industry | Indicator | Unit | Percentage | Flag |
|---|---|---|---|---|---|---:|---|
| AT | 2021 | 10-49 | C10-S951_X_K | E_AI_TANY | PC_ENT | 7.14 |  |
| AT | 2021 | 10-249 | C10-S951_X_K | E_AI_TANY | PC_ENT | 8.15 |  |
| AT | 2021 | GE10 | C10-S951_X_K | E_AI_TANY | PC_ENT | 8.83 |  |
| AT | 2021 | 50-249 | C10-S951_X_K | E_AI_TANY | PC_ENT | 14.57 |  |
| AT | 2021 | GE250 | C10-S951_X_K | E_AI_TANY | PC_ENT | 31.73 |  |

## Member 3: 03_industry_adoption.csv

- Rows: **5,600**; non-missing: **4,796**; missing: **804**; duplicate keys: 0.
- Countries: AT, BE, BG, CY, CZ, DE, DK, EE, EL, ES, EU27_2020, FI, FR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK (27 countries + EU aggregate).
- Years: 2021, 2023, 2024, 2025.
- Sizes: GE10.
- Industries (50): C, C-E, C-F, C10-C12, C10-C18, C10-S951_X_K, C13-C15, C16-C18, C19, C19-C23, C20, C21, C22_C23, C24_C25, C26, C26-C33, C27, C27_C28, C28, C29_C30, C31-C33, D, D35, D_E, E, F, G, G45, G45-S951_X_K, G46, G47, H, I, I55, ICT, J, J58-J60, J61, J62_J63, L, L68, L_M, M, M69-M71, M72, M73-M75, N, N77-N82_X_N79, N79, S951.
- Units: PC_ENT.
- Flags (including missing cells): `{'(none)': 4721, 'u': 693, '|C': 84, 'b': 101, 'bu': 1}`.
- Every output cell was traced to its JSON-stat index, including missing values and flags.

### Non-missing coverage by year and unit

| Year | Unit | Rows | Non-missing |
|---|---|---:|---:|
| 2021 | PC_ENT | 1400 | 1206 |
| 2023 | PC_ENT | 1400 | 1205 |
| 2024 | PC_ENT | 1400 | 1206 |
| 2025 | PC_ENT | 1400 | 1179 |

### Sample raw trace

Key: `{'country_code': 'AT', 'year': '2021', 'freq': 'A', 'size_emp': 'GE10', 'nace_r2': 'C-F', 'indicator_code': 'E_AI_TANY', 'unit': 'PC_ENT'}`.
Value: 6.64; status: `(none)`; raw file: `data/raw/isoc_eb_ain2_b298f73b97acddea.json`; JSON-stat `value["6132"]`.

### Columns

`country_code, country_name, year, freq, size_emp, size_label, nace_r2, industry_label, industry_level, is_comparison_sector, indicator_code, indicator_label, unit, unit_label, denominator_definition, percentage, observation_status, status_label, source_dataset, source_url, source_updated, retrieved_utc, raw_file, raw_sha256, source_observation_index`

### Five sample observations

| Country | Year | Size | Industry | Indicator | Unit | Percentage | Flag |
|---|---|---|---|---|---|---:|---|
| AT | 2021 | GE10 | C-F | E_AI_TANY | PC_ENT | 6.64 |  |
| AT | 2021 | GE10 | C-E | E_AI_TANY | PC_ENT | 9.78 |  |
| AT | 2021 | GE10 | C | E_AI_TANY | PC_ENT | 9.61 |  |
| AT | 2021 | GE10 | C10-S951_X_K | E_AI_TANY | PC_ENT | 8.83 |  |
| AT | 2021 | GE10 | C10-C18 | E_AI_TANY | PC_ENT | 4.56 |  |

## Member 4: 04_ai_adoption_barriers.csv

- Rows: **28,672**; non-missing: **14,080**; missing: **14,592**; duplicate keys: 0.
- Countries: AT, BE, BG, CY, CZ, DE, DK, EE, EL, ES, EU27_2020, FI, FR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK (27 countries + EU aggregate).
- Years: 2021, 2023, 2024, 2025.
- Sizes: 0-9, 0_1, 10-249, 10-49, 2-9, 50-249, GE10, GE250.
- Industries (1): C10-S951_X_K.
- Units: PC_ENT, PC_ENT_AI_EC, PC_ENT_AI_TX, PC_ENT_IUSE.
- Flags (including missing cells): `{'(none)': 28228, 'u': 284, 'b': 160}`.
- Every output cell was traced to its JSON-stat index, including missing values and flags.

### Non-missing coverage by year and unit

| Year | Unit | Rows | Non-missing |
|---|---|---:|---:|
| 2021 | PC_ENT | 1792 | 830 |
| 2021 | PC_ENT_AI_EC | 1792 | 822 |
| 2021 | PC_ENT_AI_TX | 1792 | 830 |
| 2021 | PC_ENT_IUSE | 1792 | 830 |
| 2023 | PC_ENT | 1792 | 890 |
| 2023 | PC_ENT_AI_EC | 1792 | 890 |
| 2023 | PC_ENT_AI_TX | 1792 | 890 |
| 2023 | PC_ENT_IUSE | 1792 | 890 |
| 2024 | PC_ENT | 1792 | 904 |
| 2024 | PC_ENT_AI_EC | 1792 | 904 |
| 2024 | PC_ENT_AI_TX | 1792 | 904 |
| 2024 | PC_ENT_IUSE | 1792 | 904 |
| 2025 | PC_ENT | 1792 | 898 |
| 2025 | PC_ENT_AI_EC | 1792 | 898 |
| 2025 | PC_ENT_AI_TX | 1792 | 898 |
| 2025 | PC_ENT_IUSE | 1792 | 898 |

### Sample raw trace

Key: `{'country_code': 'AT', 'year': '2021', 'freq': 'A', 'size_emp': '10-49', 'nace_r2': 'C10-S951_X_K', 'indicator_code': 'E_AI_BCST', 'unit': 'PC_ENT'}`.
Value: 3.13; status: `(none)`; raw file: `data/raw/isoc_eb_ai_5c8d7f499bc36b74.json`; JSON-stat `value["184116"]`.

### Columns

`country_code, country_name, year, freq, size_emp, size_label, nace_r2, industry_label, industry_level, is_comparison_sector, indicator_code, indicator_label, unit, unit_label, denominator_definition, percentage, observation_status, status_label, source_dataset, source_url, source_updated, retrieved_utc, raw_file, raw_sha256, source_observation_index`

### Five sample observations

| Country | Year | Size | Industry | Indicator | Unit | Percentage | Flag |
|---|---|---|---|---|---|---:|---|
| AT | 2021 | 10-49 | C10-S951_X_K | E_AI_BCST | PC_ENT | 3.13 |  |
| AT | 2021 | 10-49 | C10-S951_X_K | E_AI_BCST | PC_ENT_IUSE | 3.16 |  |
| AT | 2021 | 10-49 | C10-S951_X_K | E_AI_BCST | PC_ENT_AI_EC | 50.58 |  |
| AT | 2021 | 10-49 | C10-S951_X_K | E_AI_BCST | PC_ENT_AI_TX | 3.42 |  |
| AT | 2021 | 10-49 | C10-S951_X_K | E_AI_BLE | PC_ENT | 3.45 |  |

## Published 2025 reference checks

[Official Eurostat publication](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) (December 2025 data extraction).

| Country | Size | Indicator | Unit | Download | Reference | Result |
|---|---|---|---|---:|---:|---|
| EU27_2020 | GE10 | E_AI_TANY | PC_ENT | 19.95 | 19.95 | PASS |
| DK | GE10 | E_AI_TANY | PC_ENT | 42.03 | 42.03 | PASS |
| RO | GE10 | E_AI_TANY | PC_ENT | 5.21 | 5.21 | PASS |
| EU27_2020 | GE250 | E_AI_TANY | PC_ENT | 55.03 | 55.03 | PASS |
| EU27_2020 | GE10 | E_AI_BLE | PC_ENT_AI_EC | 70.31 | 70.89 | KNOWN SOURCE-VINTAGE DIFFERENCE |

### Expertise barrier discrepancy investigation

The separate [targeted official API request](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ai?lang=EN&freq=A&size_emp=GE10&nace_r2=C10-S951_X_K&indic_is=E_AI_BLE&unit=PC_ENT_AI_EC&geo=EU27_2020&time=2025) returns **70.31%**, confirming the complete-cube observation with the same dimensions and denominator. Its preserved response is `data/raw/reference_probe_225f34472ea1758d.json`.
The complete source cube was updated on 2026-06-15, after the publication data extraction in December 2025. The difference is -0.58 percentage points. Other EU barrier figures also differ from the article (legal uncertainty: current 53.61 vs published 52.52; privacy: current 52.72 vs published 48.83). This supports a source-vintage/revision explanation, rather than a decoding or unit-selection error. The API does not give a revision reason or a cell-level revision history, so the exact cause remains unconfirmed. The original 70.31 is retained; 70.89 is never substituted.

## Interpretation and limitations

- Missing grids are explicit: an empty cell can mean unavailable, not collected, or suppressed; a missing flag alone cannot distinguish those reasons.
- Optional microenterprise size classes have sparse national coverage. Use 10-49, 50-249 and GE250 for the standard size comparison; GE10 and 10-249 overlap these groups.
- Barrier observations exist in all four survey years, with availability varying by country and size. See year/unit coverage above. Preserve missing rows; do not impute them.
- Barriers permit multiple responses and do not sum to 100%. The PC_ENT_AI_EC denominator concerns non-users who considered AI; PC_ENT, PC_ENT_IUSE and PC_ENT_AI_TX have different denominators.
- Industry rates cannot be summed or averaged into totals without enterprise weights. Filter is_comparison_sector=true for the non-overlapping sector partition; other rows overlap.
- Eurostat flags include breaks in time series (notably Netherlands 2025), differing definitions, low reliability and confidentiality. Consult source metadata before comparing flagged observations.
- Current category labels are not a historical questionnaire. Language/code generation and image/video/audio generation changed across survey rounds; long-run adoption differences can reflect both uptake and questionnaire changes. No harmonisation or interpolation has been applied.
- EU aggregate is the supplied Eurostat statistic, not an unweighted country average. Survey coverage excludes enterprises below 10 persons for standard comparisons, agriculture, mining, finance and most other S activities.

## Result

Structural, raw-trace, bounds, duplicate and metadata checks: **PASS**.

**PASS WITH DOCUMENTED PUBLICATION-VINTAGE DIFFERENCE**

- Warning: Documented publication-vintage difference: Eurostat article 70.89 vs June 2026 cube 70.31 for EU27_2020/2025/GE10/E_AI_BLE/PC_ENT_AI_EC; exact revision reason unconfirmed.
