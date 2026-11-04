#!/usr/bin/env python3
"""Generate setup-light.svg and setup-dark.svg: a /jobsearch-init session in the chat.

Same palette, chrome and outlined CaskaydiaMono text as the banner (make_banner.py).
Every element rests in its final frame, so a renderer without animation shows the finished scene.
Run: python3 assets/make_setup.py  (writes the SVGs here, PNG previews to .tmp/)
"""
import subprocess

from make_banner import HERE, THEMES, advance, check, contrast, glyph_paths, runs, text_path


W = 880
FS, LH = 16, 26
HOLD = 10.0  # seconds on the final frame before the loop restarts
TYPE = 0.05  # seconds per typed character

# The session. Kinds:
#   cmd    the user's slash command, typed
#   ask    the agent asks: (text, detail)
#   reply  the user's answer, typed
#   done   a progress line: spinner, then a check: (label, detail)
#   gap    half a line of space
#   end    the closing summary: (text, detail)
SCRIPT = [
    ("cmd", "/jobsearch-init"),
    ("gap", None),
    ("done", ("Model, tools, workspace", " · uv, node, git, cratecv found, ~/jobsearch created")),
    ("gap", None),
    ("ask", ("No LinkedIn session yet. Open the login window?", "")),
    ("reply", "yes"),
    ("done", ("LinkedIn", " · logged in, your profile read")),
    ("gap", None),
    ("ask", ("Your CV dates the platform rewrite 2021, LinkedIn says 2022.", " Which is right?")),
    ("reply", "2022, and it halved deploy time"),
    ("done", ("Profile facts", " · 4 experience, 2 education, 26 skills, each sourced")),
    ("done", ("Criteria", " · remote or hybrid, full-time, senior, English and Spanish")),
    ("gap", None),
    ("ask", ("Easy Apply: off, approval or unattended?", " Limit is 2 sends a day")),
    ("reply", "approval, 2 a day is fine"),
    ("done", ("Autonomy", " · Easy Apply on your go, external forms off")),
    ("done", ("Track backend-platform", " · 6 keywords, base resume, market report")),
    ("done", ("Scheduled runs", " · Advance, Tracking, discovery, market report")),
    ("gap", None),
    ("end", ("Setup done, workspace committed.", " First discovery run tomorrow at 07:30.")),
]


class Anim:
    """Collects step-end keyframes in one cycle; elements rest in their final style."""

    def __init__(self):
        self.css, self.n, self.cycle = [], 0, None

    def pct(self, t):
        return t / self.cycle * 100

    def _rule(self, frames, rest):
        self.n += 1
        name = f"a{self.n}"
        self.css.append(f"@keyframes {name}{{{frames}}}.{name}{{{rest}animation:{name} {self.cycle:.1f}s step-end infinite}}")
        return name

    def show(self, t):
        """Hidden until t, then visible to the end."""
        p = self.pct(t)
        return self._rule(f"0%,{p:.2f}%{{opacity:0}}{p + .01:.2f}%,100%{{opacity:1}}", "")

    def window(self, a, b):
        """Visible only from a to b; hidden at rest."""
        pa, pb = self.pct(a), self.pct(b)
        return self._rule(f"0%,{pa:.2f}%{{opacity:0}}{pa + .01:.2f}%,{pb:.2f}%{{opacity:1}}{pb + .01:.2f}%,100%{{opacity:0}}",
                          "opacity:0;")

    def cursor(self, a, step, n, cw):
        """A block cursor shown from a, moving one cell per typed char, gone shortly after."""
        stops = [f"0%,{self.pct(a):.2f}%{{opacity:0;transform:translateX(0)}}",
                 f"{self.pct(a) + .01:.2f}%{{opacity:1;transform:translateX(0)}}"]
        t0 = a + 0.35
        for i in range(1, n + 1):
            stops.append(f"{self.pct(t0 + (i - 1) * step) + .01:.2f}%{{opacity:1;transform:translateX({cw * i:.2f}px)}}")
        end = self.pct(t0 + n * step + 0.35)
        stops.append(f"{end:.2f}%,100%{{opacity:0;transform:translateX({cw * n:.2f}px)}}")
        return self._rule("".join(stops), "opacity:0;")


def timeline():
    """Start time of each SCRIPT line, the typing start of typed lines, and the scene's end."""
    t, times = 0.5, []
    for kind, body in SCRIPT:
        if kind == "cmd":
            times.append(t)
            t += 0.35 + len(body) * TYPE + 0.4
        elif kind == "reply":
            t += 0.3
            times.append(t)
            t += 0.35 + len(body) * TYPE + 0.4
        elif kind == "done":
            times.append(t)
            t += 0.75
        elif kind == "ask":
            times.append(t)
            t += 0.5
        else:
            times.append(t)
            t += 0.15
    return times, t


