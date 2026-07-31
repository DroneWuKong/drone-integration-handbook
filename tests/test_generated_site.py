from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_generated_site import validate_site


class GeneratedSiteValidationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        (self.root / "assets").mkdir()
        (self.root / "assets" / "site.css").write_text("body{}", encoding="utf-8")
        (self.root / "assets" / "site.js").write_text("'use strict';", encoding="utf-8")

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_index(self, document: str) -> Path:
        index = self.root / "index.html"
        index.write_text(document, encoding="utf-8")
        return index

    def test_valid_generated_site_passes(self) -> None:
        index = self.write_index(
            """<!doctype html>
<html>
<head><link rel="stylesheet" href="assets/site.css"></head>
<body>
  <div id="platforms"></div>
  <div id="components"></div>
  <article class="chapter" id="ch1"></article>
  <article class="chapter" id="ch38"></article>
  <article class="chapter" id="ch47"></article>
  <a href="#ch38">field guide</a>
  <script id="handbookMetadata" type="application/json">[
    {"anchor":"ch1"},{"anchor":"ch38"},{"anchor":"ch47"}
  ]</script>
  <script src="assets/site.js"></script>
</body>
</html>"""
        )
        self.assertEqual(validate_site(index), [])

    def test_invalid_generated_site_reports_structural_failures(self) -> None:
        index = self.write_index(
            """<!doctype html>
<html>
<head><link rel="stylesheet" href="assets/missing.css"></head>
<body>
  <article class="chapter" id="ch1"></article>
  <div id="ch1"></div>
  <a href="#missing-target">broken anchor</a>
  <a href="../field/orphan.md">orphan source</a>
  <script id="handbookMetadata" type="application/json">not-json</script>
</body>
</html>"""
        )
        errors = "\n".join(validate_site(index))
        self.assertIn("duplicate element IDs", errors)
        self.assertIn("required published IDs are missing", errors)
        self.assertIn("in-page links target missing IDs", errors)
        self.assertIn("source Markdown links leaked", errors)
        self.assertIn("referenced UI assets are missing", errors)
        self.assertIn("search metadata is invalid JSON", errors)


if __name__ == "__main__":
    unittest.main()
