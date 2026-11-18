"""Exact raw-cube regeneration checks for the committed processed data."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_OUTPUTS = {
    "01_country_adoption.csv": "8631f2306b4259a6ff355d973c57b76dc4f2171d9dcf5075b85c5266040f817d",
    "02_company_size.csv": "ada63d0b725cc80abab19d1b2bd4e7f4d4c109484b05b603046bc50510c22907",
    "03_industry_adoption.csv": "e8b9171b58d66abc242b069c8521a8cb20ab0afb34ee6d14783cfdb1a5f21c50",
    "04_ai_adoption_barriers.csv": "ee45f84a2cb02db650f4ad42d7319dc05c8f9a7254ca7b510017deba0c9b759a",
}


class ReproducibilityTests(unittest.TestCase):
    def test_raw_files_match_manifest_and_processed_outputs_regenerate_exactly(self):
        manifest = json.loads((ROOT / "data/raw/manifest.json").read_text())
        for dataset in ("isoc_eb_ai", "isoc_eb_ain2"):
            entry = manifest[dataset]
            raw_path = ROOT / entry["file"]
            digest = hashlib.sha256(raw_path.read_bytes()).hexdigest()
            self.assertEqual(digest, entry["sha256"], dataset)

        run = subprocess.run(
            [sys.executable, "scripts/prepare_data.py"], cwd=ROOT,
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        for filename, expected in EXPECTED_OUTPUTS.items():
            actual = hashlib.sha256((ROOT / "data/processed" / filename).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, filename)


if __name__ == "__main__":
    unittest.main()
