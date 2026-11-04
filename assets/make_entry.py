#!/usr/bin/env python3
"""Generate entry-light.svg and entry-dark.svg: one entry's drafts before the user's go.

The dossier settles the entry, and the resume and answers each cite the profile
facts they come from. All text is outlined to paths with fontTools.
Each glyph is defined once and placed with <use>, which keeps the files small.
Run: python3 assets/make_entry.py  (writes the SVGs here, PNG previews to .tmp/)
"""
import subprocess
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

sys.dont_write_bytecode = True
from make_banner import THEMES as BANNER, advance, check, contrast, glyph_paths, runs  # noqa: E402

HERE = Path(__file__).resolve().parent
SANS = TTFont("/usr/share/fonts/Adwaita/AdwaitaSans-Regular.ttf")  # SIL OFL, variable wght/opsz
W, H = 880, 580
MONO = 13

# Banner palette plus the card surfaces.
THEMES = {
    "dark": {**BANNER["dark"], "card": "#1a1b26", "head": "#16161e", "line_alpha": 0.9, "tint": 0.10},
    "light": {**BANNER["light"], "card": "#f3f4f8", "head": "#e1e2e7", "line_alpha": 0.8, "tint": 0.09},
}


# ---- glyphs, defined once per build -----------------------------------------

GLYPHS = {}  # (font, size, weight, char) -> (id, path at the origin)


def glyph(key, draw):
    if key not in GLYPHS:
        d = draw()
        GLYPHS[key] = (f"g{len(GLYPHS)}", d) if d else (None, None)
    return GLYPHS[key][0]


def placed(chars, fill):
    """chars: [(glyph id, x, y)] drawn in one fill."""
    uses = "".join(f'<use href="#{g}" x="{x:.2f}" y="{y:.2f}"/>' for g, x, y in chars if g)
    return f'<g fill="{fill}">{uses}</g>'


_SANS_SETS = {}


def _sans_set(size, wght):
    key = (min(max(size, 14), 32), wght)
    if key not in _SANS_SETS:
        _SANS_SETS[key] = SANS.getGlyphSet(location={"wght": wght, "opsz": key[0]})
    return _SANS_SETS[key]


def sans_width(text, size, wght=400):
    gs, cmap = _sans_set(size, wght), SANS.getBestCmap()
    s = size / SANS["head"].unitsPerEm
    return sum(gs[cmap.get(ord(c), ".notdef")].width * s for c in text)


def sans(text, x, y, size, fill, wght=400):
    gs, cmap = _sans_set(size, wght), SANS.getBestCmap()
    s = size / SANS["head"].unitsPerEm
    out = []
    for ch in text:
        g = gs[cmap.get(ord(ch), ".notdef")]
        if not ch.isspace():
            def draw(g=g):
                pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
                g.draw(TransformPen(pen, (s, 0, 0, -s, 0, 0)))
                return pen.getCommands()
            out.append((glyph(("sans", size, wght, ch), draw), x, y))
        x += g.width * s
    return placed(out, fill)


def wrap(text, size, width, wght=400):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and sans_width(trial, size, wght) > width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur]


def mono(text, x, y, fill, size=MONO, weight="regular"):
    out = []
    for i, ch in enumerate(text):
        if not ch.isspace():
            def draw(ch=ch):
                return "".join(d for _, _, d in glyph_paths(ch, 0, 0, size, weight))
            out.append((glyph(("mono", size, weight, ch), draw), x + advance(size, i), y))
    return placed(out, fill)


def mw(text, size=MONO):
    return advance(size, len(text))


# ---- pieces ---------------------------------------------------------------

def card(t, x, y, w, h, name, sub=None):
    """A document card with a file-name header bar."""
    hb = 34
    out = []
    if t["shadow"]:
        out.append(f'<rect x="{x}" y="{y + 5}" width="{w}" height="{h}" rx="10" fill="#1a1b26" '
                   f'opacity="{t["shadow"]}" filter="url(#blur)"/>')
    out.append(f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="10" '
               f'fill="{t["card"]}" stroke="{t["border"]}"/>')
    out.append(f'<path d="M{x + .5} {y + hb}V{y + 10.5}a10 10 0 0 1 10-10H{x + w - 10.5}'
               f'a10 10 0 0 1 10 10V{y + hb}Z" fill="{t["head"]}" stroke="{t["border"]}"/>')
    out.append(mono(name, x + 16, y + 22, t["fg"], weight="semibold"))
    if sub:
        out.append(mono(sub, x + w - 16 - mw(sub), y + 22, t["dim"]))
    return "\n".join(out)


def pill(t, x, y, label, color, size=MONO):
    """A status pill with its text baseline at y; returns (svg, width)."""
    w = mw(label, size) + 18
    return (f'<rect x="{x}" y="{y - 15}" width="{w}" height="21" rx="10.5" fill="none" '
            f'stroke="{color}" stroke-width="1.4"/>' + mono(label, x + 9, y, color, size, "semibold")), w


