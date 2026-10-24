"""Assigns posting times to queued items.

Uses data/best_times.json (written by the analytics bot) once there's enough
data, otherwise the default hours in config.yaml. Minutes are varied a little
so posts don't look robotic.
"""
from __future__ import annotations

from datetime import datetime, time, timedelta

from .common import CFG, DATA, TZ, Item, load_items, read_json, recent_days, stable_int

S = CFG["schedule"]


def ranked_hours(platform: str, weekday: int, kind: str) -> list[int]:
    if kind == "story":
        base = list(S["story_hours"])
    else:
        base = list(S["default_feed_hours"])
    if S.get("use_best_times", True):
        bt = read_json(DATA / "best_times.json", {})
        learned = ((bt.get("platforms") or {}).get(platform) or {}).get(str(weekday))
        if learned and kind != "story":
            base = learned + [h for h in base if h not in learned]
        elif learned and kind == "story":
            # stories: spread across the day, nudged toward strong hours
            base = sorted(set(base[:3] + learned[:2]))
    lo, hi = S["earliest_hour"], S["latest_hour"]
    return [h for h in base if lo <= h <= hi]


def plan_day(items: list[Item]) -> int:
    if not items:
        return 0
    day = items[0].day
    wd = day.weekday()
    changed = 0
    platforms = sorted({p for it in items for p in it.platforms()})
    for plat in platforms:
        taken = [it.scheduled_at(plat) for it in items if it.scheduled_at(plat)]
        for kind in ("post", "reel", "story"):
            todo = [it for it in items if it.kind == kind and plat in it.platforms() and not it.scheduled_at(plat)]
            hours = ranked_hours(plat, wd, kind)
            gap = timedelta(minutes=S["min_gap_minutes"] if kind != "story" else 45)
            for it in todo:
                fixed = it.d.get("time")
                if fixed and fixed != "auto":
                    hh, mm = map(int, str(fixed).split(":"))
                    when = datetime.combine(day, time(hh, mm), TZ)
                else:
                    when = None
                    for h in hours + list(range(S["earliest_hour"], S["latest_hour"] + 1)):
                        jitter = stable_int(day, it.id, plat) % 23 + 3  # :03 .. :25
                        cand = datetime.combine(day, time(h, jitter), TZ)
                        same_kind = [t for t, k in taken_kinds(items, plat) if (k == "story") == (kind == "story")]
                        if all(abs(cand - t) >= gap for t in same_kind):
                            when = cand
                            break
                    if when is None:
                        when = datetime.combine(day, time(S["latest_hour"], 30), TZ)
                it.d["schedule"][plat] = when.isoformat(timespec="minutes")
                it.save()
                taken.append(when)
                changed += 1
    return changed


def taken_kinds(items: list[Item], plat: str):
    for it in items:
        t = it.scheduled_at(plat)
        if t:
            yield t, it.kind


def main():
    total = 0
    for d in recent_days(0, 3):
        items = load_items([d])
        total += plan_day(items)
    print(f"planned {total} slots")
    for it in load_items(recent_days(0, 3)):
        for p in it.platforms():
            print(f"  {it.day} {it.id:<4} {it.kind:<6} {p:<10} {it.d['schedule'].get(p)}")


if __name__ == "__main__":
    main()
