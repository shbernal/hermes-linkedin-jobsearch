#!/usr/bin/env python3
"""Generate banner-light.svg and banner-dark.svg: the approval moment.

All text is outlined to paths with fontTools, so the SVGs need no fonts.
Run: python3 assets/make_banner.py  (writes the SVGs here, PNG previews to .tmp/)
"""
import subprocess
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
FONT_DIR = Path("/usr/share/fonts/TTF")
FONTS = {
    "regular": TTFont(FONT_DIR / "CaskaydiaMonoNerdFontMono-Regular.ttf"),
    "semibold": TTFont(FONT_DIR / "CaskaydiaMonoNerdFontMono-SemiBold.ttf"),
    "bold": TTFont(FONT_DIR / "CaskaydiaMonoNerdFontMono-Bold.ttf"),
}
W, H = 1280, 320
CYCLE = 14.0  # seconds; the final frame holds from ~4s to 14s


def glyph_paths(text, x, y, size, weight="regular", spacing=0.0):
    """Return a list of (char, x, d) with each glyph outlined at baseline y."""
    font = FONTS[weight]
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font["head"].unitsPerEm
    s = size / upm
    out = []
    for ch in text:
        name = cmap.get(ord(ch), ".notdef")
        adv = font["hmtx"][name][0] * s
        if not ch.isspace():
            pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
            gs[name].draw(TransformPen(pen, (s, 0, 0, -s, x, y)))
            d = pen.getCommands()
            if d:
                out.append((ch, x, d))
        x += adv + spacing
    return out


def advance(size, n=1):
    return FONTS["regular"]["hmtx"]["a"][0] * size / 2048 * n


def text_path(text, x, y, size, fill, weight="regular", spacing=0.0, cls=None):
    d = "".join(p for _, _, p in glyph_paths(text, x, y, size, weight, spacing))
    c = f' class="{cls}"' if cls else ""
    return f'<path{c} fill="{fill}" d="{d}"/>'


def check(x, y, size, color):
    """A drawn check mark sitting on baseline y (the font has no heavy check)."""
    u = size / 16
    return (f'<path d="M{x + 1.5 * u:.1f} {y - 5.5 * u:.1f}l{3.5 * u:.1f} {3.5 * u:.1f}l{6.5 * u:.1f} {-8.5 * u:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="{2.2 * u:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')


def runs(parts, x, y, size, weight="regular"):
    """parts: [(text, fill)] laid out left to right on one mono line."""
    out = []
    for txt, fill in parts:
        if txt.strip():
            out.append(text_path(txt, x, y, size, fill, weight))
        x += advance(size, len(txt))
    return "\n".join(out)


# ---- contrast -------------------------------------------------------------

def _lum(hexc):
    hexc = hexc.lstrip("#")
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# ---- themes ---------------------------------------------------------------

THEMES = {
    "dark": dict(
        page="#0d1117", win="#1a1b26", bar="#16161e", border="#3b4261",
        fg="#c0caf5", dim="#787fa6", blue="#7aa2f7", purple="#bb9af7",
        green="#9ece6a", amber="#e0af68", red="#f7768e",
        title="#c0caf5", sub="#a9b1d6", pick="#9ece6a", pick_alpha=0.10,
        shadow=0.0,
    ),
    # Tokyo Night Day text tones: the night accents are too light on white.
    "light": dict(
        page="#ffffff", win="#e1e2e7", bar="#d4d6e4", border="#c4c8da",
        fg="#3760bf", dim="#5a6390", blue="#2a6bd6", purple="#7847bd",
        green="#4d6a2f", amber="#7a5a28", red="#c64343",
        title="#343b58", sub="#4c5372", pick="#9ece6a", pick_alpha=0.24,
        shadow=0.10,
    ),
}


