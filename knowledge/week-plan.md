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
| "One `humor` meme most days." | **One humor feed slot a week, Saturday — in a REEL slot from Nov 28, not `p1`.** Plus a story when one is free; this week none is. |
| "Stories s1–s3 tease p1–p3. s4 teases a reel. s5 rotates…" | **Two stories: `s1` teases a feed item as a quiz or checklist; `s2` carries whatever the feed had no room for.** There is no s3–s5. |
| "directives override the kind mix (e.g. 3 reels instead of 2)" | **The 3-feed-item cap beats directive volume.** "3 reels and 2 posts" means *weight the 3 slots toward reels* — 1 post + 2 reels. Never 5. |

Also ratified: **`quote` is one a week and rides a story**, not the feed. It earns the highest
reach-per-item of any template on zero engagements (playbook §6), so a feed slot spent on it is a
slot that cannot produce a DM. This week it is **Thu Nov 26 `s2`**.

---

## Week of Tuesday, November 24 – Sunday, November 29, 2026

Written by Mentor on Sunday Nov 22, 2026 (the 4:36pm PT run). Every `p`/`r`/`s` angle below was
checked with `python -m bot.seen` before it went in the file, and `--plan` was run clean after.

**Why Tue–Sun.** Scribe's 7:47pm PT run writes the queue for **two days later**, so tonight's run
writes **Tue Nov 24** and Friday's writes Sun Nov 29. `queue/2026-11-23/` is already written and
complete at 5 items — **do not touch it.**

**Updated Nov 25 2026 (Memo): the day is 5 feed items + 2 stories: `p1`, `p2` (time "07:05"), `r1`, `r2`, `r3` (time "12:05"), `s1`, `s2`.** Nothing else. (Was 3 feed items before Nov 25; read any "3 feed" below as 5.) If a `c1`
Canva carousel exists for a day, **it is that day's post slot: write no `p1`** and the day stays at
3 feed items. Memo added a `c1` on Nov 20, Nov 21 and Nov 23, so expect more this week.

### What the numbers said this week, and what it changed

- **⚠ The week's most valuable post never published.** `queue/2026-11-19/p1` — the C.A.R. October
  2026 report, the number five runs of planning had waited for, verified against two carriers — was
  scheduled **19:02 PT** and marked **`missed`, "more than 6:00:00 late"**, on Instagram, Facebook,
  LinkedIn and TikTok at 01:55 PT Nov 20. The publisher's last run that day was **11:17am PT**;
  nothing ran again until 1:55am. **It also carried Thursday's 15-minute-call offer as `cta_sub`, so
  the weekly offer never went out either.** This is not a content finding and not a reason to argue
  about `post_hours` on engagement grounds — it is that **the 7:00–9:59pm post slot is the slot the
  publisher misses.** Config is Memo's, not Mentor's. What the plan does about it: **the day's most
  valuable row and anything load-bearing go in a reel slot** (reels publish 9–11am and 3pm and have
  not been missed), and `p1` gets the row that costs least if it slips. That is why the weekly offer
  rides **Fri `r2`** this week and not a 7pm post.
- **Memo's own camera content is out-earning the bot roughly ten to one — fourth week running.**
  Nov 16–22 on Instagram: his **22 untagged rows took 148 of the week's 157 engagements** on 1,598
  reach (**9.26%**); the bot's **34 tagged rows took 9** on 1,023 reach (**0.88%**). The gym post
  Nov 21 did 40 engagements on 238 reach; a birthday post Nov 17 did 36 on 211. **The bot cannot
  make this.** Education is the floor; his footage is the ceiling.
- **Memo's Canva carousels are the best thing the bot publishes.** Both `c1` rows landed 36 reach on
  Instagram with **3 and 1 engagements** — the top two bot items of the week, and `insights.json`
  has `template:carousel` at **2.78% on 1.0 avg engagements (n=4)**, against every rendered template
  at or near 0.0%. **n=4 is thin and this is not yet a finding** — but nothing else the bot ships is
  earning anything, so when a `c1` exists it gets the post slot without argument.
- **Last week's "static posts earn nothing" line did not reproduce, and the two weeks contradict
  each other.** Nov 16–22 engagements per bot item: **posts 1.00** (6 eng on 6 items), stories 0.14,
  **reels 0.07** — the exact inverse of Nov 9–15 (reels 2.61, posts 0.00). Both samples are single
  digits. **Treat format as unmeasured and do not re-weight the feed on either week.** The reel
  weighting stands on the publisher-reliability finding above, not on engagement.
