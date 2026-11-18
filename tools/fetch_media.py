"""Downloads finished carousel slides (exported from Canva) into the queue.

A carousel item lists its slide download links under `media_src`. This saves
each one as queue/<day>/media/<id>-<n>.jpg, points every platform's media at
that list, and removes `media_src` once all slides are saved (Canva's links are
signed and expire within a day, so they shouldn't sit in the repo).

Runs in the Prepare workflow before render. Safe to run repeatedly.
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

import requests
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from bot.common import ROOT, load_items  # noqa: E402


FEED_W, FEED_H = 1080, 1350  # Instagram's API refuses feed images taller than 4:5


def fit_feed(img: Image.Image) -> Image.Image:
    """Fit a slide into 1080x1350 without cropping anything (the footer, DRE and
    logo sit at the edges). Taller slides, like Canva's 3:4, are scaled to the
    full height and the thin side margins are filled with a blurred copy."""
    if img.width / img.height >= FEED_W / FEED_H - 0.005:
        return img
    from PIL import ImageFilter
    bg = img.resize((FEED_W, FEED_H)).filter(ImageFilter.GaussianBlur(40))
    w = round(img.width * FEED_H / img.height)
    fg = img.resize((w, FEED_H), Image.LANCZOS)
    bg.paste(fg, ((FEED_W - w) // 2, 0))
    return bg


def main() -> int:
    failed = 0
    for it in load_items():
        srcs = it.d.get("media_src")
        if not it.is_carousel or not srcs:
            continue
        mdir = it.path.parent / "media"
        mdir.mkdir(parents=True, exist_ok=True)
        rels, ok = [], True
        for n, url in enumerate(srcs, 1):
            out = mdir / f"{it.id}-{n}.jpg"
            if not out.exists():
                try:
                    r = requests.get(url, timeout=60)
                    r.raise_for_status()
                    img = fit_feed(Image.open(io.BytesIO(r.content)).convert("RGB"))
                    img.save(out, "JPEG", quality=92, optimize=True)
                    print(f"saved {out.relative_to(ROOT)} {img.size}")
                except Exception as e:  # expired link etc. — leave it for a re-export
                    print(f"✗ {it.day}/{it.id} slide {n}: {e}")
                    ok = False
                    continue
            rels.append(str(out.relative_to(ROOT)))
        if ok:
            for plat in it.platforms():
                it.d["media"][plat] = rels
            it.d.pop("media_src", None)
            it.save()
        else:
            failed += 1
    print(f"fetch_media: {failed} carousel(s) still missing slides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