def build(theme):
    t = THEMES[theme]
    els = []
    css = []

    # ---- left column: the name -------------------------------------------
    lx = 28
    els.append(runs([("hermes agent · profile distribution", t["purple"])], lx, 92, 15, "semibold"))
    els.append(text_path("hermes-linkedin-", lx - 2, 146, 40, t["title"], "semibold"))
    els.append(text_path("jobsearch", lx - 4, 212, 70, t["blue"], "bold", spacing=-2))
    els.append(text_path("A job-search agent that works your", lx, 254, 17, t["sub"]))
    els.append(text_path("LinkedIn pipeline from posting to answer.", lx, 279, 17, t["sub"]))

    # ---- right: the terminal window --------------------------------------
    wx, wy, ww, wh = 512, 18, 748, 284
    bar_h = 32
    if t["shadow"]:
        els.append(f'<rect x="{wx}" y="{wy + 6}" width="{ww}" height="{wh}" rx="12" '
                   f'fill="#1a1b26" opacity="{t["shadow"]}" filter="url(#blur)"/>')
    els.append(f'<rect x="{wx + .5}" y="{wy + .5}" width="{ww - 1}" height="{wh - 1}" rx="12" '
               f'fill="{t["win"]}" stroke="{t["border"]}"/>')
    els.append(f'<path d="M{wx + .5} {wy + bar_h}V{wy + 12.5}a12 12 0 0 1 12-12H{wx + ww - 12.5}'
               f'a12 12 0 0 1 12 12V{wy + bar_h}Z" fill="{t["bar"]}" stroke="{t["border"]}"/>')
    for i, c in enumerate(("#f7768e", "#e0af68", "#9ece6a")):
        els.append(f'<circle cx="{wx + 22 + i * 20}" cy="{wy + bar_h / 2}" r="6" fill="{c}"/>')
    bt = "jobsearch: scheduled run"
    els.append(text_path(bt, wx + ww / 2 - advance(13, len(bt)) / 2, wy + 21, 13, t["dim"]))

    fs, lh = 17, 28
    cx = wx + 24
    cw = advance(fs)
    y0 = wy + bar_h + 34
    L = lambda n: y0 + n * lh

    els.append(runs([("▸ ", t["purple"]), ("07:00 run · 41 postings scanned, 3 entries ready", t["dim"])], cx, L(0), fs))

    rows = [
        ("1", "Senior Backend Engineer", "fit 86", "remote"),
        ("2", "Platform Engineer", "fit 71", "hybrid"),
        ("3", "Data Infrastructure Lead", "fit 82", "remote"),
    ]
    for i, (n, role, fit, where) in enumerate(rows):
        y = L(1.2 + i)
        picked = n in ("1", "3")
        if picked:
            els.append(f'<rect class="pick" x="{cx - 10}" y="{y - 19}" width="{ww - 28}" height="{lh - 3}" '
                       f'rx="5" fill="{t["pick"]}" opacity="{t["pick_alpha"]}"/>')
            els.append(f'<g class="pick">{check(wx + ww - 46, y, fs, t["green"])}</g>')
        cls = "skip" if not picked else ""
        els.append(f'<g class="{cls}">' + runs([
            (f" {n}  ", t["amber"]), (f"{role:<26}", t["fg"]), (f"{fit}  ", t["blue"]), (where, t["dim"])],
            cx, y, fs, "regular") + "</g>")

    els.append(runs([("Resumes and answers drafted. Reply with numbers to apply.", t["dim"])], cx, L(4.4), fs))

    # the user's reply, typed
    ry = L(5.6)
    els.append(text_path("❯", cx, ry, fs, t["green"], "bold"))
    reply = "apply 1 and 3"
    t0, step = 1.6, 0.11
    chars = glyph_paths(reply, cx + cw * 2, ry, fs, "semibold")
    idx = {}
    k = 0
    for i, ch in enumerate(reply):
        if not ch.isspace():
            idx[i] = k
            k += 1
    for i, ch in enumerate(reply):
        if ch.isspace():
            continue
        _, _, d = chars[idx[i]]
        at = (t0 + i * step) / CYCLE * 100
        css.append(f"@keyframes k{i}{{0%,{at:.2f}%{{opacity:0}}{at + .01:.2f}%,100%{{opacity:1}}}}"
                   f".c{i}{{animation:k{i} {CYCLE}s step-end infinite}}")
        els.append(f'<path class="c{i}" fill="{t["fg"]}" d="{d}"/>')

    # cursor: visible only while typing, so the resting frame has none
    cur_x0 = cx + cw * 2
    end_t = t0 + len(reply) * step
    stops = [f"0%{{opacity:1;transform:translateX(0)}}"]
    for i in range(1, len(reply) + 1):
        stops.append(f"{(t0 + (i - 1) * step) / CYCLE * 100 + .01:.2f}%{{opacity:1;transform:translateX({cw * i:.2f}px)}}")
    stops.append(f"{(end_t + .45) / CYCLE * 100:.2f}%,100%{{opacity:0;transform:translateX({cw * len(reply):.2f}px)}}")
    css.append("@keyframes cur{" + "".join(stops) + "}"
               ".cur{opacity:0;animation:cur %ss step-end infinite}" % CYCLE)
    els.append(f'<rect class="cur" x="{cur_x0 + 1}" y="{ry - 15}" width="{cw - 2}" height="19" fill="{t["fg"]}" opacity="0"/>')

    # the agent's answer and the list marking
    ans = (end_t + .7) / CYCLE * 100
    css.append(f"@keyframes ans{{0%,{ans:.2f}%{{opacity:0}}{ans + .01:.2f}%,100%{{opacity:1}}}}"
               f".ans,.pick{{animation:ans {CYCLE}s step-end infinite}}")
    css.append(f"@keyframes skip{{0%,{ans:.2f}%{{opacity:1}}{ans + .01:.2f}%,100%{{opacity:.5}}}}"
               f".skip{{opacity:.5;animation:skip {CYCLE}s step-end infinite}}")
    els.append('<g class="ans">' + check(cx, L(6.6), fs, t["green"]) + runs([
        ("  ", t["green"]), ("Easy Apply sent for 1 and 3", t["fg"]), (" · 2 stays in ready", t["dim"])],
        cx, L(6.6), fs) + "</g>")

    css.append("@media (prefers-reduced-motion:reduce){*{animation:none!important}}")

    defs = ""
    if t["shadow"]:
        defs = '<defs><filter id="blur" x="-5%" y="-10%" width="110%" height="130%"><feGaussianBlur stdDeviation="8"/></filter></defs>'
    title = "hermes-linkedin-jobsearch: the agent lists ready entries, you reply apply 1 and 3"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{defs}'
            f'<style>{"".join(css)}</style>\n' + "\n".join(els) + "\n</svg>\n")


def main():
    for theme in THEMES:
        svg = HERE / f"banner-{theme}.svg"
        svg.write_text(build(theme))
        page = THEMES[theme]["page"]
        preview = HERE.parent / ".tmp" / f"banner-{theme}.png"
        preview.parent.mkdir(exist_ok=True)
        subprocess.run(["rsvg-convert", "-b", page, "-z", "1", "-o",
                        str(preview), str(svg)], check=True)
    # contrast report: text colours against the surface they sit on
    for theme, t in THEMES.items():
        checks = {"title/page": (t["title"], t["page"]), "jobsearch/page": (t["blue"], t["page"]),
                  "tagline/page": (t["sub"], t["page"]), "eyebrow/page": (t["purple"], t["page"]),
                  "fg/win": (t["fg"], t["win"]), "dim/win": (t["dim"], t["win"]),
                  "blue/win": (t["blue"], t["win"]), "amber/win": (t["amber"], t["win"]),
                  "green/win": (t["green"], t["win"]), "border/page": (t["border"], t["page"]),
                  "win/page": (t["win"], t["page"])}
        print(theme, "  ".join(f"{k} {contrast(*v):.1f}" for k, v in checks.items()))


if __name__ == "__main__":
    main()
