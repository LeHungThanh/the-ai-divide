# Data dictionary

The four CSVs share 25 columns. Encoding: UTF-8; delimiter: comma; decimal separator: point. Booleans are lowercase text. Missing numeric values are empty fields.

Primary key / composite observation identifier: `country_code, year, freq, size_emp, nace_r2, indicator_code, unit`. Values are percentages on a 0–100 scale; 19.95 means 19.95%, not 0.1995.

## Dataset catalogue

| Output CSV | Purpose | Official source and direct API URL | Geographic / time coverage | Latest observation example |
|---|---|---|---|---|
| `01_country_adoption.csv` | Overall enterprise AI adoption by EU country and supplied EU aggregate. | [isoc_eb_ai](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ai?lang=EN) | EU27 + EU27_2020; survey years 2021, 2023, 2024, 2025. | EU27_2020, 2025, GE10, `E_AI_TANY`, `PC_ENT`: **19.95%**. |
| `02_company_size.csv` | Adoption by country and official enterprise employment-size class. | [isoc_eb_ai](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ai?lang=EN) | EU27 + EU27_2020 and retained size classes; survey years 2021, 2023, 2024, 2025. | EU27_2020, 2025, `GE250`, `E_AI_TANY`, `PC_ENT`: **55.03%** (small 10–49: 17.00%; medium 50–249: 30.36%). |
| `03_industry_adoption.csv` | Adoption by country and NACE Rev. 2 activity, including aggregates and non-overlapping comparison partition. | [isoc_eb_ain2](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ain2?lang=EN) | EU27 + EU27_2020 and all source NACE categories; survey years 2021, 2023, 2024, 2025. | EU27_2020, 2025, sector J, `E_AI_TANY`, `PC_ENT`: **62.52%**. |
| `04_ai_adoption_barriers.csv` | Eight reasons for AI non-adoption across size, country and four distinct denominator units. | [isoc_eb_ai](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ai?lang=EN) | EU27 + EU27_2020 and source size classes; survey years 2021, 2023, 2024, 2025. | EU27_2020, 2025, GE10, `E_AI_BLE`, `PC_ENT_AI_EC`: **70.31%** (considered AI but did not adopt). |

