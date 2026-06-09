#!/usr/bin/env python3
"""Generate the 'Levels of Drone Autonomy' chart as a self-contained SVG.
Dark theme matches the handbook (build.py CSS palette). No external fonts/assets
so it renders both inline in the single-page site and standalone on GitHub.
Kept as the canonical source for the chart; re-run to regenerate the SVG."""

from html import escape

# ── palette (mirrors build.py :root) ─────────────────────────────────────────
BG       = "#0a0b10"
PANEL    = "#12131e"
ELEV     = "#161824"
BORDER   = "#1e2030"
BORDER_B = "#2a2d42"
TEXT     = "#c8cad0"
TEXT_BR  = "#e8eaef"
TEXT_DIM = "#7e8294"
LABELBG  = "#0d0e16"

# per-level accent colors (red → gold ladder)
LEVELS = [
    ("Level 0",  "No\nAutonomy",        "#ff3b5c"),
    ("Level 1",  "Pilot\nAssist",       "#e0408f"),
    ("Level 2",  "Partial\nAutonomy",   "#8b5cf6"),
    ("Level 3",  "Conditional\nAutonomy","#00a3ff"),
    ("Level 4A", "High\nAutonomy",      "#06b6d4"),
    ("Level 4B", "High\nAutonomy",      "#14b8a6"),
    ("Level 4C", "High\nAutonomy",      "#22c55e"),
    ("Level 5",  "Full\nAutonomy",      "#f59e0b"),
]

# ── row content (one string per level; \n forces a hard line break) ──────────
ROWS = [
    ("What the\noperator does", [
        "100% manual\nstick input",
        "Flies; system\nholds attitude",
        "Flies; activates\nposition hold",
        "Sets waypoints /\nPOIs, ready to fly",
        "Sets area of\ninterest",
        "Sets area of\ninterest",
        "Sets area of\ninterest",
        "Sets the\nobjective only",
    ]),
    ("What the\nsystem does", [
        "Nothing\n(rate damping)",
        "Attitude &\naltitude hold",
        "Hold 3D position;\nsense walls",
        "Fly mission in set\nconditions; avoid",
        "Self-navigate\nGPS-denied; 3D map",
        "+ reason about\nobstacle type",
        "+ reason about\nmission objective",
        "Operate in all\nconditions",
    ]),
    ("Response to\nobstacles", [
        "None",
        "None",
        "Sense & Warn",
        "Sense & Avoid",
        "Sense & Navigate\n(geometric)",
        "Sense & Navigate\n(semantic)",
        "Sense & Navigate\n(semantic)",
        "Full",
    ]),
    ("World\nunderstanding", [
        "None",
        "Orientation\n& altitude",
        "Local\nposition",
        "Basic obstacle\ngeometry",
        "3D map from\nonboard sensors",
        "Classifies obstacles\n(dust vs solid)",
        "Reasons about\nobjects / people",
        "Full\nunderstanding",
    ]),
    ("ODD\n(where it's valid)", [
        "VLOS, benign,\nskilled pilot",
        "VLOS, light wind,\nGPS optional",
        "GPS or flow;\nlow clutter",
        "Mapped area, good\nvisibility, geofence",
        "GPS-denied, dark,\nsubterranean OK",
        "+ light DVE (dust,\nfog); cluttered",
        "+ smoke / heavy\nDVE; dynamic indoor",
        "Any\n(not yet reached)",
    ]),
    ("Fallback /\nminimal-risk", [
        "Pilot only — no\nauto recovery",
        "Level & hold;\npilot recovers",
        "Pos-hold / RTL;\nland on flow loss",
        "RTL or hold on\nlink loss; geofence",
        "Continue link-denied;\nhold on SLAM loss",
        "Degrade to geometric\nif unsure",
        "Abort-to-safe +\nreport on doubt",
        "Self-resolves\n(target state)",
    ]),
    ("HARDWARE MINIMUM\n(current tech)", [
        "Betaflight F4/F7\nFC (SpeedyBee\nF405); gyro only",
        "FC w/ IMU + baro\n(Matek/SpeedyBee\nF7); ANGLE mode",
        "Pixhawk 6C / Cube\nOrange + GPS (M10)\nOR flow + rangefinder",
        "+ RPi 5 / Jetson\nOrin Nano + 2D LiDAR\n(RPLiDAR) or stereo",
        "Jetson Orin NX 16GB\n+ 3D LiDAR (Livox\nMid-360) + FAST-LIO2",
        "Jetson AGX Orin +\nmulti-return LiDAR /\nradar + thermal",
        "AGX Orin 64GB +\nLWIR (FLIR Boson+)\n+ RGB + LiDAR + VLM",
        "No hardware\nsuffices today —\nopen research",
    ]),
    ("Example\nplatform", [
        "Acro FPV\nfreestyle quad",
        "DJI Neo /\nentry hover drone",
        "DJI Mini / Mavic\n(GPS loiter)",
        "DJI Mavic 3 (APAS),\nSkydio 2+",
        "Skydio X10, Exyn\nExynAero, Emesent\nHovermap ST-X",
        "Skydio X10\n(semantic), Exyn 4B",
        "Exyn 4C (research),\nPrismo APB target",
        "None — industry\nasymptote",
    ]),
]

