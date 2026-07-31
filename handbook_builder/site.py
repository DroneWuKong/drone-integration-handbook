"""Static-site builder for the Drone Integration Handbook.

The builder intentionally keeps content, presentation, and browser behavior in
separate files:

* ``config.py`` owns stable chapter IDs and navigation taxonomy.
* this module discovers Markdown, renders it, and assembles the page.
* ``templates/handbook.html`` owns document structure.
* ``assets/handbook.css`` and ``assets/handbook.js`` own the UI.
"""

from __future__ import annotations

import html
import importlib
import json
import os
import posixpath
import re
import shutil
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence
from urllib.parse import unquote, urlsplit

from .config import (
    CHAPTERS,
    COMPONENT_GROUPS,
    PARTS,
    PLATFORM_CATEGORIES,
    REPOSITORY_URL,
    SITE_DESCRIPTION,
    SITE_TITLE,
    SITE_URL,
    ChapterSpec,
)


_STATIC_ASSET_SUFFIXES = {
    ".css",
    ".js",
    ".json",
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".ico",
}

_SPECIAL_MARKDOWN_ANCHORS = {
    "platforms/README.md": "platforms",
}

_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\n]+)\)")
_HEADING_RE = re.compile(r"<h([23])([^>]*)>(.*?)</h\1>", re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
_ID_ATTR_RE = re.compile(r"\s+id=(?:\"[^\"]*\"|'[^']*')", re.IGNORECASE)
_ID_VALUE_RE = re.compile(
    r"\s+id=(?P<quote>[\"'])(?P<value>.*?)(?P=quote)",
    re.IGNORECASE | re.DOTALL,
)
_HREF_FRAGMENT_RE = re.compile(
    r"href=(?P<quote>[\"'])#(?P<fragment>[^\"']+)(?P=quote)",
    re.IGNORECASE,
)


@dataclass(slots=True)
class ContentEntry:
    """One rendered navigation/search/content unit."""

    relative_path: str
    source_path: Path
    anchor: str
    title: str
    kind: str
    group: str
    order: int
    number: int | None = None
    group_key: str = ""
    html: str = ""
    plain_text: str = ""


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if text:
            self.parts.append(text)

    def result(self) -> str:
        return " ".join(self.parts)


def _extract_text(rendered_html: str) -> str:
    parser = _TextExtractor()
    parser.feed(rendered_html)
    return re.sub(r"\s+", " ", parser.result()).strip()


def _slugify(value: str) -> str:
    value = html.unescape(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "section"


def _decorate_headings(rendered_html: str, section_anchor: str) -> str:
    """Scope heading IDs and preserve links to headings inside the entry."""

    seen: dict[str, int] = {}
    fragment_map: dict[str, str] = {}

    def replace(match: re.Match[str]) -> str:
        level, attrs, body = match.groups()
        heading_text = _TAG_RE.sub("", body)
        base = f"{section_anchor}-{_slugify(heading_text)}"
        occurrence = seen.get(base, 0) + 1
        seen[base] = occurrence
        heading_id = base if occurrence == 1 else f"{base}-{occurrence}"

        old_id_match = _ID_VALUE_RE.search(attrs)
        if old_id_match:
            old_id = html.unescape(old_id_match.group("value"))
            fragment_map[old_id] = heading_id

        clean_attrs = _ID_ATTR_RE.sub("", attrs)
        return f'<h{level}{clean_attrs} id="{heading_id}">{body}</h{level}>'

    decorated = _HEADING_RE.sub(replace, rendered_html)

    if fragment_map:
        def rewrite_fragment(match: re.Match[str]) -> str:
            fragment = html.unescape(match.group("fragment"))
            target = fragment_map.get(fragment)
            if target is None:
                return match.group(0)
            quote = match.group("quote")
            return f"href={quote}#{target}{quote}"

        decorated = _HREF_FRAGMENT_RE.sub(rewrite_fragment, decorated)

    return decorated


def _read_first_h1(path: Path) -> str:
    fallback = path.stem.replace("-", " ").replace("_", " ").title()
    try:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                stripped = line.strip()
                if stripped.startswith("# "):
                    return stripped[2:].strip()
    except OSError:
        return fallback
    return fallback


def _discover_markdown(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(
        path
        for path in root.rglob("*.md")
        if path.name.lower() not in {"readme.md", "index.md"}
    )


def _chapter_part(spec: ChapterSpec) -> tuple[str, str]:
    for part in PARTS:
        if spec.number in part.chapter_numbers:
            return part.key, part.label
    raise ValueError(f"chapter {spec.number} is not assigned to a Part")


def _ordered_chapter_specs() -> list[ChapterSpec]:
    """Use the reader-facing Part order while preserving stable chapter IDs."""

    by_number = {chapter.number: chapter for chapter in CHAPTERS}
    ordered: list[ChapterSpec] = []
    seen: set[int] = set()
    for part in PARTS:
        for number in part.chapter_numbers:
            chapter = by_number.get(number)
            if chapter is None:
                raise ValueError(f"Part references unknown chapter number {number}")
            if number in seen:
                raise ValueError(f"chapter number {number} appears in multiple Parts")
            seen.add(number)
            ordered.append(chapter)
    unassigned = sorted(set(by_number) - seen)
    if unassigned:
        raise ValueError(f"chapter numbers are not assigned to a Part: {unassigned}")
    return ordered


def _component_group(filename_stem: str) -> tuple[str, str]:
    for index, group in enumerate(COMPONENT_GROUPS):
        if any(pattern in filename_stem for pattern in group.patterns):
            return f"component-{index}", group.label
    return "component-other", "Other"


def discover_entries(base_dir: Path) -> list[ContentEntry]:
    """Discover all content and return it in reader-facing order."""

    entries: list[ContentEntry] = []
    missing: list[str] = []

    for order, spec in enumerate(_ordered_chapter_specs()):
        source = base_dir / spec.source
        if not source.is_file():
            missing.append(spec.source)
            continue
        part_key, part_label = _chapter_part(spec)
        entries.append(
            ContentEntry(
                relative_path=spec.source,
                source_path=source,
                anchor=spec.anchor,
                title=spec.title,
                kind="chapter",
                group=part_label,
                group_key=part_key,
                order=order,
                number=spec.number,
            )
        )

    if missing:
        formatted = "\n".join(f"  - {item}" for item in missing)
        raise FileNotFoundError(
            "The chapter registry references missing Markdown files:\n" + formatted
        )

    next_order = len(entries)
    platform_number = 101
    for category in PLATFORM_CATEGORIES:
        for source in _discover_markdown(base_dir / "platforms" / category.key):
            relative = source.relative_to(base_dir).as_posix()
            entries.append(
                ContentEntry(
                    relative_path=relative,
                    source_path=source,
                    anchor=f"p{platform_number}",
                    title=_read_first_h1(source),
                    kind="platform",
                    group=category.label,
                    group_key=category.key,
                    order=next_order,
                    number=platform_number,
                )
            )
            platform_number += 1
            next_order += 1

    component_number = 600
    for source in _discover_markdown(base_dir / "components"):
        relative = source.relative_to(base_dir).as_posix()
        group_key, group_label = _component_group(source.stem)
        entries.append(
            ContentEntry(
                relative_path=relative,
                source_path=source,
                anchor=f"c{component_number}",
                title=_read_first_h1(source),
                kind="component",
                group=group_label,
                group_key=group_key,
                order=next_order,
                number=component_number,
            )
        )
        component_number += 1
        next_order += 1

    return entries


def _path_anchor_maps(entries: Sequence[ContentEntry]) -> tuple[dict[str, str], dict[str, str]]:
    direct: dict[str, str] = dict(_SPECIAL_MARKDOWN_ANCHORS)
    basenames: dict[str, list[str]] = {}
    for entry in entries:
        normalized = posixpath.normpath(entry.relative_path)
        direct[normalized] = entry.anchor
        basenames.setdefault(PurePosixPath(normalized).name, []).append(entry.anchor)
    unique_basenames = {
        name: anchors[0] for name, anchors in basenames.items() if len(anchors) == 1
    }
    return direct, unique_basenames


def _split_markdown_destination(destination: str) -> tuple[str, str]:
    """Split ``url optional-title`` while preserving the optional title suffix."""

    stripped = destination.strip()
    if stripped.startswith("<"):
        close = stripped.find(">")
        if close != -1:
            return stripped[1:close], stripped[close + 1 :]
    match = re.match(r"(\S+)(.*)", stripped, re.DOTALL)
    if not match:
        return stripped, ""
    return match.group(1), match.group(2)


def rewrite_internal_markdown_links(
    markdown_text: str,
    current_path: str,
    direct_anchors: dict[str, str],
    basename_anchors: dict[str, str],
) -> str:
    """Convert links to handbook Markdown files into stable single-page anchors."""

    current_parent = PurePosixPath(current_path).parent

    def replace(match: re.Match[str]) -> str:
        label, destination = match.groups()
        raw_url, title_suffix = _split_markdown_destination(destination)
        parsed = urlsplit(unquote(raw_url))
        target_path = parsed.path
        if not target_path.lower().endswith(".md"):
            return match.group(0)

        candidates: list[str] = []
        if target_path.startswith("/"):
            candidates.append(posixpath.normpath(target_path.lstrip("/")))
        else:
            candidates.append(
                posixpath.normpath((current_parent / target_path).as_posix())
            )
            candidates.append(posixpath.normpath(target_path.lstrip("./")))

        anchor = next(
            (direct_anchors[candidate] for candidate in candidates if candidate in direct_anchors),
            None,
        )
        if anchor is None:
            anchor = basename_anchors.get(PurePosixPath(target_path).name)
        if anchor is None:
            return match.group(0)

        suffix = title_suffix if title_suffix else ""
        return f"[{label}](#{anchor}{suffix})"

    return _LINK_RE.sub(replace, markdown_text)


def rewrite_legacy_domains(rendered_html: str) -> str:
    """Normalize retired ecosystem domains at build time."""

    replacements = (
        ("https://nvmillbuilditmyself.com/patterns/", "https://uas-patterns.com/patterns/"),
        ("https://nvmillbuilditmyself.com/pro/", "https://uas-patterns.com/patterns/"),
        ("https://nvmillfindoutmyself.com/patterns/", "https://uas-patterns.com/patterns/"),
        ("https://nvmillfindoutmyself.com/pro/", "https://uas-patterns.com/patterns/"),
        ("https://forgeprole.netlify.app/intel/", "https://uas-patterns.com/intel/"),
        ("https://forgeprole.netlify.app/patterns-home/", "https://uas-patterns.com/patterns-home/"),
        ("https://forgeprole.netlify.app/patterns/", "https://uas-patterns.com/patterns/"),
        ("https://www.nvmillbuilditmyself.com", "https://uas-forge.com"),
        ("https://nvmillbuilditmyself.com", "https://uas-forge.com"),
        ("https://www.nvmillfindoutmyself.com", "https://uas-patterns.com"),
        ("https://nvmillfindoutmyself.com", "https://uas-patterns.com"),
        ("https://www.nvmilldoitmyself.com", "https://uas-handbook.com"),
        ("https://nvmilldoitmyself.com", "https://uas-handbook.com"),
        ("https://www.uas-patterns.pro", "https://uas-patterns.com"),
        ("https://uas-patterns.pro", "https://uas-patterns.com"),
        ("https://www.illdoitmyself.com", "https://uas-handbook.com"),
        ("https://illdoitmyself.com", "https://uas-handbook.com"),
        ("https://www.uas-intel.com", "https://uas-patterns.com"),
        ("https://uas-intel.com", "https://uas-patterns.com"),
        ("https://www.forgeprole.netlify.app", "https://uas-forge.com"),
        ("https://forgeprole.netlify.app", "https://uas-forge.com"),
    )
    for old, new in replacements:
        rendered_html = rendered_html.replace(old, new)
    return rendered_html


def _markdown_module():
    try:
        return importlib.import_module("markdown")
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Python-Markdown is required. Run: pip install -r requirements.txt"
        ) from exc


def render_entries(entries: Sequence[ContentEntry]) -> None:
    """Render Markdown into HTML and populate text used by the browser search."""

    direct_anchors, basename_anchors = _path_anchor_maps(entries)
    markdown_module = _markdown_module()

    for entry in entries:
        source = entry.source_path.read_text(encoding="utf-8")
        source = rewrite_internal_markdown_links(
            source,
            entry.relative_path,
            direct_anchors,
            basename_anchors,
        )
        rendered = markdown_module.markdown(
            source,
            extensions=["tables", "fenced_code", "codehilite", "toc", "sane_lists"],
            extension_configs={"codehilite": {"css_class": "codehilite"}},
        )
        rendered = rewrite_legacy_domains(rendered)
        rendered = _decorate_headings(rendered, entry.anchor)
        entry.html = rendered
        entry.plain_text = _extract_text(rendered)


def _nav_link(entry: ContentEntry) -> str:
    number = str(entry.number) if entry.kind == "chapter" else "•"
    return (
        f'<a class="rail-link" href="#{html.escape(entry.anchor)}" '
        f'data-nav-target="{html.escape(entry.anchor)}" '
        f'data-kind="{html.escape(entry.kind)}">'
        f'<span class="rail-number">{html.escape(number)}</span>'
        f'<span>{html.escape(entry.title)}</span>'
        "</a>"
    )


def _grouped(entries: Iterable[ContentEntry], attribute: str) -> dict[str, list[ContentEntry]]:
    grouped: dict[str, list[ContentEntry]] = {}
    for entry in entries:
        grouped.setdefault(getattr(entry, attribute), []).append(entry)
    return grouped


def render_navigation(entries: Sequence[ContentEntry], *, mobile: bool = False) -> str:
    """Render the shared desktop rail/mobile drawer navigation tree."""

    chapters = [entry for entry in entries if entry.kind == "chapter"]
    platforms = [entry for entry in entries if entry.kind == "platform"]
    components = [entry for entry in entries if entry.kind == "component"]
    chapter_groups = _grouped(chapters, "group_key")
    platform_groups = _grouped(platforms, "group_key")
    component_groups = _grouped(components, "group")

    open_attr = " open" if mobile else ""
    sections: list[str] = [
        '<div class="rail-shortcuts">',
        '<a href="#ch1"><span>Learn</span><small>Start with RF fundamentals</small></a>',
        '<a href="#ch12"><span>Diagnose</span><small>Open the failure tree</small></a>',
        '<a href="#platforms"><span>Compare</span><small>Browse platform references</small></a>',
        "</div>",
    ]

    for part_index, part in enumerate(PARTS):
        part_entries = chapter_groups.get(part.key, [])
        if not part_entries:
            continue
        should_open = " open" if part_index == 0 or mobile else ""
        sections.append(
            f'<details class="rail-group" data-group="{html.escape(part.key)}"{should_open}>'
            f'<summary><span>{html.escape(part.label)}</span>'
            f'<span class="rail-count">{len(part_entries)}</span></summary>'
        )
        sections.extend(_nav_link(entry) for entry in part_entries)
        sections.append("</details>")

    if platforms:
        sections.append(
            f'<details class="rail-group rail-reference" data-group="platforms"{open_attr}>'
            f'<summary><span>Platform References</span>'
            f'<span class="rail-count">{len(platforms)}</span></summary>'
        )
        for category in PLATFORM_CATEGORIES:
            group_entries = platform_groups.get(category.key, [])
            if not group_entries:
                continue
            sections.append(
                f'<details class="rail-subgroup"><summary>{html.escape(category.label)} '
                f'<span>{len(group_entries)}</span></summary>'
            )
            sections.extend(_nav_link(entry) for entry in group_entries)
            sections.append("</details>")
        sections.append("</details>")

    if components:
        sections.append(
            f'<details class="rail-group rail-reference" data-group="components"{open_attr}>'
            f'<summary><span>Component References</span>'
            f'<span class="rail-count">{len(components)}</span></summary>'
        )
        ordered_labels = [group.label for group in COMPONENT_GROUPS] + ["Other"]
        for label in ordered_labels:
            group_entries = component_groups.get(label, [])
            if not group_entries:
                continue
            sections.append(
                f'<details class="rail-subgroup"><summary>{html.escape(label)} '
                f'<span>{len(group_entries)}</span></summary>'
            )
            sections.extend(_nav_link(entry) for entry in group_entries)
            sections.append("</details>")
        sections.append("</details>")

    return "\n".join(sections)


def _entry_kicker(entry: ContentEntry) -> str:
    if entry.kind == "chapter":
        return f"Chapter {entry.number} · {entry.group}"
    if entry.kind == "platform":
        return f"Platform reference · {entry.group}"
    return f"Component reference · {entry.group}"


def _entry_footer(previous: ContentEntry | None, following: ContentEntry | None) -> str:
    links: list[str] = []
    if previous is not None:
        links.append(
            f'<a class="chapter-step previous" href="#{html.escape(previous.anchor)}">'
            '<span class="step-label">Previous</span>'
            f'<strong>{html.escape(previous.title)}</strong></a>'
        )
    else:
        links.append('<span class="chapter-step empty" aria-hidden="true"></span>')
    if following is not None:
        links.append(
            f'<a class="chapter-step next" href="#{html.escape(following.anchor)}">'
            '<span class="step-label">Next</span>'
            f'<strong>{html.escape(following.title)}</strong></a>'
        )
    else:
        links.append('<span class="chapter-step empty" aria-hidden="true"></span>')
    return '<nav class="chapter-pager" aria-label="Adjacent references">' + "".join(links) + "</nav>"


def _part_intro(part_key: str, label: str, description: str, count: int) -> str:
    return (
        f'<section class="part-divider" id="part-{html.escape(part_key)}" '
        f'data-section-title="{html.escape(label)}">'
        '<p class="eyebrow">Handbook track</p>'
        f'<h2>{html.escape(label)}</h2>'
        f'<p>{html.escape(description)}</p>'
        f'<span class="part-count">{count} reference{"s" if count != 1 else ""}</span>'
        "</section>"
    )


def _reference_intro(anchor: str, title: str, description: str, count: int, noun: str) -> str:
    return (
        f'<section class="part-divider reference-divider" id="{html.escape(anchor)}" '
        f'data-section-title="{html.escape(title)}">'
        '<p class="eyebrow">Reference library</p>'
        f'<h2>{html.escape(title)}</h2>'
        f'<p>{html.escape(description)}</p>'
        f'<span class="part-count">{count} {html.escape(noun)}{"s" if count != 1 else ""}</span>'
        "</section>"
    )


def render_content(entries: Sequence[ContentEntry]) -> str:
    """Render Part dividers, content cards, source links, and previous/next links."""

    sections: list[str] = []
    chapter_entries = [entry for entry in entries if entry.kind == "chapter"]
    platform_entries = [entry for entry in entries if entry.kind == "platform"]
    component_entries = [entry for entry in entries if entry.kind == "component"]

    chapter_by_group = _grouped(chapter_entries, "group_key")
    display_entries: list[ContentEntry] = []
    for part in PARTS:
        display_entries.extend(chapter_by_group.get(part.key, []))
    display_entries.extend(platform_entries)
    display_entries.extend(component_entries)

    previous_by_anchor: dict[str, ContentEntry | None] = {}
    next_by_anchor: dict[str, ContentEntry | None] = {}
    for index, entry in enumerate(display_entries):
        previous_by_anchor[entry.anchor] = display_entries[index - 1] if index > 0 else None
        next_by_anchor[entry.anchor] = (
            display_entries[index + 1] if index + 1 < len(display_entries) else None
        )

    for part in PARTS:
        part_entries = chapter_by_group.get(part.key, [])
        if not part_entries:
            continue
        sections.append(_part_intro(part.key, part.label, part.description, len(part_entries)))
        for entry in part_entries:
            sections.append(_render_entry(entry, previous_by_anchor, next_by_anchor))

    if platform_entries:
        sections.append(
            _reference_intro(
                "platforms",
                "Platform References",
                "Full integration profiles covering links, firmware, payloads, SDKs, compliance, and field gotchas.",
                len(platform_entries),
                "platform",
            )
        )
        sections.extend(
            _render_entry(entry, previous_by_anchor, next_by_anchor)
            for entry in platform_entries
        )

    if component_entries:
        sections.append(
            _reference_intro(
                "components",
                "Component References",
                "Deep references for propulsion, avionics, RF, sensors, compute, power, tactical systems, and complete ecosystems.",
                len(component_entries),
                "component category",
            )
        )
        sections.extend(
            _render_entry(entry, previous_by_anchor, next_by_anchor)
            for entry in component_entries
        )

    return "\n".join(sections)


def _render_entry(
    entry: ContentEntry,
    previous_by_anchor: dict[str, ContentEntry | None],
    next_by_anchor: dict[str, ContentEntry | None],
) -> str:
    source_url = f"{REPOSITORY_URL}/blob/main/{entry.relative_path}"
    return (
        f'<article class="chapter content-card" id="{html.escape(entry.anchor)}" '
        f'data-kind="{html.escape(entry.kind)}" '
        f'data-group="{html.escape(entry.group)}" '
        f'data-title="{html.escape(entry.title)}" '
        f'data-source="{html.escape(entry.relative_path)}">'
        '<header class="chapter-meta">'
        f'<p class="section-kicker">{html.escape(_entry_kicker(entry))}</p>'
        '<div class="chapter-tools">'
        f'<button class="copy-link" type="button" data-copy-anchor="{html.escape(entry.anchor)}">Copy link</button>'
        f'<a href="{html.escape(source_url)}">Source</a>'
        "</div></header>"
        f'<div class="chapter-body">{entry.html}</div>'
        f'{_entry_footer(previous_by_anchor[entry.anchor], next_by_anchor[entry.anchor])}'
        "</article>"
    )


def _search_metadata(entries: Sequence[ContentEntry]) -> str:
    payload = [
        {
            "anchor": entry.anchor,
            "title": entry.title,
            "kind": entry.kind,
            "group": entry.group,
            "source": entry.relative_path,
        }
        for entry in entries
    ]
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def _replace_tokens(template: str, replacements: dict[str, str]) -> str:
    for token, value in replacements.items():
        template = template.replace(f"{{{{{token}}}}}", value)
    unresolved = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", template)))
    if unresolved:
        raise ValueError(f"unresolved template tokens: {', '.join(unresolved)}")
    return template


def render_site(base_dir: Path, entries: Sequence[ContentEntry]) -> str:
    template_path = base_dir / "templates" / "handbook.html"
    if not template_path.is_file():
        raise FileNotFoundError(f"missing site template: {template_path}")

    counts = {
        "chapters": sum(entry.kind == "chapter" for entry in entries),
        "platforms": sum(entry.kind == "platform" for entry in entries),
        "components": sum(entry.kind == "component" for entry in entries),
    }
    template = template_path.read_text(encoding="utf-8")
    return _replace_tokens(
        template,
        {
            "SITE_TITLE": html.escape(SITE_TITLE),
            "SITE_DESCRIPTION": html.escape(SITE_DESCRIPTION),
            "SITE_URL": html.escape(SITE_URL),
            "REPOSITORY_URL": html.escape(REPOSITORY_URL),
            "NAV_DESKTOP": render_navigation(entries),
            "NAV_MOBILE": render_navigation(entries, mobile=True),
            "CONTENT": render_content(entries),
            "SEARCH_METADATA": _search_metadata(entries),
            "CHAPTER_COUNT": str(counts["chapters"]),
            "PLATFORM_COUNT": str(counts["platforms"]),
            "COMPONENT_COUNT": str(counts["components"]),
            "TOTAL_COUNT": str(len(entries)),
        },
    )


def _copy_static_assets(source_dir: Path, destination_dir: Path) -> None:
    if not source_dir.is_dir():
        raise FileNotFoundError(f"missing assets directory: {source_dir}")
    for source in source_dir.rglob("*"):
        if not source.is_file() or source.suffix.lower() not in _STATIC_ASSET_SUFFIXES:
            continue
        relative = source.relative_to(source_dir)
        destination = destination_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def _write_support_files(base_dir: Path, output_dir: Path) -> None:
    (output_dir / "robots.txt").write_text("User-agent: *\nDisallow:\n", encoding="utf-8")

    redirects = base_dir / "_redirects"
    if redirects.is_file():
        shutil.copy2(redirects, output_dir / "_redirects")

    tools = base_dir / "tools"
    if tools.is_dir():
        shutil.copytree(tools, output_dir / "tools", dirs_exist_ok=True)


def build_site(base_dir: Path | str, output_dir: Path | str) -> Path:
    """Build the complete static site and return ``site/index.html``."""

    base = Path(base_dir).resolve()
    output = Path(output_dir).resolve()
    staging = output.with_name(f"{output.name}.__building__")

    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)

    try:
        entries = discover_entries(base)
        render_entries(entries)
        document = render_site(base, entries)

        (staging / "index.html").write_text(document, encoding="utf-8")
        _copy_static_assets(base / "assets", staging / "assets")
        _write_support_files(base, staging)

        if output.exists():
            shutil.rmtree(output)
        os.replace(staging, output)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise

    index_path = output / "index.html"
    chapter_count = sum(entry.kind == "chapter" for entry in entries)
    platform_count = sum(entry.kind == "platform" for entry in entries)
    component_count = sum(entry.kind == "component" for entry in entries)
    print("Building The Drone Integration Handbook...")
    print(
        f"  Rendered {chapter_count} chapters, {platform_count} platforms, "
        f"and {component_count} component references"
    )
    print(f"  Output: {index_path}")
    print(f"  Size: {index_path.stat().st_size:,} bytes")
    print("  Done.")
    return index_path
