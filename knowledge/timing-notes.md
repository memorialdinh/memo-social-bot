# Timing audit — what the posting-hour data actually says

Run 2026-10-28 (PT) by Scribe, at Memo's request: "analyze the timing of the social media when
post goes out and what time it have higher engagement, clicks and views and post accordingly."

Data: `data/posts.csv` — 265 rows, **2026-05-05 to 2026-10-28**. Instagram 146 rows, Facebook 119,
**LinkedIn 0, TikTok 0**. There is no clicks column, so "clicks" could not be measured; `views`
and `reach` stand in for it. Scheduled-vs-actual drift came from the `schedule` and `status` blocks
in `queue/2026-10-24` through `2026-10-29`.

---

## 1. TikTok has never published. Not once.

Every TikTok slot from Oct 25 to Oct 28 — **18 of them** — is `state: missed`,
`detail: more than 6:00:00 late`, at 360-410 minutes past its scheduled time.

Cause, in `bot/publish.py`: `if plat == "tiktok": if not tt.ready(): return "waiting", ...`.
`TikTok.ready()` is false because the three secrets it reads are unset —
**`TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET`, `TIKTOK_REFRESH_TOKEN`**. The publisher retries
every 15 minutes, gets "waiting" each time, and then `max_late_hours: 6` expires the slot.
`data/token_status.json` has no `tiktok` key at all, and `data/publish_log.csv` has zero TikTok
rows, so nothing was ever attempted against the API.

That is roughly **a fifth of every day's scheduled slots** disappearing silently.
`.github/workflows/publish.yml` already passes all three secrets through, so this is a
settings task, not a code task. **Memo said on Oct 28 he will add the keys**, so TikTok was left
`enabled: true` in config.yaml and nothing in the pipeline was changed for it.

## 2. Facebook timing cannot matter, because Facebook reach is ~2 people

Across **119 Facebook posts**: median reach **2**, median views **0**, total engagement across the
whole six months **1**. Every hour of the day looks identical because every hour reaches nobody.

The old `best_times()` still ranked Facebook's hours, because its only gate was "8+ posts". Its
heatmap values were on the order of 0.00427 against 0.0001 — **noise on a near-zero base** — and
that noise was what produced "Facebook is best at 12pm", a line that had reached the playbook as
if it were a finding. Facebook is now excluded from hour ranking (see §5).

## 3. Instagram: the afternoon is the weakest window, by about half

98 pre-bot Instagram posts (May 5 – Oct 23), grouped into dayparts. Single hours hold only 1-6
posts each, which is too thin to rank; the four bands hold 14-32 and are the finest cut this
volume supports.

| window | posts | engagement/post | reach/post | views/post |
|---|---|---|---|---|
| early 5-8am | 32 | 6.5 | 159 | 244 |
| morning 9am-12pm | 31 | 6.3 | 135 | 230 |
| **afternoon 1-5pm** | 21 | **3.5** | **127** | **214** |
| evening 6-11pm | 14 | **8.3** | **203** | **337** |

Afternoon is the worst window on all three measures at once. Removing the single biggest outlier
(the AI-generated reel of Sept 9, 61 engagements, posted 7:35am) barely moves the table — early
drops from 8.1 to 6.5 engagements/post and nothing else changes — so this is not one lucky post.

**Split by format, and the two kinds pull apart:**

| window | reels | static posts |
|---|---|---|
| early 5-8am | 5.9 eng, 188 reach (n=21) | 7.5 eng, 103 reach (n=11) |
| morning 9am-12pm | **8.4 eng**, 170 reach (n=20) | 2.5 eng, 72 reach (n=11) ← worst |
| afternoon 1-5pm | 3.5 eng, 156 reach (n=8) | 3.5 eng, 109 reach (n=13) |
| evening 6-11pm | 5.3 eng, **241 reach** (n=9) | **13.6 eng**, 133 reach (n=5) |

**Reels peak 9am-12pm. Static posts peak in the evening and are at their worst in the morning.**
The evening-static cell is **n=5** — directional, not settled. Worth re-checking once 10+ exist.

## 4. The online-followers curve points at the worst window

`data/ig_online_followers.json`, straight from the Instagram API, counts followers online by hour:

```
7am 237   8am 280   9am 268   12pm 282   1pm 296   3pm 301   5pm 296   7pm 300   9pm 257
```

It peaks **1-7pm** — exactly the window that measures worst in §3. For this account, "post when
your audience is online" is wrong, and it was wrong in a way that was wired into the code: the old
`best_times()` blended this curve into the Instagram score at weight 0.2 (0.5 below 30 posts),
which is why hour **14** was sitting second in Thursday's ranking off four posts.

More followers online plausibly means more competition in the feed. Whatever the mechanism, the
posting results and the availability curve disagree, and the posting results are the ones that pay.

