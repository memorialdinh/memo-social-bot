# Playbook — the editorial brain

Maintained by **Mentor** (Sundays). Read by **Scribe** every night before writing. This is the
standing knowledge: what to say, how to say it, what not to say, and why. The week plan says *what*
goes out; this says *how it should land*.

---

## 1. What this content is for

Memo isn't selling posts, he's shortening the distance between a stranger and a consultation:
**a question → a straight answer → trust → a keyword DM → a call → a client.** Every piece moves
someone one step along that path. If a post doesn't educate, make someone feel capable, or make them
laugh enough to remember his face, it's filler.

**The keyword CTAs are the conversion point**, and they're what the engagement bot answers
automatically: `RATES`, `BUYER`, `SELLER`, `VALUE`, `PROP 19`, `AGREEMENT`, `MATH`, `INVEST`,
`BDAY`, `PLAN`. One per piece. Never two.

## 2. Voice — the four registers

Memo is direct, warm, a little punchy, and never performs expertise. Mix the registers; a feed that
is all one note stops working.
**Educational** (the floor, ~half the output). Plain answers to real questions, with the number.
The test: could a reader act on this today? "Here's what a lender actually verifies" beats
"understanding the mortgage process."

**Funny** (one feed slot a week plus stories — see §7 rule 3). The joke is about the *process*, never
about people; see the meme rules in CONTENT_BRIEF. Memo is usually the one being roasted. Humour buys
attention that education spends.

**Motivational** (one `quote` a week, on a story). Not hustle-porn, not "manifest your dream home."
The motivating thing in real estate is **clarity**: someone who thought buying was impossible
learning what it actually takes. "You don't need to be ready, you need to know your numbers" works.
"Grind until you make it" doesn't, and it isn't him.

**Empowering** (woven through). Give people the arithmetic so they can decide for themselves,
including when the answer is "don't buy yet." Someone who trusts him enough to wait a year is worth
more than someone pushed into a bad purchase. Never make a reader feel behind or stupid.

**Banned words**, always: dive in, navigate, unlock, elevate, seamless, game-changer, nestled,
boasts, "dream home" as filler. No ALL-CAPS shouting. No hype.

## 3. The audiences and what each one needs

| Audience | Where they are | What earns them |
|---|---|---|
| **First-time buyers** | Scared of the money, don't know the steps | The real number. Down payment reality, closing costs, what pre-approval checks, assistance programs |
| **Move-up sellers** | Have equity, worried about timing and the next purchase | Net sheets, pricing math, sell-first vs buy-first, what prep actually returns |
| **Investors** | Running numbers already | Cap rate vs cash-on-cash, price per sq ft used correctly, ADUs, 1031 basics, Mello-Roos |
| **Inheritors / trustees** | Overwhelmed, often grieving | Gentle, procedural, "not legal advice", timelines, who to call first |
| **Agents** (recruiting) | Weighing a move, tired of being sold to | Cost per deal, cap questions, what changes after cap. Never income promises |
| **Sphere / past clients** | Already trust him | Birthdays, anniversaries, local notes, the human stuff |

## 4. Seasonality — plan around these

- **Nov 1 / Dec 10** — CA property tax 1st installment due / delinquent. **Feb 1 / Apr 10** — 2nd.
  Reliable, useful, recurring. Always cite the county tax collector.
- **Late Nov** — FHFA announces next year's conforming loan limits.
- **Dec** — "should I wait until spring?" season. Fewer buyers, more serious ones. **Jan** —
  new-year listings, resolution energy, tax documents arriving. **Mar–Jun** — spring market, highest
  inventory and competition. **Sep–Oct** — back-to-school slowdown, then the pre-holiday push.
- **Weekly** — Freddie Mac PMMS releases Thursday mornings (holiday weeks move; never state the day).
  **Monthly** — C.A.R. sales and price report, roughly the third week, covering the prior month.

## 5. Compliance — the spine, not a disclaimer

These are not optional and they are not footnotes. A post that breaks one doesn't go out.

- **Fair Housing.** Describe homes and places, never who should live in them. No "perfect for
  families", "safe neighborhood", "exclusive community", nothing touching race, religion, national
  origin, sex, disability or familial status. Applies to jokes exactly as to listings.
