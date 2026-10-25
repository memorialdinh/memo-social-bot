"""Renders branded posts (JPG), stories (JPG) and reels (MP4) from queue items.

Usage:
  python -m bot.render                 # render anything missing in the next few days
  python -m bot.render --all --force   # re-render everything
  python -m bot.render --file queue/2026-10-24/p1.yaml
"""
from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

from .common import ASSETS, CFG, ROOT, Item, load_items, recent_days, stable_int

C = CFG["brand"]["colors"]
OBSIDIAN = C["obsidian"]
GOLD = C["gold"]
CARBON = C["carbon"]
SLATE = C["slate"]
WHITE = "#F6F4F0"

FONT_DIR = ASSETS / "fonts"
_font_cache: dict = {}


def font(family: str, weight: str, size: int) -> ImageFont.FreeTypeFont:
    key = (family, weight, size)
    if key not in _font_cache:
        path = FONT_DIR / ("SpaceGrotesk.ttf" if family == "head" else "Inter.ttf")
        f = ImageFont.truetype(str(path), size)
        try:
            f.set_variation_by_name(weight)
        except Exception:
            pass
        _font_cache[key] = f
    return _font_cache[key]


# ── text helpers ─────────────────────────────────────────────
_EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u200D]")


def tokens(text: str):
    text = _EMOJI.sub("", text)
    """Split '*gold words*' markup into words; each word is a list of (text, is_gold) runs."""
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


