import os
import re
import markdown
from collections import defaultdict

# ── CHAPTERS: kept ordered — narrative flow matters ──────────────────────────
CHAPTERS = [
    ("fundamentals/five-link-types.md",       1,  "The Five Link Types"),
    ("fundamentals/frequency-bands.md",        2,  "Frequency Bands & Regulatory Reality"),
    ("fundamentals/antennas.md",               3,  "Antennas for People Who Aren't RF Engineers"),
    ("fundamentals/link-budgets.md",           4,  "Link Budgets Without the Math"),
    ("firmware/four-firmwares.md",             5,  "The Four Firmwares"),
    ("firmware/msp-protocol.md",               6,  "MSP Protocol"),
    ("firmware/mavlink-protocol.md",           7,  "MAVLink Protocol"),
    ("firmware/uart-layout.md",                8,  "UART Layout and Why It Matters"),
    ("field/preflight.md",                     9,  "Pre-Flight Checklist That Actually Works"),
    ("field/blackbox.md",                      10, "Blackbox Logs"),
    ("field/pid-tuning.md",                    11, "PID Tuning for People Who Fly"),
    ("field/troubleshooting.md",               12, "When Things Go Wrong"),
    ("integration/companion.md",               13, "Adding a Companion Computer"),
    ("integration/mesh-radios.md",             14, "Mesh Radios for Multi-Vehicle"),
    ("integration/tak.md",                     15, "TAK Integration"),
    ("field/unsolved-problems.md",             16, "Unsolved Problems"),
]

PARTS = [
    ("Part 1 — RF Fundamentals",         [1, 2, 3, 4]),
    ("Part 2 — Flight Controller Firmware", [5, 6, 7, 8]),
    ("Part 3 — Field Operations",        [9, 10, 11, 12]),
    ("Part 4 — Integration",             [13, 14, 15]),
    ("What's Left to Solve",             [16]),
]

# Category display names for the platforms/ subdirectory names
_PLATFORM_CATS = [
    ("cots",         "COTS"),
    ("blue-uas",     "NDAA / Blue UAS"),
    ("open-source",  "Open-Source / Custom"),
    ("tactical",     "Tactical / Defense"),
]

# Component groups — organizes the flat list of 44+ component docs into
# navigable sub-categories. Matched by substring in the filename.
_COMPONENT_GROUPS = [
    ("Propulsion & Airframe", [
        "frames-", "motors", "escs", "propellers", "propulsion-system",
        "propulsion-non-electric", "power-architecture",
    ]),
    ("Flight Controllers & Firmware", [
        "flight-controller", "integrated-stacks",
    ]),
    ("RF, Comms & Control Links", [
        "comms-datalinks", "c2-datalinks", "mafiairs", "military-firmware",
    ]),
    ("Video & Cameras", [
        "fpv-cameras", "video-transmitters", "thermal-cameras",
    ]),
    ("Navigation & Sensors", [
        "gps", "gnss-", "rtk-ppk", "navigation-pnt", "lidar",
        "sensor-payload", "detect-and-avoid",
    ]),
    ("Companion & Compute", [
        "companion-computer", "ai-accelerator", "ground-control",
    ]),
    ("Batteries & Power", [
        "batteries", "battery-deep",
    ]),
    ("Defense & Tactical", [
        "electronic-warfare", "counter-uas", "esad-safe", "tactical-accessories",
        "rf-detection", "swarm-software",
    ]),
    ("Platforms & Compliance", [
        "platforms-global", "ndaa-compliance", "remote-id", "bvlos",
        "utm-airspace", "uas-maintenance", "industry-intelligence",
    ]),
    ("Manufacturer Guides", [
        "orqa-hardware", "openhd-implementation",
    ]),
]


# ── AUTO-DISCOVERY ───────────────────────────────────────────────────────────

def _title_from_file(filepath):
    """Read first H1 from a markdown file, fall back to filename."""
    title = os.path.basename(filepath).replace(".md", "").replace("-", " ").replace("_", " ").title()
    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    return line[2:].strip()
    except Exception:
        pass
    return title


def _discover_dir(base_dir, subdir, start_num):
    """
    Walk subdir, return sorted list of (rel_path, num, title).
    Skips README.md and index.md. Numbers are assigned sequentially
    starting at start_num — stable as long as filenames don't change.
    """
    root = os.path.join(base_dir, subdir)
    if not os.path.isdir(root):
        return []
    paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for fname in sorted(filenames):
            if not fname.endswith(".md"):
                continue
            if fname.lower() in ("readme.md", "index.md"):
                continue
            paths.append(os.path.join(dirpath, fname))
    return [
        (os.path.relpath(p, base_dir), start_num + i, _title_from_file(p))
        for i, p in enumerate(sorted(paths))
    ]


def _build_platforms(base_dir):
    """Discover all platform .md files, grouped by category subdir."""
    all_entries = []
    seen = set()
    for cat_key, _ in _PLATFORM_CATS:
        for entry in _discover_dir(base_dir, f"platforms/{cat_key}", len(all_entries) * 0):
            if entry[0] not in seen:
                seen.add(entry[0])
                all_entries.append(entry)
    # Re-number sequentially across all categories starting at 101
    return [(rel, 101 + i, title) for i, (rel, _, title) in enumerate(all_entries)]


def _build_components(base_dir):
    """Discover all component .md files."""
    return _discover_dir(base_dir, "components", 600)


# ── HELPERS ──────────────────────────────────────────────────────────────────

def read_chapter(filepath):
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def fix_internal_links(html_content, ch_num):
    for filepath, num, title in CHAPTERS:
        basename = os.path.basename(filepath)
        html_content = html_content.replace(f"({basename})", f"(#ch{num})")
        html_content = html_content.replace(f"(../{filepath})", f"(#ch{num})")
        html_content = html_content.replace(f"({filepath})", f"(#ch{num})")
    return html_content


