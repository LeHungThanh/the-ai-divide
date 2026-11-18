"""Regression checks for Adoption Barriers comparison calculations."""
import json
import unittest
from pathlib import Path

import pandas as pd

from src.barrier_comparisons import country_eu_barrier_comparison, size_barrier_comparison
from src.data import CONSIDERED, EU, OVERALL, barriers, load
from streamlit.testing.v1 import AppTest


class BarrierComparisonTests(unittest.TestCase):
    def test_size_gap_matches_source_values_and_categories(self):
        source = load("barrier")
        comparison, rows = size_barrier_comparison(source, "DK", 2025)
        row = comparison.loc[comparison.indicator_code.eq("E_AI_BLE")].iloc[0]
        self.assertEqual(row.small_pct, 82.44)
        self.assertEqual(row.large_pct, 73.48)
        self.assertAlmostEqual(row.difference_pp, 8.96)
        self.assertEqual(set(rows.size_emp), {"10-49", "GE250"})
        self.assertEqual(set(rows.unit), {CONSIDERED})
        self.assertEqual(set(rows.nace_r2), {OVERALL})
        self.assertEqual(set(rows.country_code), {"DK"})

    def test_country_uses_supplied_eu_aggregate_and_signed_gap(self):
        source = load("barrier")
        comparison, rows = country_eu_barrier_comparison(source, "DK", 2025, "10-49")
        row = comparison.loc[comparison.indicator_code.eq("E_AI_BLE")].iloc[0]
        self.assertEqual(row.country_pct, 82.44)
        self.assertEqual(row.eu_pct, 70.87)
        self.assertAlmostEqual(row.difference_pp, 11.57)
        self.assertEqual(set(rows.country_code), {"DK", EU})
        self.assertEqual(set(rows.size_emp), {"10-49"})
        self.assertEqual(set(rows.unit), {CONSIDERED})

    def test_missing_and_flags_are_not_replaced(self):
        source = load("barrier")
        comparison, rows = size_barrier_comparison(source, "BG", 2021)
        unavailable = comparison.loc[
            comparison.indicator_code.eq("E_AI_BEC"), "large_pct"
        ].iloc[0]
        self.assertTrue(pd.isna(unavailable))
        flagged = rows.loc[
            rows.indicator_code.eq("E_AI_BEC") & rows.size_emp.eq("GE250")
        ].iloc[0]
        self.assertTrue(pd.isna(flagged.percentage))
        self.assertEqual(flagged.observation_status, "u")

    def test_other_denominator_is_excluded(self):
        source = load("barrier")
        fake = source.loc[
            source.country_code.eq("DK") & source.year.eq(2025)
            & source.size_emp.eq("10-49") & source.indicator_code.eq("E_AI_BLE")
        ].iloc[[0]].copy()
        fake["unit"] = "PC_ENT"
        fake["percentage"] = 99.99
        augmented = pd.concat([source, fake], ignore_index=True)
        comparison, _ = size_barrier_comparison(augmented, "DK", 2025)
        row = comparison.loc[comparison.indicator_code.eq("E_AI_BLE")].iloc[0]
        self.assertEqual(row.small_pct, 82.44)
        self.assertEqual(set(barriers(augmented, size=None).unit), {CONSIDERED})

    def test_barrier_charts_do_not_animate_filter_redraws(self):
        script = Path(__file__).resolve().parents[1] / "pages" / "5_Adoption_Barriers.py"
        page = AppTest.from_file(str(script), default_timeout=30).run()
        self.assertFalse(page.exception)
        specs = [json.loads(chart.proto.spec) for chart in page.get("plotly_chart")]
        self.assertEqual(len(specs), 3)
        self.assertTrue(all(spec["layout"]["transition"]["duration"] == 0 for spec in specs))


if __name__ == "__main__":
    unittest.main()
