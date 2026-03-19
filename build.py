#!/usr/bin/env python3
"""
Build script for The Drone Integration Handbook static site.
Combines all chapter markdown files into a single-page HTML document.
Requires: pip install markdown
"""

import os
import re
import markdown

# Chapter order and file mapping
CHAPTERS = [
    ("fundamentals/five-link-types.md", 1, "The Five Link Types"),
    ("fundamentals/frequency-bands.md", 2, "Frequency Bands & Regulatory Reality"),
    ("fundamentals/antennas.md", 3, "Antennas for People Who Aren't RF Engineers"),
    ("fundamentals/link-budgets.md", 4, "Link Budgets Without the Math"),
    ("firmware/four-firmwares.md", 5, "The Four Firmwares"),
    ("firmware/msp-protocol.md", 6, "MSP Protocol"),
    ("firmware/mavlink-protocol.md", 7, "MAVLink Protocol"),
    ("firmware/uart-layout.md", 8, "UART Layout and Why It Matters"),
    ("field/preflight.md", 9, "Pre-Flight Checklist That Actually Works"),
    ("field/blackbox.md", 10, "Blackbox Logs"),
    ("field/pid-tuning.md", 11, "PID Tuning for People Who Fly"),
    ("field/troubleshooting.md", 12, "When Things Go Wrong"),
    ("integration/companion.md", 13, "Adding a Companion Computer"),
    ("integration/mesh-radios.md", 14, "Mesh Radios for Multi-Vehicle"),
    ("integration/tak.md", 15, "TAK Integration"),
]

PLATFORMS = [
    ("platforms/cots/dji-m350-rtk.md", 101, "DJI Matrice 350 RTK"),
    ("platforms/cots/dji-m30t.md", 102, "DJI Matrice 30T"),
    ("platforms/cots/dji-mavic4-pro.md", 103, "DJI Mavic 4 Pro"),
    ("platforms/cots/autel-evo-max-4t.md", 104, "Autel EVO MAX 4T V2"),
    ("platforms/cots/autel-evo2-enterprise.md", 105, "Autel EVO II Enterprise V3"),
    ("platforms/cots/dji-agras-t50.md", 106, "DJI Agras T50"),
    ("platforms/cots/dji-flycart-30.md", 107, "DJI FlyCart 30"),
    ("platforms/cots/flyability-elios-3.md", 108, "Flyability Elios 3"),
    ("platforms/cots/xag-p100-p150.md", 109, "XAG P100 Pro / P150"),
    ("platforms/cots/hylio-ag-272.md", 110, "Hylio AG-272"),
    ("platforms/cots/sensefly-ebee-x.md", 111, "senseFly eBee X"),
    ("platforms/cots/quantum-trinity-pro.md", 112, "Quantum Systems Trinity Pro"),
    ("platforms/cots/dji-mavic3-enterprise.md", 113, "DJI Mavic 3 Enterprise"),
    ("platforms/cots/dji-matrice-4.md", 114, "DJI Matrice 4 Series"),
    ("platforms/blue-uas/skydio-x10.md", 201, "Skydio X10 / X10D"),
    ("platforms/blue-uas/freefly-astro.md", 202, "Freefly Astro"),
    ("platforms/blue-uas/inspired-flight-if1200a.md", 203, "Inspired Flight IF1200A"),
    ("platforms/blue-uas/teal-2.md", 204, "Teal 2"),
    ("platforms/blue-uas/parrot-anafi-usa.md", 205, "Parrot ANAFI USA"),
    ("platforms/blue-uas/wingtra-wingtraone.md", 206, "WingtraOne / WingtraRAY"),
    ("platforms/blue-uas/ascent-aerosystems.md", 207, "Ascent Aerosystems"),
    ("platforms/open-source/holybro-x500-pixhawk6x.md", 301, "Holybro X500 V2 + Pixhawk 6X"),
    ("platforms/open-source/ardupilot-px4-reference.md", 302, "ArduPilot / PX4 General Reference"),
    ("platforms/tactical/anduril-ghost-x.md", 401, "Anduril Ghost X"),
    ("platforms/tactical/teal-black-widow.md", 402, "Teal Black Widow"),
    ("platforms/tactical/skyfish-osprey.md", 403, "Skyfish Osprey"),
    ("platforms/tactical/sifly-q12.md", 404, "SiFly Q12"),
    ("platforms/tactical/hoverfly-livesky.md", 405, "Hoverfly LiveSky / Spectre"),
    ("platforms/tactical/shield-ai-nova-2.md", 406, "Shield AI Nova 2"),
    ("platforms/tactical/neros-archer.md", 407, "Neros Archer"),
    ("platforms/tactical/modalai-fpv.md", 408, "ModalAI Seeker / Stinger"),
    ("platforms/tactical/red-cat-fang.md", 409, "Red Cat FANG F7"),
    ("platforms/tactical/skycutter-shrike.md", 410, "Skycutter Shrike 10"),
    ("platforms/tactical/vantage-robotics.md", 411, "Vantage Robotics Vesper / Trace"),
]