def md_to_html(md_text):
    return markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "codehilite", "toc"],
        extension_configs={"codehilite": {"css_class": "code"}},
    )


# ── TOC ──────────────────────────────────────────────────────────────────────

def build_toc(platforms, components):
    toc = ""
    for part_name, ch_nums in PARTS:
        toc += f'<div class="toc-part"><h3>{part_name}</h3>\n'
        for num in ch_nums:
            for filepath, ch_num, title in CHAPTERS:
                if ch_num == num:
                    toc += f'<a href="#ch{ch_num}"><span class="ch-num">{ch_num}</span>{title}</a>\n'
        toc += "</div>\n"

    # Platforms — collapsible, grouped by category
    toc += '<div class="toc-part">\n<details class="toc-collapse">\n'
    toc += (
        '<summary><h3>Part 5 — Platform References</h3>'
        f'<span class="toc-count">{len(platforms)} platforms</span></summary>\n'
    )
    # Group entries by their parent directory name
    groups = defaultdict(list)
    for rel, p_num, title in platforms:
        cat = os.path.basename(os.path.dirname(rel))
        groups[cat].append((rel, p_num, title))
    for cat_key, cat_label in _PLATFORM_CATS:
        if cat_key not in groups:
            continue
        toc += (
            f'<span style="display:block;color:var(--accent-dim);'
            f'font-size:0.8rem;margin:0.5rem 0 0.2rem 0;">{cat_label}</span>\n'
        )
        for rel, p_num, title in groups[cat_key]:
            toc += f'<a href="#p{p_num}"><span class="ch-num">&bull;</span>{title}</a>\n'
    toc += '</details>\n</div>\n'

    # Components — collapsible, grouped by topic
    toc += '<div class="toc-part">\n<details class="toc-collapse">\n'
    toc += (
        '<summary><h3>Part 6 — Component References</h3>'
        f'<span class="toc-count">{len(components)} categories</span></summary>\n'
    )
    # Build lookup: filename → (rel, c_num, title)
    comp_lookup = {os.path.basename(rel).replace('.md', ''): (rel, c_num, title)
                   for rel, c_num, title in components}
    used = set()
    for group_name, patterns in _COMPONENT_GROUPS:
        group_entries = []
        for fname, entry in comp_lookup.items():
            if fname in used:
                continue
            if any(pat in fname for pat in patterns):
                group_entries.append(entry)
                used.add(fname)
        if not group_entries:
            continue
        toc += (
            f'<details class="toc-subgroup"><summary class="toc-subgroup-label">'
            f'{group_name} <span class="toc-count">({len(group_entries)})</span>'
            f'</summary>\n'
        )
        for rel, c_num, title in group_entries:
            toc += f'<a href="#c{c_num}"><span class="ch-num">&bull;</span>{title}</a>\n'
        toc += '</details>\n'
    # Catch any ungrouped components
    ungrouped = [(rel, c_num, title) for fname, (rel, c_num, title) in comp_lookup.items()
                 if fname not in used]
    if ungrouped:
        toc += (
            '<details class="toc-subgroup"><summary class="toc-subgroup-label">'
            f'Other <span class="toc-count">({len(ungrouped)})</span>'
            '</summary>\n'
        )
        for rel, c_num, title in ungrouped:
            toc += f'<a href="#c{c_num}"><span class="ch-num">&bull;</span>{title}</a>\n'
        toc += '</details>\n'
    toc += '</details>\n</div>\n'
    return toc


# ── SECTION BUILDERS ─────────────────────────────────────────────────────────

def build_chapters(base_dir):
    out = ""
    for filepath, ch_num, title in CHAPTERS:
        md = read_chapter(os.path.join(base_dir, filepath))
        if not md:
            print(f"  WARNING: Missing {filepath}")
            continue
        html = fix_internal_links(md_to_html(md), ch_num)
        out += f'<section class="chapter" id="ch{ch_num}">\n{html}\n</section>\n\n'
        print(f"  Built chapter {ch_num}: {title}")
    return out


def build_platforms(base_dir, platforms):
    out = (
        '<section class="chapter" id="platforms">'
        '<h1>Part 5 — Platform References</h1>'
        '<p><em>Full integration profiles — RF links, firmware, payloads, SDKs, '
        'and gotchas. Vetted parts only.</em></p></section>\n'
    )
    for filepath, p_num, title in platforms:
        md = read_chapter(os.path.join(base_dir, filepath))
        if not md:
            print(f"  WARNING: Missing {filepath}")
            continue
        out += f'<section class="chapter" id="p{p_num}">\n{md_to_html(md)}\n</section>\n\n'
        print(f"  Built platform: {title}")
    return out


def build_components(base_dir, components):
    out = (
        '<section class="chapter" id="components">'
        '<h1>Part 6 — Component References</h1>'
        '<p><em>Deep dives on flight controllers, ESCs, motors, batteries, companion '
        'computers, radios, sensors, and complete ecosystems. Specs that matter, '
        "gotchas that don't show up in datasheets.</em></p></section>\n"
    )
    for filepath, c_num, title in components:
        md = read_chapter(os.path.join(base_dir, filepath))
        if not md:
            print(f"  WARNING: Missing {filepath}")
            continue
        out += f'<section class="chapter" id="c{c_num}">\n{md_to_html(md)}\n</section>\n\n'
        print(f"  Built component: {title}")
    return out


