"""Generates every static SVG in /assets (dark + light variants).
Run:  python scripts/build_assets.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from theme import *

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


def fit(text, kind, target, cap):
    """Font size so `text` is `target` wide, capped."""
    return min(cap, target / width(text, kind, 1))


# ------------------------------------------------------------------ HERO
def hero(T):
    W, H = 960, 650
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" fill="{T["bg"]}" stroke="{T["line"]}" stroke-width="2"/>']
    grid = "".join(f'<path d="M{x},2V{H-2}" />' for x in range(80, W, 80)) + \
           "".join(f'<path d="M2,{y}H{W-2}" />' for y in range(80, H, 80))
    b.append(f'<g stroke="{T["line"]}" stroke-width="1" opacity=".45">{grid}</g>')
    b.append(monogram(48, 44, 64, T))

    # statement
    for i, line in enumerate(["I build software that", "learns to see: hands,", "eyes, floor plans."]):
        b.append(f'<text x="48" y="{172+i*42}" font-family="{F_SERIF}" font-style="italic" '
                 f'font-size="32" fill="{T["ink"]}">{esc(line)}</text>')

    # three detection frames
    fx, fy, fw, fh, gap = 480, 62, 140, 170, 14
    scan_css = ("@keyframes scan{0%{transform:translateY(0)}100%{transform:translateY(" + str(fh - 4) + "px)}}"
                ".scan{animation:scan 3.2s ease-in-out infinite alternate}"
                "@keyframes flow{to{stroke-dashoffset:-32}}.flow{animation:flow 1.4s linear infinite}"
                "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}.pulse{animation:pulse 2.4s ease-in-out infinite}")
    labels = ["hand", "gaze", "route"]
    for i, lab in enumerate(labels):
        x = fx + i * (fw + gap)
        b.append(f'<rect x="{x}" y="{fy}" width="{fw}" height="{fh}" fill="{T["raised"]}"/>')
        if i == 0:
            b.append(hand(x + 20, fy + 20, fw - 40, fh - 40, T))
        elif i == 1:
            b.append(eye(x + fw / 2, fy + fh / 2, fw - 36, T))
        else:
            b.append(plan(x + 14, fy + 24, fw - 28, fh - 48, T))
        b.append(f'<rect class="scan" style="animation-delay:{i*0.9}s" x="{x}" y="{fy+2}" width="{fw}" height="2" '
                 f'fill="{T["accent"]}" opacity=".7"/>')
        b.append(brackets(x, fy, fw, fh, 22, T["accent"], 3))
        b.append(tag(x, fy, lab, T))

    b.append(f'<text x="48" y="338" font-family="{F_MONO}" font-size="17" fill="{T["dim"]}">'
             f'bca student / full-stack / ai-ml / mobile</text>')
    b.append(f'<path d="M48,356H{W-48}" stroke="{T["line"]}" stroke-width="1.5"/>')

    # name block, justified to the same measure
    meas = W - 96
    size = min(fit("MUHAMMED", "display", meas, 400), fit("HUMRAZ H.", "display", meas, 400)) * 1.0
    size = min(size, 138)
    b.append(f'<text x="48" y="{356+size*.716+28:.0f}" font-family="{F_DISPLAY}" font-weight="900" font-size="{size:.0f}" '
             f'textLength="{meas}" lengthAdjust="spacingAndGlyphs" fill="none" stroke="{T["ink"]}" '
             f'stroke-width="2.4" stroke-linejoin="round">MUHAMMED</text>')
    b.append(f'<text x="48" y="{356+size*.716*2+28+28:.0f}" font-family="{F_DISPLAY}" font-weight="900" font-size="{size:.0f}" '
             f'textLength="{meas}" lengthAdjust="spacingAndGlyphs" fill="{T["ink"]}">HUMRAZ H<tspan fill="{T["accent"]}">.</tspan></text>')
    return svg(W, H, "Muhammed Humraz H.",
               "Profile hero. Statement: I build software that learns to see: hands, eyes, floor plans. "
               "Three detection frames labelled hand, gaze and route show a hand-landmark skeleton, an eye with a gaze "
               "crosshair, and an indoor floor plan with a navigation route. Below, the name MUHAMMED HUMRAZ H. in large type.",
               "".join(b), scan_css)


# ------------------------------------------------------------------ SECTION HEADERS
def header(num, title, T):
    W, H = 960, 92
    size = 56
    b = [f'<text x="0" y="60" font-family="{F_MONO}" font-size="24" fill="{T["accent"]}">{num}</text>',
         f'<text x="64" y="64" font-family="{F_DISPLAY}" font-weight="900" font-size="{size}" '
         f'fill="{T["ink"]}">{esc(title)}</text>',
         f'<path d="M0,80H{W}" stroke="{T["line"]}" stroke-width="1.5"/>',
         f'<path d="M0,80H64" stroke="{T["accent"]}" stroke-width="4"/>']
    return svg(W, H, title, f"Section {num}: {title}", "".join(b))


HEADERS = [("01", "About", "about"), ("02", "Selected work", "work"), ("03", "Capabilities", "capabilities"),
           ("04", "Now", "now"), ("05", "Beyond code", "beyond"), ("06", "Activity", "activity"),
           ("07", "Contact", "contact")]


# ------------------------------------------------------------------ PROJECT CARDS
def panel(T):
    g = "".join(f'<path d="M{x},0V312"/>' for x in range(31, 496, 31)) + \
        "".join(f'<path d="M0,{y}H496"/>' for y in range(31, 312, 31))
    return (f'<rect x="0.5" y="0.5" width="495" height="311" fill="{T["raised"]}" stroke="{T["line"]}"/>'
            f'<g stroke="{T["line"]}" opacity=".35">{g}</g>')


def art_signspeak(T):
    o = [panel(T)]
    o.append(hand(42, 54, 142, 204, T))
    o.append(brackets(28, 40, 170, 232, 22, T["accent"])); o.append(tag(28, 40, "gesture", T))
    o.append(arrow(208, 156, 246, 156, T["dim"]))
    o.append(tag(262, 86, "text", T))
    for i, w in enumerate([190, 150, 170]):
        o.append(f'<rect x="262" y="{100+i*24}" width="{w}" height="12" fill="{T["ink"] if i else T["accent"]}"/>')
    o.append(tag(262, 196, "speech", T))
    hs = [8, 18, 30, 14, 38, 22, 10, 32, 20, 12, 26, 16, 34, 10, 22, 28, 12, 18, 8, 24, 14, 30, 10, 16, 8, 12]
    o.append("".join(f'<rect x="{262+i*8}" y="{246-h/2}" width="4" height="{h}" fill="{T["accent"]}"/>' for i, h in enumerate(hs)))
    return "".join(o)


def art_wayfind(T):
    o = [panel(T), plan(34, 44, 428, 232, T)]
    o.append(brackets(28, 38, 440, 244, 24, T["accent"])); o.append(tag(28, 38, "route", T))
    return "".join(o)


def art_edusphere(T):
    o = [panel(T)]
    o.append(f'<rect x="40" y="34" width="150" height="244" rx="16" fill="none" stroke="{T["ink"]}" stroke-width="2.4"/>')
    o.append(f'<rect x="58" y="54" width="70" height="10" fill="{T["ink"]}"/>')
    on = {1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 17}
    for i in range(20):
        cx, cy = 58 + (i % 4) * 34, 96 + (i // 4) * 34
        o.append(f'<rect x="{cx}" y="{cy}" width="26" height="26" fill="{T["accent"] if i in on else "none"}" '
                 f'stroke="{T["accent"] if i in on else T["dim"]}" stroke-width="1.6"/>')
    o.append(tag(240, 56, "roles", T))
    for i, r in enumerate(["student", "teacher", "hod", "principal", "admin"]):
        y = 90 + i * 40
        o.append(f'<circle cx="250" cy="{y-6}" r="6" fill="{T["accent"] if i == 0 else "none"}" '
                 f'stroke="{T["accent"] if i == 0 else T["dim"]}" stroke-width="2"/>'
                 f'<text x="270" y="{y}" font-family="{F_MONO}" font-size="21" fill="{T["ink"]}">{r}</text>'
                 f'<path d="M240,{y+12}H470" stroke="{T["line"]}"/>')
    return "".join(o)


def qr(x, y, s, T):
    bits = ["1110101", "1010011", "1110110", "0001101", "1101011", "0110010", "1011101"]
    c = s / 7
    return "".join(f'<rect x="{x+j*c:.1f}" y="{y+i*c:.1f}" width="{c:.1f}" height="{c:.1f}" fill="{T["ink"]}"/>'
                   for i, row in enumerate(bits) for j, v in enumerate(row) if v == "1")


def art_certify(T):
    o = [panel(T)]
    for i in range(5):
        o.append(f'<rect x="30" y="{80+i*36}" width="96" height="24" fill="none" stroke="{T["dim"]}" stroke-width="1.6"/>'
                 f'<path d="M64,{80+i*36}V{104+i*36}" stroke="{T["dim"]}"/>')
    o.append(arrow(136, 170, 170, 170, T["dim"]))
    for dx, dy in [(40, 0), (20, 16), (0, 32)]:
        x, y = 196 + dx, 44 + dy
        o.append(f'<rect x="{x}" y="{y}" width="250" height="180" fill="{T["raised"]}" stroke="{T["ink"]}" stroke-width="2"/>')
    x, y = 196, 76
    o.append(f'<rect x="{x+24}" y="{y+28}" width="130" height="14" fill="{T["ink"]}"/>'
             f'<rect x="{x+24}" y="{y+56}" width="170" height="8" fill="{T["dim"]}"/>'
             f'<rect x="{x+24}" y="{y+74}" width="120" height="8" fill="{T["dim"]}"/>'
             f'<circle cx="{x+50}" cy="{y+136}" r="24" fill="{T["accent"]}"/>'
             f'<circle cx="{x+50}" cy="{y+136}" r="15" fill="none" stroke="{T["bg"]}" stroke-width="2"/>')
    o.append(qr(x + 180, y + 112, 48, T))
    o.append(tag(196 + 40, 44, "certificate", T))
    return "".join(o)


def art_pockiva(T):
    o = [panel(T)]
    o.append(f'<rect x="40" y="34" width="150" height="244" rx="16" fill="none" stroke="{T["ink"]}" stroke-width="2.4"/>')
    o.append(f'<circle cx="115" cy="128" r="46" fill="none" stroke="{T["line"]}" stroke-width="12"/>'
             f'<circle cx="115" cy="128" r="46" fill="none" stroke="{T["accent"]}" stroke-width="12" '
             f'stroke-dasharray="196 300" transform="rotate(-90 115 128)"/>')
    for i in range(7):
        o.append(f'<circle cx="{62+i*17}" cy="222" r="5" fill="{T["accent"] if i < 4 else "none"}" '
                 f'stroke="{T["accent"] if i < 4 else T["dim"]}" stroke-width="1.6"/>')
    o.append(brackets(40, 34, 150, 244, 22, T["accent"])); o.append(tag(40, 34, "goal", T))
    cx, cy = 300, 100
    for r in (16, 30, 44):
        o.append(f'<path d="M{cx-r*.8:.1f},{cy-r*.55:.1f} A{r},{r} 0 0 1 {cx+r*.8:.1f},{cy-r*.55:.1f}" fill="none" stroke="{T["ink"]}" stroke-width="3"/>')
    o.append(f'<circle cx="{cx}" cy="{cy+10}" r="5" fill="{T["ink"]}"/>'
             f'<path d="M{cx-50},{cy+34}L{cx+50},{cy-58}" stroke="{T["accent"]}" stroke-width="4"/>')
    for i, t in enumerate(["no account", "no internet", "sqlite on device"]):
        y = 178 + i * 36
        o.append(f'<text x="240" y="{y}" font-family="{F_MONO}" font-size="21" fill="{T["ink"]}">{t}</text>'
                 f'<path d="M240,{y+11}H470" stroke="{T["line"]}"/>')
    return "".join(o)


WORKS = [
    ("signspeak", "SignSpeak AI", ["Sign language in,", "Malayalam and speech out."], "prototype, runs locally", art_signspeak),
    ("wayfind", "WayFind", ["Indoor navigation for", "buildings GPS can’t map."], "phases 1 to 4 built", art_wayfind),
    ("edusphere", "EduSphere ERP", ["One college ERP for", "every campus role."], "in progress", art_edusphere),
    ("certifypro", "CertifyPro", ["Bulk certificates,", "verified by QR."], "active", art_certify),
    ("pockiva", "Pockiva", ["Savings goals that", "work offline."], "v1.0.0 on Android", art_pockiva),
]


def card(name, tagl, status, art, T):
    W, H = 960, 360
    b = [f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>', f'<g transform="translate(24,24)">{art(T)}</g>']
    x, mw = 560, 376
    size = min(52, fit(name, "display", mw, 52))
    b.append(f'<text x="{x}" y="120" font-family="{F_DISPLAY}" font-weight="900" font-size="{size:.0f}" '
             f'fill="{T["ink"]}">{esc(name)}</text>')
    for i, l in enumerate(tagl):
        b.append(f'<text x="{x}" y="{170+i*34}" font-family="{F_SERIF}" font-style="italic" font-size="27" '
                 f'fill="{T["ink"]}">{esc(l)}</text>')
    cw = width(status, "mono", 17) + 28
    b.append(f'<rect x="{x}" y="276" width="{cw:.0f}" height="36" fill="none" stroke="{T["accent"]}" stroke-width="2"/>'
             f'<circle cx="{x+16}" cy="294" r="4.5" fill="{T["accent"]}"/>'
             f'<text x="{x+30}" y="300" font-family="{F_MONO}" font-size="17" fill="{T["ink"]}">{esc(status)}</text>')
    return svg(W, H, name, f"{name}: {' '.join(tagl)} Status: {status}.", "".join(b))


# ------------------------------------------------------------------ BANNERS
def beyond(T):
    W, H = 960, 220
    import math
    cx, cy = 150, 110
    nodes = [(420, 50), (560, 150), (700, 60), (820, 160), (900, 70), (330, 170)]
    b = [f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>']
    g = "".join(f'<path d="M{x},0V{H}"/>' for x in range(40, W, 80)) + "".join(f'<path d="M0,{y}H{W}"/>' for y in range(40, H, 80))
    b.append(f'<g stroke="{T["line"]}" opacity=".4">{g}</g>')
    links = [(0, 1), (1, 2), (2, 3), (2, 4), (0, 5), (5, 1), (3, 4)]
    for a, c in links:
        b.append(f'<path d="M{nodes[a][0]},{nodes[a][1]}L{nodes[c][0]},{nodes[c][1]}" stroke="{T["dim"]}" stroke-width="1.6"/>')
    for n in nodes:
        b.append(f'<path d="M{cx+50},{cy}L{n[0]},{n[1]}" stroke="{T["line"]}" stroke-width="1.2"/>')
    for i, (x, y) in enumerate(nodes):
        b.append(f'<circle cx="{x}" cy="{y}" r="{10 if i in (0,2,5) else 7}" fill="{T["accent"] if i in (0,2,5) else T["ink"]}"/>')
    b.append(monogram(cx - 50, cy - 50, 100, T))
    return svg(W, H, "Community network",
               "Decorative network diagram: a central monogram connected to six nodes, representing student communities "
               "and campus chapters.", "".join(b), "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}.pulse{animation:pulse 2.4s ease-in-out infinite}")


def closing(T):
    W, H = 960, 380
    lines = ["Send me something", "that doesn’t work yet."]
    size = min(fit(l, "serif", 864 / 1.32, 84) for l in lines)  # Georgia runs ~15% wider than Times metrics
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" fill="{T["bg"]}" stroke="{T["line"]}" stroke-width="2"/>']
    g = "".join(f'<path d="M{x},2V{H-2}"/>' for x in range(80, W, 80)) + "".join(f'<path d="M2,{y}H{W-2}"/>' for y in range(80, H, 80))
    b.append(f'<g stroke="{T["line"]}" opacity=".4">{g}</g>')
    for i, l in enumerate(lines):
        tl = width(l, "serif", size) * 1.12  # pin the measure so any serif fallback fits
        b.append(f'<text x="48" y="{138+i*size*1.12:.0f}" font-family="{F_SERIF}" font-style="italic" font-size="{size:.0f}" '
                 f'textLength="{tl:.0f}" lengthAdjust="spacingAndGlyphs" fill="{T["ink"]}">{esc(l)}</text>')
    b.append(f'<text x="48" y="{H-52}" font-family="{F_MONO}" font-size="19" fill="{T["dim"]}">'
             f'open to internships, collaborations and interesting problems</text>')
    b.append(monogram(W - 48 - 64, H - 48 - 64, 64, T))
    return svg(W, H, "Closing statement", "Send me something that doesn’t work yet. Open to internships, collaborations and interesting problems.",
               "".join(b), "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}.pulse{animation:pulse 2.4s ease-in-out infinite}")


# ------------------------------------------------------------------ ICONS (theme-neutral mid-tones)
def icons():
    A, G = "#7482F5", "#8B9099"
    s = lambda body: (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" role="img" '
                      f'aria-label="{{}}" fill="none" stroke-width="2.6" stroke-linecap="square" stroke-linejoin="round">{body}</svg>\n')
    defs = {
        "languages": (f'<path d="M18 14L6 24l12 10" stroke="{A}"/><path d="M30 14l12 10-12 10" stroke="{A}"/><path d="M27 10L21 38" stroke="{G}"/>'),
        "frontend": (f'<rect x="5" y="8" width="38" height="32" stroke="{G}"/><path d="M5 17H43" stroke="{G}"/><rect x="12" y="24" width="14" height="10" stroke="{A}"/><path d="M31 25h6M31 31h6" stroke="{A}"/>'),
        "backend": (f'<rect x="7" y="7" width="34" height="12" stroke="{G}"/><rect x="7" y="29" width="34" height="12" stroke="{G}"/><path d="M13 13h4M13 35h4" stroke="{A}"/><path d="M24 19v10" stroke="{A}"/>'),
        "mobile": (f'<rect x="14" y="4" width="20" height="40" rx="4" stroke="{G}"/><path d="M21 38h6" stroke="{A}"/><path d="M19 14h10M19 20h10" stroke="{A}"/>'),
        "ai": (f'<circle cx="24" cy="24" r="6" stroke="{A}"/><circle cx="8" cy="10" r="3" stroke="{G}"/><circle cx="40" cy="10" r="3" stroke="{G}"/><circle cx="8" cy="38" r="3" stroke="{G}"/><circle cx="40" cy="38" r="3" stroke="{G}"/><path d="M10 12l9 8M38 12l-9 8M10 36l9-8M38 36l-9-8" stroke="{G}"/>'),
        "databases": (f'<ellipse cx="24" cy="11" rx="15" ry="5" stroke="{A}"/><path d="M9 11v26c0 3 7 5 15 5s15-2 15-5V11" stroke="{G}"/><path d="M9 24c0 3 7 5 15 5s15-2 15-5" stroke="{G}"/>'),
        "tools": (f'<circle cx="14" cy="10" r="4" stroke="{A}"/><circle cx="14" cy="38" r="4" stroke="{G}"/><circle cx="34" cy="24" r="4" stroke="{A}"/><path d="M14 14v20M14 30c0-6 20-2 20-2" stroke="{G}"/>'),
        "design": (f'<path d="M8 40C8 18 22 8 40 8" stroke="{G}"/><rect x="5" y="37" width="6" height="6" stroke="{A}"/><rect x="37" y="5" width="6" height="6" stroke="{A}"/><path d="M8 40L24 24" stroke="{A}" stroke-dasharray="3 4"/>'),
    }
    for k, body in defs.items():
        write(f"icon-{k}.svg", s(body).replace("{}", k))


def main():
    for tn, T in THEMES.items():
        write(f"hero-{tn}.svg", hero(T))
        for num, title, slug in HEADERS:
            write(f"h-{slug}-{tn}.svg", header(num, title, T))
        for slug, name, tagl, status, art in WORKS:
            write(f"work-{slug}-{tn}.svg", card(name, tagl, status, art, T))
        write(f"beyond-{tn}.svg", beyond(T))
        write(f"closing-{tn}.svg", closing(T))
    icons()
    print("assets:", len(os.listdir(OUT)))


if __name__ == "__main__":
    main()
