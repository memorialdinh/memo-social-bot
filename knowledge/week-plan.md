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

## Week of Tuesday, November 10 – Sunday, November 15, 2026

Written by Mentor on Sunday Nov 9, 2026. Every `p`/`r` angle below was checked with
`python -m bot.seen` before it went in the file, and `--plan` was run clean after.

### ⚠ READ THIS FIRST — two nights produced no queue

`queue/2026-11-09/` and `queue/2026-11-10/` hold **only the pre-written campaign `w1`/`s5`**. No
editorial items exist for either day. The last queue-write commit is `e874fcf` (Nov 6 eve, wrote
Nov 8); the Nov 7 and Nov 8 evening runs committed "prepare content" and then nothing. So Mon Nov 9
publishes 2 items instead of 11, and Tue Nov 10 will too unless tonight's run catches it.

**Tonight's run (Sun Nov 9): check `queue/2026-11-10/` first. If it still has no `p`/`r` items,
write Tue Nov 10 before Wed Nov 11,** then write Nov 11 on Monday's run. The Nov 10 row below is
deliberately **all-evergreen, zero fetches** so it can be written late and fast. Do not touch
`queue/2026-11-09/` — that day is gone; let the campaign post stand alone and say so in the report.

**This plan runs Tue–Sun, not Mon–Sat, on purpose.** Scribe's 7:47pm PT run writes the queue for
**two days later** (playbook §6, three commits confirm it), so a Mon–Sat plan starves it on two
nights a week. Mon Nov 9 is already past.

**One fetch-dependent item a day, marked ⚠, and three days have none.** The Nov 8 note recorded the
wall coming down for two domains for the first time in seven runs — one good night, not a fix. Plan
as if one fetch gets through. If a ⚠ item can't be sourced, drop it and say so; never write the
claim from memory.

**Every `stat` row this week is already sourced in-repo.** `data/market/ca_cities.json` (generated
Nov 4, 2026) carries the C.A.R. September 2026 county table, Zillow ZHVI and ZORI through Sept 30
2026, and Realtor.com ZIP-level inventory for Sept 2026. Five of the six `stat` rows read straight
off that file and need **no fetch at all**. Carry "Sept 2026" on the graphic every time, and
describe the Zillow series as smoothed indexes of typical values — estimates, not appraisals.

**The weekly `cta` offer card is already written.** `queue/2026-11-11/w1.yaml` is a seller `cta`
card (free home value before 2027). That satisfies Memo's Oct 28 weekly-offer ask, so **no `cta`
template anywhere else this week** — which also satisfies the standing "stop using the `cta`
template" directive without dropping the offer. Leave `w1`/`s5` alone on Nov 9, 10 and 11; the
campaign ends Nov 11, so Nov 12–15 are all Scribe's, stories included.

**Where a day's five feed rows carry no `process`, the day's `process` goes on a story** — the plan
marks which one. Memo's "at least 1 process a day" ask is across all 10 pieces, not the feed alone.

### Tue Nov 10 — recovery day, no fetch needed
Campaign `w1`/`s5`: investment `tip` + investor `quiz` (the investment calculator). **Investors are
covered by `w1` today and `s5` is the day's questionnaire** — don't repeat the calculator in p1–p3.

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | seller_education | `process`: who to call first when you inherit a house, and in what order — the four calls and what each one is actually for. The inheritor/trustee audience, which got one piece all last week. "General information, not legal or tax advice"; point them at their own counsel and the county. No fetch. |
| p2 | post | humor | `meme`: every seller is certain the comps that count are the ones that sold high. The joke is on the process, not on anyone. |
| p3 | post | motivation | `quote` template. Waiting on purpose, with a date on it, is a plan — not a failure. Clarity register, no hustle talk. **First of the week's two quotes.** Carried from the Nov 5 row that got dropped. |
| r1 | reel | buyer_education | `explainer`: what an appraisal contingency actually does, and what waiving it gives up. Definitional — no figure, no fetch. Built to be saved. |
| r2 | reel | market_update | `stat`: two years of typical home values across his cities — Cerritos **+6.5%** at the top, Gardena **−0.3%** at the bottom, Sept 2024 to Sept 2026. Zillow ZHVI from `data/market/ca_cities.json`, **no fetch**. Period on the graphic. The point is that "the market" is the wrong unit. |

