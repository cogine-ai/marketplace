"""RSC guidance must retain branch-specific fixes and the affected package scope."""

import csv
import unittest
from pathlib import Path

REACT_CSV = Path(__file__).resolve().parents[2] / "data/stacks/react.csv"


class TestReactSecurityGuidance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with REACT_CSV.open(encoding="utf-8", newline="") as handle:
            cls.rows = list(csv.DictReader(handle))
        cls.security = next(row for row in cls.rows if row["No"] == "60")

    def test_fixed_versions_cover_all_three_supported_release_lines(self):
        advice = " ".join(self.security.values())
        for floor in ("19.0.4", "19.1.5", "19.2.4"):
            self.assertIn(floor, advice)
        self.assertNotIn("19.2.1+", advice)
        self.assertIn("2025/12/11", self.security["Docs URL"])

    def test_scope_names_rsc_packages_and_framework_upgrade(self):
        advice = " ".join(self.security.values()).casefold()
        for package in ("react-server-dom-webpack", "react-server-dom-parcel", "react-server-dom-turbopack"):
            self.assertIn(package, advice)
        self.assertIn("client-only apps are not affected", advice)
        self.assertIn("framework", self.security["Do"].casefold())
        self.assertIn("bundled", self.security["Do"].casefold())

    def test_upstream_actions_increment_is_retained(self):
        self.assertEqual(66, len(self.rows))
        self.assertEqual(list(range(1, 67)), [int(row["No"]) for row in self.rows])
        expected = (
            "Use useActionState for Action state",
            "Call useFormStatus from a form child",
            "Use use() with stable promises or context",
            "Call useOptimistic updates inside an Action",
            "Use form actions for Action-based submissions",
        )
        self.assertEqual(list(expected), [row["Guideline"] for row in self.rows[61:]])


if __name__ == "__main__":
    unittest.main()