- **The directive-forced `stat` row is planned in the table every day** (playbook §7 rule 9), and
  **all six are no-fetch this week.** `data/market/ca_cities.json` was regenerated **Nov 22** and now
  carries Realtor.com through **October 2026**, Zillow ZHVI/ZORI through **Oct 31 2026**, the ACS
  2020–2024 tables, and — new — **the C.A.R. October 2026 county table** (LA, Orange, Riverside, San
  Bernardino medians, sales, UII and DOM). Carry the period on the graphic every time; describe
  Zillow series as smoothed indexes of typical values, ACS as 5-year estimates, both "estimates, not
  an appraisal". **Never build a row on the owner/renter split** — tenure edges toward who lives
  where, and §5 wins.
- **The banked "share of homes selling above and below asking" is NOT no-fetch.** The Nov 23 note
  flagged this and it is correct: `ca_cities.json` has no sale-to-list field and `redfin` is `null`
  for every service city. It is struck from the banked list below.

### One fetch a day, marked ⚠ — and two of them are optional this week

- **Wed Nov 25 — Spotlight #10, Power Wednesday.** Needs an official Epique page read the same day.
  **Planned for Nov 18 and dropped when nothing loaded; it never published, so it is still fresh.**
- **Fri Nov 27 — the supplemental property tax bill.** LA County Assessor or Treasurer-Tax Collector,
  read the same day. No-fetch fallback named in the row.
