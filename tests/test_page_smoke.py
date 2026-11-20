"""Smoke-test every user-facing page and the policymaker filter workflows."""
from pathlib import Path
import json
import unittest

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "pages/1_Overview.py",
    "pages/2_Country_Divide.py",
    "pages/3_Company_Size.py",
    "pages/4_Industry_Divide.py",
    "pages/5_Adoption_Barriers.py",
    "pages/6_Conclusion_and_Sources.py",
]


class PageSmokeTests(unittest.TestCase):
    def test_member_page_headers_show_assigned_full_names(self):
        assignments = {
            PAGES[1]: "Mehul Joshi",
            PAGES[2]: "Yixin Huang",
            PAGES[3]: "Ashwinlingesh Sangeetha Ravichand",
            PAGES[4]: "Le Hung Thanh",
        }
        for page_path, name in assignments.items():
            with self.subTest(page=page_path):
                app = AppTest.from_file(str(ROOT / page_path), default_timeout=60).run()
                self.assertFalse(app.exception)
                hero = next(item.value for item in app.markdown if 'class="page-hero' in item.value)
                self.assertIn(name, hero)
                self.assertNotIn("Member ", hero)

    def test_all_six_pages_render_without_streamlit_exceptions(self):
        for page_path in PAGES:
            with self.subTest(page=page_path):
                app = AppTest.from_file(str(ROOT / page_path), default_timeout=45).run()
                self.assertFalse(app.exception, "; ".join(e.message for e in app.exception))
                visible_copy = " ".join(item.value for item in app.markdown)
                self.assertIn("Source files retrieved", visible_copy)
                self.assertIn("21 October 2026", visible_copy)
                self.assertIn("ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai", visible_copy)

    def test_policymaker_filter_workflows_and_barrier_default(self):
        overview = AppTest.from_file(str(ROOT / PAGES[0]), default_timeout=45).run()
        self.assertFalse(overview.exception)
        overview_spec = json.loads(overview.get("plotly_chart")[0].proto.spec)
        self.assertEqual(overview_spec["layout"]["xaxis"]["tickvals"], [2021, 2023, 2024, 2025])

        country = AppTest.from_file(str(ROOT / PAGES[1]), default_timeout=45).run()
        self.assertEqual(len(country.get("plotly_chart")), 2)
        country.selectbox[0].select(2024).run()
        self.assertFalse(country.exception)
        self.assertEqual(len(country.get("plotly_chart")), 2)
        country.selectbox(key="country_trend").select("SE").run()
        self.assertFalse(country.exception)
        self.assertIn("Sweden", " ".join(item.value for item in country.markdown))
        country_line = json.loads(country.get("plotly_chart")[1].proto.spec)
        self.assertEqual(country_line["layout"]["xaxis"]["tickvals"], [2021, 2023, 2024, 2025])

        company_size = AppTest.from_file(str(ROOT / PAGES[2]), default_timeout=45).run()
        self.assertEqual(len(company_size.get("plotly_chart")), 2)
        initial_gap = company_size.metric[0].value
        company_size.selectbox(key="size_country").select("DK").run()
        self.assertFalse(company_size.exception)
        self.assertNotEqual(company_size.metric[0].value, initial_gap)

        barriers = AppTest.from_file(str(ROOT / PAGES[4]), default_timeout=60).run()
        self.assertFalse(barriers.exception)
        self.assertEqual(barriers.selectbox(key="barrier_main_size").value, "GE10")
        self.assertEqual(len(barriers.get("plotly_chart")), 3)

        industry = AppTest.from_file(str(ROOT / PAGES[3]), default_timeout=45).run()
        self.assertFalse(industry.exception)
        industry.button(key="industry_clear_all").click().run()
        self.assertFalse(industry.exception)
        self.assertIn("Select at least one sector to display the heatmap.",
                      " ".join(item.value for item in industry.info))

        barriers.selectbox(key="barrier_year").select(2024).run()
        self.assertFalse(barriers.exception)
        self.assertEqual(len(barriers.get("plotly_chart")), 3)


if __name__ == "__main__":
    unittest.main()