# ── geometry ─────────────────────────────────────────────────────────────────
LABEL_W = 196
COL_W   = 176
PAD_X   = 24
PAD_TOP = 22

TITLE_H = 58
HEAD_H  = 76
# per-row heights (hardware row is taller — 3 lines)
ROW_H = [62, 62, 50, 56, 62, 62, 82, 70]

NCOL = len(LEVELS)
W = PAD_X*2 + LABEL_W + COL_W*NCOL
H = PAD_TOP + TITLE_H + HEAD_H + sum(ROW_H) + 46  # +footer

FONT = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,"
        "sans-serif")
MONO = "'JetBrains Mono','Fira Code',ui-monospace,monospace"


def lines(s):
    return s.split("\n")


def text_block(cx, cy, s, *, fill, size, weight="400", anchor="middle",
               lh=None, family=FONT, spacing="0"):
    ls = lines(s)
    lh = lh or (size + 4)
    total = (len(ls) - 1) * lh
    y0 = cy - total / 2
    out = [f'<text x="{cx:.1f}" y="{y0:.1f}" text-anchor="{anchor}" '
           f'font-family="{family}" font-size="{size}" font-weight="{weight}" '
           f'letter-spacing="{spacing}" fill="{fill}">']
    for i, ln in enumerate(ls):
        dy = 0 if i == 0 else lh
        out.append(f'<tspan x="{cx:.1f}" dy="{dy:.1f}">{escape(ln)}</tspan>')
    out.append("</text>")
    return "".join(out)


def rrect(x, y, w, h, r, fill, stroke=None, sw=1, opacity=None):
    s = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
         f'rx="{r}" ry="{r}" fill="{fill}"')
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    if opacity is not None:
        s += f' fill-opacity="{opacity}"'
    return s + "/>"