PLATFORM_PARTS = [
    ("COTS", [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114]),
    ("NDAA / Blue UAS", [201, 202, 203, 204, 205, 206, 207]),
    ("Open-Source / Custom", [301, 302]),
    ("Tactical / Defense", [401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411]),
]

PARTS = [
    ("Part 1 — RF Fundamentals", [1, 2, 3, 4]),
    ("Part 2 — Flight Controller Firmware", [5, 6, 7, 8]),
    ("Part 3 — Field Operations", [9, 10, 11, 12]),
    ("Part 4 — Integration", [13, 14, 15]),
]


def read_chapter(filepath):
    """Read a chapter markdown file."""
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def fix_internal_links(html_content, ch_num):
    """Convert inter-chapter markdown links to anchor links."""
    # Replace links like (../fundamentals/five-link-types.md) with (#ch1)
    for filepath, num, title in CHAPTERS:
        basename = os.path.basename(filepath)
        # Handle various relative path patterns
        html_content = html_content.replace(f"({basename})", f"(#ch{num})")
        html_content = html_content.replace(f"(../{filepath})", f"(#ch{num})")
        html_content = html_content.replace(f"({filepath})", f"(#ch{num})")
        # Handle patterns like (02-frequency-bands.md)
        html_content = html_content.replace(
            f"({os.path.basename(filepath)})", f"(#ch{num})"
        )
    return html_content


def md_to_html(md_text):
    """Convert markdown to HTML."""
    return markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "codehilite", "toc"],
        extension_configs={"codehilite": {"css_class": "code"}},
    )


def build_toc():
    """Build the table of contents HTML."""
    toc = ""
    for part_name, ch_nums in PARTS:
        toc += f'<div class="toc-part"><h3>{part_name}</h3>\n'
        for num in ch_nums:
            for filepath, ch_num, title in CHAPTERS:
                if ch_num == num:
                    toc += f'<a href="#ch{num}"><span class="ch-num">{num}</span>{title}</a>\n'
        toc += "</div>\n"
    # Platform profiles
    toc += '<div class="toc-part"><h3>Part 5 — Platform References</h3>\n'
    for cat_name, p_nums in PLATFORM_PARTS:
        toc += f'<span style="display:block;color:var(--accent-dim);font-size:0.8rem;margin:0.5rem 0 0.2rem 0;">{cat_name}</span>\n'
        for num in p_nums:
            for filepath, p_num, title in PLATFORMS:
                if p_num == num:
                    toc += f'<a href="#p{num}"><span class="ch-num">&bull;</span>{title}</a>\n'
    toc += "</div>\n"
    return toc


