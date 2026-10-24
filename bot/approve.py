"""Approve queued items so they can post.

  python -m bot.approve 2026-10-24            # approve a whole day
  python -m bot.approve 2026-10-24 p1 r2      # approve specific items
  python -m bot.approve --list                # show what's waiting
"""
from __future__ import annotations

import sys
from datetime import date

from .common import load_items


def main():
    args = sys.argv[1:]
    if not args or args[0] == "--list":
        waiting = [it for it in load_items() if it.needs_approval()]
        for it in waiting:
            reason = it.d.get("blocked_reason", "")
            print(f"{it.day}/{it.id}  [{it.track}]  {(it.d.get('design') or {}).get('headline', '')}  {reason}")
        print(f"{len(waiting)} waiting")
        return
    day = date.fromisoformat(args[0])
    ids = set(args[1:])
    n = 0
    for it in load_items([day]):
        if ids and it.id not in ids:
            continue
        it.d["approved"] = True
        it.d["approved_override"] = True  # you looked at it; validator won't re-block
        it.d.pop("blocked_reason", None)
        it.save()
        n += 1
    print(f"approved {n} item(s) on {day}")


if __name__ == "__main__":
    main()