def build(theme):
    t = THEMES[theme]
    GLYPHS.clear()
    els = []
    M = 16

    # ---- the ready list line this entry sits on -------------------------
    y = 30
    els.append(runs([("▸ ", t["purple"]), ("pipeline/ready.md  ", t["dim"]), ("1. ", t["amber"]),
                     ("Brightkiln, Platform Engineer", t["fg"]), (" · easy_apply · fit 4", t["dim"])],
                    M, y, 14, "regular"))
    hint = "waiting for: apply 1"
    els.append(runs([(hint, t["green"])], W - M - advance(14, len(hint)), y, 14, "semibold"))

    # ---- dossier, full width ---------------------------------------------
    dx, dy, dw, dh = M, 48, W - 2 * M, 210
    els.append(card(t, dx, dy, dw, dh, "employers/brightkiln.md", "dossier"))
    by = dy + 34
    # column 1: frontmatter
    c1 = dx + 18
    els.append(sans("Brightkiln", c1, by + 34, 22, t["title"], 650))
    fields = [("stage", "series-a"), ("headcount", "51-200"), ("remote_policy", "remote-first"),
              ("updated", "2026-11-03")]
    for i, (k, v) in enumerate(fields):
        yy = by + 62 + i * 21
        els.append(mono(k + ":", c1, yy, t["dim"]))
        els.append(mono(v, c1 + mw("remote_policy: "), yy, t["fg"]))
    # column 2: body sections
    c2 = dx + 268
    secs = [("## Product", "Scheduling software for regional clinics."),
            ("## Hiring signals", "Three platform roles open, a first SRE hired in Q3."),
            ("## Team", "CTO and two platform engineers, one a 2nd-degree connection.")]
    yy = by + 26
    for head, body in secs:
        els.append(mono(head, c2, yy, t["purple"], weight="semibold"))
        for ln in wrap(body, 14, 300):
            yy += 19
            els.append(sans(ln, c2, yy, 14, t["fg"]))
        yy += 22
    # column 3: the verdict on the entry
    vx, vy, vw, vh = dx + dw - 262, by + 14, 246, dh - 34 - 28
    els.append(f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="8" fill="{t["green"]}" '
               f'opacity="{t["tint"]}"/>')
    els.append(f'<rect x="{vx}" y="{vy}" width="3" height="{vh}" rx="1.5" fill="{t["green"]}"/>')
    els.append(mono("verdict", vx + 16, vy + 24, t["dim"]))
    p, pw = pill(t, vx + 16 + mw("verdict "), vy + 24, "shortlisted", t["green"])
    els.append(p)
    reason = "Remote-first and series-a, as criteria.md asks. No hard filter disproved."
    yy = vy + 50
    for ln in wrap(reason, 14, vw - 32):
        els.append(sans(ln, vx + 16, yy, 14, t["fg"]))
        yy += 19
    els.append(mono("entry Activity, 2026-11-03", vx + 16, vy + vh - 16, t["dim"]))

    # ---- bottom row: resume, profile facts, answers ----------------------
    ty = dy + dh + 22
    th = H - ty - M
    pw_col = 186
    gap = 30
    cw = (W - 2 * M - pw_col - 2 * gap) / 2
    rx_, px, ax = M, M + cw + gap, M + cw + gap + pw_col + gap

    facts = {"orvane": ("experience/orvane.md", t["blue"]),
             "kit": ("projects/infra-kit.md", t["purple"]),
             "about": ("about.md", t["amber"])}

    # resume card
    els.append(card(t, rx_, ty, cw, th, "resume.yaml", "tailored"))
    resume = [("Moved 40 services to Kubernetes with zero-downtime deploys", "orvane"),
              ("Cut CI time from 25 to 7 minutes for 30 engineers", "orvane"),
              ("Wrote the Terraform modules six product teams deploy with", "kit")]
    yy = ty + 34 + 28
    src_r = []
    for text, fact in resume:
        lines = wrap(text, 14, cw - 50)
        els.append(f'<circle cx="{rx_ + 21}" cy="{yy - 5}" r="2.5" fill="{t["fg"]}"/>')
        for ln in lines:
            els.append(sans(ln, rx_ + 32, yy, 14, t["fg"]))
            yy += 19
        name, col = facts[fact]
        els.append(mono("source: ", rx_ + 32, yy, t["dim"]))
        els.append(mono(name, rx_ + 32 + mw("source: "), yy, col))
        src_r.append((yy - 4, fact))
        yy += 30
    els.append(check(rx_ + 16, ty + th - 16, 15, t["green"]))
    els.append(sans("One page, every line sourced", rx_ + 36, ty + th - 16, 14, t["dim"]))

    # answers card
    els.append(card(t, ax, ty, cw, th, "answers.md", "easy apply"))
    answers = [("Years of Kubernetes experience?", "numeric · required", "4", "orvane",
                "experience/orvane.md"),
               ("Do you require visa sponsorship?", "radio · required · Yes, No", "No", "about",
                "profile/about.md")]
    yy = ty + 34 + 26
    src_a = []
    for q, meta, ans, fact, cite in answers:
        els.append(mono("## ", ax + 16, yy, t["purple"], weight="semibold"))
        els.append(sans(q, ax + 16 + mw("## "), yy, 14, t["fg"], 600))
        yy += 20
        els.append(mono(meta, ax + 16, yy, t["dim"]))
        yy += 21
        els.append(mono("Answer:", ax + 16, yy, t["dim"]))
        yy += 21
        els.append(sans(ans, ax + 16, yy, 15, t["title"], 650))
        yy += 21
        els.append(mono("Source: ", ax + 16, yy, t["dim"]))
        els.append(mono(cite, ax + 16 + mw("Source: "), yy, facts[fact][1]))
        src_a.append((yy - 4, fact))
        yy += 36

    # profile facts column
    els.append(mono("profile/", px + pw_col / 2 - mw("profile/", 14) / 2, ty + 22, t["title"], 14, "semibold"))
    els.append(sans("profile facts", px + pw_col / 2 - sans_width("profile facts", 13) / 2,
                    ty + 40, 13, t["dim"]))
    chip_y = {}
    cy = ty + 78
    for key, (name, col) in facts.items():
        w = pw_col
        els.append(f'<rect x="{px + .5}" y="{cy - 17.5}" width="{w - 1}" height="29" rx="6" '
                   f'fill="{t["card"]}" stroke="{col}" stroke-width="1.4"/>')
        els.append(mono(name, px + w / 2 - mw(name) / 2, cy + 1, col))
        chip_y[key] = cy - 3
        cy += 58
    els.append(sans("No source, no line.", px + pw_col / 2 - sans_width("No source, no line.", 14, 600) / 2,
                    ty + th - 16, 14, t["dim"], 600))

    # links: each cited source to its fact
    links = []
    for sy, fact in src_r:
        x0, x1, y1 = rx_ + cw, px, chip_y[fact]
        links.append((x0, sy, x1, y1, facts[fact][1]))
    for sy, fact in src_a:
        links.append((ax, sy, px + pw_col, chip_y[fact], facts[fact][1]))
    for x0, y0, x1, y1, col in links:
        mx = (x0 + x1) / 2
        els.append(f'<path d="M{x0:.1f} {y0:.1f}C{mx:.1f} {y0:.1f} {mx:.1f} {y1:.1f} {x1:.1f} {y1:.1f}" '
                   f'fill="none" stroke="{col}" stroke-width="1.6" opacity="{t["line_alpha"]}"/>')
        for cx_, cy_ in ((x0, y0), (x1, y1)):
            els.append(f'<circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="3.5" fill="{col}"/>')

    defs = "".join(f'<path id="{g}" d="{d}"/>' for g, d in GLYPHS.values() if g)
    if t["shadow"]:
        defs += ('<filter id="blur" x="-5%" y="-10%" width="110%" height="130%">'
                 '<feGaussianBlur stdDeviation="7"/></filter>')
    defs = f"<defs>{defs}</defs>"
    title = ("One ready entry before your go: the employer dossier with its shortlist verdict, "
             "and a tailored resume and form answers whose every line cites a profile fact")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{defs}\n' + "\n".join(els) + "\n</svg>\n")