- **No guarantees, no predictions as fact.** Not "prices will", not "rates will", not "you'll make".
- **No superiority claims.** No "best agent", "#1", "top producer".
- **Every number needs a dated source** in `sources:`. If it can't be verified, it doesn't appear.
  **The as-of date belongs on the graphic too, not only in the caption.** Stories carry no caption at
  all, so a bare figure on a story has no date anywhere. Write the period into the `stat_label`, the
  `subhead`, the `fact:` line or the story `headline` — "Oct 2026", "as of Nov 19" — every time. Found
  dateless Oct 25, 2026 (an inventory graphic and a list-price story); **four clean weeks since.**
  When a row pairs two sources with different vintages (Realtor.com October against ACS 2020–2024),
  **both periods go on the graphic.**
- **Identification** on every graphic and caption: Memo Dinh, DRE #02066757, Epique Realty, Equal
  Housing Opportunity. The renderer does this; never remove it.
- **Agent recruiting**: no income, earnings or revenue-share promises. Revenue share and equity are
  "subject to plan terms". Never disparage another brokerage.
- **Legal / tax / lending**: general information only, then "Not legal, tax or lending advice" and
  an invitation to talk. Never advise on a specific person's situation in a post.
  **That disclaimer lives in the caption footer, and stories have no caption** — and `fine_print`
  renders on `spotlight` only. So on any legal, tax or lending **story**, the disclaimer goes in the
  **`subhead`**. ⚠ **Corrected Nov 22, 2026 — it used to say `explain`, and `explain` does not
  render.** `render.py:1144` gates it behind `reveal = ans is not None and (c.video or (c.story and
  d.get("reveal")))`, so on a `quiz` story with `reveal: false` the line sits in the file, passes any
  sweep that greps the file, and **is not on the graphic.** That is how `queue/2026-11-17/s1` (rate
  vs APR) went out bare. `subhead` renders on every template. **Sweep the rendered field, not the
  file.** Two live instances found this way: Nov 6 `s1` (Prop 19, BOE cite, bare) and Nov 17 `s1`.
- **Never claim**: deal counts, "100+", sales volume, that Memo speaks Vietnamese, or his schools
  and degree.
- Values are "estimates, not an appraisal". Payment examples state their assumptions and are "not a
  loan offer".

## 6. What actually works, from Memo's own numbers

Updated by Mentor from `data/insights.json` and `data/posts.csv` each week. **As of Nov 22, 2026.**

- **Still reach-starved, so read almost every 0.0% in `insights.json` as a reach reading, not a
  content one.** Nov 16–22: 76 rows, **2,625 reach, 157 engagements, 1 save, 1 share** — up from
  2,288 and 59, essentially all of it Memo's.
- **His own camera content is out-earning the bot about ten to one — fourth week running.** On
  Instagram his **22 untagged rows took 148 of the 157 engagements** on 1,598 reach (**9.26%**); the
  bot's **34 tagged rows took 9** on 1,023 reach (**0.88%**). A gym post Nov 21 did 40 engagements on
  238 reach, a birthday post Nov 17 did 36 on 211. The fitness journey, showing days, escrow wins,
  family. **The bot cannot make this — it needs his camera.** Say it when a week looks flat.
- **⚠ NEW, the week's real finding: the 7–10pm post slot is the one the publisher misses.**
  `queue/2026-11-19/p1` — the C.A.R. October report, five runs of waiting, two carriers verified —
  was scheduled 19:02 PT and marked **`missed`, "more than 6:00:00 late"** on all four platforms; the
  publisher's last run that day was 11:17am and nothing ran again until 01:55am. **It also carried
  Thursday's 15-minute-call offer, so the weekly offer never went out.** Reels (9–11am, 3pm) have not
  been missed. `post_hours` is Memo's `config.yaml`, so **the plan adapts: load-bearing rows ride
  reels, `p1` takes what costs least if it slips.** Tell Memo — only he can change the hour.
