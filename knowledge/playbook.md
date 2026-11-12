# Playbook — the editorial brain

Maintained by **Mentor** (Sundays). Read by **Scribe** every night before writing. This is the
standing knowledge: what to say, how to say it, what not to say, and why. The week plan says *what*
goes out; this says *how it should land*.

---

## 1. What this content is for

Memo isn't selling posts, he's shortening the distance between a stranger and a consultation. The
path is always the same:

**someone has a question → he answers it straight → they trust the answer → they DM a keyword → a
call → a client.**

Every piece should move someone one step along that path. If a post doesn't educate, make someone
feel capable, or make them laugh enough to remember his face, it's filler.

**The keyword CTAs are the conversion point**, and they're what the engagement bot answers
automatically: `RATES`, `BUYER`, `SELLER`, `VALUE`, `PROP 19`, `AGREEMENT`, `MATH`, `INVEST`,
`BDAY`, `PLAN`. One per piece. Never two.

## 2. Voice — the four registers

Memo is direct, warm, a little punchy, and never performs expertise. Mix the registers; a feed that
is all one note stops working.

**Educational** (the floor, ~half the output). Plain answers to real questions, with the number.
The test: could a reader act on this today? "Here's what a lender actually verifies" beats
"understanding the mortgage process."

**Funny** (~1 a day). The joke is about the *process*, never about people — see the meme rules in
CONTENT_BRIEF. Memo is usually the one being roasted. Humour buys attention that education spends.

**Motivational** (~2 a week, `quote` template). Not hustle-porn, not "manifest your dream home."
The motivating thing in real estate is **clarity**: someone who thought buying was impossible
learning what it actually takes. "You don't need to be ready, you need to know your numbers" works.
"Grind until you make it" doesn't, and it isn't him.

**Empowering** (woven through). Give people the actual arithmetic so they can decide for themselves,
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
- **Dec** — "should I wait until spring?" season. Fewer buyers, more serious ones.
- **Jan** — new-year listings, resolution energy, tax documents arriving.
- **Mar–Jun** — spring market, highest inventory and competition.
- **Sep–Oct** — back-to-school slowdown, then the pre-holiday push.
- **Weekly** — Freddie Mac PMMS releases Thursday mornings. **Monthly** — C.A.R. sales and price
  report, roughly the third week, covering the prior month.

## 5. Compliance — the spine, not a disclaimer

These are not optional and they are not footnotes. A post that breaks one doesn't go out.

- **Fair Housing.** Describe homes and places, never who should live in them. No "perfect for
  families", "safe neighborhood", "exclusive community", nothing touching race, religion, national
  origin, sex, disability or familial status. This applies to jokes exactly as it applies to
  listings.
- **No guarantees, no predictions as fact.** Not "prices will", not "rates will", not "you'll make".
- **No superiority claims.** No "best agent", "#1", "top producer".
- **Every number needs a dated source** in `sources:`. If it can't be verified, it doesn't appear.
  **The as-of date belongs on the graphic too, not only in the caption.** Stories carry no caption at
  all, so a bare figure on a story has no date anywhere. Checked Oct 25, 2026 and found two: the p2
  graphic ("active listings rose just 0.5% in a year... Supply is 3.7 months") and the s4 story
  ("CA homes closed at 98.8% of list price") both ran dateless. Write the period into the
  `stat_label`, the `fact:` line or the story `headline` — "Sept 2026", "as of Oct 22" — every time.
- **Identification** on every graphic and caption: Memo Dinh, DRE #02066757, Epique Realty, Equal
  Housing Opportunity. The renderer does this; never remove it.
- **Agent recruiting**: no income, earnings or revenue-share promises. Revenue share and equity are
  "subject to plan terms". Never disparage another brokerage.
- **Legal / tax / lending**: general information only, then "Not legal, tax or lending advice" and
  an invitation to talk. Never advise on a specific person's situation in a post.
  **That disclaimer lives in the caption footer, and stories have no caption** — and `fine_print`
  renders on `spotlight` only. So on any legal, tax or lending **story**, write the disclaimer into
  the `explain` line. Found Nov 9, 2026: the Nov 6 `s1` Prop 19 quiz answered a property-tax
  question with a BOE cite and no disclaimer anywhere.
- **Never claim**: deal counts, "100+", sales volume, that Memo speaks Vietnamese, or his schools
  and degree.
- Values are "estimates, not an appraisal". Payment examples state their assumptions and are "not a
  loan offer".

## 6. What actually works, from Memo's own numbers

Updated by Mentor from `data/insights.json` and `data/posts.csv` each week. **As of Nov 9, 2026.**

