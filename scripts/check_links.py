#!/usr/bin/env python3
"""Internal link checker for the Drone Integration Handbook.

The directory tree IS the URL tree (see CLAUDE.md), so a renamed/moved file
silently breaks every relative link pointing at it. This script catches that
class of breakage at PR time.

What it checks:
  - Relative Markdown links/images that resolve to a file or directory in the
    repo, e.g. `[x](../firmware/uart-layout.md)`, `![](assets/diagram.svg)`,
    `[x](../../platforms/tactical)` (directory links are valid — they map to a
    section URL at build time).

What it intentionally skips (not a rename-risk, or resolved elsewhere):
  - External links (http/https/mailto/tel) and protocol-relative `//...`.
  - Root-absolute clean paths (`/compliance/`, `/patterns/`, ...) — these are
    served by `_redirects`, not by a source file.
  - Pure in-page anchors (`#section`).

Exit code is non-zero if any broken internal link is found.
"""

from __future__ import annotations

import glob
import os
import re
import sys

# [text](target) and ![alt](target); target stops at whitespace or ')'.
LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*([^)\s]+)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "//", "#", "/")


def iter_markdown(root: str):
    for path in glob.glob(os.path.join(root, "**", "*.md"), recursive=True):
        if "/.git/" in path:
            continue
        yield path


def check(root: str = ".") -> int:
    broken: list[tuple[str, str]] = []
    checked = 0
    for md in iter_markdown(root):
        base = os.path.dirname(md)
        with open(md, encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        for match in LINK_RE.finditer(text):
            raw = match.group(1).strip()
            if raw.startswith(SKIP_PREFIXES):
                continue
            target = raw.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue  # was a pure anchor/query
            checked += 1
            resolved = os.path.normpath(os.path.join(base, target))
            if not os.path.exists(resolved):
                broken.append((md, raw))

    print(f"Checked {checked} internal relative links across the handbook.")
    if broken:
        print(f"\nBROKEN ({len(broken)}):", file=sys.stderr)
        for md, raw in broken:
            print(f"  {md}  ->  {raw}", file=sys.stderr)
        print(
            "\nFix the link or restore the target. The directory tree is the "
            "URL tree — a moved file breaks every relative link to it.",
            file=sys.stderr,
        )
        return 1
    print("All internal links resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(check(os.environ.get("HANDBOOK_ROOT", ".")))
