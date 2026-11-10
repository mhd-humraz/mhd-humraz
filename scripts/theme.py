"""Shared design tokens + SVG helpers for the profile README assets."""
import html
from PIL import ImageFont

THEMES = {
    "dark": dict(bg="#17181A", raised="#1F2125", line="#3A3D44", ink="#ECEAE4",
                 dim="#8F939C", accent="#8191FF",
                 heat=["#26282D", "#343B6B", "#4B58B3", "#6676E6", "#8191FF"]),
    "light": dict(bg="#ECEDEF", raised="#F8F8F9", line="#C4C7CE", ink="#15161A",
                  dim="#595E68", accent="#2B3FDD",
                  heat=["#DEE0E5", "#C3CAF5", "#93A0EE", "#5B6EE6", "#2B3FDD"]),
}

F_DISPLAY = "'Arial Black','Helvetica Neue',Helvetica,Arial,sans-serif"
F_SERIF = "Georgia,'Iowan Old Style','Times New Roman',serif"
F_MONO = "ui-monospace,'SF Mono',Menlo,Consolas,'DejaVu Sans Mono',monospace"

_FONT_FILES = {
    "display": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "serif": "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "mono": "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
}
_cache = {}


def width(text, kind, size):
    """Approximate rendered width (Arial/Times/Courier metrics)."""
    if kind not in _cache:
        _cache[kind] = ImageFont.truetype(_FONT_FILES[kind], 1000)
    return _cache[kind].getlength(text) * size / 1000


def esc(s):
    return html.escape(s, quote=False)


def svg(w, h, title, desc, body, css=""):
    base = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t d">\n<title id="t">{esc(title)}</title>\n'
            f'<desc id="d">{esc(desc)}</desc>\n<style>{css}{base}</style>\n{body}\n</svg>\n')


def brackets(x, y, w, h, L, c, sw=3):
    d = (f"M{x},{y+L}V{y}H{x+L} M{x+w-L},{y}H{x+w}V{y+L} "
         f"M{x+w},{y+h-L}V{y+h}H{x+w-L} M{x+L},{y+h}H{x}V{y+h-L}")
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="square"/>'


def tag(x, y, text, T, size=15):
    """Detection-style label tab sitting on top of (x, y)."""
    w = width(text, "mono", size) + 18
    return (f'<rect x="{x}" y="{y-24}" width="{w:.0f}" height="24" fill="{T["accent"]}"/>'
            f'<text x="{x+9}" y="{y-7}" font-family="{F_MONO}" font-size="{size}" '
            f'fill="{T["bg"]}">{esc(text)}</text>')


def monogram(x, y, s, T, blink=True):
    """Square frame with an H drawn as a small graph; centre node pulses."""
    l, r = x + .30 * s, x + .70 * s
    ys = [y + .26 * s, y + .50 * s, y + .74 * s]
    rr = max(2.2, s * .045)
    out = [brackets(x, y, s, s, s * .22, T["accent"], max(2, s * .045))]
    st = f'stroke="{T["ink"]}" stroke-width="{max(1.6, s*.035):.1f}"'
    out.append(f'<path d="M{l},{ys[0]}V{ys[2]} M{r},{ys[0]}V{ys[2]} M{l},{ys[1]}H{r}" fill="none" {st}/>')
    for cx in (l, r):
        for cy in (ys[0], ys[2]):
            out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rr:.1f}" fill="{T["ink"]}"/>')
    cls = ' class="pulse"' if blink else ""
    out.append(f'<circle{cls} cx="{(l+r)/2:.1f}" cy="{ys[1]:.1f}" r="{rr*1.4:.1f}" fill="{T["accent"]}"/>')
    return "".join(out)


# ---------- illustration primitives (the "things I taught software to see") ----------
HAND = dict(w=(.50, .96),
            t=[(.38, .84), (.27, .71), (.19, .58), (.12, .46)],
            i=[(.40, .56), (.38, .39), (.37, .27), (.36, .15)],
            m=[(.50, .53), (.50, .34), (.50, .21), (.50, .09)],
            r=[(.60, .56), (.62, .39), (.63, .28), (.64, .18)],
            p=[(.69, .63), (.73, .49), (.75, .40), (.77, .31)])


