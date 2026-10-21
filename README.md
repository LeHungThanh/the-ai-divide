# The AI Divide: Who Is Being Left Behind?

A six-page Streamlit MVP for EU policymakers asking whether business AI adoption is becoming more inclusive or whether a digital divide is emerging.

## Run locally

From this repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

On Windows, activate with `.venv\Scripts\activate`. Then open the URL printed by Streamlit, normally `http://localhost:8501`. The CSVs are already present in `data/processed/`; no download is needed. A local copy of the supplied archive is preserved at `data/processed.zip` and excluded from Git deployment. To restore its four CSVs, run `unzip -oq data/processed.zip 'processed/*.csv' -d data`.

## Deploy

Publish the `codex/ai-divide-streamlit-deploy` branch after the group's own review, then create a Streamlit Community Cloud app with **entry point `app.py`** and **Python 3.12** in Advanced settings. The host installs the root `requirements.txt`. Keep the four CSVs under `data/processed/` in the deployed repository. Other hosts can use `python -m streamlit run app.py --server.address 0.0.0.0 --server.port $PORT` with a supplied `PORT` environment variable. No secrets or API credentials are required.

## Verify

```sh
python -m unittest discover -s tests -v
python -m streamlit run app.py --server.headless true
```

The app has Overview, four member pages, and Conclusion & Sources. Member pages include source-trace expanders, denominator labels, quality flags, and working filters. Charts omit missing values; the UI never replaces them with zero. Files are read locally at runtime.

The data covers 2021, 2023, 2024 and 2025; 2022 is unavailable. The `processed.zip` archive contains processed CSVs but no original raw Eurostat cubes. The 2025 EU expertise-barrier observation is 70.31% in the supplied snapshot, compared with 70.89% in Eurostat's December 2025 article. See [data sources](docs/data_sources.md), [member page decisions](docs/member_contributions.md), and [AI disclosure](docs/ai_usage.md).
