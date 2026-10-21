"""Essential source-selection and integrity checks for the supplied ZIP."""
import unittest
from src.data import (load, adoption, barriers, comparison_sectors, record,
                      EU, OVERALL, SECTORS, CONSIDERED)


class DataTests(unittest.TestCase):
    def test_four_files_and_missing_values(self):
        expected = {"country": 112, "size": 896, "industry": 5600, "barrier": 28672}
        for name, count in expected.items():
            with self.subTest(name=name):
                frame = load(name)
                self.assertEqual(len(frame), count)
                self.assertEqual(set(frame.year.unique()), {2021, 2023, 2024, 2025})
                self.assertTrue(frame.percentage.dropna().between(0, 100).all())
        self.assertTrue(load("barrier").percentage.isna().any())

    def test_reference_values_and_distinct_sectors(self):
        countries = adoption(load("country"))
        self.assertEqual(record(countries, country_code=EU, year=2025).percentage, 19.95)
        self.assertEqual(record(countries, country_code="DK", year=2025).percentage, 42.03)
        self.assertEqual(record(countries, country_code="RO", year=2025).percentage, 5.21)
        size = adoption(load("size"), size=None)
        self.assertEqual(record(size, country_code=EU, year=2025, size_emp="GE250").percentage, 55.03)
        sectors = comparison_sectors(adoption(load("industry"), sector=None))
        self.assertEqual(set(sectors.nace_r2.unique()), SECTORS)
        self.assertNotIn(OVERALL, set(sectors.nace_r2))

    def test_barrier_denominator_and_gap(self):
        selected = barriers(load("barrier"))
        self.assertEqual(set(selected.unit.unique()), {CONSIDERED})
        self.assertEqual(set(selected.size_emp.unique()), {"GE10"})
        expertise = record(selected, country_code=EU, year=2025, indicator_code="E_AI_BLE")
        self.assertEqual(expertise.percentage, 70.31)
        sizes = adoption(load("size"), size=None)
        large = record(sizes, country_code=EU, year=2025, size_emp="GE250")
        small = record(sizes, country_code=EU, year=2025, size_emp="10-49")
        self.assertGreater(large.percentage - small.percentage, 0)

    def test_unique_keys_and_provenance(self):
        keys = ["country_code", "year", "freq", "size_emp", "nace_r2", "indicator_code", "unit"]
        for name in ("country", "size", "industry", "barrier"):
            with self.subTest(name=name):
                frame = load(name)
                self.assertFalse(frame.duplicated(keys).any())
                self.assertTrue(frame.source_url.str.startswith("https://ec.europa.eu/eurostat/").all())
                self.assertTrue(frame.raw_sha256.str.fullmatch(r"[0-9a-f]{64}").all())
                self.assertTrue(frame.source_observation_index.notna().all())


if __name__ == "__main__":
    unittest.main()