def hand(x, y, w, h, T, dot=4.2):
    P = lambda p: (x + p[0] * w, y + p[1] * h)
    chains = [[HAND["w"]] + HAND["t"], HAND["i"], HAND["m"], HAND["r"], HAND["p"],
              [HAND["w"], HAND["i"][0], HAND["m"][0], HAND["r"][0], HAND["p"][0], HAND["w"]]]
    out = []
    for c in chains:
        pts = " ".join(f"{P(p)[0]:.1f},{P(p)[1]:.1f}" for p in c)
        out.append(f'<polyline points="{pts}" fill="none" stroke="{T["accent"]}" stroke-width="2.2" stroke-linejoin="round"/>')
    tips = {HAND["t"][-1], HAND["i"][-1], HAND["m"][-1], HAND["r"][-1], HAND["p"][-1]}
    pts = {HAND["w"]} | {p for k in "tirmp" for p in HAND[k]}
    for p in pts:
        cx, cy = P(p)
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{dot*1.2 if p in tips else dot}" '
                   f'fill="{T["accent"] if p in tips else T["ink"]}"/>')
    return "".join(out)


def eye(cx, cy, w, T):
    h = w * .30
    d = (f"M{cx-w/2:.1f},{cy:.1f} Q{cx:.1f},{cy-h*1.6:.1f} {cx+w/2:.1f},{cy:.1f} "
         f"Q{cx:.1f},{cy+h*1.6:.1f} {cx-w/2:.1f},{cy:.1f}Z")
    ir, a = w * .19, w * .30
    return (f'<path d="{d}" fill="none" stroke="{T["ink"]}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{ir:.1f}" fill="none" stroke="{T["ink"]}" stroke-width="2.2"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{ir*.42:.1f}" fill="{T["accent"]}"/>'
            f'<path d="M{cx-a:.1f},{cy}H{cx-ir*1.3:.1f} M{cx+ir*1.3:.1f},{cy}H{cx+a:.1f} '
            f'M{cx},{cy-a*.8:.1f}V{cy-ir*1.3:.1f} M{cx},{cy+ir*1.3:.1f}V{cy+a*.8:.1f}" '
            f'stroke="{T["accent"]}" stroke-width="2" fill="none"/>')


ROOMS = [(.05, .08, .30, .30), (.40, .08, .25, .30), (.70, .08, .25, .30),
         (.05, .62, .22, .30), (.32, .62, .30, .30), (.68, .62, .27, .30)]
ROUTE = [(.16, .80), (.16, .62), (.16, .50), (.52, .50), (.52, .38), (.52, .22)]


def plan(x, y, w, h, T, animate=True):
    P = lambda p: (x + p[0] * w, y + p[1] * h)
    out = []
    for rx, ry, rw, rh in ROOMS:
        out.append(f'<rect x="{x+rx*w:.1f}" y="{y+ry*h:.1f}" width="{rw*w:.1f}" height="{rh*h:.1f}" '
                   f'fill="none" stroke="{T["dim"]}" stroke-width="1.6"/>')
    for p in [(.20, .38), (.52, .38), (.82, .38), (.16, .62), (.47, .62), (.80, .62)]:
        cx, cy = P(p)
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3" fill="{T["dim"]}"/>')
    pts = " ".join(f"{P(p)[0]:.1f},{P(p)[1]:.1f}" for p in ROUTE)
    cls = ' class="flow"' if animate else ""
    out.append(f'<polyline{cls} points="{pts}" fill="none" stroke="{T["accent"]}" stroke-width="3.4" '
               f'stroke-linejoin="round" stroke-dasharray="9 7"/>')
    sx, sy = P(ROUTE[0]); ex, ey = P(ROUTE[-1])
    out.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="6" fill="{T["ink"]}"/>')
    out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="11" fill="none" stroke="{T["accent"]}" stroke-width="2.4"/>'
               f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="5" fill="{T["accent"]}"/>')
    return "".join(out)


def arrow(x1, y1, x2, y2, c, sw=2):
    return (f'<path d="M{x1},{y1}L{x2},{y2}" stroke="{c}" stroke-width="{sw}"/>'
            f'<path d="M{x2-9},{y2-6}L{x2},{y2}L{x2-9},{y2+6}" fill="none" stroke="{c}" stroke-width="{sw}"/>'
            if y1 == y2 else
            f'<path d="M{x1},{y1}L{x2},{y2}" stroke="{c}" stroke-width="{sw}"/>'
            f'<path d="M{x2-6},{y2-9}L{x2},{y2}L{x2+6},{y2-9}" fill="none" stroke="{c}" stroke-width="{sw}"/>')
