"""Checks every queued item before it can post: format, caption limits,
compliance language and risky wording (Fair Housing, guarantees).

  python -m bot.validate          # check the next few days, exit 1 on errors
"""
from __future__ import annotations

import re
import sys

from .common import CFG, KINDS, load_items, recent_days

LIMITS = {"instagram": 2200, "facebook": 60000, "linkedin": 3000, "tiktok": 2200}
HASHTAG_LIMIT = {"instagram": 30}

# Wording that creates legal/compliance risk in real estate advertising.
BLOCK = [
    r"\bguarantee(d|s)?\b", r"\brisk[- ]free\b", r"\b100\+ deals\b",
    r"\bno section 8\b", r"\bsection 8 not\b",
    r"\b(perfect|ideal|great) for (families|kids|couples|singles|retirees)\b", r"\bfamily[- ]friendly neighborhood\b",
    r"\bsafe neighborhood\b", r"\bexclusive (community|neighborhood)\b", r"\bbachelor pad\b",
    r"\b(christian|church|jewish|muslim|hispanic|asian|white|black) (neighborhood|community|area)\b",
    r"\bno (kids|children|pets allowed for families)\b", r"\bable[- ]bodied\b",
]
WARN = [
    r"\bbest agent\b", r"\b#1\b", r"\bnumber one\b", r"\bwill (go up|appreciate|increase) in value\b",
    r"\bcan't lose\b", r"\bprices will\b", r"\brates will\b",
]


def check(item) -> tuple[list[str], list[str]]:
    errs, warns = [], []
    d = item.d
    if item.kind not in KINDS:
        errs.append(f"kind must be one of {KINDS}")
    if item.track not in CFG["tracks"]:
        errs.append(f"unknown track '{item.track}' (see config.yaml → tracks)")
    design = d.get("design") or {}
    if not (design.get("headline") or d.get("topic")):
        errs.append("design.headline is required")
    if design.get("template") == "meme" and not (design.get("setup") and design.get("punch")):
        errs.append("meme template needs both design.setup and design.punch")
    if item.kind != "story":
        for p in item.platforms():
            cap = item.caption(p)
            if not cap:
                errs.append(f"missing caption for {p}")
                continue
            if len(cap) > LIMITS[p]:
                errs.append(f"{p} caption too long ({len(cap)}/{LIMITS[p]})")
            if p in HASHTAG_LIMIT and cap.count("#") > HASHTAG_LIMIT[p]:
                errs.append(f"{p}: too many hashtags")
    text = " ".join([str(design), str(d.get("captions", ""))]).lower()
    for pat in BLOCK:
        if re.search(pat, text):
            errs.append(f"compliance: blocked wording matches '{pat}'")
    for pat in WARN:
        if re.search(pat, text):
            warns.append(f"check wording: '{pat}'")
    if item.track == "laws_and_updates" and not d.get("sources"):
        errs.append("law posts must list at least one source (official .gov preferred)")
    return errs, warns


def _key(it) -> str:
    d = it.d.get("design") or {}
    txt = (d.get("headline") or it.d.get("topic") or "").lower()
    return " ".join(re.findall(r"[a-z0-9]+", txt))


def duplicates() -> dict:
    """Same headline/topic already used in the last 120 days (or twice in the queue) = duplicate."""
    from datetime import timedelta
    from .common import now
    since = now().date() - timedelta(days=120)
    seen, dups = {}, {}
    for it in sorted(load_items(), key=lambda i: (i.day, i.id)):
        if it.day < since or it.kind == "story":
            continue
        k = _key(it)
        if not k:
            continue
        if k in seen:
            dups[(it.day, it.id)] = seen[k]
        else:
            seen[k] = f"{it.day}/{it.id}"
    return dups


def main():
    bad = 0
    dups = duplicates()
    for it in load_items(recent_days(0, 7)):
        errs, warns = check(it)
        if (it.day, it.id) in dups and not any((it.d.get("status") or {}).get(p, {}).get("state") == "posted" for p in it.platforms()):
            errs.append(f"duplicate of {dups[(it.day, it.id)]} — write a new angle")
        tag = f"{it.day}/{it.id}"
        for w in warns:
            print(f"⚠ {tag}: {w}")
        for e in errs:
            print(f"✗ {tag}: {e}")
        if errs:
            bad += 1
            # an item with errors never auto-posts
            if not it.d.get("approved_override") and it.d.get("approved") is not False:
                it.d["approved"] = False
                it.d["blocked_reason"] = "; ".join(errs)[:500]
                it.save()
    print(f"validate: {bad} item(s) with errors")
    sys.exit(1 if bad and "--strict" in sys.argv else 0)


if __name__ == "__main__":
    main()
