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

Updated by Mentor from `data/insights.json` each week. As of Oct 25, 2026:

- **Reels beat static posts** — 4.3% vs 3.2% engagement rate over 60 days.
- **Instagram beats Facebook ~2.5×** — 4.1% vs 1.3%. Facebook is worth posting, not worth optimising.
- **Best hours**: Instagram ~9am and ~9pm; Facebook ~12pm and 8–9pm. Varies by weekday — the
  schedule is learned, not fixed.
- **His personal content outperforms everything the bot can make.** The fitness and weight-loss
  journey, showing days, escrow wins, family. ~80% skip rate on polished recruiting graphics by
  contrast. **The bot cannot produce this — it needs his camera.** Educational content is the
  reliable floor; his own footage is the ceiling. Mentor should remind him of this, specifically,
  when a week looks flat.
- **Saves and shares matter more than likes** for reach. Build at least one piece a week to be
  saved: a checklist, a number worth keeping, a comparison.

## 7. Standing rules for Mentor

1. Never plan a topic without running `python -m bot.seen`. His real history is ~200 posts back to
   May 2026 in `data/posts.csv`, which predates this bot.
2. Balance the week across audiences in section 3 — not five buyer posts in a row.
3. Keep one meme most days and roughly two motivational pieces a week.
4. Put anything needing fresh rates on Thursday.
5. When the data contradicts this playbook, the data wins — and update this file to say so.