def build_site(base_dir, output_dir):
    """Build the complete single-page HTML site."""
    print("Building The Drone Integration Handbook...")

    platforms  = _build_platforms(base_dir)
    components = _build_components(base_dir)
    print(f"  Discovered {len(platforms)} platforms, {len(components)} component pages")

    toc = build_toc(platforms, components)
    chapters = build_chapters(base_dir)
    plat_html  = build_platforms(base_dir, platforms)
    comp_html  = build_components(base_dir, components)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Drone Integration Handbook</title>
<meta name="description" content="An industry reference for drone RF, integration, and field operations. Built by operators, for operators.">
<meta property="og:title" content="The Drone Integration Handbook">
<meta property="og:description" content="Free. Open. No login required. An industry reference for drone RF, integration, and field operations.">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.0.3/src/regular/style.css">
<style>
:root {{
  --bg: #0a0b10;
  --bg-surface: #10111a;
  --bg-elevated: #161824;
  --bg-panel: #12131e;
  --text: #c8cad0;
  --text-dim: #5a5e6e;
  --text-bright: #e8eaef;
  --text-faint: #3e4152;
  --accent: #00d4ff;
  --accent-dim: #0088a3;
  --accent-red: #ff3b5c;
  --accent-amber: #f59e0b;
  --border: #1e2030;
  --border-bright: #2a2d42;
  --code-bg: #0d0e16;
  --success: #22c55e;
  --warn: #f59e0b;
  --mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
  --heading: 'Rajdhani', 'Barlow Condensed', sans-serif;
  --body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --radius-sm: 6px;
}}

*, *::before, *::after {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

html {{
  scroll-behavior: smooth;
  scroll-padding-top: 5rem;
}}

body {{
  font-family: var(--body);
  font-size: 15px;
  line-height: 1.7;
  color: var(--text);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
}}

/* ── TOPBAR (matches Forge) ── */
.topbar {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 20px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-panel);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}}

.topbar-left {{
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}}

.topbar-logo {{
  font-family: var(--heading);
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--accent);
  text-decoration: none;
  white-space: nowrap;
}}

.topbar-sep {{
  color: var(--text-faint);
  font-size: 0.75rem;
  flex-shrink: 0;
}}

.topbar-page {{
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--text-dim);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}

.topbar-right {{
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}}

/* ── Hamburger Button (matches Forge) ── */
.hamburger-btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: none;
  border: 1px solid var(--border);
  color: var(--text-dim);
  cursor: pointer;
  transition: all 0.15s;
  flex-shrink: 0;
  font-size: 20px;
  line-height: 1;
}}

.hamburger-btn:hover {{
  background: var(--bg-elevated);
  color: var(--accent);
  border-color: rgba(0,212,255,0.2);
}}

.hamburger-btn.open {{
  background: rgba(0,212,255,0.08);
  color: var(--accent);
  border-color: var(--accent);
}}

/* ── Topbar Pills (matches Forge) ── */
.topbar-pill {{
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 20px;
  font-family: var(--mono);
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  background: rgba(0,212,255,0.08);
  color: var(--accent);
  border: 1px solid rgba(0,212,255,0.18);
  text-decoration: none;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}}

.topbar-pill:hover {{
  background: rgba(0,212,255,0.16);
  border-color: rgba(0,212,255,0.35);
}}

.topbar-pill.ghost {{
  background: none;
  color: var(--text-dim);
  border-color: var(--border);
}}

.topbar-pill.ghost:hover {{
  color: var(--text-bright);
  border-color: var(--border-bright);
  background: var(--bg-elevated);
}}

/* Search trigger pill */
.search-trigger {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 20px;
  font-family: var(--mono);
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  background: none;
  color: var(--text-dim);
  border: 1px solid var(--border);
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}}

.search-trigger:hover {{
  color: var(--text-bright);
  border-color: var(--border-bright);
  background: var(--bg-elevated);
}}

.search-trigger kbd {{
  font-family: var(--mono);
  font-size: 0.55rem;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 0.1rem 0.3rem;
  color: var(--text-faint);
  line-height: 1;
}}

/* ── Nav Drawer (matches Forge) ── */
.nav-drawer-overlay {{
  position: fixed;
  inset: 0;
  z-index: 200;
  background: rgba(0,0,0,0.6);
  backdrop-filter: blur(4px);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s;
}}

.nav-drawer-overlay.open {{
  opacity: 1;
  pointer-events: auto;
}}

.nav-drawer {{
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 201;
  width: 280px;
  max-width: 85vw;
  background: var(--bg-panel);
  border-right: 1px solid var(--border);
  transform: translateX(-100%);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}}

.nav-drawer.open {{
  transform: translateX(0);
}}

.nav-drawer-header {{
  padding: 20px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}}

.nav-drawer-close {{
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: none;
  border: 1px solid var(--border);
  color: var(--text-dim);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: all 0.15s;
}}

.nav-drawer-close:hover {{
  color: var(--accent-red);
  border-color: rgba(255,59,92,0.3);
}}

.nav-drawer-section {{
  padding: 12px 16px 4px;
}}

.nav-drawer-label {{
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-faint);
  font-weight: 600;
  font-family: var(--mono);
  padding: 0 8px 6px;
}}

.nav-drawer-item {{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  margin: 2px 0;
  color: var(--text-dim);
  text-decoration: none;
  font-family: var(--mono);
  font-size: 0.75rem;
  transition: all 0.15s;
  border: 1px solid transparent;
}}

.nav-drawer-item:hover {{
  color: var(--text-bright);
  background: var(--bg-elevated);
}}

.nav-drawer-item.active {{
  color: var(--accent);
  background: rgba(0,212,255,0.06);
  border-color: rgba(0,212,255,0.12);
}}

.nav-drawer-item i {{
  font-size: 16px;
  width: 20px;
  text-align: center;
  flex-shrink: 0;
}}