- **⚠ NEW: Memo's Canva carousels are the best thing the bot publishes.** Both `c1` rows landed 36
  reach with **3 and 1 engagements** — the top two bot items of the week — and `template:carousel`
  reads **2.78% on 1.0 avg engagements (n=4)** against every rendered template near 0.0%. **Thin, not
  yet a finding**, but nothing else the bot ships earns anything, so **a `c1` takes the post slot
  without argument.** His own design beats the renderer, same as his footage.
- **The "static posts earn nothing" line did NOT reproduce.** Bot engagements per item Nov 16–22:
  **posts 1.00** (6 on 6), stories 0.14, **reels 0.07** — the inverse of Nov 9–15 (reels 2.61, posts
  0.00), both single-digit samples. **Format is unmeasured; don't re-weight the feed on either week.**
  Reel weighting now rests on publisher reliability, not engagement.
- **Facebook: 20 rows, 4 reach, 0 engagements**, and `best_times.json` ranks Instagram only. Keep
  posting, never optimise, never spend a caption pass on it. **Followers are not the signal** — IG
  817 → 820, FB 217 → 294 over 60 days on 4 reach for the week. Never cited as growth.
- **Both §5 defects are clean on the graphics that shipped** — fourth clean week on dated figures,
  and every legal/tax/lending story Nov 16–22 carried its qualifier in `subhead`. **But §5's own
  instruction was wrong until Nov 22** (the fix above) and had already cost one bare story. **Keep
  both sweeps every run, and sweep the rendered field, not the file.** Two standing false positives,
  so they stop being re-reported: the "REAL ESTATE 101" kicker trips a bare-number grep, and
  `posts.csv` truncates captions at 140 chars, so "no DRE footer" is an artifact
  (`common.py:120` appends it, `render.py:886` draws it).
- **The newswire workaround is a rule now.** When the issuer's host returns `PROVENANCE_REQUIRED`,
  the newswire carrying its own release does not: **C.A.R. → `prnewswire.com`** (or the Yahoo mirror),
  **Freddie Mac → `globenewswire.com`**. Read verbatim, never as a model summary, and confirm a key
  figure on a second carrier.
- **`ca_cities.json`, regenerated Nov 22, now carries the C.A.R. October 2026 county table** (LA,
  Orange, Riverside, San Bernardino medians, sales, UII, DOM) plus Realtor.com through Oct 2026 and
  ZHVI/ZORI through Oct 31. **Six no-fetch `stat` rows a week come out of it.** **Never build a row on
  the owner/renter split** — tenure edges toward who lives where, §5 wins. `redfin` is `null` for
  every service city, so **it holds no sale-to-list figure** — a ⚠ fetch, not a fallback, wrongly
  banked as one for two weeks.
- **Still no track, template or theme finding, and Mentor must not invent one.** 177 rows sit in
  `track:untagged` and the tagged tracks read near 0.0%. Until a track has 4+ posts *and* the account
  has reach worth measuring, "this track works" is not a finding — say the data is thin. The recurring
  "write an extra Untagged piece" directive is an artifact of that bucket.


## 7. Standing rules for Mentor

1. Never plan a topic without running `python -m bot.seen` — fallbacks included. His real history is
   ~200 posts back to May 2026 in `data/posts.csv`, which predates this bot. Run `--plan` clean before
   pushing. **Feed it a full topic sentence:** a bare headline under-matches, a long one over-matches
   on place names (the four-county phrasing flagged 53% on an unrelated Nov 7 quiz).
2. Balance the week across the audiences in section 3 — not five buyer posts in a row. Inheritors,
   investors and the sphere keep getting one slot; give them two or more.
3. **Ratified Nov 16, 2026; amended Nov 22.** At 3 feed items a day: **humor gets one feed slot a
   week, Saturday, and from Nov 28 it goes in a REEL slot, not `p1`** — it was dropped three
   Saturdays running out of `p1`, because `p1` is where Memo's Canva carousel lands and the brief's
   precedence list puts humor 5th. A carousel cannot take a reel slot. **`quote` is one a week and
   rides a story.** Both registers stay in the mix per §2 — they stop outbidding the educational
   floor. The three feed slots belong to Memo's Oct 28 ask (tips, education, process, questionnaire,
   CTA). Humor keeps a feed slot on its save rate; `quote` lost its because it earns reach and no
   engagements. Rewrite this when the data changes — it is Mentor's judgment, not Scribe's.