def text_layer(text, f, max_w, color=WHITE, gold=GOLD, line_gap=1.12, align="left", hl=None, hl_fg=None):
    lines = wrap(text, f, max_w)
    asc, desc = f.getmetrics()
    lh = int((asc + desc) * line_gap)
    w = max_w
    h = lh * len(lines) + 4
    img = Image.new("RGBA", (w, max(h, 1)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    space = f.getlength(" ")
    for i, line in enumerate(lines):
        lw = sum(_wlen(f, wd) for wd in line) + space * (len(line) - 1)
        x = (w - lw) / 2 if align == "center" else 0
        for wi, wd in enumerate(line):
            for t, g in wd:
                tw = f.getlength(t)
                if g and hl:
                    nxt_gold = wi + 1 < len(line) and line[wi + 1][0][1] and t is wd[-1][0]
                    pad = asc * 0.12
                    d.rectangle((x - pad, i * lh + asc * 0.12, x + tw + (space if nxt_gold else pad), i * lh + asc + desc * 0.55), fill=hl)
                d.text((x, i * lh), t, font=f, fill=(hl_fg or gold) if g and hl else gold if g else color)
                x += tw
            x += space
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


def pill(text, f, fg=GOLD, outline=GOLD, fill=None, pad=(26, 12), letter=3):
    spaced = text.upper()
    tw = sum(f.getlength(ch) for ch in spaced) + letter * (len(spaced) - 1)
    asc, desc = f.getmetrics()
    w, h = int(tw + pad[0] * 2), asc + desc + pad[1] * 2
    img = Image.new("RGBA", (w + 4, h + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((2, 2, w + 1, h + 1), radius=h // 2, outline=outline, width=3, fill=fill)
    x = pad[0] + 2
    for ch in spaced:
        d.text((x, pad[1] + 2), ch, font=f, fill=fg)
        x += f.getlength(ch) + letter
    return img


# ── themes: a different look every post, always on-brand ─────
@dataclass
class Theme:
    name: str
    bg: str          # base color
    glow: tuple      # rgb of accent glow
    fg: str          # headline
    body: str        # body text
    accent: str      # gold words, numbers, pills
    cta_bg: str
    cta_fg: str
    muted: str       # microtext
    ring: str        # headshot ring
    hl: str | None = None   # highlight box behind accent words (for light/gold themes)
    hl_fg: str | None = None
    plate: str = "#2b2b29"  # unused since Oct 2026 — the badge backs onto th.bg


THEMES = [
    Theme("noir",     "#101010", (188, 164, 128), WHITE,     CARBON,    GOLD,      GOLD,      OBSIDIAN, SLATE,     GOLD,
          plate="#2b2b29"),
    Theme("silver",   "#0e0f11", (201, 204, 209), WHITE,     "#c9ccd1", "#c9ccd1", "#c9ccd1", OBSIDIAN, "#6b6e73", "#c9ccd1",
          plate="#26282b"),
    Theme("ivory",    "#efece7", (188, 164, 128), OBSIDIAN,  "#33332f", "#7d6a48", OBSIDIAN,  GOLD,     "#6f6e69", GOLD,
          plate="#dcd7cf"),
    Theme("goldrush", "#bca480", (255, 245, 225), OBSIDIAN,  "#221f1a", OBSIDIAN,  OBSIDIAN,  GOLD,     "#3d362b", OBSIDIAN,
          hl=OBSIDIAN, hl_fg=GOLD, plate="#a68e6c"),
    Theme("graphite", "#1c1c1b", (188, 164, 128), WHITE,     CARBON,    GOLD,      WHITE,     OBSIDIAN, "#77766f", GOLD,
          plate="#333331"),
]
DECOS = ["glow", "stripe", "frame", "grid", "watermark", "arcs"]


def pick_style(item: Item, platform: str) -> dict:
    """Rotates themes/decor/layout so neighbouring posts (and each platform's
    version of the same post) never look the same."""
    forced = (item.d.get("design") or {}).get("theme")
    try:
        idx = sorted(p.stem for p in item.path.parent.glob("*.yaml")).index(item.id)
    except ValueError:
        idx = 0
    pi = ["instagram", "facebook", "linkedin", "tiktok"].index(platform) if platform in PLATFORMS_ORDER else 0
    day = item.day.toordinal()
    ti = (day * 3 + idx + pi * 2) % len(THEMES)
    th = next((t for t in THEMES if t.name == forced), THEMES[ti])
    return {
        "theme": th,
        "deco": DECOS[(day * 5 + idx * 2 + pi) % len(DECOS)],
        "side_right": (day + idx + pi) % 2 == 0,
        "shape": "circle" if (day + idx * 3 + pi) % 3 else "square",
        "center": (idx + pi + day) % 4 == 0,
    }


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


def headshot_badge(path: Path | None, size: int, ring_color: str, shape: str = "circle",
                   backing: str = "#2a2a28") -> Image.Image:
    """Headshot in a gold-ringed badge. Cut-out PNGs get a soft backing so the
    subject reads on any theme; photos with their own background are used as-is."""
    ring = 7
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    inner = size - ring * 2
    plate = Image.new("RGBA", (inner, inner), backing)
    if path:
        im = Image.open(path).convert("RGBA")
        cut = im.getchannel("A").getextrema()[0] < 250          # has transparency
        if cut:
            # Cut-out: sit him on the card's own colour so there is no visible
            # plate, and leave headroom so the top of his head never touches the
            # ring. Anchored to the bottom so the shoulders meet the badge edge.
            fitted = ImageOps.fit(im, (int(inner * 0.92), int(inner * 0.92)),
                                  centering=(0.5, 0.30))
            plate.alpha_composite(fitted, ((inner - fitted.width) // 2,
                                           inner - fitted.height))
            im = plate
        else:
            im = ImageOps.fit(im, (inner, inner), centering=(0.5, 0.3))
    else:  # placeholder until a headshot is added
        im = Image.new("RGBA", (inner, inner), SLATE)
        d = ImageDraw.Draw(im)
        f = font("head", "Bold", inner // 3)
        d.text((inner / 2, inner / 2), "MD", font=f, fill=CARBON, anchor="mm")
    mask = Image.new("L", (inner, inner), 0)
    md = ImageDraw.Draw(mask)
    d = ImageDraw.Draw(out)
    if shape == "square":
        md.rounded_rectangle((0, 0, inner - 1, inner - 1), radius=inner // 6, fill=255)
        d.rounded_rectangle((0, 0, size - 1, size - 1), radius=size // 6, fill=ring_color)
    else:
        md.ellipse((0, 0, inner - 1, inner - 1), fill=255)
        d.ellipse((0, 0, size - 1, size - 1), fill=ring_color)
    out.paste(im, (ring, ring), mask)
    return out


def logo_layer(height: int, th: Theme) -> Image.Image:
    """Epique POWER mark + wordmark lockup. The mark is only ever scaled, never reshaped."""
    light_bg = th.name in ("ivory", "goldrush")
    names = ("logo-black.png", "logo.png") if light_bg else ("logo-white.png", "logo-gold.png", "logo.png")
    ink = OBSIDIAN if light_bg else CARBON
    mark = None
    for name in names:
        p = ASSETS / "logos" / name
        if p.exists():
            im = Image.open(p).convert("RGBA")
            mh = int(height * 1.18)                       # the square mark reads small next to caps
            mark = im.resize((max(1, int(im.width * mh / im.height)), mh), Image.LANCZOS)
            break
    f = font("head", "Medium", int(height * 0.55))
    word = pill("EPIQUE REALTY", f, fg=ink, outline=(0, 0, 0, 0), pad=(0, 6), letter=6)
    if mark is None:
        return word
    gap = int(height * 0.42)
    w = mark.width + gap + word.width
    h = max(mark.height, word.height)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.alpha_composite(mark, (0, (h - mark.height) // 2))
    out.alpha_composite(word, (mark.width + gap, (h - word.height) // 2))
    return out


def _rgb(hexs: str) -> tuple:
    hexs = hexs.lstrip("#")
    return tuple(int(hexs[i:i + 2], 16) for i in (0, 2, 4))


def background(w: int, h: int, th: Theme, deco: str, variant: int) -> Image.Image:
    base = _rgb(th.bg)
    glow = th.glow
    # smooth radial glow computed small then upscaled (no banding)
    sw, sh = 54, int(54 * h / w)
    cx = sw * (0.9 if variant % 2 == 0 else 0.1)
    cy = -sh * 0.05 if deco != "arcs" else sh * 1.05
    r = sw * (1.05 if deco == "glow" else 0.8)
    strength = 0.17 if deco == "glow" else 0.09
    if th.name in ("ivory", "goldrush"):
        strength *= 0.7
    small = Image.new("RGBA", (sw, sh))
    px = []
    for yy in range(sh):
        for xx in range(sw):
            dist = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5 / r
            k = max(0.0, 1 - dist) ** 2 * strength
            px.append(tuple(int(base[c] + (glow[c] - base[c]) * k) for c in range(3)) + (255,))
    small.putdata(px)
    bg = small.resize((w, h), Image.BICUBIC)
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    acc = _rgb(th.accent if th.name != "goldrush" else OBSIDIAN)
    if deco == "stripe":
        off = 0 if variant % 2 == 0 else 1
        for i, a in ((0, 70), (60, 35)):
            x0 = w - 380 - i if not off else -200 + i
            d.polygon([(x0, -10), (x0 + 170, -10), (x0 + 170 - 520, 520), (x0 - 520, 520)] if not off else
                      [(x0, -10), (x0 + 170, -10), (x0 + 170 + 520, 520), (x0 + 520, 520)], fill=acc + (a,))
    elif deco == "frame":
        d.rectangle((34, 34, w - 35, h - 35), outline=acc + (150,), width=3)
        L = 70
        for (x, y, sx, sy) in ((34, 34, 1, 1), (w - 35, 34, -1, 1), (34, h - 35, 1, -1), (w - 35, h - 35, -1, -1)):
            d.line((x, y, x + L * sx, y), fill=acc + (255,), width=7)
            d.line((x, y, x, y + L * sy), fill=acc + (255,), width=7)
    elif deco == "grid":
        for x in range(0, w, 90):
            d.line((x, 0, x, h), fill=acc + (16,), width=1)
        for y in range(0, h, 90):
            d.line((0, y, w, y), fill=acc + (16,), width=1)
    elif deco == "watermark":
        f = font("head", "Bold", int(h * 0.62))
        d.text((w * (0.62 if variant % 2 == 0 else -0.08), h * 0.28), "E", font=f, fill=acc + (20,))
    elif deco == "arcs":
        cxp = w if variant % 2 == 0 else 0
        for i, rr in enumerate(range(260, 900, 120)):
            d.ellipse((cxp - rr, h * 0.45 - rr, cxp + rr, h * 0.45 + rr), outline=acc + (40 - i * 5,), width=2)
    bg = Image.alpha_composite(bg, ov)
    if deco != "frame":
        ImageDraw.Draw(bg).rectangle((0, 0, w, 8), fill=th.accent if th.name != "goldrush" else OBSIDIAN)
    return bg


# ── layout ───────────────────────────────────────────────────
@dataclass
class Layer:
    img: Image.Image
    x: int
    y: int
    t: float = 0.0      # reveal time (seconds) in reels
    anim: str = "up"    # up | fade | pop | count
    color: str = GOLD   # used by the count-up animation


def layout(item: Item, platform: str, w: int, h: int, variant: int, video: bool = False):
    sc = 1.0
    while True:
        bg, layers, t, overflow = _layout(item, platform, w, h, variant, video, sc)
        if not overflow or sc < 0.62:
            return bg, layers, t
        sc -= 0.06


def _layout(item: Item, platform: str, w: int, h: int, variant: int, video: bool, sc: float):
    S = lambda v: max(1, int(v * sc))
    d = item.d.get("design") or {}
    st = pick_style(item, platform)
    th: Theme = st["theme"]
    tall = h > w * 1.4
    m = 80
    inner = w - m * 2
    layers: list[Layer] = []
    t = 0.3
    center = st["center"]
    align = "center" if center else "left"
    tl = dict(color=th.fg, gold=th.accent, hl=th.hl, hl_fg=th.hl_fg)

    logo = logo_layer(54, th)
    layers.append(Layer(logo, (w - logo.width) // 2 if center else m, 58, 0.0, "fade"))

    track_label = CFG["tracks"].get(item.track, {}).get("label", item.track.upper())
    k = pill(d.get("kicker") or track_label, font("body", "SemiBold", 28), fg=th.accent, outline=th.accent)
    y = 58 + logo.height + S(74 if tall else 46)
    layers.append(Layer(k, (w - k.width) // 2 if center else m, y, t))
    y += k.height + S(36)
    t += 0.5

    template = d.get("template") or ("stat" if d.get("stat_value") else "myth" if d.get("myth") else
                                     "meme" if d.get("punch") else "quote" if d.get("quote") else "tip")

    # On a quote card the line IS the headline, so don't print both.
    if not (template == "quote" and d.get("quote")):
        headline = d.get("headline") or item.d.get("topic", "")
        head_img = fit_text(headline, "head", "Bold", inner, 4 if tall else 3, S(104 if tall else 92), S(56),
                            line_gap=1.08, align=align, **tl)
        layers.append(Layer(head_img, m, y, t))
        y += head_img.height + S(50 if tall else 34)
        t += 0.9

    if template == "stat" and d.get("stat_value"):
        sv = d["stat_value"]
        fsize = S(230 if tall else 190)
        f = font("head", "Bold", fsize)
        while f.getlength(str(sv)) > inner and fsize > 100:
            fsize -= 10
            f = font("head", "Bold", fsize)
        asc, desc = f.getmetrics()
        sim = Image.new("RGBA", (inner, asc + desc), (0, 0, 0, 0))
        sx = (inner - f.getlength(str(sv))) / 2 if center else 0
        ImageDraw.Draw(sim).text((sx, 0), str(sv), font=f, fill=th.accent)
        layers.append(Layer(sim, m - (0 if center else 6), y, t, "count" if video and not center else "up", th.accent))
        y += sim.height + 4
        t += 1.4
        if d.get("stat_label"):
            lim, _ = text_layer(d["stat_label"], font("body", "Medium", S(40 if tall else 34)), inner,
                                color=th.body, gold=th.accent, align=align)
            layers.append(Layer(lim, m, y, t - 0.6))
            y += lim.height + S(30)

    if template == "quote" and d.get("quote"):
        # Motivational / empowering card: the line carries it, so set it large,
        # with a gold rule and a small attribution underneath.
        qim = fit_text(d["quote"], "head", "Bold", inner, 6, S(96 if tall else 82), S(44),
                       line_gap=1.12, align=align, color=th.fg, gold=th.accent,
                       hl=th.hl, hl_fg=th.hl_fg)
        layers.append(Layer(qim, m, y, t, "up", th.accent))
        y += qim.height + S(36)
        t += 1.2
        rule = Image.new("RGBA", (S(90), 4), _rgb(th.accent))
        layers.append(Layer(rule, (w - rule.width) // 2 if center else m, y, t, "wipe"))
        y += rule.height + S(26)
        if d.get("attribution"):
            aim, _ = text_layer(d["attribution"], font("body", "Medium", S(36 if tall else 30)), inner,
                                color=th.muted, gold=th.accent, align=align)
            layers.append(Layer(aim, m, y, t + 0.3))
            y += aim.height + S(30)
        t += 0.5

    if template == "meme" and (d.get("setup") or d.get("punch")):
        # Setup in plain body type, then a gold rule, then the punchline big.
        # The joke carries the graphic, so no numbered points underneath.
        if d.get("setup"):
            sim, _ = text_layer(d["setup"], font("body", "Medium", S(46 if tall else 40)), inner,
                                color=th.body, gold=th.accent, align=align)
            layers.append(Layer(sim, m, y, t))
            y += sim.height + S(34)
            t += 0.8
        rule = Image.new("RGBA", (S(120), 5), _rgb(th.accent))
        layers.append(Layer(rule, (w - rule.width) // 2 if center else m, y, t, "wipe"))
        y += rule.height + S(34)
        t += 0.4
        if d.get("punch"):
            pim = fit_text(d["punch"], "head", "Bold", inner, 3, S(86 if tall else 74), S(46),
                           line_gap=1.08, align=align, color=th.accent, gold=th.fg,
                           hl=th.hl, hl_fg=th.hl_fg)
            layers.append(Layer(pim, m, y, t, "up", th.accent))
            y += pim.height + S(40)
            t += 1.2

    if template == "myth" and d.get("myth"):
        for label, txt in (("MYTH", d["myth"]), ("FACT", d.get("fact", ""))):
            fact = label == "FACT"
            tag = pill(label, font("body", "Bold", 26), fg=(th.cta_fg if fact else th.body),
                       outline=(th.cta_bg if fact else th.muted), fill=th.cta_bg if fact else None)
            body, _ = text_layer(txt, font("body", "Medium", S(44 if tall else 38)), inner,
                                 color=th.fg if fact else th.body, gold=th.accent)
            block = Image.new("RGBA", (inner, tag.height + 18 + body.height), (0, 0, 0, 0))
            block.alpha_composite(tag, (0, 0))
            block.alpha_composite(body, (0, tag.height + 18))
            layers.append(Layer(block, m, y, t))
            y += block.height + S(40)
            t += 1.6

    points = d.get("points") or []
    pf = font("body", "Medium", S(40 if tall else 34))
    nf = font("head", "Bold", S(40 if tall else 34))
    for i, p in enumerate(points[: (5 if tall else 4)]):
        body, _ = text_layer(p, pf, inner - 90, color=th.body, gold=th.accent)
        row = Image.new("RGBA", (inner, max(body.height, 50)), (0, 0, 0, 0))
        ImageDraw.Draw(row).text((0, 0), f"{i + 1:02d}", font=nf, fill=th.accent)
        row.alpha_composite(body, (90, 0))
        layers.append(Layer(row, m, y, t))
        y += row.height + S(28 if tall else 20)
        t += 1.1

    # footer: headshot + name + CTA + microtext
    hs = 250 if tall else 200
    footer_top = h - (420 if tall else 330)
    side_right = st["side_right"]
    head = headshot_badge(pick_headshot(item, platform), hs, th.ring, st["shape"], th.bg)
    hx = w - m - hs if side_right else m
    layers.append(Layer(head, hx, footer_top, 0.2, "pop"))

    name_x = m if side_right else m + hs + 36
    name_w = w - m * 2 - hs - 36
    nm = font("head", "Bold", 46 if tall else 40)
    sub = font("body", "Regular", 28 if tall else 25)
    nb = Image.new("RGBA", (name_w, 150), (0, 0, 0, 0))
    nd = ImageDraw.Draw(nb)
    nd.text((0, 0), CFG["brand"]["name"].upper(), font=nm, fill=th.fg)
    nd.text((0, 62), f'{CFG["brand"]["title"]} · {CFG["brand"]["brokerage"]}', font=sub, fill=th.body)
    site = CFG["brand"]["agent_site"] if item.track == "agent_attraction" else CFG["brand"]["website"]
    nd.text((0, 100), f'{CFG["brand"]["phone"]}  ·  {site}', font=sub, fill=th.accent)
    layers.append(Layer(nb, name_x, footer_top + (hs - 140) // 2, 0.5, "fade"))

    overflow = y + S(30) > footer_top
    cta = d.get("cta")
    if cta:
        cf = font("head", "Bold", 38 if tall else 32)
        cim, _ = text_layer(cta, cf, inner - 60, color=th.cta_fg, gold=th.cta_fg, align="center")
        bar = Image.new("RGBA", (inner, cim.height + 44), (0, 0, 0, 0))
        ImageDraw.Draw(bar).rounded_rectangle((0, 0, inner - 1, bar.height - 1), radius=18, fill=th.cta_bg)
        bar.alpha_composite(cim, (30, 22))
        cy = footer_top - bar.height - (50 if tall else 30)
        overflow = y + S(24) > cy
        layers.append(Layer(bar, m, cy, t + 0.2, "pop"))
        t += 1.0

    mf = font("body", "Regular", 22)
    micro = f'DRE #{CFG["brand"]["dre"]} · {CFG["brand"]["brokerage"]} · Equal Housing Opportunity'
    mim, _ = text_layer(micro, mf, inner, color=th.muted, align="center")
    layers.append(Layer(mim, m, h - 70, 0.0, "fade"))

    return background(w, h, th, st["deco"], variant), layers, t, overflow


def compose(bg: Image.Image, layers: list[Layer]) -> Image.Image:
    out = bg.copy()
    for L in layers:
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


def render_video(bg, layers, content_end: float, out: Path, w: int, h: int, item: Item):
    fps = 30
    hold = 3.0
    total = max(8.0, content_end + hold)
    n = int(total * fps)
    cache: dict = {}
    d = item.d.get("design") or {}
    stat = str(d.get("stat_value", ""))
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(n):
        tsec = fi / fps
        frame = bg.copy()
        for li, L in enumerate(layers):
            p = ease((tsec - L.t) / 0.6)
            if p <= 0:
                continue
            img, x, y = L.img, L.x, L.y
            if L.anim == "up":
                y = L.y + int((1 - p) * 60)
            elif L.anim == "pop":
                s = 0.85 + 0.15 * p
                if s < 0.999:
                    img = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.BILINEAR)
                    x = L.x + (L.img.width - img.width) // 2
                    y = L.y + (L.img.height - img.height) // 2
            elif L.anim == "count" and p < 1 and re.search(r"\d", stat):
                img = count_frame(L, stat, p)
            frame.alpha_composite(_faded(img, p, cache, (li, img.size)) if L.anim != "count" or p >= 1 else img, (int(x), int(y)))
        proc.stdin.write(frame.convert("RGB").tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed")


def count_frame(L: Layer, stat: str, p: float) -> Image.Image:
    m = re.search(r"[\d,]*\.?\d+", stat)
    if not m:
        return L.img
    num_s = m.group(0)
    target = float(num_s.replace(",", ""))
    decimals = len(num_s.split(".")[1]) if "." in num_s else 0
    val = target * p
    s = f"{val:,.{decimals}f}" if "," in num_s else f"{val:.{decimals}f}"
    txt = stat[: m.start()] + s + stat[m.end():]
    img = Image.new("RGBA", L.img.size, (0, 0, 0, 0))
    size = L.img.height
    f = font("head", "Bold", 230)
    # match the size used in layout by shrinking until height matches
    for fs in range(230, 90, -10):
        f = font("head", "Bold", fs)
        a, dsc = f.getmetrics()
        if a + dsc <= size:
            break
    ImageDraw.Draw(img).text((0, 0), txt, font=f, fill=L.color)
    a = img.getchannel("A").point(lambda v: int(v * min(1, p * 3)))
    img.putalpha(a)
    return img


# ── per-item rendering ──────────────────────────────────────
def _stamp(item: Item, plat: str):
    """Record the look this platform got, so analytics can attribute results to
    the design. Written even when the media already exists, or the first day of
    a design would never be measured."""
    d = item.d.get("design") or {}
    st = pick_style(item, plat)
    item.d.setdefault("rendered", {})[plat] = {
        "theme": st["theme"].name,
        "deco": st["deco"],
        "template": d.get("template") or ("stat" if d.get("stat_value") else
                                          "myth" if d.get("myth") else
                                          "meme" if d.get("punch") else
                                          "quote" if d.get("quote") else "tip"),
    }


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