.nav-drawer-footer {{
  margin-top: auto;
  padding: 16px;
  border-top: 1px solid var(--border);
  font-family: var(--mono);
  font-size: 0.6rem;
  color: var(--text-faint);
}}

/* ── HERO ── */
.hero {{
  max-width: 860px;
  margin: 0 auto;
  padding: 5rem 2rem 3.5rem;
  text-align: center;
}}

.hero h1 {{
  font-family: var(--heading);
  font-size: clamp(1.8rem, 5vw, 2.8rem);
  font-weight: 700;
  color: var(--text-bright);
  letter-spacing: 0.02em;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}}

.hero h1::before {{
  content: '// ';
  color: var(--accent);
}}

.hero .tagline {{
  font-family: var(--mono);
  font-size: 0.85rem;
  color: var(--text-dim);
  margin-bottom: 2rem;
  letter-spacing: 0.02em;
}}

.hero .intro {{
  font-size: 1.05rem;
  color: var(--text);
  max-width: 640px;
  margin: 0 auto 2.5rem;
  line-height: 1.8;
}}

.hero .meta {{
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--text-dim);
  letter-spacing: 0.05em;
}}

.hero .meta a {{
  color: var(--accent);
  text-decoration: none;
}}

.hero .meta a:hover {{
  text-decoration: underline;
}}

/* ── TABLE OF CONTENTS ── */
.toc {{
  max-width: 860px;
  margin: 0 auto 4rem;
  padding: 0 2rem;
}}

.toc-part {{
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
}}

.toc-part h3 {{
  font-family: var(--heading);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--accent);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}}

.toc-part a {{
  display: flex;
  align-items: baseline;
  width: 100%;
  box-sizing: border-box;
  padding: 0.5rem 0.75rem;
  margin: 0.15rem 0;
  color: var(--text);
  text-decoration: none;
  font-size: 0.95rem;
  border-radius: 4px;
  transition: background 0.15s, color 0.15s;
}}

.toc-part a:hover {{
  background: var(--bg-elevated);
  color: var(--text-bright);
}}

.ch-num {{
  font-family: var(--mono);
  font-size: 0.75rem;
  color: var(--accent-dim);
  min-width: 2.5rem;
  font-weight: 700;
}}

/* ── TOC COLLAPSIBLE ── */
.toc-collapse {{
  border: none;
}}

.toc-collapse summary {{
  cursor: pointer;
  list-style: none;
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
}}

.toc-collapse summary::-webkit-details-marker {{
  display: none;
}}

.toc-collapse summary::before {{
  content: '▸';
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--accent-dim);
  transition: transform 0.2s;
  flex-shrink: 0;
}}

.toc-collapse[open] summary::before {{
  transform: rotate(90deg);
}}

.toc-collapse summary h3 {{
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
  display: inline;
}}

.toc-collapse .toc-count {{
  font-family: var(--mono);
  font-size: 0.65rem;
  color: var(--text-dim);
  letter-spacing: 0.04em;
}}

.toc-collapse[open] summary {{
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}}

/* ── TOC SUBGROUPS ── */
.toc-subgroup {{
  margin: 0.25rem 0 0.25rem 0.5rem;
  border: none;
}}

.toc-subgroup-label {{
  cursor: pointer;
  list-style: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.5rem;
  font-family: var(--mono);
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--accent-dim);
  border-radius: 4px;
  transition: background 0.15s;
}}

.toc-subgroup-label:hover {{
  background: var(--bg-elevated);
}}

.toc-subgroup-label::-webkit-details-marker {{
  display: none;
}}

.toc-subgroup summary::before {{
  content: '▸';
  font-family: var(--mono);
  font-size: 0.6rem;
  color: var(--text-dim);
  transition: transform 0.15s;
  flex-shrink: 0;
}}

.toc-subgroup[open] summary::before {{
  transform: rotate(90deg);
}}

.toc-subgroup a {{
  padding-left: 1.5rem !important;
  font-size: 0.88rem;
}}

/* ── CHAPTER CONTENT ── */
.content {{
  max-width: 860px;
  margin: 0 auto;
  padding: 0 2rem 6rem;
}}

.chapter {{
  margin-bottom: 5rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border);
}}

.chapter h1 {{
  font-family: var(--heading);
  font-size: clamp(1.4rem, 3.5vw, 2rem);
  font-weight: 700;
  color: var(--text-bright);
  margin-bottom: 0.5rem;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}}

.chapter h2 {{
  font-family: var(--heading);
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--accent);
  margin: 2.5rem 0 1rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--border);
  letter-spacing: 0.02em;
  text-transform: uppercase;
}}

.chapter h3 {{
  font-family: var(--heading);
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--text-bright);
  margin: 2rem 0 0.75rem;
  letter-spacing: 0.01em;
}}

.chapter h4 {{
  font-family: var(--mono);
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-dim);
  margin: 1.5rem 0 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}}

.chapter p {{
  margin-bottom: 1rem;
}}

.chapter blockquote {{
  border-left: 3px solid var(--accent-dim);
  padding: 0.75rem 1.25rem;
  margin: 1.5rem 0;
  background: var(--bg-surface);
  border-radius: 0 4px 4px 0;
  font-style: italic;
  color: var(--text-dim);
}}

.chapter blockquote p {{
  margin-bottom: 0;
}}

.chapter ul, .chapter ol {{
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}}

.chapter li {{
  margin-bottom: 0.4rem;
}}

.chapter strong {{
  color: var(--text-bright);
  font-weight: 600;
}}

.chapter a {{
  color: var(--accent);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s;
}}

.chapter a:hover {{
  border-bottom-color: var(--accent);
}}

.chapter hr {{
  border: none;
  border-top: 1px solid var(--border);
  margin: 2rem 0;
}}

.chapter em {{
  color: var(--text-dim);
}}

