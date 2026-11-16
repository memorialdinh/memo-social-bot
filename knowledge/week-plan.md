# Week plan — topics only

**What this is.** The topic calendar for the coming week. Scribe writes the actual copy the night
before publication, with numbers verified that day, so figures are never stale. This file is the
plan; the `queue/` folders are the finished work.

**Memo can edit this file directly** (pencil icon on GitHub) to change, drop or add a topic. Scribe
follows it unless real news breaks, in which case it swaps a topic and notes the swap in its report.

**Rules Scribe applies when following this:**
- One `humor` meme most days.
- **No topic Memo has already posted.** Check `data/posts.csv` captions (his real history, ~200
  posts back to May 2026) for the last 120 days, not just `topic-log.csv`, which only covers this
  bot's own output. Every topic below was checked against that history on Oct 25, 2026.
- Thursday's market piece uses that morning's fresh Freddie Mac PMMS release.
- `laws_and_updates` always waits for Memo's approval — that is automatic, don't change it.
- Stories s1–s3 tease p1–p3. s4 teases a reel. s5 rotates: Birthday Club, a question, a local note.
- The `directives` in `data/insights.json` override the kind mix here (e.g. 3 reels instead of 2).

---

## ⚠ THE THREE RULE-BLOCK BULLETS ABOVE ARE SUPERSEDED — read these instead

The rules block is kept word for word because Memo edits this file and knows where things are.
Three of its bullets predate the Nov 12 volume cut and **Mentor has now ratified the replacement
cadence** (playbook §7 rule 3 was struck through pending this decision — it is decided):

| The old bullet says | What Scribe actually does now |
|---|---|
| "One `humor` meme most days." | **One humor feed slot a week, Saturday.** Plus a story when one is free — this week none is. |
| "Stories s1–s3 tease p1–p3. s4 teases a reel. s5 rotates…" | **Two stories: `s1` teases a feed item as a quiz or checklist; `s2` carries whatever the feed had no room for.** There is no s3–s5. |
| "directives override the kind mix (e.g. 3 reels instead of 2)" | **The 3-feed-item cap beats directive volume.** "3 reels and 2 posts" means *weight the 3 slots toward reels* — 1 post + 2 reels. Never 5. |

Also ratified: **`quote` is one a week and rides a story**, not the feed. It earns the highest
reach-per-item of any template on zero engagements (playbook §6), so a feed slot spent on it is a
slot that cannot produce a DM. This week it is **Fri Nov 20 `s2`**.

---

## Week of Tuesday, November 17 – Sunday, November 22, 2026

Written by Mentor on Sunday Nov 16, 2026 (the 4:36pm PT run). Every `p`/`r`/`s` angle below was
checked with `python -m bot.seen` before it went in the file, and `--plan` was run clean after.

**Why Tue–Sun again.** Scribe's 7:47pm PT run writes the queue for **two days later** — confirmed
again this week (`1fb526c`, Sat Nov 14 20:05 PT, wrote `queue/2026-11-16`). So tonight's run writes
**Tue Nov 17**, Monday's writes Wed Nov 18, and Friday's writes Sun Nov 22. `queue/2026-11-16/` is
already written and complete at 5 items — **do not touch it.**

**The day is 3 feed items + 2 stories: `p1`, `r1`, `r2`, `s1`, `s2`.** Nothing else. Reel-weighted
because static posts are the weakest format on this account — see the timing finding below.

### What the numbers said this week, and what it changed

- **Every one of the bot's 11 static posts last week landed between 7:02pm and 9:59pm and took
  0 engagements on 410 reach.** `config.yaml → post_hours: [19, 20, 21, …]` is deliberate, but its
  evidence was n=5 and marked "thin, treat as directional"; n=11 at zero now outweighs it.
  **This changes nothing in the plan and it is not a reason to move the hour** — reels in the
  9–11am window were the week's only bot reach — but it is why the single post slot goes to
  whatever is cheapest to lose, and the two reel slots carry the questionnaire and the Spotlight.
- **The directive-forced `stat` row is planned in the table every day** (playbook §7 rule 9), so
  Scribe never has to cut a protected piece to satisfy it. On the two Spotlight days it rides `s2`.