def build_chapters(base_dir):
    """Build all chapter HTML content."""
    chapters_html = ""
    for filepath, ch_num, title in CHAPTERS:
        full_path = os.path.join(base_dir, filepath)
        md_content = read_chapter(full_path)
        if not md_content:
            print(f"  WARNING: Missing {filepath}")
            continue

        # Convert markdown to HTML
        html_content = md_to_html(md_content)

        # Fix internal cross-references
        html_content = fix_internal_links(html_content, ch_num)

        # Wrap in chapter div with anchor
        chapters_html += f'<section class="chapter" id="ch{ch_num}">\n'
        chapters_html += html_content
        chapters_html += "\n</section>\n\n"
        print(f"  Built chapter {ch_num}: {title}")

    return chapters_html


def build_platforms(base_dir):
    """Build all platform profile HTML content."""
    platforms_html = '<section class="chapter" id="platforms"><h1>Part 5 — Platform References</h1>'
    platforms_html += '<p><em>Full integration profiles — RF links, firmware, payloads, SDKs, and gotchas. Vetted parts only.</em></p></section>\n'
    for filepath, p_num, title in PLATFORMS:
        full_path = os.path.join(base_dir, filepath)
        md_content = read_chapter(full_path)
        if not md_content:
            print(f"  WARNING: Missing {filepath}")
            continue
        html_content = md_to_html(md_content)
        platforms_html += f'<section class="chapter" id="p{p_num}">\n'
        platforms_html += html_content
        platforms_html += "\n</section>\n\n"
        print(f"  Built platform: {title}")
    return platforms_html


def build_site(base_dir, output_dir):
    """Build the complete single-page HTML site."""
    print("Building The Drone Integration Handbook...")

    toc = build_toc()
    chapters = build_chapters(base_dir)
    platforms = build_platforms(base_dir)

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
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #0a0a0a;
  --bg-surface: #111111;
  --bg-elevated: #1a1a1a;
  --text: #d4d4d4;
  --text-dim: #737373;
  --text-bright: #e5e5e5;
  --accent: #22d3ee;
  --accent-dim: #0e7490;
  --border: #262626;
  --border-bright: #404040;
  --code-bg: #0d1117;
  --success: #4ade80;
  --warn: #fbbf24;
  --mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
  --serif: 'Source Serif 4', 'Georgia', serif;
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
  font-family: var(--serif);
  font-size: 17px;
  line-height: 1.7;
  color: var(--text);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
}}

/* ── HEADER ── */
.site-header {{
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(10, 10, 10, 0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 0.75rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}}

.site-header .logo {{
  font-family: var(--mono);
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}}

.site-header .logo span {{
  color: var(--text-dim);
  font-weight: 400;
}}

.site-header .nav-desktop a {{
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--text-dim);
  text-decoration: none;
  margin-left: 1.5rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  transition: color 0.2s;
}}

.site-header .nav-desktop a:hover {{
  color: var(--accent);
}}

/* ── HERO ── */
.hero {{
  max-width: 860px;
  margin: 0 auto;
  padding: 6rem 2rem 4rem;
  text-align: center;
}}

.hero h1 {{
  font-family: var(--mono);
  font-size: clamp(1.6rem, 4vw, 2.4rem);
  font-weight: 700;
  color: var(--text-bright);
  letter-spacing: -0.02em;
  margin-bottom: 0.5rem;
}}

.hero h1::before {{
  content: '// ';
  color: var(--accent-dim);
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
}}

.toc-part h3 {{
  font-family: var(--mono);
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--accent-dim);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}}

.toc-part a {{
  display: flex;
  align-items: baseline;
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
  font-family: var(--mono);
  font-size: clamp(1.3rem, 3vw, 1.8rem);
  font-weight: 700;
  color: var(--text-bright);
  margin-bottom: 0.5rem;
  letter-spacing: -0.01em;
}}

.chapter h2 {{
  font-family: var(--mono);
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--accent);
  margin: 2.5rem 0 1rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--border);
}}

.chapter h3 {{
  font-family: var(--mono);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-bright);
  margin: 2rem 0 0.75rem;
}}