def main():
    for theme in THEMES:
        svg = HERE / f"entry-{theme}.svg"
        svg.write_text(build(theme))
        preview = HERE.parent / ".tmp" / f"entry-{theme}.png"
        preview.parent.mkdir(exist_ok=True)
        subprocess.run(["rsvg-convert", "-b", THEMES[theme]["page"], "-z", "1", "-o",
                        str(preview), str(svg)], check=True)
    for theme, t in THEMES.items():
        pairs = {f"{k}/{s}": (t[k], t[s]) for s in ("card", "head", "page")
                 for k in ("fg", "dim", "blue", "purple", "green", "amber", "title")}
        tint = t["tint"]  # the verdict box: green over the card
        box = "#" + "".join(f"{round(int(t['card'][i:i + 2], 16) * (1 - tint) + int(t['green'][i:i + 2], 16) * tint):02x}"
                            for i in (1, 3, 5))
        pairs.update({"fg/verdict": (t["fg"], box), "dim/verdict": (t["dim"], box), "green/verdict": (t["green"], box)})
        low = {k: round(contrast(*v), 2) for k, v in pairs.items() if contrast(*v) < 4.5}
        print(theme, "all text pairs >= 4.5:1" if not low else f"below 4.5: {low}")


if __name__ == "__main__":
    main()
