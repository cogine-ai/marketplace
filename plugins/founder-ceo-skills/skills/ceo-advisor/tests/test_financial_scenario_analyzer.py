import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from financial_scenario_analyzer import FinancialScenarioAnalyzer


class FinancialScenarioAnalyzerTest(unittest.TestCase):
    def setUp(self):
        self.analyzer = FinancialScenarioAnalyzer()
        self.base_case = {
            "revenue": 100.0,
            "operating_expenses": 40.0,
            "valuation": 1000.0,
        }

    def project_revenue(self, growth_model):
        scenario = {
            "name": growth_model,
            "growth_model": growth_model,
            "growth_rate": 0.10,
            "opex_growth": 0.20,
        }
        return self.analyzer._analyze_scenario(
            self.base_case,
            scenario,
        )["projections"]

    def test_growth_is_measured_from_the_scenario_baseline(self):
        exponential = self.project_revenue("exponential")
        linear = self.project_revenue("linear")

        self.assertEqual(
            [round(year["revenue"], 2) for year in exponential],
            [110.0, 121.0, 133.1],
        )
        self.assertEqual(
            [round(year["revenue"], 2) for year in linear],
            [110.0, 120.0, 130.0],
        )
        self.assertAlmostEqual(exponential[1]["operating_expenses"], 57.6)


if __name__ == "__main__":
    unittest.main()
