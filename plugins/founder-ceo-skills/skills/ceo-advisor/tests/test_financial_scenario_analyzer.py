import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from financial_scenario_analyzer import (
    FinancialScenarioAnalyzer,
    analyze_financial_scenarios,
)


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

    def test_irr_uses_cash_flow_timing(self):
        irr = self.analyzer._calculate_irr([0.0, 0.0, 133.1], 100.0)

        self.assertAlmostEqual(irr, 0.10, places=7)
        self.assertIsNone(self.analyzer._calculate_irr([10.0], 0))
        self.assertIsNone(self.analyzer._calculate_irr([-10.0], 100.0))

    def test_npv_includes_the_initial_investment(self):
        npv = self.analyzer._calculate_npv(
            [0.0, 0.0, 133.1],
            discount_rate=0.10,
            initial_investment=100.0,
        )

        self.assertAlmostEqual(npv, 0.0, places=7)

    def test_report_marks_irr_unavailable_without_an_investment(self):
        report = analyze_financial_scenarios(
            self.base_case,
            [{"name": "Base", "growth_rate": 0.10}],
        )

        self.assertIn("IRR: N/A", report)


if __name__ == "__main__":
    unittest.main()
