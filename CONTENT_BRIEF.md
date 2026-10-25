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

## Research — every run
1. Read `data/insights.json` (what's working) and `data/best_times.json`. Lean into the tracks and
   formats with the best engagement; rework the weakest.
   Read `knowledge/faq-topics.md`: the real questions followers asked this week. Turn at least one into a
   post or reel each day ("You asked: …"). Never name or quote the person who asked.
2. Research what's new, preferring: **CAR.org, Zillow Research, Realtor.com, Homes.com, Freddie Mac
   (PMMS rates), California DRE, CA Legislative Information (leginfo.legislature.ca.gov), HUD, CFPB,
   US Census, county assessor/recorder sites**.
3. Save a short dated summary to `knowledge/market-notes/YYYY-MM-DD.md` (what changed, numbers with
   source + date). This is the bot's growing memory of the market. Re-read the last 7 notes before writing.
4. Append each topic used to `knowledge/topic-log.csv` (`date,item,track,topic`).

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
