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

## Week of Monday, November 2 – Sunday, November 8, 2026

Written by Mentor on Sunday Nov 1, 2026. Every `p`/`r` angle below was checked with
`python -m bot.seen` before it went in the file, and `--plan` was run clean after.

**This plan runs Tue–Sun, not Mon–Sat, on purpose.** Three queue-write commits confirm Scribe's
7:47pm PT run writes the queue for **two days later**, not the next day (Oct 29 eve → Oct 31,
Oct 30 eve → Nov 1, Oct 31 eve → Nov 2). So a Mon–Sat plan leaves Scribe without a row on two
nights a week, which is the gap the Oct 31, Nov 1 and Nov 2 market notes all flagged. Mon Nov 2 is
already written and locked; the plan picks up at Tue Nov 3 and runs through Sun Nov 8.

**One fetch-dependent item a day, marked ⚠.** The last four Scribe runs got exactly one successful
web fetch each — the first of the run — and then hit `PROVENANCE_REQUIRED` on every later domain.
So each day below has **at most one** item that needs an outside source, and that item is the one
with a hard same-day rule. Everything else is evergreen and writable with the wall up. If the ⚠
item can't be sourced, drop it and say so; don't write the claim from memory.

**Mon Nov 2 — already written, do not rewrite.** `queue/2026-11-02/` holds Spotlight #6 (Epique
stock awards), a humor meme, and three reels on what a lender verifies, what a seller should know
about their own home, and what a comparable sale is. Scribe chose these itself when the plan ran
out. Leave the folder alone.

### Tue Nov 3
Campaign `w1`/`s5`: seller `quiz`, what sets your home's value — that quiz is the day's
questionnaire, so the five items below don't need another one. Don't repeat the value topic in p1–p3.

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | buyer_education | `explainer`: owner's title insurance vs lender's title insurance — who each policy actually protects. Definitional, no figure needed. Built to be saved. |
| p2 | post | motivation | `quote` template. You don't need a bigger budget, you need the real number in front of you. Clarity register, no hustle talk. |
| p3 | post | humor | `meme`: "we'll just paint it ourselves" — the promise, and the one wall that got done. The joke is on the process, not on anyone. |
| r1 | reel | investment | `explainer`: 1031 basics — the 45-day and 180-day clocks, and what "like kind" actually means. **⚠ the day's one fetch (IRS).** General information, not tax advice. The week's only investment piece — see the report. |
| r2 | reel | seller_education | `process`: days on market — what resets it, what doesn't, and why a cancel-and-relist still shows. No outside source needed. |

### Wed Nov 4
Campaign `w1`/`s5`: agent RevShare calculator, Spotlight #2 — **agents are covered by w1 today**, so
no agent piece in the p-slots. This is the week's `cta` offer-card day (p1).

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | seller_education | `cta`: the weekly offer card. What someone actually gets on a 15-minute call — a value range, what to fix and what to skip, a timeline. `cta: Book a 15-minute call`, `cta_sub: tidycal.com/memorialdinh/15-minute-call`. Caption still carries a keyword. |
| p2 | post | buyer_education | `process`: removing contingencies in California — the 17-day default and what day 18 actually means. **⚠ the day's one fetch (C.A.R. RPA / DRE).** "Not legal advice", point at their contract. |
| p3 | post | humor | `meme`: forty photos in the listing and one of them is the garage. |
| r1 | reel | community | `quiz`: the Birthday Club — what it is and why he runs it. CTA `BDAY`. This is the week's sphere invite the brief asks for. |
| r2 | reel | seller_education | `compare`: a rent-back after closing vs moving twice. Both columns carry their real cost; no "best" option named. |

### Thu Nov 5
Campaign `w1`/`s5`: seller `checklist`, should you sell in 2027 — that's the day's questionnaire.
**No rate piece today.** PMMS prints Thursday at noon ET, but Thursday's queue is written Tuesday
evening, so a Thursday rate row is unwritable. The rate piece is Sat Nov 7.

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | agent_attraction | `spotlight` #7: Power Coaching and Power Teams — the mentorship and team-support side. **⚠ the day's one fetch, and it must be an official Epique page read the same day.** If no Epique page loads, drop the piece and write nothing from memory. No income, earnings or revenue-share language; "subject to plan terms". Log to `spotlight-log.csv`. |
| p2 | post | seller_education | `explainer`: a buyer credit toward closing costs vs a straight price reduction — why the same money lands differently. Any dollar figure is a labelled example. |
| p3 | post | humor | `meme`: the seller who stays home during their own showings. Gentle, about the habit. |
| r1 | reel | motivation | `quote` template. Waiting on purpose, with a date on it, is a plan — not a failure. Second and last quote of the week. |
| r2 | reel | buyer_education | `quiz`: the buyer representation agreement — what you're signing and for how long. CTA `AGREEMENT` (first use of that keyword). Answer in the caption's last line. |