All four are Eurostat statistical data. Eurostat’s [reuse notice](https://ec.europa.eu/eurostat/help/copyright-notice) authorises reuse of statistical data and metadata with source acknowledgement, subject to individual notices and listed exceptions; it implements Commission Decision 2011/833/EU. This is not described as a blanket CC BY 4.0 licence for datasets. The notice separately says editorial website content is CC BY 4.0. No contrary dataset-specific notice was present in the bundled cube metadata; users should check the live dataset notice before other reuse.

Source files are exact JSON-stat API responses stored in `data/raw/`; retrieval URL, timestamp, response byte size and SHA-256 are in `data/raw/manifest.json`. The source API reports an update timestamp of 15 June 2026. The source survey covers enterprises in specified activities; the standard comparison population is enterprises with at least 10 persons employed, excluding agriculture, mining and finance.

Transformation: `scripts/prepare_data.py` selects the retained geographies and four actually available survey years from source dimensions, preserves an explicit grid of missing combinations, reads each value/status at its JSON-stat flattened index and writes the columns below. No interpolation, zero-fill, EU averaging or synthetic rows with non-missing percentages are used. Source flags are retained verbatim. Empty percentages mean unavailable, uncollected or suppressed; the source may not distinguish these causes.

| Column | Definition |
|---|---|
| country_code | Eurostat geography identifier; EL=Greece; EU27_2020 is an aggregate. |
| country_name | Official English geography label. |
| year | Integer survey year: 2021, 2023, 2024 or 2025; annual, not an interpolated series. |
| freq | Official frequency code A (annual). |
| size_emp | Official persons-employed size code; includes employees and self-employed persons. |
| size_label | Official size definition; codes are retained verbatim. |
| nace_r2 | Official NACE Rev. 2 activity or aggregate identifier. |
| industry_label | Official activity label; use methodology for exact survey coverage. |
| industry_level | overall_aggregate, section, division, group, or overlapping_group; sections also aggregate their subdivisions. |
| is_comparison_sector | Lowercase true/false. True selects C,D,E,F,G,H,I,J,L,M,N,S951 without overlaps. |
| indicator_code | E_AI_TANY for adoption; eight metadata-discovered reason codes for barriers. |
| indicator_label | Official current English indicator definition; not a per-year questionnaire label. |
| unit | Official unit code; part of the statistical key, never combine different units. |
| unit_label | Exact official percentage unit label. |
| denominator_definition | Official unit population, with considered-but-not-adopted clarification for PC_ENT_AI_EC barrier rows. Always conditional on row geography, activity and size. |
| percentage | Numeric percentage, 0–100, decimal point. Empty = unavailable/suppressed/uncollected; never zero-filled. |
| observation_status | Verbatim source flag, including combinations and punctuation. Empty = no source flag, not proof of availability. |
| status_label | Official description of the whole flag string; empty if unflagged. |
| source_dataset | isoc_eb_ai or isoc_eb_ain2. |
| source_url | Full official API request from selected raw manifest. |
| source_updated | Source dataset update timestamp from JSON-stat metadata, not observation year. |
| retrieved_utc | UTC acquisition timestamp from manifest. |
| raw_file | Repository-relative path to exact unmodified raw JSON response. |
| raw_sha256 | SHA-256 of original response bytes; verifies reproducibility. |
| source_observation_index | Zero-based flattened JSON-stat cell index. Absent value at this index means missing; this is a cube address, not an observed row number. |

## Official size classifications

| Code | Official English label |
|---|---|
| 0_1 | From 0 to 1 person employed |
| 0-9 | From 0 to 9 persons employed |
| 2-9 | From 2 to 9 persons employed |
| 10-49 | From 10 to 49 persons employed |
| 10-249 | From 10 to 249 persons employed |
| GE10 | 10 persons employed or more |
| 50-249 | From 50 to 249 persons employed |
| GE250 | 250 persons employed or more |

## Units and denominator definitions (full raw metadata)

| Code | Official English label |
|---|---|
| PC_ENT | Percentage of enterprises |
| PC_ENT_IUSE | Percentage of enterprises where persons employed have access to the internet |
| PC_ENT_AI_EC | Percentage of the enterprises which ever considered to use any of the AI technologies |
| PC_ENT_AI_TANY | Percentage of the enterprises using at least one AI technologies |
| PC_ENT_AI_TX | Percentage of the enterprises using no AI technologies |
| PC_ENT_AI_PDI | Percentage of the enterprises which process data on individuals using AI technologies |

## AI adoption and all non-adoption barriers

| Code | Official English label |
|---|---|
| E_AI_TANY | Enterprises using at least one of the AI technologies: AI_TTM, AI_TSR, AI_TNLG, AI_TIR, AI_TML, AI_TPA, AI_TAR, E_AI_TPVSG |
| E_AI_BCST | Enterprises do not use AI technologies, because the costs seem too high |
| E_AI_BLE | Enterprises do not use AI technologies, because of a lack of relevant expertise |
| E_AI_BINC | Enterprises do not use AI technologies, because of incompatibility with existing equipment, software or systems |
| E_AI_BDDT | Enterprises do not use AI technologies, because of difficulties with availability or quality of the necessary data |
| E_AI_BCDP | Enterprises do not use AI technologies, because of concerns regarding violation of data protection and privacy |
| E_AI_BLEG | Enterprises do not use AI technologies, because of a lack of clarity about the legal consequences |
| E_AI_BEC | Enterprises do not use AI technologies, because of ethical considerations |
| E_AI_BNU | Enterprises do not use AI technologies, because artificial Intelligence technologies are not useful for Enterprise |

## All industry categories

| Code | Official English label |
|---|---|
| C-F | Manufacturing, electricity, gas, steam and air conditioning supply; water supply and construction |
| C-E | Manufacturing, electricity, gas, steam and air conditioning; water supply, sewerage, waste management and remediation activities |
| C | Manufacturing |
| C10-S951_X_K | All activities (except agriculture, forestry and fishing, and mining and quarrying), without financial sector |
| C10-C18 | Manufacture of products based on: food, beverages, tobacco, textile, leather, wood, pulp and paper; publishing and printing |
| C10-C12 | Manufacture of food products; beverages and tobacco products |
| C13-C15 | Manufacture of textiles, wearing apparel, leather and related products |
| C16-C18 | Manufacture of wood, paper, printing and reproduction |
| C19-C23 | Manufacture of coke, refined petroleum, chemical and basic pharmaceutical products, rubber and plastics, other non-metallic mineral products |
| C19 | Manufacture of coke and refined petroleum products |
| C20 | Manufacture of chemicals and chemical products |
| C21 | Manufacture of basic pharmaceutical products and pharmaceutical preparations |
| C22_C23 | Manufacture of rubber and plastic products and other non-metallic mineral products |
| C24_C25 | Manufacture of basic metals and fabricated metal products, except machinery and equipment |
| C26-C33 | Manufacture of computers, electric and optical products, electrical equipment, machinery and equipment n.e.c, motor vehicles, other transport equipment, furniture, other manufacturing, repair and installation of machinery and equipment |
| C26 | Manufacture of computer, electronic and optical products |
| C27_C28 | Manufacture of electrical equipment, machinery and equipment n.e.c. |
| C27 | Manufacture of electrical equipment |
| C28 | Manufacture of machinery and equipment n.e.c. |
| C29_C30 | Manufacture of motor vehicles, trailers, semi-trailers and of other transport equipment |
| C31-C33 | Manufacture of furniture; jewellery, musical instruments, toys; repair and installation of machinery and equipment |
| D_E | Electricity, gas, steam and air conditioning supply; water supply; sewerage, waste management and remediation activities |
| D | Electricity, gas, steam and air conditioning supply |
| D35 | Electricity, gas, steam and air conditioning supply |
| E | Water supply; sewerage, waste management and remediation activities |
| F | Construction |
| G | Wholesale and retail trade; repair of motor vehicles and motorcycles |
| G45-S951_X_K | Services, without financial sector |
| G45 | Wholesale and retail trade and repair of motor vehicles and motorcycles |
| G46 | Wholesale trade, except of motor vehicles and motorcycles |
| G47 | Retail trade, except of motor vehicles and motorcycles |
| H | Transportation and storage |
| I | Accommodation and food service activities |
| I55 | Accommodation |
| J | Information and communication |
| J58-J60 | Publishing, motion picture, video, television programme production; sound recording, programming and broadcasting activities |
| J61 | Telecommunications |
| J62_J63 | Computer programming, consultancy, and information service activities |
| L_M | Real estate activities; professional, scientific and technical activities |
| L | Real estate activities |
| L68 | Real estate activities |
| M | Professional, scientific and technical activities |
| M69-M71 | Legal and accounting activities; activities of head offices; management consultancy activities; architectural and engineering activities; technical testing and analysis |
| M72 | Scientific research and development |
| M73-M75 | Advertising and market research; other professional, scientific and technical activities; veterinary activities |
| N77-N82_X_N79 | Activities for rental and leasing, employment, security and investigation, services to buildings and landscape, office administrative, office support and other business support |
| N | Administrative and support service activities |
| N79 | Travel agency, tour operator and other reservation service and related activities |
| S951 | Repair of computers and communication equipment |
| ICT | Information and Communication Technology - total |

## Geographies retained

| Code | Official English label |
|---|---|
| AT | Austria |
| BE | Belgium |
| BG | Bulgaria |
| CY | Cyprus |
| CZ | Czechia |
| DE | Germany |
| DK | Denmark |
| EE | Estonia |
| EL | Greece |
| ES | Spain |
| EU27_2020 | European Union - 27 countries (from 2020) |
| FI | Finland |
| FR | France |
| HR | Croatia |
| HU | Hungary |
| IE | Ireland |
| IT | Italy |
| LT | Lithuania |
| LU | Luxembourg |
| LV | Latvia |
| MT | Malta |
| NL | Netherlands |
| PL | Poland |
| PT | Portugal |
| RO | Romania |
| SE | Sweden |
| SI | Slovenia |
| SK | Slovakia |

## Source observation flags

| Code | Official meaning |
|---|---|
| u | low reliability |
| b | break in time series |
| &#124;C | &#124;confidential |
| d | definition differs (see metadata) |
| bu | break in time series, low reliability |

## Analysis rules

- Size comparisons: 10-49 (small), 50-249 (medium), GE250 (large). GE10 and 10-249 overlap these sizes; microenterprise classes are optional and sparse.
- Industry comparisons: filter is_comparison_sector=true. All other industry rows are retained for drilldown and overlap parts of the comparison partition. A section and its divisions must not be summed.
- Barrier comparisons: fix the unit, size and activity. PC_ENT_AI_EC means the considered-but-not-adopted group; PC_ENT_AI_TX means all non-users; PC_ENT means all enterprises in scope; PC_ENT_IUSE means the internet-access population.
- Unit definitions for PC_ENT_AI_TANY and PC_ENT_AI_PDI are included from full metadata for transparency but are not applicable barrier output planes in this snapshot.
- Percentages across countries or industries require statistical weights to aggregate. EU values are supplied by Eurostat, not computed as country means.
- Keep flags with charts and report missing coverage. See data_sources.md for questionnaire changes and data_validation_report.md for the publication-vintage discrepancy.