def build():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}" height="{H}" font-family="{FONT}" '
         f'style="max-width:100%;height:auto;display:block;margin:0 auto" '
         f'role="img" aria-label="Levels of Drone Autonomy chart">']
    # bg
    p.append(rrect(0, 0, W, H, 0, BG))

    x0 = PAD_X
    y = PAD_TOP

    # ── title ──
    p.append(text_block(x0 + 4, y + 22, "Levels of Drone Autonomy",
                        fill=TEXT_BR, size=26, weight="700", anchor="start",
                        spacing="0.5"))
    p.append(text_block(x0 + 4, y + 44,
                        "Drone Integration Handbook  ·  v1.0  ·  hardware "
                        "minimums reflect fielded 2026 technology",
                        fill=TEXT_DIM, size=12, weight="400", anchor="start"))
    # cumulative note (right aligned)
    p.append(f'<text x="{W-PAD_X:.1f}" y="{y+30:.1f}" text-anchor="end" '
             f'font-family="{MONO}" font-size="11" fill="{TEXT_DIM}">'
             f'each level includes all capabilities below it</text>')

    y += TITLE_H

    # column x helper
    def col_x(i):
        return x0 + LABEL_W + i * COL_W

    # ── header row (level chips) ──
    for i, (name, sub, color) in enumerate(LEVELS):
        cx = col_x(i)
        p.append(rrect(cx + 3, y + 3, COL_W - 6, HEAD_H - 6, 8, color))
        p.append(text_block(cx + COL_W/2, y + 26, name,
                            fill="#0a0b10", size=17, weight="700"))
        p.append(text_block(cx + COL_W/2, y + 52, sub.replace("\n", " "),
                            fill="#0a0b10", size=11, weight="600"))
    # "pilot is flying" vs "operator is not" band labels above? put small tags
    y += HEAD_H

    # in-loop / out-of-loop divider marker between L2 (idx2) and L3 (idx3)
    div_x = col_x(3)
    body_top = y
    body_bot = y + sum(ROW_H)

    # ── rows ──
    ry = y
    for r, (label, cells) in enumerate(ROWS):
        rh = ROW_H[r]
        hw = (label.startswith("HARDWARE"))
        # label cell
        p.append(rrect(x0 + 3, ry + 2, LABEL_W - 6, rh - 4, 6,
                       ELEV if hw else LABELBG,
                       stroke=BORDER_B if hw else BORDER, sw=1))
        p.append(text_block(x0 + LABEL_W/2, ry + rh/2, label,
                            fill=(TEXT_BR if hw else TEXT_DIM),
                            size=(12 if hw else 12),
                            weight=("700" if hw else "600"),
                            family=(MONO if hw else FONT), lh=15))
        # data cells
        for i, (name, sub, color) in enumerate(LEVELS):
            cx = col_x(i)
            base = PANEL if (r % 2 == 0) else "#14151f"
            if hw:
                base = ELEV
            p.append(rrect(cx + 3, ry + 2, COL_W - 6, rh - 4, 6, base,
                           stroke=BORDER, sw=1))
            # tiny accent tab on hardware row
            if hw:
                p.append(rrect(cx + 3, ry + 2, 4, rh - 4, 2, color))
            p.append(text_block(cx + COL_W/2, ry + rh/2, cells[i],
                                fill=(TEXT_BR if hw else TEXT),
                                size=(11 if hw else 11),
                                weight=("600" if hw else "400"),
                                family=(MONO if hw else FONT), lh=14))
        ry += rh

    # ── in-loop / out-of-loop divider line across body ──
    p.append(f'<line x1="{div_x:.1f}" y1="{body_top-HEAD_H+6:.1f}" '
             f'x2="{div_x:.1f}" y2="{body_bot:.1f}" stroke="{TEXT_BR}" '
             f'stroke-width="2" stroke-dasharray="2 4" opacity="0.5"/>')
    p.append(f'<text x="{col_x(0):.1f}" y="{body_top-HEAD_H-1:.1f}" '
             f'font-family="{MONO}" font-size="10" fill="{TEXT_DIM}" '
             f'text-anchor="start">◂ pilot IS flying</text>')
    p.append(f'<text x="{div_x+6:.1f}" y="{body_top-HEAD_H-1:.1f}" '
             f'font-family="{MONO}" font-size="10" fill="{TEXT_DIM}" '
             f'text-anchor="start">operator is NOT flying ▸</text>')

    # ── footer ──
    fy = ry + 26
    p.append(f'<text x="{x0+4:.1f}" y="{fy:.1f}" font-family="{MONO}" '
             f'font-size="10" fill="{TEXT_DIM}" text-anchor="start">'
             f'Structure adapted from SAE J3016 and the Exyn aerial-autonomy '
             f'levels. Hardware minimums are illustrative, not endorsements. '
             f'CC BY-SA 4.0.</text>')

    p.append("</svg>")
    return "".join(p)


if __name__ == "__main__":
    import sys
    svg = build()
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/autonomy.svg"
    with open(out, "w") as f:
        f.write(svg)
    print(f"wrote {out} ({len(svg)} bytes, {W}x{H})")