4. **The fresh-rate piece goes on SATURDAY** — PMMS normally prints Thursday and Scribe writes two
   days ahead, so Saturday's queue is written after it. **Never state the release day on a holiday
   week; use the as-of date the release carries.** If the print hasn't advanced, don't rerun the
   number — the brief only permits repeating a rate update that "carries a new weekly number." Swap
   in a banked topic. **`globenewswire.com` first** (§6), then `freddiemac.gcs-web.com`, then
   `www.freddiemac.com`.
5. When the data contradicts this playbook, the data wins — and update this file to say so.
6. **Memo's format ask (Oct 28, 2026): "more tips, education, process, questionnaire and CTA", in a
   more luxury design.** Every day: at least one `process`, one questionnaire (`checklist`/`quiz`),
   one education piece (`tip`/`explainer`/`compare`), a clear next step on everything, and the weekly
   15-minute-call offer as `cta_sub` on a client-facing feed piece — **Thursday, unless Thursday is a
   holiday, then name the day it moves to.** Name the template in the angle column. **`process` and
   the education piece may ride a story** — only the questionnaire must be in the feed — but mark
   which story or it gets dropped. **When a directive bans a template, meet the ask another way**
   (`quiz` for `checklist`, `cta_sub` for `cta`); never drop the requirement. Judge templates on
   saves and DMs, not likes.
7. **Agent attraction = a Spotlight series (Memo, Oct 28, 2026),** `template: spotlight`, one
   subject per post — a perk, tool, training, support line, cost line, event, or (only with written
   OK, a photo file and a consent date) an agent. **Two a week, Wednesday and Sunday, in a reel
   slot.** Rotate CONTENT_BRIEF's list, no repeat within 30 days (`spotlight-log.csv`), every fact
   from an official Epique source read the same day. **A Spotlight describing only Memo's own
   cadence needs no Epique fetch — keep one of those on the bench so the series never stalls.**
8. **One source-dependent item a day, maximum.** Give that slot to whatever has a hard same-day rule
   (the Spotlight, or the rate piece), mark it ⚠, and **name the no-fetch fallback in the row — and
   check the fallback with `bot.seen` too**, because a burned fallback is no fallback. Everything else
   must be writable with the wall up; `ca_cities.json` sources a `stat` with no fetch.
9. **Name the yielding row yourself, in the day heading.** The directive `stat` plus the five daily
   requirements don't fit five pieces on a Spotlight day. If Mentor doesn't choose, Scribe applies the
   brief's precedence list, which cuts humor (5th) and the Spotlight (4th) — that lost the Nov 15
   Spotlight and the Nov 14 meme. **Plan the `stat` in the table, say which requirement yields, and
   say the Wed/Sun Spotlight and Saturday's humor reel never do.** When a piece exists only because an
   audience needs it, say in the row that it must not be cut.
10. **Plan Tue–Sun, not Mon–Sat.** Scribe's 7:47pm PT run writes the queue for **two days later**,
   so a Mon–Sat plan starves it two nights a week and Monday is already written by Sunday's run.
11. **Put the week's most valuable row in a reel slot, never in `p1`.** The 7–10pm post slot is the
   one the publisher misses (§6), reels publish 9–11am and 3pm and have not been missed, and a `c1`
   carousel can take `p1` on any day with no notice. So the ⚠ fetch, the weekly 15-minute-call offer
   and the humor slot all ride reels; `p1` gets the row that costs least if it slips. **Say in each
   day heading what happens to that day's requirements if a `c1` lands.**
12. **Check that Scribe actually ran, every run.** Compare the newest `knowledge/market-notes/` file
   and the latest queue commit against today's date, and check `status:` in the last seven days'
   queue YAML for anything that is not `posted`. Nov 17–18 produced **no commit for 44 hours** and
   Nov 18's run caught up by writing two days at once; Nov 19's `p1` was marked `missed`. A missing
   night or a missed item belongs in the first line of the report.
