"""Builds assets/activity-{dark,light}.svg from public GitHub data.
No third-party widget services: the SVGs live in this repo and are refreshed by
.github/workflows/update-activity.yml.   Usage: python scripts/update_activity.py [username]
"""
import datetime as dt, html as htmllib, json, os, re, sys, urllib.request
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from theme import *

USER = sys.argv[1] if len(sys.argv) > 1 else "mhd-humraz"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
UA = {"User-Agent": "profile-readme-activity"}


def get(url, accept=None):
    h = dict(UA)
    tok = os.environ.get("GITHUB_TOKEN")
    if tok and "api.github.com" in url:
        h["Authorization"] = f"Bearer {tok}"
    if accept:
        h["Accept"] = accept
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def contributions():
    t = get(f"https://github.com/users/{USER}/contributions")
    tips = {m.group(1): m.group(2) for m in re.finditer(r'for="([^"]+)"[^>]*>([^<]*)', t)}
    days = []
    for m in re.finditer(r'<td[^>]*data-date="([^"]+)"[^>]*id="([^"]+)"[^>]*data-level="(\d)"', t):
        date, cid, level = m.groups()
        tip = tips.get(cid, "")
        n = re.match(r"(\d+) contribution", tip)
        days.append((dt.date.fromisoformat(date), int(level), int(n.group(1)) if n else 0))
    days.sort()
    return days


def repos():
    try:  # API (works in Actions with GITHUB_TOKEN)
        data = json.loads(get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner"))
        if isinstance(data, list):
            return [(r["language"], r["fork"]) for r in data]
    except Exception:
        pass
    out, seen = [], set()  # HTML fallback (deduped by repo name)
    for p in (1, 2, 3, 4):
        t = get(f"https://github.com/{USER}?tab=repositories&page={p}")
        items = t.split('itemprop="owns"')[1:]
        if not items:
            break
        for it in items:
            nm = re.search(r'href="/[^/"]+/([^"]+)"', it).group(1)
            if nm in seen:
                continue
            seen.add(nm)
            l = re.search(r'itemprop="programmingLanguage">([^<]+)', it)
            out.append((l.group(1) if l else None, "Forked from" in it))
    return out


def build(T, days, repo_rows):
    W, H = 960, 560
    total = sum(d[2] for d in days)
    active = sum(1 for d in days if d[2] > 0)
    own = [r for r in repo_rows if not r[1]]
    langs = Counter(l for l, _ in own if l).most_common()
    top = langs[:6]
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" fill="{T["bg"]}" stroke="{T["line"]}" stroke-width="2"/>']
    stats = [(f"{total:,}", "contributions, last 12 months"), (str(active), "active days"),
             (str(len(own)), "original public repositories")]
    for i, (n, l) in enumerate(stats):
        x = 48 + i * 300
        b.append(f'<text x="{x}" y="96" font-family="{F_DISPLAY}" font-weight="900" font-size="66" fill="{T["ink"]}">{n}</text>'
                 f'<text x="{x}" y="128" font-family="{F_MONO}" font-size="17" fill="{T["dim"]}">{l}</text>')
    b.append(f'<path d="M48,156H{W-48}" stroke="{T["line"]}" stroke-width="1.5"/>')
    # heatmap
    first = days[0][0]
    start = first - dt.timedelta(days=(first.weekday() + 1) % 7)  # Sunday
    cols = ((days[-1][0] - start).days // 7) + 1
    pitch = 864 / max(cols, 1); cell = pitch - 3
    for d, lvl, n in days:
        k = (d - start).days
        x, y = 48 + (k // 7) * pitch, 196 + (k % 7) * pitch
        b.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell:.1f}" height="{cell:.1f}" fill="{T["heat"][lvl]}"/>')
    seen = set()
    for d, _, _ in days:
        if d.day <= 7 and d.month not in seen and d.weekday() == 6:
            seen.add(d.month)
            b.append(f'<text x="{48+((d-start).days//7)*pitch:.1f}" y="184" font-family="{F_MONO}" font-size="14" '
                     f'fill="{T["dim"]}">{d.strftime("%b").lower()}</text>')
    gy = 196 + 7 * pitch + 22
    b.append(f'<text x="48" y="{gy:.0f}" font-family="{F_MONO}" font-size="16" fill="{T["dim"]}">less</text>')
    for i, c in enumerate(T["heat"]):
        b.append(f'<rect x="{96+i*20}" y="{gy-13:.0f}" width="14" height="14" fill="{c}"/>')
    b.append(f'<text x="204" y="{gy:.0f}" font-family="{F_MONO}" font-size="16" fill="{T["dim"]}">more</text>')
    # languages
    ly = 400
    b.append(f'<path d="M48,{ly-30}H{W-48}" stroke="{T["line"]}" stroke-width="1.5"/>')
    cols_ = [T["accent"], T["ink"], T["heat"][3], T["dim"], T["heat"][2], T["line"]]
    tot = sum(c for _, c in top) or 1
    x = 48
    for i, (n, c) in enumerate(top):
        w = 864 * c / tot
        b.append(f'<rect x="{x:.1f}" y="{ly}" width="{max(w-2,1):.1f}" height="22" fill="{cols_[i]}"/>')
        x += w
    for i, (n, c) in enumerate(top):
        lx, lyy = 48 + (i % 3) * 300, ly + 62 + (i // 3) * 38
        b.append(f'<rect x="{lx}" y="{lyy-15}" width="16" height="16" fill="{cols_[i]}"/>'
                 f'<text x="{lx+28}" y="{lyy}" font-family="{F_MONO}" font-size="20" fill="{T["ink"]}">'
                 f'{esc(n)} <tspan fill="{T["dim"]}">{c}</tspan></text>')
    b.append(f'<text x="48" y="{H-30}" font-family="{F_MONO}" font-size="15" fill="{T["dim"]}">languages: primary language of each original public repository</text>')
    desc = (f"{total} contributions in the last 12 months across {active} active days; {len(own)} original public repositories. "
            "Top languages by repository: " + ", ".join(f"{n} {c}" for n, c in top) + ".")
    return svg(W, H, "GitHub activity", desc, "".join(b))


if __name__ == "__main__":
    days, rr = contributions(), repos()
    if not days:
        sys.exit("no contribution data; keeping existing assets")
    for tn, T in THEMES.items():
        with open(os.path.join(OUT, f"activity-{tn}.svg"), "w", encoding="utf-8") as f:
            f.write(build(T, days, rr))
    print("activity updated:", sum(d[2] for d in days), "contributions,", len(rr), "repos")