.chapter h4 {{
  font-family: var(--mono);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-dim);
  margin: 1.5rem 0 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
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

/* ── HAMBURGER BUTTON ── */
.menu-btn {{
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  z-index: 200;
}}

.menu-btn span {{
  display: block;
  width: 20px;
  height: 2px;
  background: var(--text-dim);
  margin: 4px 0;
  transition: transform 0.25s, opacity 0.25s;
}}

.menu-btn.active span:nth-child(1) {{
  transform: rotate(45deg) translate(4px, 4px);
  background: var(--accent);
}}

.menu-btn.active span:nth-child(2) {{
  opacity: 0;
}}

.menu-btn.active span:nth-child(3) {{
  transform: rotate(-45deg) translate(4px, -4px);
  background: var(--accent);
}}

/* ── MOBILE MENU ── */
.mobile-menu {{
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 150;
  background: rgba(10, 10, 10, 0.97);
  backdrop-filter: blur(16px);
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}}

.mobile-menu.open {{
  display: flex;
}}

.mobile-menu-link {{
  font-family: var(--mono);
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--text);
  text-decoration: none;
  padding: 1rem 2rem;
  letter-spacing: 0.04em;
  border-bottom: 1px solid var(--border);
  width: 80%;
  text-align: center;
  transition: color 0.2s;
}}

.mobile-menu-link:last-child {{
  border-bottom: none;
}}

.mobile-menu-link:hover,
.mobile-menu-link:active {{
  color: var(--accent);
}}