def build(theme):
    t = THEMES[theme]
    anim = Anim()
    times, end = timeline()
    anim.cycle = end + HOLD
    els = []

    # ---- window --------------------------------------------------------
    bar_h = 32
    rows = sum(0.5 if k == "gap" else 1 for k, _ in SCRIPT)
    H = int(bar_h + 34 + (rows - 1) * LH + 30)
    wx, wy, ww, wh = 10, 8, W - 20, H - 8
    H += 10
    if t["shadow"]:
        els.append(f'<rect x="{wx}" y="{wy + 6}" width="{ww}" height="{wh}" rx="12" '
                   f'fill="#1a1b26" opacity="{t["shadow"]}" filter="url(#blur)"/>')
    els.append(f'<rect x="{wx + .5}" y="{wy + .5}" width="{ww - 1}" height="{wh - 1}" rx="12" '
               f'fill="{t["win"]}" stroke="{t["border"]}"/>')
    els.append(f'<path d="M{wx + .5} {wy + bar_h}V{wy + 12.5}a12 12 0 0 1 12-12H{wx + ww - 12.5}'
               f'a12 12 0 0 1 12 12V{wy + bar_h}Z" fill="{t["bar"]}" stroke="{t["border"]}"/>')
    for i, c in enumerate(("#f7768e", "#e0af68", "#9ece6a")):
        els.append(f'<circle cx="{wx + 22 + i * 20}" cy="{wy + bar_h / 2}" r="6" fill="{c}"/>')
    bt = "jobsearch chat"
    els.append(text_path(bt, wx + ww / 2 - advance(13, len(bt)) / 2, wy + 21, 13, t["dim"]))

    # ---- the session ---------------------------------------------------
    cx = wx + 24
    cw = advance(FS)
    tx = cx + cw * 2  # text column after the 2-cell marker
    y = wy + bar_h + 34

    def typed(text, at, color, weight="semibold"):
        """The prompt, then text revealed char by char from at + 0.35, with a moving cursor."""
        out = [f'<g class="{anim.show(at)}">' + text_path("❯", cx, y, FS, t["green"], "bold") + "</g>"]
        glyphs = iter(glyph_paths(text, tx, y, FS, weight))
        for i, ch in enumerate(text):
            if not ch.isspace():
                _, _, d = next(glyphs)
                out.append(f'<path class="{anim.show(at + 0.35 + i * TYPE)}" fill="{color}" d="{d}"/>')
        cur = anim.cursor(at, TYPE, len(text), cw)
        out.append(f'<rect class="{cur}" x="{tx + 1:.2f}" y="{y - 15}" width="{cw - 2:.2f}" height="19" fill="{t["fg"]}"/>')
        return "\n".join(out)

    for (kind, body), at in zip(SCRIPT, times):
        if kind == "gap":
            y += LH / 2
            continue
        if kind in ("cmd", "reply"):
            els.append(typed(body, at, t["blue"] if kind == "cmd" else t["fg"]))
        elif kind == "ask":
            text, detail = body
            els.append(f'<g class="{anim.show(at)}">' + runs([("▸ ", t["purple"]), (text, t["fg"]), (detail, t["dim"])],
                                                           cx, y, FS) + "</g>")
        elif kind == "done":
            label, detail = body
            els.append(f'<g class="{anim.window(at, at + 0.6)}">' + text_path("◌", cx, y, FS, t["amber"], "bold") + "</g>")
            els.append(f'<g class="{anim.show(at + 0.6)}">' + check(cx, y, FS, t["green"]) + "</g>")
            els.append(f'<g class="{anim.show(at)}">' + runs([(label, t["fg"])], tx, y, FS, "semibold")
                       + runs([(detail, t["dim"])], tx + cw * len(label), y, FS) + "</g>")
        elif kind == "end":
            text, detail = body
            els.append(f'<g class="{anim.show(at)}">' + runs([("▸ ", t["purple"]), (text, t["fg"]), (detail, t["dim"])],
                                                           cx, y, FS) + "</g>")
        y += LH

    css = "".join(anim.css) + "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
    defs = ""
    if t["shadow"]:
        defs = '<defs><filter id="blur" x="-5%" y="-10%" width="110%" height="130%"><feGaussianBlur stdDeviation="8"/></filter></defs>'
    title = ("jobsearch setup: /jobsearch-init logs in to LinkedIn, builds profile facts and criteria, "
             "sets autonomy, creates a first track and schedules the runs")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{defs}'
            f'<style>{css}</style>\n' + "\n".join(els) + "\n</svg>\n")


def main():
    longest = max(len(b) if isinstance(b, str) else len("".join(b)) + 2 for _, b in SCRIPT if b)
    assert longest * advance(FS) <= W - 20 - 48, f"a line of {longest} chars overflows"
    for theme, t in THEMES.items():
        svg = HERE / f"setup-{theme}.svg"
        svg.write_text(build(theme))
        preview = HERE.parent / ".tmp" / f"setup-{theme}.png"
        preview.parent.mkdir(exist_ok=True)
        subprocess.run(["rsvg-convert", "-b", t["page"], "-z", "1", "-o", str(preview), str(svg)], check=True)
        checks = {k: contrast(t[k], t["win"]) for k in ("fg", "dim", "blue", "purple", "green", "amber")}
        checks["title/bar"] = contrast(t["dim"], t["bar"])
        print(theme, "  ".join(f"{k} {v:.1f}" for k, v in checks.items()))
        low = [k for k, v in checks.items() if v < 4.5]
        assert not low, f"{theme}: contrast under 4.5 for {low}"


if __name__ == "__main__":
    main()