- **Five of the six `stat` rows need no fetch at all.** `data/market/ca_cities.json` (generated
  Nov 4, 2026) carries Realtor.com September 2026 ZIP inventory, Zillow ZHVI/ZORI through Sept 30
  2026, the C.A.R. September 2026 county table **and the ACS 2020–2024 tables, which this bot has
  never used**. Carry the period on the graphic every time; describe Zillow series as smoothed
  indexes of typical values, estimates not appraisals, and ACS figures as 5-year estimates.

### One fetch a day, marked ⚠ — and the one that matters most is Thursday

The fetch wall is up on most runs and fully up on some (Nov 15: zero successful fetches). Plan as
if one gets through, and **never write a claim from memory.**

- **Thu Nov 19 — C.A.R.'s October 2026 sales and price report.** Four runs have now recorded that
  it does not exist yet; it lands around the third week of the month, so this week is it. This is
  the week's most valuable fetch and the Thursday ⚠ slot is reserved for it. If it still isn't
  published, use the no-fetch fallback named in the row.
- **Sat Nov 21 — the PMMS print from Thu Nov 19.** Operator note from the Nov 14 run, and it is
  the useful one: **`globenewswire.com` carries Freddie Mac's own PMMS release and loaded first try
  when all three Freddie Mac hosts returned `PROVENANCE_REQUIRED`.** Try it first, then
  `freddiemac.gcs-web.com/news-releases`, then `www.freddiemac.com/pmms`. **If the print has not
  advanced past 7.11%, do not rerun it** — swap in the banked CFPB PMI topic.
- **Wed Nov 18 and Fri Nov 20** have the Spotlight and the Prop 19 quiz. Both have a hard same-day
  source rule; if nothing official loads, drop the row and say so.
- **2027 conforming loan limits: FHFA has still not announced them** (five runs in a row recording
  this). Lenders are pre-announcing their own. **A lender's limit is not the conforming limit — do
  not state a 2027 figure**, and if FHFA announces mid-week, that is real news and worth a swap.

### Where the day's requirements collide, Mentor names the row that yields

Memo's Oct 28 ask is at least one `process`, one questionnaire and one education piece a day, plus
the directive `stat`, plus the fixed Spotlight. That is five wants for five pieces, and on Spotlight
days it does not fit. **The yielding row is named in the day heading, so Scribe does not have to
pick** — this is what cost the Sunday Spotlight and the Saturday meme last week.

**The Wed/Sun Spotlight is never the row that yields.** Fixed days exist so the series stops being
dropped as the row no directive protects; it outranks the brief's precedence list on those two days.

---

### Tue Nov 17 — all four requirements fit. No fetch needed.

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | market_update | `stat`: the typical home in his cities was built **1957** (Lakewood) to **1974** (Cerritos) — Long Beach 1959, Gardena and Torrance 1964, Redondo Beach 1973. ACS 2020–2024 5-year estimates from `data/market/ca_cities.json`, **no fetch**. **First use of the ACS table.** Put "Census ACS 2020–2024" on the graphic. The point is inspection scope and insurance on a 60-year-old house, not that older is worse. Describe housing stock, **never who lives in any city.** |
| r1 | reel | buyer_education | `quiz`: the rate or the APR — which number tells you what the loan actually costs. **The day's feed questionnaire.** Definitional, no figure, no fetch. Any example rate is labelled an example and "not a loan offer". |
| r2 | reel | seller_education | `process`: what's in a California seller disclosure package and the order to work through it. 4 steps. **The day's `process`.** No statute cite and no day count unless something official loads — describe the sequence. "General information, not legal advice." |
| s1 | story | buyer_education | `quiz` teaser for `r1`: rate vs APR, answered by DM. **The story questionnaire.** |
| s2 | story | buyer_education | `explainer`: what an escrow impound account is, and why the payment changes after the first year. **The day's education piece.** No figure needed. |

