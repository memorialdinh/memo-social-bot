"""Posts everything that's due. Runs every 15 minutes from GitHub Actions.

  python -m bot.publish            # post what's due now
  python -m bot.publish --dry-run  # show what would post, touch nothing
"""
from __future__ import annotations

import argparse
import csv
import os
import traceback
from datetime import timedelta

from .common import CFG, DATA, ROOT, Item, load_items, now, recent_days
from .platforms.linkedin import LinkedIn
from .platforms.meta import Meta
from .platforms.tiktok import TikTok

DONE = {"posted", "draft_sent", "skipped", "missed"}
MAX_PER_RUN = 8


def public_url(rel: str) -> str:
    """Instagram fetches images by URL; the repo is public so raw GitHub works."""
    repo = os.environ.get("GITHUB_REPOSITORY", "OWNER/REPO")
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{rel}"


def log(row: dict):
    path = DATA / "publish_log.csv"
    new = not path.exists()
    path.parent.mkdir(exist_ok=True)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["at", "day", "item", "kind", "track", "platform", "result", "remote_id", "detail"])
        if new:
            w.writeheader()
        w.writerow(row)


def post_one(item: Item, plat: str, clients: dict) -> tuple[str, str]:
    media = item.media_path(plat)
    if not media or not media.exists():
        raise RuntimeError("media missing — render step hasn't run")
    cap = item.caption(plat)
    rel = str(media.relative_to(ROOT))
    m, li, tt = clients["meta"], clients["linkedin"], clients["tiktok"]

    if plat == "instagram":
        if not m.ready_ig():
            return "waiting", "instagram keys not set"
        if item.kind == "story":
            return "posted", m.ig_image(public_url(rel), "", story=True)
        if media.suffix == ".mp4":
            return "posted", m.ig_reel(media, cap)
        return "posted", m.ig_image(public_url(rel), cap)

    if plat == "facebook":
        if not m.ready_fb():
            return "waiting", "facebook keys not set"
        if item.kind == "story":
            return "posted", m.fb_story_photo(media)
        if media.suffix == ".mp4":
            return "posted", m.fb_reel(media, cap)
        return "posted", m.fb_photo(media, cap)

    if plat == "linkedin":
        if not li.ready():
            return "waiting", "linkedin keys not set"
        title = (item.d.get("design") or {}).get("headline", "").replace("*", "")
        return "posted", li.post(media, cap, title)

    if plat == "tiktok":
        if not tt.ready():
            return "waiting", "tiktok keys not set"
        return "draft_sent", tt.upload_draft(media)

    return "skipped", f"unknown platform {plat}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    t = now()
    late = timedelta(hours=CFG["schedule"]["max_late_hours"])
    clients = {"meta": Meta(), "linkedin": LinkedIn(), "tiktok": TikTok()}
    done = 0

    for item in load_items(recent_days(2, 0)):
        for plat in item.platforms():
            if done >= MAX_PER_RUN:
                break
            if item.state(plat) in DONE:
                continue
            when = item.scheduled_at(plat)
            if not when or when > t:
                continue
            if item.needs_approval():
                if item.state(plat) != "needs_approval":
                    item.set_status(plat, state="needs_approval")
                continue
            if t - when > late:
                if not a.dry_run:
                    item.set_status(plat, state="missed", detail=f"more than {late} late")
                continue
            if a.dry_run:
                print(f"[dry-run] would post {item.day}/{item.id} ({item.kind}) to {plat}  — due {when:%H:%M}")
                continue
            try:
                state, rid = post_one(item, plat, clients)
            except Exception as e:  # keep going with the other posts
                err = f"{type(e).__name__}: {e}"[:400]
                tries = int((item.d["status"].get(plat) or {}).get("tries", 0)) + 1
                final = tries >= 3
                item.set_status(plat, state="failed" if final else "retry", tries=tries, error=err)
                log({"at": t.isoformat(timespec="seconds"), "day": item.day, "item": item.id, "kind": item.kind,
                     "track": item.track, "platform": plat, "result": "failed" if final else "retry", "remote_id": "", "detail": err})
                print(f"✗ {item.id} → {plat}: {err}")
                traceback.print_exc()
                continue
            if state == "waiting":
                print(f"… {item.id} → {plat}: {rid}")
                continue
            item.set_status(plat, state=state, id=str(rid))
            log({"at": t.isoformat(timespec="seconds"), "day": item.day, "item": item.id, "kind": item.kind,
                 "track": item.track, "platform": plat, "result": state, "remote_id": rid, "detail": ""})
            print(f"✓ {item.id} → {plat}: {state} {rid}")
            done += 1
    print(f"done: {done} published this run")


if __name__ == "__main__":
    main()
