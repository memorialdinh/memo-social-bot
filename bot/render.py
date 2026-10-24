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


def text_layer(text, f, max_w, color=WHITE, gold=GOLD, line_gap=1.12, align="left"):
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
        for wd in line:
            for t, g in wd:
                d.text((x, i * lh), t, font=f, fill=gold if g else color)
                x += f.getlength(t)
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


# ── assets ───────────────────────────────────────────────────
def headshot_files(platform: str) -> list[Path]:
    listed = CFG.get("headshots", {}).get(platform) or []
    files = [ASSETS / "headshots" / x for x in listed if (ASSETS / "headshots" / x).exists()]
    if not files:
        files = sorted(p for p in (ASSETS / "headshots").glob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"))
    return files


def pick_headshot(item: Item, platform: str) -> Path | None:
    files = headshot_files(platform)
    if not files:
        return None
    forced = (item.d.get("design") or {}).get("headshot")
    if forced and (ASSETS / "headshots" / forced).exists():
        return ASSETS / "headshots" / forced
    pi = ["instagram", "facebook", "linkedin", "tiktok"].index(platform) if platform in ("instagram", "facebook", "linkedin", "tiktok") else 0
    return files[(stable_int(item.day, item.id) + pi) % len(files)]


def headshot_circle(path: Path | None, size: int) -> Image.Image:
    ring = 7
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    inner = size - ring * 2
    if path:
        im = Image.open(path).convert("RGBA")
        im = ImageOps.fit(im, (inner, inner), centering=(0.5, 0.3))
    else:  # placeholder until real headshots are added
        im = Image.new("RGBA", (inner, inner), SLATE)
        d = ImageDraw.Draw(im)
        f = font("head", "Bold", inner // 3)
        d.text((inner / 2, inner / 2), "MD", font=f, fill=CARBON, anchor="mm")
    mask = Image.new("L", (inner, inner), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, inner - 1, inner - 1), fill=255)
    d = ImageDraw.Draw(out)
    d.ellipse((0, 0, size - 1, size - 1), fill=GOLD)
    out.paste(im, (ring, ring), mask)
    return out


def logo_layer(height: int) -> Image.Image:
    for name in ("logo-white.png", "logo-gold.png", "logo.png"):
        p = ASSETS / "logos" / name
        if p.exists():
            im = Image.open(p).convert("RGBA")
            w = int(im.width * height / im.height)
            return im.resize((w, height), Image.LANCZOS)  # scale only; shape untouched
    f = font("head", "Medium", int(height * 0.55))
    return pill("EPIQUE REALTY", f, fg=CARBON, outline=(0, 0, 0, 0), pad=(0, 6), letter=6)


def background(w: int, h: int, variant: int) -> Image.Image:
    # smooth radial gold glow: computed small, then upscaled (no banding)
    sw, sh = 54, int(54 * h / w)
    cx = sw * (0.9 if variant % 2 == 0 else 0.1)
    cy = -sh * 0.05
    r = sw * 1.05
    small = Image.new("RGBA", (sw, sh))
    px = []
    base = (16, 16, 16)
    gold = (188, 164, 128)
    for yy in range(sh):
        for xx in range(sw):
            dist = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5 / r
            k = max(0.0, 1 - dist) ** 2 * 0.17
            px.append(tuple(int(base[c] + (gold[c] - base[c]) * k) for c in range(3)) + (255,))
    small.putdata(px)
    bg = small.resize((w, h), Image.BICUBIC)
    ImageDraw.Draw(bg).rectangle((0, 0, w, 8), fill=GOLD)
    return bg


# ── layout ───────────────────────────────────────────────────
@dataclass
class Layer:
    img: Image.Image
    x: int
    y: int
    t: float = 0.0      # reveal time (seconds) in reels
    anim: str = "up"    # up | fade | pop | count


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
    tall = h > w * 1.4
    m = 80
    inner = w - m * 2
    layers: list[Layer] = []
    t = 0.3

    logo = logo_layer(54)
    layers.append(Layer(logo, m, 64, 0.0, "fade"))

    track_label = CFG["tracks"].get(item.track, {}).get("label", item.track.upper())
    k = pill(d.get("kicker") or track_label, font("body", "SemiBold", 28))
    y = 64 + 54 + S(90 if tall else 60)
    layers.append(Layer(k, m, y, t))
    y += k.height + S(36)
    t += 0.5

    headline = d.get("headline") or item.d.get("topic", "")
    head_img = fit_text(headline, "head", "Bold", inner, 4 if tall else 3, S(104 if tall else 92), S(56), line_gap=1.08)
    layers.append(Layer(head_img, m, y, t))
    y += head_img.height + S(50 if tall else 34)
    t += 0.9

    template = d.get("template") or ("stat" if d.get("stat_value") else "myth" if d.get("myth") else "tip")

    if template == "stat" and d.get("stat_value"):
        sv = d["stat_value"]
        fsize = S(230 if tall else 190)
        f = font("head", "Bold", fsize)
        while f.getlength(str(sv)) > inner and fsize > 100:
            fsize -= 10
            f = font("head", "Bold", fsize)
        asc, desc = f.getmetrics()
        sim = Image.new("RGBA", (inner, asc + desc), (0, 0, 0, 0))
        ImageDraw.Draw(sim).text((0, 0), str(sv), font=f, fill=GOLD)
        layers.append(Layer(sim, m - 6, y, t, "count" if video else "up"))
        y += sim.height + 4
        t += 1.4
        if d.get("stat_label"):
            lim, _ = text_layer(d["stat_label"], font("body", "Medium", S(40 if tall else 34)), inner, color=CARBON)
            layers.append(Layer(lim, m, y, t - 0.6))
            y += lim.height + S(30)

    if template == "myth" and d.get("myth"):
        for label, txt, col in (("MYTH", d["myth"], SLATE), ("FACT", d.get("fact", ""), GOLD)):
            tag = pill(label, font("body", "Bold", 26), fg=OBSIDIAN if label == "FACT" else CARBON,
                       outline=col, fill=col if label == "FACT" else None)
            body, _ = text_layer(txt, font("body", "Medium", S(44 if tall else 38)), inner, color=WHITE if label == "FACT" else CARBON)
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
        body, _ = text_layer(p, pf, inner - 90, color=CARBON)
        row = Image.new("RGBA", (inner, max(body.height, 50)), (0, 0, 0, 0))
        ImageDraw.Draw(row).text((0, 0), f"{i + 1:02d}", font=nf, fill=GOLD)
        row.alpha_composite(body, (90, 0))
        layers.append(Layer(row, m, y, t))
        y += row.height + S(28 if tall else 20)
        t += 1.1

    # footer: headshot + name + CTA + microtext
    hs = 250 if tall else 200
    footer_top = h - (420 if tall else 330)
    side_right = variant % 2 == 0
    head = headshot_circle(pick_headshot(item, platform), hs)
    hx = w - m - hs if side_right else m
    layers.append(Layer(head, hx, footer_top, 0.2, "pop"))

    name_x = m if side_right else m + hs + 36
    name_w = w - m * 2 - hs - 36
    nm = font("head", "Bold", 46 if tall else 40)
    sub = font("body", "Regular", 28 if tall else 25)
    nb = Image.new("RGBA", (name_w, 150), (0, 0, 0, 0))
    nd = ImageDraw.Draw(nb)
    nd.text((0, 0), CFG["brand"]["name"].upper(), font=nm, fill=WHITE)
    nd.text((0, 62), f'{CFG["brand"]["title"]} · {CFG["brand"]["brokerage"]}', font=sub, fill=CARBON)
    site = CFG["brand"]["agent_site"] if item.track == "agent_attraction" else CFG["brand"]["website"]
    nd.text((0, 100), f'{CFG["brand"]["phone"]}  ·  {site}', font=sub, fill=GOLD)
    layers.append(Layer(nb, name_x, footer_top + (hs - 140) // 2, 0.5, "fade"))

    overflow = y + S(30) > footer_top
    cta = d.get("cta")
    if cta:
        cf = font("head", "Bold", 38 if tall else 32)
        cim, _ = text_layer(cta, cf, inner - 60, color=OBSIDIAN, gold=OBSIDIAN, align="center")
        bar = Image.new("RGBA", (inner, cim.height + 44), (0, 0, 0, 0))
        ImageDraw.Draw(bar).rounded_rectangle((0, 0, inner - 1, bar.height - 1), radius=18, fill=GOLD)
        bar.alpha_composite(cim, (30, 22))
        cy = footer_top - bar.height - (50 if tall else 30)
        overflow = y + S(24) > cy
        layers.append(Layer(bar, m, cy, t + 0.2, "pop"))
        t += 1.0

    mf = font("body", "Regular", 22)
    micro = f'DRE #{CFG["brand"]["dre"]} · {CFG["brand"]["brokerage"]} · Equal Housing Opportunity'
    mim, _ = text_layer(micro, mf, inner, color=SLATE, align="center")
    layers.append(Layer(mim, m, h - 70, 0.0, "fade"))

    return background(w, h, variant), layers, t, overflow


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
    ImageDraw.Draw(img).text((0, 0), txt, font=f, fill=GOLD)
    a = img.getchannel("A").point(lambda v: int(v * min(1, p * 3)))
    img.putalpha(a)
    return img


# ── per-item rendering ──────────────────────────────────────
def render_item(item: Item, force: bool = False) -> list[str]:
    made = []
    mdir = item.path.parent / "media"
    for i, plat in enumerate(item.platforms()):
        existing = item.media_path(plat)
        if existing and existing.exists() and not force:
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
        made.append(str(out.relative_to(ROOT)))
    if made:
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
