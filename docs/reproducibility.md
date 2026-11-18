# Reproducing the processed data

The four processed tables are derived from the exact Eurostat JSON-stat snapshots in `data/raw/`. No network access is needed to regenerate them.

```sh
python scripts/prepare_data.py
python scripts/validate_data.py
python -m unittest discover -s tests -v
```

`prepare_data.py` uses only the Python standard library. It writes the four files under `data/processed/` and refreshes the machine-generated parts of `docs/data_dictionary.md`. `validate_data.py` checks raw-file SHA-256 values against the manifest, re-derives expected observations from the JSON-stat cubes, validates schemas, keys, flags, missingness, bounds, labels, source traces, coverage and selected published references. The regression test also requires exact SHA-256 equality with the checked-in CSV snapshots:

| Output | SHA-256 |
|---|---|
| `01_country_adoption.csv` | `8631f2306b4259a6ff355d973c57b76dc4f2171d9dcf5075b85c5266040f817d` |
| `02_company_size.csv` | `ada63d0b725cc80abab19d1b2bd4e7f4d4c109484b05b603046bc50510c22907` |
| `03_industry_adoption.csv` | `e8b9171b58d66abc242b069c8521a8cb20ab0afb34ee6d14783cfdb1a5f21c50` |
| `04_ai_adoption_barriers.csv` | `ee45f84a2cb02db650f4ad42d7319dc05c8f9a7254ca7b510017deba0c9b759a` |

The current full cube and independent targeted API snapshot both report 70.31% for the 2025 EU expertise barrier. Eurostat's December 2025 article reports 70.89%. The validator preserves both figures and reports this as a known source-vintage warning; it does not change source values or count the documented discrepancy as a reproducibility failure. The exact revision reason is unknown. See `docs/data_validation_report.md`.

`scripts/download_eurostat.py --refresh` is optional and changes the raw snapshot vintage; do not run it when reproducing the published project state. It downloads directly from official Eurostat endpoints and records URLs, retrieval times and hashes. The current app reads only the checked-in processed files.
