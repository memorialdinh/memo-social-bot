# Content Brief — rules for the daily writer bot

This file is read by the Claude scheduled task that researches the market and writes
tomorrow's queue every evening. Edit it any time to change what gets written.

## Who this is for
**Memo Dinh** — Real Estate Consultant & Area Leader, Prestige Luxury Group | Epique Realty,
DRE #02066757. Southern California native. MBA, CSU Long Beach. $26M+ in residential sales volume,
largest deal ~$2.6M, 35+ agents mentored.

- Never claim "100+ deals" or any deal count.
- Never say Memo speaks Vietnamese.
- Service areas: Lakewood, Long Beach, Gardena, Torrance, Redondo Beach, El Segundo, Cypress,
  Cerritos, all of LA, Orange, Riverside and San Bernardino counties.
- Buyer/seller CTAs point to theprestige.luxe or DMs. Agent CTAs point to joinmemo.netlify.app or DMs.
- Agent-attraction content speaks to ALL licensed agents, not only Southern California agents (Memo, Nov 3 2026): Epique sponsorship works wherever an agent is licensed. Don't write "SoCal agents" in agent posts.

## Voice
Direct, relatable, strategic, slightly punchy, educational. Professional but approachable and
energetic. Short sentences. Sounds like a person, not a brand. No hype, no fluff, no corporate
filler, no "In today's market…" openers, no em-dash pileups. One idea per post.

## STOP LIST — performance cut (Memo, Nov 27, 2026: "the ones that don't [get views and engagement], stop it")
This overrides everything below where it conflicts, including the mix and template rotation sections.
Based on Instagram results Oct 20 – Nov 26, 2026, these kind + template combinations got **zero**
likes, comments, saves or shares across all their posts. Do not write them until Memo says otherwise:
- **Stories:** no `checklist`, `stat`, `process`, `spotlight`, `myth` stories. Stories use only `quiz`,
  `tip`, `quote`, `explainer` (explainer only with a DM keyword CTA) or a carousel/reel teaser.
- **Reels:** no `checklist`, `explainer`, `compare` reels. Prefer `meme`, `myth`, `spotlight`,
  `stat`, `process`, `tip`.
- **Feed posts (p1/p2 fallback slots):** no `spotlight`, `quote`, `cta`, `explainer`, `checklist`,
  `quiz` posts. Prefer `meme`, `myth`, `stat`, `compare`, `process`, `tip`.
- **Agent-attraction spotlights** move to reels only (`kind: reel`, `template: spotlight`), never a
  feed post or story. Keep the Wed/Sun Spotlight on `r1` or `r2`.
- The weekly 15-minute offer still runs; put it in a reel or a `tip`/`process` caption CTA, not a `cta` template.
- Canva carousels are the best-performing bot format (about 6x the engagement of other bot posts);
  the "Canva carousel" task now makes three a day (c1/c2/c3), so on those days write only r1, r2, s1, s2.
In your report, say "Stop list applied". Re-check monthly: if a format on the stop list is asked
for by an `insights.json` directive, skip it anyway and note it.

## Daily output (write it for TOMORROW's date)
Folder: `queue/YYYY-MM-DD/` — one YAML file per item.

| Item | Count | Platforms |
|---|---|---|
| Feed posts `p1`–`p2` | 2 | Instagram, Facebook, LinkedIn, TikTok (animated) |
| Reels `r1`–`r3` | 3 | Instagram, Facebook, LinkedIn, TikTok |
| Stories `s1`–`s2` | 2 | Instagram, Facebook |

**Memo raised the volume on Nov 25, 2026: "from now on post at 7am and 12pm too"** (he chose
"add 2 posts, 5 a day"). So the day is now **5 feed items + 2 stories**: the earlier 3 feed items
(`p1`, `r1`, `r2`, timed automatically) **plus two fixed-time slots**:
- **`p2` with `time: "07:05"`** (7am; static posts do well 5-8am on this account)
- **`r3` with `time: "12:05"`** (noon; reels peak 9am-12pm)
Always write both, with exactly those `time` values, so they go out at 7am and 12pm. Wherever this
brief or the playbook/week plan says "3 feed items", read **5**: the cap below is now 5 feed
items + 2 stories, and the precedence list for "3 slots" now has 5 slots (fill the extra two from
the next items on that list). This paragraph overrides the Nov 12 text below where they conflict.