/* ── TABLES ── */
.chapter table {{
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  font-size: 0.88rem;
  overflow-x: auto;
  display: block;
}}

.chapter thead {{
  display: table-header-group;
}}

.chapter tbody {{
  display: table-row-group;
}}

.chapter tr {{
  display: table-row;
}}

.chapter table {{
  display: table;
}}

@media (max-width: 700px) {{
  .chapter table {{
    display: block;
    overflow-x: auto;
  }}
}}

.chapter th {{
  font-family: var(--mono);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--accent-dim);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  text-align: left;
  padding: 0.6rem 0.75rem;
  border-bottom: 2px solid var(--border-bright);
  white-space: nowrap;
}}

.chapter td {{
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
}}

.chapter tr:hover td {{
  background: var(--bg-surface);
}}

/* ── CODE ── */
.chapter code {{
  font-family: var(--mono);
  font-size: 0.82em;
  background: var(--code-bg);
  padding: 0.15em 0.4em;
  border-radius: 3px;
  color: var(--accent);
}}

.chapter pre {{
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 1.25rem 1.5rem;
  overflow-x: auto;
  margin: 1.5rem 0;
  line-height: 1.5;
}}

.chapter pre code {{
  background: none;
  padding: 0;
  font-size: 0.8rem;
  color: var(--text);
}}

/* ── FOOTER ── */
.site-footer {{
  max-width: 860px;
  margin: 0 auto;
  padding: 3rem 2rem;
  border-top: 1px solid var(--border);
  text-align: center;
}}

.site-footer p {{
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--text-dim);
  letter-spacing: 0.03em;
  margin-bottom: 0.5rem;
}}

.site-footer a {{
  color: var(--accent);
  text-decoration: none;
}}

.site-footer a:hover {{
  text-decoration: underline;
}}

/* ── BACK TO TOP ── */
.back-to-top {{
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 2.5rem;
  height: 2.5rem;
  background: var(--bg-elevated);
  border: 1px solid var(--border-bright);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-dim);
  text-decoration: none;
  font-size: 1rem;
  opacity: 0;
  transition: opacity 0.3s, background 0.2s;
  pointer-events: none;
}}

.back-to-top.visible {{
  opacity: 1;
  pointer-events: auto;
}}

.back-to-top:hover {{
  background: var(--border-bright);
  color: var(--accent);
}}

/* ── RESPONSIVE ── */
@media (max-width: 768px) {{
  body {{ font-size: 14px; }}
  .hero {{ padding: 3.5rem 1.25rem 2.5rem; }}
  .toc, .content {{ padding-left: 1.25rem; padding-right: 1.25rem; }}
  .topbar {{ padding: 8px 14px; }}
  .chapter pre {{ padding: 1rem; }}
  .topbar-pill.hide-mobile {{ display: none; }}
}}

/* ── SEARCH OVERLAY ── */
.search-overlay {{
  display: none;
  position: fixed;
  inset: 0;
  z-index: 500;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  align-items: flex-start;
  justify-content: center;
  padding-top: min(15vh, 120px);
}}

.search-overlay.open {{
  display: flex;
}}

.search-modal {{
  width: min(640px, 92vw);
  max-height: 70vh;
  background: var(--bg-surface);
  border: 1px solid var(--border-bright);
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 24px 80px rgba(0,0,0,0.6);
  animation: searchSlide 0.15s ease-out;
}}

@keyframes searchSlide {{
  from {{ opacity: 0; transform: translateY(-12px) scale(0.98); }}
  to {{ opacity: 1; transform: translateY(0) scale(1); }}
}}

.search-input-wrap {{
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border);
}}

.search-icon {{
  flex-shrink: 0;
  color: var(--accent-dim);
}}

.search-input {{
  flex: 1;
  background: none;
  border: none;
  outline: none;
  font-family: var(--serif);
  font-size: 1.1rem;
  color: var(--text-bright);
  caret-color: var(--accent);
}}

.search-input::placeholder {{
  color: var(--text-dim);
  font-size: 0.95rem;
}}

.search-esc {{
  font-family: var(--mono);
  font-size: 0.6rem;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 0.15rem 0.4rem;
  color: var(--text-dim);
  flex-shrink: 0;
}}

.search-results {{
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
  scrollbar-width: thin;
  scrollbar-color: var(--border-bright) transparent;
}}

.search-empty {{
  padding: 2rem 1rem;
  text-align: center;
  font-family: var(--mono);
  font-size: 0.8rem;
  color: var(--text-dim);
}}

.search-result {{
  display: block;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  text-decoration: none;
  cursor: pointer;
  transition: background 0.12s;
}}

.search-result:hover,
.search-result.active {{
  background: var(--bg-elevated);
}}

.search-result-chapter {{
  font-family: var(--mono);
  font-size: 0.65rem;
  font-weight: 600;
  color: var(--accent-dim);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 0.25rem;
}}

.search-result-heading {{
  font-family: var(--mono);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-bright);
  margin-bottom: 0.2rem;
}}

.search-result-snippet {{
  font-size: 0.8rem;
  color: var(--text-dim);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}}

.search-result-snippet mark {{
  background: none;
  color: var(--accent);
  font-weight: 600;
}}

.search-count {{
  padding: 0.4rem 1rem 0.25rem;
  font-family: var(--mono);
  font-size: 0.65rem;
  color: var(--text-dim);
  letter-spacing: 0.04em;
}}

.search-footer {{
  display: flex;
  gap: 1.5rem;
  padding: 0.6rem 1.25rem;
  border-top: 1px solid var(--border);
  font-family: var(--mono);
  font-size: 0.6rem;
  color: var(--text-dim);
  letter-spacing: 0.03em;
}}

