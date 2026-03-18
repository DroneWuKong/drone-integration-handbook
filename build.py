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
]

PLATFORM_PARTS = [
    ("COTS", [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114]),
    ("NDAA / Blue UAS", [201, 202, 203, 204, 205, 206, 207]),
    ("Open-Source / Custom", [301, 302]),
    ("Tactical / Defense", [401, 402, 403, 404, 405, 406, 407]),
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
    <a href="https://github.com/DroneWuKong/drone-integration-handbook">GitHub</a>
    <a href="https://github.com/DroneWuKong/drone-integration-handbook/blob/main/CONTRIBUTING.md">Contribute</a>
  </nav>
  <button class="menu-btn" id="menuBtn" aria-label="Menu">
    <span></span><span></span><span></span>
  </button>
</header>

<div class="mobile-menu" id="mobileMenu">
  <a href="#toc" class="mobile-menu-link">Contents</a>
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


if __name__ == "__main__":
    # Resolve paths relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = script_dir  # chapters are in subdirs of repo root
    output_dir = os.path.join(script_dir, "site")
    build_site(base_dir, output_dir)
