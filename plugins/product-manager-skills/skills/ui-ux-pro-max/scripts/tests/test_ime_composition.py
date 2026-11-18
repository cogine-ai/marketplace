"""Retrieve IME guidance and exercise the actual CSV JavaScript example."""

import csv
from pathlib import Path
import shutil
import subprocess
import sys
import unittest

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))
from core import search  # noqa: E402


class TestImeGuidance(unittest.TestCase):
    def test_quick_references_include_the_rule(self):
        quick_reference = SCRIPTS.parent / "references/quick-reference.md"
        self.assertIn("`ime-composition-enter`", quick_reference.read_text(encoding="utf-8"))

    def test_composition_queries_retrieve_the_rule_first(self):
        for query in ("IME composition Enter", "Korean input Enter submit",
                      "Japanese Chinese composition", "한글 IME Enter"):
            with self.subTest(query=query):
                result = search(query, domain="ux", max_results=3)
                self.assertEqual("IME Composition Enter", result["results"][0]["Issue"])

    def test_csv_example_preserves_ime_and_submission_paths(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node.js is required to execute the JavaScript example")
        with (SCRIPTS.parent / "data/ux-guidelines.csv").open(
                encoding="utf-8", newline="") as handle:
            row, = [row for row in csv.DictReader(handle)
                    if row["Issue"] == "IME Composition Enter"]
        runner = r"""
const assert = require('node:assert/strict');
const source = require('node:fs').readFileSync(0, 'utf8');
let handler;
let sent = 0;
const textarea = {
  addEventListener(type, callback) {
    assert.equal(type, 'keydown');
    handler = callback;
  }
};
const form = { requestSubmit() { sent++; } };
require('node:vm').runInNewContext(source, { textarea, form });

function key(overrides, expectedSent, expectedPrevented) {
  let prevented = false;
  const event = { key: 'Enter', shiftKey: false, ctrlKey: false, metaKey: false,
    altKey: false, repeat: false, isComposing: false, keyCode: 13,
    preventDefault() { prevented = true; }, ...overrides };
  handler(event);
  assert.equal(sent, expectedSent);
  assert.equal(prevented, expectedPrevented);
}
key({isComposing: true}, 0, false);
key({isComposing: false, keyCode: 229}, 0, false);
key({key: 'Process', keyCode: 229}, 0, false);
key({key: 'a', keyCode: 65}, 0, false);
key({shiftKey: true}, 0, false);
key({ctrlKey: true}, 0, false);
key({metaKey: true}, 0, false);
key({altKey: true}, 0, false);
key({}, 1, true); // A separate Enter after confirmation submits once.
key({repeat: true}, 1, true);
"""
        subprocess.run(
            [node, "-e", runner], input=row["Code Example Good"],
            text=True, check=True,
        )


if __name__ == "__main__":
    unittest.main()
