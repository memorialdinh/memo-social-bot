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
- **Never claim**: deal counts, "100+", sales volume, that Memo speaks Vietnamese, or his schools
  and degree.
- Values are "estimates, not an appraisal". Payment examples state their assumptions and are "not a
  loan offer".

## 6. What actually works, from Memo's own numbers

Updated by Mentor from `data/insights.json` and `data/posts.csv` each week. **As of Nov 1, 2026.**

- **The whole account is reach-starved, and that is the finding that explains every other one.**
  Oct 26–Nov 1: 87 published rows, **2,101 total reach, 39 engagements, 1 save, 0 shares** across
  both platforms for the entire week. Treat almost every per-template and per-track 0.0% in
  `insights.json` as a reach reading, not a content reading.
- **Memo's own camera content is not competing with the bot — it is in a different league.**
  Same week: his **24 untagged rows took 35 of the week's 39 engagements**; the bot's **63 tagged
  rows took 4.** His top two were a no-caption post (11 engagements, 105 reach, 10.5%) and a family
  reel (9 engagements). The fitness journey, showing days, escrow wins, family. **The bot cannot
  make this — it needs his camera.** Educational content is the reliable floor; his footage is the
  ceiling. Say so when a week looks flat.
- **Reels beat posts beat stories, confirmed again.** Oct 26–Nov 1 engagements per item:
  reels **1.39**, posts **0.28**, stories **0.10**. Over 60 days `kind:reel` is 3.5% against 1.5%
  for static posts. The 3-reels-2-posts directive has evidence behind it; apply it.
- **Facebook is finished as a reach channel.** Oct 26–Nov 1: **27 posts, 8 total reach, 0
  engagements** — down from the 15-posts/65-reach week recorded Oct 25. `best_times.json` won't
  even rank it (median reach 2 over 133 posts). Keep posting, never optimise, never spend a second
  caption pass on it.
- **Follower counts are not the signal here.** Instagram 817 → 815 across the week. Facebook
  217 → **288 (+71)** while Facebook reach stayed at ~0 — recorded as a fact, not explained, and
  **not to be cited as growth** in any content or report.
- **`quote` is not a reach problem, and the directive that banned it was reading noise.** Last
  week's two `quote` posts took the **highest and eighth-highest reach of all 51 bot items** (66
  and 47) on zero engagement. On an account where almost nothing earns an engagement, a 0.0%
  engagement rate cannot distinguish templates. *Changed Nov 1: the motivational register is
  restored to the plan at two `quote` pieces a week.*
- **The queue is written TWO days ahead of publication, not one.** Three commits confirm it:
  Oct 29 eve → Oct 31, Oct 30 eve → Nov 1, Oct 31 eve → Nov 2. This has two consequences, and
  both are now in the plan: a Mon–Sat plan starves Scribe of a row on two nights a week (extend it
  through Sunday), and **the fresh-rate piece belongs on Saturday** — see §7 rule 4.
- **One fetch per day, and give it to the item that has a same-day rule.** Four consecutive Scribe
  runs got exactly **one** successful web fetch — the first of the run — then `PROVENANCE_REQUIRED`
  on every later domain, because an unattended run has nobody to answer the permission prompt.
  Plan at most one source-dependent item a day and make everything else evergreen. **This is an
  operator fix** — pre-approving the brief's named source domains would end it — and it has now
  cost two Spotlights and three topics outright.
- **The dateless-figure defect has not recurred.** Every graphic published Oct 26–Nov 1 that
  carried a market figure carried its period on the graphic. The Oct 25 failure (a p2 graphic and
  an s4 story with bare numbers) is fixed. Keep the sweep in every run.
- **There is still no track, template or theme finding, and Mentor must not invent one.** 99
  historical rows sit in `track:untagged` with an empty `track` column; the tagged tracks all read
  at or near 0.0% on 1–16 posts. Until a track has 4+ posts *and* the account has reach worth
  measuring, "this track works" is not a finding. Say the data is thin instead. The recurring
  "write an extra Untagged piece" directive is an artifact of this bucket, not an instruction that
  can be followed — it needs the analytics job to exclude `track:untagged`.

## 7. Standing rules for Mentor

1. Never plan a topic without running `python -m bot.seen`. His real history is ~200 posts back to
   May 2026 in `data/posts.csv`, which predates this bot.
2. Balance the week across audiences in section 3 — not five buyer posts in a row.
3. Keep one meme most days and roughly two motivational pieces a week.
4. **The fresh-rate piece goes on SATURDAY.** PMMS publishes Thursdays at noon ET. The Oct 28
   correction moved the rate row off Thursday to Friday on the belief that Scribe writes the night
   before; **measured Nov 1, it writes two days before** (§6), so Friday's queue is written
   Wednesday evening — still ahead of the print. Saturday's queue is written Thursday evening,
   after it. If the print hasn't advanced, don't rerun last week's number: the brief only permits
   repeating a rate update that "carries a new weekly number." Swap in a banked topic instead.
5. When the data contradicts this playbook, the data wins — and update this file to say so.
6. **Memo's format ask (Oct 28, 2026): "more tips, education, process, questionnaire and CTA",
   in a more luxury design.** Plan every day with at least one `process` piece, one questionnaire
   (`checklist` or `quiz`), one education piece (`tip`, `explainer` or `compare`), and a clear
   next step on everything. One `cta` offer card a week (the 15-minute call). Name the template in
   the angle column when it matters (e.g. "`process`: escrow, day 1 to keys"). CONTENT_BRIEF.md has
   the fields for each. Judge the new templates on saves and DMs, not likes, once 4+ of each exist.
   **Nov 1, 2026:** when a directive tells Scribe to stop using `checklist`, meet the daily
   questionnaire with a `quiz` instead. That satisfies Memo's ask and the directive at once, and it
   costs nothing — last week `quiz` and `checklist` both earned zero engagements, on 118 and 82
   reach respectively. Never drop the questionnaire itself to satisfy a template directive.
8. **Plan one source-dependent item a day, maximum**, and give that slot to whatever has a hard
   same-day rule — the Spotlight, or the rate piece. Mark it in the plan. Everything else should be
   writable with the fetch wall up. See §6.
7. **Agent attraction = a Spotlight series (Memo, Oct 28, 2026).** Every `agent_attraction` piece
   uses `template: spotlight` and spotlights ONE thing: a perk, a tool, a training, a support line,
   a cost line, an event, or (only with their written OK) an agent. Rotate through the list in
   CONTENT_BRIEF.md and don't repeat a subject within 30 days (`knowledge/spotlight-log.csv`).