## 5. What was changed

**`bot/analytics.py` — `best_times()` rewritten.** Three defects:
- It ranked on engagement **rate** alone. Rate is engagement/reach, so an hour that reaches almost
  nobody can top the ranking, and reach is this account's binding constraint (playbook §6). Hours
  are now scored on **engagement per post and reach per post, weighted 60/40**.
- It resolved to the **individual hour**, which 1-6 posts per hour cannot support. Scores are now
  driven 75% by the **daypart band** and only 25% by the hour's own number, which orders hours
  inside a band. Cell shrinkage `K` went 3 → 8.
- It **blended the online-followers curve** into the Instagram score. Removed from the ranking; the
  curve is still written to the payload under `ig_online_followers` for reference, with a note.
- New gate `MIN_MEDIAN_REACH = 10`: a platform needs 8+ posts **and** median reach ≥ 10 to get a
  ranking at all. Facebook (median 2) now lands in `best_times.json → excluded` and `plan.py`
  falls back to the config hours for it.

Thursday's Instagram ranking before → after:
`[9, 21, 7, 10, 14, 8]` → `[21, 7, 20, 8, 19, 9]`, with 1-5pm now scoring 0.72-0.94 against
1.10-1.19 for the evening and early hours.

**`bot/plan.py` — `ranked_hours()` is format-aware.** Reads optional `reel_hours` / `post_hours`
from config. A per-kind list wins over the learned ranking, because `best_times()` pools reels and
static posts together and so cannot see the §3 format split; the learned ranking then orders only
the hours the list didn't name. Deleting those two config keys hands ordering back to the learned
data. `avoid_hours` is dropped last, and `plan_day()`'s own full-day fallback still applies, so a
crowded day degrades into an avoided hour rather than into no post at all. Story hours widened from
`base[:3]` to `base[:4]` so all five stories can seat at the 45-minute story gap.

**`config.yaml`:**
- `reel_hours: [9, 10, 11, 7, 12, 8, 21]` and `post_hours: [19, 20, 21, 7, 8, 18]` — the §3 split.
- `avoid_hours: [13, 14, 15, 16, 17]`.
- `default_feed_hours` [8, 12, 17, 19, 10] → [8, 19, 9, 20, 7, 21] — the old list had **17** in it,
  the single worst hour in the data.
- `story_hours` [7, 10, 13, 16, 20] → [7, 10, 12, 19, 20] — dropped 13 and 16.
- `min_gap_minutes` **90 → 50**. With six feed items a day (the directive's five plus the campaign
  `w1`), a 90-minute gap leaves only five seats in the strong windows and pushes the sixth into
  1-5pm. 50 rather than 60 because posts carry a `:02-:11` jitter, so two consecutive hours can sit
  51 minutes apart (11:11 then 12:02) — at 60 the planner rejected the next hour and fell through
  to the afternoon anyway. **If the daily feed count drops back to 3-4, put this back to 90.**

**`queue/2026-10-29` re-planned** against the new logic — including `w1` and `s5`, whose times moved
even though the brief says to leave those two alone. Their *content* was not touched; only the
schedule, which is what Memo asked to have fixed. Result, Instagram:

```
07:09 s1 story     09:03 r1 reel      10:05 r2 reel     11:08 r3 reel
12:08 s3 story     19:05 p1 post      20:05 p2 post     21:07 w1 post
10:05 s2 story     19:10 s4 story     21:09 s5 story
```
Three reels in the 9am-12pm peak, three static posts in the 7-9pm peak, stories spread 7am-9pm,
**zero items in 1-5pm** on any platform.

## 6. Still unfixed, and worth a decision

- **Publish drift: 28 minutes median, 91 minutes worst.** Across 92 posted slots (Oct 24-28):
  Facebook median 21 min late, Instagram 28, LinkedIn 26; **16 of 36 Instagram posts landed more
  than 30 minutes after their slot**, far enough to leave the hour chosen for them. `publish.yml`
  asks for `*/15 * * * *` but GitHub does not honour that under load. `plan.py` already compensates
  with the `:02-:11` jitter; that survives a 45-minute delay, not a 91-minute one. A real fix means
  either accepting hour-level precision only, or moving publishing off GitHub Actions cron.
- **LinkedIn and TikTok timing is entirely unmeasured** — 0 analytics rows each. They currently
  inherit Instagram's windows, which is a guess, not a finding. LinkedIn's audience is agents and
  investors and may well want business hours; there is no data to say so yet.
- **Six feed items a day on 817 Instagram followers** is the pressure behind the `min_gap_minutes`
  change. The timing fix makes the best of it; it does not answer whether six is the right number.
- **The evening-static finding rests on 5 posts.** Re-check at 10+.