### Wed Nov 11
Campaign `w1`/`s5`: the seller `cta` offer card (free home value) + a `tip` story. **Don't repeat
the home-value topic in p1–p3**, and the `s5` `tip` is the day's education piece. Last campaign day.

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | agent_attraction | `spotlight` **#8: CliqueOffers** — what a consumer cash-offer request is and how it reaches the agent as a lead. **⚠ the day's one fetch, and it must be an official Epique page read the same day.** Source verified Nov 6: the joinepique.com press release. Three cautions: **do not use the executive quotes about "driving revenue" or "profitability"** (income-adjacent); **do not date the feature from the body's "This 2025 expansion"** line; frame it tightly on the cash-offer product, because Spotlight #5 already burned lead and marketing programs generally. No income language, "subject to plan terms". Log to `spotlight-log.csv`. If no Epique page loads, drop it and write nothing from memory. |
| p2 | post | buyer_education | `process`: the first 72 hours after an offer is accepted — escrow opens, the deposit, disclosures, inspections ordered. Four steps, no figure, no fetch. Built to be saved. |
| p3 | post | humor | `meme`: nobody reads the 48-page inspection report except the one page about the roof. |
| r1 | reel | seller_education | `quiz`: who orders and who pays for a termite report in a California sale — and the honest answer that most of it is negotiable and local. **The day's feed questionnaire.** |
| r2 | reel | investment | `stat`: rent and value moved the same **+2.4%** in Long Beach to Sept 2026, and apart in Lakewood (rent **+5.7%**, value **+2.6%**). Zillow ZORI and ZHVI from `data/market/ca_cities.json`, **no fetch**. Period on the graphic; both described as smoothed indexes, estimates not appraisals. Second investor piece of the week. |

### Thu Nov 12 — no rate piece today
PMMS prints Thursday at noon ET, but Thursday's queue is written **Tuesday** evening, so a Thursday
rate row is unwritable. **The rate piece is Sat Nov 14.** No campaign files from today on — all ten
items are Scribe's.

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | buyer_education | `explainer`: what a conforming loan limit is, and what makes a loan "jumbo". **Seasonality setup — FHFA announces next year's limits late November** (playbook §4), so this lands the vocabulary a week or two early. **State no limit figure**: none is announced for 2027 and the current one isn't the story. No fetch. |
| p2 | post | seller_education | `compare`: a rent-back after closing vs moving twice. Both columns carry their real cost; no "best" option named. Carried from the Nov 4 row that got dropped. |
| p3 | post | humor | `meme`: the buyer who has to see it in person, and then asks for more photos. |
| r1 | reel | market_update | `stat`: eleven Long Beach ZIP codes, median days on market from **42** to **73**, Sept 2026. Realtor.com monthly ZIP inventory in `data/market/ca_cities.json`, **no fetch**. Period on the graphic. Listings and pricing only — never who lives anywhere. |
| r2 | reel | buyer_education | `checklist`: gift funds for a down payment — what a lender needs to see before the money counts. 4 yes/no questions. **The day's feed questionnaire.** No fetch. |
| — | — | — | **The day's `process` rides `s4`**: what happens at the final walkthrough, and what is actually fixable at that point. |

### Fri Nov 13
**p1 is the second inheritor/trustee piece** — the audience that keeps getting one slot a week.

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | seller_education | `process`: what a successor trustee or executor can sign before the court signs off — the order of operations on a trust or probate sale. **⚠ the day's one fetch (California Courts self-help, or the county recorder).** If nothing official loads, write the sequence with **no statute cite and no timeline figure**, or drop it. "General information, not legal advice" — send them to their own counsel. CTA `SELLER`. |
| p2 | post | buyer_education | `checklist`: before you remove your contingency — the insurance quote, the final loan approval, the walkthrough. 4 yes/no questions. **The day's feed questionnaire**, and it carries the hazard-insurance point that most buyers leave until after. No figures, no fetch. |
| p3 | post | humor | `meme`: the agent calendar in November is just reschedule requests. |
| r1 | reel | market_update | `stat`: active listings a year apart across his cities — Cypress **+19.1%** and Gardena **+11.0%** up, Redondo Beach **−9.0%** down, Sept 2026. Realtor.com via `data/market/ca_cities.json`, **no fetch**. Period on the graphic. More supply usually means more room to negotiate; **never say where it goes next.** |
| r2 | reel | motivation | `quote` template. You cannot negotiate a number you have not written down. **Second and last quote of the week.** Clarity register. |
| — | — | — | **The day's education piece rides `s3`** as an `explainer`: what a lender credit is, in one line. |