### Fri Nov 6
Campaign `w1`/`s5`: market_update `tip`, city-by-city market pages. **p1 is the inheritor/trustee
piece — the audience that got nothing at all last week.**

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | seller_education | `process`: Prop 19 parent-to-child — how the property-tax base is handled on a home inherited from a parent. **⚠ the day's one fetch (CA BOE or the county assessor).** The tax base only, not probate steps. CTA `PROP 19`. "General information, not legal or tax advice" — send them to the county assessor and their own counsel. |
| p2 | post | buyer_education | `tip`: three things that stall a loan in the last ten days before closing. From practice, no figures. |
| p3 | post | humor | `meme`: the offer deadline set for 3pm and the buyer who opens it at 2:58. |
| r1 | reel | seller_education | `quiz`: which one actually changes your net — a price cut, a buyer credit, or new photos. |
| r2 | reel | buyer_education | `explainer`: "contingent" vs "pending" on a listing, and what each one means for a buyer still watching it. |

### Sat Nov 7
Campaign `w1`/`s5`: seller `compare`, cash offer vs listing. **This is the week's rate day** — the
Thu Nov 5 PMMS print is live by the time Saturday's queue is written (Thursday evening).

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | market_update | `stat`: the Freddie Mac weekly average for the week ending Nov 5, and what the week-over-week move does to a real monthly payment on one labelled example loan. **⚠ the day's one fetch (freddiemac.com).** Put the as-of date on the graphic, in the `stat_label`. State what happened; never where it goes next. If the print hasn't advanced, don't rerun the Oct 29 number — swap in the banked PMI topic instead. |
| p2 | post | buyer_education | `tip`: who pays which closing costs in California — buyer, seller, or negotiated. Say plainly that most of it is negotiable and local. |
| p3 | post | humor | `meme`: the moving box labelled "misc". |
| r1 | reel | buyer_education | `process`: how a monthly payment is actually built — principal, interest, taxes, insurance, HOA. Any figure is a labelled example, "not a loan offer". |
| r2 | reel | local_spotlight | `quiz`: which SoCal city — built from the Sept 2026 figures already in `data/market/ca_cities.json`, so **no fetch needed**. Listings and pricing only, never who lives anywhere. Carry the Sept 2026 period on the graphic. |

### Sun Nov 8
Campaign `w1`/`s5`: buyer `process`, saved searches and matching alerts. Don't repeat that in p1–p3.

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | buyer_education | `compare`: the appraisal comes in under the purchase price — the options, side by side. **⚠ the day's one fetch (CFPB).** If CFPB states no break-even or likelihood, state none either. |
| p2 | post | community | `tip`: the three things Memo will do for a past client any time, no transaction needed. Sphere piece, warm, no pitch. |
| p3 | post | humor | `meme`: the lockbox code that doesn't work on a Saturday morning. |
| r1 | reel | seller_education | `process`: from "I'm thinking about selling" to live on the MLS — the five steps and roughly how long each takes. Built to be saved. |
| r2 | reel | market_update | `explainer`: what "seasonally adjusted annual rate" means when you read a sales headline. Definition only — no figure, so no fetch. |

---

## Banked and checked fresh — use these when a ⚠ item can't be sourced

Each was run through `bot.seen` on Nov 1, 2026 and came back fresh. The first four need no outside
source at all, which makes them the right substitutes on a walled run.

- Escalation clauses, and why some sellers won't accept one. *(no source needed)*
- The monthly line items an agent should ask any brokerage to list out. *(no source — but agent
  pieces must be `spotlight`, so only use it if an Epique page loads)*
- "Everyone says 'just send me something' and everyone means something different." *(humor)*
- The buyer who sends a listing link at 11pm that sold in June. *(humor)*
- Private mortgage insurance — how it gets on the loan and when it comes off. *(needs CFPB)*
- The capital-gains exclusion when you sell your primary residence. *(needs IRS)*
- The supplemental property tax bill that arrives after you buy. *(needs county assessor)*

## Burned — already covered, do not plan

On top of the list in CONTENT_BRIEF: price per square foot, "is the price negotiable", "price vs
terms vs timing on an offer", "should I wait until spring", HOA dues, rate locks, how co-buyers hold
title, price bands and search filters, escrow week by week, the seller net sheet, earnest money,
discount points, the Homeowners' Exemption, special assessments, the sell-first myth, the five
numbers before a rental offer, 30-year vs 15-year, the Nov 1 property tax installment, what a seller
sees when an offer lands, the November calendar, and everything in `queue/2026-11-02/`.
Spotlight subjects burned: Power Academy, transaction and compliance support, Power Summit, the cap
and fees after cap, agent benefits and health insurance.