**Memo, Nov 25, 2026 (later the same day): "start posting these style 3 time a day starting at 7am"** — the
Canva carousels, three a day, **replacing** other feed items (he chose "replace", not "add"). From
**Thu Nov 26, 2026** every day has three Canva carousels, made by the "Canva carousel" scheduled task:
- **`c1` at `time: "07:05"`, `c2` at `time: "12:05"`, `c3` at `time: "17:05"`** — Instagram, Facebook, LinkedIn.
- When `queue/<date>/c1.yaml` (or c2/c3) exists, the daily writer writes **no `p1`, no `p2` and no `r3`**.
  It writes only **`r1`, `r2` (auto-timed reels, TikTok too) and `s1`, `s2`**. The day is then
  **5 feed items (3 carousels + 2 reels) + 2 stories**. Don't repeat any carousel's topic in the reels;
  `s1` can tease a carousel ("Swipe through today's post 👉").
- The daily requirements (process, questionnaire, education, weekly 15-minute offer) ride the reels and
  stories on carousel days; the carousels themselves are step-by-step education with a keyword CTA and
  the "Book 15 minutes" button. The Wed/Sun Spotlight takes `r1` or `r2`.
- If a carousel is missing for a day (the task failed), fall back to the Nov 25 cadence above for the
  missing slots: `p2` at 07:05 for a missing `c1`, `r3` at 12:05 for a missing `c2`, `p1` for a missing `c3`.
This paragraph overrides the Nov 25 paragraph above and the "Canva carousels (Nov 18)" bullet below where they conflict.

**Memo cut the volume on Nov 12, 2026:** "Slow down on posting on my social media, I
think 3 a day is good." So the day is **3 feed items + 2 stories**, down from 10 pieces.
The feed is reel-weighted on purpose — reels out-earn static posts by a wide margin on
this account, and static posts are the weakest format Memo publishes (playbook §6).
**This cap is a hard ceiling. It beats the `insights.json` directives on VOLUME** — a
directive that says "write 3 reels and 2 posts" now means *weight the 3 feed slots toward
reels*, not write 5. Directives still govern the mix, the templates and the tracks inside
the cap. If a directive cannot be honoured without exceeding 3 feed items, say so in the
report rather than going over.

- Stories: `s1` teases a feed item (teaser, quiz or poll-style question for the same topic);
  `s2` carries whatever the feed had no room for — the day's education piece, or a quick tip /
  "this week in the market" stat.