### Sat Nov 14 — rate day
The **Thu Nov 12** PMMS print is live by the time Saturday's queue is written (Thursday evening).

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | market_update | `stat`: the Freddie Mac 30-year weekly average from the **Nov 12** print, and what the week-over-week move does to the monthly payment on **one labelled example loan**. **⚠ the day's one fetch.** **Operator note from the Nov 7 run: the press-release host `freddiemac.gcs-web.com` loaded when `www.freddiemac.com` did not — try the press release first.** Put the as-of date in the `stat_label`. State what happened; **never where it goes next.** The payment example states its assumptions and is "not a loan offer". **If the print has not advanced, do not rerun the Nov 5 number** — swap in the banked PMI topic (CFPB) instead. |
| p2 | post | buyer_education | `explainer`: what a lender credit is, and how it trades against your rate. Any dollar or rate figure is a labelled example, "not a loan offer". |
| p3 | post | humor | `meme`: everyone says "just send me something" and everyone means something different. |
| r1 | reel | seller_education | `quiz`: why two agents price the same home differently — and the one question to ask about the gap. **The day's feed questionnaire.** No figure. |
| r2 | reel | buyer_education | `process`: what happens at the final walkthrough, and what is actually fixable at that point. Built to be saved. (If `s4` on Nov 12 already carried this, swap in the banked escalation-clause topic — check `topic-log.csv` first.) |

### Sun Nov 15
| # | kind | track | angle |
|---|---|---|---|
| p1 | post | buyer_education | `process`: what a self-employed or 1099 borrower needs two years of, and the order a lender wants it in. No figure, no fetch. |
| p2 | post | community | `tip`: three things Memo will do for a past client any time, no transaction needed. **Sphere piece. This has been planned and dropped twice — do not drop it a third time.** Warm, no pitch. CTA `BDAY`, which also covers the week's Birthday Club invite. `track:community` has 2 posts and the tips list asks for more so it can be measured. |
| p3 | post | humor | `meme`: the buyer who sends a listing link at 11pm that sold in June. |
| r1 | reel | market_update | `stat`: the share of active listings that took a price cut, Sept 2026 — Cypress **52.0%** at the top, El Segundo **25.0%** at the bottom. Realtor.com via `data/market/ca_cities.json`, **no fetch**. Period on the graphic. **Do not use Long Beach's own cut share — that ran Oct 27.** |
| r2 | reel | seller_education | `quiz`: why a cash offer is not automatically a higher net — the three lines that decide it. **The day's feed questionnaire.** No figure. |
| — | — | — | **The day's education piece rides `s3`** as a `compare`: closed sales vs pending sales, and which one describes right now. |

---

## Banked and checked fresh — use these when a ⚠ item can't be sourced

Each was run through `bot.seen` on Nov 9, 2026 and came back fresh. The first five need no outside
source at all, which makes them the right substitutes on a walled run.

- What a preliminary title report tells you, and the three things worth reading on it. *(no source)*
- Why a listing's square footage and the tax record's square footage disagree. *(no source)*
- The one page of your closing disclosure worth reading twice. *(no source)*
- The three numbers a landlord should know before renewing a lease. *(no source — investor)*
- The difference between a seller's market and a buyer's market in months of supply. *(no source —
  the figures are already in `data/market/ca_cities.json`)*
- 1031 exchange: the 45-day and 180-day clocks, and what "like kind" means. *(needs IRS — dropped
  Nov 3 for want of a fetch, still unused and still fresh)*
- Private mortgage insurance — how it gets on the loan and when it comes off. *(needs CFPB; the Nov
  8 run read consumerfinance.gov successfully, so this is probably writable now)*
- The capital-gains exclusion when you sell your primary residence. *(needs IRS)*
- The supplemental property tax bill that arrives after you buy. *(needs county assessor)*
- Removing contingencies in California — the default window and what the day after means. *(needs
  C.A.R. or DRE; **do not state a day count without that source**)*

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
what a lender verifies, and everything in `queue/2026-11-02/` through `queue/2026-11-08/`.
Spotlight subjects burned: Power Academy, transaction and compliance support, Power Summit, the cap
and fees after cap, agent benefits and health insurance, the AI toolkit, lead and marketing
programs, stock awards and the Power Award, Power Coaching and Forever Mentorship, and the three
joinmemo calculators (brokerage, RevShare, team).
