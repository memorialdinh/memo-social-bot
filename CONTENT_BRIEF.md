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
- Mix at least 1 agent-attraction piece per day and at least 1 buyer or seller education piece.
- End most CTAs with a keyword the engagement bot answers automatically: RATES, BUYER, SELLER, VALUE,
  PROP 19, AGREEMENT, MATH (agents), INVEST, BDAY. Example: "Comment VALUE and I'll DM you". The bot then DMs the resource.
- Once a week, a story invites people to the Birthday Club: "DM BDAY 🎂".
- If `queue/<date>/p0.yaml` already exists (the Birthday Club shoutout), leave it and write p1–p3 as usual.

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
  template: tip        # tip (headline + points) | stat (big number) | myth (myth vs fact)
  kicker: BUYER TIP    # small label; defaults to the track label
  headline: "Pre-qualified is *not* pre-approved."   # *stars* = gold words. <= 9 words
  points: ["...", "..."]                 # tip: 2-4 points, <= 14 words each
  stat_value: "6.2%"                     # stat template
  stat_label: "30-yr fixed avg, Freddie Mac, Oct 23"
  myth: "..."                            # myth template
  fact: "..."
  cta: "DM 'BUYER' for my roadmap"       # <= 8 words
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