.search-footer kbd {{
  display: inline-block;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 0rem 0.3rem;
  font-family: var(--mono);
  font-size: 0.6rem;
  color: var(--text-dim);
  margin-right: 0.15rem;
  line-height: 1.4;
}}

@media (max-width: 600px) {{
  .search-trigger span,
  .search-trigger kbd {{
    display: none;
  }}
  .search-trigger {{
    padding: 0.4rem 0.5rem;
    margin-left: 0;
  }}
  .search-modal {{
    max-height: 85vh;
    border-radius: 0;
    width: 100vw;
  }}
  .search-overlay {{
    padding-top: 0;
    align-items: flex-start;
  }}
  .search-footer {{
    display: none;
  }}
}}

/* ── PRINT ── */
@media print {{
  .site-header, .back-to-top {{ display: none; }}
  body {{ background: white; color: black; font-size: 11pt; }}
  .chapter {{ page-break-inside: avoid; }}
  .chapter a {{ color: black; text-decoration: underline; }}
}}
</style>
</head>
<body>

<!-- Nav Drawer Overlay -->
<div class="nav-drawer-overlay" id="navOverlay"></div>

<!-- Nav Drawer -->
<nav class="nav-drawer" id="navDrawer">
  <div class="nav-drawer-header">
    <span class="topbar-logo">Handbook</span>
    <button class="nav-drawer-close" id="navDrawerClose" aria-label="Close menu"><i class="ph ph-x"></i></button>
  </div>
  <div class="nav-drawer-section">
    <div class="nav-drawer-label">Handbook</div>
    <a href="#toc" class="nav-drawer-item"><i class="ph ph-list"></i> Table of Contents</a>
    <a href="#ch1" class="nav-drawer-item"><i class="ph ph-broadcast"></i> RF Fundamentals</a>
    <a href="#ch5" class="nav-drawer-item"><i class="ph ph-cpu"></i> Firmware</a>
    <a href="#ch9" class="nav-drawer-item"><i class="ph ph-checklist"></i> Field Ops</a>
    <a href="#ch13" class="nav-drawer-item"><i class="ph ph-plugs-connected"></i> Integration</a>
    <a href="#platforms" class="nav-drawer-item"><i class="ph ph-airplane-tilt"></i> Platform References</a>
    <a href="#components" class="nav-drawer-item"><i class="ph ph-circuitry"></i> Component Docs</a>
  </div>
  <div class="nav-drawer-section">
    <div class="nav-drawer-label">Forge Ecosystem</div>
    <a href="https://forgeprole.netlify.app" class="nav-drawer-item"><i class="ph ph-database"></i> Forge</a>
    <a href="https://forgeprole.netlify.app/tools-home/" class="nav-drawer-item"><i class="ph ph-wrench"></i> Tools</a>
    <a href="https://forgeprole.netlify.app/patterns-home/" class="nav-drawer-item"><i class="ph ph-graph"></i> Patterns</a>
    <a href="https://forgeprole.netlify.app/intel/" class="nav-drawer-item"><i class="ph ph-newspaper"></i> Intel</a>
    <a href="https://forgeprole.netlify.app/wingman/" class="nav-drawer-item"><i class="ph ph-robot"></i> Wingman AI</a>
  </div>
  <div class="nav-drawer-section">
    <div class="nav-drawer-label">Project</div>
    <a href="https://github.com/DroneWuKong/drone-integration-handbook" class="nav-drawer-item"><i class="ph ph-github-logo"></i> GitHub</a>
    <a href="https://github.com/DroneWuKong/drone-integration-handbook/blob/main/ROADMAP.md" class="nav-drawer-item"><i class="ph ph-map-trifold"></i> Roadmap</a>
    <a href="https://github.com/DroneWuKong/drone-integration-handbook/blob/main/CONTRIBUTING.md" class="nav-drawer-item"><i class="ph ph-git-pull-request"></i> Contribute</a>
  </div>
  <div class="nav-drawer-footer">v1.0 &middot; CC BY-SA 4.0</div>
</nav>

<!-- Topbar -->
<header class="topbar">
  <div class="topbar-left">
    <button class="hamburger-btn" id="hamburgerBtn" aria-label="Menu">
      <i class="ph ph-list"></i>
    </button>
    <a href="#" class="topbar-logo">Handbook</a>
  </div>
  <div class="topbar-right">
    <button class="search-trigger" id="searchTrigger" aria-label="Search">
      <i class="ph ph-magnifying-glass" style="font-size:13px;"></i>
      <span>Search</span>
      <kbd>&#8984;K</kbd>
    </button>
    <a href="https://forgeprole.netlify.app" class="topbar-pill">Forge</a>
    <a href="https://forgeprole.netlify.app/intel/" class="topbar-pill hide-mobile">Intel</a>
    <a href="https://forgeprole.netlify.app/patterns-home/" class="topbar-pill hide-mobile">Patterns</a>
    <a href="https://forgeprole.netlify.app/wingman/" class="topbar-pill">Wingman</a>
  </div>
</header>

<div class="hero">
  <h1>The Drone Integration Handbook</h1>
  <p class="tagline">Free. Open. No login required.</p>
  <p class="intro">
    A practical reference for anyone integrating, operating, or troubleshooting
    multi-platform drone systems. Not a product manual. Not a sales pitch.
    A handbook you keep open on your bench. Covers RF communications, flight
    controller firmware, field diagnostics, fleet operations, and the real-world
    problems that don't show up in manufacturer documentation.
  </p>
  <p class="meta">
    CC BY-SA 4.0 &middot; v1.0 &middot;
    <a href="https://github.com/DroneWuKong/drone-integration-handbook">Source on GitHub</a>
  </p>
</div>

<div class="toc" id="toc">
{toc}
</div>

<div class="content">
{chapters}
{plat_html}
{comp_html}
</div>

