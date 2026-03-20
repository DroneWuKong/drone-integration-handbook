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
    ("field/unsolved-problems.md", 16, "Unsolved Problems"),
]

COMPONENTS = [
    ("components/flight-controllers.md", 601, "Flight Controllers"),
    ("components/escs.md", 602, "Electronic Speed Controllers"),
    ("components/motors.md", 603, "Motors"),
    ("components/batteries.md", 604, "Batteries & Power Systems"),
    ("components/companion-computers.md", 605, "Companion Computers"),
    ("components/comms-datalinks.md", 606, "EW-Resilient Communications"),
    ("components/thermal-cameras.md", 607, "Thermal / IR Cameras"),
    ("components/counter-uas.md", 608, "Counter-UAS"),
    ("components/propulsion-non-electric.md", 609, "Non-Electric Propulsion"),
    ("components/platforms-global.md", 611, "Non-US Platforms"),
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
    ("What's Left to Solve", [16]),
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
    # Platform profiles — collapsible
    toc += '<div class="toc-part">\n'
    toc += '<details class="toc-collapse">\n'
    toc += '<summary><h3>Part 5 — Platform References</h3><span class="toc-count">' + str(len(PLATFORMS)) + ' platforms</span></summary>\n'
    for cat_name, p_nums in PLATFORM_PARTS:
        toc += f'<span style="display:block;color:var(--accent-dim);font-size:0.8rem;margin:0.5rem 0 0.2rem 0;">{cat_name}</span>\n'
        for num in p_nums:
            for filepath, p_num, title in PLATFORMS:
                if p_num == num:
                    toc += f'<a href="#p{num}"><span class="ch-num">&bull;</span>{title}</a>\n'
    toc += '</details>\n'
    toc += "</div>\n"
    # Component references — collapsible
    toc += '<div class="toc-part">\n'
    toc += '<details class="toc-collapse">\n'
    toc += '<summary><h3>Part 6 — Component References</h3><span class="toc-count">' + str(len(COMPONENTS)) + ' categories</span></summary>\n'
    for filepath, c_num, title in COMPONENTS:
        toc += f'<a href="#c{c_num}"><span class="ch-num">&bull;</span>{title}</a>\n'
    toc += '</details>\n'
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


def build_components(base_dir):
    """Build all component reference HTML content."""
    components_html = '<section class="chapter" id="components"><h1>Part 6 — Component References</h1>'
    components_html += '<p><em>Deep dives on flight controllers, ESCs, motors, batteries, companion computers, radios, sensors, and complete ecosystems. Specs that matter, gotchas that don\'t show up in datasheets.</em></p></section>\n'
    for filepath, c_num, title in COMPONENTS:
        full_path = os.path.join(base_dir, filepath)
        md_content = read_chapter(full_path)
        if not md_content:
            print(f"  WARNING: Missing {filepath}")
            continue
        html_content = md_to_html(md_content)
        components_html += f'<section class="chapter" id="c{c_num}">\n'
        components_html += html_content
        components_html += "\n</section>\n\n"
        print(f"  Built component: {title}")
    return components_html


def build_site(base_dir, output_dir):
    """Build the complete single-page HTML site."""
    print("Building The Drone Integration Handbook...")

    toc = build_toc()
    chapters = build_chapters(base_dir)
    platforms = build_platforms(base_dir)
    components = build_components(base_dir)

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

/* ── SEARCH TRIGGER ── */
.search-trigger {{
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.35rem 0.75rem;
  margin-left: 1.5rem;
  cursor: pointer;
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--text-dim);
  letter-spacing: 0.04em;
  transition: border-color 0.2s, color 0.2s;
}}

.search-trigger:hover {{
  border-color: var(--border-bright);
  color: var(--text);
}}

.search-trigger kbd {{
  font-family: var(--mono);
  font-size: 0.6rem;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 0.1rem 0.35rem;
  color: var(--text-dim);
  line-height: 1;
}}

.search-trigger svg {{
  opacity: 0.6;
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

<header class="site-header">
  <div class="logo">DRONE INTEGRATION HANDBOOK <span>v1.0</span></div>
  <nav class="nav-desktop">
    <a href="#toc">Contents</a>
    <button class="search-trigger" id="searchTrigger" aria-label="Search">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <span>Search</span>
      <kbd>&#8984;K</kbd>
    </button>
    <a href="https://forgeprole.netlify.app">Forge</a>
    <a href="https://github.com/DroneWuKong/drone-integration-handbook">GitHub</a>
    <a href="https://github.com/DroneWuKong/drone-integration-handbook/blob/main/CONTRIBUTING.md">Contribute</a>
  </nav>
  <button class="menu-btn" id="menuBtn" aria-label="Menu">
    <span></span><span></span><span></span>
  </button>
</header>

<div class="mobile-menu" id="mobileMenu">
  <a href="#" class="mobile-menu-link" id="mobileSearchLink">Search</a>
  <a href="#toc" class="mobile-menu-link">Contents</a>
  <a href="https://forgeprole.netlify.app" class="mobile-menu-link">Forge</a>
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
{components}
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

// ── MOBILE MENU ──
const menuBtn = document.getElementById('menuBtn');
const mobileMenu = document.getElementById('mobileMenu');

menuBtn.addEventListener('click', () => {{
  menuBtn.classList.toggle('active');
  mobileMenu.classList.toggle('open');
  document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
}});

mobileMenu.querySelectorAll('a').forEach(link => {{
  link.addEventListener('click', () => {{
    menuBtn.classList.remove('active');
    mobileMenu.classList.remove('open');
    document.body.style.overflow = '';
  }});
}});

// ── SEARCH ENGINE ──
(function() {{
  const overlay = document.getElementById('searchOverlay');
  const input = document.getElementById('searchInput');
  const resultsEl = document.getElementById('searchResults');
  const trigger = document.getElementById('searchTrigger');
  const mobileTrigger = document.getElementById('mobileSearchLink');
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
  mobileTrigger.addEventListener('click', (e) => {{
    e.preventDefault();
    menuBtn.classList.remove('active');
    mobileMenu.classList.remove('open');
    document.body.style.overflow = '';
    openSearch();
  }});

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

    print(f"\n  Output: {output_path}")
    print(f"  Size: {os.path.getsize(output_path):,} bytes")
    print("  Done.")



if __name__ == "__main__":
    # Resolve paths relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = script_dir  # chapters are in subdirs of repo root
    output_dir = os.path.join(script_dir, "site")
    build_site(base_dir, output_dir)
