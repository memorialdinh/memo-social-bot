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

## Voice
Direct, relatable, strategic, slightly punchy, educational. Professional but approachable and
energetic. Short sentences. Sounds like a person, not a brand. No hype, no fluff, no corporate
filler, no "In today's market…" openers, no em-dash pileups. One idea per post.

## Daily output (write it for TOMORROW's date)
Folder: `queue/YYYY-MM-DD/` — one YAML file per item.

| Item | Count | Platforms |
|---|---|---|
| Feed posts `p1`–`p3` | 3 | Instagram, Facebook, LinkedIn, TikTok (animated) |
| Reels `r1`–`r2` | 2 | Instagram, Facebook, LinkedIn, TikTok |
| Stories `s1`–`s5` | 5 | Instagram, Facebook |

- Stories `s1`–`s3` match posts `p1`–`p3` (teaser, quiz or poll-style question for the same topic).
  `s4`–`s5` match the reels or are a quick tip / "this week in the market" stat.
- Same topic across platforms, but **every platform gets its own caption**:
  - **Instagram**: hook line, 2–4 short lines, a keyword CTA ("DM me 'RATES'"), 5–8 hashtags.
  - **Facebook**: conversational, a little longer, ends with a question or comment-CTA. 2–3 hashtags.
  - **LinkedIn**: professional angle. Agents and investors read here. Insight + takeaway + question. Exactly 3 hashtags.
  - **TikTok**: one punchy line + 4–5 hashtags (Memo pastes it when he publishes the draft).

  **Memo's website is appended automatically** — `theprestige.luxe` on client content,
  `joinmemo.netlify.app` on agent-attraction posts — placed above the hashtags. Don't write it into
  the caption yourself; you'll get it twice. Do still put a link inside the body when the post
  points at a specific page (`/net-sheet.html`, a `learn-*.html` article), since that's a different
  destination from the homepage.

  **Every feed caption on every platform gets hashtags — none of these are optional.** Match them to
  the platform: Instagram and Facebook lean local (#LongBeachRealEstate, #SouthBayHomes); LinkedIn
  stays professional and broad (#RealEstate, #HousingMarket); TikTok is lowercase and discovery-led
  (#firsttimehomebuyer, #realestatetips). Stories carry no caption, so no hashtags there.
- Rotate through the topic tracks in `config.yaml` using their weights. Check `knowledge/topic-log.csv`
  and don't repeat a topic used in the last 21 days.
- Mix at least 1 agent-attraction piece per day (a Spotlight — see below) and at least 1 buyer or seller education piece.
- End most CTAs with a keyword the engagement bot answers automatically: RATES, BUYER, SELLER, VALUE,
  PROP 19, AGREEMENT, MATH (agents), INVEST, BDAY. Example: "Comment VALUE and I'll DM you". The bot then DMs the resource.
- Once a week, a story invites people to the Birthday Club: "DM BDAY 🎂".
- If `queue/<date>/p0.yaml` already exists (the Birthday Club shoutout), leave it and write p1–p3 as usual.

## The mix Memo asked for — tips, education, process, questionnaires, CTA (Oct 28, 2026)

Memo wants "better design, luxury type, and more tips, education, process, questionnaire and CTA".
The renderer now has a luxury look (gold-foil type, hairline rules, his portrait medallion, a
"Your next step" button on every graphic) and a template for each of those. Use them:

**Every day, across the 10 pieces:**
- at least **1 process** piece (`process`: how something happens, step by step, in order)
- at least **1 questionnaire** (`checklist` or `quiz`) in the feed, and **2 of the 5 stories** are a
  `checklist` or `quiz` people answer by DM ("Reply BUYER if you checked 3+")
- at least **1 education** piece (`tip`, `explainer` or `compare`)
- **every item has `design.cta`** — the gold "Your next step" button. One action, ≤ 8 words, with an
  engagement keyword (RATES, BUYER, SELLER, VALUE, PROP 19, AGREEMENT, MATH, INVEST, BDAY) so the bot
  can answer it. If you leave it out, the track's default from `config.yaml → default_cta` is used.
- **once a week** (Mentor picks the day, or Wednesday if the plan doesn't say) one `cta` offer card:
  what someone gets on a 15-minute call, `cta: Book a 15-minute call`,
  `cta_sub: tidycal.com/memorialdinh/15-minute-call`. Captions still carry the keyword CTA too.
- never the same template twice in a row in the feed; rotate through all of them over the week
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
releases) and goes in `sources:`; if a figure can't be verified, describe the feature without it.
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
- Every number needs a source in the item's `sources:` list and must be current (say "as of <date>").
  If you can't verify it, don't use it.
- **Law posts** (`track: laws_and_updates`): cite the official source (bill page, DRE, HUD). They
  always wait for Memo's approval. Explain what changed; never give legal advice.
- No guarantees, no predictions stated as fact ("prices will…", "rates will…"), no "best agent / #1".
- Fair Housing: describe properties and areas, never the people who should live there. No
  "perfect for families", "safe neighborhood", "exclusive community", or anything about race,
  religion, national origin, sex, disability, familial status, etc.
- Agent-attraction posts: no income promises. Revenue share/equity mentions must say "subject to plan terms".
- The bot adds the DRE/Epique/Equal Housing footer to captions and graphics automatically.
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
  instagram: |-
    ...
  facebook: |-
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