### Wed Nov 18 — Spotlight day. **The `process` yields; everything else fits.**

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | community | `tip`: three things to do with your closing documents after you buy, and what to keep for taxes. **Sphere / past-client piece — `track:community` has 2 posts and the tips list asks for more so it can be measured. Do not drop it; the sphere tip has already been dropped twice.** Warm, no pitch, no tax advice. CTA `BDAY` — **this carries the week's Birthday Club invite.** (The brief puts that invite on a story; there is no free story slot this week, and the feed reaches further. Noted deliberately.) **The day's education piece.** |
| r1 | reel | agent_attraction | `spotlight` **#9: Power Wednesday** — what the weekly session is and what an agent gets out of showing up. **⚠ the day's one fetch, and it must be an official Epique page read the same day** (joinepique.com, epiquerealty.com, or the current ICA). Say which source you are quoting — joinepique.com's description of a program and the agreement's definition can differ. **No income language, no "you'll earn", "subject to plan terms", never run down another brokerage.** Speaks to all licensed agents, not "SoCal agents". Log to `spotlight-log.csv`. **If no Epique page loads, drop it and write nothing from memory.** |
| r2 | reel | buyer_education | `checklist`: the five things not to do between offer acceptance and closing day — new credit, job change, large deposits, cancelled insurance, moving money. **The day's feed questionnaire**, and built to be saved. No figure, no fetch. |
| s1 | story | buyer_education | `quiz` teaser for `r2`: which one of these actually kills a loan. **The story questionnaire.** |
| s2 | story | market_update | `stat`: how much of the inventory is already spoken for — pending as a share of active listings, **September 2026**: Cerritos **66.7%**, Gardena **59.7%**, Long Beach **37.0%**. Realtor.com via `data/market/ca_cities.json`, **no fetch**. Period on the graphic. More pending means less room; **never say where it goes next.** **This is the day's directive `stat`.** |

### Thu Nov 19 — the week's best fetch, and the 15-minute-call offer. **All four requirements fit.**

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | market_update | `stat`: **C.A.R.'s October 2026 Home Sales and Price Report** — statewide median and the sales pace, with the as-of month in the `stat_label`. **⚠ the day's one fetch and the week's priority.** Four runs have recorded that no October release exists yet; it is due now. **If it still isn't published, do not infer it** — fall back to the no-fetch angle: the spread of median listing prices across Long Beach's 11 ZIP codes, **$476,000 to $1,649,750, September 2026** (Realtor.com via `ca_cities.json`), whose point is that a citywide median describes no actual house. **This is the day's client-facing feed piece, so it carries the weekly offer: keep its own keyword CTA and add `cta_sub: tidycal.com/memorialdinh/15-minute-call`.** No `cta` template anywhere this week — the standing directive bans it and `cta_sub` is how the offer is met at this volume. |
| r1 | reel | investment | `quiz`: a rent roll and a T-12 — which one tells you what the building actually earned. **The day's feed questionnaire.** Second investor piece of the week. Definitional, no figure, no fetch. |
| r2 | reel | investment | `process`: what one empty month actually costs — the lost rent, the turn, the re-listing, the days before a new tenant pays. 4 steps. **The day's `process`.** Any dollar figure is a labelled example with its assumptions, **not a projection**; no fetch. |
| s1 | story | investment | `quiz` teaser for `r1`. **The story questionnaire.** |
| s2 | story | investment | `explainer`: gross rent multiplier, in one line, and the one thing it ignores. **The day's education piece.** Cap rate and cash-on-cash ran Oct 27 — **do not restate that comparison.** |

### Fri Nov 20 — inheritors and trustees. **Education yields; `s2` carries the week's `quote`.**

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | seller_education | `process`: why you need a date-of-death value when you inherit a house, and the order to get one. **The inheritor/trustee audience, which the playbook says to give two pieces — this is one of two.** **State no tax figure, no statute cite and no dollar threshold** unless something official loads; describe the sequence and send them to their own CPA and attorney. "General information, not legal or tax advice" — and because the `s1` teaser is a story with no caption, **write that disclaimer into the story's `explain` line too** (playbook §5). **The day's `process`.** No fetch. |
| r1 | reel | seller_education | `quiz`: Prop 19's parent-to-child transfer — the one-year rule on claiming it. **The day's feed questionnaire** and the second inheritor piece. **⚠ the day's one fetch: the California BOE or the county assessor, read the same day.** A Prop 19 quiz ran Nov 6 on a different question — this is the claim deadline, not the basics. **The Nov 6 piece went out with a BOE cite and no disclaimer anywhere; do not repeat that.** Disclaimer in the `explain` line, CTA `PROP 19`. If nothing official loads, drop the row. |
| r2 | reel | market_update | `stat`: what came on against what went under contract, **September 2026** — Long Beach **242 new / 217 pending**, Torrance **92 / 93**, Cypress **32 / 20**. Realtor.com via `ca_cities.json`, **no fetch**. Period on the graphic. **This is the day's directive `stat`.** State what happened; never where it goes next. |
| s1 | story | seller_education | `quiz` teaser for `r1`, with the "not legal or tax advice" line in `explain`. **The story questionnaire.** |
| s2 | story | motivation | `quote` template. **The week's one and only `quote`.** Clarity register, not hustle: waiting on purpose is a plan; waiting because nobody has told you the number is not. No hype, no "manifest", no "grind". |

