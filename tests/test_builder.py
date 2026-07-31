from __future__ import annotations

import html
import re
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from handbook_builder.config import CHAPTERS
from handbook_builder.site import (
    build_site,
    discover_entries,
    rewrite_internal_markdown_links,
)


class _FakeMarkdown:
    """Small renderer used only to test builder orchestration without dependencies."""

    _link = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    @classmethod
    def markdown(cls, source: str, **_: object) -> str:
        rendered: list[str] = []
        paragraph: list[str] = []

        def flush() -> None:
            if not paragraph:
                return
            text = " ".join(paragraph)
            text = cls._link.sub(
                lambda match: f'<a href="{html.escape(match.group(2))}">{html.escape(match.group(1))}</a>',
                text,
            )
            rendered.append(f"<p>{text}</p>")
            paragraph.clear()

        for raw_line in source.splitlines():
            line = raw_line.strip()
            if not line:
                flush()
            elif line.startswith("### "):
                flush()
                rendered.append(f"<h3>{html.escape(line[4:])}</h3>")
            elif line.startswith("## "):
                flush()
                rendered.append(f"<h2>{html.escape(line[3:])}</h2>")
            elif line.startswith("# "):
                flush()
                rendered.append(f"<h1>{html.escape(line[2:])}</h1>")
            else:
                paragraph.append(html.escape(line))
        flush()
        return "\n".join(rendered)


class BuilderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        project_root = Path(__file__).resolve().parents[1]
        (self.root / "templates").mkdir()
        (self.root / "assets").mkdir()
        shutil.copy2(project_root / "templates" / "handbook.html", self.root / "templates" / "handbook.html")
        shutil.copy2(project_root / "assets" / "handbook.css", self.root / "assets" / "handbook.css")
        shutil.copy2(project_root / "assets" / "handbook.js", self.root / "assets" / "handbook.js")

        for chapter in CHAPTERS:
            path = self.root / chapter.source
            path.parent.mkdir(parents=True, exist_ok=True)
            body = f"# {chapter.title}\n\nReference body for chapter {chapter.number}."
            if chapter.number == 1:
                body += "\n\nSee [frequency bands](frequency-bands.md)."
            path.write_text(body, encoding="utf-8")

        platform = self.root / "platforms" / "cots" / "test-platform.md"
        platform.parent.mkdir(parents=True)
        platform.write_text("# Test Platform\n\nPlatform body.", encoding="utf-8")

        component = self.root / "components" / "flight-controller-test.md"
        component.parent.mkdir(parents=True)
        component.write_text("# Test Flight Controller\n\nComponent body.", encoding="utf-8")

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_internal_markdown_links_become_stable_anchors(self) -> None:
        rewritten = rewrite_internal_markdown_links(
            "Read [the next chapter](frequency-bands.md) and [outside](https://example.com).",
            "fundamentals/five-link-types.md",
            {"fundamentals/frequency-bands.md": "ch2"},
            {"frequency-bands.md": "ch2"},
        )
        self.assertIn("[the next chapter](#ch2)", rewritten)
        self.assertIn("[outside](https://example.com)", rewritten)

    def test_discovery_uses_reader_facing_part_order_and_stable_ids(self) -> None:
        entries = discover_entries(self.root)
        chapters = [entry for entry in entries if entry.kind == "chapter"]
        self.assertEqual([entry.number for entry in chapters[:6]], [1, 2, 3, 4, 31, 37])
        self.assertEqual(next(entry.anchor for entry in entries if entry.kind == "platform"), "p101")
        self.assertEqual(next(entry.anchor for entry in entries if entry.kind == "component"), "c600")
        self.assertEqual(next(entry.group for entry in entries if entry.kind == "component"), "Flight Controllers & Firmware")

    def test_full_build_writes_external_ui_assets_and_navigation(self) -> None:
        output = self.root / "site"
        with patch("handbook_builder.site._markdown_module", return_value=_FakeMarkdown):
            index_path = build_site(self.root, output)

        document = index_path.read_text(encoding="utf-8")
        self.assertIn('href="assets/handbook.css"', document)
        self.assertIn('src="assets/handbook.js"', document)
        self.assertIn('id="ch37"', document)
        self.assertIn('id="platforms"', document)
        self.assertIn('data-nav-target="ch12"', document)
        self.assertIn('href="#ch2"', document)
        self.assertTrue((output / "assets" / "handbook.css").is_file())
        self.assertTrue((output / "assets" / "handbook.js").is_file())


if __name__ == "__main__":
    unittest.main()
