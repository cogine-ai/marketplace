"""Project titles must stay inside the rendered terminal box without truncation."""

import re
import sys
import unicodedata
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from design_system import BOX_WIDTH, DesignSystemGenerator, format_ascii_box


def terminal_columns(text):
    """Independent Unicode column estimate; ambiguous characters use one column."""
    text = re.sub(r"\x1b\[[0-9;]*m", "", text)
    return sum(
        0 if unicodedata.combining(char) or unicodedata.category(char) == "Cf"
        else 2 if unicodedata.east_asian_width(char) in ("W", "F") else 1
        for char in text
    )


class TestAsciiBoxWidth(unittest.TestCase):
    def assert_title_fits_without_truncation(self, project):
        result = DesignSystemGenerator().generate("beauty spa wellness", project)
        lines = format_ascii_box(result).splitlines()
        header_end = next(index for index, line in enumerate(lines) if line.startswith("╚"))
        title_lines = lines[1:header_end]
        self.assertTrue(title_lines)
        for line in lines:
            with self.subTest(line=line):
                self.assertEqual(BOX_WIDTH + 1, terminal_columns(line))
        title = "".join(line[1:-1].strip() for line in title_lines)
        self.assertEqual(
            "".join(f"TARGET: {project} - RECOMMENDED DESIGN SYSTEM".split()),
            "".join(title.split()),
        )
        return title_lines

    def test_long_ascii_title_preserves_every_character(self):
        self.assertGreater(len(self.assert_title_fits_without_truncation("Product" * 35)), 1)

    def test_long_cjk_title_preserves_every_character(self):
        self.assertGreater(
            len(self.assert_title_fits_without_truncation("產品設計測試" + "中文名稱" * 20)), 1
        )

    def test_mixed_cjk_and_combining_marks_title(self):
        self.assert_title_fits_without_truncation("產品Cafe\u0301" * 25)

    def test_short_ascii_title_keeps_one_line(self):
        self.assertEqual(1, len(self.assert_title_fits_without_truncation("My Project")))


if __name__ == "__main__":
    unittest.main()