/* ── RESPONSIVE ── */
@media (max-width: 600px) {{
  body {{ font-size: 15px; }}
  .hero {{ padding: 4rem 1.25rem 3rem; }}
  .toc, .content {{ padding-left: 1.25rem; padding-right: 1.25rem; }}
  .site-header {{ padding: 0.75rem 1.25rem; }}
  .nav-desktop {{ display: none; }}
  .menu-btn {{ display: block; }}
  .chapter pre {{ padding: 1rem; }}
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

<header class="site-header">
  <div class="logo">DRONE INTEGRATION HANDBOOK <span>v1.0</span></div>
  <nav class="nav-desktop">
    <a href="#toc">Contents</a>
    <a href="forge.html">Forge</a>
    <a href="https://github.com/DroneWuKong/drone-integration-handbook">GitHub</a>
    <a href="https://github.com/DroneWuKong/drone-integration-handbook/blob/main/CONTRIBUTING.md">Contribute</a>
  </nav>
  <button class="menu-btn" id="menuBtn" aria-label="Menu">
    <span></span><span></span><span></span>
  </button>
</header>

<div class="mobile-menu" id="mobileMenu">
  <a href="#toc" class="mobile-menu-link">Contents</a>
  <a href="forge.html" class="mobile-menu-link">Forge</a>
  <a href="https://github.com/DroneWuKong/drone-integration-handbook" class="mobile-menu-link">GitHub</a>
  <a href="https://github.com/DroneWuKong/drone-integration-handbook/blob/main/CONTRIBUTING.md" class="mobile-menu-link">Contribute</a>
  <a href="https://github.com/DroneWuKong/drone-integration-handbook/blob/main/ROADMAP.md" class="mobile-menu-link">Roadmap</a>
</div>

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
{platforms}
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

<script>
// Back to top button
const btt = document.getElementById('btt');
window.addEventListener('scroll', () => {{
  btt.classList.toggle('visible', window.scrollY > 600);
}});

// Mobile menu
const menuBtn = document.getElementById('menuBtn');
const mobileMenu = document.getElementById('mobileMenu');

menuBtn.addEventListener('click', () => {{
  menuBtn.classList.toggle('active');
  mobileMenu.classList.toggle('open');
  document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
}});

// Close menu when a link is tapped
mobileMenu.querySelectorAll('a').forEach(link => {{
  link.addEventListener('click', () => {{
    menuBtn.classList.remove('active');
    mobileMenu.classList.remove('open');
    document.body.style.overflow = '';
  }});
}});
</script>

</body>
</html>"""

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n  Output: {output_path}")
    print(f"  Size: {os.path.getsize(output_path):,} bytes")
    print("  Done.")


def build_forge_dashboard(base_dir, output_dir):
    """Build the Forge Mission Control dashboard page."""
    import json
    import glob

    print("\nBuilding Forge Mission Control dashboard...")

    parts_db_dir = os.path.join(base_dir, "data", "parts-db")

    # ── Load all data ──
    def load_json(filename):
        path = os.path.join(parts_db_dir, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    drone_models = load_json("drone_models.json")
    build_guides = load_json("build_guides.json")

    # Count JSON category files
    json_files = sorted(glob.glob(os.path.join(parts_db_dir, "*.json")))
    categories = {}
    total_parts = 0
    for jf in json_files:
        fname = os.path.basename(jf)
        cat_name = fname.replace(".json", "").replace("_", " ").title()
        with open(jf, "r", encoding="utf-8") as f:
            data = json.load(f)
        count = len(data) if isinstance(data, list) else 0
        categories[cat_name] = count
        total_parts += count

    # Count platform markdown profiles
    platforms_dir = os.path.join(base_dir, "platforms")
    platform_count = 0
    platform_categories = {}
    if os.path.isdir(platforms_dir):
        for subdir in sorted(os.listdir(platforms_dir)):
            subpath = os.path.join(platforms_dir, subdir)
            if os.path.isdir(subpath):
                md_files = [f for f in os.listdir(subpath) if f.endswith(".md")]
                platform_categories[subdir] = len(md_files)
                platform_count += len(md_files)

    # Count handbook chapters
    chapter_count = len(CHAPTERS)

    # ── Build drone models table rows ──
    model_rows = ""
    for m in drone_models:
        pid = m.get("pid", "")
        name = m.get("name", "")
        build_class = m.get("build_class", "").replace("_", " ").title()
        mfr = m.get("manufacturer", "—")
        vtype = m.get("vehicle_type", "—")
        ndaa = m.get("ndaa_compliant", None)
        blue = m.get("blue_uas", None)

        # Status badges
        badges = ""
        if ndaa is True:
            badges += '<span class="badge badge-green">NDAA</span> '
        elif ndaa is False:
            badges += '<span class="badge badge-red">!NDAA</span> '
        if blue is True:
            badges += '<span class="badge badge-blue">Blue UAS</span>'

        model_rows += f"""<tr>
          <td class="cell-mono">{pid}</td>
          <td>{name}</td>
          <td>{build_class}</td>
          <td>{mfr}</td>
          <td>{badges}</td>
        </tr>\n"""

    # ── Build category cards ──
    cat_cards = ""
    for cat_name, count in sorted(categories.items()):
        cat_cards += f"""<div class="db-card">
          <div class="db-card-count">{count}</div>
          <div class="db-card-label">{cat_name}</div>
        </div>\n"""

    # ── Build platform breakdown ──
    plat_breakdown = ""
    cat_labels = {"cots": "COTS / Enterprise", "blue-uas": "NDAA / Blue UAS",
                  "open-source": "Open-Source / Custom", "tactical": "Tactical / Defense"}
    for subdir, count in platform_categories.items():
        label = cat_labels.get(subdir, subdir.replace("-", " ").title())
        plat_breakdown += f'<div class="plat-row"><span>{label}</span><span class="plat-count">{count}</span></div>\n'

    # ── Forge HTML ──
    forge_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Forge — Mission Control</title>
<meta name="description" content="Forge Mission Control — interactive dashboard for the Drone Integration Handbook parts database.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg-deep: #060a0e;
  --bg: #0a1018;
  --bg-surface: #0f1620;
  --bg-elevated: #141e2a;
  --bg-card: #111a24;
  --text: #c4d0dc;
  --text-dim: #5a6a7a;
  --text-bright: #e8eef4;
  --accent: #22d3ee;
  --accent-glow: rgba(34, 211, 238, 0.15);
  --accent-dim: #0e7490;
  --border: #1a2636;
  --border-bright: #2a3a4e;
  --green: #4ade80;
  --red: #f87171;
  --blue: #60a5fa;
  --amber: #fbbf24;
  --mono: 'JetBrains Mono', monospace;
  --sans: 'Inter', -apple-system, sans-serif;
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html {{ scroll-behavior: smooth; }}

body {{
  font-family: var(--sans);
  font-size: 14px;
  line-height: 1.5;
  color: var(--text);
  background: var(--bg-deep);
  -webkit-font-smoothing: antialiased;
  min-height: 100vh;
}}

/* ── NOISE TEXTURE ── */
body::before {{
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 0;
}}

/* ── TOP BAR ── */
.topbar {{
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(6, 10, 14, 0.88);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border);
  padding: 0 1.5rem;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}}

.topbar-left {{
  display: flex;
  align-items: center;
  gap: 0.75rem;
}}

.topbar-logo {{
  font-family: var(--mono);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}}

.topbar-logo span {{
  color: var(--text-dim);
  font-weight: 400;
  margin-left: 0.5rem;
  font-size: 0.65rem;
  letter-spacing: 0.06em;
}}

.topbar-status {{
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-family: var(--mono);
  font-size: 0.6rem;
  color: var(--green);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}}

.topbar-status::before {{
  content: '';
  width: 6px;
  height: 6px;
  background: var(--green);
  border-radius: 50%;
  box-shadow: 0 0 6px var(--green);
  animation: pulse 2s ease-in-out infinite;
}}

@keyframes pulse {{
  0%, 100% {{ opacity: 1; }}
  50% {{ opacity: 0.4; }}
}}

.topbar-nav {{
  display: flex;
  gap: 1.25rem;
}}

.topbar-nav a {{
  font-family: var(--mono);
  font-size: 0.65rem;
  color: var(--text-dim);
  text-decoration: none;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  transition: color 0.2s;
}}

.topbar-nav a:hover {{ color: var(--accent); }}

/* ── LAYOUT ── */
.forge-container {{
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
  position: relative;
  z-index: 1;
}}

.forge-header {{
  margin-bottom: 2.5rem;
}}

.forge-header h1 {{
  font-family: var(--mono);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-bright);
  letter-spacing: -0.01em;
  margin-bottom: 0.25rem;
}}

.forge-header p {{
  font-size: 0.8rem;
  color: var(--text-dim);
  max-width: 600px;
}}

.forge-credit {{
  font-family: var(--mono);
  font-size: 0.55rem;
  color: var(--text-dim);
  margin-top: 0.5rem;
  letter-spacing: 0.03em;
  opacity: 0.7;
}}

/* ── STAT CARDS ── */
.stat-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2.5rem;
}}

.stat-card {{
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.25rem 1.5rem;
  transition: border-color 0.3s, box-shadow 0.3s;
  position: relative;
  overflow: hidden;
}}

.stat-card::before {{
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--accent) 0%, transparent 100%);
  opacity: 0;
  transition: opacity 0.3s;
}}

.stat-card:hover {{
  border-color: var(--border-bright);
  box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}}

.stat-card:hover::before {{ opacity: 1; }}

.stat-number {{
  font-family: var(--mono);
  font-size: 2rem;
  font-weight: 700;
  color: var(--accent);
  line-height: 1;
  margin-bottom: 0.25rem;
}}

.stat-label {{
  font-family: var(--mono);
  font-size: 0.65rem;
  color: var(--text-dim);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}}

.stat-sub {{
  font-size: 0.7rem;
  color: var(--text-dim);
  margin-top: 0.5rem;
  font-style: italic;
}}

/* ── SECTION HEADERS ── */
.section-header {{
  font-family: var(--mono);
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--text-dim);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}}

/* ── DATABASE GRID ── */
.db-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 0.75rem;
  margin-bottom: 2.5rem;
}}

.db-card {{
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 1rem;
  text-align: center;
  transition: border-color 0.2s;
}}

.db-card:hover {{
  border-color: var(--border-bright);
}}

.db-card-count {{
  font-family: var(--mono);
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--text-bright);
}}

.db-card-label {{
  font-family: var(--mono);
  font-size: 0.6rem;
  color: var(--text-dim);
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-top: 0.25rem;
}}

/* ── PLATFORM BREAKDOWN ── */
.plat-section {{
  margin-bottom: 2.5rem;
}}

.plat-row {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0.75rem;
  border-bottom: 1px solid var(--border);
  font-size: 0.8rem;
}}

.plat-row span:first-child {{
  color: var(--text);
}}

.plat-count {{
  font-family: var(--mono);
  font-weight: 600;
  color: var(--accent);
}}

/* ── MODELS TABLE ── */
.table-wrap {{
  overflow-x: auto;
  margin-bottom: 2.5rem;
  border: 1px solid var(--border);
  border-radius: 8px;
}}

.models-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 0.78rem;
}}

.models-table thead {{
  background: var(--bg-elevated);
}}

.models-table th {{
  font-family: var(--mono);
  font-size: 0.6rem;
  font-weight: 600;
  color: var(--text-dim);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border-bright);
}}

.models-table td {{
  padding: 0.6rem 1rem;
  border-bottom: 1px solid var(--border);
  color: var(--text);
}}

.models-table tbody tr:hover {{
  background: var(--bg-surface);
}}

.cell-mono {{
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--text-dim);
}}

/* ── BADGES ── */
.badge {{
  display: inline-block;
  font-family: var(--mono);
  font-size: 0.55rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  padding: 0.15rem 0.4rem;
  border-radius: 3px;
  text-transform: uppercase;
}}

.badge-green {{ background: rgba(74,222,128,0.15); color: var(--green); }}
.badge-red {{ background: rgba(248,113,113,0.1); color: var(--red); }}
.badge-blue {{ background: rgba(96,165,250,0.15); color: var(--blue); }}

/* ── SEARCH ── */
.search-bar {{
  width: 100%;
  max-width: 400px;
  margin-bottom: 1rem;
  padding: 0.6rem 1rem;
  font-family: var(--mono);
  font-size: 0.75rem;
  color: var(--text);
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  outline: none;
  transition: border-color 0.2s;
}}

.search-bar::placeholder {{ color: var(--text-dim); }}
.search-bar:focus {{ border-color: var(--accent-dim); }}

/* ── FOOTER ── */
.forge-footer {{
  text-align: center;
  padding: 2rem 0;
  border-top: 1px solid var(--border);
  margin-top: 3rem;
}}

.forge-footer p {{
  font-family: var(--mono);
  font-size: 0.6rem;
  color: var(--text-dim);
  letter-spacing: 0.03em;
}}

.forge-footer a {{
  color: var(--accent-dim);
  text-decoration: none;
}}

.forge-footer a:hover {{ color: var(--accent); }}

/* ── RESPONSIVE ── */
@media (max-width: 768px) {{
  .topbar-nav {{ display: none; }}
  .stat-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .db-grid {{ grid-template-columns: repeat(3, 1fr); }}
  .forge-container {{ padding: 1.5rem 1rem 3rem; }}
}}

@media (max-width: 480px) {{
  .stat-grid {{ grid-template-columns: 1fr; }}
  .db-grid {{ grid-template-columns: repeat(2, 1fr); }}
}}
</style>
</head>
<body>

<div class="topbar">
  <div class="topbar-left">
    <div class="topbar-logo">FORGE<span>Mission Control</span></div>
    <div class="topbar-status">Systems Nominal</div>
  </div>
  <nav class="topbar-nav">
    <a href="index.html">Handbook</a>
    <a href="https://github.com/DroneWuKong/drone-integration-handbook">GitHub</a>
    <a href="https://github.com/DroneWuKong/drone-integration-handbook/blob/main/CONTRIBUTING.md">Contribute</a>
  </nav>
</div>

<div class="forge-container">

  <div class="forge-header">
    <h1>Mission Control</h1>
    <p>Interactive dashboard for the Drone Integration Handbook parts database. Vetted parts only.</p>
    <div class="forge-credit">Architecture: Ted Strazimiri &middot; Data: Drone Integration Handbook</div>
  </div>

  <!-- STAT CARDS -->
  <div class="stat-grid">
    <div class="stat-card">
      <div class="stat-number">{len(categories)}</div>
      <div class="stat-label">Categories</div>
      <div class="stat-sub">{total_parts:,} total parts indexed</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">{len(drone_models)}</div>
      <div class="stat-label">Drone Models</div>
      <div class="stat-sub">{len([m for m in drone_models if m.get('build_class','').startswith('enterprise') or m.get('build_class','').startswith('tactical')])} platforms + {len([m for m in drone_models if not m.get('build_class','').startswith('enterprise') and not m.get('build_class','').startswith('tactical')])} custom builds</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">{len(build_guides)}</div>
      <div class="stat-label">Build Guides</div>
      <div class="stat-sub">Step-by-step assembly &amp; config</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">{platform_count}</div>
      <div class="stat-label">Platforms</div>
      <div class="stat-sub">{len(platform_categories)} categories of integration profiles</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">{chapter_count}</div>
      <div class="stat-label">Chapters</div>
      <div class="stat-sub">Handbook reference material</div>
    </div>
  </div>

  <!-- PARTS DATABASE BREAKDOWN -->
  <div class="section-header">Parts Database</div>
  <div class="db-grid">
    {cat_cards}
  </div>

  <!-- PLATFORM BREAKDOWN -->
  <div class="section-header">Platform Profiles</div>
  <div class="plat-section">
    {plat_breakdown}
    <div class="plat-row" style="border-bottom:none;font-weight:600;">
      <span style="color:var(--text-bright);">Total</span>
      <span class="plat-count">{platform_count}</span>
    </div>
  </div>

  <!-- DRONE MODELS TABLE -->
  <div class="section-header">All Drone Models</div>
  <input type="text" class="search-bar" id="modelSearch" placeholder="Filter models...">
  <div class="table-wrap">
    <table class="models-table" id="modelsTable">
      <thead>
        <tr>
          <th>PID</th>
          <th>Model</th>
          <th>Class</th>
          <th>Manufacturer</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {model_rows}
      </tbody>
    </table>
  </div>

  <div class="forge-footer">
    <p>
      <a href="index.html">Read the Handbook</a> &middot;
      <a href="https://github.com/DroneWuKong/drone-integration-handbook">Source on GitHub</a> &middot;
      CC BY-SA 4.0
    </p>
    <p style="margin-top:0.5rem;">Built in the field. With real data. On real hardware.</p>
  </div>

</div>

<script>
// Table search/filter
const search = document.getElementById('modelSearch');
const table = document.getElementById('modelsTable');
const rows = table.querySelectorAll('tbody tr');

search.addEventListener('input', () => {{
  const q = search.value.toLowerCase();
  rows.forEach(row => {{
    const text = row.textContent.toLowerCase();
    row.style.display = text.includes(q) ? '' : 'none';
  }});
}});
</script>

</body>
</html>"""

    os.makedirs(output_dir, exist_ok=True)
    forge_path = os.path.join(output_dir, "forge.html")
    with open(forge_path, "w", encoding="utf-8") as f:
        f.write(forge_html)

    print(f"  Output: {forge_path}")
    print(f"  Size: {os.path.getsize(forge_path):,} bytes")
    print(f"  Stats: {len(categories)} categories, {len(drone_models)} models, {len(build_guides)} guides, {platform_count} platforms, {chapter_count} chapters")
    print("  Forge dashboard done.")


if __name__ == "__main__":
    # Resolve paths relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = script_dir  # chapters are in subdirs of repo root
    output_dir = os.path.join(script_dir, "site")
    build_site(base_dir, output_dir)
    build_forge_dashboard(base_dir, output_dir)
