"""Analytics bot: pulls your numbers, learns your best posting times,
scores what content works, and rebuilds the dashboard.

  python -m bot.analytics            # pull live data (needs keys)
  python -m bot.analytics --offline  # rebuild from saved data only
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import datetime, timedelta

from .common import CFG, DATA, TZ, ApiError, load_items, now, read_json, write_json
from .platforms.meta import Meta
from .platforms.tiktok import TikTok

POSTS_CSV = DATA / "posts.csv"
FOLLOW_CSV = DATA / "followers.csv"
FIELDS = ["platform", "remote_id", "posted_at", "kind", "track", "item", "caption",
          "likes", "comments", "shares", "saves", "views", "reach", "engagement", "rate", "permalink",
          "template", "theme", "save_rate", "share_rate", "followers"]


# ── storage ──────────────────────────────────────────────────
def load_posts() -> dict:
    rows = {}
    if POSTS_CSV.exists():
        with open(POSTS_CSV, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                rows[(r["platform"], r["remote_id"])] = r
    return rows


def save_posts(rows: dict):
    POSTS_CSV.parent.mkdir(exist_ok=True)
    with open(POSTS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in sorted(rows.values(), key=lambda r: r["posted_at"]):
            w.writerow({k: r.get(k, "") for k in FIELDS})


def record_followers(platform: str, count):
    if count in (None, ""):
        return
    today = now().date().isoformat()
    rows = []
    if FOLLOW_CSV.exists():
        with open(FOLLOW_CSV, encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f) if not (r["date"] == today and r["platform"] == platform)]
    rows.append({"date": today, "platform": platform, "followers": int(count)})
    with open(FOLLOW_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["date", "platform", "followers"])
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["date"], r["platform"])))


def our_items_by_remote_id() -> dict:
    """Map platform post ids back to our queue items so we know kind + track."""
    out = {}
    for it in load_items():
        for plat, st in (it.d.get("status") or {}).items():
            if st.get("id"):
                out[(plat, str(st["id"]))] = it
    return out


def n(v) -> int:
    try:
        return int(float(v or 0))
    except (TypeError, ValueError):
        return 0


# ── collectors ───────────────────────────────────────────────
_ig_metrics_ok: dict = {}


def ig_insights(m: Meta, media_id: str, product: str) -> dict:
    wanted = ["reach", "saved", "shares", "views", "total_interactions"]
    ok = _ig_metrics_ok.get(product)
    candidates = [ok] if ok else [wanted] + [[x] for x in wanted]
    out = {}
    good = []
    for metrics in candidates:
        try:
            j = m.get(f"{media_id}/insights", metric=",".join(metrics))
            for d in j.get("data", []):
                out[d["name"]] = (d.get("values") or [{}])[0].get("value", d.get("total_value", {}).get("value"))
            good += metrics
            if metrics is wanted or metrics is ok:
                break
        except ApiError:
            continue
    if good and not ok:
        _ig_metrics_ok[product] = good
    return out


def collect_instagram(m: Meta, rows: dict, idmap: dict) -> dict:
    acct = m.get(m.ig_id, fields="username,followers_count,media_count")
    record_followers("instagram", acct.get("followers_count"))
    j = m.get(f"{m.ig_id}/media", fields="id,caption,media_type,media_product_type,timestamp,like_count,comments_count,permalink", limit=100)
    for p in j.get("data", []):
        ins = ig_insights(m, p["id"], p.get("media_product_type", "FEED"))
        it = idmap.get(("instagram", p["id"]))
        kind = it.kind if it else ("reel" if p.get("media_product_type") == "REELS" else "post")
        upsert(rows, "instagram", p["id"], p["timestamp"], kind, it,
               caption=p.get("caption", ""), likes=p.get("like_count"), comments=p.get("comments_count"),
               shares=ins.get("shares"), saves=ins.get("saved"), views=ins.get("views"),
               reach=ins.get("reach"), permalink=p.get("permalink"), followers=acct.get("followers_count"))
    # stories only report insights for 24h — grab them daily
    try:
        for s in m.get(f"{m.ig_id}/stories", fields="id,timestamp,permalink").get("data", []):
            ins = ig_insights(m, s["id"], "STORY")
            upsert(rows, "instagram", s["id"], s["timestamp"], "story", idmap.get(("instagram", s["id"])),
                   reach=ins.get("reach"), shares=ins.get("shares"), views=ins.get("views"),
                   likes=ins.get("total_interactions"), permalink=s.get("permalink"), followers=acct.get("followers_count"))
    except ApiError:
        pass
    # when your followers are online (great for best-time picking before you have history)
    try:
        oj = m.get(f"{m.ig_id}/insights", metric="online_followers", period="lifetime")
        vals = (oj.get("data") or [{}])[0].get("values") or []
        hours = defaultdict(int)
        for v in vals:
            for h, c in (v.get("value") or {}).items():
                hours[int(h)] += int(c)
        if hours:
            write_json(DATA / "ig_online_followers.json", {"tz": CFG["api"]["instagram_online_followers_tz"], "hours": hours})
    except ApiError:
        pass
    return acct


def collect_facebook(m: Meta, rows: dict, idmap: dict):
    page = m.get(m.page_id, fields="name,followers_count,fan_count")
    record_followers("facebook", page.get("followers_count") or page.get("fan_count"))
    fields = "id,message,created_time,permalink_url,shares,reactions.summary(total_count).limit(0),comments.summary(total_count).limit(0)"
    j = m.get(f"{m.page_id}/published_posts", fields=fields, limit=100)
    for p in j.get("data", []):
        reach = None
        for metric in ("post_impressions_unique", "post_total_media_view_unique"):
            try:
                ins = m.get(f"{p['id']}/insights", metric=metric)
                reach = (ins.get("data") or [{}])[0].get("values", [{}])[0].get("value")
                if reach is not None:
                    break
            except ApiError:
                continue
        it = idmap.get(("facebook", p["id"]))
        upsert(rows, "facebook", p["id"], p["created_time"], it.kind if it else "post", it,
               caption=p.get("message", ""), likes=(p.get("reactions") or {}).get("summary", {}).get("total_count"),
               comments=(p.get("comments") or {}).get("summary", {}).get("total_count"),
               shares=(p.get("shares") or {}).get("count"), reach=reach, permalink=p.get("permalink_url"),
               followers=page.get("followers_count") or page.get("fan_count"))


def collect_tiktok(t: TikTok, rows: dict, idmap: dict):
    for v in t.videos(20):
        ts = datetime.fromtimestamp(int(v["create_time"]), TZ).isoformat()
        upsert(rows, "tiktok", v["id"], ts, "reel", None, caption=v.get("title", ""),
               likes=v.get("like_count"), comments=v.get("comment_count"), shares=v.get("share_count"),
               views=v.get("view_count"), reach=v.get("view_count"), permalink=v.get("share_url"))


def upsert(rows, platform, rid, ts, kind, item, followers=None, **m):
    eng = n(m.get("likes")) + n(m.get("comments")) + n(m.get("shares")) + n(m.get("saves"))
    base = n(m.get("reach")) or n(m.get("views")) or n(followers)
    rows[(platform, str(rid))] = {
        "platform": platform, "remote_id": str(rid),
        "posted_at": datetime.fromisoformat(ts.replace("Z", "+00:00").replace("+0000", "+00:00")).astimezone(TZ).isoformat(timespec="minutes"),
        "kind": kind, "track": item.track if item else "", "item": f"{item.day}/{item.id}" if item else "",
        "caption": (m.get("caption") or "")[:140].replace("\n", " "),
        **{k: n(m.get(k)) for k in ("likes", "comments", "shares", "saves", "views", "reach")},
        "engagement": eng, "rate": round(eng / base, 4) if base else 0, "permalink": m.get("permalink") or "",
        # what the graphic looked like, stamped at render time
        **_design_of(item, platform),
        # saves and shares are what push reach; score them on their own
        "save_rate": round(n(m.get("saves")) / base, 4) if base else 0,
        "share_rate": round(n(m.get("shares")) / base, 4) if base else 0,
        "followers": n(followers),
    }


def _design_of(item, platform: str) -> dict:
    r = ((item.d.get("rendered") if item else None) or {}).get(platform) or {}
    return {"template": r.get("template", ""), "theme": r.get("theme", "")}


# ── learning ─────────────────────────────────────────────────
def best_times(rows: dict) -> dict:
    """Score each weekday x hour slot by how many people a post actually reaches
    and how many of them engage, shrunk toward the platform average so one lucky
    post doesn't skew everything.

    Rewritten 2026-10-28 after a timing audit of 98 pre-bot Instagram posts and
    119 Facebook posts (May-Oct 2026). Three things the old version got wrong:

    1. It ranked on engagement RATE alone. Rate is engagement/reach, so an hour
       that reaches almost nobody can top the ranking. Reach is this account's
       binding constraint, so hours are now scored on reach per post AND
       engagement per post, weighted 40/60.
    1b. It resolved to the individual hour, which this volume of posting cannot
       support - most hours hold 1-6 posts, so one good afternoon post put 2pm
       near the top of the ranking. Scores are now driven mainly by the four
       daypart BANDS (early/morning/afternoon/evening), which hold 14-32 posts
       each and are the finest cut the data actually supports. The hour's own
       number only orders hours inside a band.
    2. It ranked every platform with 8+ posts. Facebook averaged ~2 people
       reached across 119 posts, so its hour ranking was noise on a near-zero
       base. A platform now needs MIN_MEDIAN_REACH before it gets a ranking at
       all; below that, plan.py falls back to the config hours.
    3. It blended the Instagram online-followers curve into the score (weight
       0.2-0.5). That curve peaks 1-7pm, which measured out as this account's
       WEAKEST window - 3.5 engagements per post against 6.3-8.3 everywhere
       else. The blend was actively pulling posts into the worst hours. The
       curve is still written to the payload for reference, but it no longer
       moves the ranking.
    """
    K = 8                    # shrinkage toward the prior; high, because most
                             # single hours hold only a handful of posts
    W_ENG, W_REACH = 0.6, 0.4
    W_BAND = 0.75            # the daypart band carries the score; the hour only
                             # breaks ties within it
    out = {"updated": now().isoformat(timespec="minutes"), "platforms": {}, "heatmap": {},
           "samples": {}, "excluded": {}}
    online = read_json(DATA / "ig_online_followers.json", {}).get("hours", {})
    by_plat = defaultdict(list)
    for r in rows.values():
        if r["kind"] == "story":
            continue
        t = datetime.fromisoformat(r["posted_at"])
        by_plat[r["platform"]].append((t.weekday(), t.hour, _f(r.get("engagement")), _f(r.get("reach"))))
    lo, hi = CFG["schedule"]["earliest_hour"], CFG["schedule"]["latest_hour"]
    for plat in ("instagram", "facebook", "linkedin", "tiktok"):
        data = by_plat.get(plat, [])
        out["samples"][plat] = len(data)
        if not data:
            out["heatmap"][plat] = {str(wd): {h: 0 for h in range(lo, hi + 1)} for wd in range(7)}
            continue
        med_reach = median(sorted(x[3] for x in data))
        mean_eng = sum(x[2] for x in data) / len(data)
        mean_reach = sum(x[3] for x in data) / len(data) or 1.0

        def rel(cell_vals, hour_vals, mean):
            """Shrink an hour's mean toward the same-hour-any-day mean, then the
            platform mean, and express it relative to the platform mean."""
            prior = ((sum(hour_vals) + K * mean) / (len(hour_vals) + K)) if hour_vals else mean * 0.92
            val = (sum(cell_vals) + K * prior) / (len(cell_vals) + K)
            return (val / mean) if mean else 0.0

        cells_e, cells_r = defaultdict(list), defaultdict(list)
        hours_e, hours_r = defaultdict(list), defaultdict(list)
        bands_e, bands_r = defaultdict(list), defaultdict(list)
        for wd, h, e, rc in data:
            cells_e[(wd, h)].append(e); cells_r[(wd, h)].append(rc)
            hours_e[h].append(e); hours_r[h].append(rc)
            bands_e[band_of(h)].append(e); bands_r[band_of(h)].append(rc)
        band_score = {}
        for b in set(band_of(h) for h in range(0, 24)):
            be, br = bands_e.get(b, []), bands_r.get(b, [])
            if not be:
                band_score[b] = 0.92
                continue
            e_rel = (sum(be) / len(be)) / mean_eng if mean_eng else 0.0
            r_rel = (sum(br) / len(br)) / mean_reach
            band_score[b] = W_ENG * e_rel + W_REACH * r_rel
        heat, ranked = {}, {}
        for wd in range(7):
            scores = {}
            for h in range(lo, hi + 1):
                e_rel = rel(cells_e.get((wd, h), []), hours_e.get(h, []), mean_eng)
                r_rel = rel(cells_r.get((wd, h), []), hours_r.get(h, []), mean_reach)
                hour_rel = W_ENG * e_rel + W_REACH * r_rel
                scores[h] = round(W_BAND * band_score[band_of(h)] + (1 - W_BAND) * hour_rel, 5)
            heat[str(wd)] = scores
            if len(data) >= 8 and med_reach >= MIN_MEDIAN_REACH:
                ranked[str(wd)] = [h for h, _ in sorted(scores.items(), key=lambda kv: -kv[1])][:6]
        out["heatmap"][plat] = heat
        if ranked:
            out["platforms"][plat] = ranked
        else:
            out["excluded"][plat] = (
                f"not ranked: {len(data)} posts, median reach {med_reach:.0f} "
                f"(needs 8+ posts and median reach >= {MIN_MEDIAN_REACH}). "
                "plan.py falls back to the config hours for this platform."
            )
    if online:
        out["ig_online_followers"] = {
            "hours": online,
            "note": "reference only - NOT used in the ranking. This curve peaks 1-7pm, "
                    "which measured as the weakest window for this account.",
        }
    return out


def _f(v) -> float:
    try:
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def median(xs: list) -> float:
    if not xs:
        return 0.0
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


MIN_MEDIAN_REACH = 10   # below this a platform's hour ranking is noise, not a lesson


def band_of(h: int) -> str:
    """Dayparts. These are the finest cut this posting volume supports: each
    holds 14-32 posts in the May-Oct 2026 window, where single hours hold 1-6."""
    if h < 9:
        return "early"
    if h < 13:
        return "morning"
    if h < 18:
        return "afternoon"
    return "evening"
MIN_SAMPLE = 4          # below this a difference is noise, not a lesson


def content_scores(rows: dict) -> dict:
    agg = defaultdict(lambda: {"posts": 0, "rate": 0.0, "eng": 0, "save": 0.0, "share": 0.0})
    since = now() - timedelta(days=60)
    recent = [r for r in rows.values() if datetime.fromisoformat(r["posted_at"]) >= since]
    for r in recent:
        keys = [f"track:{r['track'] or 'untagged'}", f"kind:{r['kind']}", f"platform:{r['platform']}"]
        if r.get("template"):
            keys.append(f"template:{r['template']}")
        if r.get("theme"):
            keys.append(f"theme:{r['theme']}")
        for key in keys:
            a = agg[key]
            a["posts"] += 1
            a["rate"] += float(r["rate"] or 0)
            a["eng"] += n(r["engagement"])
            a["save"] += float(r.get("save_rate") or 0)
            a["share"] += float(r.get("share_rate") or 0)
    res = {k: {"posts": v["posts"], "avg_rate": round(v["rate"] / v["posts"], 4),
               "avg_eng": round(v["eng"] / v["posts"], 1),
               "avg_save_rate": round(v["save"] / v["posts"], 4),
               "avg_share_rate": round(v["share"] / v["posts"], 4)}
           for k, v in agg.items() if v["posts"]}

    lab = lambda k: CFG["tracks"].get(k, {}).get("label", k).replace("_", " ").title()

    def ranked(prefix, metric="avg_rate", floor=MIN_SAMPLE):
        xs = [(k[len(prefix):], v) for k, v in res.items()
              if k.startswith(prefix) and v["posts"] >= floor]
        return sorted(xs, key=lambda kv: -kv[1][metric])

    # ── directives: what Scribe MUST change, in plain imperative ──
    directives, tips = [], []

    tracks = ranked("track:")
    if len(tracks) >= 2:
        best, worst = tracks[0], tracks[-1]
        if best[1]["avg_rate"] > worst[1]["avg_rate"] * 1.4:
            directives.append(
                f"Write an extra {lab(best[0])} piece and one fewer {lab(worst[0])} piece. "
                f"{lab(best[0])} earns {best[1]['avg_rate']*100:.1f}% vs {worst[1]['avg_rate']*100:.1f}% "
                f"over the last 60 days ({best[1]['posts']} vs {worst[1]['posts']} posts)."
            )

    kinds = {k[5:]: v for k, v in res.items() if k.startswith("kind:") and v["posts"] >= MIN_SAMPLE}
    if "reel" in kinds and "post" in kinds and kinds["reel"]["avg_rate"] > kinds["post"]["avg_rate"] * 1.3:
        directives.append(
            f"Write 3 reels and 2 posts today instead of 2 and 3. Reels are at "
            f"{kinds['reel']['avg_rate']*100:.1f}% against {kinds['post']['avg_rate']*100:.1f}% for static posts."
        )

    # saves and shares are what actually extend reach, so they get their own call
    savers = ranked("track:", "avg_save_rate")
    if savers and savers[0][1]["avg_save_rate"] > 0:
        directives.append(
            f"{lab(savers[0][0])} gets saved the most ({savers[0][1]['avg_save_rate']*100:.2f}% of reach). "
            "Saves and shares are what push a post to new people — write at least one piece built to be "
            "saved: a checklist, a number worth keeping, or a comparison."
        )
    sharers = ranked("template:", "avg_share_rate")
    if sharers and sharers[0][1]["avg_share_rate"] > 0:
        directives.append(
            f"The '{sharers[0][0]}' template gets shared most. Use it at least once today."
        )

    temps = ranked("template:")
    if len(temps) >= 3 and temps[-1][1]["avg_rate"] < temps[0][1]["avg_rate"] * 0.6:
        directives.append(
            f"Stop using the '{temps[-1][0]}' template for now — it runs at "
            f"{temps[-1][1]['avg_rate']*100:.1f}% against '{temps[0][0]}' at {temps[0][1]['avg_rate']*100:.1f}%."
        )

    themes = ranked("theme:")
    if len(themes) >= 3:
        tips.append(f"Best-performing look: {themes[0][0]} ({themes[0][1]['avg_rate']*100:.1f}%). "
                    f"Weakest: {themes[-1][0]} ({themes[-1][1]['avg_rate']*100:.1f}%).")

    thin = [k for k, v in res.items() if k.startswith(("track:", "template:")) and v["posts"] < MIN_SAMPLE]
    if thin:
        tips.append(f"Not enough data yet to judge: {', '.join(sorted(thin))} "
                    f"(fewer than {MIN_SAMPLE} posts each). Keep writing them so they can be measured.")

    # follower trend, so growth is visible and not just engagement rate
    growth = {}
    for plat in ("instagram", "facebook"):
        pts = sorted(((r["posted_at"], n(r.get("followers"))) for r in rows.values()
                      if r["platform"] == plat and n(r.get("followers"))), key=lambda x: x[0])
        if len(pts) >= 2:
            growth[plat] = {"first": pts[0][1], "latest": pts[-1][1], "change": pts[-1][1] - pts[0][1]}

    top = sorted(recent, key=lambda r: -float(r.get("save_rate") or 0) - float(r.get("share_rate") or 0))[:5]
    return {"updated": now().isoformat(timespec="minutes"), "scores": res,
            "directives": directives, "tips": tips, "followers": growth,
            "note": "directives are mandatory for the content writer; tips are advisory",
            "top_posts": [{k: r.get(k) for k in ("platform", "posted_at", "kind", "track", "template",
                                                 "theme", "caption", "saves", "shares", "rate", "permalink")}
                          for r in top]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args()
    rows = load_posts()
    errors = []
    if not a.offline:
        idmap = our_items_by_remote_id()
        m = Meta()
        if m.ready_ig():
            try:
                collect_instagram(m, rows, idmap)
            except Exception as e:
                errors.append(f"instagram: {e}")
        if m.ready_fb():
            try:
                collect_facebook(m, rows, idmap)
            except Exception as e:
                errors.append(f"facebook: {e}")
        t = TikTok()
        if t.ready():
            try:
                collect_tiktok(t, rows, idmap)
            except Exception as e:
                errors.append(f"tiktok: {e}")
        save_posts(rows)
    write_json(DATA / "best_times.json", best_times(rows))
    write_json(DATA / "insights.json", {**content_scores(rows), "errors": errors})
    from .dashboard import build
    build()
    print(f"analytics: {len(rows)} posts tracked; errors: {errors or 'none'}")


if __name__ == "__main__":
    main()
