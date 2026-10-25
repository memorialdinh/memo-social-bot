"""Has Memo posted this before?

Checks a topic against his REAL posting history — the captions analytics pulled
from Instagram and Facebook (data/posts.csv), going back further than this bot
has existed — not just the bot's own topic log.

  python -m bot.seen "price per square foot"
  python -m bot.seen "rate lock" "title insurance" "HOA dues"
  python -m bot.seen --days 180 "ADU"
  python -m bot.seen --plan            # check every topic in week-plan.md

Exit code is 1 if anything matched, so a workflow can fail on a duplicate.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import timedelta

from .common import DATA, ROOT, now

# words too common to mean anything on their own
STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "your", "you", "it",
        "is", "are", "what", "how", "why", "with", "that", "this", "at", "be", "not", "do",
        "does", "can", "when", "from", "by", "as", "if", "my", "me", "but", "so", "about",
        "home", "homes", "house", "real", "estate", "buyer", "buyers", "seller", "sellers"}


def words(s: str) -> set:
    return {w for w in re.findall(r"[a-z0-9]+", (s or "").lower()) if w not in STOP and len(w) > 2}


def history(days: int) -> list[dict]:
    path = DATA / "posts.csv"
    if not path.exists():
        print(f"! {path} is missing — run `python -m bot.analytics` first. "
              "Without it a topic cannot be checked and should NOT be assumed fresh.", file=sys.stderr)
        sys.exit(2)
    since = (now() - timedelta(days=days)).isoformat()
    out = []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (r.get("caption") or "").strip() and (r.get("posted_at") or "") >= since:
                out.append(r)
    return out


def check(topic: str, rows: list[dict], threshold: float) -> list[tuple]:
    tw = words(topic)
    if not tw:
        return []
    hits = []
    for r in rows:
        cap = r["caption"]
        cw = words(cap)
        if not cw:
            continue
        overlap = len(tw & cw) / len(tw)
        # a quoted phrase appearing outright always counts
        phrase = topic.lower().strip() in cap.lower()
        if phrase or overlap >= threshold:
            hits.append((round(1.0 if phrase else overlap, 2), r["posted_at"][:10],
                         r["platform"], cap[:100].replace("\n", " ")))
    hits.sort(reverse=True)
    # one row per distinct caption; the same post appears on both platforms
    seen, uniq = set(), []
    for h in hits:
        k = h[3][:50]
        if k in seen:
            continue
        seen.add(k)
        uniq.append(h)
    return uniq[:4]


def plan_topics() -> list[str]:
    p = ROOT / "knowledge" / "week-plan.md"
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if re.match(r"\|\s*[pr]\d\s*\|", line):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 4:
                out.append(cells[3])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topics", nargs="*")
    ap.add_argument("--days", type=int, default=120)
    ap.add_argument("--threshold", type=float, default=0.5,
                    help="share of the topic's distinctive words that must appear (0-1)")
    ap.add_argument("--plan", action="store_true", help="check every topic in knowledge/week-plan.md")
    a = ap.parse_args()

    topics = list(a.topics) + (plan_topics() if a.plan else [])
    if not topics:
        ap.error("give a topic, or --plan")

    rows = history(a.days)
    print(f"checking {len(topics)} topic(s) against {len(rows)} posts from the last {a.days} days\n")
    bad = 0
    for t in topics:
        hits = check(t, rows, a.threshold)
        if hits:
            bad += 1
            print(f"✗ ALREADY COVERED — {t}")
            for score, d, plat, cap in hits:
                print(f"    {d}  {plat:<9} ({score:.0%} match)  {cap}")
        else:
            print(f"✓ fresh — {t}")
    print(f"\n{bad} of {len(topics)} already covered")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
