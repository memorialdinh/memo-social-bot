"""Renders branded posts (JPG), stories (JPG) and reels (MP4) from queue items.

Usage:
  python -m bot.render                 # render anything missing in the next few days
  python -m bot.render --all --force   # re-render everything
  python -m bot.render --file queue/2026-10-24/p1.yaml

The look (Oct 28, 2026): luxury editorial. Obsidian, ivory or champagne grounds,
gold-foil accents, hairline rules, wide-tracked small caps, Space Grotesk
headlines, and Memo's cut-out portrait breaking out of a gold-ringed medallion.
Every graphic ends with a "Your next step" CTA button.

Templates (design.template) — see CONTENT_BRIEF.md for the YAML of each:
  tip        headline + 2-5 numbered points                     (save-built)
  process    headline + 3-6 steps, in order, on a timeline       (save-built)
  checklist  questionnaire: 3-6 yes/no questions + a score line  (save-built)
  quiz       one question + 2-4 options; reels reveal the answer
  explainer  education: a term, what it means, why it matters    (save-built)
  compare    A vs B in two columns                               (save-built)
  cta        the offer: what they get + one big next step
  spotlight  agent attraction: one Epique perk / tool / person per post, numbered series
  stat       one big number
  myth       myth vs fact
  meme       setup + punchline (humor track)
  quote      one line (motivation)
"""
from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

import yaml
from datetime import date, timedelta

from .common import ASSETS, CFG, QUEUE, ROOT, Item, load_items, recent_days, stable_int

C = CFG["brand"]["colors"]
OBSIDIAN = C["obsidian"]
GOLD = C["gold"]
CARBON = C["carbon"]
SLATE = C["slate"]
WHITE = "#F6F4F0"

FONT_DIR = ASSETS / "fonts"
_font_cache: dict = {}
_WEIGHTS = {"Thin": 100, "ExtraLight": 200, "Light": 300, "Regular": 400, "Medium": 500,
            "SemiBold": 600, "Bold": 700, "ExtraBold": 800, "Black": 900}

TEMPLATES = ("tip", "process", "checklist", "quiz", "explainer", "compare", "cta", "spotlight",
             "stat", "myth", "meme", "quote")
SAVEABLE = {"tip", "process", "checklist", "explainer", "compare", "spotlight"}
CENTERABLE = {"stat", "quote", "meme"}


def font(family: str, weight: str, size: int) -> ImageFont.FreeTypeFont:
    key = (family, weight, size)
    if key not in _font_cache:
        path = FONT_DIR / ("SpaceGrotesk.ttf" if family == "head" else "Inter.ttf")
        f = ImageFont.truetype(str(path), size)
        wv = _WEIGHTS.get(weight, 400)
        try:
            vals = []
            for ax in f.get_variation_axes():
                name = ax["name"].decode() if isinstance(ax["name"], bytes) else str(ax["name"])
                if "eight" in name:
                    vals.append(max(ax["minimum"], min(ax["maximum"], wv)))
                elif "ptical" in name:          # Inter's optical size: display cut for big type
                    vals.append(max(ax["minimum"], min(ax["maximum"], size * 0.8)))
                else:
                    vals.append(ax["default"])
            f.set_variation_by_axes(vals)
        except Exception:
            try:
                f.set_variation_by_name(weight)
            except Exception:
                pass
        _font_cache[key] = f
    return _font_cache[key]


def template_of(d: dict) -> str:
    t = (d.get("template") or "").strip().lower()
    if t in TEMPLATES:
        return t
    if d.get("stat_value"):
        return "stat"
    if d.get("myth"):
        return "myth"
    if d.get("punch"):
        return "meme"
    if d.get("quote"):
        return "quote"
    if d.get("steps"):
        return "process"
    if d.get("questions"):
        return "checklist"
    if d.get("options"):
        return "quiz"
    if d.get("term"):
        return "explainer"
    if d.get("left") and d.get("right"):
        return "compare"
    if d.get("series_no") or d.get("feature"):
        return "spotlight"
    return "tip"


# ── color + text helpers ─────────────────────────────────────
def _rgb(hexs: str) -> tuple:
    hexs = hexs.lstrip("#")
    return tuple(int(hexs[i:i + 2], 16) for i in (0, 2, 4))


def rgba(hexs, a: int) -> tuple:
    return (_rgb(hexs) if isinstance(hexs, str) else tuple(hexs[:3])) + (a,)


def _strip(n: int, stops) -> list:
    cols = [_rgb(s) for s in stops]
    k = len(cols) - 1
    out = []
    for i in range(max(n, 1)):
        x = i / max(1, n - 1) * k
        j = min(int(x), k - 1)
        f = x - j
        out.append(tuple(int(cols[j][c] + (cols[j + 1][c] - cols[j][c]) * f) for c in range(3)))
    return out


def gradient(w: int, h: int, stops, horizontal: bool = False, period: int | None = None) -> Image.Image:
    """Gold/silver foil: a soft multi-stop gradient. `period` repeats it (one per text line)."""
    n = period or (w if horizontal else h)
    strip = _strip(n, stops)
    if horizontal:
        im = Image.new("RGB", (w, 1))
        im.putdata([strip[x % n] for x in range(w)])
        return im.resize((w, max(h, 1)), Image.NEAREST).convert("RGBA")
    im = Image.new("RGB", (1, h))
    im.putdata([strip[y % n] for y in range(h)])
    return im.resize((max(w, 1), h), Image.NEAREST).convert("RGBA")


def foil_fill(mask: Image.Image, stops, period: int | None = None, horizontal=False) -> Image.Image:
    g = gradient(mask.width, mask.height, stops, horizontal, period)
    g.putalpha(mask)
    return g


_EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️‍]")


def tokens(text: str):
    """Split '*gold words*' markup into words; each word is a list of (text, is_gold) runs."""
    text = _EMOJI.sub("", str(text))
    words, cur, gold = [], [], False
    buf = ""
    for ch in text:
        if ch == "*":
            if buf:
                cur.append((buf, gold)); buf = ""
            gold = not gold
        elif ch.isspace():
            if buf:
                cur.append((buf, gold)); buf = ""
            if cur:
                words.append(cur); cur = []
        else:
            buf += ch
    if buf:
        cur.append((buf, gold))
    if cur:
        words.append(cur)
    return words


def _wlen(f, word):
    return sum(f.getlength(t) for t, _ in word)


def wrap(text: str, f, max_w: int):
    lines, cur, cur_w = [], [], 0
    space = f.getlength(" ")
    for word in tokens(text):
        ww = _wlen(f, word)
        if cur and cur_w + space + ww > max_w:
            lines.append(cur)
            cur, cur_w = [], 0
        cur_w += (space if cur else 0) + ww
        cur.append(word)
    if cur:
        lines.append(cur)
    return lines


def text_layer(text, f, max_w, color=WHITE, gold=GOLD, line_gap=1.12, align="left",
               hl=None, hl_fg=None, foil=None):
    """Wrapped text. *starred* words are gold: foil gradient when the theme has
    one, a solid accent otherwise, or a highlight box on champagne grounds."""
    lines = wrap(text, f, max_w)
    asc, desc = f.getmetrics()
    lh = int((asc + desc) * line_gap)
    w = max_w
    h = lh * max(len(lines), 1) + int(desc * 0.4) + 4
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    mask = Image.new("L", img.size, 0) if foil else None
    md = ImageDraw.Draw(mask) if foil else None
    space = f.getlength(" ")
    for i, line in enumerate(lines):
        lw = sum(_wlen(f, wd) for wd in line) + space * (len(line) - 1)
        x = (w - lw) / 2 if align == "center" else 0
        for wi, wd in enumerate(line):
            for t, g in wd:
                tw = f.getlength(t)
                if g and hl:
                    nxt_gold = wi + 1 < len(line) and line[wi + 1][0][1] and t is wd[-1][0]
                    pad = asc * 0.10
                    d.rectangle((x - pad, i * lh + asc * 0.10, x + tw + (space if nxt_gold else pad),
                                 i * lh + asc + desc * 0.5), fill=hl)
                    d.text((x, i * lh), t, font=f, fill=hl_fg or gold)
                elif g and foil:
                    md.text((x, i * lh), t, font=f, fill=255)
                else:
                    d.text((x, i * lh), t, font=f, fill=gold if g else color)
                x += tw
            x += space
    if foil and mask.getbbox():
        img.alpha_composite(foil_fill(mask, foil, period=lh))
    return img, len(lines)


def fit_text(text, family, weight, max_w, max_lines, start, minimum, **kw):
    size = start
    while size >= minimum:
        f = font(family, weight, size)
        img, n = text_layer(text, f, max_w, **kw)
        if n <= max_lines:
            return img
        size -= 4
    return text_layer(text, font(family, weight, minimum), max_w, **kw)[0]


def text_width(text, f) -> int:
    return int(sum(_wlen(f, w) for w in tokens(text)) + f.getlength(" ") * max(0, len(tokens(text)) - 1))