<footer class="site-footer">
  <p><em>Built in the field. With real data. On real hardware.</em></p>
  <p>
    <a href="https://github.com/DroneWuKong/drone-integration-handbook">GitHub</a> &middot;
    <a href="https://github.com/DroneWuKong/drone-integration-handbook/blob/main/CONTRIBUTING.md">Contribute</a> &middot;
    <a href="https://github.com/DroneWuKong/drone-integration-handbook/blob/main/ROADMAP.md">Roadmap</a>
  </p>
  <p>The Drone Integration Handbook &copy; 2025-2026 &middot; CC BY-SA 4.0</p>
</footer>

<a href="#" class="back-to-top" id="btt" title="Back to top">&uarr;</a>

<!-- SEARCH OVERLAY -->
<div class="search-overlay" id="searchOverlay">
  <div class="search-modal">
    <div class="search-input-wrap">
      <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input type="text" class="search-input" id="searchInput" placeholder="Search chapters, protocols, pinouts, platforms..." autocomplete="off" spellcheck="false">
      <kbd class="search-esc">ESC</kbd>
    </div>
    <div class="search-results" id="searchResults">
      <div class="search-empty">Type to search across all chapters and platform profiles.</div>
    </div>
    <div class="search-footer">
      <span><kbd>&uarr;</kbd><kbd>&darr;</kbd> navigate</span>
      <span><kbd>&#9166;</kbd> jump</span>
      <span><kbd>esc</kbd> close</span>
    </div>
  </div>
</div>

<script>
// ── BACK TO TOP ──
const btt = document.getElementById('btt');
window.addEventListener('scroll', () => {{
  btt.classList.toggle('visible', window.scrollY > 600);
}});

// ── NAV DRAWER (Forge pattern) ──
(function() {{
  const hamburger = document.getElementById('hamburgerBtn');
  const drawer = document.getElementById('navDrawer');
  const overlay = document.getElementById('navOverlay');
  const closeBtn = document.getElementById('navDrawerClose');

  function openDrawer() {{
    drawer.classList.add('open');
    overlay.classList.add('open');
    hamburger.classList.add('open');
    document.body.style.overflow = 'hidden';
  }}

  function closeDrawer() {{
    drawer.classList.remove('open');
    overlay.classList.remove('open');
    hamburger.classList.remove('open');
    document.body.style.overflow = '';
  }}

  hamburger.addEventListener('click', openDrawer);
  overlay.addEventListener('click', closeDrawer);
  closeBtn.addEventListener('click', closeDrawer);

  drawer.querySelectorAll('a').forEach(link => {{
    link.addEventListener('click', closeDrawer);
  }});

  document.addEventListener('keydown', e => {{
    if (e.key === 'Escape') closeDrawer();
  }});
}})();

