#!/usr/bin/env python3
"""Validate the generated single-page handbook before deployment.

The source-level link checker proves that Markdown targets exist in the
repository. This check covers the second half of the contract: every published
in-page link must resolve in ``site/index.html``, no source Markdown link may
leak into the static output, IDs must be unique, and required UI assets must be
present.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


_TEMPLATE_TOKEN_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
_REQUIRED_IDS = {"ch1", "ch38", "ch47", "platforms", "components"}


class _SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.chapter_ids: list[str] = []
        self.fragment_links: list[str] = []
        self.markdown_links: list[str] = []
        self.asset_paths: list[str] = []
        self.metadata_parts: list[str] = []
        self._inside_metadata = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name: value or "" for name, value in attrs}
        element_id = attributes.get("id", "").strip()
        if element_id:
            self.ids.append(element_id)

        classes = set(attributes.get("class", "").split())
        if tag == "article" and "chapter" in classes and element_id:
            self.chapter_ids.append(element_id)

        if tag == "script" and element_id == "handbookMetadata":
            self._inside_metadata = True

        href = attributes.get("href", "").strip()
        if href:
            self._record_href(href)
            if tag == "link" and "stylesheet" in attributes.get("rel", "").split():
                self._record_asset(href)

        source = attributes.get("src", "").strip()
        if source and tag in {"script", "img", "source", "video", "audio"}:
            self._record_asset(source)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._inside_metadata:
            self._inside_metadata = False

    def handle_data(self, data: str) -> None:
        if self._inside_metadata:
            self.metadata_parts.append(data)

    def _record_href(self, href: str) -> None:
        if href.startswith("#"):
            fragment = unquote(href[1:]).strip()
            if fragment:
                self.fragment_links.append(fragment)
            return

        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc or href.startswith("//"):
            return
        if parsed.path.lower().endswith(".md"):
            self.markdown_links.append(href)

    def _record_asset(self, value: str) -> None:
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc or value.startswith(("//", "data:")):
            return
        path = unquote(parsed.path).strip()
        if path:
            self.asset_paths.append(path)


def _resolve_asset(site_root: Path, asset_path: str) -> Path | None:
    relative = asset_path.lstrip("/")
    candidate = (site_root / relative).resolve()
    try:
        candidate.relative_to(site_root.resolve())
    except ValueError:
        return None
    return candidate


def validate_site(index_path: Path) -> list[str]:
    """Return a list of validation errors for a generated handbook index."""

    errors: list[str] = []
    if not index_path.is_file():
        return [f"generated index does not exist: {index_path}"]

    document = index_path.read_text(encoding="utf-8")
    parser = _SiteParser()
    parser.feed(document)

    unresolved_tokens = sorted(set(_TEMPLATE_TOKEN_RE.findall(document)))
    if unresolved_tokens:
        errors.append(f"unresolved template tokens: {', '.join(unresolved_tokens)}")

    duplicate_ids = sorted(
        element_id for element_id, count in Counter(parser.ids).items() if count > 1
    )
    if duplicate_ids:
        errors.append(f"duplicate element IDs: {', '.join(duplicate_ids)}")

    id_set = set(parser.ids)
    missing_required = sorted(_REQUIRED_IDS - id_set)
    if missing_required:
        errors.append(f"required published IDs are missing: {', '.join(missing_required)}")

    missing_fragments = sorted(set(parser.fragment_links) - id_set)
    if missing_fragments:
        errors.append(
            "in-page links target missing IDs: " + ", ".join(missing_fragments[:40])
        )

    if parser.markdown_links:
        errors.append(
            "source Markdown links leaked into generated HTML: "
            + ", ".join(sorted(set(parser.markdown_links))[:40])
        )

    site_root = index_path.parent
    missing_assets: list[str] = []
    escaping_assets: list[str] = []
    for asset_path in sorted(set(parser.asset_paths)):
        resolved = _resolve_asset(site_root, asset_path)
        if resolved is None:
            escaping_assets.append(asset_path)
        elif not resolved.is_file():
            missing_assets.append(asset_path)
    if escaping_assets:
        errors.append("asset paths escape the site directory: " + ", ".join(escaping_assets))
    if missing_assets:
        errors.append("referenced UI assets are missing: " + ", ".join(missing_assets))

    metadata_text = "".join(parser.metadata_parts).strip()
    if not metadata_text:
        errors.append("handbook search metadata is missing or empty")
    else:
        try:
            metadata = json.loads(metadata_text)
        except json.JSONDecodeError as exc:
            errors.append(f"handbook search metadata is invalid JSON: {exc}")
        else:
            if not isinstance(metadata, list):
                errors.append("handbook search metadata must be a JSON list")
            else:
                metadata_anchors = [
                    item.get("anchor")
                    for item in metadata
                    if isinstance(item, dict) and isinstance(item.get("anchor"), str)
                ]
                duplicate_metadata = sorted(
                    anchor
                    for anchor, count in Counter(metadata_anchors).items()
                    if count > 1
                )
                if duplicate_metadata:
                    errors.append(
                        "duplicate search metadata anchors: "
                        + ", ".join(duplicate_metadata)
                    )
                missing_metadata_targets = sorted(set(metadata_anchors) - id_set)
                if missing_metadata_targets:
                    errors.append(
                        "search metadata targets missing IDs: "
                        + ", ".join(missing_metadata_targets[:40])
                    )
                if len(metadata_anchors) != len(parser.chapter_ids):
                    errors.append(
                        "search metadata/article count mismatch: "
                        f"{len(metadata_anchors)} metadata entries vs "
                        f"{len(parser.chapter_ids)} article elements"
                    )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "index",
        nargs="?",
        default="site/index.html",
        type=Path,
        help="generated handbook index (default: site/index.html)",
    )
    args = parser.parse_args(argv)

    errors = validate_site(args.index)
    if errors:
        print(f"Generated site validation failed ({len(errors)} issue(s)):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"Generated site validation passed: {args.index}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