- Same topic across platforms, **three captions, not four** (changed Nov 12 2026 — see the
  Facebook note below):
  - **`captions.default`** — the Instagram caption, and **Facebook reads this same text**. Hook
    line, 2–4 short lines, a keyword CTA ("DM me 'RATES'"), 5–8 local hashtags.
  - **`captions.linkedin`**: professional angle. Agents and investors read here. Insight + takeaway + question. Exactly 3 hashtags.
  - **`captions.tiktok`**: one punchy line + 4–5 hashtags (Memo pastes it when he publishes the draft).
  - Write `captions.instagram` **only** when a piece genuinely needs to read differently on
    Instagram than on Facebook. Normally it should not exist, and `default` does both.

  **No separate Facebook caption. Decided Nov 12 2026.** Facebook stays switched on — the page
  should look alive to a past client who looks Memo up — but it stops earning its own writing
  pass. Nov 2–8: **36 Facebook rows, 5 total reach, 0 engagements**, and `best_times.json` ranks
  Instagram only. Playbook §6 has said "never spend a second caption pass on it" for weeks; this
  is the brief finally matching it. `bot/common.py → caption()` falls back to `captions.default`,
  so Facebook gets the Instagram text with its own `/fb` tracked link. If Facebook reach ever
  recovers, bring the bespoke caption back.

  **Memo's website is appended automatically** as a short tracked link (theprestige.luxe/ig, /fb, /li, /tt, or the same on joinmemo.netlify.app) so analytics shows which platform sent each visitor; — `theprestige.luxe` on client content,
  `joinmemo.netlify.app` on agent-attraction posts — placed above the hashtags. Don't write it into
  the caption yourself; you'll get it twice. Do still put a link inside the body when the post
  points at a specific page (`/net-sheet.html`, a `learn-*.html` article), since that's a different
  destination from the homepage.

  **Every feed caption gets hashtags — none of these are optional.** Match them to the platform:
  `default` (Instagram and Facebook) leans local (#LongBeachRealEstate, #SouthBayHomes); LinkedIn
  stays professional and broad (#RealEstate, #HousingMarket); TikTok is lowercase and discovery-led
  (#firsttimehomebuyer, #realestatetips). Stories carry no caption, so no hashtags there.
- Rotate through the topic tracks in `config.yaml` using their weights. Check `knowledge/topic-log.csv`
  and don't repeat a topic used in the last 21 days.
- **Two agent-attraction Spotlights a week — Wednesday and Sunday — and they take a reel slot.**
  Decided Nov 12 2026 with the volume cut (Memo: "You tell me what's best"). Not one a day: at 3
  feed items, a daily Spotlight would be a third of everything Memo publishes, aimed at one of the
  six audiences in playbook §3. Fixed days so the series is plannable and doesn't get dropped as
  the row no directive protects. A reel slot rather than the single post slot, because reels
  out-earn static posts and the post slot is wanted for the day's process or education piece.
  Spotlights are also the most fetch-dependent content in the brief — every fact needs a same-day
  official Epique source — so two a week also means two runs a week that can be blocked by the
  fetch wall instead of seven. Plus at least 1 buyer or seller education piece a day.
- End most CTAs with a keyword the engagement bot answers automatically: RATES, BUYER, SELLER, VALUE,
  PROP 19, AGREEMENT, MATH (agents), INVEST, BDAY. Example: "Comment VALUE and I'll DM you". The bot then DMs the resource.
- Once a week, a story invites people to the Birthday Club: "DM BDAY 🎂".
- **Website campaign, Oct 29 – Nov 11, 2026 (Memo asked Oct 28):** every day in that range already has
  `w1.yaml` (a feed post driving people to theprestige.luxe or joinmemo) and `s5.yaml` (its story).
  Leave both alone. Write p1–p3, r1–r2 and **s1–s4 only** on those days (5 stories total, as usual).
  Don't repeat a w1 topic in p1–p3 that same week.
- If `queue/<date>/p0.yaml` already exists (the Birthday Club shoutout), leave it and write p1–p3 as usual.
- **Canva carousels (Memo, Nov 18 2026: "add this into my social media daily post").** If
  `queue/<date>/c1.yaml` exists, it is a 4-slide carousel Memo designed in Canva and approved. It
  **is that day's post slot**: leave it alone, write **no p1**, and fill the rest of the day with
  r1–r3, p2 and s1–s2 as usual, so the day stays at 5 feed items (p2 at 07:05, r3 at 12:05). Don't repeat its topic in the reels,
  and let `s1` tease it ("Swipe through today's post 👉"). Carousels post to Instagram, Facebook and
  LinkedIn only; TikTok gets nothing from a carousel day beyond the reels.

## The mix Memo asked for — tips, education, process, questionnaires, CTA (Oct 28, 2026)

Memo wants "better design, luxury type, and more tips, education, process, questionnaire and CTA".
The renderer now has a luxury look (gold-foil type, hairline rules, his portrait medallion, a
"Your next step" button on every graphic) and a template for each of those. Use them:

**Every day, across the 5 pieces:**
- at least **1 process** piece (`process`: how something happens, step by step, in order)
- at least **1 questionnaire** (`checklist` or `quiz`) in the feed, and **1 of the 2 stories** is a
  `checklist` or `quiz` people answer by DM ("Reply BUYER if you checked 3+") — scaled down from
  "2 of 5" with the Nov 12 volume cut, same proportion
- at least **1 education** piece (`tip`, `explainer` or `compare`)
- **every item has `design.cta`** — the gold "Your next step" button. One action, ≤ 8 words, with an
  engagement keyword (RATES, BUYER, SELLER, VALUE, PROP 19, AGREEMENT, MATH, INVEST, BDAY) so the bot
  can answer it. If you leave it out, the track's default from `config.yaml → default_cta` is used.
- **The weekly 15-minute-call offer rides an existing piece — it no longer gets a slot of its own.**
  Changed Nov 12 2026. **Thursday**, on the day's client-facing feed piece: keep that piece's own
  keyword CTA and add `cta_sub: tidycal.com/memorialdinh/15-minute-call` underneath. Thursday so it
  misses the Wed/Sun Spotlight and Saturday humor. Why not a dedicated `cta` card any more: the
  standing directive bans the `cta` template (lowest reach-per-item of any template, playbook §6),
  the `w1` campaign post that hosted the offer Oct 29 – Nov 11 has ended, and at 3 feed items a day
  there is no spare slot. **Never drop the offer itself to satisfy the template directive** — that
  is the rule playbook §6 sets out, and `cta_sub` is how it's met at this volume.
- never the same template twice in a row in the feed; rotate through all of them over the week
- **Humor: one feed slot a week, on Saturday, plus stories whenever a story slot is free.**
  **`quote`: one a week, and it rides a story, not the feed.** Both changed Nov 12 2026 with the
  volume cut, down from "a meme most days and two `quote` pieces a week". The reasoning, because
  it decides the next close call too: **the three feed slots belong to what Memo actually asked
  for on Oct 28 — "more tips, education, process, questionnaire and CTA".** Humor and `quote` were
  never on that list. `quote` loses its feed slot first because it is the one template with reach
  but no conversion — playbook §6 has it at the highest reach-per-item of any template on *zero*
  engagements, so a feed slot spent on it is a slot that cannot produce a DM. Humor keeps one feed
  slot because it has the best save rate of any track (`insights.json`) and saves are what carry a
  post to new people, but one a week, not six. Both registers stay in the mix per playbook §2 —
  they just stop outbidding the educational floor.
- **What competes for 3 slots, in order.** Before the Nov 12 cut all of these fit in a 5-item
  feed: a `process`, a feed questionnaire, an education piece, the daily meme, two `quote` pieces,
  a `stat`, and a Spotlight. They no longer do. Precedence when they collide: (1) the day's
  questionnaire, (2) the `process` or education piece, (3) the `stat` a directive asks for,
  (4) the Wednesday/Sunday Spotlight, (5) Saturday humor, (6) the weekly `quote`.
  **A requirement that loses its feed slot rides a story where it can** (playbook §6) — and when
  it can't fit at all, drop it and name it in the report. Mentor still needs to rebalance the week
  plan to 3 feed rows a day; this cadence is what Scribe follows until then.
- `insights.json` directives still win (e.g. "stop using quote") — say which you applied

**Which template for what:**
| Template | Use it for | Saves? |
|---|---|---|
| `tip` | 3 things to do / avoid. 2-4 points (posts), up to 5 (stories) | yes |
| `process` | escrow timeline, how a sale closes, probate steps, 1031 sequence. 3-4 steps with detail (posts), up to 5 (reels/stories) | yes |
| `checklist` | "Ready to buy? Check yours." 3-5 yes/no questions + a `score` line | yes |
| `quiz` | one question, 2-4 options, `answer`. Posts ask (answer goes in the caption's last line or the next day's story with `reveal: true`); reels reveal it on screen automatically | — |
| `explainer` | one term in plain English: `term`, `definition`, `why`, `example` | yes |
| `compare` | A vs B: FHA vs conventional, sell first vs buy first, cap rate vs cash-on-cash | yes |
| `cta` | the offer card (see above) | — |
| `spotlight` | agent attraction: one perk / tool / person per post, numbered series (see below) | yes |
| `stat` / `myth` / `meme` / `quote` | as before | — |

**Looks never repeat.** The renderer picks each graphic's look (9 luxury color themes × 11
background accents × layout) so no platform reuses a look from its last 14 days of posts, two posts
in a row never share a color, and the same post looks different on each platform. Don't set
`design.theme` — forcing a theme takes that choice away. The look is saved in each item's
`rendered:` block; leave it alone.

**Agent attraction is a Spotlight series** (Memo, Oct 28, 2026: "for the agent attraction: spotlight
each…"). Every `agent_attraction` piece is `template: spotlight`, one subject per post, numbered:
```yaml
track: agent_attraction
design:
  template: spotlight
  kicker: EPIQUE SPOTLIGHT        # or AGENT SPOTLIGHT for a person
  series_no: 4                    # next number in knowledge/spotlight-log.csv
  headline: "Training that *doesn't* cost extra."
  subhead: "One line: what it is."
  points: ["What it means for the agent", "...", "..."]   # 2-4, concrete
  cta: "DM 'MATH' for the full breakdown"
  # fine_print is added automatically: "Subject to Epique's current plan terms and eligibility.
  # No income is guaranteed." Override with fine_print: only to make it MORE specific.
```
Rotate subjects, one per post, no repeat within 30 days: RevShare (plan terms), stock/equity awards
(plan terms), the cap and what counts toward it, fees after cap, Power Academy / training, Power
Wednesday, coaching and mentorship, transaction and compliance support, tech and AI tools, lead and
marketing programs, benefits, culture and events (Power Summit, local meetups), the Epique Asian
Network, what joining Memo's team looks like day to day. **Every fact comes from an official Epique
source the same day** (joinepique.com, ica.epiquerealty.com, epiquerealty.com, Epique's own press
releases, and the **current Independent Contractor Agreement** — see below) and goes in `sources:`;
if a figure can't be verified, describe the feature without it.

**The current ICA (Memo confirmed Nov 4, 2026).** The agreement published at
<https://docs.google.com/document/u/2/d/e/2PACX-1vTLyZL7y9zSbhwftfi6sBLK7brUGTC8RQ7vIQSe8LLTbyBGSsYhQ7g9VX1D0Vz16J95cr5yFXgidMUe/pub>
is marked **"Updated 02/26/2026"** and **supersedes the copy on ica.epiquerealty.com**, which is
marked "Updated 04/27/2025". Cite the newer one for contract terms; where the two disagree, the
newer one wins and the older one is not quoted alongside it. Two cautions that do not go away just
because the source is approved: (1) it is a **contract**, not marketing copy — joinepique.com's
description of a program and the agreement's definition of it can differ, so say which one you are
quoting; (2) its caps, fees, equity, Power Award and revenue-share figures are still bound by every
rule above — **no income promises, "subject to plan terms"** — and "the cap and fees after cap" is
already a burned Spotlight subject. Prefer the agreement for *what a thing is*, not for *what an
agent would earn*.
No income promises, no "you'll make", no comparisons that run down another brokerage.
**Agent spotlights (a real person)** need that agent's written OK: add `photo:
assets/spotlights/<file>.jpg` (Memo uploads it), `name:`, `role:` and `consent: <date they said
yes>`. The validator blocks a person spotlight without a photo file and a consent date. Never use a
photo from the web or from another post.
After writing, append `date,series_no,subject,source_url` to `knowledge/spotlight-log.csv`.

Graphics carry SHORT text. The validator warns past these: headline 9 words, a point 14, a
checklist question 12, a quiz option 8, a step 16, the CTA 8. The caption does the explaining.

## Memes — the `humor` track

Roughly one piece a day should be funny. Use `template: meme` with a `setup` line and a `punch`
line. The joke is the graphic, so skip `points`.

```yaml
design:
  template: meme
  kicker: REAL TALK
  headline: "Every buyer consult, *eventually*."
  setup: "Buyer: move-in ready, great location, under budget."
  punch: "Also buyer: *and a pool.*"
```

What's funny here is the **shared experience of the process** — wish lists versus budget, the
listing photo taken at a heroic angle, the inspection report that runs 48 pages, the buyer who
needs to "think about it" for nine months, Zestimates, the 3pm offer deadline. Memo is usually
the one being gently roasted, or in on the joke with the viewer.

**Hard rules for memes — these matter more here than anywhere:**
- **Original only.** Never recreate a known meme format's imagery, never a recognizable character,
  mascot or film still, never a celebrity's face. Typography and Memo's own headshot only.
- **Never joke about people, only about the process.** Nothing about who lives where, who can
  afford what, or any protected class — Fair Housing applies to a joke exactly as it does to a
  listing. No punching down at clients, other agents, or other brokerages.
- No hype, no fake stats as a punchline, no "guaranteed". A joke still can't claim anything untrue.
- The compliance badge and DRE footer stay on, same as every other graphic.
- If a joke needs explaining, or you're unsure it reads as kind, write a different one.

## Research — every run
0. **Read `knowledge/playbook.md` first** — the editorial brain: what this content is for, the four
   voice registers (educational, funny, motivational, empowering), the six audiences, seasonality,
   the compliance spine, and what Memo's own numbers say. Mentor maintains it. It overrides this
   brief where the two differ.
0a. **Then `knowledge/week-plan.md`** — the topic calendar. Mentor writes it Sunday afternoons and
   Memo edits it directly. Write tomorrow's row from that plan. Swap a topic only if real news
   breaks or `python -m bot.seen` flags it as already covered — and say so in your report. You no
   longer write the week plan yourself; Mentor owns it.
0b. **`data/insights.json` has a `directives` list. Those are not suggestions — do what they say.**
   They are generated from Memo's own last 60 days of results (saves, shares, reach, engagement by
   track, format, design template and theme). If a directive says to write two reels instead of
   one, or to stop using a template, follow it and say in your report which directives you applied.
1. Read the rest of `data/insights.json` (what's working) and `data/best_times.json`. Lean into the tracks and
   formats with the best engagement; rework the weakest.
   Read `knowledge/faq-topics.md`: the real questions followers asked this week. Turn at least one into a
   post or reel each day ("You asked: …"). Never name or quote the person who asked.
2. Research what's new, preferring: **CAR.org, Zillow Research, Realtor.com, Homes.com, Freddie Mac
   (PMMS rates), California DRE, CA Legislative Information (leginfo.legislature.ca.gov), HUD, CFPB,
   US Census, county assessor/recorder sites**.
3. Save a short dated summary to `knowledge/market-notes/YYYY-MM-DD.md` (what changed, numbers with
   source + date). This is the bot's growing memory of the market. Re-read the last 7 notes before writing.
4. Append each topic used to `knowledge/topic-log.csv` (`date,item,track,topic`).
5. **Check every topic against what Memo has ALREADY POSTED, not just what this bot wrote.**
   `knowledge/topic-log.csv` only covers this bot's own output, which started Oct 2026. His real
   history — roughly 200 posts back to May 2026 from the years he posted through Metricool — is in
   `data/posts.csv`, in the `caption` column. Read the captions from the **last 120 days** and skip
   any topic whose hook or core idea already appeared. A rate update with a new weekly number is
   fine to repeat; an evergreen explainer is not.
   **Run the checker — don't eyeball it:**
   ```
   python -m bot.seen "your topic here" "another topic"
   python -m bot.seen --plan          # checks every topic in week-plan.md
   ```
   It prints `fresh` or `ALREADY COVERED` with the matching post and date, and exits 1 on a hit.
   Run it on every topic BEFORE writing, and again on the week plan after you rewrite it on Sundays.
   Already covered in Oct 2026, so you can skip proposing these at all: pre-qualified vs
   pre-approved, Zestimate accuracy, ADUs, inherited/probate homes, open-house checklists, cheap
   pre-listing fixes, closing costs first-timers forget, "as-is" and disclosures, the 20%-down myth,
   rent-vs-own math, overpricing. A rate update carrying a new weekly number is fine to repeat.
   If `data/posts.csv` is missing, `bot.seen` exits 2 and says so — report that rather than
   assuming a topic is fresh.

## Facts & compliance (non-negotiable)
- **More detail, fact-checked, government sources first (Memo, Nov 27, 2026: "give more information
  details that is fact check from reliable source, mainly government website").** Every education
  piece carries at least one concrete, useful fact (a dollar limit, a deadline, a percentage, a form
  name, a rule) instead of general advice. Verify each fact today with WebFetch on the primary source,
  in this order: government sites (.gov / ca.gov / lacounty.gov / ocgov.com — e.g. IRS, HUD, CFPB,
  FHFA, VA, FHA/HUD handbook, Freddie Mac PMMS, CA BOE, CA FTB, CA DRE, CalHFA, CA Courts, LA County
  Assessor/Treasurer-Tax Collector, OC Assessor, city sites), then CAR.org, then Zillow/Realtor.com
  data pages. Blogs, news recaps, AI answers and other agents' posts never count as a source.
  Put the exact URL(s) in the item's `sources:` list and a short source tag on the graphic or in the
  caption ("Source: IRS.gov, 2026"). If a fact can't be verified on such a source today, leave it out.
- Every number needs a source in the item's `sources:` list and must be current (say "as of <date>").
  If you can't verify it, don't use it.
- **What's changing in 2027 (Memo, Nov 27, 2026: "details of what's changing, new law that's coming
  into effect in 2027, bill that has been passed but not approved yet").** Cover, with specifics:
  (1) laws taking effect in 2027 (California chaptered bills, mostly Jan 1, 2027; federal rules; LA/OC
  County and city ordinances) — what changes, who it affects, the effective date, what to do now;
  (2) bills that passed a vote but are NOT law yet (passed one house, waiting on the other house, the
  Governor/President, or a council's final vote). Always state the exact status in plain words
  ("Passed the Senate on <date>. Not law yet: still needs <next step>."), never call a pending bill a
  law, and never predict whether it will pass. Verify status and text on the official page the same
  day: leginfo.legislature.ca.gov (bill status/history and chaptered text), congress.gov, federalregister.gov,
  dre.ca.gov, hcd.ca.gov, ftb.ca.gov, boe.ca.gov, county/city clerk or council pages. CAR.org legal
  updates may point you to bills, but the bill page is the source. Put bill numbers (e.g. "AB 1234")
  and links in `sources:`. Reels and stories may tease a law item; the Canva carousel task carries the
  detailed version.
- **City by city, all of LA County and Orange County (Memo, Nov 27, 2026: "for each cities, in los
  angeles and orange county").** Local rules matter as much as state law: rent control / just-cause
  rules, rental registration, ADU and SB 9 rules, short-term rental bans, permit and inspection
  requirements, transfer taxes (e.g. City of LA Measure ULA), point-of-sale requirements, local
  homebuyer programs. Cover each city in turn (88 LA County cities + unincorporated LA County, 34 OC
  cities + unincorporated OC), starting with his service areas (Lakewood, Long Beach, Gardena,
  Torrance, Redondo Beach, El Segundo, Cypress, Cerritos). Source: the city's own site, municipal
  code, council agendas/minutes, or the county site. Log covered cities in knowledge/city-log.csv.
- **Coming soon in his cities (Memo, Nov 27, 2026: "post anything that are developing soon in the
  cities"). Track `coming_soon`.** New housing developments, mixed-use projects, retail and
  restaurants, parks, schools under construction, transit and road projects (e.g. LA Metro lines,
  station openings), civic projects, approved specific plans, in LA County and OC cities, service
  areas first. Source only official pages: the city's planning/community development "current
  projects" or "major development" list, planning commission and council agendas/staff reports,
  LA Metro / OCTA / Caltrans project pages, county pages, or the developer's own project site for
  details the city has already approved. State the exact status in plain words ("Approved by the
  Planning Commission <date>", "Under construction, city lists completion as <date>", "Proposed,
  public hearing <date>") and never present a proposal as certain. Never say a project will raise
  (or lower) home values, and never describe who the project is "for". Log projects in
  knowledge/development-log.csv (date, city, project, status, url) and update status when it changes.
- **Law posts** (`track: laws_and_updates`): cite the official source (bill page, DRE, HUD). Since
  Nov 27, 2026 they post automatically (Memo chose auto-post), so the facts check must be airtight. Explain what changed; never give legal advice.
- No guarantees, no predictions stated as fact ("prices will…", "rates will…"), no "best agent / #1".
- Fair Housing: describe properties and areas, never the people who should live there. No
  "perfect for families", "safe neighborhood", "exclusive community", or anything about race,
  religion, national origin, sex, disability, familial status, etc.
- Agent-attraction posts: no income promises. Revenue share/equity mentions must say "subject to plan terms".
- The bot adds the DRE/Epique/Equal Housing footer to captions and graphics automatically.
- **Always a disclaimer (Memo, Nov 27, 2026: "always add disclaimer to protect me").** Every caption
  gets the full footer from config.yaml automatically (general information only, not legal/tax/
  financial/lending advice, believed accurate as of posting, verify with the official source and a
  licensed professional). Every graphic, story, reel end card and carousel's last slide also shows a
  short on-image line: "General info only, not legal, tax or lending advice. Info as of <Mon YYYY>."
  Never remove or shorten it, never imply a guarantee, and never write anything that reads as
  advice to a specific person.
- `python -m bot.validate` must pass before pushing.

## YAML format
```yaml
id: p1                 # p1-p3 posts, r1-r2 reels, s1-s5 stories
kind: post             # post | reel | story
track: buyer_education # see config.yaml → tracks
topic: Pre-qualified vs pre-approved
time: auto             # or "09:30" to force a time
design:                # what's printed on the graphic (keep it SHORT)
  template: tip        # tip | process | checklist | quiz | explainer | compare | cta | spotlight | stat | myth | meme | quote
  kicker: BUYER TIP    # small label; defaults to the track label
  headline: "Pre-qualified is *not* pre-approved."   # *stars* = gold words. <= 9 words
  subhead: "..."                         # optional one-line dek under the headline
  points: ["...", "..."]                 # tip: 2-4 points, <= 14 words each
  stat_value: "6.2%"                     # stat template
  stat_label: "30-yr fixed avg, Freddie Mac, Oct 23"
  myth: "..."                            # myth template
  fact: "..."
  cta: "DM 'BUYER' for my roadmap"       # <= 8 words — EVERY item gets one
  cta_sub: "tidycal.com/memorialdinh/15-minute-call"   # optional small line under the button
captions:              # not needed for stories
  default: |-          # Instagram AND Facebook read this one
    ...
  linkedin: |-
    ...
  tiktok: "..."
sources: [https://...]
```
No emojis on the graphic itself (captions are fine).

### The new templates' fields
```yaml
# process — steps in order. "Title: detail" strings, or dicts with an optional when
design:
  template: process
  headline: "How a home sale actually *closes*."
  steps:
    - {when: "Week 1", title: "Price it right", detail: "Comps, condition and today's buyers set it."}
    - "Prep and photos: Small fixes first, then pro photos."
    - "Escrow: Inspection, appraisal and loan approval."
    - "Close: Docs record, funds wire, keys change hands."
  cta: "Comment 'SELLER' for my timeline"

# checklist — the questionnaire
design:
  template: checklist
  kicker: QUICK CHECK
  headline: "Ready to *buy*? Check yours."
  questions: ["I know my credit score.", "I have 2 months of statements ready.", "..."]
  score: "3 or more? You're *closer* than you think."
  cta: "DM 'BUYER' and I'll map your next step"

# quiz — reels reveal the answer; a story reveals it only with reveal: true
design:
  template: quiz
  kicker: POP QUIZ
  headline: "Who usually pays for the home *inspection*?"
  options: ["The seller", "The buyer", "The lender"]
  answer: B
  explain: "The buyer orders it during the contingency period."   # shown with the reveal
  reveal: false
  cta: "Comment A, B or C"

# explainer — one term, plain English
design:
  template: explainer
  kicker: REAL ESTATE 101
  headline: "Say it in *plain English*."
  term: "Contingency"
  pos: "noun · purchase contract"          # optional
  definition: "A condition in your offer that has to be met, or you can cancel and keep your deposit."
  why: "It's your safety net on the inspection, appraisal and loan."
  example: "Appraisal comes in low? That contingency lets you renegotiate or walk."
  cta: "DM 'BUYER' for my offer checklist"

# compare — A vs B
design:
  template: compare
  headline: "Sell first or *buy first*?"
  left:  {label: "Sell first", points: ["You know your exact budget", "No double payments"]}
  right: {label: "Buy first",  points: ["Move once, on your schedule", "Two payments for a while"]}
  verdict: "The right order comes down to your equity and how much overlap you can carry."
  cta: "Comment 'SELLER' for my plan"

# cta — the offer card, once a week
design:
  template: cta
  kicker: FOR HOMEOWNERS
  headline: "Selling in *2027*? Start with 15 minutes."
  points: ["Your home's value range today", "What to fix, and what to skip", "A timeline that fits your next move"]
  cta: "Book a 15-minute call"
  cta_sub: "tidycal.com/memorialdinh/15-minute-call"
```
Every number still needs its dated source — on the graphic too (a `stat_label`, a step's detail,
the `explain` line), not only in the caption.