// ── SEARCH ENGINE ──
(function() {{
  const overlay = document.getElementById('searchOverlay');
  const input = document.getElementById('searchInput');
  const resultsEl = document.getElementById('searchResults');
  const trigger = document.getElementById('searchTrigger');
  let activeIdx = -1;
  let searchIndex = null;

  // Build index on first open — scrape all section content
  function buildIndex() {{
    if (searchIndex) return;
    searchIndex = [];
    const sections = document.querySelectorAll('.chapter');
    sections.forEach(section => {{
      const id = section.id;
      // Get the chapter/platform title
      const h1 = section.querySelector('h1');
      const chapterTitle = h1 ? h1.textContent.trim() : '';

      // Index every h2/h3 as a separate entry with surrounding text
      const headings = section.querySelectorAll('h2, h3');
      if (headings.length === 0 && h1) {{
        // Section with just h1 — index the whole thing
        const text = section.textContent.replace(/\\s+/g, ' ').trim();
        searchIndex.push({{ id, chapterTitle, heading: chapterTitle, text, el: section }});
        return;
      }}

      headings.forEach(heading => {{
        // Collect text from this heading until the next heading
        let text = heading.textContent + ' ';
        let sib = heading.nextElementSibling;
        while (sib && !/^H[1-3]$/.test(sib.tagName)) {{
          text += sib.textContent + ' ';
          sib = sib.nextElementSibling;
        }}
        text = text.replace(/\\s+/g, ' ').trim();
        searchIndex.push({{
          id,
          chapterTitle,
          heading: heading.textContent.trim(),
          text,
          el: heading
        }});
      }});
    }});
    console.log('Search index built:', searchIndex.length, 'entries');
  }}

  function openSearch() {{
    buildIndex();
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    input.value = '';
    resultsEl.innerHTML = '<div class="search-empty">Type to search across all chapters and platform profiles.</div>';
    activeIdx = -1;
    setTimeout(() => input.focus(), 50);
  }}

  function closeSearch() {{
    overlay.classList.remove('open');
    document.body.style.overflow = '';
    activeIdx = -1;
  }}

  function escapeHtml(str) {{
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }}

  function highlightMatch(text, terms) {{
    let result = escapeHtml(text);
    terms.forEach(t => {{
      if (t.length < 2) return;
      const re = new RegExp('(' + t.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&') + ')', 'gi');
      result = result.replace(re, '<mark>$1</mark>');
    }});
    return result;
  }}

  function getSnippet(text, terms, maxLen) {{
    maxLen = maxLen || 160;
    const lower = text.toLowerCase();
    let bestPos = 0;
    let bestScore = -1;
    // Find the position with the most term density
    for (let i = 0; i < lower.length - 20; i += 10) {{
      const window = lower.substring(i, i + maxLen);
      let score = 0;
      terms.forEach(t => {{
        let idx = 0;
        while ((idx = window.indexOf(t, idx)) !== -1) {{
          score++;
          idx += t.length;
        }}
      }});
      if (score > bestScore) {{
        bestScore = score;
        bestPos = i;
      }}
    }}
    // Snap to word boundary
    if (bestPos > 0) {{
      const space = text.lastIndexOf(' ', bestPos + 10);
      if (space > bestPos - 20) bestPos = space + 1;
    }}
    let snippet = text.substring(bestPos, bestPos + maxLen);
    if (bestPos > 0) snippet = '…' + snippet;
    if (bestPos + maxLen < text.length) snippet += '…';
    return snippet;
  }}

  function doSearch(query) {{
    if (!query || query.length < 2) {{
      resultsEl.innerHTML = '<div class="search-empty">Type to search across all chapters and platform profiles.</div>';
      activeIdx = -1;
      return;
    }}

    const terms = query.toLowerCase().split(/\\s+/).filter(t => t.length >= 2);
    if (terms.length === 0) return;

    // Score each entry
    const scored = searchIndex.map(entry => {{
      const lower = entry.text.toLowerCase();
      const headingLower = entry.heading.toLowerCase();
      let score = 0;
      terms.forEach(t => {{
        // Heading match worth 10x
        if (headingLower.includes(t)) score += 10;
        // Body matches
        let idx = 0;
        while ((idx = lower.indexOf(t, idx)) !== -1) {{
          score++;
          idx += t.length;
        }}
      }});
      // Bonus for all terms present
      const allPresent = terms.every(t => lower.includes(t) || headingLower.includes(t));
      if (allPresent) score *= 2;
      return {{ ...entry, score }};
    }}).filter(e => e.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 25);

    if (scored.length === 0) {{
      resultsEl.innerHTML = '<div class="search-empty">No results for &ldquo;' + escapeHtml(query) + '&rdquo;</div>';
      activeIdx = -1;
      return;
    }}

    let html = '<div class="search-count">' + scored.length + ' result' + (scored.length === 1 ? '' : 's') + '</div>';
    scored.forEach((entry, i) => {{
      const snippet = getSnippet(entry.text, terms);
      html += '<a class="search-result" data-idx="' + i + '" data-id="' + entry.id + '">';
      html += '<div class="search-result-chapter">' + escapeHtml(entry.chapterTitle) + '</div>';
      html += '<div class="search-result-heading">' + highlightMatch(entry.heading, terms) + '</div>';
      html += '<div class="search-result-snippet">' + highlightMatch(snippet, terms) + '</div>';
      html += '</a>';
    }});
    resultsEl.innerHTML = html;
    activeIdx = -1;

    // Store entries for navigation
    resultsEl._scored = scored;

    // Click handlers
    resultsEl.querySelectorAll('.search-result').forEach(el => {{
      el.addEventListener('click', (e) => {{
        e.preventDefault();
        const idx = parseInt(el.dataset.idx);
        jumpToResult(idx);
      }});
    }});
  }}

  function jumpToResult(idx) {{
    const scored = resultsEl._scored;
    if (!scored || !scored[idx]) return;
    closeSearch();
    const entry = scored[idx];
    // Scroll to the heading element
    entry.el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    // Flash highlight
    entry.el.style.transition = 'background 0.3s';
    entry.el.style.background = 'rgba(34, 211, 238, 0.1)';
    entry.el.style.borderRadius = '4px';
    setTimeout(() => {{
      entry.el.style.background = '';
      setTimeout(() => entry.el.style.transition = '', 300);
    }}, 1500);
  }}

  function setActive(idx) {{
    const items = resultsEl.querySelectorAll('.search-result');
    items.forEach(el => el.classList.remove('active'));
    if (idx >= 0 && idx < items.length) {{
      items[idx].classList.add('active');
      items[idx].scrollIntoView({{ block: 'nearest' }});
    }}
    activeIdx = idx;
  }}

  // Event: trigger buttons
  trigger.addEventListener('click', openSearch);

  // Event: Cmd/Ctrl+K
  document.addEventListener('keydown', (e) => {{
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {{
      e.preventDefault();
      if (overlay.classList.contains('open')) closeSearch();
      else openSearch();
    }}
  }});

  // Event: Escape
  document.addEventListener('keydown', (e) => {{
    if (e.key === 'Escape' && overlay.classList.contains('open')) {{
      closeSearch();
    }}
  }});

  // Event: click backdrop
  overlay.addEventListener('click', (e) => {{
    if (e.target === overlay) closeSearch();
  }});

  // Event: typing
  let debounce;
  input.addEventListener('input', () => {{
    clearTimeout(debounce);
    debounce = setTimeout(() => doSearch(input.value.trim()), 80);
  }});

  // Event: arrow keys + enter
  input.addEventListener('keydown', (e) => {{
    const items = resultsEl.querySelectorAll('.search-result');
    if (e.key === 'ArrowDown') {{
      e.preventDefault();
      setActive(Math.min(activeIdx + 1, items.length - 1));
    }} else if (e.key === 'ArrowUp') {{
      e.preventDefault();
      setActive(Math.max(activeIdx - 1, 0));
    }} else if (e.key === 'Enter' && activeIdx >= 0) {{
      e.preventDefault();
      jumpToResult(activeIdx);
    }}
  }});
}})();
</script>

</body>
</html>"""

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    # robots.txt
    robots_path = os.path.join(output_dir, "robots.txt")
    with open(robots_path, "w") as f:
        f.write("User-agent: *\nDisallow:\nSitemap: https://nvmilldoitmyself.com/\n")

    print(f"\n  Output: {output_path}")
    print(f"  Size: {os.path.getsize(output_path):,} bytes")
    print("  Done.")



if __name__ == "__main__":
    # Resolve paths relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = script_dir  # chapters are in subdirs of repo root
    output_dir = os.path.join(script_dir, "site")
    build_site(base_dir, output_dir)