### Sat Nov 21 — rate day and the week's one humor slot. **The `process` yields.**

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | humor | `meme`: every seller is sure the holidays mean nobody is looking. **The week's one humor feed slot** — it has the best save rate of any track and it has now been dropped two Saturdays running. **Do not drop it.** The joke is on the process, never on a person, and Fair Housing applies to it exactly as to a listing: nothing about who lives where or who can afford what. |
| r1 | reel | market_update | `stat`: the Freddie Mac 30-year weekly average from the **Nov 19** print, and what the week-over-week move does to the payment on **one labelled example loan**. **⚠ the day's one fetch — try `globenewswire.com` first** (it carries Freddie Mac's own release and loaded when all three Freddie Mac hosts failed on Nov 14), then `freddiemac.gcs-web.com/news-releases`, then `www.freddiemac.com/pmms`. As-of date in the `stat_label`. State what happened; **never where it goes next.** The payment example states its assumptions and is "not a loan offer". **If the print has not advanced past 7.11% (Nov 12), do not rerun it** — swap in the banked CFPB PMI topic. |
| r2 | reel | buyer_education | `checklist`: the closing disclosure — the four lines worth checking twice before you sign. **The day's feed questionnaire**, built to be saved. Any figure is a labelled example, not a quote. No fetch. |
| s1 | story | buyer_education | `quiz` teaser for `r2`. **The story questionnaire.** |
| s2 | story | buyer_education | `tip`: three things to check on your first mortgage statement after closing. **The day's education piece.** Up to 5 points allowed on a story; 3 is enough. No fetch. |

### Sun Nov 22 — Spotlight day. **The `process` yields; everything else fits.**

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | seller_education | `compare`: why a cash offer is not automatically a higher net — the three lines that decide it. **This was planned for Nov 15 and never written; it is fresh and it is wanted.** Both columns carry their real cost and **no "best" option is named.** **The day's education piece.** No fetch; any dollar figure is a labelled example. |
| r1 | reel | agent_attraction | `spotlight` **#10: what the first 30 days with Memo's team actually looks like** — the cadence a new agent gets from him, week by week. **Describe only Memo's own onboarding, not an Epique program**, which is what makes this row writable with the fetch wall up: no Epique facts means no Epique source needed. **If it names any Epique program, benefit or figure, that fact needs an official Epique page read the same day or it comes out.** No income language, no "you'll earn", "subject to plan terms" on anything plan-related, never run down another brokerage, speaks to all licensed agents. CTA `MATH`. Log to `spotlight-log.csv`. |
| r2 | reel | investment | `checklist`: Mello-Roos — four things to check on a community facilities district before you buy. **The day's feed questionnaire** and the third investor piece. **State no dollar amount and no rate** unless a county or district page loads; the questions are the content. "Not tax advice." No fetch. |
| s1 | story | investment | `quiz` teaser for `r2`: which of these shows up on the tax bill. **The story questionnaire.** |
| s2 | story | market_update | `stat`: **31%** of California households could afford the **$640,000** median-priced condo or townhome in **3Q 2026**, against **19%** for the **$894,630** median single-family home. **Already verified verbatim in `knowledge/market-notes/2026-11-16.md` from C.A.R.'s Oct 30, 2026 release — no fetch needed.** Period on the graphic. The point is that the entry point and the headline are different numbers. **This is the day's directive `stat`.** **Do not use the Los Angeles County or Orange County rows — those were never verified** (the Nov 16 fetch truncated); the LA Metro Area row is verbatim and ran Nov 16. |