- **The account is still reach-starved, and that is the finding that explains every other one.**
  Nov 2–8: 108 published rows, **2,194 total reach, 34 engagements, 1 save, 0 shares** across both
  platforms for the entire week — effectively flat on the 2,101/39/1/0 recorded a week earlier.
  Treat almost every per-template and per-track 0.0% in `insights.json` as a reach reading, not a
  content reading.
- **Memo's own camera content is not competing with the bot — it is in a different league.**
  Nov 2–8: his **23 untagged rows took 26 of the week's 34 engagements** on 364 reach; the bot's
  **85 tagged rows took 8** on 1,830 reach. One gym reel he shot on Nov 4 did **18 engagements on
  139 reach (13.0%)** — more than half the week's total engagement from a single piece. Second
  week running that this holds. The fitness journey, showing days, escrow wins, family. **The bot
  cannot make this — it needs his camera.** Educational content is the reliable floor; his footage
  is the ceiling. Say so when a week looks flat.
- **Reels beat posts, confirmed a third time, and now stories beat posts too.** Nov 2–8
  engagements per item: reels **1.35**, stories **0.15**, posts **0.04**. The 3-reels-2-posts
  directive has evidence behind it; apply it.
- **Facebook is finished as a reach channel, and got worse.** Nov 2–8: **36 rows, 5 total reach,
  0 engagements**, down from 27 rows/8 reach. `best_times.json` ranks Instagram only. Keep posting,
  never optimise, never spend a second caption pass on it.
- **Follower counts are not the signal.** Instagram 817 → 816; Facebook sat at **288 all week** —
  the +71 jump recorded Nov 1 has stopped and never came with reach. A fact, not growth, and
  **not to be cited as growth** anywhere.
- **`quote` stays restored; the directive that banned it was reading noise.** Nov 2–8: 3 `quote`
  rows, 84 reach, **the highest reach-per-item of any template (28.0)** on zero engagements — same
  shape as last week. A 0.0% engagement rate cannot distinguish templates on this account. Two
  `quote` pieces a week.
- **`cta` is the one template with real evidence against it — and the fix costs nothing.**
  Nov 2–8: 2 `cta` rows, **35 reach, 0 engagements, the lowest reach-per-item of any template
  (17.5)**. *Changed Nov 9:* the standing "stop using the `cta` template" directive is now
  supported, **and it does not require dropping Memo's weekly offer card** — a pre-written campaign
  `w1` can be the `cta` card (Nov 11 is one), or the offer rides a `tip` with
  `cta_sub: tidycal.com/memorialdinh/15-minute-call`. Never drop the offer itself to satisfy the
  template directive — same principle as the `checklist`/`quiz` swap below.
- **⚠ NEW FAILURE MODE: the writer stopped producing, two nights running.** The last queue-write
  commit is `e874fcf` (Nov 6 eve → Nov 8). The Nov 7 and Nov 8 evening runs committed
  `bot: prepare content` and then **no `bot: queue <date>` commit and no market note**. So
  `queue/2026-11-09/` and `queue/2026-11-10/` hold only the pre-written campaign `w1`/`s5` —
  **2 items published Nov 9 instead of 11.** This is distinct from the fetch wall and is the single
  biggest thing costing output right now. **Check for it every run**: compare the latest
  `bot: queue` commit against today's date, and if a day is bare, say so in the first line of the
  report.
- **The fetch wall may be lifting.** Six runs got exactly one fetch each (the first), then
  `PROVENANCE_REQUIRED`; the **Nov 8 run read `consumerfinance.gov` and `joinepique.com` in full**
  — first clean run in seven. A fact, not a fix: keep planning one source-dependent item a day.
  **The press-release host `freddiemac.gcs-web.com` loads when `www.freddiemac.com` does not.**
  Pre-approving the brief's named source domains would still end this.
- **The dateless-figure defect has not recurred — second clean week.** All 11 graphics published
  Nov 2–8 that carried a market figure carried its period. (The only flag was a `$10k` example on
  the Nov 5 `s2` quiz, which is an illustration, not a dated statistic.) Keep the sweep every run.
- **⚠ NEW DEFECT, now written into §5: a legal/tax/lending story has nowhere to put the advice
  disclaimer.** The footer is appended to captions only and `fine_print` renders on `spotlight`
  only, so the Nov 6 `s1` Prop 19 quiz went out with a BOE cite and no disclaimer. Same shape as
  the dateless-figure defect; same fix (the `explain` line) until the renderer draws `fine_print`
  for every template. Nothing is still live — stories expire in 24h. Sweep stories every run.
- **When a directive forces an extra row, the cut piece is always the one no directive protects.**
  Nov 2–8 lost the second `quote` (Nov 5 r1), the `community` sphere tip (Nov 8 p2, dropped twice
  now) and the only `investment` reel (Nov 3 r1, to the fetch wall). *Fix in §7 rule 9.*