- **Sat Nov 28 — the newest Freddie Mac PMMS print.** `globenewswire.com` first (it carries Freddie
  Mac's own release and has loaded on three runs when `freddiemac.com` returned `PROVENANCE_REQUIRED`),
  then `freddiemac.gcs-web.com/news-releases`, then `www.freddiemac.com/pmms`. **This is Thanksgiving
  week: do not assume or state a release day.** Use whatever as-of date the newest release itself
  carries and put it in the `stat_label`. **If the print has not advanced past 7.28% (Nov 19), do not
  rerun it** — swap in a banked topic.
- **Tue, Thu and Sun need no fetch at all.** Tue's ⚠ CalHFA row has a no-fetch fallback; Thu and Sun
  are writable with the wall fully up.
- **⚠⚠ FHFA 2027 conforming loan limits: ten consecutive runs have recorded that they are not
  announced.** Late November is the usual window (playbook §4) and **this is the week it is most
  likely to land.** If FHFA announces, **that is real news and it takes the `p1` `stat` slot on the
  day it breaks** — the announcement itself becomes that day's one ⚠ item, the planned no-fetch stat
  moves to the banked list, and the day's other rows are unchanged. Cite FHFA's own release only.
  **A lender's pre-announced limit is not the conforming limit; do not state a 2027 figure without
  FHFA.** The conforming-limit *explainer* is already burned — the news is the number, not the concept.

### Where the day's requirements collide, Mentor names the row that yields

**The Wed/Sun Spotlight is never the row that yields**, and **neither is Saturday's humor reel** —
that is new this week and it is the point of moving humor off `p1`. See the Saturday row.

---

### Tue Nov 24 — first-time buyers and move-up sellers. All four requirements fit.

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | market_update | `stat`: same month, opposite directions — **Orange County's median was up 7.8% from a year earlier while Riverside County's was down 3.9%**, October 2026 (Orange $1,500,000 vs $1,391,000; Riverside $610,000 vs $634,990). C.A.R. October 2026 county table via `ca_cities.json`, **no fetch**. "C.A.R., Oct 2026" on the graphic. The point is that "the market" is not one number across four counties. **State what happened; never where it goes next.** **The day's directive `stat`.** |
| r1 | reel | buyer_education | `process` ⚠: how California down payment assistance actually works, and the order you'd use it. **The day's one fetch: a CalHFA page (calhfa.ca.gov) read the same day.** **Playbook §3 names assistance programs as what earns first-time buyers and this bot has never run one** — this is the week's most wanted new topic, which is why it sits in a reel slot and not at 7pm. **State no dollar amount, no income limit, no price cap and no program name's terms unless the page loads**; describe the sequence and send people to a lender. "General information, not lending advice" in **`subhead`**. **The day's `process`.** *No-fetch fallback:* `process` on who pays the property taxes for the months before you owned the house (proration at closing) — definitional, no figure. |
| r2 | reel | seller_education | `checklist`: five things a homeowner can line up now so the house is ready to go on the market after the holidays. **The day's feed questionnaire**, built to be saved, and the seasonality row (§4, the January listing wave). **Not "should I wait until spring" — that is burned.** No figure, no fetch. |
| s1 | story | seller_education | `quiz` teaser for `r2`, answered by DM. **The story questionnaire.** |
| s2 | story | buyer_education | `explainer`: what a home warranty actually covers, and what it doesn't. **The day's education piece.** No figure, no fetch. Describe coverage in general terms — **never name a provider or quote a price.** |

### Wed Nov 25 — Spotlight day. **The `process` yields; `s2` carries the education piece.**

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | market_update | `stat`: **sales fell year over year in all four Southern California counties in October 2026** — Los Angeles −17.5%, Orange −20.7%, Riverside −21.4%, San Bernardino −12.5%. C.A.R. October 2026 county table via `ca_cities.json`, **no fetch**. Period on the graphic. The statewide version of this never published (it was the missed Nov 19 post), so the county cut is both fresh and the first time Memo's feed carries the October report at all. **Fewer sales is what happened; say nothing about what comes next.** **The day's directive `stat`.** |
| r1 | reel | agent_attraction | `spotlight` **#10: Power Wednesday** — what the weekly session is and what an agent gets out of showing up. **⚠ the day's one fetch, and it must be an official Epique page read the same day** (joinepique.com, epiquerealty.com, or the current ICA). Say which source you are quoting — joinepique.com's description of a program and the agreement's definition can differ. **No income language, no "you'll earn", "subject to plan terms" on anything plan-related, never run down another brokerage.** Speaks to **all licensed agents, wherever licensed** — not "SoCal agents". CTA `MATH`. Log to `spotlight-log.csv`. **If no Epique page loads, drop it and write nothing from memory.** **Never the row that yields.** |
| r2 | reel | investment | `quiz`: what an appraisal on a 2–4 unit looks at that a single-family appraisal doesn't — the rent schedule. **The day's feed questionnaire.** Definitional, no figure, no fetch. Any example is labelled an example and "not a loan offer". |
| s1 | story | investment | `quiz` teaser for `r2`. **The story questionnaire.** Qualifier in **`subhead`**. |
| s2 | story | seller_education | `compare`: an appraisal and a CMA — two numbers that answer two different questions. **The day's education piece**, riding a story because the `process` and the Spotlight both have claims on the feed. Both columns carry their real limits and **no number is called the "right" one**; values are "estimates, not an appraisal". No fetch. |

### Thu Nov 26 — Thanksgiving. The sphere and the family conversation. **The `process` yields and the day is deliberately light.**

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | market_update | `stat`: how few homes are actually for sale — **Long Beach had 599 active listings against 181,477 housing units** (about 1 in 300), Cerritos 42 against 16,343, El Segundo 23 against 7,889. Realtor.com **October 2026** active counts with Census **ACS 2020–2024** housing-unit counts, both via `ca_cities.json`, **no fetch**. **Both periods go on the graphic** — two sources, two dates. **Describe housing stock and nothing about who lives in any city.** **The day's directive `stat`.** |
| r1 | reel | community | `tip`: three house questions that are easier to ask while everyone is in one room — where the deed actually is, whether there's a trust, and who the successor trustee is. **The inheritor/trustee audience, which the playbook says to give two or more slots, and the right piece for the one day a year the family is together.** Gentle and procedural per §3 — not morbid, not a pitch. **"General information, not legal or tax advice. Ask your own attorney." in `subhead`, not only in `explain`** (see the §5 note below). **No statute cite, no tax figure, no dollar threshold.** **The day's education piece.** No fetch. |
| r2 | reel | community | `checklist`: do you know where these four are for your own house — the grant deed, the title policy, the insurance declaration page, the current mortgage statement. **The day's feed questionnaire**, built to be saved, and the sphere/past-client row. **Distinct from the Nov 16 "four documents a seller should find" (deed, tax bill, permits, HOA) — this one is for an owner who isn't selling.** No fetch. |
| s1 | story | community | `quiz` teaser for `r2`. **The story questionnaire.** |
| s2 | story | motivation | `quote` template. **The week's one and only `quote`.** Thanksgiving, clarity register: gratitude for the people who sent him business, and that knowing your number is what makes a decision possible. **No hype, no "manifest", no "grind", no hustle-porn.** |

### Fri Nov 27 — the week's 15-minute-call offer, moved off Thanksgiving. **All four requirements fit.**

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | market_update | `stat`: five-year change in typical home values — **Cypress +31.7%, Cerritos +29.2%, Torrance +20.0%, El Segundo +14.3%**. Zillow ZHVI through **Oct 31, 2026** via `ca_cities.json`, **no fetch**. Period on the graphic; describe ZHVI as a smoothed index of typical values and "estimates, not an appraisal". **The point is that neighbouring cities moved differently, not that any of them will keep moving.** **The day's directive `stat`.** |
| r1 | reel | seller_education | `process` ⚠: the supplemental property tax bill that shows up after you buy — why it comes, roughly when, and what to do with it. **The day's one fetch: an LA County Assessor or Treasurer-Tax Collector page read the same day.** Seasonality: the 2nd installment is Feb 1 (§4), so this is the right runway. **State no dollar figure, no rate and no deadline date unless the page loads** — describe the sequence and send people to their own CPA and the county. **"General information, not tax advice" in `subhead`.** **The day's `process`.** *No-fetch fallback:* `process` on who pays the property taxes for the months before you owned the house. |
| r2 | reel | buyer_education | `quiz`: why one large deposit on a bank statement can stall a loan, and the paper trail that fixes it. **The day's feed questionnaire.** **This is the day's client-facing feed piece and it carries the weekly offer: keep its own keyword CTA and add `cta_sub: tidycal.com/memorialdinh/15-minute-call`.** **Thursday is Thanksgiving, so the offer moves to Friday — and it rides a reel, not the 7pm post slot, because that is the slot the publisher missed on Nov 19 and the offer is load-bearing.** No `cta` template anywhere this week; the directive bans it and `cta_sub` is how the offer is met at this volume. No figure, no fetch. |
| s1 | story | buyer_education | `quiz` teaser for `r2`. **The story questionnaire.** Qualifier in **`subhead`**. |
| s2 | story | investment | `explainer`: vacancy rate and economic vacancy — two different numbers, and which one a lender cares about. **The day's education piece.** Any figure is a labelled example with its assumptions, **not a projection.** No fetch. |

### Sat Nov 28 — rate day, and the humor slot moves into a reel. **The `process` yields.**

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | buyer_education | `checklist`: five things to confirm about a condo before you write the offer — reserves, pending litigation, the rental cap, the master insurance policy, any special assessment. **The day's feed questionnaire**, built to be saved. **HOA dues and special assessments are burned as their own topics; this is the pre-offer document check, which is not.** No figure, no fetch. **If a `c1` carousel lands this day it replaces `p1`, the feed questionnaire is lost and only `s1`'s remains — say so in the report. The humor reel still does not yield.** |
| r1 | reel | market_update | `stat` ⚠: the Freddie Mac 30-year weekly average from the **newest** print, and what the week-over-week move does to the payment on **one labelled example loan**. **⚠ the day's one fetch — `globenewswire.com` first**, then `freddiemac.gcs-web.com/news-releases`, then `www.freddiemac.com/pmms`. **Thanksgiving week: do not state or assume a release day.** Put the as-of date the release itself carries in the `stat_label`. The PMMS scope sentence belongs on the piece (conventional, conforming, fully amortizing purchase loans, 20% down, excellent credit). State what happened; **never where it goes next.** The payment example states its assumptions and is **"not a loan offer"**. **If the print has not advanced past 7.28% (as of Nov 19, 2026), do not rerun it** — swap in the banked IRS capital-gains exclusion, or if nothing fetches, the banked `explainer` on what the title company does between offer and closing. **The day's directive `stat`.** |
| r2 | reel | humor | `meme`: every seller is certain that nobody is looking for a house over the holidays. **The week's one humor feed slot — and it is in a reel slot on purpose.** It has now been dropped **three Saturdays running** out of `p1`, because `p1` is where Memo's Canva carousel lands and the brief's precedence list puts humor 5th. A reel slot cannot be taken by a carousel. **Do not drop it, and do not move it back to `p1`.** It has the best save rate of any track in `insights.json`. The joke is on the process, Memo is the one gently roasted, and **Fair Housing applies to it exactly as to a listing** — nothing about who lives where or who can afford what. |
| s1 | story | market_update | `quiz` teaser for `r1`: which way the weekly average moved. **The story questionnaire.** **No bare figure without its as-of date on the graphic** — stories carry no caption, so the date has nowhere else to live. |
| s2 | story | buyer_education | `explainer`: what an HOA resale package is and the window you actually get to read it. **The day's education piece.** **No day count unless a C.A.R. or DRE page loads** — describe the right rather than the number. "General information, not legal advice" in `subhead`. No fetch. |

### Sun Nov 29 — Spotlight day, and nothing on it needs a fetch. **The `process` yields.**

| # | kind | track | angle |
|---|---|---|---|
| p1 | post | market_update | `stat`: two numbers for the same city, and they are not in conflict — **the Census put Long Beach's median home value at $806,600 (ACS 2020–2024 5-year estimates) while Zillow's index reads $854,209 as of Oct 31, 2026.** Both via `ca_cities.json`, **no fetch**. **Both periods on the graphic.** The point is that "what's my house worth" depends on which question you asked: a 5-year survey estimate and a smoothed current index measure different things, and **neither is an appraisal**. **The day's directive `stat`.** |
| r1 | reel | agent_attraction | `spotlight` **#11: the questions worth asking any brokerage before you sign** — Memo's own list, the one he'd want an agent to bring to him. **Describe only Memo's own list of questions and name no Epique program, benefit, perk or figure** — that is what makes this row writable with the fetch wall fully up, the same shape that worked for #9. **If it names any Epique program or number, that fact needs an official Epique page read the same day or it comes out.** No income language, no "you'll earn", **"subject to plan terms"** on anything plan-related, **never run down another brokerage** — the list is questions, not a comparison. Speaks to all licensed agents, wherever licensed. CTA `MATH`. Log to `spotlight-log.csv`. **Never the row that yields.** |
| r2 | reel | seller_education | `checklist`: three things to sort out when you inherit a house together with your siblings — who has authority, who is paying the carrying costs, and what everyone actually wants to do with it. **The day's feed questionnaire** and **the second inheritor/trustee piece of the week** (playbook §7 rule 2). Gentle and procedural. **"General information, not legal or tax advice. Ask your own attorney." in `subhead`.** **No statute cite, no tax figure, no dollar threshold.** No fetch. |
| s1 | story | seller_education | `quiz` teaser for `r2`, with the "not legal or tax advice" line in **`subhead`**. **The story questionnaire.** |
| s2 | story | buyer_education | `myth` template: that the listing agent has to tell you what the other offers came in at. **The day's education piece** and the week's one `myth` — the template has 7 lifetime uses and the rotation wants it. **Describe what a seller may and may not instruct, in general terms; no statute cite, no "always" or "never" about another agent's duty.** "General information, not legal advice" in `subhead`. No fetch. |

---

## Banked and checked fresh — use these when a ⚠ item can't be sourced

Run through `bot.seen` on Nov 22, 2026 and fresh. The first group needs no outside source at all,
which makes them the right substitutes on a walled run.

**No source needed:**
- Who pays the property taxes for the months before you owned the house (proration at closing). *(also the Tue and Fri `r1` fallback)*
- What the title company actually does between offer and closing. *(also the Sat rate-row fallback)*
- Why an appraiser and a tax assessor arrive at different values for the same house.
- What a reconveyance is, and why it matters after you pay off a mortgage.
- Myth: you need a perfect credit score to get a mortgage.
- What a lender's rent schedule (Form 1007) is and why it matters on a small multifamily. *(hold until the Wed Nov 25 2–4 unit appraisal quiz is more than 21 days old)*

**Needs one source:**
- **California down payment assistance for first-time buyers.** *(CalHFA — Tue Nov 24 `r1`. **Playbook §3 names assistance programs as what earns first-time buyers and this bot has still never run one.** If Tuesday's fetch fails, re-plan it rather than banking it indefinitely.)*
- 1031 exchange: the 45-day and 180-day clocks, and what "like kind" means. *(IRS — banked since Nov 3, still unused, still fresh)*
- The capital-gains exclusion when you sell your primary residence. *(IRS — the Sat Nov 28 rate-row swap)*
- Removing contingencies in California — the default window and what the day after means. *(C.A.R. or DRE; **do not state a day count without that source**)*
- Prop 19's base-year transfer for homeowners 55 and older. *(BOE or county assessor. The Nov 6 piece was the parent-to-child basics and the Nov 20 one was the claim window; the 55+ transfer is a third, different rule. **Disclaimer in `subhead`.**)*
- The C.A.R. 3Q 2026 affordability rows for **Los Angeles County and Orange County**. *(needs a third pass at `.../2026releases/3qtr2026HAI` at a higher offset — the Nov 16 fetch truncated before them)*
- **The 2027 conforming loan limits, once FHFA announces.** *(FHFA's own release only. See the ⚠⚠ note above — when it lands it takes that day's `p1` `stat`.)*

**Struck from the banked list:** *the share of homes selling above and below asking across his
cities.* It was banked as needing no source. **That is wrong** — `ca_cities.json` has no
sale-to-list field and `redfin` is `null` for every service city. It needs a Redfin Data Center
fetch, so it is a ⚠ item, not a fallback. *(Flagged in the Nov 23 note; confirmed here.)*

## Spotlight subjects — #10 and #11 this week, and what's left after

Series is at **#9** (what the first 30 days with Memo's team looks like, Sun Nov 22). **#9 was the
plan's #10** — Scribe renumbered correctly, because the plan's #9 (Power Wednesday, Wed Nov 18) was
dropped when no Epique page loaded and never published. This week uses **#10 Power Wednesday**
(Wed Nov 25, ⚠ fetch) and **#11 the questions worth asking any brokerage** (Sun Nov 29, no fetch).

**Burned, do not repeat within 30 days:** the AI toolkit, the brokerage comparison calculator, the
RevShare calculator, the team calculator, lead and marketing programs and the technology fee, stock
awards / Double Stock Award / Power Award / declining caps / 401(k), Power Coaching and Forever
Mentorship, CliqueOffers, Power Academy, transaction and compliance support, Power Summit, the cap
and fees after cap, agent benefits and health insurance, **and the first 30 days with Memo's team
(#9, Nov 22)**.

**Left unused after this week:** local meetups and culture, and **the Epique Asian Network** —
which is a real subject and fresh, but it is held back deliberately. It needs an official Epique
page read the same day, it must describe a professional network for agents and say **nothing about
anyone's national origin**, and it must never imply what languages Memo speaks (the playbook bans
claiming he speaks Vietnamese). Don't write it on a walled run. **The bench is now two subjects
deep — Mentor should plan one more Memo-own-cadence Spotlight (the shape of #9 and #11, which needs
no Epique fetch) rather than let the series stall again.**

## Burned — already covered, do not plan

On top of the list in CONTENT_BRIEF: price per square foot, "is the price negotiable", "price vs
terms vs timing on an offer", "should I wait until spring", HOA dues, rate locks, how co-buyers hold
title, **what a quitclaim deed does** (Oct 29), price bands and search filters, escrow week by week,
the seller net sheet, earnest money, discount points, the Homeowners' Exemption, special
assessments, the sell-first myth, the five numbers before a rental offer, 30-year vs 15-year, the
Nov 1 property tax installment **and the Dec 10 delinquency date** (both ran in the Oct 31 calendar
note), what a seller sees when an offer lands, the November calendar, owner's vs lender's title
insurance, days on market and what resets it, **median days on market across Long Beach's 11 ZIPs
(Nov 12)**, escalation clause vs a higher offer, the appraisal coming in under the purchase price,
the seller credit vs price reduction, contingent vs pending, **months of supply by SoCal county
(Nov 7)**, the Long Beach two-year ZHVI move, the Long Beach price-cut share, the median price per
square foot, what a lender verifies, cap rate vs cash-on-cash (Oct 27), **what happens if the buyer
backs out after contingencies are removed**, and everything in `queue/2026-11-02/` through
`queue/2026-11-23/` — which now includes the rent-back comparison, gift funds, the conforming-loan-
limit explainer, successor-trustee authority, the contingency-removal checklist, the lender credit,
why two agents price differently, backup offers, the preliminary title report, listing-agreement
terms, the self-employed document list, the past-client tips, the C.A.R. 3Q affordability LA Metro
row, lease-renewal pricing, the four documents a seller should find before listing, the
square-footage discrepancy, the ACS median-year-built row, rate vs APR, the seller disclosure
package, the repair-request process, the five things not to do before closing, the pending-share
row, **the C.A.R. October statewide median and sales pace (written Nov 19, never published — the
county cuts above are the replacement, not a rerun)**, the rent roll vs T-12, the cost of a vacant
month, gross rent multiplier, the date-of-death value, the new-vs-pending row, house hacking a 2–4
unit, the Nov 19 PMMS print and the $600k example payment, the Closing Disclosure check, the first
mortgage statement, PMI and the 80/78% rules, Spotlight #9, Mello-Roos, the condo-vs-house
affordability row, solar panel verification, lining up homeowners insurance, and the asking-rent
year-over-year row.