def caps(text, f, fill, letter=4, foil=None) -> Image.Image:
    """Wide-tracked small caps — the luxury label style."""
    s = _EMOJI.sub("", str(text)).upper()
    widths = [f.getlength(ch) for ch in s]
    tw = sum(widths) + letter * max(0, len(s) - 1)
    asc, desc = f.getmetrics()
    img = Image.new("RGBA", (int(tw) + 4, asc + desc + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = 0
    for ch, cw in zip(s, widths):
        d.text((x, 0), ch, font=f, fill=fill)
        x += cw + letter
    if foil:
        return foil_fill(img.getchannel("A"), foil, horizontal=True)
    return img


SS = 3  # supersampling for smooth shapes


def shape(w: int, h: int, fn) -> Image.Image:
    big = Image.new("RGBA", (max(1, w) * SS, max(1, h) * SS), (0, 0, 0, 0))
    fn(ImageDraw.Draw(big), SS)
    return big.resize((max(1, w), max(1, h)), Image.LANCZOS)


def hairline(w: int, color, thick: int = 2) -> Image.Image:
    return Image.new("RGBA", (max(1, w), thick), color)


def vline(h: int, color, thick: int = 2) -> Image.Image:
    return Image.new("RGBA", (thick, max(1, h)), color)


def check_icon(size: int, fg, bg=None, ring=None) -> Image.Image:
    def draw(d, k):
        if bg:
            d.ellipse((0, 0, size * k - 1, size * k - 1), fill=bg)
        if ring:
            d.ellipse((k, k, (size - 1) * k, (size - 1) * k), outline=ring, width=2 * k)
        s = size * k
        d.line([(s * 0.28, s * 0.52), (s * 0.44, s * 0.67), (s * 0.73, s * 0.35)], fill=fg,
               width=max(2, int(s * 0.085)), joint="curve")
    return shape(size, size, draw)


def cross_icon(size: int, fg, ring=None) -> Image.Image:
    def draw(d, k):
        if ring:
            d.ellipse((k, k, (size - 1) * k, (size - 1) * k), outline=ring, width=2 * k)
        s = size * k
        wdt = max(2, int(s * 0.07))
        d.line([(s * 0.34, s * 0.34), (s * 0.66, s * 0.66)], fill=fg, width=wdt)
        d.line([(s * 0.66, s * 0.34), (s * 0.34, s * 0.66)], fill=fg, width=wdt)
    return shape(size, size, draw)


def bookmark_icon(size: int, fg) -> Image.Image:
    def draw(d, k):
        s = size * k
        d.polygon([(s * 0.22, s * 0.08), (s * 0.78, s * 0.08), (s * 0.78, s * 0.92), (s * 0.5, s * 0.7),
                   (s * 0.22, s * 0.92)], outline=fg, width=max(2, int(s * 0.09)))
    return shape(size, size, draw)


# ── themes: a different look every post, always on-brand ─────
@dataclass
class Theme:
    name: str
    bg: str           # base ground
    bg2: str          # ground gradient end (bottom)
    glow: tuple       # rgb of the soft light
    fg: str           # headline
    body: str         # body text
    accent: str       # solid accent (labels, rules, icons)
    foil: tuple | None  # gradient stops for gold words / big numbers
    cta_bg: str
    cta_fg: str
    cta_foil: bool    # foil-filled CTA button
    muted: str        # microtext
    ring: str         # medallion ring
    plate: str        # medallion disc
    light: bool = False
    hl: str | None = None     # highlight box behind accent words (champagne ground)
    hl_fg: str | None = None
    invert: bool = False      # headline set in foil, starred words in white (aurum)

    @property
    def line(self):
        return rgba(self.accent, 150 if self.light else 120)

    @property
    def line_soft(self):
        return rgba(self.accent, 70 if self.light else 55)


GOLD_FOIL = ("#f5e6c4", "#e2c999", "#bca480", "#8f7752", "#b59c74")
SILVER_FOIL = ("#ffffff", "#e3e5e8", "#c3c7cc", "#878b92", "#b9bdc3")
DEEP_FOIL = ("#b89c68", "#a2875a", "#8d7650", "#6a5534", "#8a7148")
GRAPHITE_FOIL = ("#a4a8ae", "#8a8e95", "#6d7177", "#4f5258", "#666a70")

THEMES = [
    Theme("noir", "#0b0b0b", "#151412", (188, 164, 128), WHITE, "#d2cdc4", GOLD, GOLD_FOIL,
          GOLD, OBSIDIAN, True, "#8b887f", GOLD, "#1d1c1a"),
    Theme("silver", "#0b0c0e", "#16181b", (200, 204, 210), WHITE, "#c8cbd0", "#c9ccd1", SILVER_FOIL,
          "#c9ccd1", OBSIDIAN, True, "#80848b", "#c9ccd1", "#1c1e21"),
    Theme("ivory", "#f5f1ea", "#e6dfd2", (188, 164, 128), OBSIDIAN, "#3a3833", "#8d7650", DEEP_FOIL,
          OBSIDIAN, "#d8c39b", False, "#77746c", GOLD, "#e4dccd", light=True),
    Theme("goldrush", "#cdb48d", "#a98f68", (255, 244, 222), OBSIDIAN, "#221e18", OBSIDIAN, None,
          OBSIDIAN, "#e8d6b0", False, "#4a4135", OBSIDIAN, "#b8a07a", light=True,
          hl=OBSIDIAN, hl_fg="#e8d6b0"),
    Theme("graphite", "#1a1a19", "#232321", (188, 164, 128), WHITE, CARBON, GOLD, GOLD_FOIL,
          WHITE, OBSIDIAN, False, "#87867f", GOLD, "#2b2b29"),
    Theme("slate", "#3b3b38", "#2b2b29", (188, 164, 128), WHITE, "#e0dcd4", "#d0b98f", GOLD_FOIL,
          GOLD, OBSIDIAN, True, "#a9a69e", GOLD, "#4a4a46"),
    Theme("carbon", "#dedbd6", "#ccc8c1", (255, 255, 255), OBSIDIAN, "#2f2e2b", "#7d6a48", DEEP_FOIL,
          OBSIDIAN, "#d8c39b", False, "#5f5d57", OBSIDIAN, "#cbc6bd", light=True),
    Theme("aurum", "#080808", "#141210", (188, 164, 128), WHITE, "#cfc9bf", GOLD, GOLD_FOIL,
          WHITE, OBSIDIAN, False, "#8a867d", GOLD, "#1b1a18", invert=True),
    Theme("porcelain", "#fbfaf8", "#ecebe7", (201, 204, 209), OBSIDIAN, "#33343a", "#6d7177", GRAPHITE_FOIL,
          OBSIDIAN, "#e3e5e8", False, "#75787e", "#8a8e95", "#e4e4e1", light=True),
]
DECOS = ["glow", "frame", "arcs", "monogram", "beam", "grid", "corners", "rules", "halo", "split", "dots"]


# ── no repeats: every new graphic gets a look its platform hasn't used lately ──
HISTORY_DAYS = 14
_stamp_cache: dict = {}


def _pool(kind: str) -> str:
    return "story" if kind == "story" else "feed"


def _stamps_in(path: Path) -> tuple[str, dict]:
    """(kind, rendered-stamps) for one queue file, cached by modification time."""
    try:
        mt = path.stat().st_mtime
    except FileNotFoundError:
        return "post", {}
    hit = _stamp_cache.get(path)
    if hit and hit[0] == mt:
        return hit[1], hit[2]
    try:
        with open(path, encoding="utf-8") as f:
            d = yaml.safe_load(f) or {}
    except Exception:
        d = {}
    kind, rend = d.get("kind", "post"), d.get("rendered") or {}
    _stamp_cache[path] = (mt, kind, rend)
    return kind, rend


def _history(item: Item, platform: str) -> list[dict]:
    """Looks this platform already got in the same pool (feed or stories), oldest
    first, in posting order: earlier days, then earlier items the same day."""
    pool = _pool(item.kind)
    out = []
    if not QUEUE.exists():
        return out
    first = item.day - timedelta(days=HISTORY_DAYS)
    for ddir in sorted(QUEUE.iterdir()):
        try:
            dd = date.fromisoformat(ddir.name)
        except ValueError:
            continue
        if dd < first or dd > item.day:
            continue
        for f in sorted(ddir.glob("*.yaml")):
            if f.resolve() == item.path.resolve():
                continue
            kind, rend = _stamps_in(f)
            st = rend.get(platform)
            if _pool(kind) == pool and isinstance(st, dict) and st.get("theme"):
                out.append(st)
    return out


def _sig(st: dict) -> tuple:
    return (st.get("theme"), st.get("deco"), st.get("side"), st.get("center"))


def _choose_style(item: Item, platform: str, template: str) -> dict:
    d = item.d.get("design") or {}
    forced = d.get("theme")
    themes = [t for t in THEMES if t.name == forced] or THEMES
    centers = (True, False) if template in CENTERABLE else (False,)
    # reels/TikTok: the app's like/comment buttons run down the right edge, so the
    # portrait always sits on the left there
    video = item.kind == "reel" or platform == "tiktok"
    sides = ("left",) if video else ("right", "left")
    cands = [(th.name, deco, side, ctr) for th in themes for deco in DECOS
             for side in sides for ctr in centers]
    hist = _history(item, platform)
    last_used: dict = {}
    for i, st in enumerate(hist):
        if st.get("side") is None:                 # stamp from before Oct 28: theme + accent only
            for c in cands:
                if c[0] == st.get("theme") and c[1] == st.get("deco"):
                    last_used[c] = i
        else:
            last_used[_sig(st)] = i
    prev_themes = [st.get("theme") for st in hist[-2:]]
    prev_deco = hist[-1].get("deco") if hist else None
    siblings = {st.get("theme") for p, st in (item.d.get("rendered") or {}).items()
                if p != platform and isinstance(st, dict)}
    rules = [
        lambda c: c not in last_used and c[0] not in prev_themes and c[0] not in siblings and c[1] != prev_deco,
        lambda c: c not in last_used and c[0] not in prev_themes[-1:] and c[0] not in siblings,
        lambda c: c not in last_used and c[0] not in prev_themes[-1:],
        lambda c: c[0] not in prev_themes[-1:],
        lambda c: True,
    ]
    for rule in rules:
        ok = [c for c in cands if rule(c)]
        if ok:
            break
    ok.sort(key=lambda c: (last_used.get(c, -1), stable_int(item.day, item.id, platform, *c)))
    th, deco, side, ctr = ok[0]
    return {"theme": th, "deco": deco, "side": side, "center": ctr}


def pick_style(item: Item, platform: str, template: str | None = None) -> dict:
    """The look for this platform's version of this item. Chosen once, then kept in
    the item's `rendered` stamp so a re-render (and analytics) see the same look.
    New looks never repeat one this platform used in the last two weeks, never
    share a color with the previous two posts, and differ from the same post's
    version on the other platforms."""
    d = item.d.get("design") or {}
    template = template or template_of(d)
    st = (item.d.get("rendered") or {}).get(platform)
    if not (isinstance(st, dict) and st.get("side") and st.get("theme") in {t.name for t in THEMES}
            and st.get("deco") in DECOS and st.get("template") == template):
        st = _choose_style(item, platform, template)
        st["template"] = template
        item.d.setdefault("rendered", {})[platform] = st
    th = next(t for t in THEMES if t.name == st["theme"])
    return {"theme": th, "deco": st["deco"], "side_right": st["side"] == "right",
            "center": bool(st.get("center")) and template in CENTERABLE}


PLATFORMS_ORDER = ("instagram", "facebook", "linkedin", "tiktok")


# ── assets ───────────────────────────────────────────────────
def pick_headshot(item: Item, platform: str) -> Path | None:
    """ONE consistent headshot on everything (config: headshots.primary)."""
    hdir = ASSETS / "headshots"
    forced = (item.d.get("design") or {}).get("headshot") or (CFG.get("headshots") or {}).get("primary")
    if forced and (hdir / forced).exists():
        return hdir / forced
    files = sorted(p for p in hdir.glob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"))
    return files[0] if files else None


def medallion(path: Path | None, size: int, th: Theme) -> Image.Image:
    """Memo's portrait in a gold-ringed disc. A cut-out PNG breaks out of the top
    of the ring (head over the ring) for depth; a normal photo sits inside it."""
    S = size
    H = int(S * 1.22)
    top = H - S
    out = Image.new("RGBA", (S, H), (0, 0, 0, 0))

    def disc(d, k):
        d.ellipse((0, 0, S * k - 1, S * k - 1), fill=th.plate)
    out.alpha_composite(shape(S, S, disc), (0, top))
    # soft light inside the disc
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((S * 0.15, S * 0.05, S * 0.85, S * 0.75), fill=th.glow + (60,))
    glow = glow.filter(ImageFilter.GaussianBlur(S * 0.12))
    cmask = shape(S, S, lambda d, k: d.ellipse((0, 0, S * k - 1, S * k - 1), fill=(255, 255, 255, 255))).getchannel("A")
    g2 = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    g2.paste(glow, (0, 0), cmask)
    out.alpha_composite(g2, (0, top))

    def ring(d, k):
        d.ellipse((2 * k, 2 * k, (S - 2) * k, (S - 2) * k), outline=th.ring, width=3 * k)
    out.alpha_composite(shape(S, S, ring), (0, top))

    if not path:
        f = font("head", "Bold", S // 3)
        ImageDraw.Draw(out).text((S / 2, top + S / 2), "MD", font=f, fill=th.accent, anchor="mm")
        return out
    im = Image.open(path).convert("RGBA")
    cut = im.getchannel("A").getextrema()[0] < 250
    person = Image.new("RGBA", (S, H), (0, 0, 0, 0))
    mask = Image.new("L", (S, H), 0)
    if cut:
        pw = int(S * 1.16)
        pim = im.resize((pw, int(im.height * pw / im.width)), Image.LANCZOS)
        person.paste(pim, ((S - pw) // 2, H - pim.height), pim)
        mask.paste(cmask, (0, top))
        # only the head rises above the ring: a soft-edged column over the centre,
        # so shoulders and arms always stay inside the circle
        col = Image.new("L", (S, H), 0)
        ImageDraw.Draw(col).rounded_rectangle((int(S * 0.27), 0, int(S * 0.73), top + int(S * 0.22)),
                                              radius=int(S * 0.2), fill=255)
        mask = ImageChops.lighter(mask, col)
    else:
        inner = S - 12
        pim = ImageOps.fit(im, (inner, inner), centering=(0.5, 0.3))
        person.paste(pim, (6, top + 6))
        mask.paste(cmask.resize((inner, inner)), (6, top + 6))
    pa = person.getchannel("A")
    person.putalpha(ImageChops.multiply(pa, mask))
    out.alpha_composite(person)
    # the ring sits in FRONT of the shoulders (so it reads as a full circle) and
    # BEHIND the head only, where the head rises over the top of it
    ring_img = Image.new("RGBA", (S, H), (0, 0, 0, 0))
    ring_img.alpha_composite(shape(S, S, ring), (0, top))
    if cut:
        head = Image.new("L", (S, H), 0)
        head.paste(person.getchannel("A").crop((0, 0, S, top + int(S * 0.22))), (0, 0))
        keep = ImageChops.invert(head.point(lambda v: 255 if v > 40 else 0))
        ring_img.putalpha(ImageChops.multiply(ring_img.getchannel("A"), keep))
    out.alpha_composite(ring_img)
    return out


def logo_layer(height: int, th: Theme) -> Image.Image:
    """Epique POWER mark + wordmark lockup. The mark is only ever scaled, never reshaped."""
    names = ("logo-black.png", "logo.png") if th.light else ("logo-white.png", "logo-gold.png", "logo.png")
    ink = OBSIDIAN if th.light else CARBON
    mark = None
    for name in names:
        p = ASSETS / "logos" / name
        if p.exists():
            im = Image.open(p).convert("RGBA")
            mh = int(height * 1.12)
            mark = im.resize((max(1, int(im.width * mh / im.height)), mh), Image.LANCZOS)
            break
    word = caps("EPIQUE REALTY", font("head", "Medium", int(height * 0.5)), ink, letter=6)
    if mark is None:
        return word
    gap = int(height * 0.38)
    w = mark.width + gap + word.width
    h = max(mark.height, word.height)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.alpha_composite(mark, (0, (h - mark.height) // 2))
    out.alpha_composite(word, (mark.width + gap, (h - word.height) // 2))
    return out


# ── background ───────────────────────────────────────────────
def background(w: int, h: int, th: Theme, deco: str, variant: int) -> Image.Image:
    b1, b2 = _rgb(th.bg), _rgb(th.bg2)
    glow = th.glow
    sw, sh = 60, int(60 * h / w)
    cx = sw * (0.88 if variant % 2 == 0 else 0.12)
    cy = sh * (-0.04 if deco != "arcs" else 0.95)
    r = sw * (1.1 if deco == "glow" else 0.85)
    strength = (0.20 if deco == "glow" else 0.11) * (0.6 if th.light else 1.0)
    vig = 0.0 if th.light else 0.28
    small = Image.new("RGB", (sw, sh))
    px = []
    for yy in range(sh):
        fy = yy / max(1, sh - 1)
        base = tuple(b1[c] + (b2[c] - b1[c]) * fy for c in range(3))
        for xx in range(sw):
            dist = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5 / r
            k = max(0.0, 1 - dist) ** 2 * strength
            ex = ((xx / sw - 0.5) ** 2 + (fy - 0.5) ** 2) ** 0.5
            v = 1 - vig * max(0.0, ex - 0.35) * 2.2
            px.append(tuple(int((base[c] + (glow[c] - base[c]) * k) * v) for c in range(3)))
    small.putdata(px)
    bg = small.resize((w, h), Image.BICUBIC).convert("RGBA")

    acc = _rgb(th.accent)
    K = 2
    ov = Image.new("RGBA", (w * K, h * K), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    if deco == "frame":
        a1, a2 = (150, 90) if th.light else (130, 70)
        o, i2 = 18, 26
        d.rectangle((o * K, o * K, (w - o - 1) * K, (h - o - 1) * K), outline=acc + (a1,), width=2 * K)
        d.rectangle((i2 * K, i2 * K, (w - i2 - 1) * K, (h - i2 - 1) * K), outline=acc + (a2,), width=1 * K)
        for (x, y) in ((o, o), (w - o - 1, o), (o, h - o - 1), (w - o - 1, h - o - 1)):
            d.rectangle(((x - 4) * K, (y - 4) * K, (x + 4) * K, (y + 4) * K), fill=acc + (220,))
    elif deco == "arcs":
        cxp = w if variant % 2 == 0 else 0
        for i, rr in enumerate(range(220, 1100, 105)):
            d.ellipse(((cxp - rr) * K, (h * 0.40 - rr) * K, (cxp + rr) * K, (h * 0.40 + rr) * K),
                      outline=acc + (max(8, 46 - i * 4),), width=K)
    elif deco == "grid":
        for x in range(0, w, 72):
            d.line((x * K, 0, x * K, h * K), fill=acc + (12,), width=1)
        for y in range(0, h, 72):
            d.line((0, y * K, w * K, y * K), fill=acc + (12,), width=1)
    elif deco == "monogram":
        f = font("head", "Light", int(h * 0.78) * K)
        d.text(((w * (0.50 if variant % 2 == 0 else -0.12)) * K, (h * 0.12) * K), "P", font=f,
               fill=acc + (13 if not th.light else 16,))
    elif deco == "beam":
        x0 = w * (0.62 if variant % 2 == 0 else 0.02)
        d.polygon([((x0) * K, -10), ((x0 + 260) * K, -10), ((x0 - 160) * K, h * K), ((x0 - 420) * K, h * K)],
                  fill=th.glow + (40 if not th.light else 34,))
    elif deco == "corners":
        L, o = 74, 30
        for (x, y, sx, sy) in ((o, o, 1, 1), (w - o, o, -1, 1), (o, h - o, 1, -1), (w - o, h - o, -1, -1)):
            d.line((x * K, y * K, (x + L * sx) * K, y * K), fill=acc + (230,), width=3 * K)
            d.line((x * K, y * K, x * K, (y + L * sy) * K), fill=acc + (230,), width=3 * K)
    elif deco == "rules":
        for y in (30, 40, h - 41, h - 31):
            d.line((30 * K, y * K, (w - 30) * K, y * K), fill=acc + (150 if y in (30, h - 31) else 80,), width=K)
    elif deco == "halo":
        cxp = w * (0.86 if variant % 2 == 0 else 0.14)
        cyp = h * 0.80
        for i, rr in enumerate((300, 360, 430)):
            d.ellipse(((cxp - rr) * K, (cyp - rr) * K, (cxp + rr) * K, (cyp + rr) * K),
                      outline=acc + (60 - i * 16,), width=(3 - i) * K if i < 2 else K)
    elif deco == "split":
        tone = _rgb(th.bg2)
        k = -14 if not th.light else 12
        tone = tuple(max(0, min(255, v + k)) for v in tone)
        if variant % 2 == 0:
            d.polygon([(w * 0.58 * K, 0), (w * K, 0), (w * K, h * K), (w * 0.30 * K, h * K)], fill=tone + (150,))
        else:
            d.polygon([(0, 0), (w * 0.42 * K, 0), (w * 0.70 * K, h * K), (0, h * K)], fill=tone + (150,))
    elif deco == "dots":
        x0 = w * 0.55 if variant % 2 == 0 else 0
        for gx in range(int(x0), int(x0 + w * 0.45), 34):
            for gy in range(0, int(h * 0.42), 34):
                fade = max(0.0, 1 - gy / (h * 0.42))
                r = 2
                d.ellipse(((gx - r) * K, (gy - r) * K, (gx + r) * K, (gy + r) * K),
                          fill=acc + (int(70 * fade) if not th.light else int(90 * fade),))
    ov = ov.resize((w, h), Image.LANCZOS)
    if deco == "beam":
        ov = ov.filter(ImageFilter.GaussianBlur(70))
    bg = Image.alpha_composite(bg, ov)
    # fine grain: the matte, printed feel of a luxury card
    grain = Image.effect_noise((w, h), 40).convert("RGBA")
    grain.putalpha(9 if not th.light else 7)
    return Image.alpha_composite(bg, grain)


# ── layout ───────────────────────────────────────────────────
@dataclass
class Layer:
    img: Image.Image
    x: int
    y: int
    t: float = 0.0       # reveal time (seconds) in reels
    anim: str = "up"     # up | fade | pop | wipe | count
    color: str = GOLD
    maker: Callable | None = None   # count-up frames for big numbers


@dataclass
class Ctx:
    th: Theme
    d: dict
    m: int
    inner: int
    tall: bool
    video: bool
    story: bool
    align: str
    center: bool
    S: Callable
    out: list


def default_cta(item: Item, template: str, d: dict) -> str:
    if template == "quiz":
        n = len((d.get("options") or [])[:4]) or 3
        letters = "ABCD"[:n]
        return f"Comment {', '.join(letters[:-1])} or {letters[-1]}"
    return (CFG.get("default_cta") or {}).get(item.track) or "DM me your question"


def layout(item: Item, platform: str, w: int, h: int, variant: int, video: bool = False):
    sc = 1.0
    while True:
        bg, layers, t, overflow = _layout(item, platform, w, h, variant, video, sc)
        if not overflow or sc < 0.60:
            return bg, layers, t
        sc -= 0.05


def _layout(item: Item, platform: str, w: int, h: int, variant: int, video: bool, sc: float):
    S = lambda v: max(1, int(v * sc))
    d = item.d.get("design") or {}
    template = template_of(d)
    st = pick_style(item, platform, template)
    th: Theme = st["theme"]
    tall = h > w * 1.4
    reel = video and tall
    m = 96 if tall else 88
    mr = 150 if reel else m            # keep clear of a reel's right-hand buttons
    inner = w - m - mr
    top = 190 if tall else 64          # stories/reels: under the profile bar
    center = st["center"]
    align = "center" if center else "left"
    head: list[Layer] = []
    content: list[Layer] = []
    foot: list[Layer] = []

    # header: Epique lockup + team name, hairline under
    logo = logo_layer(50 if tall else 44, th)
    team = caps(CFG["brand"]["team"], font("body", "SemiBold", 22 if tall else 19), th.accent, 6)
    if center:
        head.append(Layer(logo, (w - logo.width) // 2, top, 0.0, "fade"))
        y = top + logo.height + 16
        head.append(Layer(team, (w - team.width) // 2, y, 0.1, "fade"))
        y += team.height + 20
        r = hairline(130, th.line, 2)
        head.append(Layer(r, (w - r.width) // 2, y, 0.2, "wipe"))
    else:
        head.append(Layer(logo, m, top, 0.0, "fade"))
        if inner - logo.width > team.width + 30:
            head.append(Layer(team, m + inner - team.width, top + (logo.height - team.height) // 2, 0.1, "fade"))
        y = top + logo.height + 24
        head.append(Layer(hairline(inner, th.line, 2), m, y, 0.2, "wipe"))
    y += 2 + S(46 if tall else 38)

    ctx = Ctx(th, dict(d, _track=item.track), m, inner, tall, video, item.kind == "story", align, center, S,
              content)
    t = 0.4

    # kicker row: — LABEL ............ [bookmark] SAVE THIS
    track_label = CFG["tracks"].get(item.track, {}).get("label", item.track.upper())
    kf = font("body", "SemiBold", 24 if tall else 21)
    kcap = caps(d.get("kicker") or track_label, kf, th.accent, 7)
    dash = hairline(44, rgba(th.accent, 255), 2)
    if center:
        krow = Image.new("RGBA", (kcap.width + 2 * (44 + 18), kcap.height), (0, 0, 0, 0))
        krow.alpha_composite(dash, (0, kcap.height // 2 - 2))
        krow.alpha_composite(kcap, (44 + 18, 0))
        krow.alpha_composite(dash, (44 + 18 + kcap.width + 18, kcap.height // 2 - 2))
        content.append(Layer(krow, (w - krow.width) // 2, y, t))
    else:
        krow = Image.new("RGBA", (inner, kcap.height), (0, 0, 0, 0))
        krow.alpha_composite(dash, (0, kcap.height // 2 - 2))
        krow.alpha_composite(kcap, (44 + 18, 0))
        if template == "spotlight" and d.get("series_no"):
            sf = font("head", "Medium", 22 if tall else 19)
            no = d["series_no"]
            badge = caps(f"No. {int(no):02d}" if str(no).isdigit() else str(no), sf, th.accent, 4, foil=th.foil)
            krow.alpha_composite(badge, (inner - badge.width, (kcap.height - badge.height) // 2))
        elif template in SAVEABLE and not ctx.story:
            sf = font("body", "SemiBold", 18 if tall else 16)
            scap = caps("Save this", sf, th.muted, 5)
            bm = bookmark_icon(scap.height + 6, th.muted)
            sx = inner - scap.width - bm.width - 10
            if sx > 44 + 18 + kcap.width + 30:
                krow.alpha_composite(bm, (sx, (kcap.height - bm.height) // 2))
                krow.alpha_composite(scap, (sx + bm.width + 10, (kcap.height - scap.height) // 2))
        content.append(Layer(krow, m, y, t))
    y += kcap.height + S(28 if tall else 22)
    t += 0.4

    tl = dict(color=th.fg, gold=th.accent, hl=th.hl, hl_fg=th.hl_fg, foil=th.foil)
    n_items = len(d.get("steps") or d.get("questions") or d.get("points") or d.get("options") or [])
    head_start = 84 if (template in ("process", "compare", "explainer") or n_items >= 4) else 96
    headline = d.get("headline") or item.d.get("topic", "")
    if template == "quiz" and not d.get("headline"):
        headline = d.get("question") or headline
    if th.invert:
        headline = f"*{headline}*"   # whole line in foil, the starred words flip to white
    if not (template == "quote" and d.get("quote")):
        hi = fit_text(headline, "head", "Bold", inner, 4 if tall else 3, S((118 if head_start == 96 else 100) if tall else head_start), S(54),
                      line_gap=1.05, align=align, **tl)
        content.append(Layer(hi, m, y, t))
        y += hi.height + S(10)
        t += 0.8
    sub = d.get("subhead") or d.get("body")
    if sub:
        si, _ = text_layer(sub, font("body", "Regular", S(40 if tall else 31)), inner, color=th.body,
                           gold=th.accent, foil=th.foil, hl=th.hl, hl_fg=th.hl_fg, align=align, line_gap=1.32)
        content.append(Layer(si, m, y + S(8), t))
        y += si.height + S(8)
        t += 0.5
    y += S(34 if tall else 28)

    body = BODIES.get(template)
    if body:
        y, t = body(ctx, y, t)
    if template in ("stat", "myth", "meme", "quote", "explainer", "quiz") and d.get("points"):
        y, t = body_points(ctx, d["points"], y, t)

    # ── footer: medallion + next-step CTA + name ──
    footer_bottom = h - (300 if tall else 64)
    hs = 250 if tall else 196
    med = medallion(pick_headshot(item, platform), hs, th)
    col_w = inner - hs - 40
    side_right = st["side_right"]
    col_x = m if side_right else m + hs + 40
    med_x = m + inner - hs if side_right else m

    lbl = caps("Your next step", font("body", "SemiBold", 19 if tall else 16), th.muted, 5)
    btn = cta_button(d.get("cta") or default_cta(item, template, d), col_w, th, tall)
    subl = None
    if d.get("cta_sub"):
        subl, _ = text_layer(d["cta_sub"], font("body", "Regular", 22 if tall else 19), col_w,
                             color=th.muted, gold=th.accent)
    nm = caps(CFG["brand"]["name"], font("head", "Bold", 38 if tall else 31), th.fg, 3)
    l2, _ = text_layer(f'{CFG["brand"]["title"]}  ·  {CFG["brand"]["brokerage"]}',
                       font("body", "Regular", 23 if tall else 20), col_w, color=th.body)
    site = CFG["brand"]["agent_site"] if item.track == "agent_attraction" else CFG["brand"]["website"]
    l3, _ = text_layer(f'{CFG["brand"]["phone"]}  ·  {site}', font("body", "Medium", 23 if tall else 20),
                       col_w, color=th.accent)
    gap1, gap2 = (14, 26) if tall else (10, 20)
    col_h = (lbl.height + gap1 + btn.height + (subl.height + 4 if subl else 0) + gap2 + nm.height + 6
             + l2.height - 4 + l3.height)
    zone_h = max(col_h, med.height - 10)
    footer_top = footer_bottom - zone_h - (30 if tall else 24)
    foot.append(Layer(hairline(inner, th.line, 2), m, footer_top, 0.25, "wipe"))
    foot.append(Layer(med, med_x, footer_bottom - med.height, 0.3, "pop"))
    cy = footer_top + (30 if tall else 24) + (zone_h - col_h) // 2
    foot.append(Layer(lbl, col_x, cy, t + 0.1, "fade"))
    cy += lbl.height + gap1
    foot.append(Layer(btn, col_x, cy, t + 0.2, "pop"))
    cy += btn.height
    if subl:
        foot.append(Layer(subl, col_x, cy + 4, t + 0.3, "fade"))
        cy += subl.height + 4
    cy += gap2
    foot.append(Layer(nm, col_x, cy, 0.5, "fade"))
    cy += nm.height + 6
    foot.append(Layer(l2, col_x, cy, 0.6, "fade"))
    cy += l2.height - 4
    foot.append(Layer(l3, col_x, cy, 0.7, "fade"))
    t += 1.0

    mf = font("body", "Regular", 21 if tall else 18)
    micro = (f'{CFG["brand"]["name"]}  ·  CA DRE #{CFG["brand"]["dre"]}  ·  {CFG["brand"]["brokerage"]}'
             f'  ·  Equal Housing Opportunity')
    mim, _ = text_layer(micro, mf, w - 2 * m, color=th.muted, align="center")
    foot.append(Layer(mim, m, (footer_bottom + 26) if tall else (h - 50), 0.0, "fade"))

    if tall and not video:
        # stories: the bottom strip sits under Instagram's reply bar, so only a quiet sign-off goes there
        sign = caps(site, font("body", "SemiBold", 22), th.muted, 8)
        foot.append(Layer(sign, (w - sign.width) // 2, h - 200, 0.0, "fade"))
        r2 = hairline(60, th.line, 2)
        foot.append(Layer(r2, (w - r2.width) // 2, h - 224, 0.0, "fade"))

    limit = footer_top - S(30 if tall else 26)
    overflow = y > limit
    if not overflow and content:
        # breathe: centre the block a little when there's room (teaser stories, short tips)
        free = limit - y
        shift = int(free * (0.42 if tall else 0.30))
        for L in content:
            L.y += shift
    return background(w, h, th, st["deco"], variant), head + content + foot, t, overflow


def cta_button(text: str, width: int, th: Theme, tall: bool) -> Image.Image:
    arrow_w = 64
    pad = 28
    ti = fit_text(text, "head", "Bold", width - pad - arrow_w - 16, 2, 34 if tall else 29, 20,
                  color=th.cta_fg, gold=th.cta_fg, line_gap=1.08)
    bh = max(ti.height + (40 if tall else 32), 92 if tall else 80)
    rad = 12

    def plate(dr, k):
        dr.rounded_rectangle((0, 0, width * k - 1, bh * k - 1), radius=rad * k, fill=(255, 255, 255, 255))
    pm = shape(width, bh, plate).getchannel("A")
    if th.cta_foil:
        stops = SILVER_FOIL if th.name == "silver" else GOLD_FOIL
        btn = foil_fill(pm, (stops[1], stops[0], stops[2], stops[3]), horizontal=True)
    else:
        btn = Image.new("RGBA", (width, bh), _rgb(th.cta_bg) + (255,))
        btn.putalpha(pm)
    btn.alpha_composite(ti, (pad, (bh - ti.height) // 2 + 2))
    ac = _rgb(th.cta_fg)

    def arrow(dr, k):
        y0 = bh * k / 2
        x1 = (width - pad) * k
        x0 = x1 - 34 * k
        wdt = 3 * k
        dr.line([(x0, y0), (x1, y0)], fill=ac + (255,), width=wdt)
        dr.line([(x1 - 13 * k, y0 - 13 * k), (x1, y0), (x1 - 13 * k, y0 + 13 * k)], fill=ac + (255,),
                width=wdt, joint="curve")
    btn.alpha_composite(shape(width, bh, arrow))
    return btn


# ── template bodies ──────────────────────────────────────────
def _split_point(p) -> tuple[str, str, str]:
    """A step/point as (when, title, detail). Accepts a dict or 'Title: detail'."""
    if isinstance(p, dict):
        return (str(p.get("when") or ""), str(p.get("title") or p.get("text") or ""), str(p.get("detail") or ""))
    s = str(p)
    for sep in (": ", " — ", " - "):
        if sep in s:
            a, b = s.split(sep, 1)
            if len(a) <= 48:
                return ("", a.strip(), b.strip())
    return ("", s, "")


def body_points(c: Ctx, pts, y, t, icon: str = "num"):
    th, S = c.th, c.S
    pts = [str(p) if not isinstance(p, dict) else (p.get("title") or p.get("text") or "") for p in pts]
    pts = pts[: (5 if c.tall else 4)]
    nf = font("head", "Light", S(60 if c.tall else 44))
    pf = font("body", "Medium", S(42 if c.tall else 30))
    lead = S(108 if c.tall else 84)
    gap = S(22 if c.tall else 16)
    for i, p in enumerate(pts):
        if i:
            c.out.append(Layer(hairline(c.inner, th.line_soft, 1), c.m, y, t - 0.2, "wipe"))
            y += gap
        body, _ = text_layer(p, pf, c.inner - lead, color=th.fg, gold=th.accent, foil=th.foil,
                             hl=th.hl, hl_fg=th.hl_fg, line_gap=1.26)
        if icon == "check":
            ic = check_icon(S(52 if c.tall else 40), _rgb(th.cta_fg) + (255,), bg=_rgb(th.accent) + (255,))
        else:
            ic, _ = text_layer(f"*{i + 1:02d}*", nf, lead, color=th.accent, gold=th.accent, foil=th.foil,
                               hl=None)
        ba = pf.getmetrics()[0]
        if icon == "check":
            iy, by = max(0, int(ba * 0.60) - ic.height // 2 + 2), 0
        else:
            na = nf.getmetrics()[0]
            iy, by = (0, na - ba) if na >= ba else (ba - na, 0)
        row = Image.new("RGBA", (c.inner, max(body.height + by, ic.height + iy)), (0, 0, 0, 0))
        row.alpha_composite(ic, (0, iy))
        row.alpha_composite(body, (lead, by))
        c.out.append(Layer(row, c.m, y, t))
        y += row.height + gap
        t += 0.9
    return y, t


def body_tip(c: Ctx, y, t):
    return body_points(c, c.d.get("points") or [], y, t)


def body_cta(c: Ctx, y, t):
    th, S = c.th, c.S
    pts = c.d.get("points") or c.d.get("offer") or []
    if pts:
        lab = caps(c.d.get("offer_label") or "On the call", font("body", "SemiBold", S(20 if c.tall else 18)),
                   th.muted, 5)
        c.out.append(Layer(lab, c.m if not c.center else c.m + (c.inner - lab.width) // 2, y, t, "fade"))
        y += lab.height + S(18)
        y, t = body_points(c, pts, y, t, icon="check")
    if c.d.get("note"):
        ni, _ = text_layer(c.d["note"], font("body", "Regular", S(28 if c.tall else 25)), c.inner,
                           color=th.muted, gold=th.accent, align=c.align)
        c.out.append(Layer(ni, c.m, y, t))
        y += ni.height
    return y, t


def body_process(c: Ctx, y, t):
    th, S = c.th, c.S
    steps = [_split_point(p) for p in (c.d.get("steps") or c.d.get("points") or [])]
    has_detail = any(s[2] for s in steps)
    steps = steps[: ((5 if has_detail else 6) if c.tall else (4 if has_detail else 5))]
    nd = S(64 if c.tall else 50)
    tx = nd + S(30)
    tw = c.inner - tx
    tf = font("head", "Medium", S(42 if c.tall else 35))
    df = font("body", "Regular", S(32 if c.tall else 27))
    wf = font("body", "SemiBold", S(20 if c.tall else 17))
    gap = S(22 if c.tall else 18)
    rows, centers = [], []
    yy = y
    for i, (when, title, detail) in enumerate(steps):
        parts = []
        if when:
            parts.append(caps(when, wf, th.accent, 4))
        ti, _ = text_layer(title, tf, tw, color=th.fg, gold=th.accent, foil=th.foil, hl=th.hl,
                           hl_fg=th.hl_fg, line_gap=1.1)
        parts.append(ti)
        if detail:
            di, _ = text_layer(detail, df, tw, color=th.body, gold=th.accent, foil=th.foil, line_gap=1.3)
            parts.append(di)
        bh = sum(p.height for p in parts) + 4 * (len(parts) - 1)
        rh = max(nd, bh)
        row = Image.new("RGBA", (c.inner, rh), (0, 0, 0, 0))
        py = 0 if bh >= nd else (nd - bh) // 2
        for p in parts:
            row.alpha_composite(p, (tx, py))
            py += p.height + 4

        def node(dr, k, i=i):
            dr.ellipse((k, k, (nd - 1) * k, (nd - 1) * k), fill=_rgb(th.bg) + (255,),
                       outline=_rgb(th.accent) + (255,), width=2 * k)
        nimg = shape(nd, nd, node)
        nn = font("head", "Bold", int(nd * 0.40))
        ImageDraw.Draw(nimg).text((nd / 2, nd / 2 + 1), f"{i + 1}", font=nn, fill=th.accent, anchor="mm")
        row.alpha_composite(nimg, (0, 0 if bh >= nd else 0))
        rows.append((row, yy, t))
        centers.append(yy + nd // 2)
        yy += rh + gap
        t += 1.0
    if len(centers) > 1:
        x = c.m + nd // 2 - 1
        c.out.append(Layer(vline(centers[-1] - centers[0], th.line, 2), x, centers[0], rows[0][2], "fade"))
    for row, ry, rt in rows:
        c.out.append(Layer(row, c.m, ry, rt))
    return yy, t


def body_checklist(c: Ctx, y, t):
    th, S = c.th, c.S
    qs = [str(q) for q in (c.d.get("questions") or c.d.get("points") or [])][: (6 if c.tall else 5)]
    bx = S(50 if c.tall else 40)
    lead = bx + S(26)
    qf = font("body", "Medium", S(42 if c.tall else 31))
    gap = S(20 if c.tall else 14)
    ticks = []

    def box(dr, k):
        dr.rounded_rectangle((k, k, (bx - 1) * k, (bx - 1) * k), radius=7 * k, outline=_rgb(th.accent) + (255,),
                             width=2 * k)
    bimg = shape(bx, bx, box)
    for i, q in enumerate(qs):
        if i:
            c.out.append(Layer(hairline(c.inner, th.line_soft, 1), c.m, y, t - 0.2, "wipe"))
            y += gap
        qi, _ = text_layer(q, qf, c.inner - lead, color=th.fg, gold=th.accent, foil=th.foil, hl=th.hl,
                           hl_fg=th.hl_fg, line_gap=1.26)
        row = Image.new("RGBA", (c.inner, max(qi.height, bx)), (0, 0, 0, 0))
        by = max(0, int(qf.getmetrics()[0] * 0.58) - bx // 2 + 2)
        row.alpha_composite(bimg, (0, by))
        row.alpha_composite(qi, (lead, 0))
        c.out.append(Layer(row, c.m, y, t))
        ticks.append((c.m, y + by))
        y += row.height + gap
        t += 0.8
    if c.video:   # the reel ticks each box once the list is up
        tk = check_icon(bx, _rgb(th.accent) + (255,))
        for i, (tx, ty) in enumerate(ticks):
            c.out.append(Layer(tk, tx, ty, t + 0.35 * i, "pop"))
        t += 0.35 * len(ticks) + 0.4
    if c.d.get("score"):
        y += S(10)
        y, t = _panel(c, c.d["score"], y, t)
    return y, t


def _panel(c: Ctx, text: str, y, t, label: str | None = None):
    """Tinted callout with a gold bar — scores, verdicts, the takeaway."""
    th, S = c.th, c.S
    pad = S(26 if c.tall else 22)
    f = font("body", "SemiBold", S(38 if c.tall else 28))
    ti, _ = text_layer(text, f, c.inner - pad * 2 - 6, color=th.fg, gold=th.accent, foil=th.foil,
                       hl=th.hl, hl_fg=th.hl_fg, line_gap=1.25)
    lab = caps(label, font("body", "SemiBold", S(19 if c.tall else 15)), th.accent, 5) if label else None
    ph = ti.height + pad * 2 + (lab.height + 8 if lab else 0)
    panel = Image.new("RGBA", (c.inner, ph), rgba(th.accent, 38 if th.light else 26))
    ImageDraw.Draw(panel).rectangle((0, 0, 5, ph), fill=rgba(th.accent, 255))
    py = pad
    if lab:
        panel.alpha_composite(lab, (pad + 6, py))
        py += lab.height + 8
    panel.alpha_composite(ti, (pad + 6, py - 2))
    c.out.append(Layer(panel, c.m, y, t, "fade"))
    return y + ph + S(12), t + 0.9


def _answer_index(d: dict, n: int):
    a = d.get("answer")
    if a is None:
        return None
    if isinstance(a, int):
        return a - 1 if 1 <= a <= n else None
    s = str(a).strip()
    if len(s) == 1 and s.upper() in "ABCD"[:n]:
        return "ABCD".index(s.upper())
    for i, o in enumerate((d.get("options") or [])[:n]):
        if str(o).strip().lower() == s.lower():
            return i
    return None


def body_quiz(c: Ctx, y, t):
    th, S = c.th, c.S
    d = c.d
    if d.get("headline") and d.get("question"):
        qi, _ = text_layer(d["question"], font("head", "Medium", S(48 if c.tall else 36)), c.inner,
                           color=th.fg, gold=th.accent, foil=th.foil, hl=th.hl, hl_fg=th.hl_fg, line_gap=1.15)
        c.out.append(Layer(qi, c.m, y, t))
        y += qi.height + S(22)
        t += 0.7
    opts = [str(o) for o in (d.get("options") or [])][:4]
    ans = _answer_index(d, len(opts))
    reveal = ans is not None and (c.video or (c.story and d.get("reveal")))
    of = font("body", "Medium", S(42 if c.tall else 31))
    ld = S(60 if c.tall else 48)
    pad = S(20 if c.tall else 16)
    gap = S(16 if c.tall else 12)
    for i, o in enumerate(opts):
        oi, _ = text_layer(o, of, c.inner - ld - pad * 3, color=th.fg, gold=th.accent, line_gap=1.2)
        rh = max(oi.height, ld) + pad * 2

        def card(dr, k, filled=False):
            box = (k, k, (c.inner - 1) * k, (rh - 1) * k)
            if filled:
                dr.rounded_rectangle(box, radius=14 * k, fill=_rgb(th.cta_bg) + (255,))
            else:
                dr.rounded_rectangle(box, radius=14 * k, outline=th.line, width=2 * k,
                                     fill=rgba(th.accent, 14 if not th.light else 22))

        def letter_disc(fill_c, ink):
            def dr_(dr, k):
                dr.ellipse((k, k, (ld - 1) * k, (ld - 1) * k), outline=_rgb(fill_c) + (255,), width=2 * k,
                           fill=None)
            im = shape(ld, ld, dr_)
            ImageDraw.Draw(im).text((ld / 2, ld / 2 + 1), "ABCD"[i], font=font("head", "Bold", int(ld * 0.44)),
                                    fill=ink, anchor="mm")
            return im
        row = shape(c.inner, rh, card)
        row.alpha_composite(letter_disc(th.accent, th.accent), (pad, (rh - ld) // 2))
        row.alpha_composite(oi, (pad * 2 + ld, (rh - oi.height) // 2 + 2))
        c.out.append(Layer(row, c.m, y, t))
        if reveal and i == ans:
            hit = shape(c.inner, rh, lambda dr, k: card(dr, k, True))
            hit.alpha_composite(letter_disc(th.cta_fg, th.cta_fg), (pad, (rh - ld) // 2))
            oi2, _ = text_layer(o, of, c.inner - ld - pad * 3 - 60, color=th.cta_fg, gold=th.cta_fg, line_gap=1.2)
            hit.alpha_composite(oi2, (pad * 2 + ld, (rh - oi2.height) // 2 + 2))
            hit.alpha_composite(check_icon(S(40), _rgb(th.cta_fg) + (255,)), (c.inner - pad - S(40), (rh - S(40)) // 2))
            hit_layer = (hit, y)
        y += rh + gap
        t += 0.6
    if reveal:
        rt = t + (1.6 if c.video else 0)
        c.out.append(Layer(hit_layer[0], c.m, hit_layer[1], rt, "pop"))
        t = rt + 0.8
        if d.get("explain"):
            y += S(6)
            y, t = _panel(c, d["explain"], y, t, label="The answer")
    return y, t


def body_explainer(c: Ctx, y, t):
    th, S = c.th, c.S
    d = c.d
    pad = S(34 if c.tall else 28)
    iw = c.inner - pad * 2
    parts = []
    if d.get("term"):
        parts.append(fit_text(f"*{d['term']}*", "head", "Bold", iw, 2, S(74 if c.tall else 56), S(36),
                              color=th.fg, gold=th.accent, foil=th.foil, hl=th.hl, hl_fg=th.hl_fg, line_gap=1.05))
    if d.get("pos"):
        parts.append(caps(d["pos"], font("body", "Medium", S(20 if c.tall else 16)), th.muted, 4))
    parts.append(hairline(S(70), rgba(th.accent, 255), 2))
    if d.get("definition"):
        parts.append(text_layer(d["definition"], font("body", "Regular", S(39 if c.tall else 30)), iw,
                                color=th.fg, gold=th.accent, foil=th.foil, hl=th.hl, hl_fg=th.hl_fg,
                                line_gap=1.3)[0])
    gaps = S(14)
    ph = sum(p.height for p in parts) + gaps * (len(parts) - 1) + pad * 2

    def frame(dr, k):
        dr.rectangle((0, 0, c.inner * k - 1, ph * k - 1), fill=rgba(th.accent, 16 if not th.light else 26),
                     outline=th.line, width=2 * k)
    panel = shape(c.inner, ph, frame)
    py = pad
    for p in parts:
        panel.alpha_composite(p, (pad, py))
        py += p.height + gaps
    c.out.append(Layer(panel, c.m, y, t))
    y += ph + S(26 if c.tall else 20)
    t += 1.2
    lf = font("body", "SemiBold", S(20 if c.tall else 16))
    bf = font("body", "Regular", S(36 if c.tall else 28))
    for key, lab in (("why", "Why it matters"), ("example", "Example")):
        if not d.get(key):
            continue
        li = caps(lab, lf, th.accent, 5)
        bi, _ = text_layer(d[key], bf, c.inner, color=th.body, gold=th.accent, foil=th.foil, hl=th.hl,
                           hl_fg=th.hl_fg, line_gap=1.3)
        blk = Image.new("RGBA", (c.inner, li.height + 8 + bi.height), (0, 0, 0, 0))
        blk.alpha_composite(li, (0, 0))
        blk.alpha_composite(bi, (0, li.height + 8))
        c.out.append(Layer(blk, c.m, y, t))
        y += blk.height + S(18 if c.tall else 14)
        t += 0.9
    return y, t


def _side(v, default_label):
    if isinstance(v, dict):
        return str(v.get("label") or default_label), [str(p) for p in (v.get("points") or [])]
    return default_label, [str(p) for p in (v or [])]


def body_compare(c: Ctx, y, t):
    th, S = c.th, c.S
    d = c.d
    gut = S(56)
    cw = (c.inner - gut) // 2
    hf = font("head", "Bold", S(32 if c.tall else 25))
    pf = font("body", "Regular", S(34 if c.tall else 27))
    cols = []
    for side, dl in ((d.get("left"), "Option A"), (d.get("right"), "Option B")):
        label, pts = _side(side, dl)
        parts = [caps(label, hf, th.fg, 3, foil=None), hairline(cw, rgba(th.accent, 255), 2)]
        for p in pts[: (6 if c.tall else 5)]:
            pi, _ = text_layer(p, pf, cw - S(26), color=th.body, gold=th.accent, foil=th.foil, hl=th.hl,
                               hl_fg=th.hl_fg, line_gap=1.26)
            blk = Image.new("RGBA", (cw, pi.height), (0, 0, 0, 0))
            dot = S(8)
            ImageDraw.Draw(blk).rectangle((0, int(pf.getmetrics()[0] * 0.55) - dot // 2,
                                           dot, int(pf.getmetrics()[0] * 0.55) + dot // 2), fill=th.accent)
            blk.alpha_composite(pi, (S(26), 0))
            parts.append(blk)
        cols.append(parts)
    gap = S(18 if c.tall else 14)
    heights = [sum(p.height for p in col) + gap * (len(col) - 1) for col in cols]
    ch = max(heights)
    for ci, col in enumerate(cols):
        x = c.m + ci * (cw + gut)
        yy = y
        for pi_, p in enumerate(col):
            c.out.append(Layer(p, x, yy, t + ci * 0.5 + pi_ * 0.35, "wipe" if pi_ == 1 else "up"))
            yy += p.height + gap
    c.out.append(Layer(vline(ch, th.line_soft, 2), c.m + cw + gut // 2 - 1, y, t, "fade"))
    vs = S(50)

    def disc(dr, k):
        dr.ellipse((k, k, (vs - 1) * k, (vs - 1) * k), fill=_rgb(th.bg) + (255,), outline=_rgb(th.accent) + (255,),
                   width=2 * k)
    vimg = shape(vs, vs, disc)
    ImageDraw.Draw(vimg).text((vs / 2, vs / 2 + 1), "VS", font=font("head", "Bold", int(vs * 0.34)),
                              fill=th.accent, anchor="mm")
    c.out.append(Layer(vimg, c.m + cw + gut // 2 - vs // 2, y - S(6), t + 0.2, "pop"))
    t += 0.5 + 0.35 * max(len(col) for col in cols) + 0.5
    y += ch + S(24)
    if d.get("verdict"):
        y, t = _panel(c, d["verdict"], y, t, label="Bottom line")
    return y, t


def stat_image(text: str, c: Ctx, size: int) -> Image.Image:
    f = font("head", "Bold", size)
    return text_layer(f"*{text}*", f, c.inner, color=c.th.accent, gold=c.th.accent, foil=c.th.foil,
                      hl=None, align=c.align, line_gap=1.0)[0]


def body_stat(c: Ctx, y, t):
    th, S = c.th, c.S
    sv = str(c.d.get("stat_value") or "")
    if sv:
        size = S(240 if c.tall else 200)
        f = font("head", "Bold", size)
        while f.getlength(sv) > c.inner and size > 100:
            size -= 10
            f = font("head", "Bold", size)
        sim = stat_image(sv, c, size)
        maker = None
        if c.video and re.search(r"\d", sv):
            maker = lambda p, sv=sv, size=size: stat_image(_count_text(sv, p), c, size)
        c.out.append(Layer(sim, c.m - (0 if c.center else 6), y - S(18), t, "count" if maker else "up",
                           th.accent, maker))
        y += sim.height - S(18)
        t += 1.4
    if c.d.get("stat_label"):
        li, _ = text_layer(c.d["stat_label"], font("body", "Regular", S(38 if c.tall else 28)), c.inner,
                           color=th.body, gold=th.accent, foil=th.foil, align=c.align, line_gap=1.32)
        c.out.append(Layer(li, c.m, y, t - 0.6))
        y += li.height + S(22)
    return y, t


def body_myth(c: Ctx, y, t):
    th, S = c.th, c.S
    ic = S(52 if c.tall else 40)
    lead = ic + S(22)
    for n, (label, txt) in enumerate((("Myth", c.d.get("myth", "")), ("Fact", c.d.get("fact", "")))):
        if not txt:
            continue
        fact = label == "Fact"
        if n:
            c.out.append(Layer(hairline(c.inner, th.line_soft, 1), c.m, y, t - 0.2, "wipe"))
            y += S(22)
        icon = (check_icon(ic, _rgb(th.cta_fg) + (255,), bg=_rgb(th.accent) + (255,)) if fact
                else cross_icon(ic, _rgb(th.muted) + (255,), ring=_rgb(th.muted) + (255,)))
        lab = caps(label, font("body", "SemiBold", S(21 if c.tall else 17)), th.accent if fact else th.muted, 6)
        f = font("body", "Medium" if fact else "Regular", S(42 if c.tall else 30))
        bi, _ = text_layer(txt, f, c.inner - lead, color=th.fg if fact else th.body, gold=th.accent,
                           foil=th.foil, hl=th.hl, hl_fg=th.hl_fg, line_gap=1.28)
        blk = Image.new("RGBA", (c.inner, ic + S(10) + bi.height), (0, 0, 0, 0))
        blk.alpha_composite(icon, (0, 0))
        blk.alpha_composite(lab, (lead, (ic - lab.height) // 2 + 2))
        blk.alpha_composite(bi, (lead, ic + S(10)))
        c.out.append(Layer(blk, c.m, y, t))
        y += blk.height + S(22)
        t += 1.5
    return y, t


def body_meme(c: Ctx, y, t):
    th, S = c.th, c.S
    if c.d.get("setup"):
        si, _ = text_layer(c.d["setup"], font("body", "Medium", S(50 if c.tall else 37)), c.inner,
                           color=th.body, gold=th.accent, foil=th.foil, align=c.align, line_gap=1.28)
        c.out.append(Layer(si, c.m, y, t))
        y += si.height + S(26)
        t += 0.8
    rule = hairline(S(110), rgba(th.accent, 255), 3)
    c.out.append(Layer(rule, (c.m + (c.inner - rule.width) // 2) if c.center else c.m, y, t, "wipe"))
    y += rule.height + S(30)
    t += 0.4
    if c.d.get("punch"):
        pi = fit_text(c.d["punch"], "head", "Bold", c.inner, 3, S(92 if c.tall else 72), S(44),
                      line_gap=1.06, align=c.align, color=th.fg, gold=th.accent, foil=th.foil,
                      hl=th.hl, hl_fg=th.hl_fg)
        c.out.append(Layer(pi, c.m, y, t))
        y += pi.height + S(20)
        t += 1.2
    return y, t


def body_quote(c: Ctx, y, t):
    th, S = c.th, c.S
    q = c.d.get("quote")
    if not q:
        return y, t
    qm, _ = text_layer("*“*", font("head", "Bold", S(200 if c.tall else 170)), c.inner, color=th.accent,
                       gold=th.accent, foil=th.foil, align=c.align, line_gap=0.9)
    qm = qm.crop((0, 0, qm.width, int(qm.height * 0.55)))
    c.out.append(Layer(qm, c.m, y - S(20), t, "fade"))
    y += qm.height - S(10)
    qi = fit_text(q, "head", "Medium", c.inner, 6, S(92 if c.tall else 70), S(42), line_gap=1.12,
                  align=c.align, color=th.fg, gold=th.accent, foil=th.foil, hl=th.hl, hl_fg=th.hl_fg)
    c.out.append(Layer(qi, c.m, y, t + 0.3))
    y += qi.height + S(28)
    t += 1.4
    rule = hairline(S(90), rgba(th.accent, 255), 3)
    c.out.append(Layer(rule, (c.m + (c.inner - rule.width) // 2) if c.center else c.m, y, t, "wipe"))
    y += rule.height + S(22)
    if c.d.get("attribution"):
        ai = caps(c.d["attribution"], font("body", "SemiBold", S(22 if c.tall else 19)), th.muted, 5)
        c.out.append(Layer(ai, (c.m + (c.inner - ai.width) // 2) if c.center else c.m, y, t + 0.3, "fade"))
        y += ai.height + S(20)
    return y, t + 0.5


def body_spotlight(c: Ctx, y, t):
    """Agent attraction: one thing per post — a perk, a tool, a support line, an
    event, or (with their written OK) an agent. Optional photo for people."""
    th, S = c.th, c.S
    d = c.d
    photo = d.get("photo")
    pth = (ROOT / photo) if photo else None
    if pth and pth.exists():
        ps = S(200 if c.tall else 168)

        def ring(dr, k):
            dr.ellipse((k, k, (ps - 1) * k, (ps - 1) * k), outline=_rgb(th.accent) + (255,), width=3 * k)
        im = Image.open(pth).convert("RGBA")
        im = ImageOps.fit(im, (ps - 12, ps - 12), centering=(0.5, 0.3))
        m = shape(ps - 12, ps - 12, lambda dr, k: dr.ellipse((0, 0, (ps - 12) * k - 1, (ps - 12) * k - 1),
                                                              fill=(255, 255, 255, 255))).getchannel("A")
        im.putalpha(ImageChops.multiply(im.getchannel("A"), m))
        port = shape(ps, ps, ring)
        port.alpha_composite(im, (6, 6))
        tx = ps + S(28)
        nm = caps(d.get("name") or "", font("head", "Bold", S(32 if c.tall else 27)), th.fg, 3)
        rl, _ = text_layer(d.get("role") or "", font("body", "Regular", S(28 if c.tall else 24)), c.inner - tx,
                           color=th.body, gold=th.accent, foil=th.foil, line_gap=1.3)
        row = Image.new("RGBA", (c.inner, ps), (0, 0, 0, 0))
        row.alpha_composite(port, (0, 0))
        ty = (ps - nm.height - 8 - rl.height) // 2
        row.alpha_composite(nm, (tx, ty))
        row.alpha_composite(rl, (tx, ty + nm.height + 8))
        c.out.append(Layer(row, c.m, y, t, "pop"))
        y += ps + S(26)
        t += 1.0
    pts = d.get("points") or []
    if pts:
        lab = caps(d.get("points_label") or "What it means for you", font("body", "SemiBold", S(20 if c.tall else 17)),
                   th.muted, 5)
        c.out.append(Layer(lab, c.m, y, t, "fade"))
        y += lab.height + S(16)
        y, t = body_points(c, pts, y, t, icon="check")
    fine = d.get("fine_print")
    if fine is None and d.get("_track") == "agent_attraction":
        fine = "Subject to Epique's current plan terms and eligibility. No income is guaranteed."
    if fine:
        fi, _ = text_layer(fine, font("body", "Regular", S(23 if c.tall else 19)), c.inner, color=th.muted,
                           gold=th.accent, line_gap=1.3)
        c.out.append(Layer(fi, c.m, y + S(4), t, "fade"))
        y += fi.height + S(8)
    return y, t


BODIES = {
    "tip": body_tip, "process": body_process, "checklist": body_checklist, "quiz": body_quiz,
    "explainer": body_explainer, "compare": body_compare, "cta": body_cta, "spotlight": body_spotlight,
    "stat": body_stat,
    "myth": body_myth, "meme": body_meme, "quote": body_quote,
}


def compose(bg: Image.Image, layers: list[Layer]) -> Image.Image:
    out = bg.copy()
    for L in layers:
        out.paste(L.img, (int(L.x), int(L.y)), L.img) if (L.x < 0 or L.y < 0) else \
            out.alpha_composite(L.img, (int(L.x), int(L.y)))
    return out


# ── video ────────────────────────────────────────────────────
def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def _faded(img: Image.Image, a: float, cache: dict, key) -> Image.Image:
    q = round(a * 12) / 12
    ck = (key, q)
    if ck not in cache:
        if q >= 1:
            cache[ck] = img
        else:
            alpha = img.getchannel("A").point(lambda v: int(v * q))
            im = img.copy()
            im.putalpha(alpha)
            cache[ck] = im
    return cache[ck]


def _count_text(stat: str, p: float) -> str:
    m = re.search(r"[\d,]*\.?\d+", stat)
    if not m:
        return stat
    num_s = m.group(0)
    target = float(num_s.replace(",", ""))
    decimals = len(num_s.split(".")[1]) if "." in num_s else 0
    val = target * p
    s = f"{val:,.{decimals}f}" if "," in num_s else f"{val:.{decimals}f}"
    return stat[: m.start()] + s + stat[m.end():]


def render_video(bg, layers, content_end: float, out: Path, w: int, h: int, item: Item):
    fps = 30
    hold = 3.0
    total = max(8.0, content_end + hold)
    n = int(total * fps)
    cache: dict = {}
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    count_cache: dict = {}
    for fi in range(n):
        tsec = fi / fps
        frame = bg.copy()
        for li, L in enumerate(layers):
            p = ease((tsec - L.t) / 0.6)
            if p <= 0:
                continue
            img, x, y = L.img, L.x, L.y
            if L.anim == "up":
                y = L.y + int((1 - p) * 50)
            elif L.anim == "pop":
                s = 0.86 + 0.14 * p
                if s < 0.999:
                    img = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.BILINEAR)
                    x = L.x + (L.img.width - img.width) // 2
                    y = L.y + (L.img.height - img.height) // 2
            elif L.anim == "wipe":
                if p < 1:
                    img = img.crop((0, 0, max(1, int(img.width * p)), img.height))
            elif L.anim == "count" and L.maker and p < 1:
                pc = ease((tsec - L.t) / 1.4)
                q = round(pc * 40) / 40
                if (li, q) not in count_cache:
                    count_cache[(li, q)] = L.maker(q)
                img = count_cache[(li, q)]
                if pc < 1:
                    p = 1  # the number counts up at full opacity
            fade = L.anim not in ("wipe",) and not (L.anim == "count" and L.maker)
            src = _faded(img, p, cache, (li, img.size)) if fade else img
            if x < 0 or y < 0:
                frame.paste(src, (int(x), int(y)), src)
            else:
                frame.alpha_composite(src, (int(x), int(y)))
        proc.stdin.write(frame.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed")


# ── per-item rendering ──────────────────────────────────────
def _stamp(item: Item, plat: str):
    """Record the look this platform got, so analytics can attribute results to
    the design and the no-repeat rule can see it. Written even when the media
    already exists, or the first day of a design would never be measured."""
    d = item.d.get("design") or {}
    template = template_of(d)
    st = (item.d.get("rendered") or {}).get(plat)
    if isinstance(st, dict) and st.get("theme"):
        st["template"] = template if st.get("side") else st.get("template", template)
        return
    pick_style(item, plat, template)


def render_item(item: Item, force: bool = False) -> list[str]:
    made = []
    changed = False
    mdir = item.path.parent / "media"
    for i, plat in enumerate(item.platforms()):
        existing = item.media_path(plat)
        if existing and existing.exists() and not force:
            if plat not in (item.d.get("rendered") or {}):
                _stamp(item, plat)
                changed = True
            continue
        variant = (stable_int(item.day, item.id) + i) % 4
        if item.kind == "story":
            w, h, video = 1080, 1920, False
        elif item.kind == "reel" or plat == "tiktok":
            w, h, video = 1080, 1920, True
        else:
            w, h, video = 1080, 1350, False
        bg, layers, end = layout(item, plat, w, h, variant, video)
        if video:
            out = mdir / f"{item.id}-{plat}.mp4"
            render_video(bg, layers, end, out, w, h, item)
        else:
            out = mdir / f"{item.id}-{plat}.jpg"
            out.parent.mkdir(parents=True, exist_ok=True)
            compose(bg, layers).convert("RGB").save(out, "JPEG", quality=92, optimize=True)
        item.d["media"][plat] = str(out.relative_to(ROOT))
        _stamp(item, plat)
        made.append(str(out.relative_to(ROOT)))
    if made or changed:
        item.save()
    return made


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--file")
    a = ap.parse_args()
    if a.file:
        items = [Item(ROOT / a.file)]
    else:
        items = load_items(None if a.all else recent_days(0, 3))
    for it in items:
        if it.d.get("status") and all(it.state(p) in ("posted", "draft_sent") for p in it.platforms()):
            continue
        for m in render_item(it, a.force):
            print("rendered", m)


if __name__ == "__main__":
    main()