---

## Banked and checked fresh — use these when a ⚠ item can't be sourced

Run through `bot.seen` on Nov 16, 2026 and fresh. The first four need no outside source at all,
which makes them the right substitutes on a walled run.

- What a seller should ask about the buyer's loan type before accepting the offer. *(no source)*
- Three things to check on your first mortgage statement after closing. *(no source — also Sat `s2`)*
- Why a listing's square footage and the tax record's square footage disagree. *(no source — **used Nov 16 `s2`, now burned**)*
- The share of homes selling above and below asking across his cities. *(no source — figures are in `ca_cities.json`)*
- California down payment assistance for first-time buyers. *(needs CalHFA — **playbook §3 names assistance programs as what earns first-time buyers and this bot has never run one.** Worth a ⚠ slot next week.)*
- Private mortgage insurance — how it gets on the loan and when it comes off. *(needs CFPB; consumerfinance.gov read in full on the Nov 8 run. **This is the Sat Nov 21 rate-row swap.**)*
- 1031 exchange: the 45-day and 180-day clocks, and what "like kind" means. *(needs IRS — banked since Nov 3, still unused, still fresh)*
- The capital-gains exclusion when you sell your primary residence. *(needs IRS)*
- The supplemental property tax bill that arrives after you buy. *(needs county assessor)*
- Removing contingencies in California — the default window and what the day after means. *(needs C.A.R. or DRE; **do not state a day count without that source**)*
- The C.A.R. 3Q 2026 affordability rows for **Los Angeles County and Orange County**. *(needs a third pass at `.../2026releases/3qtr2026HAI` at a higher offset — the Nov 16 fetch truncated before them)*

## Spotlight subjects — #9 and #10 this week, and what's left after

Series is at **#8** (CliqueOffers, Nov 11). This week uses **#9 Power Wednesday** (Wed Nov 18) and
**#10 the first 30 days with Memo's team** (Sun Nov 22).

**Burned, do not repeat within 30 days:** the AI toolkit, the brokerage comparison calculator, the
RevShare calculator, the team calculator, lead and marketing programs and the technology fee, stock
awards / Double Stock Award / Power Award / declining caps / 401(k), Power Coaching and Forever
Mentorship, CliqueOffers, Power Academy, transaction and compliance support, Power Summit, the cap
and fees after cap, agent benefits and health insurance.

**Left unused:** local meetups and culture, and **the Epique Asian Network** — which is a real
subject and fresh, but it is held back deliberately. It needs an official Epique page read the same
day, and it must describe a professional network for agents and nothing about anyone's national
origin; it must never imply what languages Memo speaks (the playbook bans claiming he speaks
Vietnamese). Don't write it on a walled run.

## Burned — already covered, do not plan

On top of the list in CONTENT_BRIEF: price per square foot, "is the price negotiable", "price vs
terms vs timing on an offer", "should I wait until spring", HOA dues, rate locks, how co-buyers hold
title, price bands and search filters, escrow week by week, the seller net sheet, earnest money,
discount points, the Homeowners' Exemption, special assessments, the sell-first myth, the five
numbers before a rental offer, 30-year vs 15-year, the Nov 1 property tax installment **and the
Dec 10 delinquency date** (both ran in the Oct 31 calendar note), what a seller sees when an offer
lands, the November calendar, owner's vs lender's title insurance, days on market and what resets
it, escalation clause vs a higher offer, the appraisal coming in under the purchase price, the
seller credit vs price reduction, contingent vs pending, months of supply by SoCal county, the
Long Beach two-year ZHVI move, the Long Beach price-cut share, the median price per square foot,
what a lender verifies, **cap rate vs cash-on-cash (Oct 27)**, and everything in
`queue/2026-11-02/` through `queue/2026-11-16/` — which now includes the rent-back comparison, gift
funds, the conforming-loan-limit explainer, successor-trustee authority, the contingency-removal
checklist, the lender credit, the Nov 12 PMMS print, why two agents price differently, backup
offers, the preliminary title report, listing-agreement terms, the self-employed document list,
the past-client tips, the C.A.R. 3Q affordability LA Metro row, lease-renewal pricing, the four
documents a seller should find, and the square-footage discrepancy.