- **There is still no track, template or theme finding, and Mentor must not invent one.** 120
  historical rows sit in `track:untagged` with an empty `track` column; the tagged tracks all read
  at or near 0.0% on 1–43 posts. Until a track has 4+ posts *and* the account has reach worth
  measuring, "this track works" is not a finding. Say the data is thin instead. The recurring
  "write an extra Untagged piece" directive is an artifact of this bucket, not an instruction that
  can be followed — it needs the analytics job to exclude `track:untagged`.

## 7. Standing rules for Mentor

1. Never plan a topic without running `python -m bot.seen`. His real history is ~200 posts back to
   May 2026 in `data/posts.csv`, which predates this bot. Run `--plan` clean before pushing.
2. Balance the week across audiences in section 3 — not five buyer posts in a row. Inheritors and
   investors each got one piece in the Nov 2–8 week; give them two.
3. ~~Keep one meme most days and exactly two motivational `quote` pieces a week.~~
   **Superseded Nov 12 2026 by the volume cut — Scribe's note, Mentor to ratify Sunday.** At 3
   feed items a day this rule cannot coexist with the daily questionnaire, the process/education
   piece and the directive `stat`. CONTENT_BRIEF.md now says: **humor gets one feed slot a week
   (Saturday) plus stories as available; `quote` is one a week and rides a story.** `quote` was
   demoted first because §6 records it earning the highest reach-per-item of any template on zero
   engagements — reach without conversion is the cheapest thing to move off the feed. Humor kept a
   feed slot on its save rate. Rewrite or overrule this rule when you replan the week; it is
   editorial judgment and it is yours, not Scribe's.
4. **The fresh-rate piece goes on SATURDAY.** PMMS publishes Thursdays at noon ET and Scribe writes
   **two days** ahead (§6), so Saturday's queue is written Thursday evening, after the print.
   Thursday's and Friday's are written before it. If the print hasn't advanced, don't rerun last
   week's number — the brief only permits repeating a rate update that "carries a new weekly
   number." Swap in a banked topic. Point Scribe at `freddiemac.gcs-web.com` first.
5. When the data contradicts this playbook, the data wins — and update this file to say so.
6. **Memo's format ask (Oct 28, 2026): "more tips, education, process, questionnaire and CTA",
   in a more luxury design.** Plan every day with at least one `process` piece, one questionnaire
   (`checklist` or `quiz`), one education piece (`tip`, `explainer` or `compare`), and a clear
   next step on everything. One offer of the 15-minute call a week. Name the template in the angle
   column when it matters. CONTENT_BRIEF.md has the fields for each. Judge the new templates on
   saves and DMs, not likes, once 4+ of each exist. **The daily `process` and education piece may
   ride a story** — the brief requires only the questionnaire in the feed — but mark which story,
   or it gets dropped. **When a directive bans a template, meet the underlying ask another way**
   (`quiz` for a banned `checklist`; a campaign `cta` card or a `tip` with the tidycal `cta_sub`
   for a banned `cta`). Never drop the requirement itself.
7. **Agent attraction = a Spotlight series (Memo, Oct 28, 2026).** Every `agent_attraction` piece
   uses `template: spotlight` and spotlights ONE thing: a perk, a tool, a training, a support line,
   a cost line, an event, or (only with their written OK) an agent. Rotate through the list in
   CONTENT_BRIEF.md and don't repeat a subject within 30 days (`knowledge/spotlight-log.csv`).
8. **Plan one source-dependent item a day, maximum**, and give that slot to whatever has a hard
   same-day rule — the Spotlight, or the rate piece. Mark it ⚠ in the plan. Everything else should
   be writable with the fetch wall up. `data/market/ca_cities.json` (C.A.R. Sept 2026 counties,
   Zillow ZHVI and ZORI, Realtor.com ZIP inventory) sources a `stat` row with no fetch at all —
   use it for the daily `stat` the directives ask for.
9. **Name the yielding row yourself (new Nov 9, 2026).** The directives reliably force an extra
   `market_update`/`stat` row, and Scribe then cuts whichever planned piece no directive protects —
   which has now cost the sphere tip twice, the second weekly `quote` once and the only
   `investment` reel once. So plan the directive-satisfying `stat` row **in the table**, and when a
   piece exists only because an audience needs it, say in the row that it must not be dropped.
10. **Check that Scribe actually ran.** Compare the latest `bot: queue <date>` commit and the
   newest `knowledge/market-notes/` file against today's date. A missing night means a near-empty
   publishing day, and it belongs in the first line of the report.
